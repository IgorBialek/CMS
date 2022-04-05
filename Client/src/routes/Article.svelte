<script>
  export let params;

  let configuration = JSON.parse(localStorage.getItem("configuration"));
  let article = configuration.templates[
    configuration.selectedTemplate
  ].menu.articles.filter((article) => article.link == params.wild)[0];

  console.log(article);
</script>

<div class="articleContainer">
  <h1>{article.title}</h1>
  <p>{article.text}</p>
</div>

<style>
  .articleContainer {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
</style>
