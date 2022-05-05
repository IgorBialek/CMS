<script>
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";
  let configuration;
  let articles = [];
  let searchedPhrase = "";

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;

    console.log(
      configuration.templates[configuration.selectedTemplate].menu.articles
    );
    articles =
      configuration.templates[configuration.selectedTemplate].menu.articles;
  });
</script>

{#if configuration}
  <div class="searchContainer">
    <label>Search articles on website</label>
    <input type="text" bind:value={searchedPhrase} />
    <div>
      <button
        on:click={() => {
          articles = articles.sort((a, b) => a.title.localeCompare(b.title));
        }}>asc</button
      >
      <button
        on:click={() => {
          articles = articles.sort((a, b) => b.title.localeCompare(a.title));
        }}>desc</button
      >
    </div>

    <div class="searchResults">
      {#each articles.filter((article) => article.title
          .toLowerCase()
          .includes(searchedPhrase.toLowerCase())) as article}
        <div>
          <div>{article.title}</div>
          <button
            on:click={() => {
              push(`/article/${article.link}`);
            }}>Go</button
          >
        </div>
      {/each}
    </div>
  </div>
{/if}

<style>
  .searchContainer {
    text-align: center;
    display: flex;
    flex-direction: column;
    width: 100%;
    justify-content: center;
    align-items: center;
    margin: 100px 0;
  }

  .searchContainer label {
    font-size: 40px;
    margin: 10px;
  }

  .searchResults {
    margin: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .searchResults > div {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 25px;
    font-weight: bold;
  }
</style>
