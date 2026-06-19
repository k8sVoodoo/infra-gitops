#!/bin/bash

API_URL="http://localhost:8080"
WEB_URL="http://localhost:8081"

while true
do
  RATE=$(( RANDOM % 40 + 10 ))

  echo "$(date) rate=${RATE}"

  for ((i=1;i<=RATE;i++))
  do
    curl -s ${API_URL}/api/message >/dev/null &
  done

  for ((i=1;i<=RATE/2;i++))
  do
    curl -s ${WEB_URL} >/dev/null &
  done

  if (( RANDOM % 4 == 0 ))
  then
    curl -s ${API_URL}/api/error >/dev/null &
  fi

  if (( RANDOM % 3 == 0 ))
  then
    curl -s ${API_URL}/api/slow >/dev/null &
  fi

  if (( RANDOM % 2 == 0 ))
  then
    curl -s ${API_URL}/api/work >/dev/null &
  fi

  wait

  sleep 30
done