from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm
from core.models import City


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES,)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('password_change')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def load_cities(request):
    governorate_id = request.GET.get('governorate')
    cities = City.objects.filter(governorate_id=governorate_id).order_by('title')
    print(request.GET.get('governorate'))
    return render(request, 'accounts/city_dropdown_list_options.html', {'cities': cities})
