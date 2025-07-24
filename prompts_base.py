import textwrap

"""
THIS FILE CONTAINS ALL THE PROMPTS AS A DICTIONARY, AS WELL AS FUNCTIONS TO CORRECTLY INSERT THE EMOTION REPRESENTATION
AND VALUES INTO THE PROMPT.
"""


prompts_dict = {
    "llama_3_conversation": """
        You are engaging in a conversation with a human. Respond to the following line of dialogue based on the given emotion and the following keywords.
        Just add connective words and do not add any new information to the output sentence. The response should be exactly one line with nothing else other than the responding dialogue."
        Do not use the word {emo_} in the response.

        For example: 

        Emotion: Proud
        Keywords: 'running', 'marathon', 'first'
        Dialogue: Running my first marathon felt like such a huge accomplishment!

        Emotion: Sad
        Keywords: 'banana', 'plant', 'brown'
        Dialogue: It really sucks that my banana plant is turning brown

        Now, respond to the following:
        Emotion: {emo_}
        Keywords: {kwds_}
        Dialogue:""",


    "llama_3_emoji": """
        You are engaging in a conversation with a human. Respond to the following line of dialogue based on the given emotion and the following keywords.
        Just add connective words and do not add any new information to the output sentence. The response should be exactly one line with nothing else other than the responding dialogue."
    
        For example: 
    
        Emotion: 🤩
        Keywords: 'running', 'marathon', 'first'
        Dialogue: Running my first marathon felt like such a huge accomplishment!
    
        Emotion: 😭
        Keywords: 'banana', 'plant', 'brown'
        Dialogue: It really sucks that my banana plant is turning brown
        
        Emotion: 😃
        Keywords: "visit", "parents", "month"
        Dialogue: I'm finally going to visit my parents next month!
    
        Now, respond to the following:
        Emotion: {emo_}
        Keywords: {kwds_}
        Dialogue:""",


    "llama_3_conversation_vad": """   
        Valence refers to the intrinsic attractiveness or averseness of an event, object, or situation. In the context of emotions in text, valence represents the positivity or negativity of the emotion expressed. For example, words like "happy," "joyful," or "excited" have positive valence, whereas words like "sad," "angry," or "frustrated" have negative valence.
        It essentially measures the degree of pleasantness or unpleasantness of the emotion.              
    
        Arousal indicates the level of alertness, excitement, or energy associated with an emotion. It ranges from high arousal (e.g., excitement, anger) to low arousal (e.g., calm, boredom). In text, high-arousal words might include "thrilled," "furious," or "ecstatic," while low-arousal words could be "relaxed," "content," or "lethargic."
        This dimension measures how stimulating or soothing the emotional state is.
    
        Dominance reflects the degree of control, influence, or power that one feels in a particular emotional state. High dominance implies feelings of control and empowerment, while low dominance suggests feelings of submissiveness or lack of control. In text, emotions like "confident," "powerful," or "authoritative" would have high dominance, whereas "helpless," "weak," or "submissive" would have low dominance.
        It gauges the extent to which an individual feels in control or overpowered by the emotion.
    
        Now, assume you are a normal human. Say a line of natural dialogue based on the given keywords. Just add connective words and do not add any new information to the output sentence.
    
        For example: 

        Emotion: Very High Valence, High Arousal, Very High Dominance
        Keywords: 'running', 'marathon', 'first'
        Dialogue: Running my first marathon felt like such a huge accomplishment!

        Emotion: Very Low Valence, Low Arousal, Low Dominance
        Keywords: 'banana', 'plant', 'brown'
        Dialogue: It really sucks that my banana plant is turning brown
        
        Emotion: Very High Valence, Very High Arousal, High Dominance
        Keywords: "visit", "parents", "month"
        Dialogue: I'm finally going to visit my parents next month!

        Now, respond to the following:
        Emotion: {v_}, {a_}, and {d_}.
        Keywords: {kwds_}
        Dialogue:
    """,

    "llama_3_conversation_vadnum": """
        Valence refers to the intrinsic attractiveness or averseness of an event, object, or situation. In the context of emotions in text, valence represents the positivity or negativity of the emotion expressed. For example, words like "happy," "joyful," or "excited" have positive valence, whereas words like "sad," "angry," or "frustrated" have negative valence.
        It essentially measures the degree of pleasantness or unpleasantness of the emotion.
        
        0.0: Extremely negative (e.g., intense sadness, extreme anger)
        1.0: Very negative (e.g., strong dislike, significant frustration)
        2.0: Moderately negative (e.g., mild annoyance, slight disappointment)
        3.0: Neutral (e.g., indifferent, no strong emotional reaction)
        4.0: Moderately positive (e.g., mild pleasure, slight happiness)
        5.0: Extremely positive (e.g., intense joy, deep love)                        

        Arousal indicates the level of alertness, excitement, or energy associated with an emotion. It ranges from high arousal (e.g., excitement, anger) to low arousal (e.g., calm, boredom). In text, high-arousal words might include "thrilled," "furious," or "ecstatic," while low-arousal words could be "relaxed," "content," or "lethargic."
        This dimension measures how stimulating or soothing the emotional state is.
        
        0.0: Extremely low arousal (e.g., deep sleep, total relaxation)
        1.0: Very low arousal (e.g., very calm, almost drowsy)
        2.0: Moderately low arousal (e.g., relaxed, slightly tired)
        3.0: Neutral arousal (e.g., alert but not excited, calm)
        4.0: Moderately high arousal (e.g., interested, mildly excited)
        5.0: Extremely high arousal (e.g., highly excited, very agitated)

        Dominance reflects the degree of control, influence, or power that one feels in a particular emotional state. High dominance implies feelings of control and empowerment, while low dominance suggests feelings of submissiveness or lack of control. In text, emotions like "confident," "powerful," or "authoritative" would have high dominance, whereas "helpless," "weak," or "submissive" would have low dominance.
        It gauges the extent to which an individual feels in control or overpowered by the emotion.
        
        0.0: Extremely low dominance (e.g., feeling completely powerless, totally submissive)
        1.0: Very low dominance (e.g., feeling dominated, significantly submissive)
        2.0: Moderately low dominance (e.g., somewhat submissive, slightly dominated)
        3.0: Neutral dominance (e.g., feeling neither in control nor dominated)
        4.0: Moderately high dominance (e.g., feeling somewhat in control, slightly assertive)
        5.0: Extremely high dominance (e.g., feeling very powerful, completely in control)

        Now, assume you are a normal human. Say one line of natural dialogue based on the following keywords. Just add connective words and do not add any new information to the output sentence.

        For example: 

        Emotion: Valence: 4.0, Arousal: 1.0, Dominance: 2.5
        Keywords: 'running', 'marathon', 'first'
        Dialogue: Running my first marathon felt like such a huge accomplishment!

        Emotion: Valence: -4.0, Arousal: -2.5, Dominance: -4.0
        Keywords: 'banana', 'plant', 'brown'
        Dialogue: It really sucks that my banana plant is turning brown
        
        Emotion: Valence: 2.5, Arousal: 4.0, Dominance: 1.0
        Keywords: "visit", "parents", "month"
        Dialogue: I'm finally going to visit my parents next month!

        Now, respond to the following:
        Emotion: Valence: {v_}, Arousal: {a_}, Dominance: {d_} 
        Keywords: {kwds_}
        Dialogue:
    """,

    "gpt_4_conversation": """
        Here are some examples: 

        Emotion: Proud
        Keywords: 'running', 'accomplishment', 'marathon', 'first'
        Dialogue: Running my first marathon felt like such a huge accomplishment!

        Emotion: Lonely
        Keywords: 'country', 'live', 'friends', 'feel'
        Dialogue: I feel so lonely sometimes because all my friends live in a different country

        Emotion: Sad
        Keywords: 'banana', 'plant', 'leaf', 'brown'
        Dialogue: It really sucks that my banana plant's leaf is turning brown

        Now, respond to the following. Remember, do not use the word {emo_} in the dialogue.:
        Emotion: {emo_}
        Keywords: {kwds_}
        Dialogue:""",


    "gpt_4_conversation_emoji": """
        Here are some examples: 

        Emotion: 🤩
        Keywords: 'running', 'marathon', 'first'
        Dialogue: Running my first marathon felt like such a huge accomplishment!

        Emotion: 🙁
        Keywords: 'country', 'living', 'feel'
        Dialogue: I feel so lonely sometimes living out in the country

        Emotion: 😭
        Keywords: 'banana', 'plant', 'brown'
        Dialogue: It really sucks that my banana plant is turning brown

        Now, respond to the following. Remember, do not use the emoji {emo_} or any other emojis in the response. The response should be text only, with no emojis. Keep it concise and express the given feeling in as few words as possible while including the keywords:
        Emotion: {emo_}
        Keywords: {kwds_}
        Dialogue:""",


    "gpt_4_conversation_vad": """
        Now, you are a person conversing with another person. Speak a line of natural dialogue based on the following keywords. Just add connective words and do not add any new information to the output sentence.
        
        {kwds_}
        
        The response should have {v_} valence, {a_} arousal and {d_} dominance.
    """,
}


def list_prompts() -> [str]:
    return list(prompts_dict.keys())


def fetch_raw_prompt(model_task: str) -> str:
    return prompts_dict.get(model_task)


def fetch_prompt(model_task: str, emotion: str = "", keywords: [str] = "", valence: str = "low", arousal: str = "low", dominance: str = "low") -> str:
    """
    Fetches the correct prompt and inserts the
    Args:
        model_task: The model and representation and task for which we want the prompt.
        emotion: The Emotion when Words or Emoji are used as the representation.
        keywords: The keywords to be placed into the prompt and used for generating the sentence.
        valence: The Valence when VAD is used as the representation.
        arousal: The Arousal when VAD is used as the representation.
        dominance: The Dominance when VAD is used as the representation.

    Returns: The full prompt with keywords and emotions inserted.
    """
    if "vad" in model_task:
        prompt = prompts_dict.get(model_task).format(v_=valence, a_=arousal, d_=dominance, kwds_=str(keywords)[1:-1])
    elif "no_emotion" in model_task:
        prompt = prompts_dict.get(model_task).format(kwds_=str(keywords)[1:-1])
    else:
        prompt = prompts_dict.get(model_task).format(emo_=emotion, kwds_=str(keywords)[1:-1])
    return textwrap.dedent(prompt).strip()

