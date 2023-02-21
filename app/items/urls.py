from django.urls import path
from .views import ItemsView, ItemView

urlpatterns = [
    path('', ItemsView.as_view(), name='main'),
    path('item/<int:pk>', ItemView.as_view(), name='item')
]