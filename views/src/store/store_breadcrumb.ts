import { Module } from "vuex";

interface Breadcrumb {
  name: string;
  path: string;
  icon: string;
}

interface BreadcrumbState {
  breadcrumbs: Breadcrumb[];
}

const breadcrumbs: Module<BreadcrumbState, any> = {
  namespaced: true,
  state: () => ({
    breadcrumbs: [],
  }),
  mutations: {
    setBreadcrumbs(state, breadcrumbs: Breadcrumb[]) {
      state.breadcrumbs = breadcrumbs;
    },
    ADD_BREADCRUMB(state, breadcrumb: Breadcrumb) {
      state.breadcrumbs.push(breadcrumb);
    },
    REMOVE_TO_PATH(state, path: string) {
      const index = state.breadcrumbs.findIndex(
        (breadcrumb) => breadcrumb.path === path
      );
      if (index !== -1) {
        state.breadcrumbs = state.breadcrumbs.slice(0, index + 1);
      }
    },
  },
  actions: {
    updateBreadcrumbs({ commit }, breadcrumbs: Breadcrumb[]) {
      commit("setBreadcrumbs", breadcrumbs);
    },
    addBreadcrumb({ commit }, breadcrumb: Breadcrumb) {
      commit("ADD_BREADCRUMB", breadcrumb);
    },
    removeToPath({ commit }, path: string) {
      commit("REMOVE_TO_PATH", path);
    },
  },
  getters: {
    breadcrumbs: (state) => state.breadcrumbs,
  },
};

export default breadcrumbs;
