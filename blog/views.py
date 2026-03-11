
from django.urls import reverse
from django.views.generic import ListView, DetailView 

from blog.models import Post


# Create your views here.
class BlogView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post_list'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'