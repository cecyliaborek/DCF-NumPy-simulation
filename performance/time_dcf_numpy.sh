#!/bin/bash

for i in {1..10}
    do
  #      echo $i
        cd ~/Documents/studies/thesis
        { time /home/cecylia/.local/share/virtualenvs/thesis-0uGGOESp/bin/python /home/cecylia/Documents/studies/thesis/performance/run_dcf.py ; } > /dev/null 2>> /home/cecylia/Documents/studies/thesis/performance/dcf_numpy_times.txt
    done