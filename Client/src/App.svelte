<script>
  import Router from "svelte-spa-router";
  import Login from "./routes/Login.svelte";
  import Register from "./routes/Register.svelte";
  import Home from "./routes/Home.svelte";
  import Configuration from "./routes/Configuration.svelte";
  import Article from "./routes/Article.svelte";
  import Template from "./routes/Configure/Template.svelte";
  import Menu from "./routes/Configure/Menu.svelte";
  import Footer from "./routes/Configure/Footer.svelte";
  import Style from "./routes/Configure/Style.svelte";
  import Component from "./routes/Configure/Component.svelte";
  import News from "./routes/Configure/News.svelte";
  import Slider from "./routes/Configure/Slider.svelte";
  import Gallery from "./routes/Gallery.svelte";
  import Content from "./routes/Configure/Content.svelte";
  import Articles from "./routes/Configure/Articles.svelte";
  import Users from "./routes/Users.svelte";
  import Search from "./routes/Search.svelte";
</script>

<div class="container">
  <Router
    routes={{
      "/": Home,
      "/Login": Login,
      "/Register": Register,
      "/Gallery": Gallery,
      "/Configuration": Configuration,
      "/Configuration/Templates": Template,
      "/Configuration/Menu": Menu,
      "/Configuration/Articles": Articles,
      "/Configuration/Footer": Footer,
      "/Configuration/Style": Style,
      "/Configuration/Component": Component,
      "/Configuration/News/*": News,
      "/Configuration/Slider/*": Slider,
      "/Configuration/Content/*": Content,
      "/Article/*": Article,
      "/Users": Users,
      "/Search": Search,
    }}
  />
</div>
