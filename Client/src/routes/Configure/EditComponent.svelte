<script>
  import saveHandler from "../../utils/saveHandler";
  import moveComponent from "../../utils/moveComponent";

  import { onMount } from "svelte";
  let configuration;
  let components = [];

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;
    components =
      configuration.templates[configuration.selectedTemplate].components;
  });
</script>

{#if configuration}
  <div class="configContainer">
    <!--CONFIGURE COMPONENTS POSITION-->
    <h1>Configure position and visibility of elements</h1>
    <div class="componentContainer">
      {#each components as comp, i}
        <div class="component">
          <div>
            <input type="checkbox" bind:checked={comp.visible} />
          </div>
          <div>{comp.name}</div>
          <div class="positionIndex">
            <div
              on:click={() => {
                moveComponent(i, "up", components, (tab) => (components = tab));
              }}
            >
              up
            </div>
            <div
              on:click={() => {
                moveComponent(
                  i,
                  "down",
                  components,
                  (tab) => (components = tab)
                );
              }}
            >
              down
            </div>
          </div>
        </div>
      {/each}
    </div>
    <button
      on:click={() => {
        configuration.templates[configuration.selectedTemplate].components =
          components;
        saveHandler(configuration);
      }}>SAVE</button
    >
  </div>
{/if}
