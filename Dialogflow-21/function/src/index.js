const express = require('express');
const app = express();
const dff = require('dialogflow-fulfillment');


app.post('/',express.json(),(req,res) =>{
     agent = new dff.WebhookClient({
        request:req,
        response:res
    })
    //Fulfillment fn for Addition
    function addition(agent){
        const num1 = agent.parameters.number1;
        const num2 = agent.parameters.number2;
        const sum = num1 + num2;
        agent.add(sum + ' ');
    }
    //Fulfillment fn for Subtraction
    function subtraction(agent){
        const num1 = agent.parameters.number1;
        const num2 = agent.parameters.number2;
        const difference = num1 - num2;
        agent.add(difference + ' ');
    }


    var intentMap = new Map();
    intentMap.set('Addition',addition);
    intentMap.set('Subtraction',subtraction);


    agent.handleRequest(intentMap);
})



//Listening to 3000
app.listen(3000, () => {
    console.log('It is working')
})