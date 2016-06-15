from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView
)

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from enhanced_cbv.views import ListFilteredView
from allauth.account.utils import complete_signup
from allauth.account.app_settings import EMAIL_VERIFICATION

from .decorators import ForbiddenUser

from .forms import LoginForm
from .forms import SignUpUserForm

from core.models import (
    City,
    Ride,
    User,
    RideRequest,
)
from core.forms import (
    RideUpdateForm,
    RideCreateForm,
    UserUpdateForm,
    RideRequestCreateForm,
)


from core.filters import (
    RideListViewFilter,
)


class RideDetailView(DetailView):

    """Ride detail view"""
    model = Ride
    slug_field = "slug"
    template_name = "ride-detail.html"


class RideUpdateView(UpdateView):

    """Ride update view"""
    model = Ride
    form_class = RideUpdateForm
    slug_field = "slug"
    template_name = "ride-update.html"

    def get_object(self, queryset=None):
        obj = super(RideUpdateView, self).get_object(queryset)
        if obj.driver.pk != self.request.user.pk:
            raise Http404("Only owner can update Ride")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Ride succesfully updated"))
        return "/"


class RideCreateView(CreateView):

    """Ride create view"""
    model = Ride
    form_class = RideCreateForm
    template_name = "ride-create.html"

    def get_success_url(self):
        messages.success(self.request, _("Ride succesfully created"))
        return reverse("ride-detail", args=[self.object.slug, ])


class RideDeleteView(DeleteView):

    """Ride delete view"""
    model = Ride
    slug_field = "slug"
    template_name = "ride-delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Ride succesfully deleted"))
        return "/"


class RideListView(PaginationMixin, OrderableListMixin, ListFilteredView):

    """Ride list view"""

    template_name = "ride-list.html"

    model = Ride
    paginate_by = 10
    orderable_columns = [
        "from_city",
        "to_city",
        "departure_time",
        "will_visit",
        "free_places",
        "driver",
        "passangers",
        "price",
        "slug",
        "title",
    ]
    orderable_columns_default = "-id"
    filter_set = RideListViewFilter


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class UserUpdateView(UpdateView):

    """User update view"""
    model = User
    form_class = UserUpdateForm
    slug_field = "pk"
    template_name = "user-update.html"

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get_success_url(self):
        messages.success(self.request, _("User succesfully updated"))
        return "/"


class UserDetailView(DetailView):

    """User detail view"""
    model = User
    slug_field = "pk"
    template_name = "user-detail.html"


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class RideRequestCreateView(CreateView):

    """RideRequest create view"""
    model = RideRequest
    form_class = RideRequestCreateForm
    template_name = "riderequest-create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.ride = Ride.objects.get(slug=self.kwargs['ride'])
        self.object.save()
        return super(RideRequestCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("RideRequest succesfully created"))
        return "/"


def login(request):
    login_form = LoginForm()

    redirect_url = reverse('ride-list', args=[])
    redirect_url = request.GET.get('next') or redirect_url

    if request.method == 'POST' and 'login_form' in request.POST:
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            return login_form.login(request, redirect_url=redirect_url)

    return render(request, "login.html", {
        "login_form": login_form,
    })


def register(request):
    signup_form_user = SignUpUserForm(prefix="user", request=request)

    redirect_url = reverse('ride-list', args=[])
    redirect_url = request.GET.get('next') or redirect_url

    if request.method == 'POST' and 'signup_user_form' in request.POST:
        signup_form_user = SignUpUserForm(
            request.POST,
            prefix="user",
            request=request)

        if signup_form_user.is_valid():
            user = signup_form_user.save(request)
            return complete_signup(
                request,
                user,
                EMAIL_VERIFICATION,
                redirect_url)

    return render(request, "register.html", {
        "signup_form_user": signup_form_user,
    })
