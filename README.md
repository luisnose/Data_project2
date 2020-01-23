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

We are going to use already provided ElasticStreaming Virtual Machine, but we need to configure it with a minimum of  6GB of RAM. 

* Start virtual machine and logon. 

Go to the terminal in you virtual machine:

![terminal](Images/terminal.png)

In the terminal, change directory where you want to download the files and type:

```
mkdir New_Project
cd New_Project
git clone https://github.com/luisnose/Data_project2.git
```

We are  going to use already provided ElasticStreaming Virtual Machine, but we need to configure it to use 6GB of RAM. 

* Start virtual machine and logon. 

* Open Web Browser and go to  http://console.cloud.google.com/

* Create a new project called hackathon and move to it. 
<img src="./Images/CreateProject.png" width="75%"><br/>

* Go to pub/sub on left panel and create topic calling it valenbisi.
<img src="./Images/CreateTopic.png" width="50%"><br/>

* Click to the topic already created go down and click on Create Subscription called streaming, left rest as default:
<img src="./Images/CreateSubscription1.png" width="75%">
<br/>
<img src="./Images/CreateSubscription2.png" width="75%">

* Donwload key to be able to consume and populate messages to pub/sub. 
	* Go to left panel to IAM & admin --> Service accounts
	* Click on Create Service  Account
	* Create service account called streaming, and click on Continue:<br/>
	<img src="./Images/CreateKey.png" width="75%"><br/>
	
	* Add permissions to pub/sub read and consume, and click Continue:<br/>
	<img src="./Images/CreateKey2.png" width="75%"><br/>
	
	* Click on Create key, select JSON as key type and finally on Done. That will download a Json file with your credentials:<br/>
	<img src="./Images/CreateKey3.png" width="50%"><br/>
	
	
* Enable pub/sub API
	* Going to API & Services on left panel 
	* Click on Enable Apis & Services
	* Look for Pub/Sub and enable it. 

* Open a terminal and move the json key downloaded to Crendentials folder. Run the following:


```
cp Downloads/your_downloaded_credentials.json Credentials/mobilityApp.json
```  
**Carefull** \
_your_downloaded_credentials.json_ -> replace with the downloaded file name from google cloud, it must be in the Download directory.

* Edit /home/edem/bash.rc file commenting previous crendentials and adding this one as google application credentials:
```
#export GOOGLE_APPLICATION_CREDENTIALS=/home/edem/Credentials/iexCloudApp.json
export GOOGLE_APPLICATION_CREDENTIALS=/home/edem/Credentials/mobilityApp.json
```
**Carefull** \
mobilityApp.json_ -> s the name of the credential that will require NIFI


## For Apache Beam in python we will be using the following libraries, so its time to install them:
* Run the following in the terminal:
```
pip install elasticsearch
pip install ast
pip install utm
```

__ast__ library is need it in this exercise to eval a string and converted it into a list or a dictionary types.\
__utm__ library is going to convert the utm coordinates to the lat and long coordinates


## Run the platform

* Launch elasticsearch:
	* Open a terminal and run the following
	```
	Software/elasticsearch-7.4.2/bin/elasticsearch
	```  

* Launch kibana:
```
Software/kibana-7.4.2-linux-x86_64/bin/kibana
```  

* Open web browser to validate that kibana has been launched successfully --> http://localhost:5601

* Go to Dev Tools on left pannel and create a mapping for location geo point. 
```
PUT valenbisi
{
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_point"
      }
    }
  }
}
```

* Setup the Dashboards. Go to Management / Kibana (saved objects) / Import 
```
/home/edem/.../kibana/export.ndjson
```  
