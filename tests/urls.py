from rest_framework import routers

from tests.views import ExtraViewSet, FirstViewSet, SecondViewSet, ThirdViewSet


router = routers.SimpleRouter()

router.register('extras', ExtraViewSet)
router.register('firsts', FirstViewSet)
router.register('seconds', SecondViewSet)
router.register('thirds', ThirdViewSet)

urlpatterns = router.urls
