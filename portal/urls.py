# portal/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # (Your existing dashboard URL)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # --- !! THESE ARE THE MISSING LINES !! ---
    path('hiring/', views.hiring_posts_view, name='hiring'),
    path('meetups/', views.meetup_posts_view, name='meetups'),
    path('alumni/', views.alumni_list_view, name='alumni_list'),
    path('post/new/', views.create_post_view, name='create_post'),
    path('students/', views.student_list_view, name='student_list'),
    path('search/', views.search_results_view, name='search_results'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('invites/', views.invites_view, name='invites'),
    path('moderation/', views.content_moderation_view, name='content_moderation'),
    path('moderation/approve/<int:pk>/', views.approve_post_view, name='approve_post'),
    path('moderation/delete/<int:pk>/', views.delete_post_view, name='delete_post'),
    path('mentors/', views.mentor_list_view, name='mentor_list'),
]