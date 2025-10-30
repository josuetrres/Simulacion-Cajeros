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
        master.title(" Simulación de Atención en Cajas")
        master.geometry("1100x820")
        master.config(bg="#F9FAFB")

        # --- Encabezado ---
        tk.Label(
            master,
            text=" Simulación de Atención en Cajas",
            font=("Segoe UI", 22, "bold"),
            fg="#1E293B",
            bg="#F9FAFB"
        ).pack(pady=(20, 5))

        # --- Panel de configuración ---
        frame_config = tk.Frame(master, bg="#E0E7FF", highlightthickness=1, highlightbackground="#CBD5E1")
        frame_config.pack(pady=20, padx=20, ipadx=10, ipady=15)

        # Número de cajas normales
        tk.Label(frame_config, text="Cajas normales:", bg="#E0E7FF", fg="#1E293B",
                 font=("Segoe UI", 12, "bold")).grid(row=0, column=0, padx=10)

        self.num_cajas = tk.Spinbox(frame_config, from_=1, to=5, width=5, font=("Segoe UI", 12),
                                    justify="center", relief="flat", bg="#FFFFFF", fg="#1E293B",
                                    highlightthickness=1, highlightbackground="#CBD5E1", highlightcolor="#2563EB")
        self.num_cajas.grid(row=0, column=1, padx=5)

        # Rango de personas
        tk.Label(frame_config, text="Personas por caja:", bg="#E0E7FF", fg="#1E293B",
                 font=("Segoe UI", 12, "bold")).grid(row=0, column=2, padx=10)

        def entry_style(parent, default):
            e = tk.Entry(parent, font=("Segoe UI", 12), width=5, justify="center",
                         relief="flat", bg="#FFFFFF", fg="#1E293B", highlightthickness=1)
            e.insert(0, str(default))
            e.config(highlightbackground="#CBD5E1", highlightcolor="#2563EB")
            return e

        tk.Label(frame_config, text="Mínimo", bg="#E0E7FF", fg="#334155",
                 font=("Segoe UI", 11)).grid(row=0, column=3, padx=5)
        self.min_personas = entry_style(frame_config, 3)
        self.min_personas.grid(row=0, column=4)

        tk.Label(frame_config, text="Máximo", bg="#E0E7FF", fg="#334155",
                 font=("Segoe UI", 11)).grid(row=0, column=5, padx=5)
        self.max_personas = entry_style(frame_config, 7)
        self.max_personas.grid(row=0, column=6)

        # Botón moderno
        self.btn_iniciar = tk.Button(
            frame_config, text="Iniciar Simulación",
            font=("Segoe UI", 12, "bold"),
            bg="#3B82F6", fg="white",
            activebackground="#2563EB",
            activeforeground="white",
            relief="flat", bd=0,
            padx=15, pady=6,
            command=self.iniciar_simulacion
        )
        self.btn_iniciar.grid(row=0, column=7, padx=15)
        self.btn_iniciar.bind("<Enter>", lambda e: self.btn_iniciar.config(bg="#2563EB"))
        self.btn_iniciar.bind("<Leave>", lambda e: self.btn_iniciar.config(bg="#3B82F6"))

        # --- Área visual de cajas ---
        self.canvas = tk.Canvas(master, width=1000, height=420, bg="#FFFFFF",
                                highlightthickness=1, highlightbackground="#E2E8F0")
        self.canvas.pack(pady=(10, 25))

        self.info_label = tk.Label(master, text="", font=("Segoe UI", 12), bg="#F9FAFB", fg="#475569")
        self.info_label.pack()

        # --- Panel de resultados ---
        frame_resultado = tk.Frame(master, bg="#FFFFFF", highlightthickness=1, highlightbackground="#E2E8F0")
        frame_resultado.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(frame_resultado, text="📊 Resultados de la Simulación", font=("Segoe UI", 14, "bold"),
                 bg="#FFFFFF", fg="#1E293B").pack(anchor="w", padx=15, pady=(10, 0))

        self.text_resultado = tk.Text(frame_resultado, wrap="word", height=12, font=("Consolas", 10),
                                      bg="#F8FAFC", fg="#1E293B", relief="flat", padx=15, pady=10)
        self.text_resultado.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        scrollbar = tk.Scrollbar(frame_resultado, command=self.text_resultado.yview)
        scrollbar.pack(side="right", fill="y", pady=10)
        self.text_resultado.config(yscrollcommand=scrollbar.set)

    def iniciar_simulacion(self):
        self.text_resultado.delete("1.0", tk.END)
        self.info_label.config(text="")
        self.canvas.delete("all")

        try:
            minimo = int(self.min_personas.get())
            maximo = int(self.max_personas.get())
            n_cajas = int(self.num_cajas.get())

            if minimo <= 0 or maximo < minimo or n_cajas <= 0:
                raise ValueError
        except ValueError:
            self.info_label.config(text="⚠️ Ingrese valores válidos para las cajas y personas.", fg="#DC2626")
            return

        # Cajas normales + express
        extra = random.randint(3, 7)
        self.num_express = random.randint(minimo + extra, maximo + extra)
        self.num_normales = [random.randint(minimo, maximo) for _ in range(n_cajas)]

        # Colores pastel
        colores = ["#DCFCE7", "#FEF9C3", "#FFEDD5", "#E0E7FF", "#FCE7F3"]
        textos = [f"Normal {i+1}" for i in range(n_cajas)] + ["Express"]

        self.posiciones = []
        separacion = 900 // (len(textos))
        inicio = 60

        for i, texto in enumerate(textos):
            x1 = inicio + i * separacion
            y1, y2 = 120, 380

            # 💡 Color diferente para la caja Express
            if texto == "Express":
                color_fondo = "#A9B7FF" 
                borde = "#29009B"         
            else:
                color_fondo = colores[i % len(colores)]
                borde = "#CBD5E1"

            self.canvas.create_rectangle(x1, y1, x1+150, y2,
                                        fill=color_fondo,
                                        outline=borde, width=2)

            self.canvas.create_text(x1+75, 100, text=texto,
                                    font=("Segoe UI", 12, "bold"),
                                    fill="#1E293B")

            self.posiciones.append(x1+75)
            personas = self.num_normales[i] if i < n_cajas else self.num_express
            self.canvas.create_text(x1+75, 390, text=f"{personas} personas",
                                    font=("Segoe UI", 10), fill="#475569")


        # Crear filas de clientes
        self.filas = []
        for i in range(n_cajas):
            n = self.num_normales[i]
            fila = [self.canvas.create_oval(self.posiciones[i]-10, 360 - j*25,
                                            self.posiciones[i]+10, 380 - j*25, fill="#3B82F6", outline="") for j in range(n)]
            self.filas.append(fila)

        fila_exp = [self.canvas.create_oval(self.posiciones[-1]-10, 360 - j*25,
                                            self.posiciones[-1]+10, 380 - j*25, fill="#6366F1", outline="") for j in range(self.num_express)]
        self.filas.append(fila_exp)

        Thread(target=self.simular, daemon=True).start()

    def simular(self):
        totales = {}
        detalles = {}

        for i in range(len(self.num_normales)):
            total, datos = simular_caja_normal(self.num_normales[i])
            totales[f"Normal {i+1}"] = total
            detalles[f"Normal {i+1}"] = datos

        total_exp, datos_exp = simular_caja_express(self.num_express)
        totales["Express"] = total_exp
        detalles["Express"] = datos_exp

        # --- Animación ---
        for nombre, datos in detalles.items():
            fila = self.filas[int(nombre.split()[-1])-1] if "Normal" in nombre else self.filas[-1]
            for d in datos:
                self.info_label.config(
                    text=f"{nombre}: Cliente {d['persona']} | {d['productos']} prod | {d['pago']} | Cajero {d['cajero']} | {d['tiempo'] / 60:.2f} min",
                    fg="#334155"
                )
                time.sleep(0.4)
                if fila:
                    self.canvas.delete(fila[-1])
                    fila.pop()

        # --- Resultado final detallado ---
        mas_rapida = min(totales, key=totales.get)

        resumen = "=== RESULTADOS DETALLADOS ===\n\n"
        for caja, clientes in detalles.items():
            resumen += f"{caja}:\n"
            for d in clientes:
                resumen += (f"  Cliente {d['persona']:>2}: "
                            f"{d['productos']:>2} productos | "
                            f"Pago: {d['pago']:<8} | "
                            f"Cajero: {d['cajero']:<9} | "
                            f"Tiempo: {d['tiempo'] / 60:.2f} min\n")
            resumen += f"➡️ Tiempo total: {totales[caja] / 60:.2f} min\n\n"

        resumen += f"💡 Caja más rápida: {mas_rapida} ({totales[mas_rapida] / 60:.2f} min)"
        self.text_resultado.insert("1.0", resumen)
        self.info_label.config(text="✅ Simulación completada", fg="#15803D")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulacionCajas(root)
    root.mainloop()
