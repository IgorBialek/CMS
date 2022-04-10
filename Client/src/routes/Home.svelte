<script>
  import { link, replace } from "svelte-spa-router";
  import { onMount, onDestroy } from "svelte";

  let user = JSON.parse(localStorage.getItem("user"));

  let configuration = JSON.parse(localStorage.getItem("configuration"));
  let styles = configuration.templates[configuration.selectedTemplate].styles;
  let components =
    configuration.templates[configuration.selectedTemplate].components;
  let menu = configuration.templates[configuration.selectedTemplate].menu;
  let footer = configuration.templates[configuration.selectedTemplate].footer;

  let sliderSelectors = configuration.templates[
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

  let intervals = [];

  const onInterval = (callback, milliseconds) => {
    const interval = setInterval(callback, milliseconds);

    intervals.push(interval);
  };

  onMount(() => {
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

<div
  class="homeContainer"
  style="--fontSize: {styles.fontSize}px; --fontFamily: {styles.selectedFont}; --lightColor: {styles
    .colors.lightColor}; --mediumColor: {styles.colors
    .mediumColor}; --darkColor: {styles.colors
    .darkColor}; --navDirection: {menu.type == 'vertical' ? 'column' : 'none'}"
>
  <nav>
    <div class="navItems">
      <a href="/#/Gallery">Gallery</a>
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
    {#each components as comp, i}
      {#if comp.visible}
        <div class="sectionContainer">
          <h1>{comp.name}</h1>
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
                    <a href={`/#/${news.link}`}>Go to {news.link}</a>
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
    margin: 0 !important;
    font-size: var(--fontSize);
    font-family: var(--fontFamily), sans-serif;
  }

  nav {
    width: 100%;
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
    margin-bottom: 15px;
  }

  .footer {
    width: 33%;
    margin: 15px;
    display: flex;
    justify-content: space-around;
  }
</style>
