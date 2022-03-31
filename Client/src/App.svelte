<script>
	import Router from "svelte-spa-router";
	import Login from "./routes/Login.svelte"
	import Test from "./routes/Test.svelte"
</script>

<Router
routes={{
  "/": Login,
  "/test": Test,
}}
/>