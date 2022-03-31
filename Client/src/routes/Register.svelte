<script>
    let email = ""
    let password = ""
    let repPassword = ""
    let errorMessage = ""

    const handleRegister = async () => {
        //fetch server

        const response = await fetch("?")

        errorMessage = response.errorMessage ?? ""
    }
</script>

<div class="centerContainer">
    <h1>Register</h1>
    <div class="userForm">
        <label>Email</label>
        <input type="email" bind:value={email}/>
        <label>Password</label>
        <input type="password" bind:value={password}/>
        <label>Repeat password</label>
        <input type="password" bind:value={repPassword}/>
        <button class="userFormButton" on:click={handleRegister}>Register</button>
    </div>
</div>

<style>
    .centerContainer {
        flex-direction: column;
        display: flex;
        width: 100%;
        justify-content: center;
        align-items: center;

    }

    .userForm {
        padding: 25px;
        border-radius: 10px;
        border: 1px solid black;
        display: flex;
        flex-direction: column;
    }

    .userForm label {
        margin: 5px 0;
    }

    .userForm input {
        width: 250px;
    }

    .userFormButton {
        align-self: center;
        width: 100px;
        margin-top: 25px;
    }
</style>