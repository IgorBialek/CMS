<script>
  import { link, replace } from "svelte-spa-router";

  let user = JSON.parse(localStorage.getItem("user"));

  let configuration = JSON.parse(localStorage.getItem("configuration"));
  let styles = configuration.templates[configuration.selectedTemplate].styles;
  let components =
    configuration.templates[configuration.selectedTemplate].components;
  let menu = configuration.templates[configuration.selectedTemplate].menu;
  let footer = configuration.templates[configuration.selectedTemplate].footer;

  //May refresh permissions

  const logout = () => {
    localStorage.setItem("user", null);
    replace("/");
  };
</script>

<div
  class="homeContainer"
  style="--fontSize: {styles.fontSize}px; --fontFamily: {styles.selectedFont}; --lightColor: {styles
    .colors.lightColor}; --mediumColor: {styles.colors
    .mediumColor}; --darkColor: {styles.colors
    .darkColor}; --navDirection: {menu.type == 'vertical' ? 'column' : 'none'}"
>
  <nav>
    <div class="navItems">
      {#each menu.articles as article}
        <a href={`/#/article/${article.link}`}>{article.title}</a>
      {/each}
    </div>
    <div class="userActions">
      {#if !user}
        <a href="/#/Login" class="login">Login</a>
        <a href="/#/Register" class="register">Register</a>
      {/if}

      {#if user && user.permission == "admin"}
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

  <footer>
    <div class="footer">
      {#each footer.links as link}
        <a href={`/#/${link.link}`}>{link.title}</a>
      {/each}
    </div>
    <div>Michał Dubrowski & Igor Białek 3P</div>
  </footer>
</div>

<style>
  @import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");
  @import url("https://fonts.googleapis.com/css2?family=Quicksand&display=swap");
  @import url("https://fonts.googleapis.com/css2?family=Oswald&display=swap");
  /*
 font-family: 'Roboto', sans-serif;
 font-family: 'Quicksand', sans-serif;
font-family: 'Oswald', sans-serif;
 */

  .homeContainer {
    margin: 0 !important;
    font-size: var(--fontSize);
    font-family: var(--fontFamily), sans-serif;
  }

  nav {
    width: 100%;
    height: 75px;
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .userActions {
    margin: 25px;
    display: flex;
  }

  .userActions > a {
    margin: 10px;
  }

  .navItems {
    margin: 25px;
    height: 100%;
    display: flex;
    flex-direction: var(--navDirection);
    align-items: center;
    justify-content: center;
  }

  .navItems > a {
    margin: 10px;
  }

  .login,
  .register,
  .logout,
  .config {
    padding: 10px;
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
    background-color: var(--mediumColor);
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
    background-color: var(--lightColor);
  }

  .newsContent a {
    padding: 10px;
    color: white;
    background-color: var(--darkColor);
    align-self: start;
  }

  .homeContainer {
    display: flex;
    flex-direction: column;
    margin: 25px;
  }

  footer {
    border-top: 1px solid black;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .footer {
    width: 33%;
    margin: 15px;
    display: flex;
    justify-content: space-around;
  }
</style>
