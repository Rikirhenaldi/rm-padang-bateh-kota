from django.urls import path

from . import views_auth, views_dashboard, views_public

urlpatterns = [
    path("", views_public.home, name="home"),
    path("menu/", views_public.menu, name="menu"),
    path("gallery/", views_public.gallery, name="gallery"),
    path("lokasi/", views_public.location, name="location"),
    path("kontak/", views_public.contact, name="contact"),
    path("media/<path:path>", views_public.media, name="media"),
    path("healthz/", views_public.healthz, name="healthz"),
    path("sitemap.xml", views_public.sitemap, name="sitemap"),
    path("robots.txt", views_public.robots, name="robots"),
    path("dashboard/login/", views_auth.login_view, name="dashboard-login"),
    path("dashboard/logout/", views_auth.logout_view, name="dashboard-logout"),
    path("dashboard/", views_dashboard.index, name="dashboard"),
    path("dashboard/restaurant/", views_dashboard.restaurant, name="dashboard-restaurant"),
    path("dashboard/settings/", views_dashboard.settings_view, name="dashboard-settings"),
    path("dashboard/menu/", views_dashboard.menu_list, name="dashboard-menu"),
    path("dashboard/menu/new/", views_dashboard.menu_form, name="dashboard-menu-new"),
    path("dashboard/menu/<str:item_id>/edit/", views_dashboard.menu_form, name="dashboard-menu-edit"),
    path("dashboard/menu/<str:item_id>/delete/", views_dashboard.menu_delete, name="dashboard-menu-delete"),
    path("dashboard/categories/", views_dashboard.category_list, name="dashboard-categories"),
    path("dashboard/categories/new/", views_dashboard.category_form, name="dashboard-category-new"),
    path("dashboard/categories/<str:item_id>/edit/", views_dashboard.category_form, name="dashboard-category-edit"),
    path("dashboard/categories/<str:item_id>/delete/", views_dashboard.category_delete, name="dashboard-category-delete"),
    path("dashboard/gallery/", views_dashboard.gallery_list, name="dashboard-gallery"),
    path("dashboard/gallery/upload/", views_dashboard.gallery_upload, name="dashboard-gallery-upload"),
    path("dashboard/gallery/<str:item_id>/delete/", views_dashboard.gallery_delete, name="dashboard-gallery-delete"),
]
