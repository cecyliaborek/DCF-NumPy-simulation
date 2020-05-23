import numpy as np

def dcf_simulation(N, cw_min, cw_max):
    """Simulates DCF function as method of multiple access in 802.11 network
    and returns mean probability of colliosion per station

    Arguments:
        N {int} -- number of stations contending for the wireless medium
        cw_min {int} -- value of CWmin of BEB algorithm
        cw_max {int} -- value of CWmax of BEB algorithm

    Returns:
        numpy.float64 -- mean probabilty of collision for station
    """

    simulation_rounds  = 10000

    successful = np.zeros(N)
    collisions = np.zeros(N)
    cw = np.ones(N) * cw_min

    backoffs = np.random.randint(low=0, high=cw_min, size=N)

    for round in range(simulation_rounds):
        min_backoff = np.amin(backoffs)
        next_tx = np.where(backoffs == min_backoff)[0]
        backoffs -= min_backoff
        if len(next_tx) == 1:
            successful[next_tx] +=1
            cw[next_tx] = cw_min
            backoffs[next_tx] = np.random.randint(low=0, high=cw[next_tx])
        else:
            for tx in next_tx:
                collisions[tx] +=1
                if cw[tx] < cw_max:
                    cw[tx] *= 2
                backoffs[tx] = np.random.randint(low=0, high=cw[tx])

    collision_probability = np.array([collisions[sta]/(successful[sta] + collisions[sta]) for sta in range(N)])
    mean_collision_probability = np.mean(collision_probability)

    return mean_collision_probability