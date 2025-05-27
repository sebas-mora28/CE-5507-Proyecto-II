from logic.process import Process
from logic.product import Product
from time import sleep

class Simulator:

    def __init__(self):
        self.current_time = 0
        self.processes: list[Process] = []
        self.products: list[Product] = []
        self.final_process = None

    def add_process(self, process: Process):
        if(len(self.processes) != 0 ):
             self.processes[-1].next_process = process
        self.processes.append(process)


    def next_tick(self):
        print("Time: ", self.current_time + 1)
        for process in self.processes[::-1]:
                process.run(self.current_time)

        self.current_time += 1

    
    def has_finish(self):
        print("-------------------------\n")
        print(len(self.products))
        for product in self.products:
              print(product.name, "   ",  product.has_finish)
              if not(product.has_finish):
                   return False
        return True
    

    def summary(self):
         
        first_product_time = self.products[0].end_time
        last_product_time = self.products[-1].end_time

        total_products_time = sum(product.end_time for product in self.products) 
        average_products_time = total_products_time / len(self.products)
            
        return {
             "first_product_time": first_product_time,
             "last_product_time": last_product_time,
             "products_average_time": average_products_time,
             "total_products_time": total_products_time,
             "process_bottleneck": '',
             "process_with_longest_waitng_time": '',
             "task_with_longest_time": '' 
        }
              
    def reset(self):
         self.current_time = 0 
         for process in self.processes:
              process.reset()


    def set_products_number(self, products_number):
        for i in range(products_number):
            product = Product(f"Product-{i+1}")
            self.products.append(product)
            self.processes[0].add_product(product)
            

            






