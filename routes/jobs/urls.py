from django.urls import path,include
from rest_framework.routers import DefaultRouter

from Jobs.views import (
                        JobCategoryView,UserJobViewSet,JobMaterialView,
                        JobMaterialRetrieveUpdateDestroy,UserJobRetrieveUpdateDestroy,
                        UpdateJobStatus,ActivateJob
                        )

# app_name = 'Jobs'
router_v1= DefaultRouter()
router_v1.register('jobs',UserJobViewSet)

urlpatterns = [
    path("job-categories/", JobCategoryView.as_view(), name='job-category'),
    path("job-categories/<str:id>", JobCategoryView.as_view(), name='update-and-delete-category'),
    path('', include(router_v1.urls)),
    path("job/<str:id>",UserJobRetrieveUpdateDestroy.as_view(),name='update-and-delete-user-job'),
    path("jobmaterials",JobMaterialView.as_view(),name='add-and-get-job-material'),
    path("inactive_jobs",UpdateJobStatus.as_view(), name='inactive-jobs'),
    path("jobmaterials/<str:id>",JobMaterialRetrieveUpdateDestroy.as_view(),name='delete-and-update-job-material'),
    path('activate_job/<str:id>', ActivateJob.as_view(), name='activate_job')
    ]