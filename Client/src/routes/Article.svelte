<script>
  export let params;

  import { onMount } from "svelte";
  let configuration;
  let article = [];

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;

    article = configuration.templates[
      configuration.selectedTemplate
    ].menu.articles.filter((article) => article.link == params.wild)[0];
  });
</script>

<div class="articleContainer">
  <h1>{article.title}</h1>
  <p>{article.text}</p>
</div>

<style>
  .articleContainer {
    font-size: 25px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .articleContainer p {
    width: 50%;
  }
</style>
