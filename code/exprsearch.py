import csv
from plot import Plot

unaries = ["log", "sqrt", "exp"]
binaries = ["+", "-", "*", "/", "**"]

def alluryexpr(feature, expr):
    uryexpr = ["v['" + feature + "']"]
    for unary in unaries:
        if expr:
            uryexpr.append(unary + "(" + feature + ")")
        else:
            uryexpr.append(unary + "(v['" + feature + "'])")
    return uryexpr

class Exprsearch:
    def __init__(self, ftrs):
        self.features = ftrs
        self.count = 0
        self.best = Plot("","")
        
    def testExpr(self, x, y, data):
        flag = False
        plot = Plot(x, y)
        try:
            plot.setData(self.features, data)
            score = plot.calculateScore2()
        except:
            return flag
        self.count = self.count + 1
        if score > self.best.score:
            self.best = plot
            print(self.best.score)
            flag = True
        print("Expr " + str(self.count) + ":" + str((x, y)) + "\t" + str(score))
        print("\tCurrent best" + str(self.best.expr) + "\t" + str(self.best.score))
        return flag

    def pairSearch(self, data):
        for i in range(len(self.features)):
            for j in range(i + 1, len(self.features)):
                for iexpr in alluryexpr(self.features[i], False):
                    for jexpr in alluryexpr(self.features[j], False):
                        self.testExpr(iexpr, jexpr, data)
    
    def tripleSearch(self, data):
        (x, y) = self.best.expr
        remainForReturn = None
        for feature in self.features:
            if feature in x or feature in y:
                continue
            for expr in alluryexpr(feature, False):
                for binary in binaries:
                        if self.testExpr(x + binary + expr, y, data):
                            remainForReturn = 'r'
                        if self.testExpr(expr + binary + x, y, data):
                            remainForReturn = 'r'
                        if self.testExpr(x, y + binary + expr, data):
                            remainForReturn = 'l'
                        if self.testExpr(x, expr + binary + y, data):
                            remainForReturn = 'l'
        return remainForReturn
    
    def quadrupleSearch(self, data, remain):
        (x, y) = self.best.expr
        for feature in self.features:
            if feature in x or feature in y:
                continue
            for expr in alluryexpr(feature, False):
                for binary in binaries:
                    if remain != 'r':
                        self.testExpr(x + binary + expr, y, data)
                        self.testExpr(expr + binary + x, y, data)
                    if remain != 'l':
                        self.testExpr(x, y + binary + expr, data)
                        self.testExpr(x, expr + binary + y, data)
    
    def search(self,data):
        self.pairSearch(data)
        remain = self.tripleSearch(data)
        self.quadrupleSearch(data, remain)
        #for x in alluryexpr(self.best.expr[0], True):
            #for y in alluryexpr(self.best.expr[1], True):
                #self.testExpr(x, y, data)
        return self.best
    
with open('seeds_dataset.txt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter = '\t')
    data = []
    for row in spamreader:
        if '?' not in row:
            data.append(row)
    #p = Plot("log(v['area A'])+sqrt(v['compactness'])", "log(v['length of kernel groove'])")
    #p.setData(data[0],data[1:])
    #p.plotData()
    search = Exprsearch(data[0])
    best = search.search(data[1:])
    best.plotData()
    
    
