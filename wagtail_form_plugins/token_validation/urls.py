from django.urls import path

from .views import TokenValidationView


urlpatterns = [
    path(
        "submissions/<int:submission_id>/validate/<str:token>/",
        TokenValidationView.as_view(),
        name="validate_submission",
    ),
]
