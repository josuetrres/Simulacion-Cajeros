# -*- coding: utf-8 -*-

import tkinter as tk
import random
import time
from threading import Thread
from caja_normal import simular_caja_normal
from caja_express import simular_caja_express

class SimulacionCajas:
    def __init__(self, master):
        self.master = master
        master.title("Simulación de Cajeros Automáticos")
        master.geometry("1000x700")
        master.config(bg="#f0f0f0")

        self.canvas = tk.Canvas(master, width=950, height=500, bg="white")
        self.canvas.pack(pady=20)

        self.btn_iniciar = tk.Button(master, text="Iniciar Simulación", font=("Arial", 14),
                                     command=self.iniciar_simulacion, bg="#4CAF50", fg="white")
        self.btn_iniciar.pack(pady=10)

        self.info_label = tk.Label(master, text="", font=("Arial", 12), bg="#f0f0f0")
        self.info_label.pack()

        self.resultado_label = tk.Label(master, text="", font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.resultado_label.pack(pady=5)

    def iniciar_simulacion(self):
        self.resultado_label.config(text="")
        self.info_label.config(text="")
        self.canvas.delete("all")

        # Crear número aleatorio de personas por caja
        self.num_express = random.randint(3, 7)
        self.num_normales = [random.randint(3, 7) for _ in range(4)]

        # Dibujar cajas
        colores = ["#2196F3", "#2196F3", "#2196F3", "#2196F3", "#8BC34A"]
        textos = [f"Normal {i+1}" for i in range(4)] + ["Express"]

        self.posiciones = []
        for i, texto in enumerate(textos):
            x1 = 60 + i*180
            y1, y2 = 100, 420
            self.canvas.create_rectangle(x1, y1, x1+120, y2, fill=colores[i], outline="black", width=2)
            self.canvas.create_text(x1+60, 80, text=texto, font=("Arial", 11))
            self.posiciones.append(x1+60)

        # Crear filas de clientes
        self.filas = []
        for i in range(4):
            n = self.num_normales[i]
            fila = [self.canvas.create_oval(self.posiciones[i]-10, 400 - j*25, self.posiciones[i]+10, 420 - j*25, fill="blue") for j in range(n)]
            self.filas.append(fila)

        # Express
        fila_exp = [self.canvas.create_oval(self.posiciones[-1]-10, 400 - j*25, self.posiciones[-1]+10, 420 - j*25, fill="green") for j in range(self.num_express)]
        self.filas.append(fila_exp)

        Thread(target=self.simular, daemon=True).start()

    def simular(self):
        totales = {}
        detalles = {}

        # --- Simular las 4 cajas normales ---
        for i in range(4):
            total, datos = simular_caja_normal(self.num_normales[i])
            totales[f"Normal {i+1}"] = total
            detalles[f"Normal {i+1}"] = datos

        # --- Simular la caja express ---
        total_exp, datos_exp = simular_caja_express(self.num_express)
        totales["Express"] = total_exp
        detalles["Express"] = datos_exp

        # --- Animación de atención ---
        for nombre, datos in detalles.items():
            fila = self.filas[int(nombre.split()[-1])-1] if "Normal" in nombre else self.filas[-1]
            for i, d in enumerate(datos):
                self.info_label.config(
                    text=f"{nombre}: Cliente {d['persona']} | {d['productos']} prod | {d['pago']} | Cajero {d['cajero']} | {d['tiempo']:.1f}s"
                )
                time.sleep(0.5)
                if fila:
                    self.canvas.delete(fila[-1])
                    fila.pop()

        # --- Resultado final ---
        mas_rapida = min(totales, key=totales.get)
        resumen = "\n".join([f"{k}: {v:.1f}s" for k, v in totales.items()])

        self.resultado_label.config(
            text=f"{resumen}\n🏆 Caja más rápida: {mas_rapida}",
            fg="#000"
        )
        self.info_label.config(text="✅ Simulación completada")

# --- EJECUTAR ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SimulacionCajas(root)
    root.mainloop()
