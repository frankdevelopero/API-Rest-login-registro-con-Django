from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from users.viewsets import UserViewSet
from users.viewsets import UserLoginAPIView

# APIRouter
router = DefaultRouter()
router.register('users', UserViewSet, base_name='users')

urlpatterns = [
    url('login/', UserLoginAPIView.as_view(), name='login'),

]

urlpatterns += router.urls
