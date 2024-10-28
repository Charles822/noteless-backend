from django.urls import path
from .views import StripeCheckoutViewPack1, StripeCheckoutViewPack2, StripeCheckoutViewPack3

urlpatterns = [
    path('create-checkout-session-pack1', StripeCheckoutViewPack1.as_view()),
    path('create-checkout-session-pack2', StripeCheckoutViewPack2.as_view()),
    path('create-checkout-session-pack3', StripeCheckoutViewPack3.as_view()), 
]