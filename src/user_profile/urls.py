from django.urls import path

from . import views
urlpatterns = [
    path('<pk>', views.ProfileDetailView.as_view(), name='profile_detail'),
    # path('create', views.CreateProfile.as_view(), name="create_profile"),
    path('<pk>/update', views.UpdateProfile.as_view(), name="get_profile"),
]