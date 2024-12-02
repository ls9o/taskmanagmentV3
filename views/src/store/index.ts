// src/store/index.ts

import { createStore } from "vuex";
import storeLogin, { State as StoreLoginState } from "./store_login";
import breadcrumbs from "./store_breadcrumb"; // หากมีประเภท state ให้เพิ่มที่นี่

export interface RootState {
  storeLogin: StoreLoginState; // ชนิดของ state ที่ใช้ในโมดูล storeLogin
  // หาก breadcrumbs มีประเภท state ก็เพิ่มที่นี่ด้วย
}

const store = createStore<RootState>({
  modules: {
    storeLogin,
    breadcrumbs,
  },
});

export default store; // ส่งออก store
