#!/bin/bash 

DISTRIBUTION_ID=$1 

aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"