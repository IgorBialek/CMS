<script>
  import { replace } from "svelte-spa-router";

  let email = "";
  let password = "";
  let repPassword = "";
  let errorMessage = "";
  let error = false;

  const handleRegister = async () => {
    error = !valid();

    if (!error) {
      let user = { email, password, permission: "admin" };

      //fetch server
      //   const response = await fetch("?", {
      //         method: 'POST',
      //             'Content-Type': 'application/json',
      //         },
      //         body: JSON.stringify(user),
      //     });

      //   if (response.errorMessage) {
      //     errorMessage = response.errorMessage;
      //     return
      //   }

      localStorage.setItem("user", JSON.stringify(user));

      replace("/");
    } else {
      errorMessage = "Please fill all inputs";
    }
  };

  const valid = () => {
    if (email && password && repPassword && password == repPassword) {
      return true;
    } else {
      errorMessage = "Please fill all inputs";
      return false;
    }
  };
</script>

<div class="centerContainer">
  <h1>Register</h1>
  <form class="userForm">
    <label>Email</label>
    <input type="email" bind:value={email} autocomplete="username" />
    <label>Password</label>
    <input type="password" autocomplete="new-password" bind:value={password} />
    <label>Repeat password</label>
    <input
      type="password"
      autocomplete="new-password"
      bind:value={repPassword}
    />
    {#if error}
      <p>{errorMessage}</p>
    {/if}
    <button class="userFormButton" on:click={handleRegister}>Register</button>
  </form>
</div>

<style>
  .centerContainer {
    flex-direction: column;
    display: flex;
    width: 100%;
    justify-content: center;
    align-items: center;
  }

  .userForm {
    padding: 25px;
    border-radius: 10px;
    border: 1px solid black;
    display: flex;
    flex-direction: column;
  }

  .userForm label {
    margin: 5px 0;
  }

  .userForm input {
    width: 250px;
  }

  .userFormButton {
    align-self: center;
    width: 100px;
    margin-top: 25px;
  }
</style>
