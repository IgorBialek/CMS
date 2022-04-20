<script>
  import { onMount } from "svelte";
  import saveUserHandler from "./../utils/saveUsersHandler"

  let user = JSON.parse(localStorage.getItem("user"))
  let users = [];
  let repeatedPasswords = []
  let error = false
  let incorrectness = []

  onMount(async () => {
    if(user.permission != "admin") {
      console.log(user)
      users = (await (await fetch("/getUsers")).json()).users.filter(u => u._id == user.email)
    }else {
      users = (await (await fetch("/getUsers")).json()).users;
    }



    users.forEach(user => {
      repeatedPasswords.push(user.password)
    });
  });

  const validate = () => {
    incorrectness = users.filter((user, i) => user.password != repeatedPasswords[i]).length

    if(incorrectness > 0) {
      error = true
    }
    else {
      error = false
    }
  }
</script>

<div class="usersContainer">
  <!-- <div class="userContainer title">
    <div>Login</div>
    <div>Password</div>
    <div>Permission</div>
  </div> -->
  {#each users as u, i}
    <div class="userContainer">
      <input bind:value={u._id}/>
      <input bind:value={u.password}/>
      <input bind:value={repeatedPasswords[i]}/>
      {#if user.permission == "admin"}
      <select bind:value={u.permission}>
        <option value="admin">admin</option>
        <option value="permitted">permitted</option>
        <option value="user">user</option>
      </select>
      {/if}
    </div>
  {/each}
  <button
      on:click={() => {
validate()
if(!error) {
  saveUserHandler(users);
}


      }}>SAVE</button
    >
    {#if error}
    <h1>Some passwords are not the same</h1>
    {/if}
</div>

<style>
  .usersContainer {
    margin: 100px 0;
    display: flex;
    width: 100%;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .userContainer {
    width: 75%;
    font-size: 20px;
    margin: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .userContainer > div {
    width: 25%;
    text-align: center;
  }

  .title {
    font-weight: bold;
    font-size: 25px;
    margin: 0;
    padding: 0;
  }
</style>
