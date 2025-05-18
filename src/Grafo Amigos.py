# 1.- ---------------- Encabezado ----------------------------------------------
'''
Programa: Practica 3.2 Grafos
Autores: Jorge Anuar Pacheco Cedillo 
Fecha: 09 de abril del 2025
Descripción: Interfaz gráfica para ingresar perfiles de amigos, relacionarlos con etiquetas
             y visualizar la red de amigos mediante grafos, basada en tkinter y matplotlib.

Modificado por: Politrón Díaz Josué Yered
Fecha de modificación : 18/05/2025
'''

# 2.- ---------------- Importación de Módulos y Bibliotecas --------------------
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 3.- ---------------- Definición de Funciones o clases ------------------------
class GrafoAmigos:
    def __init__(self):
        self.adyacencias = {}

    def agregarPersona(self, nombre):
        if nombre not in self.adyacencias:
            self.adyacencias[nombre] = []

    def agregarAmistad(self, p1, p2, etiqueta):
        self.agregarPersona(p1)
        self.agregarPersona(p2)
        if not any(amigo == p2 for amigo, _ in self.adyacencias[p1]):
            self.adyacencias[p1].append((p2, etiqueta))
        if not any(amigo == p1 for amigo, _ in self.adyacencias[p2]):
            self.adyacencias[p2].append((p1, etiqueta))

    def eliminarAmistad(self, p1, p2):
        if p1 in self.adyacencias:
            self.adyacencias[p1] = [a for a in self.adyacencias[p1] if a[0] != p2]
        if p2 in self.adyacencias:
            self.adyacencias[p2] = [a for a in self.adyacencias[p2] if a[0] != p1]

    def eliminarPersona(self, nombre):
        if nombre in self.adyacencias:
            self.adyacencias.pop(nombre)
        for persona in self.adyacencias:
            self.adyacencias[persona] = [a for a in self.adyacencias[persona] if a[0] != nombre]

    def obtenerAmigos(self, nombre):
        return [amigo for amigo, _ in self.adyacencias.get(nombre, [])]

    def amigosEnComun(self, p1, p2):
        return list(set(self.obtenerAmigos(p1)) & set(self.obtenerAmigos(p2)))

    def obtenerRed(self):
        return self.adyacencias

    def obtenerGrafo(self):
        G = nx.Graph()
        añadidas = set()
        for persona, amigos in self.adyacencias.items():
            for amigo, etiqueta in amigos:
                arista = tuple(sorted((persona, amigo)))
                if arista not in añadidas:
                    G.add_edge(persona, amigo, label=etiqueta)
                    añadidas.add(arista)
        return G

# 4.- ---------------- Interfaz Gráfica ----------------------------------------
class InterfazRedAmigos:
    def __init__(self, root):
        self.red = GrafoAmigos()
        self.root = root
        self.root.title("Red de Amigos")
        self.root.configure(bg="#f5f5f5")
        self.root.geometry("1000x700")

        self._crear_estilo()
        self._crear_widgets()

    def _crear_estilo(self):
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", padding=4)

    def _crear_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nombre 1:").grid(row=0, column=0, sticky="e")
        self.nombre1_entry = ttk.Entry(frame, width=30)
        self.nombre1_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Nombre 2:").grid(row=1, column=0, sticky="e")
        self.nombre2_entry = ttk.Entry(frame, width=30)
        self.nombre2_entry.grid(row=1, column=1, padx=5)

        ttk.Label(frame, text="Etiqueta Amistad:").grid(row=2, column=0, sticky="e")
        self.etiqueta_entry = ttk.Entry(frame, width=30)
        self.etiqueta_entry.grid(row=2, column=1, padx=5)

        ttk.Button(frame, text="Agregar Perfil", command=self._agregar_perfil).grid(row=0, column=2, padx=10)
        ttk.Button(frame, text="Agregar Amistad", command=self._agregar_amistad).grid(row=1, column=2, padx=10)
        ttk.Button(frame, text="Eliminar Amistad", command=self._eliminar_amistad).grid(row=2, column=2, padx=10)
        ttk.Button(frame, text="Eliminar Perfil", command=self._eliminar_perfil).grid(row=3, column=2, padx=10)
        ttk.Button(frame, text="Amigos en Común", command=self._mostrar_comunes).grid(row=4, column=2, padx=10)
        ttk.Button(frame, text="Visualizar Red", command=self._mostrar_red).grid(row=5, column=2, padx=10)
        ttk.Button(frame, text="Visualizar Grafo", command=self._mostrar_grafo).grid(row=6, column=2, padx=10)
        ttk.Button(frame, text="Acerca de", command=self._mostrar_acerca).grid(row=7, column=2, padx=10)

        self.salida_text = tk.Text(frame, width=70, height=12, wrap="word", font=("Consolas", 10))
        self.salida_text.grid(row=6, column=0, columnspan=2, rowspan=4, pady=10)

        self.canvas_frame = ttk.LabelFrame(self.root, text="Visualización del Grafo", padding=10)
        self.canvas_frame.pack(fill="both", expand=True)

    def _limpiar_campos(self):
        self.nombre1_entry.delete(0, tk.END)
        self.nombre2_entry.delete(0, tk.END)
        self.etiqueta_entry.delete(0, tk.END)

    def _agregar_perfil(self):
        nombre = self.nombre1_entry.get().strip()
        if nombre:
            self.red.agregarPersona(nombre)
            self._mostrar_mensaje(f"Perfil '{nombre}' agregado.")
        self._limpiar_campos()

    def _agregar_amistad(self):
        p1 = self.nombre1_entry.get().strip()
        p2 = self.nombre2_entry.get().strip()
        etiqueta = self.etiqueta_entry.get().strip()
        if p1 and p2 and etiqueta:
            self.red.agregarAmistad(p1, p2, etiqueta)
            self._mostrar_mensaje(f"Amistad agregada entre '{p1}' y '{p2}' con etiqueta '{etiqueta}'.")
        self._limpiar_campos()

    def _eliminar_amistad(self):
        p1 = self.nombre1_entry.get().strip()
        p2 = self.nombre2_entry.get().strip()
        if p1 and p2:
            self.red.eliminarAmistad(p1, p2)
            self._mostrar_mensaje(f"Amistad entre '{p1}' y '{p2}' eliminada.")
        self._limpiar_campos()

    def _eliminar_perfil(self):
        nombre = self.nombre1_entry.get().strip()
        if nombre:
            self.red.eliminarPersona(nombre)
            self._mostrar_mensaje(f"Perfil '{nombre}' eliminado.")
        self._limpiar_campos()

    def _mostrar_comunes(self):
        p1 = self.nombre1_entry.get().strip()
        p2 = self.nombre2_entry.get().strip()
        comunes = self.red.amigosEnComun(p1, p2)
        self._mostrar_mensaje(f"Amigos en común entre '{p1}' y '{p2}': {comunes}")
        self._limpiar_campos()

    def _mostrar_red(self):
        red = self.red.obtenerRed()
        texto = "\n".join(f"{k}: {v}" for k, v in red.items())
        self._mostrar_mensaje("Red de Amigos:\n" + texto)

    def _mostrar_grafo(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        grafo = self.red.obtenerGrafo()
        fig, ax = plt.subplots(figsize=(6, 4))
        pos = nx.spring_layout(grafo)
        nx.draw(grafo, pos, ax=ax, with_labels=True, node_color='skyblue', node_size=700, font_weight='bold')
        labels = nx.get_edge_attributes(grafo, 'label')
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels, ax=ax)
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _mostrar_acerca(self):
        messagebox.showinfo("Acerca de", "Desarrollado por:\n- Jorge Anuar Pacheco Cedillo\n- Politrón Díaz Josué Yered")

    def _mostrar_mensaje(self, mensaje):
        self.salida_text.delete("1.0", tk.END)
        self.salida_text.insert(tk.END, mensaje)

# 5.- ---------------- Bloque Principal ----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazRedAmigos(root)
    root.mainloop()

# 6.- ---------------- Documentación y Comentarios------------------------------