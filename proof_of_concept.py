import numpy as np

N = 10
simulation_rounds  = 1000

successful = 0
collisions = 0

for round in range(simulation_rounds):
    backoffs = np.random.randint(low=0, high=16, size=N)
    next_tx = np.where(backoffs == np.amin(backoffs))[0]
    if len(next_tx) == 1:
        successful +=1
    else:
        collisions +=1

transmissions = np.array([successful, collisions])

print(transmissions)
print(transmissions/simulation_rounds * 100)