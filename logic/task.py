from logic.product import Product
from queue import Queue

class Task: 

    def __init__(self, name: str, processing_time: int):

        self.name: str = name
        self.queued_products: Queue[Product] = Queue()
        self.processing_time: int = processing_time
        self.is_busy: bool = False
        self.current_product: Product = None

        self.time_count: int = 0

    def enqueue_product(self, product: Product):
        self.queued_products.put(product)


    def reset(self):
        self.time_count = 0
        self.queued_products = Queue()
        self.current_product = None
        self.is_busy = False
        self.cumulative_waiting_time = 0


    def is_processing(self):
        return self.current_product != None


    def process(self):
        print(self.queued_products.empty())
        if(self.queued_products.empty() and not self.is_busy):
            # No hay productos encolados, la tarea continua esperando
            print(f"Tarea [{self.name}] no tiene elementos pendientes para procesar")
            return
            
        if(self.is_busy):
            self.time_count += 1  # Se aumenta el tiempo actual de la tarea
            if(self.time_count == self.processing_time):
                # La tarea ahora esta disponible y se devuelve el producto
                print(f"Tarea [{self.name}] ha terminado el producto [{self.current_product.name}] ({self.time_count}/{self.processing_time})")
                self.is_busy = False
                self.time_count = 0
                processed_product = self.current_product
                self.current_product = None
                return processed_product
            
            # La tarea se encuentra procesando 
            print(f"Tarea [{self.name}] está ocupada ({self.time_count}/{self.processing_time})")
            return None
                       
        self.current_product = self.queued_products.get()
        self.is_busy = True
        self.time_count += 1
        print(f"Tarea [{self.name}] ha comenzando un nuevo producto [{self.current_product.name}]")  
        return None


        
        

            




    

    