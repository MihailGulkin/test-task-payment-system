from django.urls import (
    path,
)
from .views import (
    BuyView,
    ItemView,
    OrderView
)

urlpatterns = [
    path('buy/<int:pk>/', BuyView.as_view()),
    path('item/<int:pk>/', ItemView.as_view()),
    path('orders/', OrderView.as_view())
]
