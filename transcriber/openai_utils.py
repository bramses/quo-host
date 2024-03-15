from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
GPT3_MODEL = "gpt-3.5-turbo"
GPT4_MODEL = "gpt-4-turbo-preview"

quotes = [
    {
        "text": "What difference there might be resolves itself into the presence or absence of the idea of honor, which regards death as \"something to be seen,\" and the presence or absence of the formal aesthetic of death that goes with it—in other words, the tragic nature of the approach to death and the beauty of the body going to its doom. Thus, where a beautiful death is concerned, men are condemned to inequalities and degrees of fortune commensurate with the inequalities and degrees of fortune bestowed on them by fate at their birth—though this inequality is obscured nowadays by the fact that modern man is almost devoid of the desire of the ancient Greeks to live \"beautifully\" and die \"beautifully.\" Why should a man be associated with beauty only through a heroic, violent death? In ordinary life, society maintains a careful surveillance to ensure that men shall have no part in beauty; physical beauty in the male, when considered as an \"object\" in itself without any intermediate agent, is despised, and the profession of the male actor—which involves constantly being \"seen\"—is far from being accorded true respect. A strict rule is imposed where men are concerned. It is this: a man must under normal circumstances never permit his own objectivization; he can only be objectified through the supreme action—which is, I suppose, the moment of death, the moment when, even without being seen, the fiction of being seen and the beauty of the object are permitted. Of such is the beauty of the suicide squad, which is recognized as beauty not only in the spiritual sense but, by men in general, in an ultra-erotic sense also. Moreover, serving as agent in this case is a heroic action of an intensity beyond the resources of the ordinary mortal, so that \"objectivization\" without an agent is not possible here. However close mere words may get to this moment of supreme action that acts as intermediary for beauty, they can no more overtake it than a flying body can attain the speed of light.",
        "title": "Sun and Steel",
        "similarity": 0.870219573433458,
        "id": 687722070,
        "author": "Yukio Mishima"
    },
    {
        "text": "In 1996 the psychologist Amos Tversky learned that he was dying of metastatic melanoma. He carried on his normal routine, and most of those who encountered him were oblivious to his condition. He died not long afterward, at age fifty-nine. During a discussion of his impending death, he told a friend: “Life is a book. The fact that it was a short book doesn’t mean it wasn’t a good book. It was a very good book.”1 Although Tversky died a natural death, he had obtained drugs that would allow him to end his life quickly and painlessly, if he chose to do so. The ancient Stoics would have understood this choice. They thought that under some circumstances, suicide wasn’t just morally acceptable; it was sensible. Seneca, for example, imagined God explaining his thinking to us: “I have made nothing easier than dying. I placed life on a downward slope: if it is prolonged, only observe and you will see how short, how easy is the path that leads to freedom.”2 Dying, then, is the easy part of your Stoic exit exam; the challenge is to retain your equanimity. I should add that as long as your continued existence can help others, Stoics would regard it as cowardly to commit suicide.",
        "title": "The Stoic Challenge: A Philosopher's Guide to Becoming Tougher, Calmer, and More Resilient",
        "similarity": 0.864330617977021,
        "id": 575337501,
        "author": "William B. Irvine"
    },
    {
        "text": "Typically, the thought of death may be expected, first, to usher us towards whatever happens to matter most to us (be it drinking beside the banks of the Nile, writing a book or making a fortune), and second, to encourage us to pay less attention to the verdicts of others—who will not, after all, be doing the dying for us. The prospect of our own extinction may draw us towards that way of life on which our hearts place the greatest value. This theme animates “To His Coy Mistress” (1681), Andrew Marvell’s famous poetic attempt to lure a hesitant young woman into bed, through lines that stress not only her beauty and his fidelity but also the less obviously romantic notion that both she and he will soon enough be stone dead.",
        "title": "Status Anxiety (Vintage International)",
        "similarity": 0.862274572311573,
        "id": 100099636,
        "author": "Alain De Botton"
    }
]

transcription = "I've been reading sun and steel by Yukiyo Mishima and it's been having a great impact on me. Death is something to be seen. Ancient Greeks wanting to live and die beautifully. A man can only be objectified through his supreme action, which is the moment of his death. These are really interesting thoughts."


def choose_quote(quotes, transcription):
    prompt = "choose the most interesting and relevant quote of the quotes given the transcription. the quote chosen should be the one that stimulates the most conversation. look at each in the context of the transcription before choosing. return the following: the index of the quote (index from zero), and your reasoning as to why that is the choice. return in JSON form as { index, reasoning }. say nothing else"

    quotes_title_author_mapped = [f"{quote['text']}\n--{quote['title']} by {quote['author']}" for quote in quotes]

    data = f"Quotes: {quotes_title_author_mapped}\nTranscription: {transcription}"
    completion = client.chat.completions.create(
        model=GPT3_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": data},
        ]
    )
    return json.loads(completion.choices[0].message.content.replace("```json", "").replace("```", "").strip())


def bold_quote(quote, transcription, reasoning):
    prompt = '''bold the text in the quote that makes a complete thought in reference to the transcription and the reasoning. do not bold the entire quote, it will only be glanced at. you can bold multiple parts of the quote if relevant.
    
    return the edited full quote. YOU MUST REPEAT THE QUOTE VERBATIM.
    
    SAY NOTHING ELSE OTHER THAN THE EDITED QUOTE VERBATIM (AN EXACT COPY WITH BOLD HIGHLIGHTS as JSON in form { edited_quote }.
    
    Example:

    Transcription: Software developers never attain the same level of acclaim as authors, but in my opinion that is due to the way software is set up and the types of rewards one can or should expect.

    Reasoning for Quote Choice in Transcript: This quote is interesting because much like academics, software developers are often working on projects that are not immediately recognized by the public.

    Quote: <start>Most academics, and most authors I assume, have a more-or-less secret dream of writing a bestseller. We tell ourselves that we would like the money—and we would—but what we really crave is the recognition. We want our work, in all its craggy peculiarity, to elicit the respect, the passionate admiration, the love, of millions of people. And this secret dream feels to us so disreputable, so infantile, so desperate, that we protect ourselves against it by assuring ourselves that of course our work is too good to be popular. Then most of us—at least those of us raised in the great tradition of American populism—become ashamed of this defense, and in turn defend against it by an ironic confession of the very grandiosity against which the whole structure is a defense. Hence clever remarks like mine about “sufficient condition.”<end>


    returns the following. note that the quote is the same as the one given in the prompt it is VERBATIM. the only thing that changes is the bolded text.

    Edited Quote Only:
    {
        "edited_quote": "<start>**Most academics, and most authors I assume, have a more-or-less secret dream of writing a bestseller.** **We tell ourselves that we would like the money—and we would—but what we really crave is the recognition.** **We want our work, in all its craggy peculiarity, to elicit the respect,** the passionate admiration, the love, **of millions of people.** And **this secret dream feels to us so disreputable, so infantile, so desperate, that we protect ourselves against it by assuring ourselves that of course our work is too good to be popular.** Then **most of us—at least those of us raised in the great tradition of American populism—become ashamed of this defense, and in turn defend against it by an ironic confession of the very grandiosity against which the whole structure is a defense.** Hence clever remarks like mine about “sufficient condition.”<end>"
    }
    '''
    data = f"Transcription: {transcription}\n\nReasoning for Quote Choice in Transcript: {reasoning}\n\nQuote:\n<start>{quote}<end>\n\nEdited Quote Only:\n"
    completion = client.chat.completions.create(
        model=GPT3_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": data},
        ]
    )
    print(completion.choices[0].message.content)
    return json.loads(completion.choices[0].message.content.replace("```json", "").replace("```", "").strip())["edited_quote"].replace("<start>", "").replace("<end>", "")


# quote = choose_quote(quotes, transcription)
# print(quote)
# json_quote = json.loads(quote)
# bolded_quote = bold_quote(
#     quotes[json_quote['index']], transcription, json_quote['reasoning'])
# print(bolded_quote)
