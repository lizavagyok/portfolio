from abc import ABC, abstractmethod
import pandas as pd

class BaseDataProcessor(ABC):
    """
    Abstract Base Class for all data processors in the portfolio.
    Demonstrates OOP principles: Abstraction and Inheritance.
    """
    
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.raw_data = self._load_data()
        self.clean_data = self._preprocess(self.raw_data)
        
    def _load_data(self):
        """Encapsulated data loading logic."""
        return pd.read_csv(self.csv_path)
    
    @abstractmethod
    def _preprocess(self, df):
        """Abstract method to be implemented by subclasses (Polymorphism)."""
        pass

    def get_summary_stats(self):
        """Common functionality shared by all processors."""
        return self.clean_data.describe()
