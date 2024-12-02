import { createApp } from "vue";
import App from "./App.vue";
import store from "./store/index";
import routerPromise from "./router";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap-icons/font/bootstrap-icons.css";
import "primevue/resources/themes/saga-blue/theme.css"; // Theme
import "primevue/resources/primevue.min.css"; // Core CSS
import "primeicons/primeicons.css";
import "@fortawesome/fontawesome-free/css/all.css";
import "bootstrap";
import PrimeVue from "primevue/config";
import Paginator from "primevue/paginator";

const app = createApp(App);
app.use(PrimeVue);
app.component("MyPaginator", Paginator);

routerPromise
  .then((router) => {
    app.use(router);
    app.use(store);
    app.use(PrimeVue);
    app.mount("#app");

    const user = JSON.parse(localStorage.getItem("user") || "null");
    if (user) {
      store.commit("router.beforeEach/SET_USER", user);
      // ถ้าผู้ใช้ล็อกอินอยู่ ให้ส่งไปหน้าแรก
      if (router.currentRoute.value.path === '/login2') {
        router.push('/');
      }
    } else {
      // ถ้ายังไม่ล็อกอิน ให้ไปที่หน้า login2
      router.push('/login2');
    }
  })
  .catch((error) => {
    console.error("Failed to initialize router:", error);
  });
