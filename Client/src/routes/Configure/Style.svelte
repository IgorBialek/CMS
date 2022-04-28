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
  <div
    class="configContainer"
    style="--fontSize: calc({styles.fontSize / 20}vw + {styles.fontSize /
      20}vh)  !important; --fontFamily: {styles.selectedFont} !important; --lightColor: {styles
      .colors.lightColor}; --mediumColor: {styles.colors
      .mediumColor}; --darkColor: {styles.colors.darkColor};"
  >
    <!--CONFIGURE STYLES-->
    <h1>Configure styles</h1>
    <div class="componentContainer wrap">
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
      <div class="newsContainer">
        <div class="newsSingle">
          <div class="newsTitle">New's title</div>
          <div class="newsContent">
            <h2>New's headline</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam
              sagittis dolor sit amet molestie sagittis. Fusce condimentum
              pulvinar arcu. Sed lacinia, ipsum eu posuere dapibus, nunc nisi
              ullamcorper odio, a tristique lacus mauris vel tellus. Mauris
              hendrerit erat et convallis aliquam. In sit amet ex auctor,
              efficitur justo in, bibendum sem. Duis scelerisque enim quis dui
              fringilla maximus. Suspendisse potenti. Vestibulum dictum placerat
              massa sit amet sollicitudin. Nam efficitur eleifend justo, eu
              interdum enim blandit at. Donec sit amet aliquet quam. Fusce
              tincidunt auctor nisl ut ullamcorper.
            </p>
            <span>Go to news</span>
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
  @import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");
  @import url("https://fonts.googleapis.com/css2?family=Quicksand&display=swap");
  @import url("https://fonts.googleapis.com/css2?family=Oswald&display=swap");

  .fontContainer {
    display: flex;
    justify-content: space-evenly;
    flex-wrap: wrap;
  }

  .newsContainer {
    font-size: var(--fontSize);
    font-family: var(--fontFamily), sans-serif !important;
    margin-top: 50px;
    width: 100%;
    background-color: var(--darkColor);
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: stretch;
  }

  .newsSingle {
    margin: 1.5vw;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    max-width: 500px;
  }

  .newsTitle {
    padding: 10px;
    background-color: var(--mediumColor);
    text-align: left;
    color: white;
  }

  .newsContent h2 {
    margin: 0;
  }

  .newsContent span {
    padding: 10px;
    align-self: flex-start;
    margin-top: auto;
    background-color: var(--mediumColor);
    transition: 0.5s;
  }

  .newsContent span:hover {
    cursor: pointer;
    transition: 0.5s;
    background-color: var(--darkColor);
  }

  .newsContent {
    padding: 25px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    text-align: left;
    color: white;
    background-color: var(--lightColor);
  }

  .newsContent a {
    padding: 10px;
    color: white;
    background-color: rgb(68, 68, 68);
    align-self: start;
  }
</style>
