from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    # path('category', views.CategoriesView.as_view()),
    path('secret/',views.secret),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('manager-view/', views.manager_view),
    path('throttle-check-anon/', views.throttle_check_anon, name='throttle_check_anon'),
    path('throttle-check-user/', views.throttle_check_user, name='throttle_check_user'),
    path('admin/menuitem/create/', views.MenuItemCreateView.as_view(), name='menuitem-create'),
    path('admin/category/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('manager/update-featured/', views.UpdateFeaturedItemView.as_view(), name='update-featured'),
    path('manager/assign-order/', views.AssignOrderToDeliveryView.as_view(), name='assign-order'),
    path('delivery/orders/', views.delivery_team_orders, name='delivery-orders'),
    path('delivery/order/update/', views.UpdateOrderStatusView.as_view(), name='update-order'),
    path('customer/categories/', views.CategoryListView.as_view(), name='categories-list'),
    path('customer/menuitems/', views.MenuItemListView.as_view(), name='menuitems-list'),
    path('customer/cart/add/', views.AddToCartView.as_view(), name='cart-add'),
    path('customer/order/', views.PlaceOrderView.as_view(), name='place-order'),
]
