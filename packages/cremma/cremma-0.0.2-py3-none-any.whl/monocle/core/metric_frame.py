import pandas as pd

class Metric():
    
    def __init__(self, filters=dict(), formulas=dict()):
        self.filters = filters
        self.formulas = formulas
    
    def generate(self):
        for formula in self.formulas :
            pass