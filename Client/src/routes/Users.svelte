<script>
  import { onMount } from "svelte";

  let users = [];

  onMount(async () => {
    users = (await (await fetch("/getUsers")).json()).users;
  });
</script>

<div class="usersContainer">
  <div class="userContainer title">
    <div>Login</div>
    <div>Password</div>
    <div>Permission</div>
  </div>
  {#each users as user}
    <div class="userContainer">
      <div>{user._id}</div>
      <div>{user.password}</div>
      <div>{user.permission}</div>
    </div>
  {/each}
</div>

<style>
  .usersContainer {
    margin: 100px 0;
    display: flex;
    width: 100%;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .userContainer {
    width: 50%;
    font-size: 20px;
    margin: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .userContainer > div {
    width: 33%;
    text-align: center;
  }

  .title {
    font-weight: bold;
    font-size: 25px;
  }
</style>
