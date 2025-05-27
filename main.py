# from logic.simulator import Simulator
# from logic.process import Process
# from logic.task import Task


# simulator = Simulator()


# process1 = Process("Proceso 1", [])

# process1.add_task(Task("task 1.1", 2))
# process1.add_task(Task("task 1.2", 3))



# process2 = Process("Proceso 2", )

# process2.add_task(Task("task 2.1", 1))
# process2.add_task(Task("task 2.2", 2))

# process1.next_process = process2


# process3 = Process("Proceso 3", [])


# process3.add_task(Task("task 3.1", 3))
# process3.add_task(Task("task 3.2", 3))

# process2.next_process = process3


# simulator.add_process(process1)
# simulator.add_process(process2)
# simulator.add_process(process3)

# simulator.set_products_number(2)




# while(True):
#     simulator.next_tick()
#     input("Enter enter to continue: ")


from tkinter.ttk import *
import tkinter as tk
from tkinter import messagebox
from logic.process import Process
from logic.task import Task
from logic.simulator import Simulator
import time 
import threading
from tkinter import simpledialog


class ProcessContainer(tk.Frame):
    def __init__(self, master, title, tasks: list[Task], **kwargs):
        super().__init__(master, relief="raised", bd=2, padx=10, pady=5, **kwargs)

        self.title_label = Label(self, text=title, font=("Arial", 12, "bold"), padding=(5, 5))
        self.title_label.pack(pady=(0, 5))


        self.task_labels = []
        for task in tasks:
            background = "lightgreen" if task.is_processing() else "#aba7a7"
            product_text = f"\n Product: \n {task.current_product.name if task.is_processing() else "None"}"
            label = tk.Label(self, text=f"Nombre: {task.name} {product_text}" , width=12, background=background, foreground="#000000", font=("Arial", 11), borderwidth=2)
            label.pack(pady=20)
            self.task_labels.append(label)


class createProcessModal(tk.Toplevel):
    def __init__(self, master, create_process_cb):
        super().__init__(master)
        self.title("Crear nuevo proceso")
        self.geometry("550x400")
        self.on_save_callback = create_process_cb

        self.process_name_var = tk.StringVar()
        self.task_name_var = tk.StringVar()
        self.task_time_var = tk.IntVar()
        self.tasks = []

        Label(self, text="Nombre del Proceso:").pack(pady=5)
        self.name_entry = Entry(self, textvariable=self.process_name_var)
        self.name_entry.pack(fill="x", padx=10)

        Label(self, text="Agregar Tarea:").pack(pady=(10, 0))
        task_frame = Frame(self)
        task_frame.pack(fill="x", padx=10)

        self.task_name = Entry(task_frame, textvariable=self.task_name_var)
        self.task_name.pack(side="left", fill="x", expand=True)

        self.task_time = Entry(task_frame, textvariable=self.task_time_var)
        self.task_time.pack(side="left", fill="x", expand=True)

        add_button = Button(task_frame, text="Agregar", command=self.add_task)
        add_button.pack(side="right", padx=5)

        columnas = ("#1", "#2")
        self.tree = Treeview(self, columns=columnas, show="headings")
        self.tree.heading("#1", text="Nombre")
        self.tree.heading("#2", text="Tiempo de procesamiento")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        save_button = Button(self, text="Guardar Proceso", command=self.add_process)
        save_button.pack(pady=10)

    def add_task(self):
        task_name = self.task_name_var.get().strip()
        task_time = self.task_time_var.get()
        if task_name and task_time:
            self.tree.insert("", tk.END, values=(task_name, task_time))
            self.tasks.append(Task(task_name, task_time))
            self.task_name_var.set("")
            self.task_time_var.set(0)

    def add_process(self):
        name = self.process_name_var.get().strip()
        if name and len(self.tasks) != 0:
            self.on_save_callback(Process(name, self.tasks))
            self.destroy()
        else:
            messagebox.showwarning("Campos incompletos", "Debes ingresar un nombre y al menos una tarea.")


class SummaryModal(tk.Toplevel):
    def __init__(self, master, summary):
        super().__init__(master)
        self.title("Resumen de la ejecución")
        self.geometry("550x400")
        self.grab_set() 


        title = tk.Label(self, text="Reportes Generados", font=("Arial", 14, "bold"))
        title.pack(pady=10)


        columns = ("#1", "#2")
        table = Treeview(self, columns=columns, show="headings")

        table.heading("#1", text="Criterio")
        table.heading("#2", text="Valor")

        for key, value in summary.items():
            table.insert("", tk.END, values=(key, value))

        table.pack(fill="both", expand=True, padx=20, pady=10)

        Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Línea de Producción")

        self.root.geometry("800x1000")
        self.simulator = Simulator()
        self.processes = []

        self.sim_thread = None
        self.stop = False 
        self.pause = False

        self.create_widgets()

    """
            WIDGETS
    """
    def create_widgets(self):

        control_frame = Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky="ew")

        self.start_button = Button(control_frame, text="Iniciar", command=self.start_simulation)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = Button(control_frame, text="Pausar", command=self.pause_simulation)
        self.pause_button.grid(row=1, column=0, padx=5)

        self.reset_button = Button(control_frame, text="Reiniciar", command=self.restart_simulation)
        self.reset_button.grid(row=0, column=1, padx=5)

        self.create_process_button = Button(control_frame, text="Agregar proceso", command=self.open_proces_modal)
        self.create_process_button.grid(row=1, column=1, padx=5)

        self.time = Label(self.root, text=f"Tiempo: {self.simulator.current_time}", font=("Arial", 20, "bold"))
        self.time.grid(row=1, padx=10, pady=30)

        self.container = tk.Frame(self.root)
        self.container.grid(row=2, column=0, sticky='ew')

        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def update_widgets(self):

        self.time.config(text=f"Tiempo: {self.simulator.current_time}")

        for i, process in enumerate(self.simulator.processes):
            block = ProcessContainer(self.container, process.name, process.tasks, bg="#ffffff")
            block.grid(row=0, column=i, padx=10, pady=20)
            self.processes.append(block) 
    

    def add_process(self, process):
        self.simulator.add_process(process)
        self.simulator.final_process = process
        self.update_widgets()

    """
        Simulation control
    """

    def __start_simulation(self, stop, pause, show_summary_cb):
        while(True):
            if(pause()):
                # Continue to the next iteration if user pauses the simularion
                continue
            if(stop() or self.simulator.has_finish()):
                # Break the loop if user stop the simulation
                if(self.simulator.has_finish()):
                    show_summary_cb()
                break
            self.simulator.next_tick()
            self.update_widgets()
            time.sleep(2)

    def stop_thread(self):
        self.stop = True
        self.sim_thread.join()


    def ask_products(self):
        user_input = int(simpledialog.askstring("Antes de comenzar", "Ingrese una cantidad de productos: "))
        self.simulator.set_products_number(int(user_input))
        

    def start_simulation(self):
        self.simulator.reset()
        if(len(self.simulator.processes) == 0):
            messagebox.showwarning("No se puede comenzar la simulacion", "Debe existir al menos 1 proceso")
            return
        
        self.ask_products()

        self.update_widgets()
                
        self.start_button.config(state="disabled")
        self.sim_thread = threading.Thread(target=self.__start_simulation, args=(lambda : self.stop, lambda: self.pause, self.show_summary, ))
        self.sim_thread.start()


    def pause_simulation(self):

        if(self.pause):
            self.pause_button.config(text="Pausar")
            self.pause = False 
        else:
            self.pause_button.config(text="Reanudar")
            self.pause = True

    def restart_simulation(self):
        self.stop_thread()
        self.stop = False
        self.pause = False
        self.simulator = Simulator()
        
        for process in self.processes:
            process.destroy()

        self.processes = []
        self.update_widgets()

    def show_summary(self):
        summary = self.simulator.summary()
        SummaryModal(self.root, summary)

    def open_proces_modal(self):
        createProcessModal(self.root, self.add_process)


# Ejecutar la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = UI(root)
    root.mainloop()



