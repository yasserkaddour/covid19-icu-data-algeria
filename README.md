# COVID-19 Data with daily ICUs occupancy for Algeria

The Algerian ministry of Health publish little Covid-19 data, vaccination and testing rate are unknown.
However, they do publish daily **number of people in ICUs** in addition to the number of new cases,
recoveries and deaths. The crucial data about ICUs occupancy was not readily available in a compiled format until now.

This script scrap daily Covid-19 data from the Twitter feed of [the Algerian Ministry of Health](https://twitter.com/Sante_Gouv_dz) and save them in a CSV file.

You need `twitter_consumer_key` and `twitter_consumer_secret` setup in a `config.py` file to run.

## The data
The data scraped is saved in `algeria-covid19-icu-data.csv`, you will find the date, the number of new cases, the number of recoveries, the number of deaths, the number of people in ICUs, the complete copy of the tweet and the link to the original tweet. There are some days in which the data is missing, I plan on adding them later from other sources like the official [WHO publication for Algeria](https://www.afro.who.int/fr/countries/publications?country=980).

## Special thanks
To the Our World in Data team for the awesome [COVID-19 Dataset](https://github.com/owid/covid-19-data) project. Especially [Lucas Rodés-Guirao](https://github.com/lucasrodes) from which a large portion of the code came from.

## License
Data, and code are completely open access under the [Creative Commons BY license](https://creativecommons.org/licenses/by/4.0/). You have the permission to use, distribute, and reproduce these in any medium, provided the source and authors are credited.
