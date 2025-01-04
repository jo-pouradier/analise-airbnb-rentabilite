#/bin/bash

# Download the data
curl -s -o ../data/loyers.csv https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/logement-encadrement-des-loyers/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B
curl -s -o ../data/listings.csv.gz https://data.insideairbnb.com/france/ile-de-france/paris/2024-09-06/data/listings.csv.gz 
curl -s -o ../data/calendar.csv.gz https://data.insideairbnb.com/france/ile-de-france/paris/2024-09-06/data/calendar.csv.gz
curl -s -o ../data/calendar-2023.csv.gz https://data.insideairbnb.com/france/ile-de-france/paris/2023-12-12/data/calendar.csv.gz
# Unzip the data
gunzip ../data/listings.csv.gz
gunzip ../data/calendar.csv.gz
gunzip ../data/calendar-2023.csv.gz

rm -rf ../data/listings.csv.gz
rm -rf ../data/calendar.csv.gz
rm -rf ../data/calendar-2023.csv.gz
