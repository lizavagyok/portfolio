from base_model import BaseDataProcessor
import pandas as pd

class OECDDataProcessor(BaseDataProcessor):
    """
    Object-Oriented processor for OECD health risk factor data.
    Inherits from BaseDataProcessor, showcasing Polymorphism.
    """
    
    def _preprocess(self, df):
        """Concrete implementation of the preprocessing for OECD data."""
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
        
        # Data cleaning and standardization
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
        
        # Consistent filtering for dashboard display
        lost_meas = ['Daily vegetables', 'Daily fruits', 'Daily smokers', 
                     'Regular vaping users', 'Alcohol consumption']
        for meas in lost_meas:
            mask = (df['measure'] == meas) & (df['age'] == 'Y_GE15')
            df.loc[mask, 'age'] = '_T'
            
        return df[(df['age'] == '_T') & (df['sex'] == '_T')].copy()

    def get_countries(self):
        """Returns a sorted list of unique countries."""
        return sorted(self.clean_data['country'].unique().tolist())

    def get_measures(self):
        """Returns a sorted list of unique health measures."""
        return sorted(self.clean_data['measure'].unique().tolist())

    def filter_data(self, country, measure):
        """Filters clean data based on user input for visualization."""
        mask = (self.clean_data['country'] == country) & (self.clean_data['measure'] == measure)
        return self.clean_data[mask].sort_values('year')
