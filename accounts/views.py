from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


from .forms import SignUpForm, UpdateProfile, EmailChangeForm
from core.models import City
from .tokens import account_activation_token

'''
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
'''


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES,)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    user = get_user_model()

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


def load_cities(request):
    governorate_id = request.GET.get('governorate')
    cities = City.objects.filter(governorate_id=governorate_id).order_by('title')
    print(request.GET.get('governorate'))
    return render(request, 'accounts/city_dropdown_list_options.html', {'cities': cities})


@login_required()
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required()
def update_profile(request):
    if request.method == 'POST':
        user_profile = UpdateProfile(request.POST, instance=request.user)
        if user_profile.is_valid():
            user_profile.save()
            # messages.success(request, _('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            return redirect('profile')
            # messages.error(request, _('Please correct the error below.'))
    else:

        user_profile = UpdateProfile(instance=request.user)
    return render(request, 'accounts/update_profile.html', {'form': user_profile, })


@login_required
def email_change(request):
    if request.method == 'POST':
        current_user = request.user
        form = EmailChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, _('successfully updated.'))
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email_change.html', {
                'user': current_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(current_user.pk)),
                'token': account_activation_token.make_token(current_user),
            })
            current_user.email_user(subject, message)
            return redirect('account_activation_sent')
        else:  # if the form is not valid, pass the invalid form in the context
            return render(request, 'accounts/email_change.html', {'form': form, })
    form = EmailChangeForm(user=request.user)
    return render(request, 'accounts/email_change.html', {'form': form, })


def activate_change(request, uidb64, token):
    user = get_user_model()

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email = user.temp_email
        user.temp_email = None
        user.save()
        return redirect('login')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


