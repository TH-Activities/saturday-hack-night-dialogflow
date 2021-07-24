let user_form = document.querySelector("form");
let user_input = document.querySelector("#search");

window.onload = () => {
  user_input.focus();
};

user_form.onsubmit = async (e) => {
  e.preventDefault();

  // Put API fetch requests here onwards
};
