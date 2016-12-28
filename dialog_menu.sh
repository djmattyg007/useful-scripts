#!/bin/bash

cmd=(dialog --menu "Select option:" 22 76 16)
options=(1 "Option 1"    # any option can be set to default to "on"
         2 "Option 2"
         3 "Option 3"
         4 "Option 4")
choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
clear
for choice in $choices; do
    echo $choice
done
