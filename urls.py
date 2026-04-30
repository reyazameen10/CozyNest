# This file is used to define the URL patterns for the project app. It maps the URLs to the corresponding views.
# Rey Ameen, CS412

from django.urls import path, reverse_lazy

from . import views
from .views import ListingListView, ListingDetailView, SignUpView, message_host, my_hub, toggle_favorite, add_review, create_booking, CreateListingView, UpdateListingView, DeleteListingView, cancel_booking, delete_message   
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
    path('listing/new/', CreateListingView.as_view(), name='create_listing'), #new: for creating a new listing
    path('my-hub/', my_hub, name='my_hub'), #new: for user hub view
    path('listing/<int:pk>/edit/', UpdateListingView.as_view(), name='update_listing'),
    path('listing/<int:pk>/delete/', DeleteListingView.as_view(), name='delete_listing'),
    path('booking/<int:pk>/cancel/', cancel_booking, name='cancel_booking'),
    path('message/<int:pk>/delete/', delete_message, name='delete_message'), #just out of curiosity, I added this URL pattern for deleting messages, which is a feature I implemented in the views.py file but forgot to add the URL pattern for it.
]