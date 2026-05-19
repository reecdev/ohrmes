# ohrmes - hrm models made easy
Ohrmes is a wrapper for HRM-Text that makes it easy to use HRM-Text models locally on your computer.

## Quickstart
Use a Transformers build that includes the hrm_text model class. If your installed release does not include it yet, install Transformers directly from the upstream main branch:

```bash
pip install --upgrade "git+https://github.com/huggingface/transformers.git@main"
```

Then, clone the repository:

```bash
git clone https://github.com/reecdev/ohrmes.git
```

## Using ohmres
Use the ohrmes.py script to use Ohmres.

```bash
python ohrmes.py --serve &
python ohrmes.py --run sapientinc/HRM-Text-1B # run cli
```