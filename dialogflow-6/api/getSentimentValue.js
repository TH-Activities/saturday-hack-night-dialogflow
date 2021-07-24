// Imports the Dialogflow client library
const dialogflow = require("@google-cloud/dialogflow").v2;

// use the uuid package to generate a random identifier for the session
const uuid = require("uuid");

module.exports = (req, res) => {
  // Instantiate a DialogFlow client.
  const sessionClient = new dialogflow.SessionsClient({
    credentials: {
      private_key: process.env.PRIVATE_KEY,
      client_email: process.env.CLIENT_EMAIL,
    },
  });

  const projectId = "tinkerhub-hack-night-otbq";
  const sessionId = uuid.v4();
  const query = decodeURIComponent(req.query.query);
  const languageCode = "en-US";

  // Define session path
  const sessionPath = sessionClient.projectAgentSessionPath(
    projectId,
    sessionId
  );

  async function detectIntentandSentiment() {
    // The text query request.
    const request = {
      session: sessionPath,
      queryInput: {
        text: {
          text: query,
          languageCode: languageCode,
        },
      },
      queryParams: {
        sentimentAnalysisRequestConfig: {
          analyzeQueryTextSentiment: true,
        },
      },
    };

    // Send request and log result
    const responses = await sessionClient.detectIntent(request);
    console.log("Detected intent");

    //   console.log(responses);

    const result = responses[0].queryResult;
    //   console.log(`  Query: ${result.queryText}`);
    //   console.log(`  Response: ${result.fulfillmentText}`);

    if (result.intent) {
      console.log(`  Intent: ${result.intent.displayName}`);
    } else {
      console.log("  No intent matched.");
    }

    if (result.sentimentAnalysisResult) {
      res.status(200).json(result.sentimentAnalysisResult);
    } else {
      console.log("No sentiment Analysis Found");
      res.status(400).send("No sentiment Analysis Found");
    }
  }

  detectIntentandSentiment();
};
