<script>
  import Router from "svelte-spa-router";
  import Login from "./routes/Login.svelte";
  import Register from "./routes/Register.svelte";
  import Home from "./routes/Home.svelte";
  import Configuration from "./routes/Configuration.svelte";
  import Article from "./routes/Article.svelte";
</script>

<div class="container">
  <Router
    routes={{
      "/": Home,
      "/Login": Login,
      "/Register": Register,
      "/Configuration": Configuration,
      "/Article/*": Article,
    }}
  />
</div>

<style>
  .container {
    margin: 10px;
  }
</style>
