export default async function saveComment(config) {
  await fetch("/saveConfiguration", {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });
  // localStorage.setItem("configuration", JSON.stringify(config));
}
