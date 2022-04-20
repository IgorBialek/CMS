<script>
  import { push } from "svelte-spa-router";
  import { onMount } from "svelte";
  let configuration;
  let components = [];
  let user = JSON.parse(localStorage.getItem("user"));

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;

    components =
      configuration.templates[configuration.selectedTemplate].components;
  });
</script>

<div class="configContainer">
  {#if user.permission == "admin"}
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
      <div>
        <a href="/#/Configuration/Articles">Articles</a>
      </div>
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
  {:else}
    <h1>Configure news</h1>
    <div class="blockContainer">
      {#each components as comp, i}
        {#if comp.news.length > 0}
          <div>
            <a href={`/#/Configuration/News/${i}`}>{comp.name}'s news</a>
          </div>
        {/if}
      {/each}
    </div>
  {/if}
  <button
    on:click={() => {
      push("/");
    }}>Back to website</button
  >
</div>

<style>
  .configContainer h2 {
    margin: 0;
  }

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
    width: 6vw;
    height: 6vw;
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
    padding: 0 10px;
  }

  .blockContainer a:hover {
    text-decoration: none;
  }
</style>
