const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: {public : true},
    children: [
      {path : '', component: () => import('pages/OnboardingPage.vue')},

    ]
  },
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    meta: {public : true},
    children: [
      {path : 'login', component: () => import('pages/Login/LoginStep1.vue')},
      {path : 'otp', component: () => import('pages/Login/OtpPage.vue')},
      {path : 'set-password', component: () => import('pages/Login/NewPass.vue')},
      {path : 'sign-up', component: () => import('pages/Login/SignUp-Step1.vue')},
      {path : 'create-user', component: () => import('pages/Login/CreateUser.vue')},
      {path : 'create-password', component: () => import('pages/Login/NewPass.vue')},
    ]
  },
  {
    path: '/home',
    meta: {public : true},
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      {path : '', component: () => import('pages/Home/HomePage.vue')},
      {path:'profile', component: () => import('src/pages/Home/Profile/ProfilePage.vue') },
      {path:'shop', component: () => import('src/pages/Home/Shop/ShopHomePage.vue') },

    ]
  },
  {
    path: '/account',
    component: () => import('layouts/HomeLayout.vue'),
    meta: { hideFooter: true, hideHeader: true,public : true },
    children: [
      {path:'wallet', component: () => import('src/pages/Home/wallet/WalletPage.vue'), meta: { hideFooter: false, hideHeader: false,public : true }, },
      {path:'', component: () => import('src/pages/Home/wallet/withdrawal/WithdrawPage.vue'),meta : {title : 'برداشت وجه'} },
      {path: 'buy/:type', component: () => import('pages/Home/wallet/AssetDetails/BuyAssetPage.vue')},
      {path: 'sell/:type', component: () => import('pages/Home/wallet/AssetDetails/SellAssetPage.vue')},
      {path:'asset-detail/:type', component: () => import('pages/Home/wallet/AssetDetails/AssetDetailsPage.vue') },
      {path:':slug', component: () => import('src/pages/Home/wallet/withdrawal/WithdrawalSlug.vue'),meta : {title : 'برداشت وجه'} },
      {path: 'product-details/:id', name: 'product-details',component: () => import('pages/Home/wallet/ProductsShop/ProductDetails.vue') },
      {path:'delivery-inperson', component: () => import('pages/Home/wallet/ProductsShop/PhysicalDeliveryPage.vue'), },
      {path:'deposit', component: () => import('pages/Home/wallet/DepositePage.vue'), meta: { title: 'واریز وجه' } },
      {path:'edit', component: () => import('src/pages/Home/Profile/EditProfilePage.vue'), meta : { title : 'ویرایش پروفایل'} },
      {path:'notifications', component: () => import('src/pages/Home/Profile/NotificationsPage.vue'), meta : { title : 'نوتیفیکیشن ها'} },
      {path:'history', component: () => import('src/pages/Home/Profile/HistoryTransactionsProfilePage.vue'), meta : { title : 'تاریخچه سفارشات'} },
      {path:'BankCard', component: () => import('src/pages/Home/Profile/ShebaCardsPage.vue'), meta : { title : 'شماره شبا'} },
      {path:'invite-friends', component: () => import('src/pages/Home/Profile/InviteFriendsPage.vue'), meta : { title : 'دعوت از دوستان'} },
      {path:'about-us', component: () => import('src/pages/Home/Profile/AboutUsPage.vue'), meta : { title : 'درباره ما'} },
      {path:'address', component: () => import('src/pages/Home/Profile/AddressesPage.vue'), meta : { title : 'ادرس ها'} },
      {path:'products-shop-detailes/:id',name:'product-shop-details', component: () => import('src/pages/Home/Shop/productsDetailsShopHome.vue')},

    ]
  },


  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
