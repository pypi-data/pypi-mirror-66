# tornamona

[![pyup.io](https://pyup.io/repos/github/andrewbolster/tornamona/shield.svg)](https://pyup.io/repos/github/andrewbolster/tornamona/)
[![Build Status](https://travis-ci.org/andrewbolster/tornamona.svg?branch=master)](https://travis-ci.org/andrewbolster/tornamona)
[![Documentation Status](https://readthedocs.org/projects/tornamona/badge/?version=latest)](https://tornamona.readthedocs.io/en/latest/?badge=latest)
[![Mergify Status](https://img.shields.io/endpoint.svg?url=https://gh.mergify.io/badges/andrewbolster/tornamona&style=flat)](https://mergify.io)


A series of fixes for Data originating from Northern Ireland

This is very much a work in progress and I'll only really add to it as things annoy me,
but if you have a data set that's messy, and you can use similar workflows as demonstrated
in this repo, please feel free to use this and PR the crap out of it.

I make no claims of liability, credit, or property over any of this, and make no promises
that anything will ever work or be fixed.

## Current Datasets

### NISRA Weekly Deaths Datasets

Source: https://www.nisra.gov.uk/publications/weekly-deaths

#### What is this data?
* Weekly death registrations in Northern Ireland, from 2009 - 2020
* Also includes tracking of 2020 COVID outbreak

#### What is wrong with the data as presented?
* The Usual Boilerplate (i.e. non numerical footers, non-merged multi row headers, overly complex column headers, inconsistent structure)
* A typo in the 2014 Week Start date ([Which actually inspired me to make this repo in the first place](https://twitter.com/Bolster/status/1254017115817943041))

#### How do I use the new one

```python
from tornamona.fixes import nisra

dataset = nisra.WeeklyDeaths().get().clean()
dataset.data.head().to_markdown()
```
|    |   Week | Week Start          | Week End            |   Total Deaths |   Average Deaths for previous 5 years |   Min 5 year deaths |   Max 5 year deaths |   Respiratory Deaths |   Average Respiratory Deaths for previous 5 years |   COVID19 Deaths |
|---:|-------:|:--------------------|:--------------------|---------------:|--------------------------------------:|--------------------:|--------------------:|---------------------:|--------------------------------------------------:|-----------------:|
|  0 |      1 | 2008-12-27 00:00:00 | 2009-01-02 00:00:00 |            373 |                                 332.4 |                 309 |                 364 |                  nan |                                               nan |              nan |
|  1 |      2 | 2009-01-03 00:00:00 | 2009-01-09 00:00:00 |            454 |                                 329.2 |                 302 |                 377 |                  nan |                                               nan |              nan |
|  2 |      3 | 2009-01-10 00:00:00 | 2009-01-16 00:00:00 |            388 |                                 310.2 |                 290 |                 340 |                  nan |                                               nan |              nan |
|  3 |      4 | 2009-01-17 00:00:00 | 2009-01-23 00:00:00 |            402 |                                 324   |                 281 |                 367 |                  nan |                                               nan |              nan |
|  4 |      5 | 2009-01-24 00:00:00 | 2009-01-30 00:00:00 |            353 |                                 305.6 |                 272 |                 333 |                  nan |                                               nan |              nan |


## Proposed Datasets

Everything that has ever pissed me off about open data

[![NIDC2018](http://img.youtube.com/vi/mtrIEW2nCMc/0.jpg)](http://www.youtube.com/watch?v=mtrIEW2nCMc "Idiots Guide to (Open) Data Science")

# Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter)
and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.

