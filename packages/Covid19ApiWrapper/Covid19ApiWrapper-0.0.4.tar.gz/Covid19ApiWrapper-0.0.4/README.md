# Covid 19 API Wrapper

## THE API CREDIT GOES TO [corona.lmao.ninja](https://github.com/NovelCOVID/API), big thanks!
### [Their Discord](https://discordapp.com/invite/EvbMshU)

## Python API Wrapper
Interacts with the API.
Hopefully this saves some people a few steps :)
Enjoy!

## [Fixed] API endpoint changed to "corona.lmao.ninja/v2/"

### UPDATE [...0.0.4] [Fixed]
Until this fix [~0.0.4], functionality was broken due to changes made to the API endpoint sometime today, April 17th, 2020.

All is well and working now :)

*And remember: Social-distancing is key!!*


-------

### Without using "countries" endpoint:

```py

from Covid19ApiWrapper import *

#define the object
x = covidUpdate(BOOL_country_data=False)

print(x.totalCases)
print(x.totalDeaths)
print(x.totalRecovered)
print(x.timeUpdatedUnix)
```
-------

### Using both endpoints:
```py

from Covid19ApiWrapper import *

#define the object
x = covidUpdate(BOOL_country_data=True)

print(x.totalCases)
print(x.totalDeaths)
print(x.totalRecovered)
print(x.timeUpdatedUnix)

#Possible Usage: cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion
print(x.countryData['China']['cases'])
print(x.countryData['China']['todayCases'])

```
-------

### Download/Interact With CDC World Map:
```py

from Covid19ApiWrapper import *

#GET CURRENT CDC GLOBAL INFECTION MAP/LINKS
x = getCdcWorldMap()

print(x.WorldMapLocalFile)
print(x.WorldMapLink)
print(x.WorldMapHtml)

#GET FLAG LINKS/DOWNLOAD FLAG PNG
y = getCountryFlag("USA", download=True)

print(y.flagLink)
print(y.flagLocalFile)
print(y.flagHtml)


```
-------
### Enjoy and be safe!
