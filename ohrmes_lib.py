import socketio
import time

def chat(model: str, messages: list, stream: bool = False):
    sio = socketio.Client()
    sio.connect('http://localhost:6769')

    state = {
        'generating': True,
        'chunks': [],
        'done': False
    }

    @sio.on('token')
    def on_token(data):
        text = data['text']
        chunk_data = {"message": {"role": "assistant", "content": text}, "done": False}
        if stream:
            state['chunks'].append(chunk_data)
        else:
            state['chunks'].append(text)

    @sio.on('done')
    def on_done():
        state['done'] = True
        if stream:
            state['chunks'].append({"message": {"role": "assistant", "content": ""}, "done": True})
        state['generating'] = False

    sio.emit('chat', {'model': model, 'messages': messages})

    if stream:
        def generator():
            try:
                while state['generating'] or state['chunks']:
                    if state['chunks']:
                        yield state['chunks'].pop(0)
                    else:
                        time.sleep(0.005)
            finally:
                sio.disconnect()
        return generator()
    else:
        while state['generating']:
            time.sleep(0.005)
        sio.disconnect()
        full_content = "".join(state['chunks'])
        return {"message": {"role": "assistant", "content": full_content}, "done": True}