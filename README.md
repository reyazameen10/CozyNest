# CozyNest

A full-stack Airbnb-inspired vacation rental platform where travelers can discover and book unique cozy stays, and hosts can manage their properties and guests built with Django using class-based views, Django ORM, and full CRUD operations.

## Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## Features

### Guest Experince 
- Brows and discover vacation rental listing with real photos and pricing
- View deatiled listing pages with location, price, reviews, and similar properties
- Save listing to a personal favorites collection
- Leave reviews on completed stays
- Message hosts directly from a listing page
 

### Host Dashboard
- Dedicated host dashboard to manage all property listing
- Add, update, and delete listing with image uploads
- View all reservations, guest messages, and review per listing
- See total booking prices and guest details at a glance


## Technical Highlights
- Built with Django class-based views including `ListView`, `DetailView`, `CreateView`, `UpdateView`, and `DeleteView`
- Authentication and access control using `LoginRequiredMixin`
- Custom `get_context_data()`, `get_object()`, and `form_valid()` methods
- Complex Django ORM queries with filtering, comparison, and aggregate operations
- Form validation across multiple combined forms
- Clean URL routing with proper slug usage
- Realistic model data with images across all listings
- Inline comments and file headers across all files

## Demo
Watch the full project walkthrough: https://youtu.be/3w3t9iaiCPo

## Run Locally
```bash
git clone https://github.com/reyazameen10/CozyNest
cd CozyNest
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
