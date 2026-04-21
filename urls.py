# This file is used to define the URL patterns for the project app. It maps the URLs to the corresponding views.
# Rey Ameen, CS412

from django.urls import path, reverse_lazy
from .views import ListingListView, ListingDetailView, SignUpView, message_host, toggle_favorite, add_review, create_booking
from django.contrib.auth.views import LoginView, LogoutView
from .views import host_dashboard #new: for host dashboard view

urlpatterns = [
    path('', ListingListView.as_view(), name='listing_list'),
    path('listing/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(
        template_name='project/login.html',
        next_page=reverse_lazy('listing_list')
    ), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('listing_list')), name='logout'),
    path('listing/<int:pk>/review/', add_review, name='add_review'),
    path('listing/<int:pk>/book/', create_booking, name='create_booking'),
    path('listing/<int:pk>/favorite/', toggle_favorite, name='toggle_favorite'),
    path('listing/<int:pk>/message/', message_host, name='message_host'),
    path('host-dashboard/', host_dashboard, name='host_dashboard'),#new: for host dashboard view
]