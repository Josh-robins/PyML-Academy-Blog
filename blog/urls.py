from django.urls import path
from .views import BlogView, PostDetailView

urlpatterns = [
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('', BlogView.as_view(), name='home'),  
]