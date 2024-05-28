from copy import deepcopy
from timeit import default_timer

from InputData import *
from OutputData import *
from EvaluationLogic import *

class Solver:

    def __init__(self, path):
        self.path = path  
        self.solutPoool = [] #Langzeitgedächtnis, nimmt langfristig alle lokal besten Lösungen auf
        

    def generateNeighboorhood(self, firstSolution, matrix, tabuList, type = 'swap', maxIterations=10000):
        self.matrix = matrix
        self.firstSolution = firstSolution
        self.type = type
        self.maxIterations = maxIterations
        self.tabuList = tabuList
        localBestSolution = []
        it=0
        #Aspirationskriterium initialisiert mit einem maximalen Wert und bei einer Verbesserung wird die List überschrieben
        aspirationskriterium = [EvaluationLogic().SolutionFinder(deepcopy(firstSolution), self.matrix), deepcopy(firstSolution)]
        

        if type == "swap": #swap Nachbarschaft wird gestartet
            localBestSolution.clear()

            for i in range(1, len(self.firstSolution)-1):
                for j in range(1, len(self.firstSolution)-1):
                    if it == self.maxIterations:
                        break
                    else:
                        it+=1
                        if i < j:
                            indexA = j
                            indexB = i
                            nextSolution = list(self.firstSolution) # create a copy of the permutation

                            #swap der Punkte an den indice STellen wird vorgenommen
                            nextSolution[indexA] = deepcopy(self.firstSolution[indexB])
                            nextSolution[indexB] = deepcopy(self.firstSolution[indexA])

                            tauschKombi = (i, j)
                            
                            #Abgleich mit TabuListe ODER Aspirationskriterium ist wahr, falls aktuelle Lösung besser als alle bisher, wird aspirationskriterium upgedated
                            if (tauschKombi not in self.tabuList) or (EvaluationLogic().SolutionFinder(deepcopy(nextSolution), self.matrix) < aspirationskriterium[0])==True:
                                    localBestSolution.append(nextSolution)
                                    if aspirationskriterium[0] > EvaluationLogic().SolutionFinder(nextSolution, self.matrix):
                                        aspirationskriterium[0] = EvaluationLogic().SolutionFinder(nextSolution, self.matrix)
                                        aspirationskriterium[1] = nextSolution
            
            #durchsuchen der localBestSolution Liste nach der besten lokalen Lösung der Nachbarschaft
            zwischenSpeicher = []
            for i in localBestSolution:
                zwischenSpeicher.append(EvaluationLogic().SolutionFinder(deepcopy(i), self.matrix))

            index_min = min(range(len(zwischenSpeicher)), key=zwischenSpeicher.__getitem__) #Suche nach dem Index mit dem geringsten Lösungswert
            singleLocalBestSolution = deepcopy(localBestSolution[index_min])

            #print(f'eine Weglänge von {EvaluationLogic().SolutionFinder(deepcopy(singleLocalBestSolution), self.matrix)} über {singleLocalBestSolution} wurde mit swap erreicht')
            return singleLocalBestSolution

        elif type == 'insertion': #insertion Nachbarschaft wird gestartet
            nextPermut = []
            nextPermuts = []
            localBestSolution.clear()
            firstSolutio = deepcopy(self.firstSolution)

            for i in range(1, len(firstSolutio)-1):
                for j in range(1, len(firstSolutio)-1):
                    if it == self.maxIterations:
                        break
                    if i == j or i == j + 1:
                        continue
                    elif i<j:
                        it+=1
                        nextPermuts.clear()
                        nextPermut.clear()
                        indexA = deepcopy(i)
                        indexB = deepcopy(j)

                        for k in range(len(firstSolutio)):
                            if k == i:
                                continue
                            nextPermut.append(deepcopy(firstSolutio[k]))
                        nextPermut.insert(indexB, deepcopy(firstSolutio[i]))
                        tauschKombi = (i, j) #TauschKombination, die am Ende an die TabuListe weitergegeben wird
                        nextPermuts = [nextPermut, tauschKombi] #Liste besteht aus nächster Permutation und TauschKombination, da die tauschKombi an TabuSearch zurückgegeben werden muss, um TabuListe zu ergänzen

                        #Abgleich mit TabuListe ODER Aspirationskriterium ist wahr, falls aktuelle Lösung besser als alle bisher, wird aspirationskriterium upgedated
                        if (tauschKombi not in self.tabuList) or (EvaluationLogic().SolutionFinder(nextPermuts[0], self.matrix) < aspirationskriterium[0])==True:
                            localBestSolution.append(deepcopy(nextPermuts))
                            nextSolu = EvaluationLogic().SolutionFinder(nextPermuts[0], self.matrix)
                            if aspirationskriterium[0] > nextSolu:
                                aspirationskriterium[0] = nextSolu
                                aspirationskriterium[1] = nextPermuts[0]

            #durchsuchen der localBestSolution Liste nach der besten lokalen Lösung der Nachbarschaft
            zwischenSpeicher = []
            localBestSolution2 = [item[0] for item in localBestSolution] #rausfiltern der TauschKombination, die an die jeweilige Permutation angeknüpft wurde, um eine List mit ausschließlich Permutationen zu errechnen -> beste lokale Lösungssuche
            for i in localBestSolution2:
                zwischenSpeicher.append(EvaluationLogic().SolutionFinder(deepcopy(i), self.matrix))

            index_min = min(range(len(zwischenSpeicher)), key=zwischenSpeicher.__getitem__) #Suche nach dem Index mit dem geringsten Lösungswert
            singleLocalBestSolution = deepcopy(localBestSolution[index_min])

            #print(f'eine Weglänge von {EvaluationLogic().SolutionFinder(deepcopy(singleLocalBestSolution[0]), self.matrix)} über {singleLocalBestSolution[0]} wurde mit insertion erreicht')
            return singleLocalBestSolution 

        #else:
                #print('Bitte enscheiden Sie sich zwischen swap und insertion!')     

    def tabuSearch(self, firstSolution, matrix, path, maxTabuListLength=5, maxIterations = 500):
        self.firstSolution = firstSolution
        self.matrix = matrix
        self.path = path
        tabuList = [] #Kurzzeitgedächtnis, nimmt entsprechend des Parameters eine gewisse Anzahl von durchgeführten Tauschen auf, die danach verboetn werden, bis sie rausgelöscht werden
        Solution = deepcopy(firstSolution) #Startwert der ersten Iteration
        self.solutPoool.append(deepcopy(firstSolution)) #Startlösung dem Langzeitgedächtnis aka LösungsPool hinzufügen
        self.maxTabuListLength = maxTabuListLength
        self.maxIterations = maxIterations
        time_needed=default_timer() #starte Zeitabgleich/Timer
        timer = 0
        iteration = 1
        tauschKombination = []
        xtauschKombination = []

        if len(self.matrix[0])<50: #Vorgabe der Rechenzeit abzüglich Pauschal Erfahrungswert an Sekunden zur Beendigung der letzten Iteration und Durchsuchung des Langzeitgedächtnisses nach der besten Lösung
            maxTabuSearchTime = 10
        else:
            maxTabuSearchTime = 280
        
        while timer < maxTabuSearchTime: #Abbruchkriterium in Form eines Zeittimers
            #print(f"\nTabu-Search, Iteration {iteration}")
            iteration+=1
            
            #durchsuche beide Nachbarschaften nach der besten Lösung, die nicht auf tabuList ist ODER aspirationskriterium erfüllt
            di = self.generateNeighboorhood(deepcopy(Solution), self.matrix, tabuList, type='swap', maxIterations=self.maxIterations)
            ds = self.generateNeighboorhood(deepcopy(Solution), self.matrix, tabuList, type='insertion', maxIterations=self.maxIterations)
            
            #Auswertung der Ergebnisse
            if EvaluationLogic().SolutionFinder(di, self.matrix) <= EvaluationLogic().SolutionFinder(ds[0], self.matrix):#falls swap Ergebnis besser oder gleich insertion Ergebnis ist:   
                tauschKombination = []

                for index, (first, second) in enumerate(zip(Solution, di)): #herausfinden, welche Tausche gemacht wurden, dazu wird die letzte Lösung mit der neuen Lösung verglichen und geänderte Stellen in tauschKombination gespeichert
                    if first != second:
                        tauschKombination.append(index)

                xtauschKombination = tauschKombination[0], tauschKombination[1] #Liste wird in Tupel konvertiert, um eindeutig zuordnen zu können
                tabuList.append(xtauschKombination) #Kurzzeitgedächtnis erweitern mit letztem Tupel
                Solution=deepcopy(di) #Startwert der kommenden Iteration
                self.solutPoool.append(deepcopy(Solution)) #dem Langzeitgedächtnis die lokale beste Lösung hinzufügen

            else: #insertion Wert war besser
                tauschKombination = deepcopy(ds[1]) #beste Tauschkombination ist an der zweiten Stelle der Rückgabeliste gepseichert (Besonderheit im Vergleich zu swap)
                tabuList.append(tauschKombination) #Kurzzeitgedächtnis erweitern mit letztem Tupel
                
                Solution=deepcopy(ds[0]) #Startwert der kommenden Iteration
                self.solutPoool.append(deepcopy(Solution))  #dem Langzeitgedächtnis die lokale beste Lösung hinzufügen

            timer = default_timer() - time_needed #Timer aktualisieren


            while len(tabuList) > self.maxTabuListLength: #wenn TabuListe länger als Vorgabewert, lösche den ältesten Eintrag an erster Stelle
                tabuList.pop(0)

        #Abbruchkriterium wurde erreicht, Zeit ist abgelaufen: durchsuche gesamten LangzeitGedächtnis - Lösungsraum
        zwischenSpeicher = []
        for i in self.solutPoool:
            zwischenSpeicher.append(EvaluationLogic().SolutionFinder(i, self.matrix)) #errechne für alle in SolutionPool enthaltenen Lösungen die Weglänge

        index_min = min(range(len(zwischenSpeicher)), key=zwischenSpeicher.__getitem__) #Suche nach dem Index mit dem geringsten Lösungswert
        bestFinalSolution = deepcopy(self.solutPoool[index_min]) #die gesamte-beste Lösung

        #print(f'\nDie beste globale Lösung der MetaHeuristik ist {bestFinalSolution} mit {EvaluationLogic().SolutionFinder(deepcopy(bestFinalSolution), self.matrix)}.')
        #print(f'Dafür hat die MetaHeuristik {timer} Sekunden an Rechenzeit benötigt.')

        outputAlgorithm(bestFinalSolution, self.matrix, self.path).startOutput() #starte Output auf Basis der gesamt-besten Lösung
        
        return bestFinalSolution