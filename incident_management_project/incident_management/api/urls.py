from django.urls import path
from . import views
from .views import MyTokenObtainPairView, restrictedView,approveIncident
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('restricted/',restrictedView, name='restricted'),
    path('approve/',approveIncident,name='approve-incident')
]