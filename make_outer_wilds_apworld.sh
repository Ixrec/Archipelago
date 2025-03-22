#!/usr/bin/env bash

python worlds/outer_wilds/shared_static_logic/pickle_static_logic.py 1>/dev/null
cd worlds/ 1>/dev/null
if [[ $(grep --recursive --no-messages "Logic Options Experiment" | wc -l) -gt 0 ]]; then
    rm -f outer_wilds_logic_options_experiment.apworld 1>/dev/null
    7z -tzip a outer_wilds_logic_options_experiment.apworld outer_wilds/ 1>/dev/null
    7z rn outer_wilds_logic_options_experiment.apworld outer_wilds outer_wilds_logic_options_experiment 1>/dev/null
else
    rm -f outer_wilds.apworld 1>/dev/null
    7z -tzip a outer_wilds.apworld outer_wilds/ 1>/dev/null
fi
cd - 1>/dev/null
