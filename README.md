# LLaMaFinetuneCece

## Setup
1. Install python dependencies in a Python 3.9 environment.

```shell
pip install -r requirements.txt
```

2. Create a `keys.py` file inside `configs/`, then place the API keys accordingly as described in `configs/__init__.py`


## Files

`prompts_base.py` contains the prompts for each model (in this case, just GPT-4 and Llama 3, though most of GPT-4's prompts are actually inside its generator)

`generate_response.py` contains two classes used for generating outputs: one for Llama and one for GPT-4. The class for Llama could be repurposed for any model on HuggingFace.

`run_infer.py` is a starting point and can be executed to generate a single sentence. See below for examples on how to run and pass parameters to it.

`gen_questions.py` was used for generating the user participant survey questions. It takes in the questions_data file, which has the representation, keywords, and emotion on each row and generates an sentence for each line.

The folder `stats/` contains the notebooks used for analyzing the survey participant responses. Both notebooks are identical but separated for convenience. The survey response datasets are also included in the folder.

## To Run
```shell
python run_infer.py --model_task "gpt_4_conversation" --emotion "Happy" --keywords "Morning, Cat, Woke"
```
Check `prompts_base.py` for a list of the available options for model_task.

When running on UMBC's HPC cluster through Slurm, use the following line. Adjust the time and memory requirements as needed by the model. For example:

```shell
srun --mem=12000 --time=00:05:00 --gres=gpu:1 python run_infer.py --model_task "llama_3_conversation" --emotion "😡" --keywords "Morning, Cat, Woke"
````
```shell
srun --mem=12000 --time=00:15:00 --gres=gpu:1 python run_infer.py -M "gpt_4_conversation_vad" -V "Low" -A "High" -D "High" -K "Morning, Cat, Woke"
```

To run `gen_questions.py` on an open-source model, I recommend a higher end GPU and several hours.

```shell
srun --mem=32000 --time=04:00:00 --gres=gpu:4 --constraint='rtx_6000' python gen_questions.py
```

## Paper

```
@report{Choudhury2025GPTsDevastated,
title={{GPT's Devastated and LLaMA's Content: Emotion Representation Alignment in LLMs for Keyword-based Generation}},
author={Choudhury, Shadab and Kumar, Asha and Martin, Lara J.},
year={2025},
eprint={2503.11881},
archivePrefix={arXiv},
url={https://arxiv.org/abs/2503.11881},
doi={10.48550/arXiv.2503.11881},
month={03}
}
```

