#!/bin/bash

keyboard_id=9 # use xinput to find your keyboard id

xinput test $keyboard_id | while read line ; do
    case $line in
        "key press   44") echo -e "\n == j pressed ==" ;;
        "key press   45") echo -e "\n == k pressed ==" ;;
    esac
done