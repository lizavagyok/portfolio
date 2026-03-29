import pandas as pd
import numpy as np

class OECDDataProcessor:
    """Object-Oriented processor for OECD health risk factor data."""
    
    def __init__(self, csv_path):
        self.raw_data = pd.read_csv(csv_path)
        self.clean_data = self._preprocess(self.raw_data)
        
    def _preprocess(self, df):
        # Select and rename columns based on notebook analysis
        cols = {
            'Reference area': 'country',
            'TIME_PERIOD': 'year',
            'Measure': 'measure',
            'SEX': 'sex',
            'AGE': 'age',
            'OBS_VALUE': 'value',
            'METHODOLOGY': 'method',
            'Unit of measure': 'units'
        }
        df = df[list(cols.keys())].rename(columns=cols)
        
        # Mapping for cleaner names
        measure_rename = {
            'Share of population consuming vegetables daily': 'Daily vegetables',
            'Share of population consuming fruits daily': 'Daily fruits',
            'Share of population who are daily smokers': 'Daily smokers',
            'Share of population who are overweight': 'Overweight',
            'Share of population who are obese': 'Obese',
            'Share of population who are overweight or obese': 'Overweight or obese',
            'Share of population who are regular vaping product users': 'Regular vaping users'
        }
        df['measure'] = df['measure'].replace(measure_rename)
        
        # Handle the age mapping for specific measures as per notebook
        lost_meas = ['Daily vegetables', 'Daily fruits', 'Daily smokers', 
                     'Regular vaping users', 'Alcohol consumption']
        for meas in lost_meas:
            mask = (df['measure'] == meas) & (df['age'] == 'Y_GE15')
            df.loc[mask, 'age'] = '_T'
            
        # Return only total population rows for simplicity in this dashboard
        return df[(df['age'] == '_T') & (df['sex'] == '_T')].copy()

    def get_countries(self):
        return sorted(self.clean_data['country'].unique().tolist())

    def get_measures(self):
        return sorted(self.clean_data['measure'].unique().tolist())

    def filter_data(self, country, measure):
        mask = (self.clean_data['country'] == country) & (self.clean_data['measure'] == measure)
        return self.clean_data[mask].sort_values('year')
