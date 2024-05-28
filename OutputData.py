import csv
from EvaluationLogic import *
import os

class outputAlgorithm:
    def __init__(self, order_final, matrix, path):
        self.order_final = order_final
        self.matrix = matrix
        self.path = path

    def startOutput(self):

        if not os.path.exists('Solutions'):
            os.mkdir('Solutions')

        #Einführen von Zählvariablen zur Vorbereitung des Outputs der Lösung
        zaehlvar = 1
        writer_path = 'Solutions\Solution-' + self.path.replace('.json', '') + '.csv' #Generieren des Output-Paths auf Basis der Input-Datei, dabei muss die Dateiendung der Input-Datei gelöscht werden
        cum_sum = 0 #Einführen der kumulierten Summe zum Abspeichern der CSV-Datei

        #Generierung einer neuen Datei oder Überschreibung einer bereits existierenden Lösung mit Feldnamen 'Id' und 'Distances'
        with open(writer_path, 'w', newline='') as file: #'w' damit vorhandene Datei überschrieben/resettet wird, newline = '' damit keine Absätze nach jeder Zeile generiert werden
            dw = csv.DictWriter(file, delimiter=';', fieldnames=['Id', 'Distance']) #Trennungszeichen ';' eingeführt und Feldnamen eingegeben
            dw.writeheader()

        #Output/CSV-Generierung mithilfe der besten Lösung/Permutation aus Solver-Algorithmus
        for i in self.order_final: #Für jedes Element der finalen Lösung wird der Weg nochmals nachvollzogen und in CSV-Datei exportiert. Beschreibung der Schleife siehe Solver
            if zaehlvar == len(self.matrix[0]):
                cum_sum = cum_sum + self.matrix.iloc[i, self.order_final[(zaehlvar)-1]]   #Beim ersten Abbruchkriterium aufgrund des letzten Elementes des Arrays muss (order_final[(zaehlvar)-1) gecoded werden, 
                                                                                #da als letzte Instanz in der vorherigen Iteration die (zaehlvar) um eins erhöht wurde und dies rückgängig gemacht werden muss

                with open(writer_path, mode='a', newline='') as file: #mode='a' damit die bereits existierende CSV-Datei nur erweitert (appended) wird. Ein 'w' würde alle bisherigen Einträge löschen
                    write_row = csv.writer(file, delimiter=';')
                    write_row.writerow([i, cum_sum])
                break
            elif self.matrix.iloc[i, self.order_final[zaehlvar]] == -1:
                with open(writer_path, mode='a', newline='') as file: #mode='a' damit die bereits existierende CSV-Datei nur erweitert (appended) wird. Ein 'w' würde alle bisherigen Einträge löschen
                    write_row = csv.writer(file, delimiter=';')
                    write_row.writerow(['Path is not valid']) #Abbruchkriterium falls 'ideale Lösung' des Solvers nicht erlaubt ist 
                zaehlvar +=1
                break    
            else:
                with open(writer_path, mode='a', newline='') as file: #mode='a' damit die bereits existierende CSV-Datei nur erweitert (appended) wird. Ein 'w' würde alle bisherigen Einträge löschen
                    write_row = csv.writer(file, delimiter=';')
                    write_row.writerow([i, cum_sum])

                cum_sum = cum_sum + self.matrix.iloc[i, self.order_final[zaehlvar]]
                zaehlvar += 1