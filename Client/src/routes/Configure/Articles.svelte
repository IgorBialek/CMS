<script>
  import saveHandler from "../../utils/saveHandler";
  import moveComponent from "../../utils/moveComponent";
  import App from "../../App.svelte";

  import { onMount } from "svelte";
  let configuration;
  let menu;

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;
    menu = configuration.templates[configuration.selectedTemplate].menu;
  });

  const deleteArticle = (index) => {
    menu.articles = menu.articles.filter((article, i) => i != index);
  };

  const addArticle = () => {
    menu.articles = [...menu.articles, { title: "", text: "", link: "" }];
  };
</script>

{#if configuration}
  <div class="configContainer">
    <!--CONFIGURE MENU-->
    <h1>Configure Articles</h1>
    <div class="componentContainer">
      <h2>Articles</h2>
      <div class="articles">
        {#each menu.articles as article, i}
          <div class="article">
            <div
              on:click={() => {
                deleteArticle(i);
              }}
            >
              X
            </div>
            <div>
              <input type="checkbox" bind:checked={article.visible} />
            </div>
            <div class="inputs">
              <div class="data">
                <label>Title</label>
                <input type="text" bind:value={article.title} />
              </div>
              <div class="data">
                <label>Text</label>
                <input type="text" bind:value={article.text} />
              </div>
              <div class="data">
                <label>Link</label>
                <input type="text" bind:value={article.link} />
              </div>
            </div>
            <div class="positionIndex">
              <div
                on:click={() => {
                  moveComponent(
                    i,
                    "up",
                    menu.articles,
                    (tab) => (menu.articles = tab)
                  );
                }}
              >
                up
              </div>
              <div
                on:click={() => {
                  moveComponent(
                    i,
                    "down",
                    menu.articles,
                    (tab) => (menu.articles = tab)
                  );
                }}
              >
                down
              </div>
            </div>
          </div>
        {/each}
      </div>
      <button on:click={addArticle}>Add article</button>
    </div>
    <button
      on:click={() => {
        configuration.templates[configuration.selectedTemplate].menu = menu;
        saveHandler(configuration);
      }}>SAVE</button
    >
  </div>
{/if}

<style>
  .articles {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
  }

  .article {
    flex-grow: 1;
    display: flex;
    justify-content: space-around;
    align-items: center;
  }

  .inputs {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .inputs > div {
    margin: 5px;
  }
</style>
