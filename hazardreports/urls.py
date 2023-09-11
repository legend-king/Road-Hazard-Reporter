from django.urls import path
from .import views

urlpatterns = [
    path("add_report", views.add_report, name='add-report'),
    path("", views.user_reports, name="home"),
]
