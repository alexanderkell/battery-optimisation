# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd

def main(input_filepath, output_filepath, number_of_lags):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    data = pd.read_csv(input_filepath)

    lagged_data = data.copy()
    logger.info('creating {} lags'.format(number_of_lags))
    for lag_number in range(number_of_lags):
        lagged_data['lag_{}'.format(lag_number)] = data.groupby('Consumption Category')['consumption'].shift(lag_number)
    
    logger.info('saving CSV')
    lagged_data.to_csv(output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    number_of_lags = 384 # 8 days worth of lags

    project_dir = Path(__file__).resolve().parents[2]
    input_filepath = "{}/data/processed/2012-2013-solar-electricity-data.csv".format(project_dir)
    output_filepath = "{}/data/processed/lagged_{}_2012-2013-solar-electricity-data.csv".format(project_dir, number_of_lags)
    main(input_filepath, output_filepath, number_of_lags)