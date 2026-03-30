from base_model import BaseDataProcessor
from typing import Dict, Any
import pandas as pd
import numpy as np

class PortfolioData(BaseDataProcessor):
    """
    An Object-Oriented approach to managing portfolio data.
    Inherits from BaseDataProcessor, demonstrating Abstraction and Encapsulation.
    """
    def __init__(self, n_points: int = 100):
        """
        Initializes the portfolio data generator.
        
        Args:
            n_points: Number of data points to generate.
        """
        self.n_points = n_points
        # For simulated data, we don't need an external data source path
        super().__init__(data_source=None)

    def _load_data(self) -> pd.DataFrame:
        """
        Overrides _load_data to simulate data generation instead of reading a file.
        
        Returns:
            A DataFrame with simulated random walk data.
        """
        return self._generate_data()

    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Implementation of required abstract method.
        
        Args:
            df: The simulated DataFrame.
            
        Returns:
            The processed (unchanged) DataFrame.
        """
        return df

    def _generate_data(self) -> pd.DataFrame:
        """
        Private method to simulate data generation.
        
        Returns:
            A DataFrame with x and y values.
        """
        np.random.seed(42)
        return pd.DataFrame({
            'x': np.arange(self.n_points),
            'y': np.random.normal(0, 1, self.n_points).cumsum()
        })

    def update_points(self, n: int):
        """
        Updates the number of points and regenerates data.
        
        Args:
            n: The new number of points.
        """
        self.n_points = n
        self.clean_data = self._generate_data()

    def get_summary_stats(self) -> pd.DataFrame:
        """
        Returns enhanced summary statistics for the simulated walk.
        
        Returns:
            A DataFrame with summary metrics.
        """
        stats = self.clean_data['y'].describe().to_frame().T
        stats['total_distance'] = np.abs(np.diff(self.clean_data['y'])).sum()
        return stats
