from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('event/<int:event_id>/feedback/', views.event_feedback, name='event_feedback'),
    
    path('event/<int:event_id>/rate-organizer/', views.rate_organizer, name='rate_organizer'),
    
    path('event/<int:event_id>/rate-volunteer/<int:volunteer_id>/', views.rate_volunteer, name='rate_volunteer'),
    
    path('ratings/', views.user_ratings, name='my_ratings'),
    path('ratings/<int:user_id>/', views.user_ratings, name='user_ratings'),
]