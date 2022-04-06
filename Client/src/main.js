import App from "./App.svelte";

if (!localStorage.getItem("configuration")) {
  localStorage.setItem(
    "configuration",
    JSON.stringify({
      selectedTemplate: 0,
      templates: [
        {
          name: "First template",
          menu: {
            type: "horizontal",
            articles: [
              { title: "TEST1", text: "55555555", link: "test" },
              { title: "TEST2", text: "666666666", link: "test2" },
            ],
          },
          footer: {
            links: [
              { title: "article", link: "test" },
              { title: "article2", link: "test2" },
              { title: "article3", link: "test3" },
            ],
          },
          styles: {
            fontSize: 16,
            selectedFont: "Roboto",
            colors: {
              lightColor: "#f3e9dc",
              mediumColor: "#c08552",
              darkColor: "#5e3023",
            },
          },
          components: [
            {
              name: "Slider",
              visible: true,
              news: [],
              slider: null,
            },
            {
              name: "News",
              visible: true,
              news: [
                {
                  title: "News 1",
                  headline: "Special title treatment",
                  text: "Gdybyś nie istniała, miastu by wygodniej się żyło Jestem tu, byłem tam, zresztą w sumie, kto nie był? Jest tu cała WWA, z wyjątkiem Ciebie",
                  link: "nothingnow",
                },
                {
                  title: "News 2",
                  headline: "Special title treatment",
                  text: "Idę ulicami, gapiąc się na panny hoże Czarne płaszcze, czarne rury no i czarne Roshe Rozbity iPhone 6, choć zarabia marne grosze",
                  link: "nothingnow",
                },
              ],
              slider: null,
            },
            { name: "Content", visible: true, news: [], slider: null },
          ],
        },
        {
          name: "Second template",
          menu: {
            type: "vertical",
            articles: [
              { title: "TEST3", text: "77777777", link: "test3" },
              { title: "TEST4", text: "888888888", link: "test4" },
            ],
          },
          footer: {
            links: [
              { title: "article", link: "test" },
              { title: "article2", link: "test2" },
            ],
          },
          styles: {
            fontSize: 14,
            selectedFont: "Roboto",
            colors: {
              lightColor: "#f3e9dc",
              mediumColor: "#c08552",
              darkColor: "#5e3023",
            },
          },
          components: [
            {
              name: "Slider",
              visible: true,
              news: [],
              slider: null,
            },
            {
              name: "News",
              visible: true,
              news: [
                {
                  title: "News 1",
                  headline: "Special title treatment",
                  text: "Gdybyś nie istniała, miastu by wygodniej się żyło Jestem tu, byłem tam, zresztą w sumie, kto nie był? Jest tu cała WWA, z wyjątkiem Ciebie",
                  link: "nothingnow",
                },
              ],
              slider: null,
            },
            { name: "Content", visible: true, news: [], slider: null },
          ],
        },
      ],
    })
  );
}

const app = new App({
  target: document.body,
});

export default app;
