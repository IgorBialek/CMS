<style>
  nav {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }

  #login,
  #register,
  #logout,
  #config {
    padding: 10px;
    margin: 10px;
  }

  #login:hover,
  #register:hover,
  #logout:hover,
  #config:hover {
    text-decoration: none;
  }

  #login,
  #logout {
    border: 1px solid green;
    border-radius: 10px;
    color: green;
  }

  #register {
    border: 1px solid blue;
    border-radius: 10px;
    color: blue;
  }

  #config {
    border: 1px solid orangered;
    border-radius: 10px;
    color: orangered;
  }
</style>

<script>
  import { replace } from "svelte-spa-router";

  let user = JSON.parse(localStorage.getItem("user"));

  //May refresh permissions

  const logout = () => {
    localStorage.setItem("user", null);
    replace("/");
  };
</script>

<div>
  <nav>
    <div id="navItems">
      <a>Icon</a>
      <a>Features</a>
      <a>Pricing</a>
      <a>FAQs</a>
      <a>About</a>
    </div>
    <div id="userActions">
      {#if !user}
        <a href="/#/Login" id="login">Login</a>
        <a href="/#/Register" id="register">Register</a>
      {/if}

      {#if user.permission == "admin"}
        <a href="/#/Configuration" id="config">Configuration</a>
      {/if}

      {#if user}
        <a href="/" id="logout" on:click="{logout}">Logout</a>
      {/if}
    </div>
  </nav>

  <!-- <div id="slider">
        <div></div>
        <div></div>
    </div>

    <div id="news"></div>

    <main></main>

    <footer></footer> -->
</div>
