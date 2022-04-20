import { push } from "svelte-spa-router";

export default async function saveUsersHandler(users) {

  let user = JSON.parse(localStorage.getItem("user"))
  let oldUsers = []

    if(user.permission != "admin") {
      localStorage.setItem("user", JSON.stringify({email: users[0]._id, password: users[0].password, permission: users[0].permission}));
      oldUsers = (await (await fetch("/getUsers")).json()).users.filter(u => u._id == user.email)
    }else {

      oldUsers = (await (await fetch("/getUsers")).json()).users;
    }

  users = users.map((user, i) => {
    return {...user, old_id: oldUsers[i]._id}
  })



  console.log(users)
  await fetch("/updateUsers", {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({users}),
  });

  push("/");
}
