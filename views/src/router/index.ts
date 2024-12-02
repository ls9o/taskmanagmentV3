import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { apiService } from "../Service/apiService";
import store from "../store"; // แน่ใจว่า path ของ store ถูกต้อง 

// ปรับปรุงประเภทของ Menu
interface Submenu {
  name: string;
  selected_system: string;
  url: string;
}

interface Menu {
  menu_name: string;
  has_submenu: boolean;
  submenus: Submenu[];
  selected_system: string;
  selected_icon: string;
  url: string;
}

const loadView = (view: string) => {
  return () => import(`../views/${view}.vue`);
};

// กำหนดประเภทคืนค่าของ createDynamicRouter
const createDynamicRouter = async (): Promise<
  ReturnType<typeof createRouter>
> => {
  try {
    const [menuResponse] = await Promise.all([apiService.getMenu()]);
    const menuData: Menu[] = menuResponse.data;

    const allRoutes: RouteRecordRaw[] = [
      {
        path: "/login2",
        component: loadView("LoginView2"),
      },
      // สร้างเส้นทางสำหรับเมนูหลัก ถ้าไม่มีเมนูย่อย
      ...menuData
        .filter((menu) => !menu.has_submenu) // กรองเฉพาะเมนูที่ไม่มีเมนูย่อย
        .map((menu) => ({
          path: menu.url,
          component: loadView(menu.selected_system), // ใช้ menu_name เป็นชื่อ view
          meta: { requiresAuth: true },
        })),
      // สร้างเส้นทางสำหรับเมนูย่อย ถ้าเมนูหลักมีเมนูย่อย
      ...menuData
        .filter((menu) => menu.has_submenu) // กรองเฉพาะเมนูที่มีเมนูย่อย
        .flatMap((menu) =>
          menu.submenus.map((submenu) => ({
            path: submenu.url,
            component: loadView(submenu.selected_system), // ใช้ selected_system เป็นชื่อ view
            meta: { requiresAuth: true },
          }))
        ),
      {
        path: "/",
        component: loadView("HomeView"),
        meta: { requiresAuth: true },
      },
      {
        path: "/asset/:id",
        component: loadView("AssetDetailView"),
        meta: { requiresAuth: true },
      },
      {
        path: "/user/:id",
        component: loadView("CustomerDetails"),
        meta: { requiresAuth: true },
      },
      {
        path: "/employee/:id",
        component: loadView("EmployeeDetails"),
        meta: { requiresAuth: true },
      },
      {
        path: "/Addinfo/:id",
        component: loadView("AddinfoView"),
        meta: { requiresAuth: true },
      },
      {
        path: "/TaskDetail/:id",
        component: loadView("TaskDetailView"),
        meta: { requiresAuth: true },
      },
      {
        path: "/process/:id",
        component: loadView("TaskDetailView"),
        meta: { requiresAuth: true },
      },
      {
        path: "/CreateUser/",
        component: loadView("CreateUserView"),
        meta: { requiresAuth: true },
      },
      {
        path: "/CreateTeam/",
        component: loadView("CreateTeamView"),
        meta: { requiresAuth: true },
      },
      {
        path: "/:catchAll(.*)",
        component: loadView("NotFound"),
      },
    ];

    const router = createRouter({
      history: createWebHistory(),
      routes: allRoutes,
    });

    router.beforeEach((to, from, next) => {
      const isLoggedIn = store.state.storeLogin.isLoggedIn || localStorage.getItem("user");

      if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (!isLoggedIn) {
          next("/login2"); // ถ้ายังไม่ล็อกอิน ให้ไปหน้า login
        } else {
          next(); // ถ้าล็อกอินแล้ว ให้ไปหน้าเดิม
        }
      } else {
        next(); // ถ้าไม่ต้องล็อกอินให้ไปต่อ
      }
    });

    return router;
  } catch (error) {
    console.error("Error creating dynamic router:", error);
    throw error;
  }
};

const routerPromise = createDynamicRouter();
export default routerPromise;
