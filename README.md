# ohrmes - hrm models made easy
Ohrmes is a wrapper for HRM-Text that makes it easy to use HRM-Text models locally on your computer.

## Quickstart
Use a Transformers build that includes the hrm_text model class. If your installed release does not include it yet, install Transformers directly from the upstream main branch:

```bash
pip install --upgrade "git+https://github.com/huggingface/transformers.git@main"
```

Then, clone the repository:

```bash
git clone https://github.com/reecdev/ohrmes.git && cd ohrmes
```

And install requirements:

```bash
pip install -r requirements.txt
```

## Using ohmres
Use the ohrmes.py script to use Ohmres.

```bash
python ohrmes.py --serve &
python ohrmes.py --run sapientinc/HRM-Text-1B # run cli
```

You can also use the ohrmes_lib.py script in your python scripts:
```python
from ohrmes_lib import chat

print(chat(model="sapientinc/HRM-Text-1B", messages=[{"role": "user", "content": "Why is the sky blue?"}])["message"]["content"])
```