"""AppBuilder9000 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

import TB_Stat_Tracker
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('Journal/', include('Journal.urls')),
    path('DwarfFortGen/', include('DwarfFortGen.urls')),
    path('DeadByDaylight/', include('DeadByDaylight.urls')),
    path('ItemsApp/', include('ItemsApp.urls')),
    path('StatBattler/', include('StatBattler.urls')),
    path('Herbs/', include('Herbs.urls')),
    path('AnimalCrossing/', include('AnimalCrossing.urls')),
    path('AskYourAngels/', include('AskYourAngels.urls')),
    path('Planets/', include('Planets.urls')),
    path('TB_Stat_Tracker/', include('TB_Stat_Tracker.urls')),
    path('CelticsArchive/', include('CelticsArchive.urls')),
    path('NFL/', include('NFL.urls')),
    path('Anime/', include('Anime.urls')),
    path('NewOrleans/', include('NewOrleans.urls')),
    path('NFL2/', include('NFL2.urls')),
    path('GroceryCosts/', include('GroceryCosts.urls')),
    path('AppIdeaArchive/', include('AppIdeaArchive.urls')),
    path('PortlandBreweries/', include('PortlandBreweries.urls')),
]
