#!/bin/bash

# Define the base URL and the endpoints
base_url="https://66dbf2ce6722fdb9097e9e07-lb-496.bm-south.lab.poridhi.io"
# for localhost use localhost:3000

fast_endpoint="/fast"
medium_endpoint="/medium"
slow_endpoint="/slow"

# Number of requests to send
total_requests=5000

# Loop to send requests
for i in $(seq 1 $total_requests); do
   # Send request to the /fast endpoint
   fast_status_code=$(curl -s -o /dev/null -w "%{http_code}" "$base_url$fast_endpoint")
   echo "Request $i (/fast): $fast_status_code"

   # Send request to the /medium endpoint
   medium_status_code=$(curl -s -o /dev/null -w "%{http_code}" "$base_url$medium_endpoint")
   echo "Request $i (/medium): $medium_status_code"

   # Send request to the /slow endpoint
   slow_status_code=$(curl -s -o /dev/null -w "%{http_code}" "$base_url$slow_endpoint")
   echo "Request $i (/slow): $slow_status_code"
done
