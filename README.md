# COVID-19 Data with daily ICUs occupancy for Algeria🇩🇿
[![Data](https://img.shields.io/badge/public-data-purple)](public/data/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Open Source Love png3](https://badges.frapsoft.com/os/v3/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)



The Algerian ministry of Health publish little Covid-19 data, vaccination and testing rate are unknown.
However, they do publish daily **number of people in ICUs** in addition to the number of new cases,
recoveries and deaths. The crucial data about ICUs occupancy was not readily available in a compiled format until now.

🎉 **This compiled data is now used to feed the [Our World in Data](https://ourworldindata.org/explorers/coronavirus-data-explorer?zoomToSelection=true&time=2020-03-01..latest&pickerSort=asc&pickerMetric=location&Metric=ICU+patients&Interval=7-day+rolling+average&Relative+to+Population=false&Align+outbreaks=false&country=~DZA) covid-19 dataset.** 🎉
![Our World in Data feature the number of COVID-19 patients in intensive care (ICU) in Algeria 🇩🇿 ](https://user-images.githubusercontent.com/7279640/134263252-88fa87dc-c68c-4ed6-8b71-318068ac482d.png)

## The script

This script scrap daily Covid-19 data from the Twitter feed of [the Algerian Ministry of Health](https://twitter.com/Sante_Gouv_dz) and save them in a CSV file.

You need `TWITTER_CONSUMER_KEY` and `TWITTER_CONSUMER_SECRET` setup in a `config.py` file or as environment variable to run.

## The data
The data scraped is saved in `algeria-covid19-icu-data.csv`, you will find the date, the number of new cases, the number of recoveries, the number of deaths, the number of people in ICUs, the complete copy of the tweet and the link to the original tweet. I removed duplicate tweets and corrected two obvious mistakes. There are some days in which the data is missing, I plan on adding them later from other sources like the official [WHO publication for Algeria](https://www.afro.who.int/fr/countries/publications?country=980).

## Special thanks
To the Our World in Data team for the awesome [COVID-19 Dataset](https://github.com/owid/covid-19-data) project. Especially [Lucas Rodés-Guirao](https://github.com/lucasrodes) from which a large portion of the code came from.

## License
Data, and code are completely open access under the [Creative Commons BY license](https://creativecommons.org/licenses/by/4.0/). You have the permission to use, distribute, and reproduce these in any medium, provided the source and authors are credited.
