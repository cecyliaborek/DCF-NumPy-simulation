import numpy as np
import math

def dcf_simulation(N, cw_min, cw_max, seed, data_rate = 54, control_rate = 6, mac_payload = 2304):
    """Simulates DCF function as method of multiple access in 802.11 network
    and returns mean probability of colliosion per station

    Arguments:
        N (int): number of stations contending for the wireless medium
        cw_min (int): value of CWmin of BEB algorithm
        cw_max (int): value of CWmax of BEB algorithm
        seed (int): seed for the numpy random generator, allowing to reproduce the simulation
        data_rate (int): rate at which data is transmitted in Mb/s (one of the defined in 802.11a standard)
        control_rate (int): rate at which control data is transmitted in Mb/s
        mac_payload (int): payload of MAC frame in B, maximally 2304B
        
        Values cw_min and cw_max should be the powers of 2 minus 1, i.e. 15, 31...1023

    Returns:
        numpy.float64: mean probabilty of collision for station
    """

    simulation_rounds  = 10000
    retry_limit = 4

    successful = np.zeros(N)
    collisions = np.zeros(N)
    retransmissions = np.zeros(N)
    cw = np.ones(N) * (cw_min + 1)

    tx_time = np.zeros(simulation_rounds)

    np.random.seed(seed)
    backoffs = np.random.randint(low=0, high=cw_min+1, size=N)

    for round in range(simulation_rounds):
        min_backoff = np.amin(backoffs)
        next_tx = np.where(backoffs == min_backoff)[0]
        backoffs = backoffs - min_backoff - 1
        if len(next_tx) == 1:
            successful[next_tx] +=1
            retransmissions[next_tx] = 0
            cw[next_tx] = cw_min+1
            backoffs[next_tx] = np.random.randint(low=0, high=cw[next_tx])
        else:
            for tx in next_tx:
                collisions[tx] +=1
                if retransmissions[tx] <= retry_limit:
                    retransmissions[tx] +=1
                    cw[tx] = min(cw_max+1, cw[tx]*2)
                else:
                    retransmissions[tx] = 0
                    cw[tx] = cw_min + 1
                
                backoffs[tx] = np.random.randint(low=0, high=cw[tx])
        tx_time[round] = transmission_time(min_backoff, data_rate, control_rate, mac_payload)

    collision_probability = collisions/(successful + collisions)
    mean_collision_probability = np.mean(collision_probability)

    print(tx_time)

    return mean_collision_probability


def transmission_time(backoff_slots, data_rate, control_rate, mac_payload):
    """Calculates the time of single round of contention in dcf

    Args:
        backoff_slots (int): number of slots of backoff period in given round
        data_rate (int): rate at which data is transmitted in Mb/s (one of the defined in 802.11a standard)
        control_rate (int): rate at which control data is transmitted in Mb/s
        mac_payload (int): payload of MAC frame in B, maximally 2304B
    Returns:
        int: time of single round of contention in slots
    """

    #dictionary: (data rate, bits per symbol)
    bits_per_symbol = dict([(6, 48), (9, 48), (12, 96), (18, 96), (24, 192), (36, 192), (48, 288), (54, 288)])

    slot_duration = 9e-6 #s
    sifs = 16e-6 #s
    difs = sifs + 2 * slot_duration #s

    ofdm_preamble = 16e-6 #s
    ofdm_signal = 24 #bits
    ofdm_signal_duration = ofdm_signal/(control_rate * 1e6) #s
    service = 16 #bits
    tail = 6 #bits
    
    
    #ack frame
    ack = 14*8 #bits
    ack_duration = ofdm_preamble + ofdm_signal_duration + (service + ack + tail)/(control_rate * 1e6) #s  

    #data frame
    mac_header = 36*8 #bits
    mac_tail = 4*8 #bits
    mac_frame = mac_header + mac_payload*8 + mac_tail #bits
    padding = math.ceil((service + mac_frame + tail)/bits_per_symbol[data_rate]) * bits_per_symbol[data_rate] - (service + mac_frame + tail) #bits

    data_duration = ofdm_preamble + ofdm_signal_duration + (service + mac_frame + tail + padding)/(data_rate * 1e6) #s

    tx_time = difs + data_duration + sifs + ack_duration #s
    tx_time_slots = math.ceil(tx_time/slot_duration) + backoff_slots #slots

    return tx_time_slots