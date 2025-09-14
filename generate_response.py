import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import os
from openai import OpenAI

import accelerate

from configs import org, api_key

"""
THIS FILE CONTAINS TWO GENERATOR CLASSES FOR TWO MODELS LLAMA 3 AND GPT-4.

EACH CLASS LOADS THE MODEL WHEN INITIALIZED (THOUGHT GPT-4 DOESN'T ACTUALLY HAVE TO BE LOADED). THEN FOR ACTUAL GENERATION, THE response FUNCTION IS called.

FOR LLAMA 3, THE RESPONSE FUNCTION IS THE SAME FOR ALL EMOTION REPRESENTATIONS AND DIFFERENT PROMPTS ARE USED TO IMPLEMENT THEM. FOR GPT-4, THE RESPONSE FUNCTION
VARIES BASED ON THE REPRESENTATION USED.
"""

class llama_3_generator:

    def __init__(self):
        """
        Change model to change which model (on Huggingface) is used for the text generation.
        Although if you use a different model you might just want to refactor this function to be a 'general' one.
        """

        model = "meta-llama/Llama-3.3-70B-Instruct"

        self.gen_model = "llama3"       # Name of the model. Goes into the output file name.

        quantization_config = BitsAndBytesConfig(load_in_8bit=True)

        self.quantized_model = AutoModelForCausalLM.from_pretrained(
            model, device_map="auto", torch_dtype=torch.bfloat16, quantization_config=quantization_config)

        self.tokenizer = AutoTokenizer.from_pretrained(model)

    def response(self, prompt, save=False, emotion=None, keywords=None, num_return_sequences=1, max_length=64) -> str:
        """
        Generates a short sentence based on the given keywords that also hews to a certain emotion.

        Args:
            prompt: The prompt given to the model.
            save: Whether to save the generated sentence or not. This is separate from generating the csv file and simply saves to a text file for test/debug/demo purposes.
            emotion: If saving to a text file, pass the emotion here so it's also recorded. Otherwise, ignore.
            keywords: If saving to a text file, pass the keywords here so it's also recorded. Otherwise, ignore.
            num_return_sequences: Defaults to 1. If you want to do something like ranking multiple responses, increase this.
            max_length: Defaults to 64. Kept this short to get faster outputs (and our goal's to have mostly sentences under 50 tokens anyway)

        Returns: The generated sentence as a string.
        """

        input_text = prompt
        input_ids = self.tokenizer(input_text, return_tensors="pt").to("cuda")

        output = self.quantized_model.generate(**input_ids, max_new_tokens=128)

        op = self.tokenizer.decode(output[0], skip_special_tokens=True)

        if save and emotion and keywords:
            with open(os.path.join("outputs", "text_responses", f"{self.gen_model}_output_convresp.txt"), "a") as myfile:
                op_to_file = f"Emotion: {emotion}\nKeywords: {str(keywords)[1:-1]}\nDialogue: {op}"
                myfile.write(op_to_file)
                myfile.write("\n===========================================================\n")

        # return op


class gpt_oai_generator:

    def __init__(self):
        """
        Make sure you correctly place and import the OpenAI org key and api key.
        Change self.model to change which model or model version from the OpenAI API is used for the text generation.
        """

        self.client = OpenAI(
            api_key=api_key
        )

        self.model = "gpt-4-turbo-2024-04-09"

        self.gen_model = "gpt4"         # Name of the model. Just goes into the output file name.


    def response(self, prompt, save=False, emotion=None, keywords=None) -> str:
        """
        Generates a short sentence based on the given keywords that also hews to a certain emotion given as either text
        or emoji.

        Args:
            prompt: The prompt given to the model.
            save: Whether to save the generated sentence or not. This is separate from generating the csv file and simply saves to a text file for test/debug/demo purposes.
            emotion: If saving to a text file, pass the emotion here so it's also recorded. Otherwise ignore.
            keywords: If saving to a text file, pass the keywords here so it's also recorded. Otherwise ignore

        Returns: The generated sentence as a string.
        """

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",
                 "content": "You are engaging in a conversation with a human. Respond to the following line of "
                            "dialogue based on the given emotion and the following keywords."
                            "Just add connective words and do not add any new information to the output sentence."
                            f"Do not use the word '{emotion}' in the response and express the sentiment in a different way"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        op = completion.choices[0].message.content

        if save and emotion and keywords:
            with open(os.path.join("outputs", f"{self.gen_model}_output_convresp.txt"), "a") as myfile:
                op_to_file = f"Emotion: {emotion}\nKeywords: {str(keywords)[1:-1]}\nDialogue: {op}"
                myfile.write(op_to_file)
                myfile.write("\n===========================================================\n")

        return op


    def response_vad(self, prompt, save=False, valence=None, arousal=None, dominance=None, keywords=None) -> str:
        """
        Generates a short sentence based on the given keywords that also hews to a certain emotion given in lexical VAD format.

        Args:
            prompt: The prompt given to the model.
            save: Whether to save the generated sentence or not. This is separate from generating the csv file and simply saves to a text file for test/debug/demo purposes.
            valence: If saving to a text file, pass the Valence here so it's also recorded. Otherwise, ignore.
            arousal: If saving to a text file, pass the Arousal here so it's also recorded. Otherwise, ignore.
            dominance: If saving to a text file, pass the Dominance here so it's also recorded. Otherwise, ignore.
            keywords: If saving to a text file, pass the keywords here so it's also recorded. Otherwise ignore

        Returns: The generated sentence as a string.
        """

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user",
                 "content": "Please define valence, arousal and dominance in the context of emotion in text."},
                {"role": "assistant",
                 "content": """In the context of emotion in text, **valence**, **arousal**, and **dominance** are three dimensions commonly used to describe and analyze emotional states. These dimensions provide a way to quantify and understand the emotional content conveyed in written language.
                    
                    1. **Valence**: 
                       - Valence refers to the intrinsic attractiveness or averseness of an event, object, or situation. In the context of emotions in text, valence represents the positivity or negativity of the emotion expressed. For example, words like "happy," "joyful," or "excited" have positive valence, whereas words like "sad," "angry," or "frustrated" have negative valence.
                       - It essentially measures the degree of pleasantness or unpleasantness of the emotion.
                    
                    2. **Arousal**: 
                       - Arousal indicates the level of alertness, excitement, or energy associated with an emotion. It ranges from high arousal (e.g., excitement, anger) to low arousal (e.g., calm, boredom). In text, high-arousal words might include "thrilled," "furious," or "ecstatic," while low-arousal words could be "relaxed," "content," or "lethargic."
                       - This dimension measures how stimulating or soothing the emotional state is.
                    
                    3. **Dominance**: 
                       - Dominance reflects the degree of control, influence, or power that one feels in a particular emotional state. High dominance implies feelings of control and empowerment, while low dominance suggests feelings of submissiveness or lack of control. In text, emotions like "confident," "powerful," or "authoritative" would have high dominance, whereas "helpless," "weak," or "submissive" would have low dominance.
                       - It gauges the extent to which an individual feels in control or overpowered by the emotion.
                    
                    These three dimensions are often used in psychological and computational studies to create a comprehensive representation of emotions in text, facilitating better analysis and understanding of emotional expression."""},
                {"role": "user",
                 "content": prompt},
            ],
            temperature=0.5
        )
        op = completion.choices[0].message.content

        if save and valence and arousal and dominance and keywords:
            with open(os.path.join("outputs", "gpt4_output_convresp.txt"), "a") as myfile:
                op_to_file = f"Valence: {valence}, Arousal: {arousal}, Dominance: {dominance}\nKeywords: {str(keywords)[1:-1]}\nDialogue: {op}"
                myfile.write(op_to_file)
                myfile.write("\n===========================================================\n")

        return op

    def response_vad_num(self, prompt, save=False, valence=None, arousal=None, dominance=None,
                             keywords=None) -> str:
        """
        Generates a short sentence based on the given keywords that also hews to a certain emotion given in numeric VAD format.

        Args:
            prompt: The prompt given to the model.
            save: Whether to save the generated sentence or not. This is separate from generating the csv file and simply saves to a text file for test/debug/demo purposes.
            valence: If saving to a text file, pass the Valence here so it's also recorded. Otherwise, ignore.
            arousal: If saving to a text file, pass the Arousal here so it's also recorded. Otherwise, ignore.
            dominance: If saving to a text file, pass the Dominance here so it's also recorded. Otherwise, ignore.
            keywords: If saving to a text file, pass the keywords here so it's also recorded. Otherwise ignore

        Returns: The generated sentence as a string.
        """

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user",
                 "content": "Please define valence, arousal and dominance in the context of emotion in text."},
                {"role": "assistant",
                 "content": """In the context of emotion in text, **valence**, **arousal**, and **dominance** are three dimensions commonly used to describe and analyze emotional states. These dimensions provide a way to quantify and understand the emotional content conveyed in written language.

                    1. **Valence**: 
                       - Valence refers to the intrinsic attractiveness or averseness of an event, object, or situation. In the context of emotions in text, valence represents the positivity or negativity of the emotion expressed. For example, words like "happy," "joyful," or "excited" have positive valence, whereas words like "sad," "angry," or "frustrated" have negative valence.
                       - It essentially measures the degree of pleasantness or unpleasantness of the emotion.

                    2. **Arousal**: 
                       - Arousal indicates the level of alertness, excitement, or energy associated with an emotion. It ranges from high arousal (e.g., excitement, anger) to low arousal (e.g., calm, boredom). In text, high-arousal words might include "thrilled," "furious," or "ecstatic," while low-arousal words could be "relaxed," "content," or "lethargic."
                       - This dimension measures how stimulating or soothing the emotional state is.

                    3. **Dominance**: 
                       - Dominance reflects the degree of control, influence, or power that one feels in a particular emotional state. High dominance implies feelings of control and empowerment, while low dominance suggests feelings of submissiveness or lack of control. In text, emotions like "confident," "powerful," or "authoritative" would have high dominance, whereas "helpless," "weak," or "submissive" would have low dominance.
                       - It gauges the extent to which an individual feels in control or overpowered by the emotion.

                    These three dimensions are often used in psychological and computational studies to create a comprehensive representation of emotions in text, facilitating better analysis and understanding of emotional expression."""},
                {"role": "user",
                 "content": "For the next part, lets define each dimension on a scale of -5.0 to 5.0."
                },
                {"role": "assistant",
                 "content": """Sure, here's how each dimension can be defined on a scale from -5.0 to 5.0:
                    Valence:
                        -5.0: Extremely negative (e.g., intense sadness, extreme anger)
                        -2.5: Moderately negative (e.g., mild annoyance, slight disappointment)
                        0.0: Neutral (e.g., indifferent, no strong emotional reaction)
                        2.5: Moderately positive (e.g., mild pleasure, slight happiness)
                        5.0: Extremely positive (e.g., intense joy, deep love)
                    Arousal:
                        -5.0: Extremely low arousal (e.g., deep sleep, total relaxation)
                        -2.5: Moderately low arousal (e.g., relaxed, slightly tired)
                        0.0: Neutral arousal (e.g., alert but not excited, calm)
                        2.5: Moderately high arousal (e.g., interested, mildly excited)
                        5.0: Extremely high arousal (e.g., highly excited, very agitated)
                    Dominance:
                        -5.0: Extremely low dominance (e.g., feeling completely powerless, totally submissive)
                        -2.5: Moderately low dominance (e.g., somewhat submissive, slightly dominated)
                        0.0: Neutral dominance (e.g., feeling neither in control nor dominated)
                        2.5: Moderately high dominance (e.g., feeling somewhat in control, slightly assertive)
                        5.0: Extremely high dominance (e.g., feeling very powerful, completely in control)
                    These scales provide a way to quantify and compare the emotional dimensions in a structured manner."""
                },
                {"role": "user",
                 "content": prompt},
            ],
            temperature=0.5
        )
        op = completion.choices[0].message.content

        if save and valence and arousal and dominance and keywords:
            with open(os.path.join("outputs", "gpt4_output_convresp.txt"), "a") as myfile:
                op_to_file = f"Valence: {valence}, Arousal: {arousal}, Dominance: {dominance}\nKeywords: {str(keywords)[1:-1]}\nDialogue: {op}"
                myfile.write(op_to_file)
                myfile.write("\n===========================================================\n")

        return op


