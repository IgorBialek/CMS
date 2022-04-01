<style>
  #configContainer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  #positionContainer,
  #newsContainer {
    width: 50%;
    border: 1px solid black;
    padding: 50px;
    border-radius: 10px;
  }

  #position,
  #news {
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
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
  }

  #newsData > div {
    margin: 0 50px;
  }
</style>

<script>
  let componentPositions = [
    { name: "Slider", visible: true },
    { name: "News", visible: true },
    { name: "Content", visible: true },
  ];

  let newsComponents = [
    {
      title: "News 1",
      headline: "Special title treatment",
      text: "Gdybyś nie istniała, miastu by wygodniej się żyło Jestem tu, byłem tam, zresztą w sumie, kto nie był? Jest tu cała WWA, z wyjątkiem Ciebie",
      link: "/nothingnow",
    },
    {
      title: "News 2",
      headline: "Special title treatment",
      text: "Idę ulicami, gapiąc się na panny hoże Czarne płaszcze, czarne rury no i czarne Roshe Rozbity iPhone 6, choć zarabia marne grosze",
      link: "/nothingnow",
    },
  ];

  const movePosition = (index, direction) => {
    if (direction == "up" && index > 0) {
      [componentPositions[index], componentPositions[index - 1]] = [
        componentPositions[index - 1],
        componentPositions[index],
      ];
    }

    if (direction == "down" && index < componentPositions.length - 1) {
      [componentPositions[index], componentPositions[index + 1]] = [
        componentPositions[index + 1],
        componentPositions[index],
      ];
    }
  };

  const moveNews = (index, direction) => {
    if (direction == "up" && index > 0) {
      [newsComponents[index], newsComponents[index - 1]] = [
        newsComponents[index - 1],
        newsComponents[index],
      ];
    }

    if (direction == "down" && index < newsComponents.length - 1) {
      [newsComponents[index], newsComponents[index + 1]] = [
        newsComponents[index + 1],
        newsComponents[index],
      ];
    }
  };

  const deleteNews = (index) => {
    newsComponents = newsComponents.filter((news, i) => i != index);
  };

  const addNews = () => {
    newsComponents = [
      ...newsComponents,
      {
        title: "",
        headline: "",
        text: "",
        link: "",
      },
    ];
  };
</script>

<div id="configContainer">
  <h1>Configure position and visibility of elements</h1>
  <div id="positionContainer">
    {#each componentPositions as comp, i}
      <div id="position">
        <div id="positionVisibility">
          <input type="checkbox" bind:checked="{comp.visible}" />
        </div>
        <div id="positionName">{comp.name}</div>
        <div id="positionIndex">
          <div
            on:click="{() => {
              movePosition(i, 'up');
            }}"
          >
            up
          </div>
          <div
            on:click="{() => {
              movePosition(i, 'down');
            }}"
          >
            down
          </div>
        </div>
      </div>
    {/each}
  </div>
  <h1>Configure news</h1>
  <div id="newsContainer">
    {#each newsComponents as news, i}
      {#if i != 0}
        <hr />
      {/if}
      <div id="news">
        <div id="deleteNews" on:click="{() => deleteNews(i)}">X</div>
        <div id="newsData">
          <div>
            <label>Title</label>
            <input bind:value="{news.title}" />
          </div>
          <div>
            <label>Headline</label>
            <input bind:value="{news.headline}" />
          </div>
          <div>
            <label>Text</label>
            <input bind:value="{news.text}" />
          </div>
          <div>
            <label>Link</label>
            <input bind:value="{news.link}" />
          </div>
        </div>
        <div id="positionIndex">
          <div
            on:click="{() => {
              moveNews(i, 'up');
            }}"
          >
            up
          </div>
          <div
            on:click="{() => {
              moveNews(i, 'down');
            }}"
          >
            down
          </div>
        </div>
      </div>
    {/each}
    <div id="addNews" on:click="{addNews}">ADD</div>
  </div>
  <span>{JSON.stringify(componentPositions, null, 5)}</span>
  <span>{JSON.stringify(newsComponents, null, 5)}</span>
</div>
