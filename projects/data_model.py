import pandas as pd
import numpy as np

class PortfolioData:
    """An Object-Oriented approach to managing portfolio data."""
    def __init__(self, n_points=100):
        self.n_points = n_points
        self.data = self._generate_data()

    def _generate_data(self):
        """Private method to simulate data generation."""
        np.random.seed(42)
        return pd.DataFrame({
            'x': np.arange(self.n_points),
            'y': np.random.normal(0, 1, self.n_points).cumsum()
        })

    def get_summary(self):
        """Returns statistical summary of the data."""
        return self.data.describe()

    def update_points(self, n):
        """Updates the number of points and regenerates data."""
        self.n_points = n
        self.data = self._generate_data()
