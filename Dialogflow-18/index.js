const express = require("express");
const df = require("./dialogflow.js");



const app = express();
app.use(express.json());
app.set("view engine", "ejs")
app.get('/', function(req, res) {
    res.render('index');
})

app.post("/", async function(req, res) {
    query = req.body.query;

    reply = await df(query);
    console.log(reply);
    res.redirect("/");
})



app.listen(5000, function() {
    console.log("server running")
})