from django.shortcuts import render
from Wallets.serializers import UserWalletBalanceSerializer,WebhookSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
import json
from datetime import datetime,date
import pytz
from django.conf import settings
from Auth.models import User
from utils import requested_services
from rest_framework import status
from decimal import Decimal
import logging
from Wallets.models import Wallet
from django.conf import settings
from Jobs.models import UserJob

logger = logging.getLogger(__name__)

# Create your views here.
class WalletBalanceView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            user_wallet = Wallet.objects.create(user=request.user)
        serializer = UserWalletBalanceSerializer(user_wallet)
        response = {
                'status': '00',
                'data': serializer.data
            }
        return Response(response, status=status.HTTP_200_OK)


class MonnifyWebhookView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = WebhookSerializer
    def get_object(self,**data):
        hash_text = requested_services.hashKey(**data)
        return hash_text

    def post(self, request):

        clientSecret = settings.MONNIFY_SECRET_KEY
        paymentReference = request.data['paymentReference']
        amountPaid = request.data['amountPaid']
        paidOn = request.data['paidOn']
        user_email = request.data['customer']['email']
        transactionReference = request.data['transactionReference']
        trans_url = requested_services.MONNIFY_URLS['get_transaction']
        #f'https://sandbox.monnify.com/api/v1/merchant/transactions/query?transactionReference={transactionReference}'
        login_url = requested_services.MONNIFY_URLS['login']
        data = {'clientSecret':clientSecret,
                'paymentReference':paymentReference,
                'amountPaid':amountPaid,
                'paidOn':paidOn,
                'transactionReference':transactionReference 
                }
        
        calc_hash = self.get_object(**data)
        if calc_hash == request.data["transactionHash"]:
            token = requested_services.generate_monnify_token(**{'transactiontoken':True})
            request_data = {'transactionReference':transactionReference}
            try:
                info = requested_services.ExtendedRequests.get_data(trans_url,token=token[1],token_data={'auth_type':'Basic'},**request_data)
                #info = services.ExtendedRequests2.get_data(trans_url,token=token[1],token_data={'auth_type':'Basic'},)
            except Exception as e:
                logger.info(e)
                return Response({'message': str(e), 'status': '99'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if (info[1]['responseMessage'] == 'success') and (info[1]['responseBody']["paymentStatus"] == 'PAID'):
                    amount = Decimal(amountPaid)
                    data = request.data
                    try:
                        user = User.objects.get(email=user_email)
                        user_wallet = Wallet.objects.get(user=user)
                        prev_bal = Decimal(user_wallet.balance) + Decimal(user_wallet.bonus_balance)
                        user_wallet.balance += Decimal(amount)
                        new_bal = Decimal(user_wallet.balance) + Decimal(user_wallet.bonus_balance)
                        user_wallet.save()
                    except Wallet.DoesNotExist:
                        prev_bal = Decimal('0.00')
                        new_bal = Decimal(amount)
                        
                    # activate job
                    try:
                        user = User.objects.get(email=user_email)
                        print(user, 'hererre')
                        job=UserJob.objects.get(user=user)
                        print(job)
                        job.is_active = True
                        job.save()
                    except:
                        UserJob.DoesNotExist
                        pass
                    

                    #     user_wallet = UserWallet.objects.create(user=user, balance=Decimal(amount)) #create wallet for old users that might not have wallet
                    # WebTransactionRecord.objects.create(
                    #     user=user,
                    #     transaction=transactionReference,
                    #     amount=amount, 
                    #     reference=paymentReference,
                    #     status='success',
                    #     transaction_type='WALLET'
                    # )
                    # data = dict(user=user, transaction_type='CREDIT',transaction_category = 'WALLET DEPOSIT', main_balance = amount,
                    #             bonus_balance = Decimal('0.00'), previous_balance=prev_bal , new_balance =new_bal , 
                    #             description = services.WALLET_DESCRIPTIONS['DEPOSIT'],
                    #             )
                    # UserWalletHistory.objects.create(**data)
                    response = {
                        'status': '00',
                        'message': "Wallet funded successfully "
                    }
                    logger.info('wallet successfully funded with monnify')
                    return Response(response, status=status.HTTP_200_OK)
                else:
        
                    return Response({'message': f"from monnify {info[1]['responseMessage']}", 'status': '99'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "transaction hash doesnt match", 'status': '99'}, status=status.HTTP_400_BAD_REQUEST)

class AutoUpdateMOnifyAccounts(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        all_user = User.objects.all()
        for user in all_user:
            userwallet = UserWallet.objects.filter(user=user)
            if userwallet.exists():
                userwalletref = userwallet[0].wallet_accountReference
            else:
                print(f'No wallet available')
                userwalletref = None
            if user.first_name and user.last_name and userwallet.exists() and not userwalletref:
                reserve_acc_url = services.MONNIFY_URLS['account_reservation']
                monnify_data = {"accountReference": str(user.id),
                "accountName": user.first_name + user.last_name,
                "currencyCode": services.monnify_currency_code,
                "contractCode": services.monnify_contract_code,
                "customerEmail": user.email,}
                mstatus,token = services.generate_monnify_token()
                try:
                    info = services.ExtendedRequests.post_data(reserve_acc_url,token=token,token_data={'auth_type':'Bearer'},**monnify_data)

                except Exception as e:
                    print(e)
                else:
                    if (info[0] in [200,201,202,203,204]) and (info[1]["responseMessage"] == "success") :
                        accountReference = info[1]["responseBody"]["accountReference"]
                        accountName = info[1]["responseBody"]["accountName"]
                        accountNumber = info[1]["responseBody"]["accountNumber"]
                        bankName = info[1]["responseBody"]["bankName"]
                        bankCode = info[1]["responseBody"]["bankCode"]
                        reservationReference = info[1]["responseBody"]["reservationReference"]
                        userwallet = UserWallet.objects.get(user=user)
                        userwallet.wallet_accountReference=accountReference
                        userwallet.wallet_accountName=accountName
                        userwallet.wallet_accountNumber=accountNumber
                        userwallet.wallet_bankName=bankName
                        userwallet.wallet_bankCode=bankCode
                        userwallet.wallet_reservationReference=reservationReference
                        userwallet.save()

                        print(f'moonify reservation of account was successful, status {info[0]}')
   
                    else:
                        print( f'code {info[0]} {info[1]["responseMessage"]}')
        
        return Response({'message':'All moonify reservation of accounts were successful'}, status=status.HTTP_200_OK)