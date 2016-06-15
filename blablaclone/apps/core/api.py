from rest_framework.routers import DefaultRouter
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
)

from core.models import (
    City,
    Ride,
    User,
    RideRequest,
)


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City


class RideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class RideRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = RideRequest


class CityViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        CreateModelMixin,
        GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_fields = ["name", ]


class RideViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        CreateModelMixin,
        GenericViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    filter_fields = [
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


class UserViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        CreateModelMixin,
        GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = [
        "email",
        "name",
        "surname",
        "car",
        "phone",
        "birthdate",
        "about",
        "photo",
    ]

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current':
            kwargs['pk'] = request.user.pk

        return super(UserViewSet, self).dispatch(request, *args, **kwargs)


class RideRequestViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        CreateModelMixin,
        GenericViewSet):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer
    filter_fields = ["user", "ride", "message", ]


router = DefaultRouter()
router.register(r'citys', CityViewSet)
router.register(r'rides', RideViewSet)
router.register(r'users', UserViewSet)
router.register(r'riderequests', RideRequestViewSet)
