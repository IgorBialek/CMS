<script>
  export let params;
  import saveHandler from "../../utils/saveHandler";

  import { onMount } from "svelte";
  let configuration;
  let components = [];
  let contentComponent;

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;
    components =
      configuration.templates[configuration.selectedTemplate].components;
    contentComponent = components
      .filter((comp, i) => comp.content && i == params.wild)
      .map((comp, i) => {
        return { content: comp.content, compName: comp.name, compIndex: i };
      })[0];
  });

  const imageHandler = ({ target: { files } }) => {
    document.getElementById("uploadedImages").innerHTML = "";
    contentComponent.content.image = null;

    var reader = new FileReader();

    reader.onload = function (frEvent) {
      document.getElementById(
        "uploadedImages"
      ).innerHTML += `<div style="height: 50px; width: 50px;"><img style='max-height: 100%;max-width: 100%;' src="${frEvent.target.result}" /></div>`;
      contentComponent.content.image = frEvent.target.result;
    };

    reader.readAsDataURL(files[0]);
  };
</script>

{#if configuration}
  <div class="configContainer">
    <h1>
      Configure {contentComponent.compName} slider
    </h1>
    <div class="componentContainer">
      <div class="inputs">
        <div class="data">
          <label>Title</label>
          <input type="text" bind:value={contentComponent.content.title} />
        </div>
        <div class="data ">
          <label>Text</label>
          <input type="text" bind:value={contentComponent.content.text} />
        </div>
        <div class="data fileInput">
          <label>Image</label>
          <input type="file" accept=".jpg,.png" on:change={imageHandler} />
        </div>
      </div>
      <div id="uploadedImages" />
    </div>
    <button
      on:click={() => {
        components.content = contentComponent.content;
        configuration.templates[configuration.selectedTemplate].components =
          components;
        saveHandler(configuration);
      }}>SAVE</button
    >
  </div>
{/if}

<style>
  #uploadedImages {
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
