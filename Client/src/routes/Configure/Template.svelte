<script>
    import { push } from "svelte-spa-router";
    import saveHandler from "../../utils/saveHandler"

    let configuration = JSON.parse(localStorage.getItem("configuration"));
    let newTemplateName = ""

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

  const templateChangeHandler = (e) => {
    configuration.selectedTemplate = e.target.value;
  };
</script>

<div class="configContainer">
    <!--CONFIGURE TEMPLATES-->
    <h1>Configure templates</h1>
        <div class="componentContainer">
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
    <button on:click="{() => {saveHandler(configuration)}}">SAVE</button>
</div>