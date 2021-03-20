# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd

def main(input_filepath, output_filepath, lagged_list):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    data = pd.read_csv(input_filepath)

    logger.info("convert datetime to pd.datetime")
    data.datetime = pd.to_datetime(data.datetime)

    logger.info("sorting data")
    data = data.sort_values(["Customer", "datetime"])

    lagged_data = data.copy()
    logger.info('creating lags')
    for lag_number in lagged_list:
        lagged_data['lag_{}'.format(lag_number)] = data.groupby('Consumption Category')['consumption'].shift(lag_number)
    
    lagged_data = lagged_data.dropna()
    logger.info('saving CSV')
    lagged_data.to_csv(output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    lagged_list = list(range(10)) + list(range(15,31)) + list(range(42,50))  # selected due to autocorrelation plot

    project_dir = Path(__file__).resolve().parents[2]
    input_filepath = "{}/data/processed/2012-2013-solar-electricity-data.csv".format(project_dir)
    output_filepath = "{}/data/processed/lagged_2012-2013-solar-electricity-data.csv".format(project_dir)
    main(input_filepath, output_filepath, lagged_list)