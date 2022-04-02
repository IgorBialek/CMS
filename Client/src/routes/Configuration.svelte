<script>
  import { push } from "svelte-spa-router";

  let configuration = JSON.parse(localStorage.getItem("configuration"));
  let components = configuration.components;
  let styles = configuration.styles;

  const moveComponent = (index, direction, tab, callback) => {
    if (direction == "up" && index > 0) {
      [tab[index], tab[index - 1]] = [tab[index - 1], tab[index]];
    }

    if (direction == "down" && index < tab.length - 1) {
      [tab[index], tab[index + 1]] = [tab[index + 1], tab[index]];
    }

    callback(tab);
  };

  const addComponent = () => {
    components = [...components, { name: "", visible: true, news: [] }];
  };

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

  const deleteNews = (newsIndex, compIndex) => {
    components = components.map((comp, i) => {
      if (i == compIndex) {
        comp.news = comp.news.filter((news, i) => i != newsIndex);
      }
      return comp;
    });
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
  };
</script>

<div id="configContainer">
  <h1>Configure styles</h1>
  <div id="componentContainer">
    <div id="fontContainer">
      <div>
        <label>Font family</label>
        <select
          bind:value={styles.selectedFont}
          on:input={(e) => {
            styles.selectedFont = e.target.value;
          }}
        >
          <option>Roboto</option>
          <option>Quicksand</option>
          <option>Inconsolata</option>
        </select>
      </div>
      <div>
        <label>Font size</label>
        <input type="number" bind:value={styles.fontSize} />
      </div>
      <div>
        <label>Colors</label>
        <select
          bind:value={styles.selectedColor}
          on:input={(e) => {
            styles.selectedColor = e.target.value;
            console.log(styles.selectedColor);
          }}
        >
          {#each styles.colors as colorSet, i}
            <option value={i}>
              {i}
            </option>
          {/each}
        </select>
      </div>
    </div>
    <div class="colorsContainer">
      {#each styles.colors as colorSet, i}
        <div class="singleColor">
          <p>{i}.</p>
          <div
            class="colorBubble"
            style="background-color: {colorSet.lightColor};"
          />
          <div
            class="colorBubble"
            style="background-color: {colorSet.mediumColor};"
          />
          <div
            class="colorBubble"
            style="background-color: {colorSet.darkColor};"
          />
        </div>
      {/each}
    </div>
  </div>

  <h1>Configure components</h1>
  <div id="componentContainer">
    {#each components as comp, i}
      <div id="component">
        <div id="deleteComponent" on:click={() => deleteComponent(i)}>X</div>
        <div id="componentName">{comp.name}</div>
        <div id="componentObjects">
          <button>Add slider</button>
          <button on:click={() => addComponentNews(i)}>Add news</button>
          <button>Add content</button>
        </div>
      </div>
    {/each}
  </div>

  <h1>Configure position and visibility of elements</h1>
  <div id="componentContainer">
    {#each components as comp, i}
      <div id="component">
        <div id="positionVisibility">
          <input type="checkbox" bind:checked={comp.visible} />
        </div>
        <input id="positionName" bind:value={comp.name} />
        <div id="positionIndex">
          <div
            on:click={() => {
              moveComponent(i, "up", components, (tab) => (components = tab));
            }}
          >
            up
          </div>
          <div
            on:click={() => {
              moveComponent(i, "down", components, (tab) => (components = tab));
            }}
          >
            down
          </div>
        </div>
      </div>
    {/each}
    <button on:click={addComponent}>Add</button>
  </div>
  {#each components.map((comp, i) => {
    if (comp.news) {
      return { news: comp.news, compName: comp.name, compIndex: i };
    }
  }) as newsComponent}
    {#if newsComponent.news.length > 0}
      <h1>Configure {newsComponent.compName} news</h1>
      <div id="componentContainer">
        {#each newsComponent.news as news, newsIndex}
          {#if newsIndex != 0}
            <hr />
          {/if}
          <div id="component">
            <div
              id="deleteNews"
              on:click={() => deleteNews(newsIndex, newsComponent.compIndex)}
            >
              X
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
                up
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
                down
              </div>
            </div>
          </div>
        {/each}
        <div id="addNews" on:click={() => addNews(newsComponent.compIndex)}>
          ADD
        </div>
      </div>
    {/if}
  {/each}
  <button
    on:click={() => {
      configuration.components = components;
      configuration.styles = styles;
      localStorage.setItem("configuration", JSON.stringify(configuration));
      push("/");
    }}>SAVE</button
  >
</div>

<style>
  #configContainer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  #componentContainer {
    width: 50%;
    border: 1px solid black;
    padding: 50px;
    border-radius: 10px;
  }

  #component {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 100px;
  }

  #positionIndex {
    display: flex;
    flex-direction: column;
  }

  #newsData {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
  }

  #newsData > div {
    width: 100%;
    margin: 0 10px;
  }

  #fontContainer {
    display: flex;
    justify-content: space-evenly;
  }

  label {
    margin: 5px;
  }

  .colorsContainer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .singleColor {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .singleColor > div {
    margin: 5px;
  }

  .colorBubble {
    width: 20px;
    height: 20px;
    border-radius: 50%;
  }
</style>
