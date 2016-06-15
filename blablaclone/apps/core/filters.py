import django_filters
import django_select2

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Reset

from core.models import (
    City,
    Ride,
    User,
    RideRequest,
)


class CityChoiceField(django_select2.AutoModelSelect2Field):
    queryset = City.objects.all()
    search_fields = ['name__icontains']


class RideChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Ride.objects.all()
    search_fields = ['title__icontains']


class UserChoiceField(django_select2.AutoModelSelect2Field):
    queryset = User.objects.all()
    search_fields = [
        'name__icontains',
        'surname__icontains',
        'car__icontains',
        'phone__icontains',
        'about__icontains',
    ]


class RideRequestChoiceField(django_select2.AutoModelSelect2Field):
    queryset = RideRequest.objects.all()
    search_fields = ['message__icontains']


class CityChoiceFilter(django_filters.Filter):
    field_class = CityChoiceField


class RideChoiceFilter(django_filters.Filter):
    field_class = RideChoiceField


class UserChoiceFilter(django_filters.Filter):
    field_class = UserChoiceField


class RideRequestChoiceFilter(django_filters.Filter):
    field_class = RideRequestChoiceField


class RideListViewFilter(django_filters.FilterSet):

    from_city = CityChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'From_city',
                'minimumInputLength': 0}))

    to_city = CityChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'To_city',
                'minimumInputLength': 0}))

    @property
    def form(self):
        form = super(RideListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Ride

        fields = [u'from_city', u'to_city']

        exclude = []


# Have to call it clearly to help django_select2 register fields
CityChoiceField()
RideChoiceField()
UserChoiceField()
RideRequestChoiceField()
