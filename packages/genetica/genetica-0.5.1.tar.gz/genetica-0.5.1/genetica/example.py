from model import Genetica
from dna import genify

# EXAMPLE
# This is how a target class should be structured

class ExampleModel:
    def __init__(self, dna):
        self.dna = dna

        # Class paraters that are inputs for optimization
        self.a1 = genify(range(1,1890), dna.genes[0])
        self.a2 = genify(range(1,2017), dna.genes[1])

        #                 | enum of         | just get a
        #                    possible        certain gen
        #                        params |    to randomize 
        #                 |             |    this parameter|   
        #                 |             |   |              |
        #self.a2 = genify( range(1,2017),      dna.genes[1] )

        # Target parameter to optimize
        self.result = self.fitness()
        
    def fitness(self):
        return self.a1 ** self.a1 + self.a1 * self.a2 + self.a2


# EXAMPLE
# Finding min of parameter result in ExampleModel
# Genetica gets class, number of needed genes to genify parameters, and lambda function, that is,
# essentially a fitness function

model = Genetica(ExampleModel, 2, 1000, lambda x: x.result)
model.run()

print("BEST FIT:", model.get_best_fit())
print("PARAMS OF BEST FIT:", model.get_best_specie().a1, model.get_best_specie().a2)

# Getting populations history of best results for each epoch
model.plot()