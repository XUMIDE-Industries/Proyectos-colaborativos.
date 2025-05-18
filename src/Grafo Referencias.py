# 1.- ---------------- Encabezado ----------------------------------------------
'''
Programa: Grafo Referencias
Autores: Fuertes Espinosa Ioshua Daniel 
Fecha: 07/04/2025
Descripción: Sistema de selección de productos y sus referencias representado como un grafo.

Modificado por: Politrón Díaz Josué Yered
Fecha de modificación : 18/05/2025
'''

# 2.- ---------------- Importación de Módulos y Bibliotecas --------------------
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 3.- ---------------- Definición de Funciones o clases ------------------------
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

    def buscar(self, dato):
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                return actual
            actual = actual.siguiente
        return None

    def obtener_lista(self):
        datos = []
        actual = self.cabeza
        while actual:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos

class GrafoNoDirigido:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, vertice):
        if vertice not in self.vertices:
            self.vertices[vertice] = []

    def agregar_arista(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            if v2 not in self.vertices[v1]:
                self.vertices[v1].append(v2)
            if v1 not in self.vertices[v2]:
                self.vertices[v2].append(v1)

    def mostrar_grafo(self):
        print("\nGrafo:")
        for v, adyacentes in self.vertices.items():
            print(f"{v} -> {adyacentes}")

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Red de Productos y Referencias")
        self.root.configure(bg="#F5F5F5")
        self.root.geometry("1000x700")

        self.productos = ListaDoblementeEnlazada()
        self.referencias = ListaDoblementeEnlazada()
        self.grafo = GrafoNoDirigido()
        self.canvas_grafo = None

        self._inicializar_datos()
        self._crear_interfaz()

    def _inicializar_datos(self):
        for producto in ["Cafetera", "Televisor", "Celular"]:
            self.productos.agregar(producto)

        for referencia in [
            "1. Cafe en Grano (Nescafe)", "2. Vaso de Cafetera", "3. Filtros de Cafe",
            "4. Bocina", "5. Cable HDMI", "6. Luces RGB",
            "7. Cargador (Samsung)", "8. Funda", "9. Audifonos Bluetooth"
        ]:
            self.referencias.agregar(referencia)

    def _crear_interfaz(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TButton", font=("Segoe UI", 10, "bold"), background="#2E8B57", foreground="white", padding=6)
        estilo.configure("TLabel", font=("Segoe UI", 10), background="#F5F5F5")
        estilo.configure("TCombobox", font=("Segoe UI", 10))

        # Frame superior (formulario)
        self.frame_superior = tk.Frame(self.root, bg="#F5F5F5")
        self.frame_superior.pack(pady=10)

        ttk.Label(self.frame_superior, text="Selecciona un producto:").pack(pady=5)
        self.combo_producto = ttk.Combobox(self.frame_superior, values=self.productos.obtener_lista(), state="readonly")
        self.combo_producto.pack(pady=5)

        ttk.Label(self.frame_superior, text="Selecciona hasta 3 referencias:").pack(pady=5)
        self.combo_referencias = [ttk.Combobox(self.frame_superior, values=self.referencias.obtener_lista(), state="readonly") for _ in range(3)]
        for cb in self.combo_referencias:
            cb.pack(pady=2)

        ttk.Button(self.frame_superior, text="Agregar al Grafo", command=self._agregar_datos).pack(pady=10)
        ttk.Button(self.frame_superior, text="Limpiar Campos", command=self._limpiar_campos).pack(pady=5)
        ttk.Button(self.frame_superior, text="Acerca de", command=self._mostrar_acerca_de).pack(pady=5)

        # Frame con scroll para el grafo
        self.frame_scroll = tk.Frame(self.root)
        self.frame_scroll.pack(pady=10, fill="both", expand=True)

        self.canvas_scroll = tk.Canvas(self.frame_scroll, bg="#FFFFFF", width=960, height=400)
        self.canvas_scroll.pack(side=tk.LEFT, fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.frame_scroll, orient="vertical", command=self.canvas_scroll.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas_scroll.configure(yscrollcommand=self.scrollbar.set)

        # Frame interno dentro del canvas (contenedor real del grafo)
        self.frame_grafo = tk.Frame(self.canvas_scroll, bg="#FFFFFF")
        self.canvas_scroll.create_window((0, 0), window=self.frame_grafo, anchor="nw")

        self.frame_grafo.bind("<Configure>", lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all")))

    def _agregar_datos(self):
        producto = self.combo_producto.get()
        if not producto:
            messagebox.showwarning("Aviso", "Selecciona un producto.")
            return

        nodo_producto = self.productos.buscar(producto)
        self.grafo.agregar_vertice(producto)

        for cb in self.combo_referencias:
            ref = cb.get()
            if ref:
                nodo_ref = self.referencias.buscar(ref)
                if nodo_ref:
                    self.grafo.agregar_vertice(ref)
                    self.grafo.agregar_arista(producto, ref)

        self._limpiar_campos()
        self._mostrar_grafo()  # Actualiza automáticamente el grafo
        messagebox.showinfo("Éxito", "Producto y referencias añadidas al grafo.")

    def _limpiar_campos(self):
        self.combo_producto.set("")
        for cb in self.combo_referencias:
            cb.set("")

    def _mostrar_grafo(self):
        if self.canvas_grafo:
            self.canvas_grafo.get_tk_widget().destroy()

        G = nx.Graph()
        for nodo, adyacentes in self.grafo.vertices.items():
            for vecino in adyacentes:
                G.add_edge(nodo, vecino)

        fig = plt.Figure(figsize=(9, 4), dpi=100)
        ax = fig.add_subplot(111)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="#9FE2BF",
                node_size=2000, font_size=10, font_weight="bold", ax=ax)

        self.canvas_grafo = FigureCanvasTkAgg(fig, master=self.frame_grafo)
        self.canvas_grafo.draw()
        self.canvas_grafo.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def _mostrar_acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            "Programa: Grafo Referencias\n"
            "Autores: Fuertes Espinosa Ioshua Daniel\n"
            "Modificado por: Politrón Díaz Josué Yered\n"
            "Fecha de modificación: 18/05/2025"
        )

# 5. ---------------- Bloque Principal ----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()
