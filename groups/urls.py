from django.urls import path
from .views import (
    CreateEqubGroupView,
    JoinEqubGroupView,
    MakePaymentView,
    RotatePayoutView,
    GroupDetailView,
    GroupLedgerView,
    AdminGroupList
)

urlpatterns = [
    path('', CreateEqubGroupView.as_view(), name='create-group'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('admin/all/',AdminGroupList.as_view(),name='all-equb-groubs'),
    path('<int:pk>/join/', JoinEqubGroupView.as_view(), name='join-group'),
    path('<int:pk>/pay/', MakePaymentView.as_view(), name='make-payment'),
    path('<int:pk>/rotate/', RotatePayoutView.as_view(), name='rotate-payout'),
    path('<int:pk>/ledger/', GroupLedgerView.as_view(), name='group-ledger'),
]