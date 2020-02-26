from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from core.models import Governorate, City

User = get_user_model()


class SignUpForm(UserCreationForm):
    governorate = forms.ModelChoiceField(queryset=Governorate.objects.all().order_by('title'), label='Governorate')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',
                  'gender', 'birth_date', 'avatar', 'governorate', 'city', 'address',
                  'whatsapp', 'specialist', 'job_title', 'facebook', 'youtube', 'twitter', 'google', 'instagram'
                  )
        # fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['birth_date'] = forms.DateField(widget=forms.SelectDateWidget(), label='Birthday')
        self.fields['city'] = forms.ModelChoiceField(queryset=City.objects.none())

        if 'governorate' in self.data:
            try:
                governorate_id = int(self.data.get('governorate'))
                self.fields['city'].queryset = City.objects.filter(governorate_id=governorate_id).order_by('title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.governorate.city_set.order_by('title')  # need to know

        # self.fields['birth_date'].required = True


class UpdateProfile(forms.ModelForm):

    governorate = forms.ModelChoiceField(queryset=Governorate.objects.all().order_by('title'), label='Governorate')

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'gender', 'birth_date', 'city', 'address',
                  'whatsapp', 'specialist', 'job_title', 'facebook', 'youtube', 'twitter', 'google', 'instagram'
                  )
        # fields = '__all__'

    def save(self, commit=True):
        # do something with self.cleaned_data['governorate']
        return super(UpdateProfile, self).save(commit=commit)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['city'] = forms.ModelChoiceField(queryset=City.objects.none())

        if 'governorate' in self.data:
            try:
                governorate_id = int(self.data.get('governorate'))
                print(governorate_id)
                self.fields['city'].queryset = City.objects.filter(governorate_id=governorate_id).order_by('title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['governorate'].initial = self.instance.city.governorate
            self.fields['city'].queryset = City.objects.filter(governorate_id=self.instance.city.governorate).order_by(
                'title')  # if there is a value

        # self.fields['birth_date'].required = True



