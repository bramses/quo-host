from openai_utils import predict_paragraph

print('Simulating a "real" transcription process...')
res = predict_paragraph('''In the last issue, I made the case that the widely-discussed-but-never-acted-upon suffering of social media is caused by a saturation point that we have long past by avoiding acknowledging the sunk cost fallacies of our "profiles". I claimed that the remedy for this supersaturated state is to "hit the reset button", to download the data and restart your digital profile's existence (or delete it all together!).

The inspiration for that issue ironically came from the one you are reading right now, the issue posted after. I had been meditating on the value of craft, art, business, and human creativity in the era of "content creation schedules". The seed of last issue's craft argument was that if you are truly good at what you do and have a strong base of self-esteem, deleting your profile should be an overall good thing for your craft, as it will allow you to prove it wasn't luck that got you to success in the first place.

Specifically, I had been trying to divine the value of effort being put into a personal website. After all, time is limited and everything we do has an expiration date. Surely, there must be a more effective use of one's time, yes?

The answers I found in this process took me from the caves of Lascaux, to the Twitter page of Mr. Beast.

Following is a short journey into incentive structure, motivation, and finding what it means to be an artist.

Let's start in 1905.

In the first decade of the 20th century, writer W.J. Dawson found a cottage to live in.

Dawson spent the beginning of his career in London as a salaryman, and began to tire of the hypocrisies of urbanity and industrialization. He was disgruntled with how mundane life had become under the thumb of his employer, the noise of his crowded London neighborhood and his neighbors in his posh flat, and most critically, his desires to have novelty and beauty in life.

As a response, he began to plan his flight into the "wilderness",
''')
print(res)
