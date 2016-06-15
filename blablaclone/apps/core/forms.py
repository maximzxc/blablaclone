from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field

from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm as AllAuthSignupForm
from allauth.account.forms import LoginForm as AllAuthLoginForm

from core.models import (
    City,
    Ride,
    User,
    RideRequest,
)


class RideUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RideUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Ride
        fields = [
            'from_city',
            'to_city',
            'departure_time',
            'will_visit',
            'driver',
            'free_places',
            'passangers',
            'price',
            'title',
        ]


class RideCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RideCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Ride
        fields = [
            'from_city',
            'to_city',
            'departure_time',
            'will_visit',
            'driver',
            'passangers',
            'free_places',
            'price',
            'title',
        ]


class UserUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'surname',
            'car',
            'phone',
            'birthdate',
            'about',
            'photo',
        ]


class RideRequestCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RideRequestCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = RideRequest
        exclude = [
            'user',
            'ride',
        ]
        fields = [
            'message',
        ]


class LoginForm(AllAuthLoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('login_form', _('Login')))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'


class SignUpUserForm(AllAuthSignupForm):

    email = forms.EmailField(
        max_length=150,
        required=True,
    )
    name = forms.CharField(
        required=True,
        max_length=150,
    )
    surname = forms.CharField(
        required=True,
        max_length=150,
    )
    car = forms.CharField(
        required=False,
        max_length=150,
    )
    photo = forms.ImageField(
        required=False,
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(SignUpUserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('signup_user_form', _('SignUp')))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_action = reverse('register') + '?user_type=user'
        self.helper.form_action += "&next=%s" % request.GET.get('next', '')

    def save(self, request):
        user = super(SignUpUserForm, self).save(request)
        setattr(user, 'email', self.cleaned_data.get('email'))
        setattr(user, 'name', self.cleaned_data.get('name'))
        setattr(user, 'surname', self.cleaned_data.get('surname'))
        setattr(user, 'car', self.cleaned_data.get('car'))
        setattr(user, 'photo', self.cleaned_data.get('photo'))
        user.save()
        return user
