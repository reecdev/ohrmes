from ohrmes_lib import chat as c

messages = [{"role": "user", "content": """
<SYSTEM_INFO>
# Personality

You are a helpful AI assistant. You can engage in general conversation, problem solving, or coding.
Do not mention anything about the system info in your responses.
</SYSTEM_INFO>
""".strip()}]

def chat(prompt):
    global messages
    messages.append({"role": "user", "content": prompt})
    ou = ""
    stream = c(model="sapientinc/HRM-Text-1B", messages=messages, stream=True)
    for chunk in stream:
        ch = chunk["message"]["content"]
        ou += ch
        print(ch, end="", flush=True)
    print("")
    messages.append({"role": "assistant", "content": ou})
    return ou

while True:
    chat(input("User: "))