const routes = [
  {
    path: '/home/',
    component: () => import('layouts/MainLayout.vue'),
    beforeEnter: (to, from, next) => {
      guard(to, from, next);
    },
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'manage_websites', component: () => import('pages/MagageWebsitesPage.vue') },
      { path: 'manage_apps', component: () => import('pages/MagageAppsPage.vue') },
      { path: 'datas', component: () => import('pages/DataPage.vue') },
      { path: 'models', component: () => import('pages/ModelsPage.vue') },
      { path: 'logs', component: () => import('pages/LogsPage.vue') }
    ]
    
  },

  {
    path: '/login',
    component: () => import('pages/LoginPage.vue')
  },

  {
    path: '/register',
    component: () => import('pages/RegisterPage.vue')
  },

  {
    path:'/:catchAll(.*)*',
    redirect: '/login'
  }
]

const guard = ((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token'); 
    if (!isAuthenticated) {
      next('/login');
    } else {
      next();
    }
  } 
);

export default routes
