from django.urls import path

from main_app import views

app_name = "main_app"

urlpatterns = [
    path("", views.home, name="home"),
    path("car", views.ListCar.as_view(), name="car_list"),
    path("car/create", views.CreateCar.as_view(), name="car_create"),
    path("car/edit/<int:pk>", views.UpdateCar.as_view(), name="car_update"),
    path("car/delete/<int:pk>", views.DeleteCar.as_view(), name="car_delete"),
    path("manufacturer", views.ListManufacturer.as_view(), name="manufacturer_list"),
    path(
        "manufacturer/create",
        views.CreateManufacturer.as_view(),
        name="manufacturer_create",
    ),
    path(
        "manufacturer/edit/<int:pk>",
        views.UpdateManufacturer.as_view(),
        name="manufacturer_update",
    ),
    path(
        "manufacturer/delete/<int:pk>",
        views.DeleteManufacturer.as_view(),
        name="manufacturer_delete",
    ),
]
