import math

class EvaluationLogic:

    def __init__(self):
        self.path_sum = 0

    def SolutionFinder(self, order, matrix):    
    #Einführen von Lauf-/Zählvariablen
        self.path_sum = 0 #Gibt die Summe der Wegkosten an
        i = 0 #Iteriert wird über jedes Element des wieder zusammengesetzten Arrays order
        zaehlvariable = 1   #Wird benötigt, um Abbruchkriterium einzubauen, da sonst ein Fehler geworfen wird, wenn Iteration beim letzten Element ist, da in for-Schleife die Wegkosten
                        #vom aktuellen Element zum nächsten Element im Array aufsummiert werden. Beim letzten Element im Array gibt es allerdings kein darauffolgendes Element.
                        #deshalb wird ein Abbruchkriterium 'if zaehlvariable == len(data[0])' eingebaut
                        #zudem dient sie zum anpeilen des nächsten Elements im array nach i -> siehe for-Schleife, Teil "else:..."

        for i in order: #über jedes Element im Array order iteriert
            if zaehlvariable == len(matrix[0]): #Abbruchkriterium
                break #wenn dies eintritt, wird for-Schleife abgebrochen und der Code außerhalb fortgesetzt
            elif matrix.iloc[i, order[zaehlvariable]] == -1: #Zweites Abbruchkriterium: wenn eine Verbindung eine Bewertun von '-1' hat, bedeutet dies, dass diese Verbindung unzulässig ist.
                self.path_sum = math.inf #wenn Verbindung unzulässig, wird den Wegkosten dieser Permutation der WErt Unendlich zugewiesen und for-Schleife abgebrochen, nächste Permutation wird gestartet
                break
            else: #wenn kein Abbruchkriterium erfüllt, wird folgender Code ausgeführt
                self.path_sum = self.path_sum + matrix.iloc[i, order[zaehlvariable]]  #Wegkosten werden kumuliert, indem zu den bisherigen Wegkosten die Kantenbewertung vom Punkt i zum darauffolgenden Punkt im Array addiert werden
                                                                        #hierbei muss allerdings der darauffolgende Punkt mit 'order[zaehlvariable]' angesprochen werden, da 'i+1' lediglich zur inkrementellen Erhöhung 
                                                                        #des Wertes i führt und nicht zur nächsten Stelle im Array. Dafür wurde die Zählvariable 'zaehlvariable' eingeführt
                zaehlvariable += 1 #Zählvariable inkrementell erhöhen, für nächsten Iterationsschritt
        return self.path_sum