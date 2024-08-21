from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login

class RegisterView(TemplateView):

    template_name = 'registration/sign_up.html'

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            print(repr(form.errors))
            content = {
                'form': form
            }
            return render(request, self.template_name, content)


