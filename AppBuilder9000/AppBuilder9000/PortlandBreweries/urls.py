#Imports the django path module and the functions from the app's view file to establish url patterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='PDX_home'), #Sets the home page as the default path of the PortlandBreweries app
    path('AddBrewery/', views.AddBrewery, name='AddBrewery'), #Establishes the URl path for the Add Brewery template
    path('Breweries/', views.DisplayBreweries, name='DisplayBreweries'), #Establishes the URl path for the Display Breweries template
    path('Search/', views.SearchResults, name='SearchResults'), #Establishes the URl path for the Search Results template
    path('<int:pk>/Details/', views.DisplayDetails, name='DisplayDetails'), #Establishes the URl path for the Search Results template
    path('<int:pk>/Edit/', views.EditBrewery, name='EditBrewery'), #Establishes the URl path for the edit Brewery template
    path('<int:pk>/Delete/', views.DeleteBrewery, name='DeleteBrewery'), #Establishes the URl path for the edit Brewery function
    path('<int:pk>/ConfirmDelete/', views.DeleteConfirmed, name='DeleteConfirmed'), #Establishes the URl path for the confirm deletion template
    path('BrewersAssociationDB/', views.OpenBreweryDB, name='OpenBreweryDB'), #Establishes the URl path for the OpenBreweryDB template
    path('BrewersAssociationDBSearch/', views.DBsearchResults, name='DBsearchResults'), #Establishes the URl path for the OpenBreweryDB Search Results template
    path('BeerEvents/', views.BeerEvents, name='BeerEvents'), #Establishes the URl path for the Beer Events template
]
