import App from "./App.svelte";

if (!localStorage.getItem("configuration")) {
  localStorage.setItem(
    "configuration",
    JSON.stringify([
      {
        name: "Slider",
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
      { name: "News", visible: true, news: [] },
      { name: "Content", visible: true, news: [] },
    ])
  );
}

const app = new App({
  target: document.body,
});

export default app;
