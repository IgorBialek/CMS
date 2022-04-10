<script>
  import { push } from "svelte-spa-router";

  let configuration = JSON.parse(localStorage.getItem("configuration"));
  let components =
    configuration.templates[configuration.selectedTemplate].components;
</script>

<div class="configContainer">
  <button
    on:click={() => {
      push("/");
    }}>Back to website</button
  >
  <h1>Configure anything you want</h1>
  <h2>Site</h2>
  <div class="blockContainer">
    <div>
      <a href="/#/Configuration/Templates">Templates</a>
    </div>
    <div>
      <a href="/#/Configuration/Style">Style</a>
    </div>
    <div>
      <a href="/#/Configuration/Menu">Menu</a>
    </div>
    <!-- <div>
      <a href="/#/Configuration/Footer">Footer</a>
    </div> -->
    <div>
      <a href="/#/Configuration/Component">Components</a>
    </div>
    <div>
      <a href="/#/Configuration/EditComponent">Edit Components</a>
    </div>
  </div>
  <h2>News</h2>
  <div class="blockContainer">
    {#each components as comp, i}
      {#if comp.news.length > 0}
        <div>
          <a href={`/#/Configuration/News/${i}`}>{comp.name}'s news</a>
        </div>
      {/if}
    {/each}
  </div>
  <h2>Sliders</h2>
  <div class="blockContainer">
    {#each components as comp, i}
      {#if comp.slider}
        <div>
          <a href={`/#/Configuration/Slider/${i}`}>{comp.name}'s slider</a>
        </div>
      {/if}
    {/each}
  </div>
  <h2>Contents</h2>
  <div class="blockContainer">
    {#each components as comp, i}
      {#if comp.content}
        <div>
          <a href={`/#/Configuration/Content/${i}`}>{comp.name}'s content</a>
        </div>
      {/if}
    {/each}
  </div>
</div>

<style>
  .blockContainer {
    width: 75%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
  }

  .blockContainer > div {
    transition: 0.2s;
    margin: 25px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 8vw;
    height: 8vw;
    border: 1px solid black;
    border-radius: 10px;
  }

  .blockContainer > div:hover {
    background-color: rgb(233, 233, 233);
    cursor: pointer;
    transition: 0.2s;
    transform: scale(1.1);
  }

  .blockContainer a {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    color: black;
  }

  .blockContainer a:hover {
    text-decoration: none;
  }
</style>
