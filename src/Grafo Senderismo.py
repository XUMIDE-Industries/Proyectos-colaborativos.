# 1.- ---------------- Encabezado ----------------------------------------------
'''
Programa: Ejercicio 5 (Senderismo)
Autor: Rodriguez de Matias Adrian
Fecha: 07/04/2025
Descripción: Aplicación de grafo no dirigido en situaciones diarias.
             Azul: Nodos visitados durante la búsqueda.
             Verde: Nodo de origen.
             Rojo: Nodo de destino.
             Amarillo: Nodos que están en la ruta final más corta.

Modificado por: Politrón Díaz Josué Yered
Fecha de modificación : 18/05/2025
'''
# 2.- ---------------- Importación de Módulos y Bibliotecas --------------------
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from tkinter import scrolledtext
# 3.- ---------------- Definición de Funciones o clases ------------------------
class Nodo:
    def __init__(self, nombre, peso=0):
        self.nombre = nombre
        self.peso = peso
        self.siguiente = None

class ListaAdyacencia:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre, peso):
        nuevo = Nodo(nombre, peso)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def obtener_vecinos(self):
        vecinos = []
        actual = self.cabeza
        while actual:
            vecinos.append((actual.nombre, actual.peso))
            actual = actual.siguiente
        return vecinos

class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, nombre):
        if nombre not in self.vertices:
            self.vertices[nombre] = ListaAdyacencia()

    def agregar_arista(self, origen, destino, peso):
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self.vertices[origen].agregar(destino, peso)
        self.vertices[destino].agregar(origen, peso)

    def obtener_vecinos(self, nombre):
        if nombre in self.vertices:
            return self.vertices[nombre].obtener_vecinos()
        return []

    def bfs_camino_mas_corto(self, inicio, destino):
        visitados = set()
        cola = deque([[inicio]])
        nodos_visitados = []

        while cola:
            camino = cola.popleft()
            nodo = camino[-1]

            if nodo not in visitados:
                visitados.add(nodo)
                nodos_visitados.append(nodo)

                if nodo == destino:
                    return camino, nodos_visitados

                for vecino, _ in self.obtener_vecinos(nodo):
                    nuevo_camino = list(camino + [vecino])
                    cola.append(nuevo_camino)
        return None, nodos_visitados

# 4.- ---------------- Interfaz Gráfica ----------------------------------------
class InterfazGrafo:
    def __init__(self, root):
        self.root = root
        self.root.title("Explorador de Senderos - Grafo BFS")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f4f7")

        self.grafo = Grafo()
        self._inicializar_datos()

        self.origen = None
        self.destino = None

        self._crear_interfaz()

    def _inicializar_datos(self):
        self.grafo.agregar_arista("Cabaña Principal", "Río Claro", 120)
        self.grafo.agregar_arista("Cabaña Principal", "Mirador Norte", 200)
        self.grafo.agregar_arista("Río Claro", "Bosque Encantado", 150)
        self.grafo.agregar_arista("Mirador Norte", "Bosque Encantado", 100)
        self.grafo.agregar_arista("Bosque Encantado", "Cascada Alta", 180)
        self.grafo.agregar_arista("Cascada Alta", "Zona de Camping", 130)
        self.grafo.agregar_arista("Zona de Camping", "Lago Escondido", 110)
        self.grafo.agregar_arista("Mirador Norte", "Zona de Camping", 140)
        self.grafo.agregar_arista("Cabaña Principal", "Lago Escondido", 300)

    def _crear_interfaz(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8, background="#3b8ed0", foreground="white")
        estilo.configure("TLabel", font=("Segoe UI", 11), background="#f0f4f7")
        estilo.configure("TCombobox", font=("Segoe UI", 10))

        frame_izquierdo = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        frame_izquierdo.place(x=20, y=20, width=300, height=660)

        ttk.Label(frame_izquierdo, text="Punto de Origen:").pack(pady=10)
        self.combo_origen = ttk.Combobox(frame_izquierdo, values=list(self.grafo.vertices.keys()), state="readonly")
        self.combo_origen.pack(pady=5)

        ttk.Label(frame_izquierdo, text="Punto de Destino:").pack(pady=10)
        self.combo_destino = ttk.Combobox(frame_izquierdo, values=list(self.grafo.vertices.keys()), state="readonly")
        self.combo_destino.pack(pady=5)

        ttk.Button(frame_izquierdo, text="Mostrar Recorrido BFS", command=self._visualizar_bfs).pack(pady=20)
        ttk.Button(frame_izquierdo, text="Visualizar Todo el Grafo", command=self._visualizar_grafo_completo).pack(pady=5)
        ttk.Button(frame_izquierdo, text="Limpiar Campos", command=self._limpiar_campos).pack(pady=20)
        ttk.Button(frame_izquierdo, text="Acerca De", command=self._mostrar_acerca_de).pack(pady=10)

        ttk.Label(frame_izquierdo, text="Mensajes:").pack(pady=5)
        self.texto_mensajes = scrolledtext.ScrolledText(frame_izquierdo, width=35, height=10, font=("Segoe UI", 9))
        self.texto_mensajes.pack(pady=5)

        self.frame_grafo = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.frame_grafo.place(x=340, y=20, width=640, height=660)

    def _mostrar_mensaje(self, mensaje):
        self.texto_mensajes.insert(tk.END, mensaje + "\n\n")
        self.texto_mensajes.see(tk.END)

    def _limpiar_campos(self):
        self.combo_origen.set("")
        self.combo_destino.set("")
        self.texto_mensajes.delete("1.0", tk.END)
        for widget in self.frame_grafo.winfo_children():
            widget.destroy()

    def _mostrar_acerca_de(self):
        messagebox.showinfo("Acerca De", "Desarrollado por:\nRodriguez de Matias Adrian\nModificado por: Politrón Díaz Josué Yered\nFecha: 18/05/2025")

    def _visualizar_grafo_completo(self):
        self._dibujar_grafo()

    def _visualizar_bfs(self):
        self._limpiar_grafo_visual()
        origen = self.combo_origen.get()
        destino = self.combo_destino.get()
        if not origen or not destino:
            self._mostrar_mensaje("Debes seleccionar un nodo de origen y uno de destino.")
            return

        camino, visitados = self.grafo.bfs_camino_mas_corto(origen, destino)
        if camino:
            self._mostrar_mensaje(f"Camino más corto de {origen} a {destino}:\n{' → '.join(camino)}")
        else:
            self._mostrar_mensaje("No se encontró un camino válido.")
        self._dibujar_grafo(camino, visitados, origen, destino)

    def _limpiar_grafo_visual(self):
        for widget in self.frame_grafo.winfo_children():
            widget.destroy()

    def _dibujar_grafo(self, camino=[], visitados=[], origen=None, destino=None):
        G = nx.Graph()
        for v in self.grafo.vertices:
            for vecino, peso in self.grafo.obtener_vecinos(v):
                if not G.has_edge(v, vecino):
                    G.add_edge(v, vecino, weight=peso)

        pos = nx.spring_layout(G, seed=42)
        colores_nodos = []
        for nodo in G.nodes():
            if nodo == origen:
                colores_nodos.append("green")
            elif nodo == destino:
                colores_nodos.append("red")
            elif nodo in camino:
                colores_nodos.append("yellow")
            elif nodo in visitados:
                colores_nodos.append("skyblue")
            else:
                colores_nodos.append("lightgray")

        fig, ax = plt.subplots(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color=colores_nodos, ax=ax, node_size=1000, font_size=9)
        etiquetas = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, ax=ax)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# 5.- ---------------- Bloque Principal ----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafo(root)
    root.mainloop()
