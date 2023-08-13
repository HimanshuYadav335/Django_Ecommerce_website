from django.urls import path
from . import views
urlpatterns=[
    path('home/',views.show,name="home"),
    path('signup/',views.send_mail_on_signup,name="signup"),
    path('login/',views.send_mail_on_login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('detail/<int:id>',views.product_detail,name='detail'),
    path('contact/',views.contact,name="contact"),
    path('delete_cart/<int:id>',views.delete_cart,name="delete_cart"),
    path('cart',views.cart_detail,name='cart_detail'),
path('update_cart/<int:id>', views.inc_dec, name='update_cart'),
path('confirm_order/<int:id>',views.proceed_order,name="confirm_order"),
path('order_status',views.order_status,name="order_status"),
path('generate_razorpay_order/<int:productID>/',views.generate_razorpay_order,name="generate_razorpay_order")
    # path('login/',views.login)
    # path('basic/',StudentView.as_view())
] 