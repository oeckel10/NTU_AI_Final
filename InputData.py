import json
import pandas as pd

class InputData:

    def __init__(self, path):
        #Eingabe des Verzeichnisses der Touren-Daten
        self.path = path
        self.DataLoad()

    def DataLoad(self):
        var = ['Test instances']
        var.append(self.path)

        #Eingabe des Verzeichnisses der Touren-Daten
        path = '\\'.join(var)

        #Einlesen der Daten aus der Touren-Daten-Datei und abspeichern in Variable "data"
        with open(path) as f:
            inputData = json.load(f)

        #Abspeichern der Wegematrix
        self.data = inputData['Distances']

        #Generierung eines Arrays mit den Zahlen 0-(Anzahl Punkte im Tourenplan) zur Achsenbeschriftung, um eindeutiger und einfacher Matrix nachvollziehen zu können
        axis = [i for i in range(len(self.data[0]))]

        #Erstellung einer Matrix mittels Pandas-DataFrame, da mit diesem Kontrukt relativ leicht gearbeitet werden kann
        self.matrix = pd.DataFrame()
        for row in self.data:
            self.matrix = pd.DataFrame(self.data, columns = axis, index = axis) #Einfügen der Daten mit Beschriftung der Achsen x,y