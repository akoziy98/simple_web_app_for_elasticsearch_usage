# Web application for analysis of authors documents

This web application shows how to work with:
  * Docker
  * [ElasticSearch](https://hub.docker.com/_/elasticsearch)
  * [FastAPI](https://fastapi.tiangolo.com)

There is used toy-example ElasticSearch database: we fill it with random authors, random texts and random creation datetimes. However, despite the simplicity, presented project architecture and docker settings can be used for more complex database examples and FastApi applications.

## Quick start

The easiest way to run this application is to use docker. To do it, you should run the next command at the project folder:

```
docker-compose up -d --build
```

This command runs docker and after about 1 minute you will obtaine working web apllication. This time consists of enviroment setting time and database filling time. 

Wait to the next console message:

```
[+] Running 2/2
 - Container elasticsearch  Started                                                                                0.7s
 - Container web            Started                                                                                21.7s
```

After that wait also about 30s to fill the database with test records. By default, there is 20 different authors and 80 different documents.

## Possible Quick start issues

May be you have already running container with ElasticSearch database. You should stop and remove the containers with ElasticSearch. You can use the next commands.

Search for the ElasticSearch container:

```
docker ps -a
```

You should stop and delete the ElasticSearch container by it's id:

```
docker stop <id>
docker rm <id>
```

## Documentation
  
After you have launched web application, you can find its documentation at the following address: 
  
http://127.0.0.1:8001/docs


## Web application endpoints
  
We have implemented three GET queries in out web application.
  
  ### Hello-world
  
  The simplest test to understand if the application is working or not. You should run the next query:
  
  http://127.0.0.1:8001
  
  If web application works correctly, then query will return: {"message":"Welcome to simple Web application by Andrey Koziy"}
  
  ### Top n authors
  
  First one endpoint get parameter n, and returns top n authors, ranked by the texts number. Parameter n should be less or equal to total authors number, othervise it will return message "Internal Server Error". This value set default to 20. It means, that you can obtain maximum top 20 authors. This query runs as:
  
  http://127.0.0.1:8001/documents/authors/top/10/
  
  This query returns top 10 authors.
  
  Return format is:  {"Tiffany Valenzuela":10,"Delia Whiteford":6,...}
  
  ### Distribution of text creation datetime at last n months
  
  Second one endpoint get parameter n, and returns distribution of datetimes at last n months. It returns sorted datetimes, from the most modern to the oldest. If you try to get distribution of texts creation time at February, with the current date 29, 30 or 31, an error will occur. As example, if now is 2021-11-29, then query with n = 9 will return message "Internal Server Error". This query runs as:
  
  http://127.0.0.1:8001/documents/dates/lastmonths/24/

  This query return distribution of datetimes at last 24 months.
  
  Return format is: ["2021-11-22","2021-11-05",...]


