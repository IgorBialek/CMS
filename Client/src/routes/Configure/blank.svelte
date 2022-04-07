<script>
    import saveHandler from "../../utils/saveHandler"

    let configuration = JSON.parse(localStorage.getItem("configuration"));
</script>

<div class="configContainer">
   
    <button on:click="{() => {saveHandler(configuration)}}">SAVE</button>
</div>