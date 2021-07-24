import { apiReq } from "./api.js";

let user_form = document.querySelector("form");
let user_input = document.querySelector("#search");

window.onload = () => {
  user_input.focus();
};

user_form.onsubmit = async (e) => {
  e.preventDefault();

  // Put API fetch requests here onwards

  // Mood response
  let mood;
  let img_link;
  fetch(`https://defiant-tabby-climb.glitch.me/meme/"${user_input.value}"`)
    .then((resp) => {
      return resp.json();
    })
    .then((data) => {
      mood = data;
    })
    .then(() => {
      img_link = apiReq(mood, user_input.value);
      return img_link;

    })
  // .then((data) => { console.log(img_link); return img_link; });
  // Meme response
};
