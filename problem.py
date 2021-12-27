import random
import copy
from itertools import combinations

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

class Problem:
	def __init__(self, n_fluids, n_sacrificing_orchids, n_days):
		self.n_fluids = n_fluids
		self.n_sacrificing_orchids = n_sacrificing_orchids
		self.n_days = n_days
		self.n_possible_pairs = self.n_fluids * (self.n_fluids - 1) / 2
		self.n_genes = self.n_days * self.n_sacrificing_orchids
	
	def initial_population(self):
		self.population = [[[random.sample(ALPHABET[:self.n_fluids], k=2) for _ in range(self.n_days)] \
					for o in range(self.n_sacrificing_orchids)] for i in range(self.population_size)]
	
	def fitness(self, individual):
		poisonous_barrels_combinations = list(
			combinations(ALPHABET[:self.n_fluids], 2))
		outcomes = set()
		for poisonous_barrels in poisonous_barrels_combinations:
			died_on = []
			for o in range(4):
				dead_orchid = False
				for d in range(3):
					if not dead_orchid and any([p in individual[o][d]
												for p in poisonous_barrels]):
						dead_orchid = True
						died_on.append(d)
					elif not dead_orchid and d==2:
						died_on.append(3)
			outcomes.add(tuple(died_on))
		return self.n_possible_pairs - len(outcomes)
	
	def selection(self):
		random.shuffle(self.population)
		self.parents = self.population[:self.tournament_size]
		self.parents = sorted(self.parents, key=lambda agent: self.fitness(
			agent), reverse=False)[:self.parents_size]
	
	def breed(self, parent1, parent2):
		pivot_orchid = random.choice(range(self.n_sacrificing_orchids))
		pivot_day = random.choice(range(self.n_days))
		
		child1 = []
		child2 = []
		
		for i in range(self.n_sacrificing_orchids):
			sequence1 = []
			sequence2 = []
			if i < pivot_orchid:
				for j in range(self.n_days):
					sequence1.append(parent1[i][j][:])
					sequence2.append(parent2[i][j][:])
			elif i == pivot_orchid:
				for j in range(self.n_days):
					if j < pivot_day:
						sequence1.append(parent1[i][j][:])
						sequence2.append(parent2[i][j][:])
					else:
						sequence1.append(parent2[i][j][:])
						sequence2.append(parent1[i][j][:])
			else:
				for j in range(self.n_days):
					sequence1.append(parent2[i][j][:])
					sequence2.append(parent1[i][j][:])
			child1.append(sequence1)
			child2.append(sequence2)
		
		return child1, child2
		
	
	def breed_offsprings(self):
		
		self.children = []
		
		for _ in range(self.breed_rate):
			random.shuffle(self.parents)
			for i in range(int(len(self.parents)/2)):
				child1, child2 = self.breed(self.parents[i], self.parents[len(self.parents)-i-1])
				self.children.append(child1)
				self.children.append(child2)
		
	def mutate(self, individual):
		if(random.random() < self.mutation_rate):
			o1, d1 = random.randrange(
				self.n_sacrificing_orchids), random.randrange(self.n_days)
			o2, d2 = random.randrange(
				self.n_sacrificing_orchids), random.randrange(self.n_days)
			while len(set(individual[o1][d1] + individual[o2][d2])) < 4:
				o2, d2 = random.randrange(
					self.n_sacrificing_orchids), random.randrange(self.n_days)
			individual[o1][d1][1], individual[o2][d2][1] = individual[o2][d2][1], individual[o1][d1][1]
	
	def mutate_offsprings(self):
		for individual in self.children:
			self.mutate(individual)
	
	def replacement(self):
		self.children = sorted(
			self.children, key=lambda agent: self.fitness(agent), reverse=False)
		self.parents = sorted(
			self.parents, key=lambda agent: self.fitness(agent), reverse=False)

		self.population = self.children[:-self.elite_size] + self.parents[:self.elite_size]
		self.population = sorted(
                    self.population, key=lambda agent: self.fitness(agent), reverse=False)
	
	def evaluate(self):
		pop_fitness = [self.fitness(agent) for agent in self.population]
	
		return sum(pop_fitness), min(pop_fitness)

	def GA(self, population_size, tournament_size, parents_size, mutation_rate, elite_size, n_generations):
		self.population_size = population_size
		self.tournament_size = tournament_size
		self.parents_size = parents_size
		self.breed_rate = int(self.population_size/self.parents_size)
		self.mutation_rate = mutation_rate
		self.elite_size = elite_size
		self.n_generations = n_generations

		self.initial_population()
		
		for epoch in range(self.n_generations):
			self.selection()
			self.breed_offsprings()
			self.mutate_offsprings()
			self.replacement()
			eval_ = self.evaluate()
			
			print("Epoch", epoch, ":\tPopulation total fitness:",
                            eval_[0], "\tBest fitness:", eval_[1])
			
			if int(eval_[1]) == 0:
				break
		
		print(self.fitness(self.population[0]), self.population[0])
