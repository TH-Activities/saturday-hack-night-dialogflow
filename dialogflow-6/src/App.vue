<template>
  <div id="app">
    <h1>mood-o-(meme)ter</h1>
    <div class="description">
      <p>your current mood based on memes</p>
    </div>
    <StringInput />
  </div>
</template>

<script>
import StringInput from "@/components/StringInput.vue";

export default {
  name: "App",
  components: {
    StringInput: StringInput,
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap");

:root {
  --sans: "Inter", "Helvetica", sans-serif;
  --baby-blue-eyes: #9ac4f8ff;
  --magic-mint: #99edccff;
  --rosy-brown: #cb958eff;
  --blush: #e36588ff;
  --jazzberry-jam: #9a275aff;
}

body {
  font-family: var(--sans);
  margin: 0 auto;
  max-width: 700px;
  background-color: var(--baby-blue-eyes);
  padding-top: 40px;
  padding-bottom: 40px;
}

h1 {
  color: var(--jazzberry-jam);
  text-align: center;
  margin-bottom: 0px;
}

button {
  display: block;
  margin-top: 15px;
  box-shadow: none;
  color: white;
  font-family: var(--sans);
  transition: 150ms;
  padding: 10px 20px;
  cursor: pointer;
  background-color: var(--blush);
  border-radius: 3px;
  font-size: 14px;
  border: none;
  box-shadow: 0 2.3px 1.9px rgba(0, 0, 0, 0.013),
    0 5.4px 4.3px rgba(0, 0, 0, 0.019), 0 9.7px 7.7px rgba(0, 0, 0, 0.023),
    0 16.1px 12.8px rgba(0, 0, 0, 0.027), 0 26.5px 21.2px rgba(0, 0, 0, 0.031),
    0 46.2px 37px rgba(0, 0, 0, 0.037), 0 100px 80px rgba(0, 0, 0, 0.05);
  transition: 200ms;
}

button:hover {
  box-shadow: none;
  transition: 200ms;
}

.description p {
  text-align: center;
  font-size: 1.5em;
  margin-top: 0px;
}
</style>
