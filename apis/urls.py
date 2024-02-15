from django.urls import path
from apis.views import *
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('login', LoginView.as_view()),  
    path('products', ProductViews.as_view()),
    path('pendingProducts', PendingProductsViewS.as_view()),
    path('aprove', AproveProductViews.as_view()),
    path('reject', RejectProjectViews.as_view()),
]
