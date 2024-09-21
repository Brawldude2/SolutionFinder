import itertools
import re
import numpy as np
from sympy import primefactors
from time import sleep
import time


SEARCH_MODE = "max"
VARIABLES_FILE = "Variables.txt"
CONDITIONS_FILE = "Conditions.txt"
RESULT_FILE = "Result.txt"

class Solver():
    def __init__(self):
        self.mode = "max" #Default search mode
        self.VarNames = list()
        self.Combinations = None
        self.ResultExpression = str()
        self.Conditions = list()
        self.Solutions = dict()
        self.SolutionsSorted = list()
        self.SolutionsOutput = str()

    def __str__(self):
        return self.SolutionsOutput

    def load(self):
        self.import_variables()
        self.import_conditions()

    def solve(self):
        solutions = dict()
        re = self.ResultExpression #Optimization reasons
        check = self.check_conditions #Optimization reasons
        for comb in self.Combinations:
            try:
                res = eval(re.format(*comb))
                if check(comb):
                    solutions[comb] = res
            except ZeroDivisionError:
                continue
        self.Solutions = solutions

    def output(self):
        self.apply_mode()
        self.SolutionsOutput = str()
        for solution in self.SolutionsSorted:
            template = ""
            VarValues = solution[0]
            result = solution[1]
            for _val,_name in zip(VarValues,self.VarNames): #Iterate over variable values and names
                template += _name + "=" + str(_val) + " "
            template += "    Sonuç=" + str(result) + "\n"
            self.SolutionsOutput += template
        self.SolutionsOutput += f"\n{len(self.Solutions)} solutions were found."

    def display(self):
        print(self)

    def save(self):
        with open(RESULT_FILE,"w") as f:
            f.write(self.SolutionsOutput)

    def set_mode(self,mode):
        self.mode = str(mode).lower()

    def apply_mode(self):
        if self.mode.lower() == "max":
            self._mode_max()
        if self.mode.lower() == "min":
            self._mode_min()
        if self.mode.lower() == "count":
            self._mode_count()

    def _mode_max(self):
        self.SolutionsSorted = sorted(self.Solutions.items(), key=lambda x:x[1],reverse=False)
    def _mode_min(self):
        self.SolutionsSorted = sorted(self.Solutions.items(), key=lambda x:x[1],reverse=True)

    def import_variables(self):
        var_ranges = list()
        var_names = list()
        with open(VARIABLES_FILE) as vf:
            lines = vf.readlines()
            for line in lines:
                _name,_range = line.split("|")[1:3]
                var_names.append(_name)
                _min,_max = _range.split(",")
                var_ranges.append(range(int(_min),int(_max)+1))
        self.VarNames = var_names
        self.Combinations = itertools.product(*var_ranges)

    def import_conditions(self):
        conditions = list()
        final_expression = str()
        with open(CONDITIONS_FILE) as cf:
            global SEARCH_MODE
            lines = cf.readlines()
            final_expression = self.convert_to_formattable_string(lines[0].split("|")[1],self.VarNames)
            SEARCH_MODE = lines[0].split("|")[2].lower()
            for line in lines[1:]:
                conditions.append(self.convert_to_formattable_string(line.split("|")[1],self.VarNames))
        self.ResultExpression = final_expression
        self.Conditions = conditions

    def convert_to_formattable_string(self,expression,var_names):
        formatted_string = expression
        for i,name in enumerate(var_names):
            formatted_string = re.sub(name,"{"+str(i)+"}",formatted_string)
        return formatted_string

    def check_conditions(self,comb):
        for c in self.Conditions:
            if not eval(c.format(*comb)):
                return False
        return True
        
now = time.time()
S = Solver()
S.load()
S.solve()
S.set_mode(SEARCH_MODE)
S.output()
S.display()
S.save()
print((time.time()-now)*1000," ms")

input("\nProgram başarıyla sonuçlandı. İşlemi kapatmak için Enter'a basın.")
