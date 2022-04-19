<script>
  import saveHandler from "../../utils/saveHandler";
  import { onMount } from "svelte";
  let configuration;
  let styles;

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;
    styles = configuration.templates[configuration.selectedTemplate].styles;
  });
</script>

{#if configuration}
  <div class="configContainer">
    <!--CONFIGURE STYLES-->
    <h1>Configure styles</h1>
    <div class="componentContainer">
      <div class="fontContainer">
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
    <button
      on:click={() => {
        configuration.templates[configuration.selectedTemplate].styles = styles;
        saveHandler(configuration);
      }}>SAVE</button
    >
  </div>
{/if}

<style>
  .fontContainer {
    display: flex;
    justify-content: space-evenly;
  }
</style>
