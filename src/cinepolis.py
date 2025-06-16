# 1. ---------------- Encabezado -----------------------------------
'''
Programa: Simulación de Dulcería Cinépolis (Atención Eficiente)
Autores: Politrón Díaz Josué Yered, 
        Pacheco Cedillo Jorge Anuar, 
        Fuertes Espinosa Ioshua Daniel, 
        Rodriguez de Matias Adrian
        Robles Cedillo Irving Xnuviko
Fecha: 16/06/2025
Descripción: Simula la atención eficiente a clientes en la dulcería de Cinépolis con 5 cajas.
Cada cliente llega, espera en fila y es atendido cuando una caja se libera.
Se calcula el tiempo que tarda cada caja en atender y cuánto tiempo esperó cada cliente.
Interfaz gráfica profesional, con colores, botones y estadísticas.
'''
# 2. ---------------- Importación de Módulos y Bibliotecas ---------------------
import tkinter as tk
import threading
import queue
import time
import random
import csv
import os
import subprocess
from tkinter import messagebox

# 3. ---------------- Definición de Funciones o Clases -------------------------
class CinepolisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Cinépolis - Simulación Dulcería")
        self.root.geometry("970x600")
        self.root.configure(bg="#f4f4f4")

        self._cola_clientes = queue.Queue()
        self._lock_atendidos = threading.Lock()
        self._atendidos = 0
        self._tiempos_cajas = [[] for _ in range(5)]
        self._clientes_en_espera = []
        self._timestampllegada = {}

        self.productos = {
            "Palomitas": 20,
            "Nachos con queso": 25,
            "Refresco": 15,
            "Ice": 12
        }

        self._crear_interfaz()

    def _crear_interfaz(self):
        titulo = tk.Label(self.root, text="🍿 Simulación Dulcería Cinépolis", font=('Helvetica', 18, 'bold'), bg="#f4f4f4", fg="#004080")
        titulo.place(x=20, y=10)

        self.marco_cajas = tk.LabelFrame(self.root, text="Cajas", font=('Arial', 12, 'bold'), bg="#f4f4f4")
        self.marco_cajas.place(x=20, y=60, width=550, height=300)

        self.caja_labels = []
        for i in range(5):
            label = tk.Label(self.marco_cajas, text=f'Caja {i+1}: Disponible', bg='lightgreen',
                             width=60, font=('Arial', 11), anchor='w', relief='sunken', padx=5)
            label.place(x=10, y=10 + i*50)
            self.caja_labels.append(label)

        self.clientes_text = tk.Text(self.root, height=25, width=45, font=('Consolas', 10), bg="#fffaf0", relief='sunken', bd=2)
        self.clientes_text.place(x=590, y=60)

        self.total_label = tk.Label(self.root, text="Total atendidos: 0", font=('Arial', 12, 'bold'), bg="#f4f4f4", fg="black")
        self.total_label.place(x=20, y=370)

        self.estadisticas_label = tk.Label(self.root, text="⏱️ Tiempo promedio por caja:\n" + "\n".join([f"Caja {i+1}: -" for i in range(5)]),
                                            font=('Arial', 10), bg="#f4f4f4", justify="left")
        self.estadisticas_label.place(x=20, y=410)

        self.btn_iniciar = tk.Button(self.root, text="▶ Iniciar Simulación", font=('Arial', 12, 'bold'),
                                     bg="#146397", fg="white", command=self.iniciar_simulacion)
        self.btn_iniciar.place(x=740, y=520, width=200, height=40)
        
        self.btn_csv = tk.Button(self.root, text="📄 Abrir CSV", font=('Arial', 11),
                         bg="#146397", fg="white", command=self._abrir_csv)
        self.btn_csv.place(x=160, y=520, width=130, height=30)

        self.btn_acerca = tk.Button(self.root, text="ℹ Acerca De", font=('Arial', 11),
                                    bg="#146397", fg="white", command=self._mostrar_acerca_de)
        self.btn_acerca.place(x=20, y=520, width=120, height=30)

        self.label_espera = tk.Label(self.root, text="🕒 Clientes en espera: 0", font=('Arial', 11), bg="#f4f4f4", fg="darkred")
        self.label_espera.place(x=600, y=450)

    def _mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", 
            "📌 Desarrolladores del Programa:\n\n"
            "• Politrón Díaz Josué Yered\n"
            "• Pacheco Cedillo Jorge Anuar\n"
            "• Robles Cedillo Irving Xnuviko\n"
            "• Rodriguez de Matias Adrian\n"
            "• Fuertes Espinosa Ioshua Daniel\n\n"
            "💻Versión: 1.2\n📅 Fecha: 16 de junio de 2025\n\n"
            "🎯 Proyecto de concurrencia y GUI - Cinépolis")

    def iniciar_simulacion(self):
        self._registro_csv = []
        self._atendidos = 0
        self._tiempos_cajas = [[] for _ in range(5)]
        self._clientes_en_espera.clear()
        self._timestampllegada.clear()
        self.clientes_text.delete(1.0, tk.END)
        self.total_label.config(text="Total atendidos: 0")
        self.label_espera.config(text="🕒 Clientes en espera: 0")
        self.estadisticas_label.config(text="⏱️ Tiempo promedio por caja:\n" + "\n".join([f"Caja {i+1}: -" for i in range(5)]))

        total_clientes = 50
        for i in range(1, 6):
            threading.Thread(target=self._caja, args=(i,), daemon=True).start()

        threading.Thread(target=self._llegada_clientes, args=(total_clientes,), daemon=True).start()

    def _llegada_clientes(self, total):
        for i in range(1, total + 1):
            time.sleep(random.uniform(1.0, 2.0))
            producto = random.choice(list(self.productos.keys()))
            cliente = (f"Cliente-{i}", producto)
            self._cola_clientes.put(cliente)
            self._clientes_en_espera.append(cliente)
            self._timestampllegada[cliente[0]] = time.time()
            self._actualizar_espera()
            self._agregar_cliente_texto(cliente)

    def _agregar_cliente_texto(self, cliente):
        nombre, producto = cliente
        self.clientes_text.insert(tk.END, f"🟢 {nombre} llegó y espera por {producto}\n")
        self.clientes_text.see(tk.END)

    def _actualizar_estado_caja(self, index, ocupado, cliente="", producto=""):
        if ocupado:
            texto = f"❌ Caja {index+1}: Atendiendo a {cliente} - {producto}"
            color = "#ff4d4d"
        else:
            texto = f"✅ Caja {index+1}: Disponible"
            color = "lightgreen"
        self.caja_labels[index].config(text=texto, bg=color)

    def _actualizar_espera(self):
        self.label_espera.config(text=f"🕒 Clientes en espera: {self._cola_clientes.qsize()}")

    def _actualizar_estadisticas(self):
        texto = "⏱️ Tiempo promedio por caja:\n"
        for i in range(5):
            tiempos = self._tiempos_cajas[i]
            if tiempos:
                promedio = sum(tiempos) / len(tiempos)
                texto += f"Caja {i+1}: {promedio:.2f} s\n"
            else:
                texto += f"Caja {i+1}: -\n"
        self.estadisticas_label.config(text=texto)

    def _caja(self, numero):
        index = numero - 1
        while True:
            nombre, producto = self._cola_clientes.get()
            llegada = self._timestampllegada.pop(nombre, time.time())
            espera = round(time.time() - llegada, 2)

            with self._lock_atendidos:
                if (nombre, producto) in self._clientes_en_espera:
                    self._clientes_en_espera.remove((nombre, producto))

            self._actualizar_espera()
            self._actualizar_estado_caja(index, True, nombre, producto)

            inicio = time.time()
            time.sleep(self.productos[producto])
            fin = time.time()
            duracion = round(fin - inicio, 2)
            self._tiempos_cajas[index].append(duracion)

            with self._lock_atendidos:
                self._atendidos += 1
                self.total_label.config(text=f"Total atendidos: {self._atendidos}")
                self._actualizar_estadisticas()
                self._registro_csv.append({
                    "Cliente": nombre,
                    "Producto": producto,
                    "Caja": numero,
                    "Espera (s)": espera,
                    "Atención (s)": duracion
                })

            self.clientes_text.insert(tk.END, f"📦 Caja {numero} atendió a {nombre} ({producto})\n"
                                            f"⏳ Esperó: {espera:.2f} s | Atención: {duracion:.2f} s\n\n")
            self.clientes_text.see(tk.END)

            self._actualizar_estado_caja(index, False)
            self._cola_clientes.task_done()

            if self._atendidos == 50:
                self._guardar_datos_csv()
    
    def _guardar_datos_csv(self):
        nombre_archivo = "registro_clientes_cinepolis.csv"
        with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
            campos = ["Cliente", "Producto", "Caja", "Espera (s)", "Atención (s)"]
            writer = csv.DictWriter(archivo, fieldnames=campos)
            writer.writeheader()
            writer.writerows(self._registro_csv)
        print(f"📁 Datos guardados en '{nombre_archivo}'")
        
    def _abrir_csv(self):
        nombre_archivo = "registro_clientes_cinepolis.csv"
        if os.path.exists(nombre_archivo):
            try:
                if os.name == 'nt':  
                    os.startfile(nombre_archivo)
                else: 
                    subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', nombre_archivo])
            except Exception as e:
                print(f"Error al abrir el archivo: {e}")
        else:
            print("Archivo CSV no encontrado.")

# 4. ---------------- Bloque Principal -----------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CinepolisGUI(root)
    root.mainloop()
