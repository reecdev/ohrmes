import argparse
import sys
import time

def serve():
    print("starting server..")
    from flask import Flask, request
    from flask_socketio import SocketIO, emit
    import transformers
    import torch
    from threading import Thread, Event

    app = Flask(__name__)
    socketio = SocketIO(app, async_mode="threading")

    model_cache = {}

    @socketio.on('get_device')
    def handle_get_device():
        device = "cuda" if torch.cuda.is_available() else "cpu"
        emit('device_response', {'device': device})

    @socketio.on('chat')
    def handle_chat(data):
        sid = request.sid

        model_name = data.get('model')
        messages = data.get('messages', [])

        if model_name not in model_cache:
            tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
            device_str = "cuda" if torch.cuda.is_available() else "cpu"
            model = transformers.AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.bfloat16 if device_str == "cuda" else torch.float32,
                trust_remote_code=True,
            ).to(device_str).eval()
            model_cache[model_name] = (tokenizer, model)
        else:
            tokenizer, model = model_cache[model_name]

        condition = "<|quad_end|><|object_ref_end|>"
        prompt = ""
        for msg in messages:
            if msg["role"] == "user":
                prompt += f"<|im_start|>{condition}{msg['content']}<|im_end|>"
            elif msg["role"] == "assistant":
                prompt += f"{msg['content']}<|im_end|>"

        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        inputs["token_type_ids"] = torch.ones_like(inputs["input_ids"])

        streamer = transformers.TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        stop_event = Event()

        generation_kwargs = dict(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            streamer=streamer,
        )

        @socketio.on('disconnect')
        def handle_disconnect():
            stop_event.set()

        def run_generation():
            thread = Thread(target=model.generate, kwargs=generation_kwargs)
            thread.start()

            for text in streamer:
                if stop_event.is_set():
                    for _ in streamer:
                        pass
                    break
                socketio.emit('token', {'text': text}, to=sid)
                time.sleep(0.001)

            if not stop_event.is_set():
                socketio.emit('done', to=sid)

        socketio.start_background_task(run_generation)

    socketio.run(app, port=6769)


def run_model(model_name: str):
    import socketio

    sio = socketio.Client()
    try:
        sio.connect('http://localhost:6769')

        state = {'generating': False, 'response': [], 'device': 'unknown'}

        @sio.on('device_response')
        def on_device(data):
            state['device'] = data['device']

        sio.emit('get_device')
        time.sleep(0.2)
        
        print(f"Running model {model_name} on {state['device']}")

        messages = []

        @sio.on('token')
        def on_token(data):
            text = data['text']
            state['response'].append(text)
            print(text, end="", flush=True)

        @sio.on('done')
        def on_done():
            print()
            messages.append({"role": "assistant", "content": "".join(state['response'])})
            state['response'].clear()
            state['generating'] = False

        while True:
            try:
                user_input = input(">> ")
            except (EOFError, KeyboardInterrupt):
                break

            if user_input.strip() == "/bye":
                print("quitting chat...")
                break
            elif user_input.strip() == "/clear":
                messages.clear()
                print("Cleared context.")
                continue

            messages.append({"role": "user", "content": user_input})
            state['generating'] = True
            sio.emit('chat', {'model': model_name, 'messages': messages})

            while state['generating']:
                time.sleep(0.01)

        sio.disconnect()
    except:
        print("halt! (did you forget to serve?)")


def main():
    parser = argparse.ArgumentParser(
        description="Ohrmes CLI"
    )

    parser.add_argument("--serve", action="store_true",
                        help="Serve Ohrmes")

    parser.add_argument("--run", type=str, metavar="MODEL",
                        help="Run a model. Requires server to be running")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.serve:
        serve()
        return

    if args.run:
        run_model(args.run)
        return

    parser.print_help()


if __name__ == "__main__":
    main()