from django.urls import path
from .views import UserList, UserDetail, RegisterView, LoginView, LogoutView

urlpatterns = [
    path('api/', UserList.as_view(), name = "user-list"),
    path('api/<int:pk>', UserDetail.as_view(), name ="user-detail"),
    path('api/register',RegisterView.as_view(),name = "register"),
    path('api/login', LoginView.as_view(), name = "login"),
    path('api/logout',LogoutView.as_view(), name = "logout"),
]
