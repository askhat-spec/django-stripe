from django.urls import path
from django.views.generic import TemplateView
from .views import ItemsView, ItemView, CreateCheckoutSessionView


urlpatterns = [
    path('', ItemsView.as_view(), name='main'),
    path('item/<int:pk>/', ItemView.as_view(), name='item'),
    path('buy/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', TemplateView.as_view(template_name='checkout/success.html'), name='success_payment'),
    path('cancel/', TemplateView.as_view(template_name='checkout/cancel.html'), name='cancel_payment'),
]