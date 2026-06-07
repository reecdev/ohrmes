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

Note: Some platforms will download the CPU-only version of PyTorch by default. If you have an NVIDIA GPU, check if CUDA is available.

```bash
python -c "import torch; print(torch.cuda.is_available())"
# ^ should return True if you have an NVIDIA gpu
```

```bash
# reinstall pytorch with gpu support if it returns False
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Optionally, add Ohrmes CLI as a custom command via alias if using macOS or Linux:

```bash
# switch ~/.bashrc to ~/.zshrc if using zsh
echo "alias ohrmes='python $(pwd)/ohrmes.py'" >> ~/.bashrc
source ~/.bashrc

# Now you can run it from anywhere!
ohrmes --run sapientinc/HRM-Text-1B
```

## Using ohmres
Use the ohrmes.py script to use Ohmres.

```bash
python ohrmes.py --serve &
python ohrmes.py --run sapientinc/HRM-Text-1B
```

You can also use the ohrmes_lib.py script in your python scripts:
```python
from ohrmes_lib import chat

print(chat(model="sapientinc/HRM-Text-1B", messages=[{"role": "user", "content": "Why is the sky blue?"}])["message"]["content"])
```

Or with streaming:

```python
from ohrmes_lib import chat

stream = chat(model="sapientinc/HRM-Text-1B", messages=[{"role": "user", "content": "Why is the sky blue?"}], stream=True)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
```

---

### Why did I make this?
I believe that the HRM-Text models are the next big thing in AI. I'm building a wrapper for HRM-Text to make it much easier for people to adopt it.

### Special Thanks
Special thanks to the people at SapientINC for creating [HRM-Text](https://github.com/sapientinc/HRM-Text) and Ollama for the inspiration of this project. I support the work of SapientINC and look forward to seeing more from HRM models!
