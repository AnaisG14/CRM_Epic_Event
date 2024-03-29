from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import LoginForm


class LoginPage(View):
    template_name = 'authentication/login_page.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                if user.role == 'MANAGER':
                    return redirect('admin/')
                return redirect('api/client/')
            else:
                message = 'Connexion failed. Please verify your username and password or contact your administrator.'
        return render(request, self.template_name, context={'form': form, 'message': message})
