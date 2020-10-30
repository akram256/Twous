from django.urls import path
from Wallets.views import WalletBalanceView,MonnifyWebhookView,AutoUpdateMOnifyAccounts


urlpatterns = [
    path('wallet/balance', WalletBalanceView.as_view(), name='wallet-balance'),
    path('confirm/monnify/transaction', MonnifyWebhookView.as_view(), name='monify-webhook'),
    path('auto/update/monify',AutoUpdateMOnifyAccounts.as_view(),name='auto-update'),
]