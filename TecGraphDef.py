import sys
import urllib.request, json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

ventana = Tk()        #Ventana Principal
duracion =StringVar() #Variable tipo string donde se almacena la duracion
ruta =StringVar()     #Variable tipo string donde se almacena la ruta optima

"""
___________________________________Graph Class_______________________________
"""
class Graph(object):

    '''
    Metodo que inicia la clase Graph
    '''
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    '''
    Metodo que construye el grafo mediante la implementacion de diccionarios y lista
    '''
    def construct_graph(self, nodes, init_graph):
        '''
        Se asegura de que el grafo es simetrico. Si existe camino de A a B con un peso definido,
        tiene que haber camino de B a A con el mismo peso        
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
        '''
        Retorna los nodos del grafo
        '''
        return self.nodes
    
    def get_outgoing_edges(self, node):
        '''
        Retorna los nodos que se relacionan con un nodo
        '''
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections
    
    def value(self, node1, node2):
        '''
        Retorna el peso de un nodo a otro
        '''
        return self.graph[node1][node2]

def print_result(previous_nodes, shortest_path, start_node, target_node):
    '''
    Imprime el resultado y asigna a los labels correspondientes la ruta y la duración
    '''
    path = []
    node = target_node
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    path.append(start_node)
    duracion.set("Tiempo estimado de llegada = {}".format(int(shortest_path[target_node]) + int(combo_atraso.get())) + " minutos")
    nodos = "-> \n".join(reversed(path))
    ruta.set(nodos)
    print(duracion.get())
    print(ruta.get())
    Ruta.config(text=ruta.get())
    Duracion.config(text=duracion.get())
    

"""
___________________________________Dijkstra Algorithm_______________________________
"""

def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
    '''
    Utiliza diccionarios para guardar el peso entre nodos y actualizar si encuentra una ruta más corta
    También guarda la secuencia de nodos que se toma por la mejor ruta correspondiente
    '''
    shortest_path = {}
    previous_nodes = {}

    '''
    Se maximiza el peso del grafo en cuestión en un grafo aparte
    '''
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
        
    '''
    Se toma el peso para llegar de un nodo a sí mismo siempre como 0
    '''
    shortest_path[start_node] = 0
    
    '''
    Comienza hasta que se maximicen todos los nodos
    '''
    while unvisited_nodes:
        '''
        Busca el menor peso para llegar a cada nodo
        '''
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        '''
        Actualiza los nodos vecinos con la distancia más baja encontrada correspondientemente
        Analiza en un bucle el camino mas bajo entre las relaciones posibles
        '''
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                '''
                Actualiza la mejor ruta
                '''
                previous_nodes[neighbor] = current_min_node
 
        '''
        Descarta los nodos una vez comparados
        '''
        unvisited_nodes.remove(current_min_node)
    '''
    Finalmente retorna en una tupla los nodos previos junto con la ruta más corta
    desde el nodo de partida, hasta cada uno de los nodos del grafo
    '''
    return previous_nodes, shortest_path

"""
___________________________________Google Maps API_______________________________
"""

'''
Utiliza el API Key de Directions para acceder a las funciones de Google Maps y retornar la distancia
entre nodos esto se genera mediante coordenadas o mediante el nombre detallado del lugar deseado
'''
def distancias(ori, des):
    origin = ori.replace(' ','+')
    destination = des.replace(' ','+')
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyD3NCK3J3vDD6k0hGyYIDmkShjebXmGcX0'
    #Genera el URL para la solicitud
    nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
    request = endpoint + nav_request
    #Solicita y obtiene la respuesta
    response = urllib.request.urlopen(request).read()
    #Carga la respuesta en un JSON
    directions = json.loads(response)
    routes = directions['routes']
    metros = routes[0]['legs']
    return metros[0]['distance']['value']

"""
___________________________________Main Implementation_______________________________
"""

'''
Nodos Principales del Tecnologico de Costa Rica
'''
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
velocidad = 83.33 #Velocidad del caminar de un ser humano (5 km/h -> 83.33 m/min)

'''
Inicialización del grafo y asociación de distancias mediante coordenadas obtenidas del API Directions
'''
init_graph = {}
for node in nodes:
    init_graph[node] = {}
#1. PUI-EPT
PUI_EPT = distancias("9.856707, -83.914954", "9.858114, -83.913348") / velocidad
#print(PUI_EPT)
init_graph["Parque Urbanización Iztarú"]["Entrada Principal TEC"] = PUI_EPT

#2. PUI-ALC
PUI_ALC = distancias("9.856707, -83.914954", "9.856030, -83.912605") / velocidad
#print(PUI_ALC)
init_graph["Parque Urbanización Iztarú"]["Aulas y Laboratorio de Computo"] = PUI_ALC

#3. ALC-TD
ALC_TD = distancias("9.856030, -83.912605", "9.855707, -83.911784") / velocidad
#print(ALC_TD)
init_graph["Aulas y Laboratorio de Computo"]["TEC Digital"] = ALC_TD

#4. EPT-CIC
EPT_CIC = distancias("9.858114, -83.913348", "9.857023, -83.912935") / velocidad 
#print(EPT_CIC)
init_graph["Entrada Principal TEC"]["Centro Investigación Computación"] = EPT_CIC

#5. CIC-ALC
CIC_ALC = distancias("9.857023, -83.912935", "9.856028, -83.912557") / velocidad
#print(CIC_ALC)
init_graph["Centro Investigación Computación"]["Aulas y Laboratorio de Computo"] = CIC_ALC

#6. ALC-BJFF
ALC_BJFF = distancias("9.856028, -83.912557", "9.854893, -83.912642") / velocidad
#print(ALC_BJFF)
init_graph["Aulas y Laboratorio de Computo"]["Biblioteca José Figueres Ferrer"] = ALC_BJFF

#7. EPT-PGT
EPT_PGT = distancias("9.858114, -83.913348", "9.856779, -83.910583") / velocidad
#print(EPT_PGT)
init_graph["Entrada Principal TEC"]["Piscina y Gimnasio TEC"] = EPT_PGT

#8. PGT-ESLA
PGT_ESLA = distancias("9.856779, -83.910583", "9.857450, -83.904895") / velocidad
#print(PGT_ESLA)
init_graph["Piscina y Gimnasio TEC"]["Estación de Servicio Los Ángeles"] = PGT_ESLA

#9. PGT-ZDC
PGT_ZDC = distancias("9.856779, -83.910583", "9.855945, -83.908715") / velocidad
#print(PGT_ZDC)
init_graph["Piscina y Gimnasio TEC"]["Zona Deportiva y Canchas"] = PGT_ZDC

#10. PGT-TD
PGT_TD = distancias("9.856779, -83.910583", "9.855707, -83.911784") / velocidad
#print(PGT_TD)
init_graph["Piscina y Gimnasio TEC"]["TEC Digital"] = PGT_TD

#11. PGT-F3M
PGT_F3M = distancias("9.856779, -83.910583", "9.854889, -83.909081") / velocidad
#print(PGT_F3M)
init_graph["Piscina y Gimnasio TEC"]["Edificio F3 Mecatrónica"] = PGT_F3M

#12. TD-F3M
TD_F3M = distancias("9.856779, -83.910583", "9.854889, -83.909081") / velocidad
#print(TD_F3M)
init_graph["TEC Digital"]["Edificio F3 Mecatrónica"] = TD_F3M

#13. BJFF-LT
BJFF_LT = distancias("9.854893, -83.912642", "9.854412, -83.910298") / velocidad
#print(BJFF_LT)
init_graph["Biblioteca José Figueres Ferrer"]["Lago del TEC"] = BJFF_LT

#14. F3M-LT
F3M_LT = distancias("9.854889, -83.909081", "9.854412, -83.910298") / velocidad
#print(F3M_LT)
init_graph["Edificio F3 Mecatrónica"]["Lago del TEC"] = F3M_LT

#15. LT-NPSS
LT_NPSS = distancias("9.854412, -83.910298", "9.852750, -83.911575") / velocidad
#print(LT_NPSS)
init_graph["Lago del TEC"][ "Nuclear and Plasma Science Society"] = LT_NPSS

#16. LT-CIB
LT_CIB = distancias("9.854412, -83.910298", "9.852917, -83.907495") / velocidad
#print(LT_CIB)
init_graph["Lago del TEC"]["Centro de Investigación de Biotecnología"] = LT_CIB

#17. F3M-CME
F3M_CME = distancias("9.854889, -83.909081", "9.853733, -83.906980") / velocidad
#print(F3M_CME)
init_graph["Edificio F3 Mecatrónica"]["Comedor Estudiantil"] = F3M_CME

#18. CME-CIB
CME_CIB = distancias("9.853733, -83.906980", "9.852917, -83.907495") / velocidad
#print(CME_CIB)
init_graph["Comedor Estudiantil"]["Centro de Investigación de Biotecnología"] = CME_CIB

#19. ESLA-McD
ESLA_McD = distancias("9.857450, -83.904895", "9.855717, -83.904419") / velocidad
#print(ESLA_McD)
init_graph["Estación de Servicio Los Ángeles"]["McDonald's"] = ESLA_McD

graph = Graph(nodes, init_graph)


'''
Conjunto de funciones encargadas de mostrar las cercanías que existen alrededor de los
nodos del grafo, numeros de telefono, horarios y disponibilidad de parqueo
'''
def parrafo(lista): #Rescata la informacion de cada nodo guardada en una matriz
    if lista == []:
        return ""
    else:
        return "- "+lista[0]+"\n"+parrafo(lista[1:])
'''
Obtiene la posición del nodo escogido,
dicha posicion permite buscar en la matriz la informacion de cada nodo
'''
def posicion(lista,lugar): 
    if lista[0] == lugar:
        return 0
    else:
        return 1+posicion(lista[1:],lugar)
def informacion_origen(): #Se encarga de buscar la información para el nodo de partida únicamente
    if combo_origen.get()!= "":
        mensaje = parrafo(Cercanias[posicion(Lugares,combo_origen.get())])
        print(mensaje)
        messagebox.showinfo(message=mensaje, title="Información")
def informacion_destino(): #Se encarga de buscar la información para el nodo de llegada únicamente
    if combo_desti.get()!= "":
        mensaje = parrafo(Cercanias[posicion(Lugares,combo_desti.get())])
        print(mensaje)
        messagebox.showinfo(message=mensaje, title="Información")
'''
Se encarga tanto de llamar a la funcion de calculo de la mejor ruta, como de
llamar a las funciones que obtienen la informacion de los datos del nodo
'''
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

'''
Ventana Principal de la aplicacion
'''
#Ventana Principal de la aplicación
ventana.title("PathFinder") 
ventana.minsize(1800,1000)
ventana.configure(bg="gray75")
ventana.resizable(False, False)

#Canvas encargado de almacenar las imagenes deseadas
canvas = Canvas(ventana , width=1200, height = 950, bg = "white")

#Carga de imagenes de los archivos del computador
imagen = PhotoImage(file = "grafopeso.png")
mapa = PhotoImage(file = "tecmapa.png")
spec1 = PhotoImage(file = "spec1.png")
spec2 = PhotoImage(file = "spec2.png")
image_btn_dist = PhotoImage(file = "btndist.png")
image_btn_info = PhotoImage(file = "btninfo.png")

#Crea las imagenes en el canvas para la aplicacion
canvas.create_image(820, 170, image = imagen)
canvas.create_image(580, 650, image = mapa)
canvas.create_image(325, 180, image = spec1)
canvas.create_image(105, 180, image = spec2)
canvas.place(x=515, y=15)
#|PUI 0  |EPT 1  |CIC 2   |ALC 3  |BJFF 4  |PGT 5  |ESLA 6 |ZDC 7  |TD 8

#|F3M 9  |LT 10  |NPSS 11  |McD 12  |CME 13  |CIB 14

'''
Lista que almacena las opciones de los Combobox de Tkinter
'''
Lugares =[" Parque Urbanización Iztaru", " Entrada Principal TEC",
                        " Centro Investigación Computación", " Aulas y Labs Computo",
                        " Biblioteca José Figueres Ferrer", " Piscinas y Gimnasio TEC",
                        " Estación Servicio Los Ángeles", " Zona Deportiva y Canchas",
                        " Tec Digital", " F3 Mecatrónica", " Lago del TEC",
                        " Nuclear and Plasma Science Society", " McDonalds",
                        " Comedor Estudiantil"," Centro Investigación Biotecnología"]

Atraso = ["0", "2", "5", "7", "10", "15", "20"]


#Matriz de Informacion de cada nodo
Cercanias = [["Horario: abierto las 24 horas","Estudio de ballet Maureen Rivera","Apartamentos Ronald-Escualo","Edificio Parasol"], ##0

             ["Numero telefonico: +50625525333","Estacion de bicicletas","MTB RG Eventos","Super Fresnos"], ##1


             ["Numero telefonico: +50625509160","Abierto de 7:30 AM - 4:30 PM","Recursos Humanos TEC",
              "Vicerrectoría de Vida Estudiantil y Servicios Académicos"],                                   ##2

             
             ["Federación de Estudiantes del Tecnológico de Costa Rica (FEITEC)","Cajero automatico Banco Nacional","Cajero automatico Banco Popular",
              "Cajero automatico Banco de Costa Rica"],                                                      ##3

             ["Soda ASETEC","Centro de Investigación y de Servicios Químicos y Microbiológicos CEQIATEC","Restaurante Institucional",
              "Disponibilidad de parqueo"],                                                                  ##4


             ["Números de teléfono: +50625502763, +50625502563","Restaurante El Ferrocarril",
              "Horario Gimnasio: 4:00 AM  - 10:00 PM | Horario Piscina: 7:30 AM  - 4:30 PM","Disponibilidad de parqueo"], ##5

             ["Número telefónico: +50625914550","Centro Comercial El Pinar","Restaurante Estación 76","Walmart"],     ##6


             ["Plaza de Fútbol TEC","TEC Emprende Lab","Edificios código F","Disponibilidad de parqueo"],  ##7


             ["Horario: 7:00 AM - 4:30 PM","Número telefónico: +50625502069","La Reina del Mundo","Tribunal Institucional Electoral"],  ##8


             ["Escuela de Agronegocios","Laboratorio Institucional de Microscopia","Parada de buses TEC - Cartago","Disponibilidad de parqueo"],  ##9


             ["Soda El Lago","Kinder del TEC (ATIPTEC)","Oficina de Ingeniería del ITCR","Disponibilidad de parqueo"],  ##10

             ["FUNDATEC","Horario: 8:00 AM - 5:00 PM","Número telefónico: +50625509314","Disponibilidad de parqueo"],  ##11


             ["Horario de 9:00 AM - 12:00 AM","Número telefónico: +5069052860101","Tienda de Mascotas Más que Mascotas","Disponibilidad de parqueo"],  ##12


             ["Horario: 7:00 AM  - 7:00 PM","Learning Commons. Sistema de Bibliotecas del TEC","Escuela Ingeniería de Salud Ocupacional",
              "Disponibilidad de parqueo"],  ##13

             
             ["Número telefónico: +50625502479","Escuela Química e Ingeneria Ambiental","Bosques del TEC",
              "Disponibilidad de parqueo"]   ##14
             ] 

#Estilo de todos los Combobox de la aplicación, almacenado en un diccionario
combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'ghost white',
                                       'selectforeground': 'gray10',
                                       'fieldbackground': 'ghost white',
                                       'background': 'SeaGreen1'
                                       }}})
combostyle.theme_use('combostyle')

'''
Objetos generados dentro de la aplicación
'''
#Combobox de nodo de partida
combo_origen = ttk.Combobox(ventana)
combo_origen.place(x=125, y=50)
combo_origen.configure(width=33, height=50)
combo_origen["values"] = sorted(Lugares)
combo_origen["state"] = "readonly"
combo_origen.set(" Entrada Principal TEC")

#Combobox de nodo de llegada
combo_desti = ttk.Combobox(ventana)
combo_desti.configure(width=33, height=50)
combo_desti.place(x=125, y=110)
combo_desti["values"] = sorted(Lugares)
combo_desti["state"] = "readonly"
combo_desti.set(" Centro Investigación Biotecnología")

#Combobox de nodo de posibles atrasos
combo_atraso = ttk.Combobox(ventana)
combo_atraso.place(x=125, y=170)
combo_atraso.configure(width=7, height=50)
combo_atraso["values"] = Atraso
combo_atraso["state"] = "readonly"
combo_atraso.set("0")

#Boton para calcular la mejor ruta con Dijkstra
Distancia=Button(ventana,image=image_btn_dist,command=prueba,bg="gray75")
Distancia.place(x=20,y=210)

#Botones que despliegan la información del nodo correspondiente
Info_Origen=Button(ventana, image=image_btn_info,command=informacion_origen,bg="gray75")
Info_Origen.place(x=350,y=40)
Info_Destino=Button(ventana,image=image_btn_info,command= informacion_destino,bg="gray75")
Info_Destino.place(x=350,y=107)

#Etiquetas utilizadas para guiar al usuario
Origen = Label(ventana, text="Origen",bg="gray75",font=("Comic Sans MS", 16),fg="SeaGreen1")
Origen.place(x=20, y=40)
Destino = Label(ventana, text="Destino",bg="gray75",font=("Comic Sans MS", 16),fg="SeaGreen1")
Destino.place(x=20, y=100)
Atraso = Label(ventana, text="Atraso",bg="gray75",font=("Comic Sans MS", 16),fg="SeaGreen1")
Atraso.place(x=20, y=160)
ruta.set("__________")
duracion.set("__________")
Ruta = Label(ventana, text=ruta.get(),bg="gray75",font=("Comic Sans MS", 16),fg="Black")
Ruta.place(x=120, y=300)
Duracion = Label(ventana, text=duracion.get(),bg="gray75",font=("Comic Sans MS", 16),fg="Black")
Duracion.place(x=120, y=500)
Ruta = Label(ventana, text="Ruta:    ",bg="gray75",font=("Comic Sans MS", 16),fg="SeaGreen1")
Ruta.place(x=20, y=300)
Duracion = Label(ventana, text="Duración:",bg="gray75",font=("Comic Sans MS", 16),fg="SeaGreen1")
Duracion.place(x=20, y=500)

ventana.mainloop()
