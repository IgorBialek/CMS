<script>
  import { onMount } from "svelte";
  import saveUserHandler from "./../utils/saveUsersHandler";

  let user = JSON.parse(localStorage.getItem("user"));
  let users = [];
  let repeatedPasswords = [];
  let error = false;
  let incorrectness = [];

  onMount(async () => {
    if (user.permission != "admin") {
      console.log(user);
      users = (await (await fetch("/getUsers")).json()).users.filter(
        (u) => u._id == user.email
      );
    } else {
      users = (await (await fetch("/getUsers")).json()).users;
    }

    users.forEach((user) => {
      repeatedPasswords.push(user.password);
    });
  });

  const validate = () => {
    incorrectness = users.filter(
      (user, i) => user.password != repeatedPasswords[i]
    ).length;

    let nameError = false;

    users.forEach((u, i) => {
      users.forEach((u_two, i_two) => {
        if (!nameError) {
          if (u._id == u_two._id && i != i_two) {
            console.log("AAA");
            nameError = true;
          }
        }
      });
    });

    console.log(nameError);

    if (incorrectness > 0 || nameError) {
      error = true;
    } else {
      error = false;
    }

    console.log("ERROR", error);
  };
</script>

<div class="usersContainer">
  <div class="userContainer title" />
  {#each users as u, i}
    {#if u._id != "admin"}
      <div class="userContainer">
        <div>
          <div>Login</div>
          <input bind:value={u._id} />
        </div>
        <div>
          <div>Password</div>
          <input bind:value={u.password} />
        </div>

        <div>
          <div>Repeated Password</div>
          <input bind:value={repeatedPasswords[i]} />
        </div>
        {#if user.permission == "admin"}
          <div>
            <div>Permission</div>

            <select bind:value={u.permission}>
              <option value="admin">admin</option>
              <option value="permitted">permitted</option>
              <option value="user">user</option>
            </select>
          </div>
        {/if}
      </div>
    {/if}
  {/each}
  <button
    on:click={() => {
      validate();
      if (!error) {
        saveUserHandler(users);
      }
    }}>SAVE</button
  >
  {#if error}
    <h1 class="error">Some passwords are not the same or names are repeated</h1>
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
    flex-wrap: wrap;
  }

  .userContainer > div {
    display: flex;
    justify-content: center;
    text-align: center;
    flex-direction: column;
    flex-wrap: wrap;
    align-items: center;
  }

  .userContainer > div > div {
    text-align: center;
    font-size: 12px;
    margin: 5px;
  }

  .userContainer input {
    display: flex;
    justify-content: center;
    width: 300px;
    text-align: center;
  }

  .title {
    font-weight: bold;
    font-size: 25px;
    margin: 0;
    padding: 0;
  }
</style>
