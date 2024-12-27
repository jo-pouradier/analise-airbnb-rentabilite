#/bin/bash


curl -s -o ../data/arrrondissements.zip https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/arrondissements/exports/shp?lang=fr&timezone=Europe%2FBerlin

unzip ../data/arrrondissements.zip -d ../data/arrondissements

rm -rf ../data/arrrondissements.zip