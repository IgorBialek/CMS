import App from "./App.svelte";

if (!localStorage.getItem("configuration")) {
  localStorage.setItem(
    "configuration",
    JSON.stringify({
      selectedTemplate: 0,
      templates: [
        {
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
            },
            { name: "Content", visible: true, news: [] },
          ],
        },
        {
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
            },
            { name: "Content", visible: true, news: [] },
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
