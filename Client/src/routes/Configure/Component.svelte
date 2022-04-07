<script>
    import saveHandler from "../../utils/saveHandler"

    let configuration = JSON.parse(localStorage.getItem("configuration"));
    let components =
    configuration.templates[configuration.selectedTemplate].components;

    const deleteComponent = (index) => {
    components = components.filter((comp, i) => i != index);
  };

  const addComponentNews = (index) => {
    components = components.map((comp, i) => {
      if (i == index) {
        return {
          ...comp,
          news: [
            {
              title: "",
              headline: "",
              text: "",
              link: "",
            },
          ],
        };
      } else {
        return comp;
      }
    });
  };

  const addComponentSlider = (index) => {
    components = components.map((comp, i) => {
      if (i == index) {
        return {
          ...comp,
          slider: { images: [], description: "", switchTime: null },
        };
      } else {
        return comp;
      }
    });
  };

  const addComponent = () => {
    components = [...components, { name: "", visible: true, news: [], slider: null }];
  };
</script>

<div class="configContainer">
    <!--CONFIGURE COMPONENTS-->
 <h1>Configure components</h1>
 <div class="componentContainer">
   {#each components as comp, i}
     <div class="component">
       <div  on:click={() => deleteComponent(i)}>X</div>
       <input bind:value={comp.name} />
       <div >
         <button on:click={() => addComponentSlider(i)}>Add slider</button>
         <button on:click={() => addComponentNews(i)}>Add news</button>
         <button>Add content</button>
       </div>
     </div>
   {/each}
   <button on:click={addComponent}>Add</button>
 </div>
    <button on:click="{() => {
        configuration.templates[configuration.selectedTemplate].components = components
        saveHandler(configuration)}}">SAVE</button>
</div>

