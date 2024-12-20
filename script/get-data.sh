#/bin/bash

# Download the data
curl -s -o ./data/listings.csv.gz https://data.insideairbnb.com/france/auvergne-rhone-alpes/lyon/2024-09-13/data/listings.csv.gz 
curl -s -o ./data/calendar.csv.gz https://data.insideairbnb.com/france/auvergne-rhone-alpes/lyon/2024-09-13/data/calendar.csv.gz 
# Unzip the data
gunzip ./data/listings.csv.gz
gunzip ./data/calendar.csv.gz

rm -rf ./data/listings.csv.gz
rm -rf ./data/calendar.csv.gz

