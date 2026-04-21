#This file is used to register the models in the admin site so that we can manage them through the Django admin interface.
#Rey Ameen, CS412

from django.contrib import admin
from .models import Listing, Booking, Review, Favorite, Message

admin.site.register(Listing)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Message)