from simulation import dcf_simulation

R = 10
runs = [r for r in range(R)]
N = 50
sim_time = 100

results, _ = dcf_simulation(N=N, cw_min=15, cw_max=1023, seed=1, sim_time=sim_time)