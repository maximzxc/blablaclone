from django.core.urlresolvers import reverse
from django.utils import formats

from django_webtest import WebTest
from webtest import Upload
from model_mommy import mommy
from allauth.account.models import EmailAddress

from core.models import (
    City,
    Ride,
    User,
    RideRequest,
)


class AuthTestMixin(object):

    def init_users(self):
        # Create User object
        self.user = User.objects.create(email='user@mail.com')
        self.user.set_password('test')
        self.user.save()
        # confirmation - sometimes it's required
        EmailAddress.objects.create(
            user=self.user,
            email='user@mail.com',
            primary=True,
            verified=True
        )

    def login(self, login, password):
        resp = self.app.get(reverse('account_login'))
        form = resp.forms[0]
        form['login'] = login
        form['password'] = password
        form.submit()

    def logout(self):
        resp = self.app.get('/accounts/logout/')


class RideTest(WebTest, AuthTestMixin):

    def test_detail(self):
        """Create Ride in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        ride = mommy.make('core.Ride', _fill_optional=True)
        url = reverse('ride-detail', args=(ride.slug,))

        ride = mommy.make('core.Ride', _fill_optional=True)
        url = reverse('ride-detail', args=(ride.slug,))

        resp = self.app.get(url)
        self.assertContains(resp, ride.from_city)

        self.assertContains(resp, ride.to_city)

        self.assertContains(resp, ride.will_visit)

        self.assertContains(resp, ride.free_places)

        self.assertContains(resp, ride.driver)

        self.assertContains(resp, ride.passangers)

        self.assertContains(resp, ride.price)

        self.assertContains(resp, ride.slug)

        self.assertContains(resp, ride.title)

        ride = mommy.make('core.Ride', _fill_optional=True)
        url = reverse('ride-detail', args=(ride.slug,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, ride.from_city)

        self.assertContains(resp, ride.to_city)

        self.assertContains(resp, ride.will_visit)

        self.assertContains(resp, ride.free_places)

        self.assertContains(resp, ride.driver)

        self.assertContains(resp, ride.passangers)

        self.assertContains(resp, ride.price)

        self.assertContains(resp, ride.slug)

        self.assertContains(resp, ride.title)

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        ride = mommy.make('core.Ride', _fill_optional=True)

        url = reverse('ride-update', kwargs={
            'slug': ride.slug, })

        ride_compare = mommy.make(
            'core.Ride',
            driver=self.anonymoususer,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['from_city'] = ride_compare.from_city.pk
        form['to_city'] = ride_compare.to_city.pk
        form['will_visit'] = ride_compare.will_visit.pk
        form['free_places'] = ride_compare.free_places
        form['driver'] = ride_compare.driver.pk
        form['passangers'] = ride_compare.passangers.pk
        form['price'] = ride_compare.price
        form['title'] = ride_compare.title
        form.submit()

        ride_updated = Ride.objects.get(pk=ride.pk)

        self.assertEqual(
            ride_compare.free_places,
            ride_updated.free_places
        )
        self.assertEqual(
            ride_compare.price,
            ride_updated.price
        )
        self.assertEqual(
            ride_compare.title,
            ride_updated.title
        )

        self.login(self.user.email, 'test')

        ride_compare = mommy.make(
            'core.Ride',
            driver=self.user,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['from_city'] = ride_compare.from_city.pk
        form['to_city'] = ride_compare.to_city.pk
        form['will_visit'] = ride_compare.will_visit.pk
        form['free_places'] = ride_compare.free_places
        form['driver'] = ride_compare.driver.pk
        form['passangers'] = ride_compare.passangers.pk
        form['price'] = ride_compare.price
        form['title'] = ride_compare.title
        form.submit()

        ride_updated = Ride.objects.get(pk=ride.pk)

        self.assertEqual(
            ride_compare.free_places,
            ride_updated.free_places
        )
        self.assertEqual(
            ride_compare.price,
            ride_updated.price
        )
        self.assertEqual(
            ride_compare.title,
            ride_updated.title
        )

        self.logout()

    def test_create(self):
        """Create Ride object using view
        Check database for created object
        """
        self.init_users()

        ride = mommy.make('core.Ride', _fill_optional=True)

        url = reverse('ride-create', kwargs={
        })

        resp = self.app.get(url)

        form = resp.form
        if ride.from_city:
            form['from_city'] = ride.from_city.pk
        if ride.to_city:
            form['to_city'] = ride.to_city.pk
        if ride.will_visit:
            form['will_visit'] = ride.will_visit.pk
        form['free_places'] = ride.free_places
        if ride.driver:
            form['driver'] = ride.driver.pk
        if ride.passangers:
            form['passangers'] = ride.passangers.pk
        form['price'] = ride.price
        form['title'] = ride.title
        form.submit()

        ride_created = Ride.objects.latest('id')

        self.assertEqual(
            ride_created.free_places,
            ride.free_places
        )
        self.assertEqual(
            ride_created.price,
            ride.price
        )
        self.assertEqual(
            ride_created.title,
            ride.title
        )

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        if ride.from_city:
            form['from_city'] = ride.from_city.pk
        if ride.to_city:
            form['to_city'] = ride.to_city.pk
        if ride.will_visit:
            form['will_visit'] = ride.will_visit.pk
        form['free_places'] = ride.free_places
        if ride.driver:
            form['driver'] = ride.driver.pk
        if ride.passangers:
            form['passangers'] = ride.passangers.pk
        form['price'] = ride.price
        form['title'] = ride.title
        form.submit()

        ride_created = Ride.objects.latest('id')

        self.assertEqual(
            ride_created.free_places,
            ride.free_places
        )
        self.assertEqual(
            ride_created.price,
            ride.price
        )
        self.assertEqual(
            ride_created.title,
            ride.title
        )

        self.logout()

    def test_delete(self):
        """Create Ride in database,
        open delete view and
        check that object was removed
        """
        self.init_users()

        ride = mommy.make('core.Ride', _fill_optional=True)
        self.assertEqual(Ride.objects.count(), 1)
        url = reverse('ride-delete', args=(ride.slug,))

        Ride.objects.all().delete()

        ride = mommy.make('core.Ride', _fill_optional=True)
        url = reverse('ride-delete', args=(ride.slug,))

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Ride.objects.count(), 0)

        ride = mommy.make('core.Ride', _fill_optional=True)
        url = reverse('ride-delete', args=(ride.slug,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Ride.objects.count(), 0)

        self.logout()

    def test_list(self):
        """Create list of Ride in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        ride_list = []
        ride = mommy.make('core.Ride', _fill_optional=True)
        ride_list.append(ride)

        url = reverse('ride-list')

        ride_list = []
        ride = mommy.make('core.Ride', _fill_optional=True)
        ride_list.append(ride)

        url = reverse('ride-list')

        url = reverse('ride-list')
        resp = self.app.get(url)

        for ride in ride_list:
            self.assertContains(resp, ride.from_city)
            self.assertContains(resp, ride.to_city)
            pass
            self.assertContains(resp, ride.will_visit)
            self.assertContains(resp, ride.free_places)
            self.assertContains(resp, ride.driver)
            self.assertContains(resp, ride.passangers)
            self.assertContains(resp, ride.price)
            self.assertContains(resp, ride.slug)
            self.assertContains(resp, ride.title)

        ride_list = []
        ride = mommy.make('core.Ride', _fill_optional=True)
        ride_list.append(ride)

        url = reverse('ride-list')

        self.login(self.user.email, 'test')

        url = reverse('ride-list')
        resp = self.app.get(url)

        for ride in ride_list:
            self.assertContains(resp, ride.from_city)
            self.assertContains(resp, ride.to_city)
            pass
            self.assertContains(resp, ride.will_visit)
            self.assertContains(resp, ride.free_places)
            self.assertContains(resp, ride.driver)
            self.assertContains(resp, ride.passangers)
            self.assertContains(resp, ride.price)
            self.assertContains(resp, ride.slug)
            self.assertContains(resp, ride.title)

        self.logout()


class UserTest(WebTest, AuthTestMixin):

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        user = mommy.make('core.User', _fill_optional=True)

        url = reverse('user-update', kwargs={
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        user = self.user
        user_compare = mommy.make('core.User', _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['email'] = user_compare.email
        form['name'] = user_compare.name
        form['surname'] = user_compare.surname
        form['car'] = user_compare.car
        form['phone'] = user_compare.phone
        form['about'] = user_compare.about
        if user.photo:
            form['photo'] = Upload(user_compare.photo.path)
        form.submit()

        user_updated = User.objects.get(pk=user.pk)

        self.assertEqual(
            user_compare.email,
            user_updated.email
        )
        self.assertEqual(
            user_compare.name,
            user_updated.name
        )
        self.assertEqual(
            user_compare.surname,
            user_updated.surname
        )
        self.assertEqual(
            user_compare.car,
            user_updated.car
        )
        self.assertEqual(
            user_compare.phone,
            user_updated.phone
        )
        self.assertEqual(
            user_compare.about,
            user_updated.about
        )
        if user.photo:
            self.assertEqual(
                file(user_compare.photo.path).read(),
                file(user_updated.photo.path).read()
            )

        self.logout()

    def test_detail(self):
        """Create User in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        user = mommy.make('core.User', _fill_optional=True)
        url = reverse('user-detail', args=(user.pk,))

        user = mommy.make('core.User', _fill_optional=True)
        url = reverse('user-detail', args=(user.pk,))

        resp = self.app.get(url)
        self.assertContains(resp, user.email)

        self.assertContains(resp, user.name)

        self.assertContains(resp, user.surname)

        self.assertContains(resp, user.car)

        self.assertContains(resp, user.phone)

        self.assertContains(resp, user.about)

        self.assertContains(resp, user.photo or "")

        user = mommy.make('core.User', _fill_optional=True)
        url = reverse('user-detail', args=(user.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, user.email)

        self.assertContains(resp, user.name)

        self.assertContains(resp, user.surname)

        self.assertContains(resp, user.car)

        self.assertContains(resp, user.phone)

        self.assertContains(resp, user.about)

        self.assertContains(resp, user.photo or "")

        self.logout()


class RideRequestTest(WebTest, AuthTestMixin):

    def test_create(self):
        """Create RideRequest object using view
        Check database for created object
        """
        self.init_users()

        riderequest = mommy.make('core.RideRequest', _fill_optional=True)

        url = reverse('riderequest-create', kwargs={
            'ride': riderequest.ride.pk,
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['message'] = riderequest.message
        form.submit()

        riderequest_created = RideRequest.objects.latest('id')

        self.assertEqual(
            riderequest_created.message,
            riderequest.message
        )

        self.logout()
