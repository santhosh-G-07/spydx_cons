# ✅ Clean and working version of auth only (signup, login, logout, dashboard)
# ✅ No AI, no resume, no extra dashboard pages wired

# consultant_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),


    # Consultant authentication
    path('consultant/signup/', views.consultant_signup, name='consultant_signup'),
    path('consultant/login/', views.consultant_login, name='consultant_login'),
    path('consultant/logout/', views.consultant_logout, name='consultant_logout'),
    path('consultant/dashboard/', views.consultant_dashboard_view, name='consultant_dashboard'),

    # Admin placeholders
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/signup/', views.admin_signup, name='admin_signup'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
     path('consultant/profile/', views.consultant_profile, name='consultant_profile'),
    
   
    
    path('consultant/notifications/', views.consultant_notifications, name='consultant_notifications'),
    path('consultant/tracker/', views.consultant_tracker, name='consultant_tracker'),
    path('consultant/reports/', views.consultant_reports, name='consultant_reports'),
    path('consultant/settings/', views.consultant_settings, name='consultant_settings'),

    path('consultant/projects/', views.project_list_view, name='consultant_projects'),
    path('consultant/projects/add/', views.project_add_view, name='consultant_project_add'),
    path('consultant/resume/', views.resume_upload_view, name='consultant_resume'),
    
# or for a list or upload page if different
# path('consultant/resume/upload/', views.resume_upload_view, name='consultant_resume_upload'),
# path('consultant/resume/list/', views.resume_list_view, name='consultant_resume_list'),

   path('consultant/ats/', views.ats_upload_view, name='consultant_ats_upload'),
    path('consultant/ats/mistakes/', views.ats_view_mistakes, name='consultant_ats_mistakes'),

]
