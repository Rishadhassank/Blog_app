from django.db.models import Count
from typing import Any
from django.db.models.query import QuerySet
from django.http import  HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post
from .forms import CommentForm
from django.urls import reverse
from django.views.generic import ( ListView, 
                                   DetailView,
                                   CreateView,
                                   UpdateView,
                                   DeleteView
                                 )
from .models import Post





# def home(request):
#     context = {
#         'posts':Post.objects.all()
#     }
#     return render(request,'blog/home.html',context)





class PostListView(ListView): # used class because these are class based view
    model = Post
    template_name = 'blog/home.html'     # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = [ '-date_posted' ]
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(like_count=Count('likes'))
        return queryset


    


   


class UserPostListView(ListView): 
    model = Post
    template_name = 'blog/user_posts.html'     # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = [ '-date_posted' ]
    paginate_by = 5

    # def get_queryset(self):
    #     user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        queryset = super().get_queryset().filter(author=user)
        queryset = queryset.annotate(like_count=Count('likes'))
        return queryset
    
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'






    # All in one
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = self.get_object()  # Get the current post object

    #     # Calculate number of likes for the post
    #     liked = False
    #     if post.likes.filter(id=self.request.user.id).exists():
    #         liked = True
    #     context['number_of_likes'] = post.likes.count()
    #     context['post_is_liked'] = liked

    #     # Get all comments related to the post
    #     context['comments'] = post.comments.all()
    #     # Pass an instance of the comment form to the template
    #     context['comment_form'] = CommentForm()

    #     return context
        

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        post = self.get_object()  # Get the current post object
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = post.likes.count()  # Calculate number of likes dynamically
        data['post_is_liked'] = liked
        return data

    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['comments'] = self.object.comments.all()  # Get all comments related to the post
    #     context['comment_form'] = CommentForm()  # Pass an instance of the comment form to the template
    #     return context
        
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = [ 'title','content' ]

    def form_valid(self, form): 
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = [ 'title','content' ]

    def form_valid(self, form): 
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    



def BlogPostLike(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))    



def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Assuming user is authenticated
            comment.save()
            return redirect('post-detail', pk=post.pk)  # Corrected the redirect argument
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

def about(request):
    return render(request,'blog/about.html', {'title':'about'})












# > LoginRequiredMixin : if logout ,if anyone tries to add a post using url , 
                       # then it shows that 'Login required to post

# UserPassesTestMixin : if someone logout ,if anyone tries to update a post using url , 
                       # then it shows that 'Login required to post