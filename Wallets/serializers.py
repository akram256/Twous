from rest_framework import serializers
from .models import Wallet


class UserWalletBalanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Wallet
        fields = ('balance', 'bonus_balance','user', 'last_credited_amount','wallet_accountName','wallet_accountNumber' ,'wallet_bankName')



class WebhookSerializer(serializers.Serializer):

    transactionReference = serializers.CharField(allow_blank=True, max_length=254)
    paymentReference = serializers.CharField(allow_blank=True, max_length=254)
    amountPaid = serializers.CharField(allow_blank=True, max_length=254)
    totalPayable = serializers.CharField(allow_blank=True, max_length=254)
    paidOn = serializers.CharField(allow_blank=True, max_length=254)
    paymentStatus = serializers.CharField(allow_blank=True, max_length=254)
    paymentDescription = serializers.CharField(allow_blank=True, max_length=254)
    transactionHash = serializers.CharField(allow_blank=True, max_length=254)
    currency = serializers.CharField(allow_blank=True, max_length=254)
    paymentMethod  = serializers.CharField(allow_blank=True, max_length=254)
    product  = serializers.CharField(allow_blank=True, max_length=254)
    cardDetails = serializers.CharField(allow_blank=True, max_length=254)
    accountDetails = serializers.CharField(allow_blank=True, max_length=254)
    accountPayments = serializers.CharField(allow_blank=True, max_length=254)
    customer = serializers.CharField(allow_blank=True, max_length=254)