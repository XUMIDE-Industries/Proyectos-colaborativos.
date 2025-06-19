# 1.- ---------------- Encabezado ----------------------------------------------

'''

'''

# 2.- ---------------- Importación de Módulos y Bibliotecas --------------------
import threading
import queue
import time
import random


# 3.- ---------------- Definición de Funciones o clases ------------------------
class Cinepolis:
  def __init__(self):
    self._cola_clientes = queue.Queue()
    self._lock_atendidos = threading.Lock()
    self._sem = threading.Semaphore(3)
    self._atendidos = 0
    self._cerrar = False
  def llegada_clientes(self, total):
    for i in range(1, total + 1):
      time.sleep(random.uniform(0.5,0.2))
      self._cola_clientes.put(f"Cliente-{i}")
      print(f"Llegó Cliente-{i} (En Cola: {self._cola_clientes.qsize()})")
  def caja (self, numero):
    while True:
      try:
        cliente = self._cola_clientes.get(timeout=2)
      except queue.Empty:
        break
      with self._sem:
        print(f"[Caja-{numero}] Atendiendo a {cliente}")
        time.sleep(random.uniform(0.2,0.6))
        temp = self._atendidos 
        time.sleep(0.001)
        self._atendidos = temp + 1
        print(f"[Caja-{numero}] Terminó con {cliente} | Total atendidos: {self._atendidos}")
      self._cola_clientes.task_done()
  def simulacion_cola(self):
    total_clientes = 50 
    hilo_productor = threading.Thread(target=self.llegada_clientes, args=(total_clientes,)) 
    hilo_productor.start()
    hilos_cajas = [threading.Thread(target=self.caja, args=(i,)) for i in range(1,6)] 
    print("Simulacion Dulceria Cinepolis")
    for hilo in hilos_cajas:
      hilo.start()
    hilo_productor.join()
    self._cerrar = True 
    for h in hilos_cajas:
      h.join()
    print(f"\nFINALIZADO \nTotal Esperados: {total_clientes} | Total Atendidos: {self._atendidos}") 
class Hilo:
  def __init__(self, dulceria_instance, total): 
    self._dulceria = dulceria_instance 
    self._total = total 
  def start(self):
    self._hilo = threading.Thread(target=self._dulceria.llegada_clientes, args=(self._total,)) 
    self._hilo.start()
    self._hilo_cajas = [threading.Thread(target=self._dulceria.caja, args=(i,)) for i in range(1,6)] 
    print("Simulacion Dulceria Cinepolis")
    for hilo in self._hilo_cajas:
      hilo.start()
    self._hilo.join()
    self._dulceria._cola_clientes.join() 
    for h in self._hilo_cajas:
      h.join()
    print(f"\nFINALIZADO \nTotal Esperados: {self._total} | Total Atendidos: {self._dulceria._atendidos}") 
# 4.- ---------------- Variables Globales --------------------------------------


# 5.- ---------------- Bloque Principal ----------------------------------------
if __name__ == "__main__":
  dulceria = Cinepolis()
  dulceria.simulacion_cola()
  hilo = Hilo(dulceria, 50) 
  hilo.start()

# 6.- ---------------- Manejo de Excepciones -----------------------------------


# 7.- ---------------- Documentación y Comentarios------------------------------