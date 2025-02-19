# Live Project - Appbuilder9000

In this project I developed a web application in the Django framework, compatible with an existing parent structure. My app is an unofficial database and information site for breweries in Portland, Oregon. During my sprint, through several stories, I accomplished 3 main objectives. 

* [Build a local database with Create-Read-Update-Delete (CRUD) functionality](#basic-app-model-and-crud-pages)
* [Integrate an external database API](#external-database-api)
* [Integrate a web scraper to display regularly updated information from another website](#displaying-web-scraped-data)


## Basic app, model and CRUD pages 
Jump to: [Page Top](#live-project---appbuilder9000) | [External database API](#external-database-api) | [Displaying web scraped data](#displaying-web-scraped-data)

Once I’d set up the PortlandBreweries app, it’s basic Model-View-Template (MVT) structure and linked it to the AppBuilder9000 main app I built the Brewery <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/models.py">model</a> and <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/forms.py">form</a> for the local database. The model tracks 7 properties, 3 required and 4 optional. In order to register a brewery in the database, the user will have to provide its name, main address and whether that address is open to the public. That last property is a function to capture a common practice for breweries in Portland to sell their product onsite, due to the state’s tax regulations. The user is therefore prompted to specify whether the main address is their visit location and they can enter the optional property of a visit address, if it’s different from the main address. They’re also given the option to provide the brewery’s email address, year of establishment and a short description. 

Brewery model:

    yes_no_choices = (
        ('Yes','Yes'),
        ('No','No'),
    )
    
    class Brewery(models.Model):
        name = models.CharField(max_length=100, default="", verbose_name="Brewery name", blank=False, null=True)
        est_year = models.IntegerField(default="", verbose_name="Established year", blank=True, null=True)
        main_address =  models.CharField(max_length=500, default="", verbose_name="Brewery Address", blank=False, null=True)
        main_visit = models.CharField(max_length=3, choices=yes_no_choices, verbose_name="Open to the public?", blank=False, null=True)
        visit_address =  models.CharField(max_length=500, default="", verbose_name="Brewery Visit Address", blank=True, null=True)
        email = models.EmailField(max_length=200, default="", verbose_name="Brewery Contact Email", blank=True, null=True)
        description = models.TextField(max_length=1000, default="", verbose_name="Tell us about the brewery", blank=True, null=True)
    
    
        objects = models.Manager()
    
    
        def __str__(self):
            return self.name 

Brewery form:

    class BreweryForm(ModelForm):
        class Meta:
            model = Brewery
            fields = '__all__'

The <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/templates/PortlandBreweries_base.html">base template</a> loads in Bootstrap, external fonts and static files, namely my custom <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/static/css/PortlandBreweries_style.css">CSS</a> and <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/static/js/PortlandBreweries_script.js">JavaScript</a>. Additionally, it calls in the navbar and footer templates to make sure all these elements render on each view. 

```html
{% load static %}
{% load django_bootstrap5 %}

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{% block title %}Portland Breweries{% endblock %}</title>
        <link rel="stylesheet" type="text/css" href="{% static 'css/PortlandBreweries_style.css' %}">
        <link href="https://fonts.googleapis.com/css2?family=Asul:wght@400;700&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Red+Rose&display=swap"
              rel="stylesheet">}
    </head>

    <body>
        {% bootstrap_css %}
        {% include "PortlandBreweries_navbar.html" %}
        <header class="header_title">
            {% block header %}{% endblock %}
        </header>
        {% block content %}{% endblock %}
        {% include "PortlandBreweries_footer.html" %}
        {% bootstrap_javascript %}
        <script src="{% static 'js/PortlandBreweries_script.js' %}"></script>
    </body>
</html>
```

The app has views and templates for the home page, and for the user to <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/templates/PortlandBreweries/AddBrewery.html">Add</a>, <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/templates/PortlandBreweries/BreweryDetails.html">Display</a>, <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/templates/PortlandBreweries/EditBrewery.html">Edit</a> and <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/templates/PortlandBreweries/ConfirmDelete.html">Delete</a> entries.  

    def home(request):
        return render(request, "PortlandBreweries/PortlandBreweries_home.html")
    
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
    
    def DisplayBreweries(request):
        breweries = Brewery.objects.all().order_by('name')
        return render(request, 'PortlandBreweries/DisplayBreweries.html', {'breweries' : breweries})
    
    def DisplayDetails(request, pk):
        brewery = get_object_or_404(Brewery, pk=pk)
        return render(request, 'PortlandBreweries/BreweryDetails.html', {'brewery': brewery})
    
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
    
    def DeleteBrewery(request, pk):
        brewery = get_object_or_404(Brewery, pk=pk)
        if request.method == 'POST':
            if 'Cancel' in request.POST:
                return redirect('DisplayDetails', pk=pk)
            else:
                brewery.delete()
            return redirect('DisplayBreweries')
        return render(request, 'PortlandBreweries/ConfirmDelete.html', {'brewery': brewery})
    
    def DeleteConfirmed(request, pk):
        if request.method == 'POST':
            form = BreweryForm(request.POST or None)
            if form.is_valid():
                form.delete()
                return redirect('DisplayBreweries')
        else:
            return redirect('DisplayBreweries')
 

I also created views/templates that allows the users to <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/templates/PortlandBreweries/SearchResults.html">search</a> for entries in the database and have them display 

    def SearchResults(request):
        query = request.GET.get('q', '')
        results = Brewery.objects.filter(name__icontains=query)
        return render(request, 'PortlandBreweries/SearchResults.html', {'results': results, 'query': query})

![CRUD DEMO](https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/PresentationMaterials/CRUDdemo-ezgif.com-video-to-gif-converter.gif) 


## External database API 
Jump to: [Page Top](#live-project---appbuilder9000) | [Basic app, model and CRUD pages](#basic-app-model-and-crud-pages) | [Displaying web scraped data](#displaying-web-scraped-data)

In addition to the database that the user can contribute to, I plugged in an API from the <a href="https://www.openbrewerydb.org/">Open Brewery Database</a> for the user to cross-reference against. This database is periodically updated with information from the <a href="https://www.brewersassociation.org/">Brewers Association’s</a> database. For the <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/templates/PortlandBreweries/OpenBreweryDB.html">basic view</a>, I used a URL for the API that filters for breweries located in Portland, Oregon, to create a more lightweight JSON response and keep the load time relatively quick. The JSON response is then parsed and each object is instantiated and rendered to the template.  

    def OpenBreweryDB(request):
        response = requests.get("https://api.openbrewerydb.org/v1/breweries?by_state=oregon&by_city=portland")
        brewerydata = response.json()
        breweries = []
        for item in brewerydata:
            brewerylist = dbBrewery(item['name'], item['address_1'], item['website_url'])
            breweries.append(brewerylist)
        return render(request, "PortlandBreweries/OpenBreweryDB.html", {'breweries': breweries})

I then included a search bar letting the user to input a query, which is concatenated to a separate JSON request that queries the full database based on that input and returns a commensurate response, rendered to a separate <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/templates/PortlandBreweries/OBDBsearchResults.html">search result view</a>. 

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
 
![API DEMO](https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/PresentationMaterials/APIdemo-ezgif.com-video-to-gif-converter.gif) 


## Displaying web scraped data 
Jump to: [Page Top](#live-project---appbuilder9000) | [Basic app, model and CRUD pages](#basic-app-model-and-crud-pages) | [External database API](#external-database-api) 

In addition to the databases I included a regularly updated view to display upcoming beer events (festivals etc.). In order to automate this, I used the Beautiful Soup package to parse the <a href="https://www.travelportland.com/culture/beer/">TravelPortland website’s beer and breweries page</a>, for the elements that displays upcoming beer events. The event name and date/dates are the scraped, instantiated as objects and rendered to a <a href="https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/AppBuilder9000/AppBuilder9000/PortlandBreweries/templates/PortlandBreweries/BeerEvents.html">template</a>. 

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
 

![WEB SCRAPE DEMO](https://github.com/Matssim/Live_Project-Appbuilder9000/blob/main/PresentationMaterials/WebScrapeDemo-ezgif.com-video-to-gif-converter.gif) 

Jump to: [Page Top](#live-project---appbuilder9000) | [Basic app, model and CRUD pages](#basic-app-model-and-crud-pages) | [External database API](#external-database-api) | [Displaying web scraped data](#displaying-web-scraped-data)
