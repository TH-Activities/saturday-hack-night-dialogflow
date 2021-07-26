const dialogflow = require('@google-cloud/dialogflow');
require('dotenv').config();
async function getResponse(query) {

    let result = ""
    const projectId = process.env.projectId;
    // console.log(projectId)
    const sessionId = '123456';
    const queries = [query]

    const languageCode = 'en';

    const sessionClient = new dialogflow.SessionsClient();

    async function detectIntent(
        projectId,
        sessionId,
        query,
        contexts,
        languageCode
    ) {
        // The path to identify the agent that owns the created intent.
        const sessionPath = sessionClient.projectAgentSessionPath(
            projectId,
            sessionId
        );

        // The text query request.
        const request = {
            session: sessionPath,
            queryInput: {
                text: {
                    text: query,
                    languageCode: languageCode,
                },
            },
        };

        if (contexts && contexts.length > 0) {
            request.queryParams = {
                contexts: contexts,
            };
        }

        const responses = await sessionClient.detectIntent(request);
        return responses[0];
    }

    async function executeQueries(projectId, sessionId, queries, languageCode) {
        // Keeping the context across queries let's us simulate an ongoing conversation with the bot
        let context;
        let intentResponse;
        for (const query of queries) {
            try {
                // console.log(`Sending Query: ${query}`);
                intentResponse = await detectIntent(
                    projectId,
                    sessionId,
                    query,
                    context,
                    languageCode
                );

                // console.log('Detected intent', intentResponse.queryResult.fulfillmentText);
                result = intentResponse.queryResult.fulfillmentText;
                // Use the context from this response for next queries
                // context = intentResponse.queryResult.outputContexts;
            } catch (error) {
                console.log(error);
            }
        }
    }

    await executeQueries(projectId, sessionId, queries, languageCode);
    // console.log("Response: ", result)
    return result;
}

module.exports = getResponse;

// getResponse("what is your age dear brother")