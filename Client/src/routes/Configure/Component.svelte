<script>
  import saveHandler from "../../utils/saveHandler";
  import moveComponent from "../../utils/moveComponent";

  import { onMount } from "svelte";
  let configuration;
  let components = [];

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;
    components =
      configuration.templates[configuration.selectedTemplate].components;
  });

  const deleteComponent = (index) => {
    components = components.filter((comp, i) => i != index);
  };

  const addComponentNews = (index) => {
    components = components.map((comp, i) => {
      if (i == index) {
        return {
          ...comp,
          news: [
            {
              title: "",
              headline: "",
              text: "",
              link: "",
            },
          ],
        };
      } else {
        return comp;
      }
    });
  };

  const removeComponentNews = (index) => {
    components = components.map((comp, i) => {
      if (i == index) {
        return {
          ...comp,
          news: [],
        };
      } else {
        return comp;
      }
    });
  };

  const addComponentSlider = (index) => {
    components = components.map((comp, i) => {
      if (i == index) {
        return {
          ...comp,
          slider: { images: [], description: "", switchTime: null },
        };
      } else {
        return comp;
      }
    });
  };

  const removeComponentSlider = (index) => {
    components = components.map((comp, i) => {
      if (i == index) {
        return {
          ...comp,
          slider: null,
        };
      } else {
        return comp;
      }
    });
  };

  const addComponentContent = (index) => {
    components = components.map((comp, i) => {
      if (i == index) {
        return {
          ...comp,
          content: { image: null, title: "", text: "" },
        };
      } else {
        return comp;
      }
    });
  };

  const removeComponentContent = (index) => {
    components = components.map((comp, i) => {
      if (i == index) {
        return {
          ...comp,
          content: null,
        };
      } else {
        return comp;
      }
    });
  };

  const addComponent = () => {
    components = [
      ...components,
      { name: "", visible: true, news: [], slider: null },
    ];
  };
</script>

<div class="configContainer">
  <!--CONFIGURE COMPONENTS-->
  <h1>Configure components</h1>
  <div class="componentContainer">
    {#each components as comp, i}
      <div class="component comp">
        <div on:click={() => deleteComponent(i)} class="delete">
          <img src="delete.svg" />
        </div>
        <div>
          <label>Visible</label>
          <input type="checkbox" bind:checked={comp.visible} />
        </div>
        <input bind:value={comp.name} />
        <div class="positionIndex">
          <div
            on:click={() => {
              moveComponent(i, "up", components, (tab) => (components = tab));
            }}
          >
            <img src="up-arrow.svg" />
          </div>
          <div
            on:click={() => {
              moveComponent(i, "down", components, (tab) => (components = tab));
            }}
          >
            <img src="down-arrow.svg" />
          </div>
        </div>
        <div class="componentActions">
          {#if !comp.slider}
            <button on:click={() => addComponentSlider(i)}>Add slider</button>
          {:else}
            <button on:click={() => removeComponentSlider(i)}
              >Remove slider</button
            >
          {/if}
          {#if comp.news.length == 0}
            <button on:click={() => addComponentNews(i)}>Add news</button>
          {:else}
            <button on:click={() => removeComponentNews(i)}>Remove news</button>
          {/if}
          {#if !comp.content}
            <button on:click={() => addComponentContent(i)}>Add content</button>
          {:else}
            <button on:click={() => removeComponentContent(i)}
              >Remove content</button
            >
          {/if}
        </div>
      </div>
    {/each}
    <button on:click={addComponent}>Add</button>
  </div>
  <button
    on:click={() => {
      configuration.templates[configuration.selectedTemplate].components =
        components;
      saveHandler(configuration);
    }}>SAVE</button
  >
</div>

<style>
  .comp {
    flex-wrap: wrap;
  }

  .componentActions {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
  }

  .componentActions > button {
    width: 125px;
    min-height: 64px;
    margin: 0 25px;
  }

  .componentActions input {
    margin: 0 !important;
  }
</style>
