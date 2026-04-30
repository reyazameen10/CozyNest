# models.py, this file defines the database models for the project app, including User, Listing, Booking, Review. Each model has fields that correspond to the attributes of the entities they represent, and they are linked together using foreign keys where appropriate.
#Rey Ameen, CS412 


from django.db import models
from django.contrib.auth.models import User

#listing model to represent a property listing
class Listing(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price_per_night = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
#string representation of the listing model, returns the title of the listing
    def __str__(self):
        return self.title

#booking model to represent a booking made by a user for a listing
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.listing}"

#review model to represent a review left by a user for a listing
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.listing}"

#favorite model to represent a user's favorite listings, with a unique constraint to prevent duplicate favorites
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.username} likes {self.listing.title}"

#
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.recipient}"
    
#location model to represent a location where listings can be found, with fields for name, city, and country
class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name
