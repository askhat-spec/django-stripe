from django.urls import path
from django.views.generic import TemplateView
from .views import (
    ItemsView,
    ItemView,
    CreatePaymentIntentView,
    CheckoutView,
    get_config
)


urlpatterns = [
    path('', ItemsView.as_view(), name='main'),
    path('item/<int:pk>/', ItemView.as_view(), name='item'),
    # path('buy/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('buy/', CreatePaymentIntentView.as_view(), name='create_payment_intent'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('config/', get_config, name='config'),

    path('checkout/success/', TemplateView.as_view(template_name='checkout/success.html'), name='success_payment'),
    path('checkout/cancel/', TemplateView.as_view(template_name='checkout/cancel.html'), name='cancel_payment'),
]