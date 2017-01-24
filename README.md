# Omaha World-Herald
*Beginning October 2016*

Below are projects I have worked on as a data intern at the Omaha World-Herald.

* [Nebraska Legislature Scraper](#legislative)
* [Douglas County Restaurant Inspections](#inspections)
* [Salaries database](#salaries)
* [Nebraska State Assessment scores](#testscores)

<a name="legislative"></a>
# [Nebraska Legislature](http://dataomaha.com/legislature)

I created a project that scrapes [the Nebraska Legislature website](http://nebraskalegislature.gov) and keeps the data in a MySQL database. The scrapers run every two hours, collecting information about senators, committees and bills.

The data is then presented online in a Django project. Readers can find information on a specific bill, including co-sponsors, recent actions and how senators have voted.

Readers can also find their senator, using a Fusion Table map. 

<a name="inspections"></a>
# [Douglas County Restaurant Inspections](http://dataomaha.com/media/inspections/)

The World-Herald published a map with restaurant inspections for Douglas County last year.

I requested data from the Douglas County Health Department and received a PDF. I converted the data into an Excel file and cleaned it. 

I then created a Fusion Table map based on the ratings restaurants received and updated the website with the new map.

An in-progress manual can be found [here](UpdatingRestaurantInspections.md).

<a name="salaries"></a>
# [Salaries database](http://dataomaha.com/salaries)
The World-Herald keeps a database of Nebraska public employee salaries for public perusal. The website is created using Django.  

I cleaned data provided by the State of Nebraska and added it to the database. I also updated the Django templates to handle special cases present in the State of Nebraska data.

<a name="testscores"></a>
# [Nebraska State Assessment scores](http://dataomaha.com/school-ratings)

Last year, the Nebraska Department of Education released a new set of ratings for public schools named Accountability for a Quality Education System, Today and Tomorrow. Those ratings were collected and published online in a Django website.

This year, the Department of Education released preliminary scores for the Nebraska State Assessment. I cleaned and organized the data, uploaded it to the database and created new templates to show the data.
