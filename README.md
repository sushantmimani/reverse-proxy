## Description
`This is a reverse-proxy service for NextBus.`

## Required Software
`Docker`<br/>
`docker-compose`<br/>
`Python 2.7`

## How to start
`docker-compose up`

## Scaling
`docker-compose up --scale web=<number>`

## Design

The API calls have been segregated into 3 high level groups. <br/>
*       config (/api/v1/config)
        The config endpoint supports 3 commands: agencyList, routeList, routeConfig
            agencyList:  /api/v1/config?command=agencyList
            routeList:   /api/v1/config?command=routeList&a=<agency_tag>
            routeConfig: /api/v1/config?command=routeConfig&a=<agency_tag>, or
                         /api/v1/config?command=routeConfig&a=<agency_tag>&r=<route_tag>
                          
        
*       prediction (/api/v1/prediction)
        The prediction endpoint supports 3 commands: predictions, predictionsForMultiStops and schedule
        predictions: 
        predictionsForMultiStops: /api/v1/prediction?command=predictionsForMultiStops&a=<agency_tag>&stops=<stop_tag>&stops=<stop_tag> (User can specify multiple stops)
        schedule: /api/v1/prediction?command=schedule&a=<agency_tag>&r=<route_tag>
        
*       message (/api/v1/message)
        The message endpoint supports 2 commands: messages and vehicleLocations
        messages: /api/config/message?command=messages&a=<agency_tag>, or
                  /api/config/message?command=messages&a=<agency_tag>&r=<route_a>&r=<route_2> (User can specify multiple routes)
        vehicleLocations: /api/config/message?command=vehicleLocations&a=<agency_tag>&r=<route_tag>&t=<time in epoch>
                  
                  
`The reverse-proxy service is hosted on docker containers and is made scalable with the use of 
docker-compose and a round-robin scheduling algorithm provided by the docker image dockercloud/haproxy.
The load balance is linked to the service in the docker-compose.yml file. There is a databse container
that is also associated with the service. It is used as a common data-store of api requests made 
across all docker containers`

## How to terminate

` docker-compose down -v`
` The -v option is to make sure that all volumes are freed once the service is stopped. 
This helps avoid errors is starting up the mongodb container due to dangling volumes`

## Limitations

In order to prevent some users from being able to download so much data that it would interfere with other users we have imposed restrictions on data usage. These limitations could change at any time. They currently are:
*   Maximum characters per requester for all commands (IP address): 2MB/20sec
*   Maximum routes per "routeConfig" command: 100
*   Maximum stops per route for the "predictionsForMultiStops" command: 150
*   Maximum number of predictions per stop for prediction commands: 5
*   Maximum timespan for "vehicleLocations" command: 5min

