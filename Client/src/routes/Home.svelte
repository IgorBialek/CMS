<script>
  import { link, replace } from "svelte-spa-router";

  let user = JSON.parse(localStorage.getItem("user"));

  let configuration = JSON.parse(localStorage.getItem("configuration"));
  let styles = configuration.styles;
  let components = configuration.components;

  //May refresh permissions

  const logout = () => {
    localStorage.setItem("user", null);
    replace("/");
  };
</script>

<div class="homeContainer" style="font-size: {styles.fontSize};">
  <nav>
    <div class="navItems">
      <a>Icon</a>
      <a>Features</a>
      <a>Pricing</a>
      <a>FAQs</a>
      <a>About</a>
    </div>
    <div class="userActions">
      {#if !user}
        <a href="/#/Login" class="login">Login</a>
        <a href="/#/Register" class="register">Register</a>
      {/if}

      {#if user.permission == "admin"}
        <a href="/#/Configuration" class="config">Configuration</a>
      {/if}

      {#if user}
        <a href="/" class="logout" on:click={logout}>Logout</a>
      {/if}
    </div>
  </nav>

  <div class="componentsContainer">
    {#each components as comp}
      {#if comp.visible}
        <div>
          <h1>{comp.name}</h1>
          {#if comp.news.length > 0}
            <div class="newsContainer">
              {#each comp.news as news}
                <div class="newsSingle">
                  <div class="newsTitle">{news.title}</div>
                  <div class="newsContent">
                    <h2>{news.headline}</h2>
                    <p>{news.text}</p>
                    <a href={`/#/${news.link}`}>Go to {news.link}</a>
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      {/if}
    {/each}
  </div>

  <!-- <div id="slider">
        <div></div>
        <div></div>
    </div>

    <div id="news"></div>

    <main></main> -->

  <footer>Michał Dubrowski & Igor Białek 3P</footer>
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");
  @import url("https://fonts.googleapis.com/css2?family=Quicksand&display=swap");
  @import url("https://fonts.googleapis.com/css2?family=Inconsolata&display=swap");

  /*
 font-family: 'Roboto', sans-serif;
 font-family: 'Quicksand', sans-serif;
 font-family: 'Inconsolata', monospace;
 */

  nav {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }

  .login,
  .register,
  .logout,
  .config {
    padding: 10px;
    margin: 10px;
  }

  .login:hover,
  .register:hover,
  .logout:hover,
  .config:hover {
    text-decoration: none;
  }

  .login,
  .logout {
    border: 1px solid green;
    border-radius: 10px;
    color: green;
  }

  .register {
    border: 1px solid blue;
    border-radius: 10px;
    color: blue;
  }

  .config {
    border: 1px solid orangered;
    border-radius: 10px;
    color: orangered;
  }
  .componentsContainer {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    text-align: center;
  }

  .componentsContainer > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .newsContainer {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: stretch;
  }

  .newsSingle {
    margin: 50px;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    width: 25%;
  }

  .newsTitle {
    padding: 10px;
    background-color: gray;
    text-align: left;
    color: white;
  }

  .newsContent h2 {
    margin: 0;
  }

  .newsContent {
    padding: 25px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: left;
    color: white;
    background-color: darkgray;
  }

  .newsContent a {
    padding: 10px;
    color: white;
    background-color: rgb(59, 59, 59);
    align-self: start;
  }

  .homeContainer {
    display: flex;
    flex-direction: column;
    margin: 25px;
  }

  footer {
    width: 300px;
    position: fixed;
    bottom: 20px;
    right: calc(50% - 185px);
  }
</style>
