#!/bin/bash

# This is an enhanced script from https://wiki.batocera.org/diy-arcade-controls#troubleshooting1 that supports
# automatic switching of trackball and spinner based on the game being run.

system="${1}"
rom="${2}"
romname="${3}"

spinner_games=("arkanoid" "arknoid2u" "arkretrn" "tempest" "arknoid2" "blstroid" "wolfpack" "tron" "mplanets" "720" "aztarac" "forgottn" "kroozr" "crater" "wfortune" "victory" "twotiger" "mhavoc" "puchicar" "puchicaru")

# RetroArch log file must be enabled for this to work
batocera-settings-set global.retroarch.log_dir "/userdata/system/logs/retroarch"
batocera-settings-set global.retroarch.log_to_file true
batocera-settings-set global.retroarch.log_to_file_timestamp false

# NAME OF DESIRED MOUSE INPUT
# Can be found via the RetroArch log file or by running 'evtest'
mouse_name="Ultimarc Button/Joystick/Trackball Interface  Mouse"

for item in "${spinner_games[@]}"; do
    if [[ "$item" == "$rom" ]] then
        mouse_name="Baolian industry Co., Ltd. TS-BSP-02"
    fi
done

# log_path="/userdata/system/logs/retroarch/retroarch.log"
# Use grep with multiple patterns to search the file once
# if grep -q -E "$(
#     IFS="|"
#     echo "${spinner_games[*]}"
# )" "$log_path"; then
#     mouse_name="Baolian industry Co., Ltd. TS-BSP-02"
# fi

# Read the mouse index values from the last RetroArch log file
# and update the config for the next time RetroArch is run
# NOTE: Using '~' as a sed delimiter as some device names include the traditional '/' delimiter
# NOTE: Pipe to 'head -1' to return the index of the first matching device, as some devices expose multiple inputs
mouse_index=$(sed -En "s~.*Mouse.* #(.*): \"$mouse_name\".*~\1~p" /userdata/system/logs/retroarch/retroarch.log | head -1)
if [[ -z "$mouse_index" ]]; then
    mouse_index=0
fi
batocera-settings-set global.retroarch.input_player1_mouse_index $mouse_index

echo "System: '$system'" > /userdata/system/configs/emulationstation/scripts/game-start/launch.log
echo "Rom: '$rom'" >> /userdata/system/configs/emulationstation/scripts/game-start/launch.log
echo "Romname: '$romname'" >> /userdata/system/configs/emulationstation/scripts/game-start/launch.log
echo "Mouse Name: '$mouse_name'" >> /userdata/system/configs/emulationstation/scripts/game-start/launch.log
echo "Mouse Index: '$mouse_index'" >> /userdata/system/configs/emulationstation/scripts/game-start/launch.log
