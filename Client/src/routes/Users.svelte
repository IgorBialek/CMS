<script>
  import { onMount } from "svelte";

  let users;

  onMount(async () => {
    users = await (await fetch("/getUsers")).json();
  });
</script>

<p>{JSON.stringify(users, null, 5)}</p>
