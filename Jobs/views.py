from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated
from Jobs.models import JobCategory, UserJob, JobMaterial
from Jobs.serializers import JobCategorySerializer,UserJobSerilizer,JobMaterialSerializer,ActivateJob
import secrets
from django.conf import settings
from Auth.models import User
from django.shortcuts import get_object_or_404
from Wallets.models import Wallet
from Auth.permissions import IsProvider, IsUser,IsProfileOwner
import logging
from .filters import JobCategoryFilter
logger = logging.getLogger(__name__)

# Create your views here.
class JobCategoryView(ListAPIView):
    serializer_class=JobCategorySerializer
    permission_classes=(AllowAny,)
    queryset=JobCategory.objects.all()
    filter_class = JobCategoryFilter


    def post(self, request):
        post_data = {"name":request.data["name"],"details":request.data["details"],"summary":request.data["summary"],"image":request.data["image"],"avg_budget":request.data["avg_budget"],"reviews":request.data["reviews"],"no_running_services":request.data["no_running_services"]}
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Job Category successfully created"},
                        status=status.HTTP_201_CREATED)


class JobCategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):

    serializer_class=JobCategorySerializer
    permission_classes=(AllowAny,)
    queryset=JobCategory.objects.all()
    lookup_field = 'id'
   

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message":'Successfully updated'},serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Job Category has been successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)



class UserJobViewSet(viewsets.ModelViewSet):
    serializer_class=UserJobSerilizer
    permission_classes=(IsUser,)
    queryset = UserJob.objects.all()

    def create(self, request):

        post_data = {
                    # "title":request.data["title"],
                    "details":request.data["details"],
                    # "summary":request.data["summary"],
                    "budget":request.data["budget"],
                    # "job_delivery_time":request.data["job_delivery_time"],
                    "pictures":request.data["pictures"],
                    "location":request.data["location"],

                     }
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        amount = settings.CHARGE_PER_DELIVERY
        user=User.objects.filter(pk=request.user.pk)
        user_wallet=Wallet.objects.filter(user=request.user).first()
        sufficient_balance = user_wallet.is_balance_sufficient(amount)
        if not sufficient_balance:
            serializer.save()
            return Response({'detail': 'Job successfully created, Please Fund your wallet to make Job active'},
                                status=status.HTTP_400_BAD_REQUEST) 
        serializer.save(is_active=True)
        return Response({"message":"Job successfully created"},
                        status=status.HTTP_201_CREATED)

class UpdateJobStatus(ListAPIView):
    permission_classes=(IsUser,)
    serializer_class=UserJobSerilizer
   
    def get_queryset(self,job_id):
        try:
            Job_object = UserJob.objects.get(id=job_id)
            #resolved_game = ResolvedGame.objects.filter(game = game_object)
            print(Job_object)
            return Job_object
        except Exception as e:
            logger.info(e)
            return None
        finally:
            logger.info('this has ran')


    def get(self,request):
        job_objects = UserJob.objects.filter(is_active=False)#.count()
        if job_objects:
            inactive_jobs = [job for job in job_objects]
            data = [ {'game_name':job.title,
                     'game_id':job.id,
                     'is_active':job.is_active,
                     } for job in inactive_jobs]

            payload={
                    'inactive_jobs':data,
                    }
            return Response(payload, status=status.HTTP_200_OK) 
        else:
            return Response({'message': 'Requested resource does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


    # def post(self,request,*args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         job_id = request.data.get('job_id')
    #         Job_object = self.get_queryset(job_id)
    #         print(Job_object)
    #         if Job_object :
    #             job = UserJob.objects.filter(id=job_id)
    #             amount = settings.CHARGE_PER_DELIVERY
    #             user=User.objects.filter(pk=request.user.pk)
    #             user_wallet=Wallet.objects.filter(user=user[0]).first()
    #             sufficient_balance = user_wallet.is_balance_sufficient(amount)
    #             if not sufficient_balance:
    #                 return Response({'detail': 'Please Fund your wallet to make Job active'},
    #                                     status=status.HTTP_400_BAD_REQUEST) 
    #             # active_job= UserJob.objects.filter(is_active=True)
    #             # if active_job:
    #             #     return Response({'message': 'Job is alreadly active'}, status=status.HTTP_400_BAD_REQUEST)
    #             # else:
    #             job.update(is_active=True)
    #             return Response({'message': 'Job has been made active'}, status=status.HTTP_200_OK)

        #     else:
        #         Response({'message': 'Requested Job does not exist. Please check the Job ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        # else:
        #     Response({'message': 'Field errors'}, status=status.HTTP_400_BAD_REQUEST)


class ActivateJob(RetrieveUpdateDestroyAPIView):

    serializer_class=ActivateJob
    permission_classes=(AllowAny,)
    queryset = UserJob.objects.all()
    lookup_field = 'id'
   

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data={"is_active":True}
        serializer = self.get_serializer(instance, data=data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message":'Job successfully activated'}, status=status.HTTP_200_OK)
      

class UserJobRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):

    serializer_class=UserJobSerilizer
    permission_classes=(AllowAny,)
    queryset = UserJob.objects.all()
    lookup_field = 'id'
   

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message":'Successfully updated'},serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User Job has been successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)


class JobMaterialView(ListAPIView):
    serializer_class=JobMaterialSerializer
    permission_classes=(AllowAny,)
    queryset=JobMaterial.objects.all()


    def post(self, request):
        post_data = {"job":request.data["job"],"name":request.data["name"],"price":request.data["price"],"picture":request.data["picture"]}
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Job Material successfully Input"},
                        status=status.HTTP_201_CREATED)


    
class JobMaterialRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):

    serializer_class=JobMaterialSerializer
    permission_classes=(AllowAny,)
    queryset=JobMaterial.objects.all()

    lookup_field = 'id'
   

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message":'Successfully updated'},serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User Job has been successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

  
        