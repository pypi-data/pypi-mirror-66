"""GeniePy Package entry point."""
from pkg_resources import get_distribution, DistributionNotFound
import geniepy.config as config
from geniepy.datamgmt import DaoManager
from geniepy.classmgmt import ClassificationMgr


# import geniepy.config as config
# from geniepy.datamgmt import DaoManager
# from geniepy.classmgmt import ClassificationMgr

try:
    # Change here if project is renamed and does not equal the package name
    DIST_NAME = __name__
    __version__ = get_distribution(DIST_NAME).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

__author__ = "The Harvard LAMP Team"
__copyright__ = "The Harvard LAMP Team"
__license__ = "MIT"


__all__ = ["runjob"]


def run_predictions():
    """Calculate predictions for all records in database."""
    daomgr: DaoManager = config.get_daomgr()
    classmgr: ClassificationMgr = config.get_classmgr()
    chunksize = config.get_classmgr()
    for records in daomgr.gen_records(chunksize):
        predicted_df = classmgr.predict(records)
        daomgr.save_predictions(predicted_df)


def run_downloads():
    """Call scrapes to download data and create/append tables."""
    daomgr: DaoManager = config.get_daomgr()
    chunksize = config.get_classmgr()
    daomgr.download(chunksize)


def run_job():
    """Cron-job function to scrape sources for updated data and update predictions."""
    # Download all new data
    run_downloads()
    # Start parsing table
    run_predictions()
    print("Done")
