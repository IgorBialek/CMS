<script>
  import { replace } from "svelte-spa-router";

  let email = "";
  let password = "";
  let errorMessage = "";
  let error = false;

  const handleRegister = async () => {
    error = !valid();

    if (!error) {
      let user = { email, password };

      //fetch server
      const res = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(user),
      });

      const response = await res.json();

      console.log(response);

      if (response.errorMessage) {
        errorMessage = response.errorMessage;
        error = true;
        return;
      }

      //Set user from response
      localStorage.setItem("user", JSON.stringify(response));

      replace("/");
    } else {
      errorMessage = "Please fill all inputs";
    }
  };

  const valid = () => {
    if (email && password) {
      return true;
    } else {
      errorMessage = "Please fill all inputs";
      return false;
    }
  };
</script>

<div class="centerContainer">
  <h1>Login</h1>
  <div class="userForm">
    <label>Email</label>
    <input type="email" bind:value={email} autocomplete="username" />
    <label>Password</label>
    <input type="password" autocomplete="new-password" bind:value={password} />
    {#if error}
      <p class="error">{errorMessage}</p>
    {/if}
    <button class="userFormButton" on:click={handleRegister}>Login</button>
  </div>
</div>

<style>
  .centerContainer {
    flex-direction: column;
    display: flex;
    width: 100%;
    justify-content: center;
    align-items: center;
    font-weight: bold;
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
