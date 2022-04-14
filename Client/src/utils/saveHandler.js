import { push } from "svelte-spa-router";

export default async function saveHandler(config) {
  await fetch("/saveConfiguration", {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });
  localStorage.setItem("configuration", JSON.stringify(config));
  push("/Configuration");
}
