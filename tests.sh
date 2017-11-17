#!/usr/bin/env bash


curl -G "http://localhost/api/v1/config?command=agencyList"
echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/stats"
echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/config?command=routeList"
echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/config?command=routeList&a=sf-muni"
echo "----------------------------END OF RESPONSE----------------------------"



echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/message?command=messages&a=sf-muni"
echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/message?command=messages&a=SF-muni"
echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/message?command=messages&a=sf-muni&r=F&r=J"
echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/message?command=vehicleLocations&a=sf-muni"
echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/stats"
echo "----------------------------END OF RESPONSE----------------------------"

curl -G "http://localhost/api/v1/prediction?command=schedule&a=sf-muni&r=N"
echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/prediction?command=predictionsForMultiStops&a=sf-muni&stops=N|6997&stops=N|3909"
echo "----------------------------END OF RESPONSE----------------------------"
curl -G "http://localhost/api/v1/stats"
echo "----------------------------END OF RESPONSE----------------------------"

