from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show_entry, name="entry"),
    path("search/", views.search, name="search"),
    path("create/", views.create_page, name="create_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page")
    
]
