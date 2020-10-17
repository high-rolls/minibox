from django.urls import include, path
from rest_framework import routers
from miniboxapi import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'groups', views.GroupViewSet)
router.register(r'phone_numbers', views.PhoneNumberViewSet)
router.register(r'permissions', views.PermissionViewSet)
router.register(r'content_types', views.ContentTypeViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'files', views.FileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('django.contrib.auth.urls')),
]
