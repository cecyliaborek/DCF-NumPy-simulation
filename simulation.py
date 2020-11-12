import numpy as np
import math


def dcf_simulation(N, cw_min, cw_max, seed, data_rate=54, control_rate=6, mac_payload=2304, debug=False):
    """Simulates DCF function as method of multiple access in 802.11 network
    and returns mean probability of colliosion per station

    Arguments:
        N (int): number of stations contending for the wireless medium
        cw_min (int): value of CWmin of BEB algorithm
        cw_max (int): value of CWmax of BEB algorithm
        seed (int): seed for the numpy random generator, allowing to reproduce the simulation
        data_rate (int): rate at which data is transmitted in Mb/s (one of the defined in 802.11a standard),
            default 54 Mb/s
        control_rate (int): rate at which control data is transmitted in Mb/s, default 6 Mb/s
        mac_payload (int): payload of MAC frame in B, maximally 2304B, default 2304Bs

        Values cw_min and cw_max should be the powers of 2 minus 1, i.e. 15, 31...1023

    Returns:
        Results: class that has two fields - aggregate network throughput in b/s and mean per station
            probability of collision
    """

    contention_rounds = 10000
    retry_limit = 7
    slot_time = 9e-6  # s

    successful = np.zeros(N)  # successful transmissions per station
    collisions = np.zeros(N)  # collisions per station
    retransmissions = np.zeros(N)  # counter of retransmissions per station
    cw = np.ones(N) * (cw_min + 1)
    # table of current CW for each station, changed after collisions
    # and reset back to cw_min on success, contains upper excluded
    # limits, i.e. 16, 32,..., 1024

    tx_time = np.zeros(contention_rounds)  # times of all contention rounds
    throughput = np.zeros(N)  # throughput per station

    np.random.seed(seed)  # setting the seed of PRN generator

    # random backoff for each station
    backoffs = np.random.randint(low=0, high=cw_min+1, size=N)

    # initializing list of all backoff values throught the simulation
    all_backoffs = backoffs

    for round in range(contention_rounds):
        collision = False  # variable determining if collision occured or not,
        # necessary for transmission time calculation
        min_backoff = np.amin(backoffs)  # find the minimal value of backoff
        next_tx = np.where(backoffs == min_backoff)[0]  # an array of index(es)
        # of station(s) with lowest backoff(s)
        backoffs = backoffs - min_backoff - 1  # subtract from all stations' backoffs,
        # time they've already waited
        if len(next_tx) == 1:  # only one station had smallest backoff - success
            successful[next_tx] += 1
            retransmissions[next_tx] = 0
            cw[next_tx] = cw_min+1
            # selecting new backoff for the stations
            backoffs[next_tx] = np.random.randint(low=0, high=cw[next_tx])
            # appending the newly selected backoff to the array of all backoffs
            all_backoffs = np.append(all_backoffs, backoffs[next_tx])
        else:  # more than one station with smallest backoff - collision
            collision = True  # collision set to True, necesarry for transmission time calculation
            for tx in next_tx:
                collisions[tx] += 1
                if retransmissions[tx] <= retry_limit:
                    retransmissions[tx] += 1
                    cw[tx] = min(cw_max+1, cw[tx]*2)
                    # cw is always the upper limit (excluded), therefore we only need to
                    # multiply it by two to get the next value of cw limit
                else:  # if retry limit is met, values of cw and retransmissions couter are reset
                    retransmissions[tx] = 0
                    cw[tx] = cw_min + 1
                # new backoff chosen for all the station that collided
                backoffs[tx] = np.random.randint(low=0, high=cw[tx])
                # appending the newly selected backoff to the array of all backoffs
                all_backoffs = np.append(all_backoffs, backoffs[tx])
        # calculation of round time in slots
        tx_time[round] = transmission_time(
            min_backoff, data_rate, control_rate, mac_payload, collision)['tx_time']

    simulation_results = Results()

    # calculation of collision probabilty per station and mean value of it
    collision_probability = collisions/(successful + collisions)
    simulation_results.mean_collision_probability = np.mean(
        collision_probability)

    # calculation of throughput per station in b/s and aggregate throughput of whole network
    simulation_time = np.sum(tx_time) * slot_time
    throughput = successful * mac_payload * 8 / (simulation_time)
    simulation_results.network_throughput = np.sum(throughput)

    # debug info
    debug_info = (np.sum(successful), np.sum(collisions), simulation_time)

    if(debug):
        return simulation_results, debug_info

    return simulation_results, all_backoffs


def transmission_time(backoff_slots, data_rate, control_rate, mac_payload, collision):
    """Calculates the time of single round of contention in dcf

    Args:
        backoff_slots (int): number of slots of backoff period in given round
        data_rate (int): rate at which data is transmitted in Mb/s (one of the defined in 802.11a standard)
        control_rate (int): rate at which control data is transmitted in Mb/s
        mac_payload (int): payload of MAC frame in B, maximally 2304B
        collision (Bool): boolean value indicating if collision, in given round, occured or not;
            True if there was a collision, False otherwise
    Returns:
        results (str:int): dictionary with duration of contention round and duration of mac frame
    """

    # dictionary: (data rate, bits per symbol)
    bits_per_symbol = dict([(6, 48), (9, 48), (12, 96),
                            (18, 96), (24, 192), (36, 192), (48, 288), (54, 288)])

    results = {}

    slot_duration = 9e-6  # s
    sifs = 16e-6  # s
    difs = sifs + 2 * slot_duration  # s

    ofdm_preamble = 16e-6  # s
    ofdm_signal = 24  # bits
    ofdm_signal_duration = ofdm_signal/(control_rate * 1e6)  # s
    service = 16  # bits
    tail = 6  # bits

    # ack frame
    ack = 14*8  # bits
    ack_duration = ofdm_preamble + ofdm_signal_duration + \
        (service + ack + tail)/(control_rate * 1e6)  # s

    # data frame
    mac_header = 36*8  # bits
    mac_tail = 4*8  # bits
    mac_frame = mac_header + mac_payload*8 + mac_tail  # bits
    padding = (math.ceil((service + mac_frame + tail) /
                         bits_per_symbol[data_rate]) * bits_per_symbol[data_rate]) - (service + mac_frame + tail)  # bits

    data_duration = ofdm_preamble + ofdm_signal_duration + \
        (service + mac_frame + tail + padding)/(data_rate * 1e6)  # s

    tx_time = difs + data_duration  # s
    # adding sifs and ack duration only if the transmission was successful
    if not collision:
        tx_time += sifs + ack_duration  # s
    # adding ack timeout (2*sifs) in case of collision
    else:
        tx_time += 2*sifs  # s

    tx_time_slots = math.ceil(tx_time/slot_duration) + backoff_slots  # slots

    results['tx_time'] = tx_time_slots
    results['frame_time'] = data_duration

    return results


class Results:

    def __init__(self):
        self.mean_collision_probability = 0
        self.network_throughput = 0
