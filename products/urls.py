from django.urls import path , include
from . import views
from django.contrib import admin

urlpatterns = [
    path('',views.homepage,name='home'),

    path('login/',views.login_page,name='login'),
    path('login/forgot-password',views.forgotpass,name='forgot-password'),
    path('sign_up/',views.signup,name='sign-up'),
    path('sign_up/verify-number',views.number_verify,name='verify-numver'),
    path('sign_up/set-password',views.set_password,name='set_password'),
    path('logout',views.user_logout,name='logout'),

    path('send_ticket/<str:ticket_type>/',views.send_ticket,name='send-ticket'),
    path('ticket-sent/',views.registered_ticket,name='registered-ticket'),
    path('buy-product/<int:pid>/',views.buy_product1,name='buy-product'),
    path('confirm-buy/',views.buy_product2,name='confirm'),
    path('order-sent/',views.registered_order,name='resgtered-order'),

    path('products/',views.view_products,name='products'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('about-us/',views.about_us,name='about-us'),
    path('resume/<str:slug>/', views.resume_detail_view, name='resume_detail'),
]
