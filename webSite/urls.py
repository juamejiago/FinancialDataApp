"""
URL configuration for webSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from webApp.views import (
    create_tag,
    delete_tag,
    home,
    tag_ordering,
    update_tag,
    delete_category,
    visualize_category,
    delete_tag_from_category,
    add_tag_to_category,
    transfer_tag_between_categories,
    presentation,
    register,
    login,
    exit,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Login system implementation
    path("accounts/", include("django.contrib.auth.urls")),
    path("", presentation, name="presentation"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", exit, name="logout"),
    path("home/", home, name="home"),
    path("create_tag/", create_tag),
    path("visualize_category/", visualize_category, name="visualize_category"),
    path("delete_tag/", delete_tag),
    path("delete_category/", delete_category),
    path("tag_ordering/", tag_ordering),
    path("update_tag/", update_tag),
    path("delete_tag_from_category/", delete_tag_from_category),
    path("add_tag_to_category/", add_tag_to_category),
    path("transfer_tag_between_categories/", transfer_tag_between_categories),
]
