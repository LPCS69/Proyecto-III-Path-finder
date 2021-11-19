
"""
Simple Program to help you get started with Google's APIs
"""
from tkinter import *
from tkinter import ttk
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
    print(metros[0]['distance']['value'])
    return metros[0]['distance']['value']
distancias("Zona Deportiva, Provincia de Cartago, Cartago","Canchas Sinteticas ITCR, Provincia de Cartago, Cartago")
ventana = Tk()
ventana.title("TecGraph") 
ventana.minsize(900,600) 
ventana.maxsize(900,600)
canvas = Canvas(ventana , width= 330, height = 310, bg = "#50328B")
imagen = PhotoImage(file = "tecgraph.png")
canvas.create_image(20,10,anchor=NW,image = imagen)
canvas.place(x=515, y=15)
Distancia=Button(ventana, text="Distancia",width=15, height=3, command=distancias("Zona Deportiva, Provincia de Cartago, Cartago"
                                                                      ,"Canchas Sinteticas ITCR, Provincia de Cartago, Cartago"))
com_origen = ttk.Combobox(ventana)
com_origen.place(x=125, y=50)
com_origen.configure(width=30, height=50)
com_origen["values"] = [" Zona Deportiva"]
combo_desti = ttk.Combobox(ventana)
combo_desti.configure(width=30, height=50)
combo_desti.place(x=125, y=150)
combo_desti["values"] = [" Canchas Sinteticas ITCR"]
Distancia.place(x=20,y=200)
Distancia.configure(width=10, height=2)
Origen = Label(ventana, text="Origen")
Origen.place(x=20, y=50)
Destino = Label(ventana, text="Destino")
Destino.place(x=20, y=150)
ventana.mainloop()
