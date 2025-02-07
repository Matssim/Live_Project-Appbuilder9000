from django.db import models

#Creates fixed input alternatives ('Yes' or 'No')
yes_no_choices = (
    ('Yes','Yes'),
    ('No','No'),
)
#Calls the Model module to create a database input form in the class/table "Brewery"
class Brewery(models.Model):
    name = models.CharField(max_length=100, default="", verbose_name="Brewery name", blank=False, null=True) #Required name field
    est_year = models.IntegerField(default="", verbose_name="Established year", blank=True, null=True) #Optional established year field
    main_address =  models.CharField(max_length=500, default="", verbose_name="Brewery Address", blank=False, null=True) #Required address field
    main_visit = models.CharField(max_length=3, choices=yes_no_choices, verbose_name="Open to the public?", blank=False, null=True) #Required yes/no field if address is open to the public
    visit_address =  models.CharField(max_length=500, default="", verbose_name="Brewery Visit Address", blank=True, null=True) #Optional alt. address field
    email = models.EmailField(max_length=200, default="", verbose_name="Brewery Contact Email", blank=True, null=True) #Optional email field
    description = models.TextField(max_length=1000, default="", verbose_name="Tell us about the brewery", blank=True, null=True) #Optional description field

    #Creates a database object from the user input
    objects = models.Manager()

    #Creates a reference for the object using the name input
    def __str__(self):
        return self.name

#Creates a class where each dictionary (brewery) in the JSON response from the Open Brewery DB API
# is turned into an instance, which in turn can be turned to objects and rendered to a template
class dbBrewery:
    def __init__(self, name, address_1, website_url):
        self.name = name
        self.address_1 = address_1
        self.website_url = website_url
