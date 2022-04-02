<script>
  import { link, replace } from "svelte-spa-router";

  let user = JSON.parse(localStorage.getItem("user"));

  let components = JSON.parse(localStorage.getItem("configuration"));

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
        <a href="/" id="logout" on:click={logout}>Logout</a>
      {/if}
    </div>
  </nav>

  <div id="componentsContainer">
    {#each components as comp}
      {#if comp.visible}
        <div>
          <h1>{comp.name}</h1>
          {#if comp.news.length > 0}
            <div id="newsContainer">
              {#each comp.news as news}
                <div id="newsSingle">
                  <div id="newsTitle">{news.title}</div>
                  <div id="newsContent">
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

    <main></main>

    <footer></footer> -->
</div>

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
  #componentsContainer {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    text-align: center;
  }

  #componentsContainer > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  #newsContainer {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: flex-start;
  }

  #newsSingle {
    width: 25%;
    margin: 50px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: gainsboro;
  }

  #newsTitle {
    background-color: gray;
    width: 100%;
    color: white;
    text-align: left;
  }

  #newsContent h2 {
    margin: 0;
  }

  #newsContent {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 25px;
    text-align: left;
  }

  #newsContent a {
    background-color: darkgray;
    padding: 10px;
  }
</style>
