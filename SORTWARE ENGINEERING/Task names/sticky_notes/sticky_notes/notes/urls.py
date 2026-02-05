from django.urls import path
from . import views

urlpatterns = [
    # Home page - displays all notes
    path('', views.note_list, name='note_list'),
    
    # Displays a specific note (e.g., /note/5/)
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    
    # Creates a new note
    path('note/new/', views.note_create, name='note_create'),
    
    # Edits an existing note (e.g., /note/5/edit/)
    path('note/<int:pk>/edit/', views.note_update, name='note_update'),
    
    # Deletes a note with confirmation (e.g., /note/5/delete/)
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
]