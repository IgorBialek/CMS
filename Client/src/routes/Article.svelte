<script>
  export let params;

  import { onMount } from "svelte";
  import saveComment from "./../utils/saveComment";
  let configuration;
  let article;
  let commentText = "";

  let user = JSON.parse(localStorage.getItem("user"));

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;

    article = configuration.templates[
      configuration.selectedTemplate
    ].menu.articles.filter((article) => article.link == params.wild)[0];
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
</script>

<div class="articleContainer">
  {#if article}
    <h1>{article.title}</h1>
    <p>{article.text}</p>
    <h2>Comments section</h2>
    <div class="addComment">
      <input type="text" placeholder="Your comment" bind:value={commentText} />
      <button on:click={addHandler}>Add</button>
    </div>
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
  {:else}
    <h1>No matching articles found!</h1>
  {/if}
</div>

<style>
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
    margin: 50px 0;
  }

  .articleContainer > p {
    width: 50%;
  }

  .addComment {
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
