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

transcription = "So this is a call to myself to start working out, to start building a body that I can be proud of to die in. I do aspire for the beauty of form internally and externally. I look for beautiful things in the world. I eat beautiful things, I look at beautiful things and I listen to beautiful things. It's time to make my body one of those beautiful things."


data = f"Conversation Transcription: {transcription}\nQuotes: {quotes}"

completion = client.chat.completions.create(
  model="gpt-4-turbo-preview",
  messages=[
    {"role": "system", "content": sys_prompt},
    {"role": "user", "content": data},
  ]
)

print(completion.choices[0].message.content)
