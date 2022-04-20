<script>
  import { link, replace } from "svelte-spa-router";
  import { onMount, onDestroy } from "svelte";
  import Article from "./Article.svelte";

  let user = JSON.parse(localStorage.getItem("user"));

  let configuration = null;
  let styles;
  let components;
  let menu;
  let sliderSelectors;
  let intervals = [];

  const onInterval = (callback, milliseconds) => {
    const interval = setInterval(callback, milliseconds);

    intervals.push(interval);
  };

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;
    styles = configuration.templates[configuration.selectedTemplate].styles;
    components =
      configuration.templates[configuration.selectedTemplate].components;
    menu = configuration.templates[configuration.selectedTemplate].menu;
    sliderSelectors = configuration.templates[
      configuration.selectedTemplate
    ].components
      .map((comp, i) => {
        return {
          compIndex: i,
          selectedImage: 0,
          slider: comp.slider,
        };
      })
      .filter((comp) => comp.slider);

    sliderSelectors.forEach((selector, i) => {
      if (selector.slider.images.length > 1) {
        onInterval(() => {
          console.log("III");
          if (selector.selectedImage == selector.slider.images.length - 1) {
            selector.selectedImage = 0;
          } else {
            selector.selectedImage += 1;
          }

          sliderSelectors[i] = selector;
        }, selector.slider.switchTime * 1000);
      }
    });
  });

  onDestroy(() => {
    intervals.forEach((interval) => clearInterval(interval));
  });

  const sliderSelectorChange = (direction, compIndex) => {
    let slider = sliderSelectors.filter((sel) => sel.compIndex == compIndex)[0];

    if (direction == "down") {
      if (slider.selectedImage > 0) {
        sliderSelectors = sliderSelectors.map((sel) => {
          if (sel.compIndex == compIndex) {
            return { ...sel, selectedImage: sel.selectedImage - 1 };
          } else return sel;
        });
      } else {
        sliderSelectors = sliderSelectors.map((sel) => {
          if (sel.compIndex == compIndex) {
            return { ...sel, selectedImage: slider.slider.images.length - 1 };
          } else return sel;
        });
      }
    } else if (direction == "up") {
      if (slider.selectedImage < slider.slider.images.length - 1) {
        sliderSelectors = sliderSelectors.map((sel) => {
          if (sel.compIndex == compIndex) {
            return { ...sel, selectedImage: sel.selectedImage + 1 };
          } else return sel;
        });
      } else {
        sliderSelectors = sliderSelectors.map((sel) => {
          if (sel.compIndex == compIndex) {
            return { ...sel, selectedImage: 0 };
          } else return sel;
        });
      }
    }

    console.log(sliderSelectors);
  };

  //May refresh permissions

  const logout = () => {
    localStorage.setItem("user", null);
    replace("/");
  };
</script>

{#if configuration}
  <div
    class="homeContainer"
    style="--fontSize: {styles.fontSize}px  !important; --fontFamily: {styles.selectedFont} !important; --lightColor: {styles
      .colors.lightColor}; --mediumColor: {styles.colors
      .mediumColor}; --darkColor: {styles.colors
      .darkColor}; --navDirection: {menu.type == 'vertical'
      ? 'column'
      : 'none'}; --containerDirection:{menu.type == 'vertical'
      ? 'none'
      : 'column'}; --navWidth:{menu.type == 'vertical'
      ? '10%'
      : 'calc(100% - 30px)'}; --navJustify:{menu.type == 'vertical'
      ? 'flex-start'
      : 'space-between'}"
  >
    <nav>
      <div class="navItems">
        <a href="/#/Gallery">Gallery</a>
        {#each menu.articles as article}
          {#if article.visible}
            <a href={`/#/article/${article.link}`}>{article.title}</a>
          {/if}
        {/each}
      </div>
      <div class="userActions">
        <a href="/#/Search" class="search">Search</a>

        {#if user && user.permission != "user"}
          <a href="/#/Configuration" class="config">Configuration</a>
        {/if}

        {#if user}
          <a href="/#/Users" class="users">Users</a>
          <a href="/" class="logout" on:click={logout}>Logout</a>
        {/if}

        {#if !user}
          <a href="/#/Login" class="login">Login</a>
          <a href="/#/Register" class="register">Register</a>
        {/if}
      </div>
    </nav>

    <div class="componentsContainer">
      {#each components as comp, i}
        {#if comp.visible}
          <div id={comp.name} class="sectionContainer">
            <!-- <h1>{comp.name}</h1> -->
            {#if comp.slider}
              <div class="sliderContainer">
                <div class="sliderDescription">
                  <p>{comp.slider.description}</p>
                </div>
                <div
                  class="sliderDown"
                  on:click={() => {
                    sliderSelectorChange("down", i);
                  }}
                >
                  <p>{"<"}</p>
                </div>
                <div
                  class="sliderUp"
                  on:click={() => {
                    sliderSelectorChange("up", i);
                  }}
                >
                  <p>{">"}</p>
                </div>
                <img
                  alt="slider"
                  src={comp.slider.images[
                    sliderSelectors.filter((slider) => slider.compIndex == i)[0]
                      .selectedImage
                  ]}
                />
              </div>
            {/if}
            {#if comp.news.length > 0}
              <div class="newsContainer">
                {#each comp.news as news}
                  <div class="newsSingle">
                    <div class="newsTitle">{news.title}</div>
                    <div class="newsContent">
                      <h2>{news.headline}</h2>
                      <p>{news.text}</p>
                      <a href={`/#/article/${news.link}`}>Go to news</a>
                    </div>
                  </div>
                {/each}
              </div>
            {/if}
            {#if comp.content}
              <div class="contentContainer">
                <div class="contentText">
                  <h2>{comp.content.title}</h2>
                  <p>{comp.content.text}</p>
                </div>
                <img alt="Nothing here" src={comp.content.image} />
              </div>
            {/if}
          </div>
        {/if}
      {/each}
      <footer>
        <div class="footer">
          {#each components as comp}
            <a href={`#${comp.name}`}>{comp.name}</a>
          {/each}
        </div>
        <div>Michał Dubrowski & Igor Białek 3P</div>
      </footer>
    </div>

    <!-- <div id="slider">
      <div></div>
      <div></div>
  </div>

  <div id="news"></div>

  <main></main> -->
  </div>
{/if}

<style>
  @import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");
  @import url("https://fonts.googleapis.com/css2?family=Quicksand&display=swap");
  @import url("https://fonts.googleapis.com/css2?family=Oswald&display=swap");
  /*
 font-family: 'Roboto', sans-serif;
 font-family: 'Quicksand', sans-serif;
font-family: 'Oswald', sans-serif;
 */

  .sectionContainer {
    width: 100%;
    margin-bottom: 50px;
  }

  .contentContainer {
    width: 75%;
    display: flex;
    justify-content: space-around;
    align-items: center;
  }

  .contentContainer img {
    max-width: 30vw;
  }

  .contentText {
    margin: 0 5% 0 0;
    text-align: left;
    width: 66%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
  }

  .sliderContainer {
    width: calc(100% - 100px);
    height: 25vw;
    background-color: blue;
    position: relative;
  }

  .sliderContainer > img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .sliderDown,
  .sliderUp,
  .sliderDescription {
    position: absolute;
    color: white;
    width: 10%;
    height: 10%;
    top: calc(50% - 2.5vw);
  }

  .sliderDown > p,
  .sliderUp > p,
  .sliderDescription > p {
    padding: 0;
    margin: 0;
    font-size: 5vw;
    transition: 0.2s;
  }

  .sliderDown > p:hover,
  .sliderUp > p:hover {
    transition: 0.2s;
    cursor: pointer;
    text-shadow: black 0 0 5px;
  }

  .sliderUp {
    right: 0;
  }

  .sliderDescription {
    width: 80%;
    left: 10%;
    text-shadow: black 0 0 5px;
  }

  .homeContainer {
    flex-direction: var(--containerDirection) !important;
    display: flex;
    margin: 0 !important;
    font-size: var(--fontSize) !important;
    font-family: var(--fontFamily), sans-serif !important;
  }

  nav {
    padding: 15px;
    background-color: rgb(68, 68, 68);
    width: var(--navWidth);
    position: relative;
    display: flex;
    justify-content: var(--navJustify);
    align-items: center;
    flex-direction: var(--navDirection);
  }

  .userActions {
    display: flex;
    align-items: center;
    flex-direction: var(--navDirection);
    display: flex;
  }

  .userActions > a {
    margin: 10px;
  }

  .navItems {
    display: flex;
    flex-direction: var(--navDirection);
    align-items: center;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .navItems > a {
    margin: 10px;
    color: white;
  }

  .login,
  .register,
  .logout,
  .config,
  .users,
  .search {
    padding: 10px;
  }

  .login:hover,
  .register:hover,
  .logout:hover,
  .config:hover,
  .users:hover,
  .search:hover {
    text-decoration: none;
  }

  .login,
  .logout {
    border: 2px solid green;
    border-radius: 10px;
    color: green;
  }

  .register {
    border: 2px solid blue;
    border-radius: 10px;
    color: blue;
  }

  .config {
    border: 2px solid orangered;
    border-radius: 10px;
    color: orangered;
  }

  .users {
    border: 2px solid yellow;
    border-radius: 10px;
    color: yellow;
  }

  .search {
    border: 2px solid pink;
    border-radius: 10px;
    color: pink;
  }

  .componentsContainer {
    min-width: calc(100vw - var(--navWidth) - 30px);
    margin-top: 50px;
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
    max-width: 500px;
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

  .newsContent a {
    margin-top: auto;
  }

  .newsContent {
    padding: 25px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
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
    overflow-x: hidden;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    margin: 25px;
  }

  footer {
    width: 100%;
    border-top: 1px solid black;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin-bottom: 15px;
    margin-top: auto;
  }

  .footer {
    width: 100%;
    padding: 15px;
    display: flex;
    justify-content: space-evenly;
  }
</style>
