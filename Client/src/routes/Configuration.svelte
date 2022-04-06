<script>
  import { push } from "svelte-spa-router";

  let configuration = JSON.parse(localStorage.getItem("configuration"));
  let components =
    configuration.templates[configuration.selectedTemplate].components;
  let styles = configuration.templates[configuration.selectedTemplate].styles;
  let menu = configuration.templates[configuration.selectedTemplate].menu;
  let footer = configuration.templates[configuration.selectedTemplate].footer;

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
    console.log(components);
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

  const templateChangeHandler = (e) => {
    components = configuration.templates[e.target.value].components;
    styles = configuration.templates[e.target.value].styles;
    configuration.selectedTemplate = e.target.value;
  };

  let newTemplateName = "";

  const addTemplate = () => {
    configuration.templates = [
      ...configuration.templates,
      {
        name: newTemplateName,
        menu: {
          type: "horizontal",
          articles: [],
        },
        styles: {
          fontSize: 16,
          selectedFont: "Roboto",
          colors: {
            lightColor: "#edf2f4",
            mediumColor: "#8d99ae",
            darkColor: "#2b2d42",
          },
        },
        components: [],
      },
    ];

    newTemplateName = "";
  };

  const deleteArticle = (index) => {
    menu.articles = menu.articles.filter((article, i) => i != index);
  };

  const addArticle = () => {
    menu.articles = [...menu.articles, { title: "", text: "", link: "" }]
  }

  const deleteLink = (index) => {
    footer.links = footer.links.filter((link, i) => i != index);
  };

  const addLink = () => {
    footer.links = [...footer.links, { title: "", link: "" }]
  }
</script>

<div id="configContainer">

  <!--CONFIGURE TEMPLATES-->
  <h1>Configure templates</h1>
  <div id="componentContainer">
    <input type="text" bind:value={newTemplateName} />
    <button on:click={addTemplate}>Add template</button>
    <div class="template">
      <p>Select template</p>
      <select
        on:input={templateChangeHandler}
        bind:value={configuration.selectedTemplate}
      >
        {#each configuration.templates as template, i}
          <option value={i}>{template.name}</option>
        {/each}
      </select>
    </div>
  </div>

  <!--CONFIGURE MENU-->
  <h1>Configure menu</h1>
  <div id="componentContainer">
    <div id="menu">
      <label>Horizontal</label>
      <input
        type="radio"
        name="menu"
        checked
        on:change={() => {
          menu.type = "horizontal";
        }}
      />
      <label>Vertical</label>
      <input
        type="radio"
        name="menu"
        on:change={() => {
          menu.type = "vertical";
        }}
      />
    </div>
    <div id="articles">
      <h2>Articles</h2>
      {#each menu.articles as article, i}
        <div id="article">
          <div
            on:click={() => {
              deleteArticle(i);
            }}
          >
            X
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
          <div id="positionIndex">
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
      <button on:click="{addArticle}">Add article</button>
    </div>
  </div>

  <!--CONFIGURE FOOTER-->
  <h1>Configure Footer</h1>
  <div id="componentContainer">
    <div id="footerLinks">
      <h2>Articles</h2>
      {#each footer.links as link, i}
        <div id="footerLink">
          <div
            on:click={() => {
              deleteLink(i);
            }}
          >
            X
          </div>
          <div class="inputs">
            <div class="data">
              <label>Title</label>
              <input type="text" bind:value={link.title} />
            </div>
            <div class="data">
              <label>Link</label>
              <input type="text" bind:value={link.link} />
            </div>
          </div>
          <div id="positionIndex">
            <div
              on:click={() => {
                moveComponent(
                  i,
                  "up",
                  footer.links,
                  (tab) => (footer.links = tab)
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
                  footer.links,
                  (tab) => (footer.links = tab)
                );
              }}
            >
              down
            </div>
          </div>
        </div>
      {/each}
      <button on:click="{addLink}">Add link</button>
    </div>
  </div>


  <!--CONFIGURE STYLES-->
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
          <option>Oswald</option>
        </select>
      </div>
      <div>
        <label>Font size</label>
        <input type="number" bind:value={styles.fontSize} />
      </div>
      <div>
        <label>Colors</label>
        <div>
          <input type="color" bind:value={styles.colors.lightColor} />
          <input type="color" bind:value={styles.colors.mediumColor} />
          <input type="color" bind:value={styles.colors.darkColor} />
        </div>
      </div>
    </div>
  </div>

  <!--CONFIGURE COMPONENTS-->
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

    <!--CONFIGURE COMPONENTS POSITION-->
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

  <!--CONFIGURE COMPONENTS NEWS-->
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
      configuration.templates[configuration.selectedTemplate].components =
        components;
      configuration.templates[configuration.selectedTemplate].styles = styles;
      configuration.templates[configuration.selectedTemplate].menu = menu;
      configuration.templates[configuration.selectedTemplate].footer = footer;

      localStorage.setItem("configuration", JSON.stringify(configuration));
      push("/");
    }}>SAVE</button
  >
</div>

<style>
  #configContainer {
    width: 100%;
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

  input[type="color"] {
    -webkit-appearance: none;
    border: 0;
    padding: 0;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin: 5px;
  }
  input[type="color"]::-webkit-color-swatch-wrapper {
    padding: 0;
  }
  input[type="color"]::-webkit-color-swatch {
    border: none;
    border-radius: 50%;
  }

  .template {
    display: flex;
    justify-content: center;
  }

  .template select {
    margin: 5px;
  }

  #menu {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #menu input {
    padding: 0;
    margin: 0;
  }

  .inputs {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .data input {
    margin: 5px;
    width: 100px;
  }

  #article {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
  }

  #footerLink {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
  }
</style>
