from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .models import BlogPost, UserProfile
from .forms import BlogPostForm, LoginForm, CustomUserCreationForm
from django.shortcuts import render, redirect
from django.views import View


class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.bio = form.cleaned_data["bio"]
            user.profile_picture = form.cleaned_data["profile_picture"]
            user.save()

            messages.success(
                request,
                "Your account has been created successfully! You can now log in.",
            )
            return redirect(
                "login"
            ) 

        return render(request, self.template_name, {"form": form})


# Blog Post List View
class PostListView(ListView):
    model = BlogPost
    template_name = "post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


class PostDetailView(DetailView):
    model = BlogPost
    template_name = "post_detail.html"


@method_decorator(login_required, name="dispatch")
class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@method_decorator(login_required, name="dispatch")
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class SearchView(ListView):
    model = BlogPost
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return BlogPost.objects.filter(
            title__icontains=query
        ) | BlogPost.objects.filter(content__icontains=query)


class UserProfileView(DetailView):
    model = UserProfile
    template_name = "user_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user__username=self.kwargs["username"])


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, f"Welcome back, {form.get_user()}")
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("post_list")
