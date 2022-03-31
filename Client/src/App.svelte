<script>
	import Router from "svelte-spa-router";
	import Login from "./routes/Login.svelte"
	import Register from "./routes/Register.svelte"
	import Test from "./routes/Test.svelte"
	import Home from "./routes/Home.svelte"

</script>

<div class="container">
	<Router
	routes={{
	"/": Home,
	"/Login": Login,
	"/Register": Register,
	}}
	/>
</div>

<style>

	.container {
		margin: 10px;
	}
</style>