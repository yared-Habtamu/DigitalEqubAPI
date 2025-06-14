from django.urls import path
from .views import PaymentView

urlpatterns = [
    path('groups/<int:group_id>/pay/', PaymentView.as_view(), name='make-payment'),
]