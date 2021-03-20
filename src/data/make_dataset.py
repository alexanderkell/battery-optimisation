# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path


def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    logger.info('reading csv')
    data = pd.read_csv(input_filepath)
    data = data.drop(columns=["Row Quality"])

    logger.info('porforming melt')
    data = pd.melt(data, id_vars=["Customer", "Generator Capacity",'Postcode','Consumption Category',"date"], var_name="time",value_name="consumption")
    
    data["datetime"] = data["date"] + " " + data["time"]

    logger.info('datetime to pd.datetime column')
    data["datetime"] = pd.to_datetime(data.datetime)
    
    logger.info('renaming columns')
    data['Consumption Category'] = data['Consumption Category'].replace({"CL":"controlled_load_consumption", "GC": "general_electricity_consumption", "GG": "solar_generation"})

    logger.info('saving to csv')
    data.to_csv(output_filepath)



if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    input_filepath = "{}/data/raw/Solar home half-hour data - 1 July 2012 to 30 June 2013/2012-2013 Solar home electricity data v2.csv".format(project_dir)
    output_filepath = "{}/data/processed/2012-2013-solar-electricity-data.csv".format(project_dir)
    main(input_filepath, output_filepath)
