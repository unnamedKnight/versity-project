from django.urls import path


from . import views

urlpatterns = [
    path("register/", views.RegisterUser.as_view(), name="register"),
    path("login/", views.CustomAuthToken.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # path("activate/<uidb64>/<token>", views.Activate.as_view(), name="activate"),
]
