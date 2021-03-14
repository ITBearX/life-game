#!/usr/bin/python

import life_core
from life_core import LifeGrid

life = LifeGrid((5, 5))
print("Created an empty one:\n", life)

life.rand()
print("Filled it with random values:\n", life)

life.resize((8, 3))
print("Resized it:\n", life)

print("Moore neighbourhood:\n", life.calcMoore())
print("von Neumann neighbourhood:\n", life.calcVonNeumann())

life.nextGen()
print("New generation:\n", life)
