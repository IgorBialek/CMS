<script>
  export let params;
  import saveHandler from "../../utils/saveHandler";
  import moveComponent from "../../utils/moveComponent";

  import { onMount } from "svelte";
  let configuration;
  let components = [];
  let newsComponent = [];

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;
    components =
      configuration.templates[configuration.selectedTemplate].components;
    newsComponent = components
      .map((comp, i) => {
        if (comp.news && i == params.wild) {
          return { news: comp.news, compName: comp.name, compIndex: i };
        }
      })
      .filter((comp) => comp)[0];
  });

  const deleteNews = (newsIndex, compIndex) => {
    components = components.map((comp, i) => {
      if (i == compIndex) {
        comp.news = comp.news.filter((news, i) => i != newsIndex);
      }
      return comp;
    });

    newsComponent = components
      .map((comp, i) => {
        if (comp.news && i == params.wild) {
          return { news: comp.news, compName: comp.name, compIndex: i };
        }
      })
      .filter((comp) => comp)[0];
  };

  const addNews = (compIndex) => {
    components = components.map((comp, i) => {
      if (i == compIndex) {
        comp.news = [
          ...comp.news,
          {
            title: "",
            headline: "",
            text: "",
            link: "",
          },
        ];
      }
      return comp;
    });

    newsComponent = components
      .map((comp, i) => {
        if (comp.news && i == params.wild) {
          return { news: comp.news, compName: comp.name, compIndex: i };
        }
      })
      .filter((comp) => comp)[0];
  };
</script>

{#if configuration}
  <div class="configContainer">
    <h1>Configure {newsComponent.compName} news</h1>
    <div class="componentContainer">
      {#each newsComponent.news as news, newsIndex}
        <div class="component">
          <div on:click={() => deleteNews(newsIndex, newsComponent.compIndex)}>
            <img src="delete.svg" />
          </div>
          <div id="newsData">
            <div>
              <label>Title</label>
              <input bind:value={news.title} />
            </div>
            <div>
              <label>Headline</label>
              <input bind:value={news.headline} />
            </div>
            <div>
              <label>Text</label>
              <input bind:value={news.text} />
            </div>
            <div>
              <label>Link</label>
              <input bind:value={news.link} />
            </div>
          </div>
          <div id="positionIndex">
            <div
              on:click={() => {
                moveComponent(
                  newsIndex,
                  "up",
                  newsComponent.news,
                  (tab) => (newsComponent.news = tab)
                );
              }}
            >
              <img src="up-arrow.svg" />
            </div>
            <div
              on:click={() => {
                moveComponent(
                  newsIndex,
                  "down",
                  newsComponent.news,
                  (tab) => (newsComponent.news = tab)
                );
              }}
            >
              <img src="down-arrow.svg" />
            </div>
          </div>
        </div>
      {/each}
      <button on:click={() => addNews(newsComponent.compIndex)}> ADD </button>
    </div>
    <button
      on:click={() => {
        configuration.templates[configuration.selectedTemplate].components =
          components;
        saveHandler(configuration);
      }}>SAVE</button
    >
  </div>
{/if}

<style>
  #newsData {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
  }

  #newsData input {
    margin: 5px;
  }
</style>
