import itertools
expression = "(-{}+{}/{})/({}-{}/{})"
numbersList = [1,2,3,4,5,6]
integer = True


solutions = {}
for comb in itertools.permutations(numbersList):
    try:
        res = eval(expression.format(*comb))
        if res == int(res):
            solutions[comb] = res
    except ZeroDivisionError:
        continue


for e in sorted(solutions.items(), key=lambda x:x[1]):
    print(e)
    
