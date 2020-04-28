from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.register),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('tabs/', views.GuitarTabListView.as_view()),
    path('tabs/<int:pk>/', views.guitar_tab),
    path('comments/<int:pk>/', views.comment),
    path('tabs/new/', views.GuitarTabCreate.as_view()),
    path('comments/new/', views.CommentsView.as_view()),
]
