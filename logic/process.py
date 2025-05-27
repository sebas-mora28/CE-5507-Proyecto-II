from logic.task import Task
from logic.product import Product

class Process:

    def __init__(self, name: str, tasks: list[Task] = []):
        self.name: str = name
        self.tasks: list[Task] = tasks
        self.next_process: Process = None
        self.processed_products = 0


    def add_task(self, task: Task):
        self.tasks.append(task)

    def add_product(self, product: Product):
        if(len(self.tasks) == 0):
            raise Exception("No se puede agregar el producto. No existen tareas asociadas al proceso")
        self.tasks[0].enqueue_product(product)

    
    def reset(self):
        for task in self.tasks:
            task.reset()
    
    def run(self, current_time: int):
        print(f"-----------------{self.name} ----------------------")
        for i, task in enumerate(reversed(self.tasks)):
            product = task.process()

            if not product:
                continue

            is_last_task = i == 0
   
            if(is_last_task):
                if (self.next_process):
                    print(f"Producto {product.name} se mueve al sigueinte proceso [{self.next_process.name}]")
                    self.processed_products += 1
                    self.next_process.add_product(product)
                else:
                   print(f"Producto terminado {product.name}")
                   # Si no hay un siguiente proceso, quiere decir que el producto llegó al final de la linea de produccion
                   product.finish_product(current_time)

            else:
                print(f"El producto [{product.name}] se mueve a la siguiente tarea [{self.tasks[::-1][i-1].name}]")
                self.tasks[::-1][i-1].enqueue_product(product)

        print("----------------------------------------------\n")
                
            

            