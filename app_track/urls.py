from django.urls import path
from app_track.views import (
    add_app_view,
    edit_app_view,
    details_app_view,
    delete_app_view,
    install_app_view,
    uninstall_app_view,
    get_subcategories,
)

urlpatterns = [
    path('add_app/',add_app_view,name='add-app'),
    path('edit_app/<int:id>',edit_app_view,name='edit-app'),
    path('delete_app/',delete_app_view,name='delete-app'),
    path('details_app/<int:id>',details_app_view,name='details-app'),
    path('install_app/<int:id>',install_app_view,name='install-app'),
    path('uninstall_app_user/',uninstall_app_view,name='uninstall-app'),
    path('get_subcategories/', get_subcategories, name='get_subcategories'),
]