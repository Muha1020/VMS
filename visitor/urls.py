from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('visitor/', views.register_visitor, name='visitor'),
    path('report/', views.report, name='report'),
    path('checkout/<int:visitor_id>/', views.checkout_visitor, name='checkout_visitor'),
]
