from rest_framework import serializers
from Jobs.models import JobCategory, UserJob,JobMaterial


class JobCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobCategory
        fields = ('id','name', 'details','summary', 'image','total_transactions_amount', 'reviews','no_running_services')


class UserJobSerilizer(serializers.ModelSerializer):
    class Meta:
        model = UserJob
        fields = ('id','details','location',
                  'pictures','budget',
                  'created_by'
                #   ,'status',
                #   'base_charge_amount'
                #  'job_category'
                # 'job_delivery_time',
                #   'provider_arrival','before_pictures','after_pictures','part_replacement_required','provider_job_cost',
                #   'agree_job_cost','user_provided_cost','total_cost', 'provider_complete_job','user_signoff_on_job',
                # 'is_active',
                )

        extra_kwargs ={
            'id': {
                'read_only': True
        }
        }
class JobMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model= JobMaterial
        fields=('job', 'name', 'price', 'picture','created_at')

class ActivateJob(serializers.ModelSerializer):
    class Meta:
        model =UserJob
        fields=fields = ('id','details','location','is_active',
                'budget'
                )

        extra_kwargs ={
            'id': {
                'read_only': True
        },
        'pictures':{
            'read_only':True
        }
        }