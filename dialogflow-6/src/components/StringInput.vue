<template>
  <div v-if="showInput === true">
    <form @submit.prevent="getSentiment()" class="sentiment-input-form">
      <label for="sentiment-text">so tell me, how do you feel right now?</label>
      <textarea
        id="sentiment-text"
        v-model="sentiment.sentimentText"
        rows="5"
        cols="50"
        maxlength="500"
        placeholder="Type here..."
        required
      ></textarea>
      <!-- <input type="submit" class="sentiment-input-submit" value="Submit" /> -->
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    <div class="results" v-if="showOutput === true">
      <p
        :style="{
          textTransform: 'uppercase',
          fontSize: '12px',
          marginBottom: '0px',
        }"
      >
        STATS FOR NERDS
      </p>
      <p class="magnitude">
        Magnitude: {{ sentiment.sentimentOutput.queryTextSentiment.magnitude }}
      </p>
      <p class="score">
        Score: {{ sentiment.sentimentOutput.queryTextSentiment.score }}
      </p>
      <p class="finalEmotion">
        It looks like you're {{ sentiment.finalEmotion }}
      </p>

      <img :src="memeSrc" alt="A meme for your mood." class="meme" />
    </div>
    <TextLoading :showLoadingOverlay="showTextLoading" />
  </div>
</template>

<script>
import DOMPurify from "dompurify";

import TextLoading from "@/components/TextLoading.vue";

export default {
  name: "StringInput",
  data() {
    return {
      sentiment: {
        sentimentText: null,
        sentimentOutput: null,
        finalEmotion: null,
      },
      showOutput: false,
      showTextLoading: false,
    };
  },
  components: {
    TextLoading,
  },
  computed: {
    cleanedSentimentText: function () {
      return DOMPurify.sanitize(this.sentiment.sentimentText);
    },
  },
  props: {
    showInput: {
      default: false,
      type: Boolean,
    },
  },
  methods: {
    getSentiment: async function () {
      // show loading stuff
      this.showTextLoading = true;

      // fetch backend API to get sentiment analysis
      let sentiment = await fetch(
        "/api/getSentimentValue?query=" +
          encodeURIComponent(this.cleanedSentimentText)
      );
      let response = await sentiment.json();
      this.sentiment.sentimentOutput = response;
      this.showOutput = true;
      this.showTextLoading = false;

      if (
        response.queryTextSentiment.score > 0 &&
        response.queryTextSentiment.score < 0.5
      ) {
        this.sentiment.finalEmotion = "both happy and sad?";
      } else if (response.queryTextSentiment.score > 0.5) {
        this.sentiment.finalEmotion = "definitely feeling joyful!";
      } else if (
        response.queryTextSentiment.score < 0 &&
        response.queryTextSentiment.score > -0.5
      ) {
        this.sentiment.finalEmotion = "feeling both happy and sad! Cheer up!";
      } else if (response.queryTextSentiment.score < -0.5) {
        this.sentiment.finalEmotion =
          "feeling down, but nothing that a meme can't improve!";
      }
    },
  },
};
</script>

<style scoped>
.sentiment-input-form {
  margin-top: 40px;
  margin-bottom: 40px;
}

.sentiment-input-form > * {
  display: block;
  margin-top: 20px;
  margin-bottom: 20px;
}

textarea {
  display: block;
  box-shadow: none;
  border: none;
  font-size: 72px;
  color: var(--black);
  transition: 150ms;
  width: 100%;
  background-color: var(--lightpink);
  font-size: 24px;
  font-family: var(--sans);
  padding: 20px 20px;
  border: 1px solid var(--rosy-brown);
  border-radius: 3px;
}

.magnitude,
.score {
  margin: 0px;
}

.finalEmotion {
  font-size: 24px;
  font-weight: 500;
  background-color: var(--magic-mint);
  border-radius: 3px;
  padding: 20px 20px;
  width: 100%;
}
</style>