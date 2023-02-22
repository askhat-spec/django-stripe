from django.urls import path
from . import views


urlpatterns = [
    path('', views.order_detail, name='order_detail'),
    path('add/<int:item_id>', views.order_add, name='order_add'),
    path('remove/<int:item_id>', views.order_remove, name='order_remove'),
]