from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.register),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('tabs/', views.GuitarTabDetailsView.as_view()),
    path('tabs/<int:pk>', views.GuitarTabView.as_view()),
    path('tabs/create/', views.GuitarTabCreate.as_view()),
    path('comments/', views.CommentsView.as_view()),
]
