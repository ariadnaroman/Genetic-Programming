import random
import csv
from math import *
import numpy as np

MAX_DEPTH = 5
FUNCTION_SET = ["+", "-", "*", "sin", "cos"]
TERMINAL_SET = [0, 1, 2, 3, 4, 5]


class Chromosome:
    def __init__(self):
        self.representation = []
        self.fitness = 0.0

    def full(self, crtDepth):
        if crtDepth == MAX_DEPTH:
            terminal = random.choice(TERMINAL_SET)
            self.representation.append(terminal)
        elif crtDepth < MAX_DEPTH:
            function = random.choice(FUNCTION_SET)
            self.representation.append(function)
            if function == "sin" or function == "cos":
                self.full(crtDepth + 1)
            else:
                self.full(crtDepth + 1)
                self.full(crtDepth + 1)

    def eval(self, inExample, pos):
        if self.representation[pos] in TERMINAL_SET:
            return inExample[self.representation[pos]]
        elif self.representation[pos] in FUNCTION_SET:
            if self.representation[pos] == "+":
                pos += 1
                left = self.eval(inExample, pos)
                pos += 1
                right = self.eval(inExample, pos)
                return left + right
            elif self.representation[pos] == "-":
                pos += 1
                left = self.eval(inExample, pos)
                pos += 1
                right = self.eval(inExample, pos)
                return left - right
            elif self.representation[pos] == "*":
                pos += 1
                left = self.eval(inExample, pos)
                pos += 1
                right = self.eval(inExample, pos)
                return left * right
            elif self.representation[pos] == "sin":
                pos += 1
                elem = self.eval(inExample, pos)
                return sin(elem)
            elif self.representation[pos] == "cos":
                pos += 1
                elem = self.eval(inExample, pos)
                return cos(elem)

    def __str__(self):
        return str(self.representation)

    def __repr__(self):
        return str(self.representation)


def init(pop, popSize):
    for i in range(0, popSize):
        indiv = Chromosome()
        indiv.full(0)
        pop.append(indiv)


def transfer(value):
    return 1.0 / (1.0 + np.exp(-value))


def computeFitness(chromo, inData, outData):
    err = 0.0
    for i in range(0, len(inData)):
        crtEval = chromo.eval(inData[i], 0)
        crtEval = transfer(crtEval)
        crtErr = abs(crtEval - outData[i]) ** 2
        err += crtErr
    chromo.fitness = err/len(inData)


def evalPop(pop, trainInput, trainOutput):
    for indiv in pop:
        computeFitness(indiv, trainInput, trainOutput)


def selection(pop):
    pos1 = random.randrange(len(pop))
    pos2 = random.randrange(len(pop))
    if pop[pos1].fitness < pop[pos2].fitness:
        return pop[pos1]
    else:
        return pop[pos2]


def selectionRoulette(pop):
    sectors = [0]
    sum = 0.0
    for chromo in pop:
        sum += chromo.fitness
    for chromo in pop:
        sectors.append(chromo.fitness / sum + sectors[len(sectors) - 1])

    print(sectors)
    r = random.random()
    i = 1
    while (i < len(sectors)) and (sectors[i] <= r):
        i += 1
    return pop[i - 1]


def mutation(off):
    pos = random.randrange(len(off.representation))
    if off.representation[pos] in TERMINAL_SET:
        terminal = random.choice(TERMINAL_SET)
        off.representation[pos] = terminal
    elif off.representation[pos] in FUNCTION_SET:
        if off.representation[pos] == "+" or off.representation[pos] == "-" or off.representation[pos] == "*":
            function = random.choice(["+", "-", "*"])
        else:
            function = random.choice(["sin", "cos"])
        off.representation[pos] = function
    return off


def bestSolution(pop):
    best = pop[0]
    for indiv in pop:
        if indiv.fitness < best.fitness:
            best = indiv
    return best


def GP_generational(popSize, noGenerations, trainIn, trainOut, maxDepth):
    global MAX_DEPTH
    MAX_DEPTH = maxDepth
    pop = []
    init(pop, popSize)
    evalPop(pop, trainIn, trainOut)
    for g in range(0, noGenerations):
        popAux = []
        for k in range(0, popSize):
            M = selection(pop)
            off = mutation(M)
            popAux.append(off)
        pop = popAux.copy()
        evalPop(pop, trainIn, trainOut)
    sol = bestSolution(pop)
    return sol


def GP_steadyState(popSize, noGenerations, trainIn, trainOut, maxDepth):
    global MAX_DEPTH
    MAX_DEPTH = maxDepth
    pop = []
    init(pop, popSize)
    evalPop(pop, trainIn, trainOut)
    for g in range(0, noGenerations):
        for k in range(0, popSize):
            M = selection(pop)
            off = mutation(M)
            computeFitness(off, trainIn, trainOut)
            crtBest = bestSolution(pop)
            if off.fitness < crtBest.fitness:
                crtBest = off
    return crtBest


