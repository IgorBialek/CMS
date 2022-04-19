<script>
  import saveHandler from "../../utils/saveHandler";
  import moveComponent from "../../utils/moveComponent";

  import { onMount } from "svelte";
  let configuration;
  let footer;

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;
    footer = configuration.templates[configuration.selectedTemplate].footer;
  });

  const deleteLink = (index) => {
    footer.links = footer.links.filter((link, i) => i != index);
  };

  const addLink = () => {
    footer.links = [...footer.links, { title: "", link: "" }];
  };
</script>

{#if configuration}
  <div class="configContainer">
    <!--CONFIGURE FOOTER-->
    <h1>Configure Footer</h1>
    <div class="componentContainer">
      <h2>Links</h2>
      <div class="footerLinks">
        {#each footer.links as link, i}
          <div class="footerLink">
            <div
              on:click={() => {
                deleteLink(i);
              }}
            >
              X
            </div>
            <div class="inputs">
              <div class="data">
                <label>Title</label>
                <input type="text" bind:value={link.title} />
              </div>
              <div class="data">
                <label>Link</label>
                <input type="text" bind:value={link.link} />
              </div>
            </div>
            <div class="positionIndex">
              <div
                on:click={() => {
                  moveComponent(
                    i,
                    "up",
                    footer.links,
                    (tab) => (footer.links = tab)
                  );
                }}
              >
                up
              </div>
              <div
                on:click={() => {
                  moveComponent(
                    i,
                    "down",
                    footer.links,
                    (tab) => (footer.links = tab)
                  );
                }}
              >
                down
              </div>
            </div>
          </div>
        {/each}
      </div>
      <button on:click={addLink}>Add link</button>
    </div>
    <button
      on:click={() => {
        configuration.templates[configuration.selectedTemplate].footer = footer;
        saveHandler(configuration);
      }}>SAVE</button
    >
  </div>
{/if}

<style>
  .footerLinks {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
  }

  .footerLink {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    align-items: center;
  }

  .inputs {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .inputs > div {
    margin: 5px;
  }
</style>
