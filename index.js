const express = require('express');
const app = express();

// let quoteData = {
//     "text": `**"The revolutions in biotech and infotech will give us control of the world inside us and will enable us to engineer and manufacture life.** We will learn how to design brains, extend lives, and kill thoughts at our discretion. Nobody knows what the consequences will be. **Humans were always far better at inventing tools than using them wisely.** It is easier to manipulate a river by building a dam than it is to predict all the complex consequences this will have for the wider ecological system. Similarly, it will be easier to redirect the flow of our minds than to divine what that will do to our personal psychology or to our social systems."`,
//     "title": "Civilized to Death: The Price of Progress",
//     "author": "Christopher Ryan",
// };

app.use(express.json()); // for parsing application/json
app.use(express.static('public'));

const STYLING = true

app.get('/', (req, res) => {
    res.sendFile(__dirname + (STYLING ? '/public/static-index.html' : '/public/live-index.html'));
});

app.post('/new-quote-data', (req, res) => {
    console.log('POST request received');
    quoteData = req.body;
   // render index.html with new quoteData
   res.json(quoteData);
});

app.get('/quote-data', (req, res) => {
    if (!quoteData) {
        res.json({error: 'No quote data found'});
    }
    console.log('GET request received');
    res.json(quoteData);
})

app.listen(3000, () => {
    console.log('Server is listening on port 3000');
});