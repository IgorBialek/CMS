import { push } from "svelte-spa-router";

export default function saveHandler(config) {
  localStorage.setItem("configuration", JSON.stringify(config));
  push("/Configuration");
}
