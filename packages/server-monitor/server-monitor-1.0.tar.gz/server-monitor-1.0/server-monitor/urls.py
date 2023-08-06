from django.urls import path 
from . import views

urlpatterns = [
    path('check/health/', views.HealthCheckView.as_view()),
    path('choices/', views.AvailableSystemMonitoringChoicesView.as_view()),
    path('data/', views.ReturningSystemDataView.as_view()),
    path('job/create/', views.SettingCronJobForCurrentUserView.as_view()),
    path('job/edit/', views.EditingACronJobView.as_view()),
    path('job/check/', views.CheckingIfACronJobIsPresentOrNotView.as_view()),
    path('job/delete/', views.DeletingACronJobView.as_view()),
    path('job/delete/all/', views.DeletingAllCronJobView.as_view()),
]