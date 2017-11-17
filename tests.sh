#!/usr/bin/env bash


curl -G "http://localhost/api/v1/config?command=agencyList"
echo -e "\n----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/stats"
echo -e "\n----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/config?command=routeList"
echo -e "\n----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/config?command=routeList&a=sf-muni"
echo -e "\n----------------------------END OF RESPONSE----------------------------"


curl -G "http://localhost/api/v1/message?command=messages&a=sf-muni"
echo -e "\n----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/message?command=messages&a=SF-muni"
echo -e "\n----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/message?command=messages&a=sf-muni&r=F&r=J"
echo -e "\n----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/message?command=vehicleLocations&a=sf-muni"
echo -e "\n----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/stats"
echo -e "\n----------------------------END OF RESPONSE----------------------------"

curl -G "http://localhost/api/v1/prediction?command=schedule&a=sf-muni&r=N"
echo -e "\n----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/prediction?command=predictionsForMultiStops&a=sf-muni&stops=N|6997&stops=N|3909"
echo -e "\n----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/stats"
echo -e "\n----------------------------END OF RESPONSE----------------------------"

