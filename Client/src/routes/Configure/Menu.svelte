<script>
  import saveHandler from "../../utils/saveHandler";
  import moveComponent from "../../utils/moveComponent";
  import App from "../../App.svelte";

  let configuration = JSON.parse(localStorage.getItem("configuration"));
  let menu = configuration.templates[configuration.selectedTemplate].menu;

  const deleteArticle = (index) => {
    menu.articles = menu.articles.filter((article, i) => i != index);
  };

  const addArticle = () => {
    menu.articles = [...menu.articles, { title: "", text: "", link: "" }];
  };
</script>

<div class="configContainer">
  <!--CONFIGURE MENU-->
  <h1>Configure menu</h1>
  <div class="componentContainer">
    <div class="menu">
      <div>
        <label>Horizontal</label>
        <input
          type="radio"
          name="menu"
          checked={menu.type == "horizontal"}
          on:change={() => {
            menu.type = "horizontal";
          }}
        />
      </div>
      <div>
        <label>Vertical</label>
        <input
          type="radio"
          name="menu"
          checked={menu.type == "vertical"}
          on:change={() => {
            menu.type = "vertical";
          }}
        />
      </div>
    </div>
  </div>
  <button
    on:click={() => {
      configuration.templates[configuration.selectedTemplate].menu = menu;
      saveHandler(configuration);
    }}>SAVE</button
  >
</div>

<style>
  .menu {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .menu input {
    padding: 0;
    margin: 0;
  }

  .menu > div {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .inputs > div {
    margin: 5px;
  }
</style>
