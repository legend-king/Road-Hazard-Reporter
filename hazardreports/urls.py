from django.urls import path
from .import views

urlpatterns = [
    path("add_report", views.add_report, name='add-report'),
    path("", views.user_reports, name="home"),
    path("location_reports", views.location_reports, name='location-reports'),
    path("update_status/<int:report_id>/", views.update_status, name='update-status'),
    path('visualize', views.generate_pie_chart_data, name='visualize'),
]
