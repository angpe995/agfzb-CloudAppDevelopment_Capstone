from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout
    path('dealer/<int:id>/review', views.add_review, name='add_review'),
    path(route='', view=views.get_dealerships, name='index'),
    path(route='about', view=views.about, name='about'),
    path('dealer/<int:id>/', views.get_dealer_details, name='dealer_details'),
    path(route ='dealer/<int:id>/add_review', view=views.add_review, name='add_review'),
    path(route='contact', view=views.contact, name='contact'),
    path(route="login", view=views.login_request, name='login'),
    path(route="logout", view=views.logout_request, name='logout'),
    path(route="registration", view = views.registration_request, name = 'registration')

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)