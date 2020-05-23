import numpy as np

N = 10
simulation_rounds  = 1000

successful = np.zeros(N)
collisions = np.zeros(N)
cw = np.ones(N) * 16

backoffs = np.random.randint(low=0, high=16, size=N)



for round in range(simulation_rounds):
    min_backoff = np.amin(backoffs)
    next_tx = np.where(backoffs == min_backoff)[0]
    backoffs -= min_backoff
    if len(next_tx) == 1:
        successful[next_tx] +=1
        cw[next_tx] = 16
        backoffs[next_tx] = np.random.randint(low=0, high=cw[next_tx])
    else:
        for tx in next_tx:
            collisions[tx] +=1
            #if cw[tx] < 1024:
                #cw[tx] *= 2
            backoffs[tx] = np.random.randint(low=0, high=cw[tx])


collision_probability = np.array([collisions[sta]/(successful[sta] + collisions[sta]) for sta in range(N)])
mean_collision_probability = np.mean(collision_probability)

print("per STA successful transmissions:", successful)
print("per STA collisions:", collisions)
print("per STA collision probability:", collision_probability)
print("average collision probability:", mean_collision_probability)
print(type(mean_collision_probability))