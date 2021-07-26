const express = require("express");
const df = require("./dialogflow.js");
const bodyParser = require('body-parser')



const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.set("view engine", "ejs")

let reply = "";
app.get('/', function(req, res) {
    res.render('index', { reply: reply });
    reply = "";
})

app.post("/", async function(req, res) {
    query = req.body.query;


    reply = await df(query);

    res.redirect("/");
})
let port = process.env.PORT || 5000;





app.listen(port, function() {
    console.log("server running on port " + port)
})