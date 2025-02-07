from django.shortcuts import render, redirect, get_object_or_404
from .forms import BreweryForm
from .models import Brewery, dbBrewery
import requests
from bs4 import BeautifulSoup

#The below function renders the home page view
def home(request):
    return render(request, "PortlandBreweries/PortlandBreweries_home.html")

#This function will retrieve the user input from the Brewery form, validate it and add it to
# the database if valid, then re-render the form to the user
def AddBrewery(request):
    form = BreweryForm(request.POST or None)
    if request.method == 'POST':
        if 'Cancel' in request.POST:
            return redirect('PDX_home')
        elif form.is_valid():
            form.save()
            return redirect('PDX_home')
        else:
            print(form.errors)
            form = BreweryForm()
    return render(request, 'PortlandBreweries/AddBrewery.html', {'form': form})

# This function will retrieve all objects in the Brewery model database, and return them
# on the rendered object list, ordered alphabetically by the name of the breweries
def DisplayBreweries(request):
    breweries = Brewery.objects.all().order_by('name')
    return render(request, 'PortlandBreweries/DisplayBreweries.html', {'breweries' : breweries})

#This function will query the database with the user's input, retrieve the objects with  matching
# name and return them on the rendered object list
def SearchResults(request):
    query = request.GET.get('q', '')
    results = Brewery.objects.filter(name__icontains=query)
    return render(request, 'PortlandBreweries/SearchResults.html', {'results': results, 'query': query})

#This function uses the primary key passed from the display templates to retrieve the corresponding
# object and render its fields to the detail template
def DisplayDetails(request, pk):
    brewery = get_object_or_404(Brewery, pk=pk)
    return render(request, 'PortlandBreweries/BreweryDetails.html', {'brewery': brewery})

#This function uses the primary key passed through the DisplayDetails function to retrieve the
# corresponding object and post the updated fields to overwrite it. If the form is valid, the
# user wil then be redirected back to the object's (updated) details page
def EditBrewery(request, pk):
    brewery = get_object_or_404(Brewery, pk=pk)
    if request.method == 'POST':
        if 'Cancel' in request.POST:
            return redirect('PDX_home')
        form = BreweryForm(request.POST, instance=brewery)
        if form.is_valid():
            form.save()
            return redirect('DisplayDetails', pk=pk)
    else:
        form = BreweryForm(instance=brewery)
    return render(request, 'PortlandBreweries/EditBrewery.html', {'form': form, 'brewery': brewery})

#This function uses the primary key passed through the DisplayDetails function to retrieve the
# corresponding object and passes the delete function on that object to the ConfirmDelete template
def DeleteBrewery(request, pk):
    brewery = get_object_or_404(Brewery, pk=pk)
    if request.method == 'POST':
        if 'Cancel' in request.POST:
            return redirect('DisplayDetails', pk=pk)
        else:
            brewery.delete()
        return redirect('DisplayBreweries')
    return render(request, 'PortlandBreweries/ConfirmDelete.html', {'brewery': brewery})

#This function posts the DeleteBrewery function to the database when the user confirms
# (submits the ConfirmDelete template form) and returns the user to the list of breweries
def DeleteConfirmed(request, pk):
    if request.method == 'POST':
        form = BreweryForm(request.POST or None)
        if form.is_valid():
            form.delete()
            return redirect('DisplayBreweries')
    else:
        return redirect('DisplayBreweries')

#This function connects to the Open Brewery DB API and retrieves items from their database filtered for
# breweries located in Portland, Oregon. The response is passed to the dbBreweries class where each
# dictionary (brewery) is instantiated, then each instance is made into an object and rendered to
# the template
def OpenBreweryDB(request):
    response = requests.get("https://api.openbrewerydb.org/v1/breweries?by_state=oregon&by_city=portland")
    brewerydata = response.json()
    breweries = []
    for item in brewerydata:
        brewerylist = dbBrewery(item['name'], item['address_1'], item['website_url'])
        breweries.append(brewerylist)
    return render(request, "PortlandBreweries/OpenBreweryDB.html", {'breweries': breweries})

#This function concatenates the user's input to a string that queries the API by search term. The
# JSON response is handled in the same way as in the OpenBreweryDB function to render the results
# to the template
def DBsearchResults(request):
    input = request.GET.get('q', '')
    query_elements = ["https://api.openbrewerydb.org/v1/breweries/search?query=", input]
    query = "".join(query_elements)
    response = requests.get(query)
    brewerydata = response.json()
    breweries = []
    for item in brewerydata:
        search_results = dbBrewery(item['name'], item['address_1'], item['website_url'])
        breweries.append(search_results)
    return render(request, "PortlandBreweries/OBDBsearchResults.html", {'breweries': breweries, 'input': input})

#This function retrieves the "Portland Beer and Breweries" page on the Travel Portland Website.
# It then uses Beautiful Soup to parse the site's HTML, locate its event grid (upcoming beer
# events). From there it extracts the header and date of each event, turns them into objects
# and renders them to the template
def BeerEvents(request):
    page = requests.get("https://www.travelportland.com/culture/beer/")
    soup = BeautifulSoup(page.text, 'lxml')
    event_cards = soup.find_all("div", class_="tp-card__content")
    events = []
    for event_item in event_cards:
        date_element = event_item.find('div', class_="tp-card__date")
        name_element = event_item.find('h3', class_="tp-card__title")
        date = date_element.text.strip() if date_element else "No date given"
        name = name_element.text.strip() if name_element else "No title given"
        events.append({'date': date, 'name': name})
    return render(request, "PortlandBreweries/BeerEvents.html", {'dictionaries': events})


