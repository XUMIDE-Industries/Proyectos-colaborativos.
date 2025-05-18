# 1. ---------------- Encabezado -----------------------------------
'''
Programa: Conexiones de Vuelos entre Aeropuertos (Grafo Dirigido con BFS)
Autores: Politrón Díaz Josué Yered, Pacheco Cedillo Jorge Anuar, Robles Cedillo Irving Xnuviko y Flores Duarte Ana Yuritzy
Fecha: 06/05/2025
Descripción: Este programa representa una red de aeropuertos mediante un grafo dirigido.
Cada aeropuerto es un nodo y cada vuelo directo es una arista dirigida. Se utiliza una lista
doblemente enlazada para gestionar las conexiones. Incluye una función de búsqueda en anchura
(BFS) que recorre los aeropuertos desde un origen, mostrando gráficamente el recorrido paso a paso.
'''
# 2. ---------------- Importación de Módulos y Bibliotecas ---------------------
import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 3. ---------------- Definición de Funciones o Clases -------------------------
class Aeropuerto:
    def __init__(self, codigo, nombre, pais, zona_horaria):
        self._codigo = codigo
        self._nombre = nombre
        self._pais = pais
        self._zona_horaria = zona_horaria

class Nodo:
    def __init__(self, dato):
        self._dato = dato
        self._anterior = None
        self._siguiente = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self._inicio = None
        self._fin = None
    def agregar(self, dato):
        nuevoNodo = Nodo(dato)
        if not self._inicio:
            self._inicio = self._fin = nuevoNodo
        else:
            self._fin._siguiente = nuevoNodo
            nuevoNodo._anterior = self._fin
            self._fin = nuevoNodo
    def eliminar(self, dato):
        actual = self._inicio
        while actual:
            if actual._dato == dato:
                if actual._anterior:
                    actual._anterior._siguiente = actual._siguiente
                else:
                    self._inicio = actual._siguiente
                if actual._siguiente:
                    actual._siguiente._anterior = actual._anterior
                else:
                    self._fin = actual._anterior
                return
            actual = actual._siguiente
    def contiene(self, dato):
        actual = self._inicio
        while actual:
            if actual._dato == dato:
                return True
            actual = actual._siguiente
        return False
    def mostrar(self):
        elementos = []
        actual = self._inicio
        while actual:
            elementos.append(actual._dato)
            actual = actual._siguiente
        return elementos

class GrafoDeVuelos:
    def __init__(self):
        self._aeropuertos = {}
        self._conexiones = {}
    def agregar_aeropuerto(self, codigo, nombre, pais, zona_horaria):
        if codigo not in self._aeropuertos:
            self._aeropuertos[codigo] = Aeropuerto(codigo, nombre, pais, zona_horaria)
            self._conexiones[codigo] = ListaDoblementeEnlazada()
    def agregar_vuelo(self, origen, destino):
        if origen == destino:
            raise ValueError("No se permiten vuelos desde y hacia el mismo aeropuerto")
        if origen not in self._aeropuertos or destino not in self._aeropuertos:
            raise ValueError("Ambos aeropuertos deben estar registrados")
        if not self._conexiones[origen].contiene(destino):
            self._conexiones[origen].agregar(destino)
    def eliminar_vuelo(self, origen, destino):
        if origen in self._conexiones:
            self._conexiones[origen].eliminar(destino)
    def eliminar_aeropuerto(self, codigo):
        if codigo in self._aeropuertos:
            del self._aeropuertos[codigo]
            del self._conexiones[codigo]
        for conexiones in self._conexiones.values():
            conexiones.eliminar(codigo)
    def mostrar_red(self):
        return {
            origen: destinos.mostrar()
            for origen, destinos in self._conexiones.items()
        }
    def _construir_networkx(self):
        G = nx.DiGraph()
        for codigo in self._aeropuertos:
            G.add_node(codigo)
        for origen, lista in self._conexiones.items():
            for destino in lista.mostrar():
                G.add_edge(origen, destino)
        return G
    def visualizar_red_embebida(self, frame):
        G = self._construir_networkx()
        etiquetas = {
            codigo: f"{a._codigo}\n{a._pais}\n{a._zona_horaria}"
            for codigo, a in self._aeropuertos.items()
        }
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.clear()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=ax, with_labels=True, labels=etiquetas,
                node_color='plum', edge_color='black', node_size=4000,
                font_size=8, arrows=True, font_weight='bold')
        ax.set_title("Red de Vuelos Internacionales", fontsize=10)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    def bfs_embebido(self, inicio, frame):
        if inicio not in self._aeropuertos:
            messagebox.showerror("Error", f"No existe el aeropuerto {inicio}")
            return
        G = self._construir_networkx()
        visitados = set()
        cola = deque([inicio])
        pos = nx.spring_layout(G)
        fig, ax = plt.subplots(figsize=(8, 6))
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        while cola:
            actual = cola.popleft()
            if actual not in visitados:
                visitados.add(actual)
                ax.clear()
                colores = []
                for nodo in G.nodes:
                    if nodo == actual:
                        colores.append('red')
                    elif nodo in visitados:
                        colores.append('lightgreen')
                    else:
                        colores.append('lightgray')
                nx.draw(G, pos, ax=ax, with_labels=True,
                        node_color=colores, edge_color='black',
                        node_size=4000, font_size=10, arrows=True)
                ax.set_title(f"Visitando: {actual}")
                canvas.draw()
                frame.update()
                frame.after(1000)
                vecinos = self._conexiones[actual].mostrar()
                for v in vecinos:
                    if v not in visitados:
                        cola.append(v)

# 4. ---------------- Interfaz Gráfica -----------------------------------
class InterfazApp:
    def __init__(self, root):
        self.red = GrafoDeVuelos()
        self.root = root
        self.root.title("Red de Vuelos entre Aeropuertos")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#f2f2f2")

        self.frame_izq = tk.Frame(root, bg="#e6f0ff", padx=10, pady=10)
        self.frame_izq.pack(side="left", fill="y")

        self.frame_der = tk.Frame(root, bg="#ffffff", relief="sunken", bd=2)
        self.frame_der.pack(side="right", expand=True, fill="both")

        self._crear_widgets()

    def _crear_widgets(self):
        estilo_titulo = {"font": ("Helvetica", 14, "bold"), "background": "#e6f0ff", "anchor": "center"}
        estilo_entrada = {"font": ("Helvetica", 10), "width": 25}
        estilo_boton = {"font": ("Helvetica", 10, "bold"), "bg": "#0066cc", "fg": "white", "activebackground": "#005bb5"}

        # Sección Aeropuertos
        tk.Label(self.frame_izq, text="Registro de Aeropuerto", **estilo_titulo).pack(pady=(0, 10))

        tk.Label(self.frame_izq, text="Código IATA").pack()
        self.cod_entry = tk.Entry(self.frame_izq, **estilo_entrada)
        self.cod_entry.pack(pady=2)

        tk.Label(self.frame_izq, text="Ciudad").pack()
        self.nom_entry = tk.Entry(self.frame_izq, **estilo_entrada)
        self.nom_entry.pack(pady=2)

        tk.Label(self.frame_izq, text="País").pack()
        self.pais_entry = tk.Entry(self.frame_izq, **estilo_entrada)
        self.pais_entry.pack(pady=2)

        tk.Label(self.frame_izq, text="Zona Horaria").pack()
        self.zona_entry = tk.Entry(self.frame_izq, **estilo_entrada)
        self.zona_entry.pack(pady=2)

        tk.Button(self.frame_izq, text="Agregar Aeropuerto", command=self._agregar_aeropuerto, **estilo_boton).pack(pady=6)

        # Sección Vuelos
        tk.Label(self.frame_izq, text="Gestión de Vuelos", **estilo_titulo).pack(pady=(20, 10))

        tk.Label(self.frame_izq, text="Origen").pack()
        self.origen_entry = tk.Entry(self.frame_izq, **estilo_entrada)
        self.origen_entry.pack(pady=2)

        tk.Label(self.frame_izq, text="Destino").pack()
        self.destino_entry = tk.Entry(self.frame_izq, **estilo_entrada)
        self.destino_entry.pack(pady=2)

        tk.Button(self.frame_izq, text="Agregar Vuelo", command=self._agregar_vuelo, **estilo_boton).pack(pady=5)
        tk.Button(self.frame_izq, text="Eliminar Vuelo", command=self._eliminar_vuelo, **estilo_boton).pack(pady=5)
        tk.Button(self.frame_izq, text="Eliminar Aeropuerto", command=self._eliminar_aeropuerto, **estilo_boton).pack(pady=5)

        # Red y BFS
        tk.Label(self.frame_izq, text="Visualización", **estilo_titulo).pack(pady=(20, 10))
        tk.Button(self.frame_izq, text="Visualizar Red", command=self._visualizar_red, **estilo_boton).pack(pady=5)

        tk.Label(self.frame_izq, text="Inicio BFS").pack()
        self.bfs_entry = tk.Entry(self.frame_izq, **estilo_entrada)
        self.bfs_entry.pack(pady=2)
        tk.Button(self.frame_izq, text="BFS", command=self._bfs, **estilo_boton).pack(pady=5)

        # Botón de limpieza
        tk.Button(self.frame_izq, text="Limpiar Campos", command=self._limpiar_campos, **estilo_boton).pack(pady=10)
        
        # Botón Acerca De
        tk.Button(self.frame_izq, text="Acerca De", command=self._mostrar_acerca_de, **estilo_boton).pack(pady=10)

    def _agregar_aeropuerto(self):
        cod = self.cod_entry.get().strip()
        nom = self.nom_entry.get().strip()
        pais = self.pais_entry.get().strip()
        zona = self.zona_entry.get().strip()
        self.red.agregar_aeropuerto(cod, nom, pais, zona)
        messagebox.showinfo("Listo", f"Aeropuerto {cod} agregado")
        self._limpiar_campos()

    def _agregar_vuelo(self):
        try:
            self.red.agregar_vuelo(self.origen_entry.get(), self.destino_entry.get())
            messagebox.showinfo("Vuelo agregado", "Se agregó el vuelo correctamente")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        finally:
            self._limpiar_campos()

    def _eliminar_vuelo(self):
        self.red.eliminar_vuelo(self.origen_entry.get(), self.destino_entry.get())
        messagebox.showinfo("Vuelo eliminado", "Se eliminó el vuelo")

    def _eliminar_aeropuerto(self):
        self.red.eliminar_aeropuerto(self.cod_entry.get())
        messagebox.showinfo("Aeropuerto eliminado", "Se eliminó el aeropuerto")

    def _visualizar_red(self):
        for widget in self.frame_der.winfo_children():
            widget.destroy()
        self.red.visualizar_red_embebida(self.frame_der)

    def _bfs(self):
        for widget in self.frame_der.winfo_children():
            widget.destroy()
        self.red.bfs_embebido(self.bfs_entry.get(), self.frame_der)
        
    def _limpiar_campos(self):
        self.cod_entry.delete(0, tk.END)
        self.nom_entry.delete(0, tk.END)
        self.pais_entry.delete(0, tk.END)
        self.zona_entry.delete(0, tk.END)
        self.origen_entry.delete(0, tk.END)
        self.destino_entry.delete(0, tk.END)
        self.bfs_entry.delete(0, tk.END)

    def _mostrar_acerca_de(self):
        mensaje = (
            "Desarrolladores del Programa:\n\n"
            "• Politrón Díaz Josué Yered\n"
            "• Pacheco Cedillo Jorge Anuar\n"
            "• Robles Cedillo Irving Xnuviko\n"
            "• Flores Duarte Ana Yuritzy\n\n"
            "Fecha de desarrollo: 17/05/2025\n"
            "Proyecto: Conexiones de Vuelos entre Aeropuertos"
        )
        messagebox.showinfo("Acerca De", mensaje)
        
# 5. ---------------- Bloque Principal -----------------------------------
if __name__ == '__main__':
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()