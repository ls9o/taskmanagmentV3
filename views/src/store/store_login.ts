import { Module, createStore } from "vuex";
import { apiService } from "../Service/apiService";

interface User {
  usercode: string;
  username: string;
  LastName: string;
  EmployeeTerm: string;
  Branch: string;
}

export interface State {
  user: User | null;
  isLoggedIn: boolean;
}

const store_login: Module<State, any> = {
  namespaced: true,
  state: {
    user: null, // จะตั้งค่าในตอนล็อกอิน
    isLoggedIn: false, // จะตั้งค่าในตอนล็อกอิน
  },
  mutations: {
    SET_USER(state, user: User) {
      state.user = user;
      state.isLoggedIn = true;
      localStorage.setItem("user", JSON.stringify(user));
    },
    LOGOUT(state) {
      state.user = null;
      state.isLoggedIn = false;
      localStorage.removeItem("user");
    },
  },
  actions: {
    async login({ commit }, credentials: { username: string; password: string }) {
      try {
        const response = await apiService.login(credentials);
        if (response && response.data && response.data.data.user) {
          commit("SET_USER", response.data.data.user);
        } else {
          throw new Error("Invalid login response structure");
        }
      } catch (error) {
        console.error("Login failed:", error);
        throw error;
      }
    },
    logout({ commit }) {
      commit("LOGOUT");
    },
  },
};

export default store_login;
