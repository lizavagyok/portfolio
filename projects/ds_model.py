from base_model import BaseDataProcessor
from typing import List, Dict
import pandas as pd

class OECDDataProcessor(BaseDataProcessor):
    """
    Object-Oriented processor for OECD health risk factor data.
    Demonstrates Inheritance and Polymorphism.
    """
    
    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes OECD data to standardize column names and filter for relevant groups.
        
        Args:
            df: Raw DataFrame.
            
        Returns:
            Cleaned DataFrame.
        """
        if df.empty:
            return df

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
        # Only rename columns that exist in the dataframe
        existing_cols = [c for c in cols.keys() if c in df.columns]
        df = df[existing_cols].rename(columns={c: cols[c] for c in existing_cols})
        
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
        if 'measure' in df.columns:
            df['measure'] = df['measure'].replace(measure_rename)
        
        # Standardize for general dashboard display
        if 'measure' in df.columns and 'age' in df.columns:
            lost_meas = ['Daily vegetables', 'Daily fruits', 'Daily smokers', 
                         'Regular vaping users', 'Alcohol consumption']
            for meas in lost_meas:
                mask = (df['measure'] == meas) & (df['age'] == 'Y_GE15')
                df.loc[mask, 'age'] = '_T'
            
            return df[(df['age'] == '_T') & (df['sex'] == '_T')].copy()
        return df

    def get_countries(self) -> List[str]:
        """Returns a sorted list of unique countries."""
        if 'country' not in self.clean_data.columns:
            return []
        return sorted(self.clean_data['country'].unique().tolist())

    def get_measures(self) -> List[str]:
        """Returns a sorted list of unique health measures."""
        if 'measure' not in self.clean_data.columns:
            return []
        return sorted(self.clean_data['measure'].unique().tolist())

    def filter_data(self, country: str, measure: str) -> pd.DataFrame:
        """
        Filters cleaned data based on specific country and measure.
        
        Args:
            country: Name of the country to filter.
            measure: Name of the health measure to filter.
            
        Returns:
            Filtered and year-sorted DataFrame.
        """
        mask = (self.clean_data['country'] == country) & (self.clean_data['measure'] == measure)
        return self.clean_data[mask].sort_values('year')
