import { defineBoot } from "@quasar/app-vite/wrappers";
import { useAuthStore } from "src/stores/auth";

export default defineBoot(async ({ router }) => {
  const authStore = useAuthStore();

  router.beforeEach(async (to, from, next) => {

    if (to.meta.public) {
      return next();
    }

    if (!authStore.isInitialized) {
      await authStore.checkAuth();
    }

    if (authStore.isAuthenticated) {
      next();
    } else {
      next('/auth/login');
    }
  });
});
