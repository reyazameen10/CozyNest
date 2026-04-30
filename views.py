#This file defines the views for the project app. It includes a ListView for displaying all listings and a DetailView for displaying the details of a specific listing.
#Rey Ameen, CS412


from django.http import HttpResponse
from django.db import models
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Listing, Booking, Review, Favorite, Message
from .forms import SignUpForm, BookingForm, ReviewForm, MessageForm, ListingForm


#view for creating a new listing, only accessible to logged-in users, with a form for entering the listing details and saving it to the database

class CreateListingView(CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'project/create_listing.html'
    success_url = reverse_lazy('listing_list')

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)


#view for updating an existing listing, only accessible to the host of the listing, with a form for editing the listing details and saving the changes to the database
class UpdateListingView(UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'project/update_listing.html'
    success_url = reverse_lazy('host_dashboard')

    def dispatch(self, request, *args, **kwargs):
        listing = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        if listing.host != request.user:
            return redirect('host_dashboard')

        return super().dispatch(request, *args, **kwargs)
    

#view for deleting a listing, only accessible to the host of the listing, with a confirmation page and redirecting to the host dashboard after deletion
class DeleteListingView(DeleteView):
    model = Listing
    template_name = 'project/listing_confirm_delete.html'
    success_url = reverse_lazy('host_dashboard')

    def dispatch(self, request, *args, **kwargs):
        listing = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        if listing.host != request.user:
            return redirect('host_dashboard')

        return super().dispatch(request, *args, **kwargs)
    

#view for user registration, with a form for entering the username, email, and password, and logging in the user after successful registration
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'project/signup.html'
    success_url = reverse_lazy('listing_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

#list view for displaying all listings with search and filter functionality
class ListingListView(ListView):
    model = Listing
    template_name = 'project/listing_list.html'
    context_object_name = 'listings'

    def get_queryset(self):
        queryset = Listing.objects.annotate(avg_rating=Avg('reviews__rating'))

        search = self.request.GET.get('search')
        max_price = self.request.GET.get('max_price')
        sort = self.request.GET.get('sort')

        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(location__icontains=search) |
                models.Q(description__icontains=search)
            )

        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)

        if sort == 'low':
            queryset = queryset.order_by('price_per_night')
        elif sort == 'high':
            queryset = queryset.order_by('-price_per_night')
        elif sort == 'rating':
            queryset = queryset.order_by('-avg_rating')

        return queryset


@login_required
def add_review(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.listing = listing
            review.save()
            return redirect('listing_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'project/add_review.html', {'form': form, 'listing': listing})

@login_required
def host_dashboard(request):
    my_listings = Listing.objects.filter(host=request.user)

    bookings = Booking.objects.filter(listing__host=request.user).select_related('user', 'listing')
    messages = Message.objects.filter(recipient=request.user).select_related('sender', 'listing')
    reviews = Review.objects.filter(listing__host=request.user).select_related('user', 'listing')

    context = {
        'my_listings': my_listings,
        'bookings': bookings,
        'messages': messages,
        'reviews': reviews,
    }
    return render(request, 'project/host_dashboard.html', context)


# This will give information about the user's bookings, messages, and reviews related to their listings, allowing them to manage their hosting activities effectively.
@login_required
def my_hub(request):
    bookings = Booking.objects.filter(user=request.user).select_related('listing')

    favorites = Favorite.objects.filter(user=request.user).select_related('listing')

    messages = Message.objects.filter(sender=request.user).select_related('recipient', 'listing')

    reviews = Review.objects.filter(user=request.user).select_related('listing')

    context = {
        'bookings': bookings,
        'favorites': favorites,
        'messages': messages,
        'reviews': reviews,
    }

    return render(request, 'project/my_hub.html', context)


# This view will show the user's bookings, favorites, messages, and reviews related to their activities as a guest, allowing them to manage their travel plans and interactions with hosts effectively.

@login_required
def create_booking(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.listing = listing

            nights = (booking.check_out_date - booking.check_in_date).days
            booking.total_price = nights * listing.price_per_night

            overlap = Booking.objects.filter(
                listing=listing,
                check_in_date__lt=booking.check_out_date,
                check_out_date__gt=booking.check_in_date
            ).exists()

            if overlap:
                return render(request, 'project/booking_error.html', {'listing': listing})

            booking.save()
            return redirect('listing_detail', pk=pk)
    return redirect('listing_detail', pk=pk)

#view for canceling a booking, only accessible to the user who made the booking, with a confirmation page and redirecting to the user hub after cancellation
def cancel_booking(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        booking.delete()
        return redirect('my_hub')

    return redirect('my_hub')

@login_required
def toggle_favorite(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        favorite.delete()
    return redirect('listing_detail', pk=pk)

@login_required
def message_host(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = listing.host
            msg.listing = listing
            msg.save()
    return redirect('listing_detail', pk=pk)



@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)

    if message.sender != request.user and message.recipient != request.user:
        return redirect('my_hub')

    if request.method == 'POST':
        message.delete()

    return redirect('my_hub')

class LocationListView(ListView):
    model = Listing
    template_name = 'project/location_list.html'
    context_object_name = 'locations'

    def get_queryset(self):
        return Listing.objects.values('location').distinct()

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'project/listing_detail.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        listing = self.object

        context['avg_rating'] = listing.reviews.aggregate(avg=Avg('rating'))['avg']
        context['similar_listings'] = Listing.objects.filter(
            location=listing.location
        ).exclude(pk=listing.pk)[:3]

        context['booking_form'] = BookingForm()
        context['message_form'] = MessageForm()

        return context
    
