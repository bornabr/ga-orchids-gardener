# Genetic Algorithm for the Orchids Gardener Problem

A gardener has 12 barrels of special liquid to irrigate his orchids. Exactly two barrels are poisonous. Using any amount, even a drop from a poisonous barrel destroys the precious orchid in 24 hours. The gardener only has three days to figure out which barrel is good. He wants to sacrifice four orchids by irrigating them with a mixture of 2 barrels. How can he find poisonous barrels?

## Problem
We have a table showing what barrels were used each day for each of these four orchids. We want to figure which one of these barrels was poisonous. There is 66 possible combination of two poisonous barrels. Also, based on our table and the two poisonous barrels, the only information we have is that each orchid has died on which day. Therefore, the best way to be sure that a specific table is a solution is to have a unique outcome (the day of death of each orchid) to figure out the poisonous barrels based on this outcome.

## Genetic Algorithm
Based on the nature of the problem, using the Genetic Algorithm is logical. Our fitness function is the number of possible poisonous barrels that did not have a unique outcome. The chromosomes are the described tables.

We have a population of these tables that were randomly initiated at the beginning, and we evaluate their fitness based on the number of possible poisonous barrels that did not have a unique outcome. Our goal is to reach **zero** common outcome (all outcomes be unique).

### Selection
We randomly select a subset of our population based on the `tournament_size`, then select the best of them based on the fitness and the `parents_size`.

### Breeding offsprings
We randomly pair parents together and create two children based on them. For making children, we randomly select a point and crossover the two parents based on that. 

### Mutation
We do mutation based on a variable called `mutation_rate`. When one individual is being mutated, we select two pairs of days and orchids, and we mix their barrels with each other.

### Replacement
We keep the best of parents based on the `elite_size`, and we select the rest of the next population with the best of children.

## Test
I did many tests we many parameters, and I have mentioned some of them below.
### Test 1
In this example, we consider all of our population as parents and keep half of them in the next generation.
`population_size` = 200, `tournament_size` = 200, `parents_size` = 200, `mutation_rate` = 0.9, `elite_size` = 100, `n_generations` = 103
```bash
Epoch 90 :      Population total fitness: 1074.0        Best fitness: 2.0
Epoch 91 :      Population total fitness: 1016.0        Best fitness: 1.0
Epoch 92 :      Population total fitness: 1030.0        Best fitness: 1.0
Epoch 93 :      Population total fitness: 1019.0        Best fitness: 1.0
Epoch 94 :      Population total fitness: 980.0         Best fitness: 1.0
Epoch 95 :      Population total fitness: 982.0         Best fitness: 1.0
Epoch 96 :      Population total fitness: 913.0         Best fitness: 1.0
Epoch 97 :      Population total fitness: 953.0         Best fitness: 1.0
Epoch 98 :      Population total fitness: 1003.0        Best fitness: 1.0
Epoch 99 :      Population total fitness: 953.0         Best fitness: 1.0
Epoch 100 :     Population total fitness: 914.0         Best fitness: 1.0
Epoch 101 :     Population total fitness: 936.0         Best fitness: 1.0
Epoch 102 :     Population total fitness: 926.0         Best fitness: 0.0
0.0 [[['d', 'h'], ['k', 'a'], ['b', 'f']], [['b', 'c'], ['k', 'i'], ['e', 'd']], [['a', 'j'], ['l', 'h'], ['f', 'g']], [['e', 'g'], ['l', 'i'], ['c', 'j']]]
```
### Test 2
In this example, we reach the value `1` really fast, but it did not reach `0`.
`population_size` = 200, `tournament_size` = 100, `parents_size` = 80, `mutation_rate` = 0.9, `elite_size` = 20, `n_generations` = 2000
```bash
Epoch 1991 :    Population total fitness: 1167.0        Best fitness: 1.0
Epoch 1992 :    Population total fitness: 1177.0        Best fitness: 1.0
Epoch 1993 :    Population total fitness: 1257.0        Best fitness: 1.0
Epoch 1994 :    Population total fitness: 1213.0        Best fitness: 1.0
Epoch 1995 :    Population total fitness: 1177.0        Best fitness: 1.0
Epoch 1996 :    Population total fitness: 1283.0        Best fitness: 1.0
Epoch 1997 :    Population total fitness: 1152.0        Best fitness: 1.0
Epoch 1998 :    Population total fitness: 1168.0        Best fitness: 1.0
Epoch 1999 :    Population total fitness: 1175.0        Best fitness: 1.0
1.0 [[['b', 'c'], ['a', 'i'], ['k', 'i']], [['j', 'g'], ['e', 'f'], ['k', 'd']], [['l', 'k'], ['f', 'i'], ['b', 'g']], [['d', 'a'], ['c', 'e'], ['h', 'g']]]
```

## Analysis

### population_size
We need a moderated number because a high value can add to our processing time without any benefit, and a low value might not lead us to `0`.

### tournament_size
The higher the value of `tournament_size`, the lower our exploration. In this problem, considering it equal to `population_size` had a good result.

### parents_size
The higher the value of `tournament_size`, the higher our exploitation. In this problem, considering it equal to `population_size` had a good result.

### mutation_rate
`mutation_rate` played a vital role in my tests as it is crucial in finding new solutions. Considering a high value for it made great result in my tests.

### elite_size
`elite_size` speeds up, reaching an optimum, but it might cause the model to be stuck in a local optimum. Therefore, I had to try several things to find a good value.
