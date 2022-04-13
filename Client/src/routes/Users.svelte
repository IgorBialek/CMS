<script>
import { onMount } from "svelte";

let users

onMount(async ()=>{
    users = await(await fetch("/users")).json()
})

</script>

<p>{JSON.stringify(users, null, 5)}</p>