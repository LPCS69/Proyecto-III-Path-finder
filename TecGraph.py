import sys
import urllib.request, json
from tkinter import *
from tkinter import ttk
global indice_origen 
global indice_destino
ventana = Tk()
duracion =StringVar()
ruta =StringVar()

"""
___________________________________Interfaz_______________________________
"""



"""
___________________________________Graph Class_______________________________
"""
class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)
        
    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical. In other words,
        if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}
        
        graph.update(init_graph)
        
        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value
                    
        return graph
    
    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes
    
    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    duracion.set("Ruta:  ")
    ruta.set("Duración:  ")
    duracion.set(duracion.get()+"We found the following best path with a value of {}.".format(shortest_path[target_node] + atraso))
    ruta.set(ruta.get()+" -> ".join(reversed(path)))
    print(duracion.get())
    print(ruta.get())
    Ruta.config(text=ruta.get())
    Duracion.config(text=duracion.get())
    

"""
___________________________________Dijkstra Algorithm_______________________________
"""

def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

"""
___________________________________Google Maps API_______________________________
"""

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
    #print(metros[0]['distance']['value'])
    return metros[0]['distance']['value']

"""
___________________________________Matrix Printing_______________________________
"""

def printMatriz(matriz):
    i = 0
    while i < 15:
        print(matriz[i])
        i += 1

"""
___________________________________Main Implementation_______________________________
"""
nodes = [
    "Parque Urbanización Iztarú",
    "Entrada Principal TEC",
    "Centro Investigación Computación",
    "Aulas y Laboratorio de Computo",
    "Biblioteca José Figueres Ferrer",
    "Piscina y Gimnasio TEC",
    "Estación de Servicio Los Ángeles",
    "Zona Deportiva y Canchas",
    "TEC Digital",
    "Edificio F3 Mecatrónica",
    "Lago del TEC",
    "Nuclear and Plasma Science Society",
    "McDonald's",
    "Comedor Estudiantil",
    "Centro de Investigación de Biotecnología",  
]

atraso = 2 #minutos
velocidad = 83.33 #metros/minuto
 
init_graph = {}
for node in nodes:
    init_graph[node] = {}


#Grafo de tiempos asociados
#1. PUI-EPT
PUI_EPT = distancias("9.856707, -83.914954", "9.858114, -83.913348") / velocidad  #minutos
#print(PUI_EPT)
init_graph["Parque Urbanización Iztarú"]["Entrada Principal TEC"] = PUI_EPT

#2. PUI-ALC
PUI_ALC = distancias("9.856707, -83.914954", "9.856030, -83.912605") / velocidad  #minutos
#print(PUI_ALC)
init_graph["Parque Urbanización Iztarú"]["Aulas y Laboratorio de Computo"] = PUI_ALC

#3. ALC-TD
ALC_TD = distancias("9.856030, -83.912605", "9.855707, -83.911784") / velocidad  #minutos
#print(ALC_TD)
init_graph["Aulas y Laboratorio de Computo"]["TEC Digital"] = ALC_TD

#4. EPT-CIC
EPT_CIC = distancias("9.858114, -83.913348", "9.857023, -83.912935") / velocidad  #minutos
#print(EPT_CIC)
init_graph["Entrada Principal TEC"]["Centro Investigación Computación"] = EPT_CIC

#5. CIC-ALC
CIC_ALC = distancias("9.857023, -83.912935", "9.856028, -83.912557") / velocidad  #minutos
#print(CIC_ALC)
init_graph["Centro Investigación Computación"]["Aulas y Laboratorio de Computo"] = CIC_ALC

#6. ALC-BJFF
ALC_BJFF = distancias("9.856028, -83.912557", "9.854893, -83.912642") / velocidad  #minutos
#print(ALC_BJFF)
init_graph["Aulas y Laboratorio de Computo"]["Biblioteca José Figueres Ferrer"] = ALC_BJFF

#7. EPT-PGT
EPT_PGT = distancias("9.858114, -83.913348", "9.856779, -83.910583") / velocidad  #minutos
#print(EPT_PGT)
init_graph["Entrada Principal TEC"]["Piscina y Gimnasio TEC"] = EPT_PGT

#8. PGT-ESLA
PGT_ESLA = distancias("9.856779, -83.910583", "9.857450, -83.904895") / velocidad  #minutos
#print(PGT_ESLA)
init_graph["Piscina y Gimnasio TEC"]["Estación de Servicio Los Ángeles"] = PGT_ESLA

#9. PGT-ZDC
PGT_ZDC = distancias("9.856779, -83.910583", "9.855945, -83.908715") / velocidad  #minutos
#print(PGT_ZDC)
init_graph["Piscina y Gimnasio TEC"]["Zona Deportiva y Canchas"] = PGT_ZDC

#10. PGT-TD
PGT_TD = distancias("9.856779, -83.910583", "9.855707, -83.911784") / velocidad  #minutos
#print(PGT_TD)
init_graph["Piscina y Gimnasio TEC"]["TEC Digital"] = PGT_TD

#11. PGT-F3M
PGT_F3M = distancias("9.856779, -83.910583", "9.854889, -83.909081") / velocidad  #minutos
#print(PGT_F3M)
init_graph["Piscina y Gimnasio TEC"]["Edificio F3 Mecatrónica"] = PGT_F3M

#12. TD-F3M
TD_F3M = distancias("9.856779, -83.910583", "9.854889, -83.909081") / velocidad  #minutos
#print(TD_F3M)
init_graph["TEC Digital"]["Edificio F3 Mecatrónica"] = TD_F3M

#13. BJFF-LT
BJFF_LT = distancias("9.854893, -83.912642", "9.854412, -83.910298") / velocidad  #minutos
#print(BJFF_LT)
init_graph["Biblioteca José Figueres Ferrer"]["Lago del TEC"] = BJFF_LT

#14. F3M-LT
F3M_LT = distancias("9.854889, -83.909081", "9.854412, -83.910298") / velocidad  #minutos
#print(F3M_LT)
init_graph["Edificio F3 Mecatrónica"]["Lago del TEC"] = F3M_LT

#15. LT-NPSS
LT_NPSS = distancias("9.854412, -83.910298", "9.852750, -83.911575") / velocidad  #minutos
#print(LT_NPSS)
init_graph["Lago del TEC"][ "Nuclear and Plasma Science Society"] = LT_NPSS

#16. LT-CIB
LT_CIB = distancias("9.854412, -83.910298", "9.852917, -83.907495") / velocidad  #minutos
#print(LT_CIB)
init_graph["Lago del TEC"]["Centro de Investigación de Biotecnología"] = LT_CIB

#17. F3M-CME
F3M_CME = distancias("9.854889, -83.909081", "9.853733, -83.906980") / velocidad  #minutos
#print(F3M_CME)
init_graph["Edificio F3 Mecatrónica"]["Comedor Estudiantil"] = F3M_CME

#18. CME-CIB
CME_CIB = distancias("9.853733, -83.906980", "9.852917, -83.907495") / velocidad  #minutos
#print(CME_CIB)
init_graph["Comedor Estudiantil"]["Centro de Investigación de Biotecnología"] = CME_CIB

#19. ESLA-McD
ESLA_McD = distancias("9.857450, -83.904895", "9.855717, -83.904419") / velocidad  #minutos
#print(ESLA_McD)
init_graph["Estación de Servicio Los Ángeles"]["McDonald's"] = ESLA_McD

graph = Graph(nodes, init_graph)




def posicion(lista,lugar):
    if lista[0] == lugar:
        return 0
    else:
        return 1+posicion(lista[1:],lugar)
def prueba():
    if combo_origen.get()!= "" and combo_desti.get() != "":
        print("Origen   "+ str(posicion(Lugares,combo_origen.get())))
        print("Destino  "+ str(posicion(Lugares,combo_desti.get())))
        indice_origen  = posicion(Lugares,combo_origen.get())
        indice_destino = posicion(Lugares,combo_desti.get())
        previous_nodes, shortest_path = dijkstra_algorithm(graph = graph,
                                                   start_node = nodes[indice_origen])
        print_result(previous_nodes, shortest_path, start_node = nodes[indice_origen],
             target_node = nodes[indice_destino])
distancias("Zona Deportiva, Provincia de Cartago, Cartago","Canchas Sinteticas ITCR, Provincia de Cartago, Cartago")
ventana.title("TecGraph") 
ventana.minsize(900,600) 
ventana.maxsize(900,600)
canvas = Canvas(ventana , width= 330, height = 310, bg = "#50328B")
imagen = PhotoImage(file = "tecgraph.png")
canvas.create_image(20,10,anchor=NW,image = imagen)
canvas.place(x=515, y=15)
Distancia=Button(ventana, text="Distancia",width=15, height=3, command=prueba)
#|PUI 0  |EPT 1  |CIC 2   |ALC 3  |BJFF 4  |PGT 5  |ESLA 6 |ZDC 7  |TD 8

#|F3M 9  |LT 10  |NPSS 11  |McD 12  |CME 13  |CIB 14
Lugares =[" Parque Urbanización Iztaru", " Entrada Principal TEC",
                        " Centro Investtigación Computación", " Aulas y Labs Computo",
                        " Biblioteca José Figueres Ferrer", " Piscinas y Gimnasio TEC",
                        " Estación Servicio Los Ángeles", " Zona Deportiva y Canchas",
                        " Tec Digital", " F3 Mecatrónica", " Lago del TEC",
                        " Nuclear and Plasma Science Society", " McDonalds",
                        " Comedor Estudiantil"," Centro Investigación Biotecnología"]
combo_origen = ttk.Combobox(ventana)
combo_origen.place(x=125, y=50)
combo_origen.configure(width=30, height=50)
combo_origen["values"] = sorted(Lugares)
combo_desti = ttk.Combobox(ventana)
combo_desti.configure(width=30, height=50)
combo_desti.place(x=125, y=150)
combo_desti["values"] = sorted(Lugares)
Distancia.place(x=20,y=200)
Distancia.configure(width=10, height=2)
Origen = Label(ventana, text="Origen")
Origen.place(x=20, y=50)
Destino = Label(ventana, text="Destino")
Destino.place(x=20, y=150)
ruta.set("Ruta:")
duracion.set("Duracion:")
Ruta = Label(ventana, text=ruta.get())
Ruta.place(x=20, y=350)
Duracion = Label(ventana, text=duracion.get())
Duracion.place(x=20, y=450)
ventana.mainloop()
