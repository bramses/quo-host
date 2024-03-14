'''
1. choose the most interesting and relevant quote of the quotes given the transcription. the quote chosen should be the one that stimulates the most conversation. look at each in the context of the transcription before choosing.
2. bold the text in the quote that makes a complete thought in reference to the transcription. do not bold the entire quote, it will only be glanced at. you can bold multiple parts of the quote if relevant.
3. feed back edited full quote, say nothing else

---

Conversation Transcription: {transcription}

Quotes: {quotes}
'''

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

sys_prompt = '''1. choose the most interesting and relevant quote of the quotes given the transcription. the quote chosen should be the one that stimulates the most conversation. look at each in the context of the transcription before choosing.
2. bold the text in the quote that makes a complete thought in reference to the transcription. do not bold the entire quote, it will only be glanced at. you can bold multiple parts of the quote if relevant.
3. feed back edited full quote, say nothing else'''

quotes = [
	{
		"text": "I should strive to make my life a reflection of my inner vision of the good.",
		"title": "The Six Pillars of Self-Esteem",
		"similarity": 0.852123460440625,
		"id": 549479811,
		"author": "Nathaniel Branden"
	},
	{
		"text": "My idea will be, and always has been, to leave the muscles to look after themselves, but I place a premium upon the possession of untiring energy, great stamina and vital power and a sound constitution.",
		"title": "The Development of Physical Power",
		"similarity": 0.845016604019956,
		"id": 690177134,
		"author": "Arthur Saxon"
	},
	{
		"text": "If you do your best in the search for personal freedom, in the search for self-love, you will discover that it’s just a matter of time before you find what you are looking for. It’s not about daydreaming or sitting for hours dreaming in meditation. You have to stand up and be a human. You have to honor the man or woman that you are. Respect your body, enjoy your body, love your body, feed,",
		"title": "The Four Agreements: A Practical Guide to Personal Freedom (A Toltec Wisdom Book)",
		"similarity": 0.837050464211422,
		"id": 41702217,
		"author": "Don Miguel Ruiz, Janet Mills"
	}
]

transcription = "I don't know when it started. I've been working on my blog for years now, and in a way that feels like it's kind of like my legacy with all the effort that I put into it. But the truth is, I think I'm just afraid of working out. I'm afraid of pain. I have a very low pain tolerance."


# data = f"Conversation Transcription: {transcription}\nQuotes: {quotes}"

# completion = client.chat.completions.create(
#   model="gpt-4-turbo-preview",
#   messages=[
#     {"role": "system", "content": sys_prompt},
#     {"role": "user", "content": data},
#   ]
# )

# print(completion.choices[0].message.content)


def choose_quote(quotes, transcription):
    prompt = "choose the most interesting and relevant quote of the quotes given the transcription. the quote chosen should be the one that stimulates the most conversation. look at each in the context of the transcription before choosing. return the following: the index of the quote, and your reasoning as to why that is the choice. return in JSON form as { index, reasoning }. say nothing else"
    data = f"Quotes: {quotes}\nTranscription: {transcription}"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": data},
        ]
    )
    return completion.choices[0].message.content.replace("```json", "").replace("```", "").strip()

def bold_quote(quote, transcription, reasoning):
    prompt = "bold the text in the quote that makes a complete thought in reference to the transcription and the reasoning. do not bold the entire quote, it will only be glanced at. you can bold multiple parts of the quote if relevant.\n\nreturn the edited full quote. say nothing else."
    data = f"Quote: {quote}\n\nTranscription: {transcription}\n\nReasoning for Quote Choice in Transcript: {reasoning}"
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": data},
        ]
    )
    return completion.choices[0].message.content

quote = choose_quote(quotes, transcription)
json_quote = json.loads(quote)
bolded_quote = bold_quote(quotes[json_quote['index']], transcription, json_quote['reasoning'])
print(bolded_quote)
