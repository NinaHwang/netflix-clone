from django.urls import path

from .views import (
    CheckEmailView,
    SignUpView,
    SignInView,
    ShowProfileImagesView,
    CreateSubUserView,
    SubUserSignInView,
    ManageSubUserView
)

urlpatterns = [
    path('email', CheckEmailView.as_view()),
    path('signup', SignUpView.as_view()),
    path('signin', SignInView.as_view()),
    path('profile/images', ShowProfileImagesView.as_view()),
    path('profile/create', CreateSubUserView.as_view()),
    path('profile/signin', SubUserSignInView.as_view()),
    path('profile/edit', ManageSubUserView.as_view())
]
