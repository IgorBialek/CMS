<script>
  import { push } from "svelte-spa-router";
  import saveHandler from "../../utils/saveHandler";

  import { onMount } from "svelte";
  let configuration;

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;
  });

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

    configuration.selectedTemplate = configuration.templates.length - 1;
    newTemplateName = "";
  };

  const removeTemplate = () => {
    if (configuration.templates.length > 1) {
      configuration.templates = configuration.templates.filter(
        (template, i) => configuration.selectedTemplate != i
      );
      configuration.selectedTemplate = 0;
    } else {
      alert("You must have at least one template");
    }
  };

  const templateChangeHandler = (e) => {
    configuration.selectedTemplate = e.target.value;
  };

  const importTemplate = () => {
    var input = document.createElement("input");
    input.type = "file";

    input.onchange = (e) => {
      // getting a hold of the file reference
      var file = e.target.files[0];

      // setting up the reader
      var reader = new FileReader();
      reader.readAsText(file, "UTF-8");

      // here we tell the reader what to do when it's done reading...
      reader.onload = async (readerEvent) => {
        var content = readerEvent.target.result; // this is the content!

        configuration.templates = [
          ...configuration.templates,
          JSON.parse(content),
        ];

        configuration.selectedTemplate = configuration.templates.length - 1;
      };
    };

    input.click();
  };

  function downloadObjectAsJson(exportObj, exportName) {
    var dataStr =
      "data:text/json;charset=utf-8," +
      encodeURIComponent(JSON.stringify(exportObj));
    var downloadAnchorNode = document.createElement("a");
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", exportName + ".json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  }

  const exportTemplate = () => {
    downloadObjectAsJson(
      configuration.templates[configuration.selectedTemplate],
      configuration.templates[configuration.selectedTemplate].name
    );
  };
</script>

{#if configuration}
  <div class="configContainer">
    <!--CONFIGURE TEMPLATES-->
    <h1>Configure templates</h1>
    <div class="componentContainer">
      <input
        type="text"
        bind:value={newTemplateName}
        placeholder="Template name"
      />
      <button on:click={addTemplate}>Add template</button>
      <button on:click={importTemplate}>Import template (JSON)</button>
      <div class="template">
        <h2>Select template</h2>
        <select
          on:input={templateChangeHandler}
          bind:value={configuration.selectedTemplate}
        >
          {#each configuration.templates as template, i}
            <option value={i}>{template.name}</option>
          {/each}
        </select>
        <button on:click={removeTemplate}>Remove selected template</button>
        <button on:click={exportTemplate}>Export selected template</button>
      </div>
    </div>
    <button
      on:click={() => {
        saveHandler(configuration);
      }}>SAVE</button
    >
  </div>
{/if}
