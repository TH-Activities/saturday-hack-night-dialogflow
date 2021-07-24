export function apiReq(mood, text) {
  const param1 = {
    template_id: 101287,
    //happy kid
    username: "jojo6789",
    password: "jojo@007",
    font: "arial",
    text0: text,
  };
  const param2 = {
    //pain harold
    template_id: 27813981,
    username: "jojo6789",
    password: "jojo@007",
    font: "arial",
    text0: text,
  };
  const param3 = {
    //sad pablo escobar
    template_id: 80707627,
    username: "jojo6789",
    password: "jojo@007",
    font: "arial",
    text0: text,
  };
  const param4 = {
    //this is fine dog
    template_id: 55311130,
    username: "jojo6789",
    password: "jojo@007",
    font: "arial",
    text0: text,
  };
  const param5 = {
    //dicaprio laughing
    template_id: 259237855,
    username: "jojo6789",
    password: "jojo@007",
    font: "arial",
    text0: text,
  };
  const param6 = {
    //scared cat
    template_id: 4173692,
    username: "jojo6789",
    password: "jojo@007",
    font: "arial",
    text0: text,
  };
  const param7 = {
    //grumpy cat
    template_id: 405658,
    username: "jojo6789",
    password: "jojo@007",
    font: "arial",
    text0: text,
  };
  const param0 = {
    //guy holding cardboard
    template_id: 216951317,
    username: "jojo6789",
    password: "jojo@007",
    font: "arial",
    text0: text,
  };
  let params;
  switch (mood) {
    case "happy":
      params = param1;
      break;
    case "pain":
      params = param2;
      break;
    case "sad":
      params = param3;
      break;
    case "trouble":
      params = param4;
      break;
    case "laugh":
      params = param5;
      break;
    case "scared":
      params = param6;
      break;
    case "grumpy":
      params = param7;
      break;
    default:
      params = param0;
  }

  let url = `https://api.imgflip.com/caption_image?=${Object.keys(params)
    .map((key) => key + "=" + params[key])
    .join("&")}`;

  console.log(url);
  fetch(url)
    .then((response) => response.json())
    .then((data) => console.log(data));

  // try {
  //   let json = await response.json();
  //   return json.data.url;
  // } catch (error) {
  //     console.log(error);
  // }
}
