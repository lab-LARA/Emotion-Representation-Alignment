import time
import argparse
import prompts_base
from generate_response import *


def fetch_response_function(generator, task):
    """
    Returns the response function based on the type of emotion representation (which is given as task).

    Each model (GPT-4, Llama 3) have different functions per emotion representation, so.

    Args:
        generator: generator object that was initialized in main()
        task: emotion representation to use - words/emoji, vad, or vad_num

    Returns: the exact function from generator that will be called to generate the sentence.
    """

    if generator.gen_model == "llama3":
        return generator.response
    if generator.gen_model == "gpt4":
        if "vad_num" in task:
            return generator.response_vad_num
        elif "vad" in task:
            return generator.response_vad
        else:
            return generator.response

generator = llama_3_generator()

def main(task, keywords, emo="Neutral", v=None, a=None, d=None):
    """
    First, checks the task to determine which model to use. Initializes the generator object for that model,
    then calls the response function for model. Then fetches the prompt based on the task and uses the two
    to generate an output.

    This be used on its own for debug/test/demo purposes, ori

    Args:
        task: the task determines which model and prompt to use. It should be one of the keys from the prompt_dict in prompts_base.py
        keywords: The keywords to use when generating sentences.
        emo: The emotion to use. This should be passed when using Words or Emojis as the emotion representation.
        v: The valence. This should be passed when using Lexical or Numeric VAD as the emotion representation.
        a: The arousal. This should be passed when using Lexical or Numeric VAD as the emotion representation.
        d: The dominance. This should be passed when using Lexical or Numeric VAD as the emotion representation.

    Returns: A tuple with [the generated output sentence, and the full prompt used to generate it]
    """

    # if "llama_3" in task:
    #     generator = llama_3_generator()
    # elif "gpt_4" in task:
    #     generator = gpt_oai_generator()

    kwds = keywords.replace(", ", ",").split(",")

    response_function = fetch_response_function(generator=generator, task=task)

    task = task.replace("_num", "")
    prompt = prompts_base.fetch_prompt(
        model_task=task,
        emotion=emo, keywords=kwds, valence=v, arousal=a, dominance=d
    )

    start_time = time.time()
    output = response_function(prompt=prompt).replace('"', '').replace("'", "").replace(prompt, "").strip()#.split("\n")[0]
    print(f"Inference Time for {task}: {time.time() - start_time:.4f}")

    formatted_resp = f'"{task}", "{emo}", "{v}", "{a}", "{d}", "{kwds}", "{output}"\n'

    print(formatted_resp)

    return output, prompt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-M', '--model_task', type=str, required=True, help='Which model/prompt to use.')
    parser.add_argument('-E', '--emotion', type=str, required=False, help='The emotion to be expressed.')
    parser.add_argument('-V', '--valence', type=str, required=False, help='Valence')
    parser.add_argument('-A', '--arousal', type=str, required=False, help='Arousal')
    parser.add_argument('-D', '--dominance', type=str, required=False, help='Dominance')
    parser.add_argument('-K', '--keywords', type=str, required=True, help='Keywords for the sentence. The keywords should be separated by commas')
    parser.add_argument('-S', '--save', type=str, required=False, help='True to save, blank to not.')

    args = parser.parse_args()
    print(args)

    main(args.model_task, emo=args.emotion, v=args.valence, a=args.arousal, d=args.dominance, keywords=args.keywords, save=args.save)

    # Examples:
    # python run_infer.py -M "gpt_4_conversation" -E "Annoyed" -K "Morning, Cat, Woke"
    # python run_infer.py -M "gpt_4_conversation_vad" -V "Low" -A "High" -D "High" -K "Morning, Cat, Woke"
    # python run_infer.py -M "llama_3_conversation_vad" -V "Low" -A "High" -D "High" -K "Morning, Cat, Woke" -S "True"

