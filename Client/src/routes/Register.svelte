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
      const res = await fetch("/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify(user),
      });

      const response = await res.json();

      console.log(response);

      if (response.errorMessage) {
        errorMessage = response.errorMessage;
        error = true
        return;
      }

      localStorage.setItem("user", JSON.stringify(response));

      replace("/");
    } 
  };

  const valid = () => {
    if (email && password && repPassword) {
      if(password == repPassword) {
        console.log("AAAA")
        return true
      }else {
        errorMessage = "Passwords are not the same";
        return false
      }
    } else {
      errorMessage = "Please fill all inputs";
      return false;
    }
  };
</script>

<div class="centerContainer">
  <h1>Register</h1>
  <div class="userForm">
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
  </div>
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
