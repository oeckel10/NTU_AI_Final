from EvaluationLogic import *
from InputData import *
import random
from copy import deepcopy
import math
pd.options.mode.chained_assignment = None

class BestStartSolution:
    def __init__(self, matrix, seed):
        self.matrix = matrix
        self.start_solution_pool = []
        self.zwischenspeicher = []
        self.seed = seed

    def generate_best_start_solution(self):
        # Generate FirstComeFirstServe Solution
        fcfs = list(range(len(self.matrix)))
        self.start_solution_pool.append(deepcopy(fcfs))

        # Generate random solutions, 200 reproducible random numbers with seed
        random.seed(self.seed)
        random_numbers = [random.randint(0, 10000) for _ in range(200)]
        random_zwischenspeicher = []

        for i in random_numbers:  # Use all numbers as different seeds
            axis = list(range(len(self.matrix[0])))
            axis.remove(0)
            axis.remove(len(self.matrix[0]) - 1)
            size = len(self.matrix)

            first_order = random.sample(axis, len(self.matrix[0]) - 2)
            order = [0] + first_order + [size - 1]

            if not random_zwischenspeicher:
                random_zwischenspeicher.append(order)
            else:
                if EvaluationLogic().SolutionFinder(order, self.matrix) < EvaluationLogic().SolutionFinder(random_zwischenspeicher[-1], self.matrix):
                    random_zwischenspeicher.append(order)

        self.start_solution_pool.append(deepcopy(random_zwischenspeicher[-1]))

        # Generate ShortestProcessingTime
        matrice = deepcopy(self.matrix)

        for i in range(len(matrice[0]) - 1):
            matrice.iloc[i,i] = math.inf  # Prevent visiting the same point
        matrice.replace(-1, math.inf, inplace=True)  # Set impossible path lengths to infinity

        reihenfolge = []
        zeile = 0
        i = 0

        matrice.drop(matrice.tail(1).index, inplace=True)
        matrice = matrice.iloc[:, :-1]
        length = len(matrice[0] - 1)

        while i < (length - 1):  # Search for the best successor with the lowest path evaluation for each row
            matrice.iloc[zeile].idxmin()
            zeile_alt = deepcopy(zeile)
            reihenfolge.append(matrice.loc[zeile].idxmin())

            zeile = matrice.loc[zeile].idxmin()
            del matrice[zeile_alt]  # Delete visited point from matrix (column)
            i += 1

        reihenfolge.append(len(matrice))
        reihenfolge.insert(0, 0)

        self.start_solution_pool.append(deepcopy(reihenfolge))

        # Return the best solution
        if EvaluationLogic().SolutionFinder(self.start_solution_pool[0], self.matrix) <= EvaluationLogic().SolutionFinder(self.start_solution_pool[1], self.matrix) and \
           EvaluationLogic().SolutionFinder(self.start_solution_pool[0], self.matrix) <= EvaluationLogic().SolutionFinder(self.start_solution_pool[2], self.matrix):
            return self.start_solution_pool[0]
        elif EvaluationLogic().SolutionFinder(self.start_solution_pool[1], self.matrix) <= EvaluationLogic().SolutionFinder(self.start_solution_pool[0], self.matrix) and \
             EvaluationLogic().SolutionFinder(self.start_solution_pool[1], self.matrix) <= EvaluationLogic().SolutionFinder(self.start_solution_pool[2], self.matrix):
            return self.start_solution_pool[1]
        else:
            return self.start_solution_pool[2]
