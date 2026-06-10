from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('visitor/', views.register_visitor, name='visitor'),
    path('report/', views.report, name='report'),
    path('checkout/<int:visitor_id>/', views.checkout_visitor, name='checkout_visitor'),
    path('blacklist/', views.blacklist_list, name='blacklist_list'),
    path('blacklist/<int:visitor_id>/', views.blacklist_visitor, name='blacklist_visitor'),
    path('blacklist/remove/<int:entry_id>/', views.remove_blacklist, name='remove_blacklist'),
]
