#!/bin/bash

for i in {1..10}
    do
  #      echo $i
        cd ~/ns-allinone-3.31/ns-3.31/
        { time ./waf --run "scratch/80211a-performance --simulationTime=50 --nWifi=50 --payload=1500" ; } > /dev/null 2>> /home/cecylia/Documents/studies/thesis/performance/ns3_times.txt
    done