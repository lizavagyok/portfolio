from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
import pandas as pd

class BaseDataProcessor(ABC):
    """
    Abstract Base Class for all data processors in the portfolio.
    Demonstrates OOP principles: Abstraction, Inheritance, and Encapsulation.
    """
    
    def __init__(self, data_source: Optional[str] = None):
        """
        Initializes the processor with an optional data source path.
        
        Args:
            data_source: Path to the CSV file or other data identifier.
        """
        self.data_source = data_source
        self.raw_data = self._load_data()
        self.clean_data = self._preprocess(self.raw_data)
        
    def _load_data(self) -> pd.DataFrame:
        """
        Loads data from the source. Can be overridden for non-CSV sources.
        
        Returns:
            A pandas DataFrame containing the raw data.
        """
        if self.data_source:
            try:
                return pd.read_csv(self.data_source)
            except Exception as e:
                print(f"Error loading data from {self.data_source}: {e}")
                return pd.DataFrame()
        return pd.DataFrame()
    
    @abstractmethod
    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Abstract method to be implemented by subclasses to perform data cleaning.
        
        Args:
            df: The raw DataFrame.
            
        Returns:
            A cleaned and processed DataFrame.
        """
        pass

    def get_summary_stats(self) -> pd.DataFrame:
        """
        Returns basic statistical summary of the cleaned data.
        
        Returns:
            A DataFrame with summary statistics.
        """
        return self.clean_data.describe()

    def get_column_info(self) -> Dict[str, Any]:
        """
        Returns metadata about the cleaned columns.
        
        Returns:
            A dictionary containing column names and their data types.
        """
        return self.clean_data.dtypes.to_dict()
