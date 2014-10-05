# Hackish dirty code, if your eyes start bleeding, leave this repository immediately

## Basic usage

Edit `blablanalytics.py` to add your default routes

Initialise the database

    $ python ./blablanalytics.py init
Fetch the corresponding offers (run regularly)

    $ python ./blablanalytics.py update
Plot some data (requires matplotlib)

    $ python ./blablanalytics.py plot
## Requirements

- BeautifulSoup
- sqlalchemy
- matplotlib (optional)
