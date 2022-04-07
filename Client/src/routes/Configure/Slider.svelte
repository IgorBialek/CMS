<script>
        export let params;
    import saveHandler from "../../utils/saveHandler"

    let configuration = JSON.parse(localStorage.getItem("configuration"));
    let components =
    configuration.templates[configuration.selectedTemplate].components;

    let sliderComponent = components
    .filter((comp, i) => comp.slider && i ==params.wild)
    .map((comp, i) => {
      return { slider: comp.slider, compName: comp.name, compIndex: i };
    })[0]

    const imageHandler = ({ target: { files } }) => {
    document.getElementById("uploadedImages").innerHTML = "";

    for (let i = 0; i < files.length; i++) {
      var reader = new FileReader();

      reader.onload = function (frEvent) {
        document.getElementById(
          "uploadedImages"
        ).innerHTML += `<div style="height: 50px; width: 50px;"><img style='max-height: 100%;max-width: 100%;' src="${frEvent.target.result}" /></div>`;
      };
      console.log(files[i]);
      reader.readAsDataURL(files[i]);
    }
  };

</script>


<div class="configContainer">
    <h1>
        Configure {sliderComponent.compName} slider
      </h1>
      <div class="componentContainer">
        <div class="inputs"> 
          <div class="data fileInput">
            <label>Images</label>
            <input
              type="file"
              multiple
              accept=".jpg,.png"
              on:change={imageHandler}
            />
          </div>
          <div class="data">
            <label>Description</label>
            <input type="text" bind:value={sliderComponent.slider.description} />
          </div>
          <div class="data ">
            <label>Switch time (seconds)</label>
            <input type="number" bind:value={sliderComponent.slider.switchTime} />
          </div>
        </div>
        <div id="uploadedImages" />
      </div>
    <button on:click="{() => {
                configuration.templates[configuration.selectedTemplate].components = components
        saveHandler(configuration)}}">SAVE</button>
</div>

<style>

    #uploadedImages{
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>