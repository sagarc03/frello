import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/DashBoard.vue'),
    },
    {
      path: '/project',
      name: 'project-page',
      component: () => import('@/views/ProjectPage.vue'),
    },
  ],
});

export default router;
