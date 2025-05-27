

class Product():
    def __init__(self, name: str):
        self.name: str = name
        self.history = []
        self.end_time: int = None
        self.has_finish = False

    def finish_product(self, time):
        self.has_finish = True
        self.end_time = time 


        



        

