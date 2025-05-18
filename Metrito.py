'''
Nombre: Fuertes Espinosa Ioshua Daniel
        Adrian Rodriguez de Matias
        Peréz Marcelo Israel
Fecha: 17/05/2025
Descripción: Sistema para encontrar la ruta más corta entre estaciones de metro utilizando el algoritmo BFS, 
             con interfaz gráfica en Tkinter.
'''

import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Button
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import sys

class Nodo:
    def __init__(self, dato):
        self._dato = dato
        self._siguiente = None
        self._anterior = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self._cabeza = None
        self._cola = None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self._cabeza is None:
            self._cabeza = nuevo_nodo
            self._cola = nuevo_nodo
        else:
            nuevo_nodo._anterior = self._cola
            self._cola._siguiente = nuevo_nodo
            self._cola = nuevo_nodo

    def buscar(self, dato):
        nodo_actual = self._cabeza
        while nodo_actual is not None:
            if nodo_actual._dato == dato:
                return nodo_actual
            nodo_actual = nodo_actual._siguiente
        return None

    def recorrer(self):
        resultados = []
        nodo_actual = self._cabeza
        while nodo_actual is not None:
            resultados.append(nodo_actual._dato)
            nodo_actual = nodo_actual._siguiente
        return resultados

class Grafo:
    def __init__(self):
        self._vertices = {}
        self._adyacencias = {}

    def agregar_vertice(self, vertice):
        if vertice not in self._vertices:
            self._vertices[vertice] = []
            self._adyacencias[vertice] = []

    def agregar_arista(self, origen, destino):
        if origen in self._vertices and destino in self._vertices:
            self._vertices[origen].append(destino)
            self._adyacencias[origen].append(destino)

    def mostrar_grafo(self):
        for vertice, aristas in self._vertices.items():
            print(f"{vertice} -> {aristas}")

    def bfs(self, inicio):
        visitados = set()
        cola = deque([inicio])
        recorrido = []
        while cola:
            nodo = cola.popleft()
            if nodo not in visitados:
                visitados.add(nodo)
                recorrido.append(nodo)
                cola.extend([vecino for vecino in self._adyacencias[nodo] if vecino not in visitados])
        return recorrido

    def bfs_ruta(self, inicio, destino):
        if inicio not in self._vertices or destino not in self._vertices:
            return None
        padres = {inicio: None}
        visitados = set([inicio])
        cola = deque([inicio])
        while cola:
            nodo_actual = cola.popleft()
            if nodo_actual == destino:
                camino = []
                actual = destino
                while actual is not None:
                    camino.append(actual)
                    actual = padres[actual]
                camino.reverse()
                return camino
            for vecino in self._adyacencias[nodo_actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    padres[vecino] = nodo_actual
                    cola.append(vecino)
        return None 

class Metro:
    def __init__(self):
        self._grafo = Grafo()
        self._lineas = {
            "Rosa": ["Observatorio", "Tacubaya", "Juanacatlán", "Chapultepec", "Sevilla",
                     "Insurgentes", "Cuauhtémoc", "Balderas", "Salto del Agua", "Isabel la Católica",
                     "Pino Suárez", "Merced", "Candelaria", "San Lázaro", "Moctezuma", "Balbuena",
                     "Boulevard Puerto Aéreo", "Gómez Farías", "Zaragoza", "Pantitlán"],
            "Azul": ["Cuatro Caminos", "Panteones", "Tacuba", "Cuitláhuac", "Popotla",
                    "Colegio Militar", "Normal", "San Cosme", "Revolución", "Hidalgo",
                    "Bellas Artes", "Allende", "Zócalo", "Pino Suárez", "San Antonio Abad", "Chabacano", "Viaducto", "Xola"],
            "Verde Olivo": ["Indios Verdes", "Deportivo 18 de Marzo", "Potrero", "La Raza",
                           "Tlatelolco", "Guerrero", "Hidalgo", "Juárez", "Balderas"],
            "Naranja": ["Tacubaya", "Constituyentes", "Auditorio", "Polanco", "San Joaquín", "Tacuba"]
        }
        self._estaciones_info = {}
        self.inicializar_grafo()

    def inicializar_grafo(self):
        for linea, estaciones in self._lineas.items():
            for estacion in estaciones:
                self._grafo.agregar_vertice(estacion)
                if estacion not in self._estaciones_info:
                    self._estaciones_info[estacion] = {"lineas": [linea]}
                else:
                    self._estaciones_info[estacion]["lineas"].append(linea)
        
        for linea, estaciones in self._lineas.items():
            for i in range(len(estaciones) - 1):
                self._grafo.agregar_arista(estaciones[i], estaciones[i + 1])
                self._grafo.agregar_arista(estaciones[i + 1], estaciones[i])

    def obtener_colores_disponibles(self):
        return sorted(list(self._lineas.keys()))

    def obtener_estaciones_por_color(self, color):
        if color in self._lineas:
            return self._lineas[color]
        return []

    def obtener_linea_de_estacion(self, estacion):
        if estacion in self._estaciones_info:
            return self._estaciones_info[estacion]["lineas"]
        return []

    def obtener_ruta(self, origen, destino):
        return self._grafo.bfs_ruta(origen, destino)

    def obtener_lista_estaciones(self):
        return sorted(list(self._estaciones_info.keys()))

    def crear_grafo_completo(self):
        G = nx.DiGraph()
        for nodo, lista_adyacencia in self._grafo._vertices.items():
            G.add_node(nodo)
            for vecino in lista_adyacencia:
                G.add_edge(nodo, vecino)
        return G

    def crear_grafo_ruta(self, ruta):
        if not ruta:
            return None
            
        G = nx.DiGraph()
        for i, estacion in enumerate(ruta):
            G.add_node(estacion, orden=i+1)
        for i in range(len(ruta) - 1):
            G.add_edge(ruta[i], ruta[i + 1])
        
        return G, ruta

class MetroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Metro - Búsqueda de Rutas")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.metro = Metro()
        self.menu_principal = tk.Menu(self.root)
        self.root.config(menu=self.menu_principal)
        self.menu_ayuda = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Ayuda", menu=self.menu_ayuda)
        self.menu_ayuda.add_command(label="Acerca de", command=self.acerca_de)
        
        self.setup_ui()
        
    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Desrrolldores del Programa:\n-Fuertes Espinosa Ioshua Daniel\n-Adrian Rodriguez de Matias\n-Peréz Marcelo Israel\n\nFecha de desarrollo: 17/05/2025\nProyecto: Sistema de Metro")
        
    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tab_buscar_ruta = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_buscar_ruta, text="Buscar Ruta")
        self.tab_grafo_completo = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_grafo_completo, text="Grafo Completo")
        self.tab_estaciones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_estaciones, text="Estaciones por Línea")
        self.setup_buscar_ruta_tab()
        self.setup_grafo_completo_tab()
        self.setup_estaciones_tab()
    
    def setup_buscar_ruta_tab(self):
        main_frame = ttk.Frame(self.tab_buscar_ruta)
        main_frame.pack(fill=tk.BOTH, expand=True)
        left_frame = ttk.LabelFrame(main_frame, text="Selección de Estaciones")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.right_frame = ttk.LabelFrame(main_frame, text="Resultados")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        origen_frame = ttk.Frame(left_frame)
        origen_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(origen_frame, text="Línea Origen:").pack(side=tk.LEFT, padx=5)
        self.combo_linea_origen = ttk.Combobox(origen_frame, state="readonly", width=15)
        self.combo_linea_origen.pack(side=tk.LEFT, padx=5)
        self.combo_linea_origen['values'] = self.metro.obtener_colores_disponibles()
        self.combo_linea_origen.bind("<<ComboboxSelected>>", self.actualizar_estaciones_origen)
        
        ttk.Label(origen_frame, text="Estación Origen:").pack(side=tk.LEFT, padx=5)
        self.combo_estacion_origen = ttk.Combobox(origen_frame, state="readonly", width=20)
        self.combo_estacion_origen.pack(side=tk.LEFT, padx=5)
        destino_frame = ttk.Frame(left_frame)
        destino_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(destino_frame, text="Línea Destino:").pack(side=tk.LEFT, padx=5)
        self.combo_linea_destino = ttk.Combobox(destino_frame, state="readonly", width=15)
        self.combo_linea_destino.pack(side=tk.LEFT, padx=5)
        self.combo_linea_destino['values'] = self.metro.obtener_colores_disponibles()
        self.combo_linea_destino.bind("<<ComboboxSelected>>", self.actualizar_estaciones_destino)
        
        ttk.Label(destino_frame, text="Estación Destino:").pack(side=tk.LEFT, padx=5)
        self.combo_estacion_destino = ttk.Combobox(destino_frame, state="readonly", width=20)
        self.combo_estacion_destino.pack(side=tk.LEFT, padx=5)
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Buscar Ruta", command=self.buscar_ruta).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_busqueda).pack(side=tk.LEFT, padx=5)

        self.resultado_frame = ttk.Frame(self.right_frame)
        self.resultado_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.resultado_texto = tk.Text(self.resultado_frame, wrap=tk.WORD, height=10, width=40)
        self.resultado_texto.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.resultado_texto, orient="vertical", command=self.resultado_texto.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultado_texto.config(yscrollcommand=scrollbar.set)
        self.resultado_texto.config(state=tk.DISABLED)
        
        self.grafico_frame = ttk.Frame(self.right_frame)
        self.grafico_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_grafo_completo_tab(self):
        self.grafo_completo_frame = ttk.Frame(self.tab_grafo_completo)
        self.grafo_completo_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(self.grafo_completo_frame, text="Visualizar Grafo Completo", 
                   command=self.visualizar_grafo_completo).pack(pady=10)
        
        self.grafo_completo_canvas_frame = ttk.Frame(self.grafo_completo_frame)
        self.grafo_completo_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_estaciones_tab(self):
        estaciones_frame = ttk.Frame(self.tab_estaciones)
        estaciones_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        linea_frame = ttk.Frame(estaciones_frame)
        linea_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(linea_frame, text="Seleccione Línea:").pack(side=tk.LEFT, padx=5)
        self.combo_linea_estaciones = ttk.Combobox(linea_frame, state="readonly", width=15)
        self.combo_linea_estaciones.pack(side=tk.LEFT, padx=5)
        self.combo_linea_estaciones['values'] = self.metro.obtener_colores_disponibles()
        self.combo_linea_estaciones.bind("<<ComboboxSelected>>", self.mostrar_estaciones_por_linea)
        
        estaciones_list_frame = ttk.LabelFrame(estaciones_frame, text="Estaciones")
        estaciones_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(estaciones_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.estaciones_listbox = tk.Listbox(estaciones_list_frame, yscrollcommand=scrollbar.set)
        self.estaciones_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.estaciones_listbox.yview)
    
    def actualizar_estaciones_origen(self, event=None):
        linea = self.combo_linea_origen.get()
        estaciones = self.metro.obtener_estaciones_por_color(linea)
        self.combo_estacion_origen['values'] = estaciones
        self.combo_estacion_origen.current(0) if estaciones else None
    
    def actualizar_estaciones_destino(self, event=None):
        linea = self.combo_linea_destino.get()
        estaciones = self.metro.obtener_estaciones_por_color(linea)
        self.combo_estacion_destino['values'] = estaciones
        self.combo_estacion_destino.current(0) if estaciones else None
    
    def mostrar_estaciones_por_linea(self, event=None):
        linea = self.combo_linea_estaciones.get()
        estaciones = self.metro.obtener_estaciones_por_color(linea)
        self.estaciones_listbox.delete(0, tk.END)
        for i, estacion in enumerate(estaciones):
            self.estaciones_listbox.insert(tk.END, f"{i+1}. {estacion}")
    
    def buscar_ruta(self):
        if not self.combo_linea_origen.get() or not self.combo_estacion_origen.get() or \
           not self.combo_linea_destino.get() or not self.combo_estacion_destino.get():
            messagebox.showwarning("Datos incompletos", "Por favor, seleccione todas las opciones necesarias.")
            return
        
        estacion_origen = self.combo_estacion_origen.get()
        estacion_destino = self.combo_estacion_destino.get()
        ruta = self.metro.obtener_ruta(estacion_origen, estacion_destino)
        if ruta:
            self.mostrar_resultado_texto(ruta, estacion_origen, estacion_destino)
            self.mostrar_grafico_ruta(ruta)
        else:
            messagebox.showinfo("Sin ruta", f"No se encontró ruta entre {estacion_origen} y {estacion_destino}.")
    
    def mostrar_resultado_texto(self, ruta, estacion_origen, estacion_destino):
        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, f"=== RUTA DE {estacion_origen} A {estacion_destino} ===\n\n")
        lista_ruta = ListaDoblementeEnlazada()
        for estacion in ruta:
            lista_ruta.agregar(estacion)
        transbordo_anterior = None
        for i, estacion in enumerate(ruta):
            lineas = self.metro.obtener_linea_de_estacion(estacion)
            if i > 0:
                estacion_anterior = ruta[i-1]
                lineas_anterior = set(self.metro.obtener_linea_de_estacion(estacion_anterior))
                lineas_actual = set(lineas)
                lineas_comunes = lineas_anterior.intersection(lineas_actual)
                if lineas_comunes:
                    linea_actual = list(lineas_comunes)[0]
                else:
                    linea_actual = lineas[0]
            else:
                color_origen = self.combo_linea_origen.get()
                linea_actual = color_origen if color_origen in lineas else lineas[0]

            if i > 0:
                estacion_anterior = ruta[i-1]
                lineas_anterior = self.metro.obtener_linea_de_estacion(estacion_anterior)
                if set(lineas).intersection(set(lineas_anterior)):
                    pass
                else:
                    linea_anterior = lineas_anterior[0]
                    linea_nueva = lineas[0]
                    transbordo = f"TRANSBORDO en {estacion}: Línea {linea_anterior} → Línea {linea_nueva}\n"
                    if transbordo != transbordo_anterior:
                        self.resultado_texto.insert(tk.END, transbordo)
                        transbordo_anterior = transbordo
            if i == 0:
                self.resultado_texto.insert(tk.END, f"Inicio: {estacion} (Línea {linea_actual})\n")
            elif i == len(ruta) - 1:
                self.resultado_texto.insert(tk.END, f"Llegada: {estacion} (Línea {linea_actual})\n")
            else:
                self.resultado_texto.insert(tk.END, f"{i}. {estacion} (Línea {linea_actual})\n")
        self.resultado_texto.insert(tk.END, f"\nTotal de estaciones: {len(ruta)}\n")
        self.resultado_texto.config(state=tk.DISABLED)
    
    def mostrar_grafico_ruta(self, ruta):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()
        G, ruta = self.metro.crear_grafo_ruta(ruta)
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        colores_lineas = {
            "Rosa": '#FF69B4',       # Rosa fuerte
            "Azul": '#1E90FF',       # Azul real
            "Verde Olivo": '#556B2F', # Verde olivo
            "Naranja": '#FF8C00'     # Naranja oscuro
        }
        node_colors = []
        lineas_por_estacion = {}  # Para incluir en las etiquetas
        
        for estacion in G.nodes():
            lineas = self.metro.obtener_linea_de_estacion(estacion)
            lineas_por_estacion[estacion] = lineas
            if len(lineas) > 1:  # Cuando sea un transbordo se pondrá un color diferente
                color = '#800080'  # Purpura
            else:
                linea = lineas[0]
                color = colores_lineas.get(linea, '#A9A9A9')
            node_colors.append(color)
        lineas_activas = {}
        for i in range(len(ruta) - 1):
            estacion_actual = ruta[i]
            estacion_siguiente = ruta[i + 1]
            lineas_actuales = set(self.metro.obtener_linea_de_estacion(estacion_actual))
            lineas_siguientes = set(self.metro.obtener_linea_de_estacion(estacion_siguiente))
            lineas_comunes = lineas_actuales.intersection(lineas_siguientes)
            if lineas_comunes:
                linea_activa = sorted(list(lineas_comunes))[0]
            else:
                linea_activa = sorted(list(lineas_actuales))[0]
            lineas_activas[(estacion_actual, estacion_siguiente)] = linea_activa
        pos = {}
        for i, estacion in enumerate(ruta):
            pos[estacion] = (i, 0)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=1500, edgecolors='black', linewidths=1.5)
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            linea_actual = lineas_activas.get((origen, destino), "")
            color_arista = colores_lineas.get(linea_actual, 'black')
            nx.draw_networkx_edges(
                G, pos, ax=ax,
                edgelist=[(origen, destino)],
                width=2,
                edge_color=color_arista,
                arrowstyle='-|>',
                arrowsize=15,
                alpha=0.8
            )
        labels = {}
        for node in G.nodes():
            orden = G.nodes[node]['orden']
            lineas_texto = ", ".join(lineas_por_estacion[node])
            labels[node] = f"{node}\n({orden})\n{lineas_texto}"
        nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=7, font_weight='bold')
        ax.set_title("Ruta completa del metro a seguir", fontsize=12, fontweight='bold')
        ax.axis('off')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def visualizar_grafo_completo(self):
        for widget in self.grafo_completo_canvas_frame.winfo_children():
            widget.destroy()
        G = self.metro.crear_grafo_completo()
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', 
                node_size=700, font_size=8, font_weight='bold', 
                arrowstyle='-|>', arrowsize=10, alpha=0.8)
        ax.set_title("Grafo Completo del Sistema de Metro", fontsize=14, fontweight='bold')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.grafo_completo_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def limpiar_busqueda(self):
        self.combo_linea_origen.set('')
        self.combo_estacion_origen.set('')
        self.combo_linea_destino.set('')
        self.combo_estacion_destino.set('')
        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.config(state=tk.DISABLED)
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = MetroGUI(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Error en la aplicación: {e}")
        print(f"Error en la aplicación: {e}")