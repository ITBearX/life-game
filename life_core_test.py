#!/usr/bin/python

from life_core import LifeGrid

life = LifeGrid(5, 5)
print('Created an empty one:\n', life)

life.rand()
print('Filled it with random values:\n', life)

life.resize(8, 3)
print('Resized it:\n', life)

print('Cell 1,2:', life[1, 2])
life[1, 2] = not life[1, 2]
print('Cell 1,2 after flip:', life[1, 2])
print(life)

print('Neighbourhood type:', life.nbr_func.__name__)
print('Neighbourhood:\n', life.nbr_func())

life.next_gen()
print('New generation:\n', life)
