import csv
import geneticProgramming


class Console:

    def __showMenu(self):
        print("\n1. Genetic Programming Generational")
        print("2. Steady state\n")

    def __showSolveGenerational(self):
        def showError(error):
            print("\n", error, "\n")
            self.__showSolveEA()

        print("***************** GENETIC PROGRAMMING -> GENERATIONAL ******************\n")

        maxDepth = input("Max depth (d=5): ")
        popSize = input("Population size (d=10): ")
        noGenerations = input("Number of generations (d=10): ")

        if maxDepth == "d":
            maxDepth = 5
        if popSize == "d":
            popSize = 10
        if noGenerations == "d":
            noGenerations = 10

        try:
            maxDepth = int(maxDepth)
            popSize = int(popSize)
            noGenerations = int(noGenerations)
        except ValueError:
            showError("Incorrect values")

        if maxDepth > 20 or maxDepth < 3:
            showError("Max depth must be between 3 and 20")
        if popSize < 1:
            showError("Incorrect population size")
        if noGenerations < 1:
            showError("Incorrect number of generations")

        with open('column_2C.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            classificationDataTestInput = []
            classificationDataTestOutput = []
            classificationDataTrainInput = []
            classificationDataTrainOutput = []
            i = 0
            for row in spamreader:
                if row[-1] == 'Abnormal':
                    row[-1] = 1
                else:
                    row[-1] = 0

                for j in range(0, len(row) - 1):
                    row[j] = float(row[j])
                row[len(row) - 1] = int(row[len(row) - 1])

                if i < 60:
                    classificationDataTestInput.append(row[:-1])
                    classificationDataTestOutput.append(row[-1])
                else:
                    classificationDataTrainInput.append(row[:-1])
                    classificationDataTrainOutput.append(row[-1])
                i += 1
            learntModel = geneticProgramming.GP_generational(popSize, noGenerations, classificationDataTrainInput,
                                                             classificationDataTrainOutput, maxDepth)
            print("Model: " + str(learntModel))
            print("Training quality: ", learntModel.fitness)
            geneticProgramming.computeFitness(learntModel, classificationDataTestInput, classificationDataTestOutput)
            print("Testing quality: ", learntModel.fitness)

        print()

    def __showSolveSteadyState(self):
        def showError(error):
            print("\n", error, "\n")
            self.__showSolveEA()

        print("***************** GENETIC PROGRAMMING -> STEADY STATE ******************\n")

        maxDepth = input("Max depth (d=5): ")
        popSize = input("Population size (d=10): ")
        noGenerations = input("Number of generations (d=10): ")

        if maxDepth == "d":
            maxDepth = 5
        if popSize == "d":
            popSize = 10
        if noGenerations == "d":
            noGenerations = 10

        try:
            maxDepth = int(maxDepth)
            popSize = int(popSize)
            noGenerations = int(noGenerations)
        except ValueError:
            showError("Incorrect values")

        if maxDepth > 20 or maxDepth < 3:
            showError("Max depth must be between 3 and 20")
        if popSize < 1:
            showError("Incorrect population size")
        if noGenerations < 1:
            showError("Incorrect number of generations")

        with open('column_2C.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            classificationDataTestInput = []
            classificationDataTestOutput = []
            classificationDataTrainInput = []
            classificationDataTrainOutput = []
            i = 0
            for row in spamreader:
                if row[-1] == 'Abnormal':
                    row[-1] = 1
                else:
                    row[-1] = 0

                for j in range(0, len(row) - 1):
                    row[j] = float(row[j])
                row[len(row) - 1] = int(row[len(row) - 1])

                if i < 60:
                    classificationDataTestInput.append(row[:-1])
                    classificationDataTestOutput.append(row[-1])
                else:
                    classificationDataTrainInput.append(row[:-1])
                    classificationDataTrainOutput.append(row[-1])
                i += 1
            learntModel = geneticProgramming.GP_steadyState(popSize, noGenerations, classificationDataTrainInput,
                                                            classificationDataTrainOutput, maxDepth)
            print("Model: " + str(learntModel))
            print("Training quality: ", learntModel.fitness)
            geneticProgramming.computeFitness(learntModel, classificationDataTestInput, classificationDataTestOutput)
            print("Testing quality: ", learntModel.fitness)

        print()

    def startUi(self):
        self.__showMenu()
        option = input("Option: ")
        print()

        if option == "1":
            self.__showSolveGenerational()
        elif option == "2":
            self.__showSolveSteadyState()
        else:
            print("\nInvalid option!\n")
            self.startUi()


