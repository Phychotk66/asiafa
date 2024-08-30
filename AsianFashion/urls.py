from django.urls import path
from . import views
# ex:/AsianFashion/ 
app_name = "AsianFashion"
urlpatterns = [
    # Not Signed-in Version of APP:
    path("", views.women_bag, name="main_page"),
    path("women/bag/", views.women_bag, name="women_bag"),
    path("women/phonecase/", views.women_phonecase, name="women_phonecase"),
    path("women/leather/", views.women_leather, name="women_leather"),
    path("men/bag/", views.men_bag, name="men_bag"),
    path("<int:item_id>/", views.item_detail, name = "item_detail"),
    path("<int:item_id>/buy_or_add_item_to_cart/", views.buy_or_add_item_to_cart, name="buy_or_add_item_to_cart"),

    # Signed-in Version of APP:
    path("signed_in/<slug:customer_uuid>/women/bag/", views.women_bag_signed_in, name = "women_bag_signed_in"),
    path("signed_in/<slug:customer_uuid>/women/phonecase/", views.women_phonecase_signed_in, name="women_phonecase_signed_in"),
    path("signed_in/<slug:customer_uuid>/women/leather/", views.women_leather_signed_in, name="women_leather_signed_in"),
    path("signed_in/<slug:customer_uuid>/men/bag/", views.men_bag_signed_in, name="men_bag_signed_in"),
    path("signed_in/<slug:customer_uuid>/<int:item_id>/", views.item_detail_signed_in, name="item_detail_signed_in"),
    path("signed_in/<slug:customer_uuid>/cart/",views.cart_signed_in, name="cart_signed_in"),
    
    # Utilities:
    path("sign_in/", views.sign_in, name = "sign_in"),
    path("sign_up/", views.sign_up, name = "sign_up"),    
    path("sign_out/", views.sign_out, name="sign_out"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("check_out/", views.check_out, name="check_out"),
    path("pay", views.pay, name="pay"),
    path("payment_success", views.payment_success, name="payment_success"),
    path("payment_cancel", views.payment_cancel, name="payment_cancel")
]