<template>
  <form @submit.prevent="getSentiment()" class="sentiment-input-form">
    <label for="sentiment-text">so tell me, how do you feel right now?</label>
    <textarea
      id="sentiment-text"
      v-model="sentimentText"
      rows="5"
      cols="50"
      maxlength="500"
      placeholder="Type here..."
    ></textarea>
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
</template>

<script>
import DOMPurify from "dompurify";

export default {
  name: "StringInput",
  data() {
    return {
      sentimentText: null,
    };
  },
  computed: {
    cleanedSentimentText: function () {
      return DOMPurify.sanitize(this.sentimentText);
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
</style>