from django.db import models
from Auth.models import User
from helpers.models import BaseAbstractModel
from decimal import Decimal
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class JobCategory(BaseAbstractModel):
    """ This is model that categorizes the jobs to be done """

    name= models.CharField(max_length=255, blank=True, null=True)
    details=models.TextField(null=True)
    summary= models.CharField(max_length=255, blank=True, null=True) 
    image= models.ImageField(upload_to='pictures/', null=True)
    total_transactions_amount= models.DecimalField(max_digits=12, decimal_places=2, null=True)
    reviews= models.CharField(max_length=255, blank=True, null=True) 
    no_running_services=models.IntegerField(blank=True, null = True)
    # no_providers= models.IntegerField(blank=True)

    def __str__(self):
        return "{}".format(self.name)



class UserJob(BaseAbstractModel):
    STATUS = (
        ('complete', 'complete'),
        ('in-progress', 'in-progress'),
        ('rejected', 'rejected'),
        ('Not-started','Not-started')
    )

    """This is a model for the jobs input by the user """
    id = models.CharField(max_length=200, primary_key=True, unique=True,)
    title= models.CharField(max_length=255, blank=True, null=True)
    summary= models.CharField(max_length=255, blank=True, null=True)
    details=models.TextField(null=True)
    location=models.CharField(max_length=255, blank=True, null=True)
    # job_delivery_time=models.DateTimeField(null=True, blank=True)
    pictures=ArrayField(
        ArrayField(
            models.CharField(max_length=255, null=True),
            size=8,
        ))
    job_delivery_time=models.CharField(max_length=255, blank=True, null=True)
    # pictures=models.CharField(max_length=255, blank=True, null=True) 
    budget= models.DecimalField(max_digits=12, decimal_places=2, null=True)
    job_category_id= models.ForeignKey(to='Jobs.JobCategory', on_delete=models.DO_NOTHING, null=True) 
    created_by= models.ForeignKey(to='Auth.User', on_delete=models.DO_NOTHING, null=True)
    status=models.CharField(max_length=255, blank=True, default='Not-started',choices=STATUS)
    base_charge_amount=models.DecimalField(max_digits=12, decimal_places=2, null=True)
    # provider_arrival=models.DateTimeField(null=True, blank=True)
    provider_arrival=models.CharField(max_length=255, blank=True, null=True)
    before_pictures=models.ImageField(upload_to='pictures/', null=True)
    after_pictures=models.ImageField(upload_to='pictures/', null=True)
    part_replacement_required=models.BooleanField(default=False)
    provider_job_cost=models.DecimalField(max_digits=12, decimal_places=2, null=True)
    agree_job_cost=models.DecimalField(max_digits=12, decimal_places=2, null=True)
    user_provided_cost=models.DecimalField(max_digits=12, decimal_places=2, null=True) 
    total_cost=models.DecimalField(max_digits=12, decimal_places=2, null=True)
    provider_complete_job=models.BooleanField(default=False)
    user_signoff_on_job=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    @property
    def job_category(self):
        return self.job_category_id.name

class JobMaterial(BaseAbstractModel):
    """This is a model for job materials needed or required """

    job=models.ForeignKey(to='Jobs.UserJob', on_delete=models.DO_NOTHING, null=True)
    name=models.CharField(max_length=255, blank=True, null=True)
    price= models.DecimalField(max_digits=12, decimal_places=2, null=True)
    picture=models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


class Bids(BaseAbstractModel):
    """This is a model for job bids """
    
    job= models.ForeignKey(to='Jobs.UserJob', on_delete=models.DO_NOTHING, null=True)
    # provider=models.ForeignKey(to='Auth.User', on_delete=models.DO_NOTHING, null=True)
    bid_amount= models.DecimalField(max_digits=12, decimal_places=2, null=True)
    bid_status=  models.CharField(max_length=255, blank=True, null=True)
    availability_time=models.DateTimeField(null=True, blank=True)
    base_amount_charged=models.DecimalField(max_digits=12, decimal_places=2, null=True)

    def __str__(self):
        return "{}".format(self.job)

    @property
    def job_name(self):
        return self.job.name

    @property
    def provider_name(self):
        return self.provider.name