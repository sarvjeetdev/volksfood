from django.contrib import admin
from django.urls import path
from .views import SignUpView, MyLoginView, MyLogoutView
from Food import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', views.login_user, name='login'),
    path('home', views.home, name='home'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('checkout/',views.checkout,name='checkout'),
    path('orders/',views.order_history,name='orders'),
    path('contact/',views.contact,name='contact'),
    path('food/search/', views.food_search, name='food_search'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)