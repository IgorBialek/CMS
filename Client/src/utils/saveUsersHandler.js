import { push } from "svelte-spa-router";

export default async function saveUsersHandler(config) {

  console.log({users: config})
  await fetch("/updateUsers", {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({users: config}),
  });
  // localStorage.setItem("configuration", JSON.stringify(config));
  push("/");
}
