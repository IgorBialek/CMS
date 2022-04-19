<script>
  import { onMount } from "svelte";

  let configuration;
  let components;
  let images = [];

  onMount(async () => {
    configuration = (await (await fetch("/getConfiguration")).json())
      .configuration.configuration;

    components =
      configuration.templates[configuration.selectedTemplate].components;

    images = [];

    components.forEach((comp) => {
      if (comp.slider && comp.slider.images.length > 0) {
        comp.slider.images.forEach((image) => images.push(image));
      }

      if (comp.content && comp.content.image) {
        images.push(comp.content.image);
      }
    });

    images = [...new Set(images)];
  });

  const imageHandler = ({ target: { files } }) => {
    for (let i = 0; i < files.length; i++) {
      var reader = new FileReader();

      reader.onload = function (frEvent) {
        images = [...images, frEvent.target.result];
      };
      reader.readAsDataURL(files[i]);
    }
  };
</script>

<h1>FOR TEST PURPOSE</h1>
<input type="file" multiple accept=".jpg,.png" on:change={imageHandler} />

<div class="imagesContainer">
  {#each images as image}
    <div>
      <img alt="some err" src={image} />
    </div>
  {/each}
</div>

<style>
  img {
    width: 100%;
  }

  .imagesContainer {
    width: 75%;
    margin: 0 auto;
    column-count: 4;
    column-gap: 16px;
  }
  .imagesContainer > div {
    display: inline-block;
    margin-bottom: 16px;
    width: 100%;
  }

  @media (max-width: 1199px) {
    .imagesContainer {
      column-count: 3;
    }
  }

  @media (max-width: 991px) {
    .imagesContainer {
      column-count: 2;
    }
  }

  @media (max-width: 767px) {
    .imagesContainer {
      column-count: 1;
    }
  }
</style>
