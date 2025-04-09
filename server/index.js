import express from 'express';

const app = express();
const port = 8080;

app.get('/search', (req, res) => {
    const q = req.query.q;

    console.log(q);

    res.send("Got it!");
});

app.listen(port, () => {
    console.log(`listening on port ${port}`)
});
