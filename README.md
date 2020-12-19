# An IEEE 802.11 Channel Access Simulator based on the Python NumPy Library

### Created as an engineering project at AGH University of Science and Technology

Author: Cecylia Borek, Supervisor: Szymon Szott, PhD

## Basic Description

This IEEE 802.11 channel access simulator was created to support some basic simulation scenarios and study research. It allows specifying various input parameters and returns probability of collission and aggregate network throughput as primary results. It was created in accordance to the *a* amendment of the IEEE 802.11 standard. For more information regarding the simulator, project goals and assumpiots made during the implementation of the simulator, refernce [the thesis].

## Usage

The main part of the simulator is the [dcf_simulation](https://github.com/cecyliaborek/DCF-NumPy-simulation/blob/master/simulation.py) function. It can be used in the following way:
```python
results = dcf_simulation(N=10, cw_min=15, cw_max=1023, seed=1, data_rate=54, control_rate=24, mac_payload=1500)
```
The full list of possible input parametrs and their meaning can be found in the docstring of the [dcf_simulation](https://github.com/cecyliaborek/DCF-NumPy-simulation/blob/master/simulation.py) function.

The results returned by the function are in the form of a class, which contains two fields: mean probability of collision and aggregate network throughput. They can be accessed the following way:

```python
p_coll = results.mean_collision_probability
thr = results.network_throughput
```
The full list of possible return values and their meaning can be found in the docstring of the [dcf_simulation](https://github.com/cecyliaborek/DCF-NumPy-simulation/blob/master/simulation.py) function.
