import { createApp } from "vue";
import App from "./App.vue";

import routerPromise from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "@fortawesome/fontawesome-free/css/all.css";
import "bootstrap";

routerPromise
  .then((router) => {
    app.use(router);
    app.mount("#app");
  })
  .catch((error) => {
    console.error("Failed to initialize router:", error);
  });
