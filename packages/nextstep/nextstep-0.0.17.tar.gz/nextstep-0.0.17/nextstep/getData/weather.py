from wwo_hist import retrieve_hist_data
import pandas as pd


def get_weather_data(config):
    """CSV will be written to the current directory."""
    retrieve_hist_data(config['api_key'],
                       config['location_list'],
                       config['start_date'],
                       config['end_date'],
                       config['frequency'],
                       location_label = config['location_label'],
                       export_csv = True,
                       store_df = False)
    return None
