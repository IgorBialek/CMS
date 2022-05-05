<script>
  export let params;
  import { push } from "svelte-spa-router";

  import { onMount } from "svelte";
  import saveComment from "./../utils/saveComment";
  let configuration;
  let article;
  let styles;
  let menu;
  let components;
  let commentText = "";

  let user = JSON.parse(localStorage.getItem("user"));

  $: if (params.wild && configuration) {
    article = configuration.templates[
      configuration.selectedTemplate
    ].menu.articles.filter((article) => article.link == params.wild)[0];

    styles = configuration.templates[configuration.selectedTemplate].styles;
    components =
      configuration.templates[configuration.selectedTemplate].components;
    menu = configuration.templates[configuration.selectedTemplate].menu;
  }

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;

    article = configuration.templates[
      configuration.selectedTemplate
    ].menu.articles.filter((article) => article.link == params.wild)[0];

    styles = configuration.templates[configuration.selectedTemplate].styles;
    components =
      configuration.templates[configuration.selectedTemplate].components;
    menu = configuration.templates[configuration.selectedTemplate].menu;
  });

  const addHandler = () => {
    configuration.templates[configuration.selectedTemplate].menu.articles =
      configuration.templates[configuration.selectedTemplate].menu.articles.map(
        (article) => {
          if (article.link == params.wild) {
            return {
              ...article,
              comments: article.comments
                ? [...article.comments, { user: user.email, text: commentText }]
                : [{ user: user.email, text: commentText }],
            };
          } else {
            return article;
          }
        }
      );

    saveComment(configuration);

    article = configuration.templates[
      configuration.selectedTemplate
    ].menu.articles.filter((article) => article.link == params.wild)[0];

    commentText = "";
  };

  const logout = () => {
    localStorage.setItem("user", null);
    replace("/");
  };
</script>

{#if configuration}
  <div
    class="homeContainer"
    style="--fontSize: calc({styles.fontSize / 20}vw + {styles.fontSize /
      20}vh)  !important; --fontFamily: {styles.selectedFont} !important; --lightColor: {styles
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
      : 'space-between'}; --navBorderBottom:{menu.type == 'vertical'
      ? 'none'
      : '1px solid var(--mainColor)'}; --navBorderRight:{menu.type == 'vertical'
      ? '1px solid var(--mainColor)'
      : 'none'};"
  >
    <nav>
      <div class="navItems">
        <a href="/#/">Home</a>
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

    <div class="articleContainer">
      {#if article}
        <h1>{article.title}</h1>
        <p>{article.text}</p>
        <h2>Comments section</h2>
        {#if user}
          <div class="addComment">
            <input
              type="text"
              placeholder="Your comment"
              bind:value={commentText}
            />
            <button on:click={addHandler}>Add</button>
          </div>
        {/if}
        {#if article.comments && article.comments.length > 0}
          <div class="comments">
            {#each article.comments as comment}
              <div>
                <p class="commentUser">{comment.user}</p>
                <div class="commentTextContainer">
                  <p class="commentText">{comment.text}</p>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      {:else}
        <h1>No matching articles found!</h1>
      {/if}
      <footer>
        <div class="footer">
          {#each components as comp}
            <a href={`#${comp.name}`}>{comp.name}</a>
          {/each}
        </div>
        <div>Michał Dubrowski & Igor Białek 3P</div>
      </footer>
    </div>
  </div>
{/if}

<style>
  .homeContainer {
    flex-direction: var(--containerDirection) !important;
    display: flex;
    margin: 0 !important;
    font-size: var(--fontSize) !important;
    font-family: var(--fontFamily), sans-serif !important;
  }

  .comments {
    width: 100%;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-direction: column;
  }

  .comments > div {
    width: 33%;
    padding: 10px;
    min-width: 300px;
    display: flex;
    flex-direction: column;
  }

  .comments p {
    margin: 0;
  }

  .commentUser {
    margin: 5px !important;
    font-size: 14px;
  }

  .commentText {
    font-size: 25px;
  }

  .commentTextContainer {
    background-color: rgb(240, 240, 240);
    padding: 10px;
    border-radius: 10px;
  }

  .articleContainer {
    font-size: 25px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin: 50px 0 0 0;
    text-align: justify;
  }

  .articleContainer > p {
    width: 50%;
  }

  .addComment {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  nav {
    text-align: center;
    font-weight: bold;
    padding: 15px;
    background-color: white;
    width: var(--navWidth);
    position: relative;
    display: flex;
    justify-content: var(--navJustify);
    align-items: center;
    flex-direction: var(--navDirection);
    border-bottom: var(--navBorderBottom);
    border-right: var(--navBorderRight);
  }

  .userActions {
    display: flex;
    align-items: center;
    flex-direction: var(--navDirection);
    flex-wrap: wrap;
  }

  .userActions > a {
    color: white;
    font-weight: bold;
    margin: 10px;
    padding: 0.8vw;
    border-radius: 15px;
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
    color: rgb(24, 24, 24);
    transition: 0.3s;
  }

  .navItems > a:hover {
    color: #004cff;
    text-decoration: none;
    transition: 0.3s;
  }

  .login,
  .register,
  .logout,
  .config,
  .users,
  .search {
    transition: 0.5s;
    padding: 10px 20px;
    color: rgb(24, 24, 24);

    background-color: #004cff;
  }

  .login:hover,
  .register:hover,
  .logout:hover,
  .config:hover,
  .users:hover,
  .search:hover {
    transition: 0.5s;
    box-shadow: 0px 0px 10px -5px #004cff;
    background-color: #0031a6;
    text-decoration: none;
  }

  footer {
    font-weight: bold;
    margin-top: 1.5vw;
    width: 100%;
    border-top: 1px solid #004cff;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding-bottom: 15px;
  }

  .footer {
    width: 100%;
    padding: 15px 0;
    display: flex;
    justify-content: space-evenly;
    font-size: calc(0.8vw + 0.8vh) !important;
  }

  .footer a {
    color: #004cff;
    transition: 0.3s;
  }

  .footer a:hover {
    transition: 0.3s;
    text-decoration: none;
    color: rgb(24, 24, 24);
  }

  footer div:nth-of-type(2) {
    font-size: 16px;
    color: rgb(24, 24, 24);
  }
</style>
