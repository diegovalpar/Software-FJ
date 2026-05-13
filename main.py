import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from logica import *
from custom_exceptions import *

class SoftwareFJ_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Gestión Fase 4")
        self.root.geometry("650x680")

        frame_input = tk.LabelFrame(root, text=" Registro Manual ", padx=15, pady=10)
        frame_input.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_input, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.ent_nombre = tk.Entry(frame_input)
        self.ent_nombre.grid(row=0, column=1, pady=2, sticky="ew")

        tk.Label(frame_input, text="Cédula:").grid(row=1, column=0, sticky="w")
        self.ent_id = tk.Entry(frame_input)
        self.ent_id.grid(row=1, column=1, pady=2, sticky="ew")

        tk.Label(frame_input, text="Servicio:").grid(row=2, column=0, sticky="w")
        self.cb_servicio = ttk.Combobox(frame_input, values=["Sala", "Equipo", "Asesoría"], state="readonly")
        self.cb_servicio.grid(row=2, column=1, pady=2, sticky="ew"); self.cb_servicio.current(0)

        tk.Label(frame_input, text="Cantidad:").grid(row=3, column=0, sticky="w")
        self.ent_cantidad = tk.Entry(frame_input)
        self.ent_cantidad.grid(row=3, column=1, pady=2, sticky="ew")

        tk.Button(frame_input, text="Procesar Registro", command=self.procesar_manual, bg="blue", fg="white").grid(row=4, columnspan=2, pady=10)

        tk.Button(root, text="EJECUTAR 10 OPERACIONES DE PRUEBA", command=self.ejecutar_simulacion, bg="green", fg="white").pack(pady=5)
        
        self.monitor = scrolledtext.ScrolledText(root, width=75, height=18)
        self.monitor.pack(padx=20, pady=10)

    def log_interfaz(self, mensaje):
        self.monitor.insert(tk.END, mensaje + "\n")
        self.monitor.see(tk.END)

    def procesar_manual(self):
        try:
            c = Cliente(self.ent_nombre.get(), self.ent_id.get())
            cant = int(self.ent_cantidad.get())
            tipo = self.cb_servicio.get()
            s = Sala("Sala", 50) if tipo == "Sala" else Equipo("PC", 30) if tipo == "Equipo" else Asesoria("Asesor", 100)
            
            # Ahora usamos la clase Reserva e imprimimos el estado
            reserva = Reserva(c, s, cant)
            res = f"[MANUAL] {c.mostrar_detalle()} | Estado: {reserva.estado} | Total: ${reserva.total}"
            self.log_interfaz(res)
            registrar_evento(res)
            messagebox.showinfo("Éxito", f"Reserva {reserva.estado}")
        except (InvalidClientDataError, ReservationError) as e:
            self.log_interfaz(f"[ERROR] {e}")
            registrar_evento(f"Error Manual: {e}")
        except ValueError:
            self.log_interfaz("[ERROR] Error: La cantidad debe ser numérica.")

    def ejecutar_simulacion(self):
        self.monitor.delete('1.0', tk.END)
        self.log_interfaz(">>> INICIANDO SIMULACIÓN DE 10 OPERACIONES <<<\n")
        casos = [
            ("C_OK", "Ana", "01"), ("C_ERR", "", "02"), ("S_OK", "Sala", 5),
            ("R_ERR", "Equipo", -2), ("OK_S", "Asesoría", 2), ("P_ERR", "Pago", "X"),
            ("C_OK", "Luis", "03"), ("V_ERR", "Servicio", "X"), ("S_OK", "Equipo", 3), ("C_ERR", "Pedro", "")
        ]
        for i, (tipo, d1, d2) in enumerate(casos, 1):
            self.log_interfaz(f"Op #{i}:")
            try:
                if tipo == "C_OK": 
                    c = Cliente(d1, d2); msg = f"  ÉXITO: {c.mostrar_detalle()}."
                elif tipo == "C_ERR": Cliente(d1, d2)
                elif tipo == "S_OK":
                    s = Sala("Sala", 50) if d1 == "Sala" else Asesoria("Asesor", 80)
                    r = Reserva(Cliente("Simulado", "000"), s, d2)
                    msg = f"  ÉXITO: {d1} | Estado: {r.estado} | Total: ${r.total}"
                elif tipo == "R_ERR": raise ReservationError(f"Cantidad {d2} inválida.")
                elif tipo == "P_ERR": raise InvalidPaymentMethodError("Pago rechazado.")
                elif tipo == "V_ERR": raise ServiceUnavailableError("Sin cupo.")
            except SoftwareFJError as e:
                self.log_interfaz(f"  EXCEPCIÓN: {type(e).__name__}"); registrar_evento(f"Simulacion {i}: {e}")
            else:
                self.log_interfaz(msg); registrar_evento(f"Simulacion {i}: {msg}")
            finally: self.log_interfaz("  Estado: Finalizado.")
        messagebox.showinfo("Simulación", "Operaciones completadas.")

if __name__ == "__main__":
    root = tk.Tk(); app = SoftwareFJ_GUI(root); root.mainloop()






