
"""
Simple Program to help you get started with Google's APIs
"""
import urllib.request, json
def distancias(ori, des):
    origin = ori.replace(' ','+')
    destination = des.replace(' ','+')
    #Google MapsDdirections API endpoint
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyD3NCK3J3vDD6k0hGyYIDmkShjebXmGcX0'
    #Building the URL for the request
    nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
    request = endpoint + nav_request
    #Sends the request and reads the response.
    response = urllib.request.urlopen(request).read()
    #Loads response as JSON
    directions = json.loads(response)
    routes = directions['routes']
    metros = routes[0]['legs']
    return metros[0]['distance']['value']


distancias("Zona Deportiva, Provincia de Cartago, Cartago","Canchas Sinteticas ITCR, Provincia de Cartago, Cartago")
