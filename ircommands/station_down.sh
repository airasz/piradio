#!/bin/bash

function sdown {
    mpc prev
    exit 0
}

function volup {
    vol=$'mpc volume \+5'
    $vol
    #mpc volume +5
    exit 0
}
case $1 in
  sdown)
    sdown
  ;;
  volup)
    volup
  ;;
  *)
  exit 0
  ;;
esac
exit 0