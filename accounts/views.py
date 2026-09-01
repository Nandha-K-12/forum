from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
    PasswordChangeDoneView as BasePasswordChangeDoneView,
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetCompleteView as BasePasswordResetCompleteView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetView as BasePasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View

from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


class SignInView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class SignOutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'accounts/logout.html')

    def post(self, request):
        logout(request)
        return redirect('home')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user


# Aliases for compatibility
signin = SignInView.as_view()
signout = SignOutView.as_view()