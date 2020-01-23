# Hackathon 2: Team Wonder Woman

![Logo](Images/Logo.png)

In this second project we were appointed by Hypermobility to improve an existing dashboard with more real time data. Here is a brief of the project:

The original architecture::

![Exercise architecture](Images/Diagrama.png)

It received data from only one API of the Ayuntamiento de Valencia Spain, giving status information of all the Valenbisi bicycles located in Valencia, Spain. As follow:

![Kibana Dashboard](Images/KibanaDashboard.png)



First, we look for the Ayuntamiento de Valencia APIS:

![Ayuntamiento de Valencia Logo](Images/ayuntamiento_Valencia.png)

| Name               | API          |
| --------           | -------------- |
| Traffic Status     | http://apigobiernoabiertortod.valencia.es/apirtod/rest/datasets/estado_trafico.json|
| Aparcabicis Loc    | http://gobiernoabierto.valencia.es/es/dataset/?id=aparcabicis|
| Bicycles Count        |http://gobiernoabierto.valencia.es/es/dataset/?id=puntos-medida-trafico-espiras-electromagneticas |
|Car Count      | http://apigobiernoabiertortod.valencia.es/apirtod/rest/datasets/intensidad_trafico.json |

_Traffic Status_: measure every 3 min a linestring UTM zone 30 (Spain) coordinates, related to the following value for specific traffic status:


* 0 Fluido - Fluid
* 1 Denso - Dense
* 2 Congestionado - Congested
* 3 Cortado – Out of line

_Aparcabicis Loc_: Is a complete data set of the location of every parking structure build in the city.

_Bicycles Count_: Is a measure in real time of the number of bicycles that pass through certain point of the city due induction loop traffic detector.

_Cars Count_: Is a measure in real time of the number of Cars that pass through certain point of the city due induction loop traffic detector.


## Now the cherry in the top of the ice cream: 

![Ayuntamiento de Valencia Logo](Images/Twitter_API_Developers.jpg)


Twitter developers APi allows you to create apps that take advantage of integration with Twitter features such as user profiles, tweets, timelines, and search.

Using the filter (“Patinetes”) the dashboard will show in real time the tends that follow the world of patinetes.

# Now we present our MVP:

![NEW](Images/Architecture2.png)

The following exercise will be performance in the follow environment:

* Linux --version (Ubuntu(64bit))
![linux](Images/linux.png)

* elasticsearch --version 7.4.2
* Kibana        --version 7.4.2
* Nifi          --version 1.9.2
* Google Cloud (Pub/Sub)

## To follow this exercise, after creating the needed environment in linux, the first step is downloading the coding to you machines:

Go to the terminal in you virtual machine:

![terminal](Images/terminal.png)

In the terminal, change directory where you want to download the files and type:

```
mkdir New_Project
cd New_Project
git clone https://github.com/luisnose/Data_project2.git
```

