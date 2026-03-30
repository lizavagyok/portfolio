import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List, Optional

# Add the current directory to sys.path to import models
sys.path.append(os.path.dirname(__file__))

from ds_model import OECDDataProcessor
from ca_earnings_model import CAEarningsProcessor
from data_model import PortfolioData

class StaticPlotGenerator:
    """
    A class to handle the generation of static visualizations for the portfolio.
    Encapsulates the rendering logic for each distinct project dataset.
    """
    
    def __init__(self, output_dir: str = "images"):
        """
        Initializes the generator with an output directory.
        
        Args:
            output_dir: The subdirectory where images will be saved.
        """
        self.output_dir = os.path.join(os.path.dirname(__file__), output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_oecd_plots(self):
        """Generates plots for the OECD health risk factors project."""
        csv_path = os.path.join(os.path.dirname(__file__), "data", "alc_tob.csv")
        processor = OECDDataProcessor(csv_path)
        df = processor.clean_data
        
        if df.empty:
            print("Warning: OECD data is empty, skipping plots.")
            return

        # Plot 1: Alcohol Consumption Trends
        plt.figure(figsize=(10, 6))
        countries = ['United States', 'France', 'Germany', 'United Kingdom', 'Japan']
        for country in countries:
            country_df = processor.filter_data(country, 'Alcohol consumption')
            if not country_df.empty:
                plt.plot(country_df['year'], country_df['value'], label=country, marker='o', markersize=4)
        
        plt.title('Alcohol Consumption Trends (Liters per capita)', fontsize=14)
        plt.xlabel('Year')
        plt.ylabel('Liters per capita')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "oecd_alcohol_trends.png"), dpi=300)
        plt.close()
        
        # Plot 2: Obesity rates comparison
        plt.figure(figsize=(10, 6))
        
        # Get latest available data point for EACH country for the 'Obese' measure
        obese_all = df[df['measure'] == 'Obese'].copy()
        if not obese_all.empty:
            # Group by country and get the index of the maximum year for each
            idx = obese_all.groupby('country')['year'].idxmax()
            latest_obese_per_country = obese_all.loc[idx]
            
            # Now take the top 15 of these latest data points
            top_15_obese = latest_obese_per_country.sort_values('value', ascending=False).head(15)
            
            plt.bar(top_15_obese['country'], top_15_obese['value'], color='salmon')
            plt.title('Top 15 OECD Countries by Obesity Rate (Most Recent Data)', fontsize=14)
            plt.xlabel('Country')
            plt.ylabel('Percentage of population')
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "oecd_obesity_comparison.png"), dpi=300)
        plt.close()

    def generate_ca_plots(self):
        """Generates plots for the California earnings analysis project."""
        csv_path = os.path.join(os.path.dirname(__file__), "data", "ca_earnings.csv")
        processor = CAEarningsProcessor(csv_path)
        
        # Plot 1: Earnings by Education and Gender
        edu_gender_df = processor.get_earnings_by_edu_gender()
        if not edu_gender_df.empty:
            edu_order = [e for e in processor.EDU_ORDER if e in edu_gender_df.index]
            edu_gender_df = edu_gender_df.reindex(edu_order)
            
            edu_gender_df.plot(kind='bar', figsize=(12, 7), color=['lightcoral', 'skyblue'])
            plt.title('Mean Weekly Earnings by Education Level and Gender (California 2014)', fontsize=14)
            plt.xlabel('Education Level')
            plt.ylabel('Mean Weekly Earnings ($)')
            plt.xticks(rotation=45, ha='right')
            plt.legend(title='Gender')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "ca_earnings_by_edu.png"), dpi=300)
            plt.close()
        
        # Plot 2: Gender Gap by Union Membership
        gap_df = processor.get_gender_gap_by_union()
        if not gap_df.empty:
            plt.figure(figsize=(10, 6))
            gap_df = gap_df.sort_values('Gender Gap (%)', ascending=False)
            
            plt.bar(gap_df.index, gap_df['Gender Gap (%)'], color='mediumpurple')
            plt.title('Gender Wage Gap by Union Membership (California 2014)', fontsize=14)
            plt.xlabel('Union Member (Yes/No)')
            plt.ylabel('Gender Wage Gap (%)')
            plt.ylim(0, max(gap_df['Gender Gap (%)']) * 1.2)
            
            for i, v in enumerate(gap_df['Gender Gap (%)']):
                plt.text(i, v + 0.5, f"{v:.1f}%", ha='center', fontweight='bold')
                
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "ca_gender_gap_union.png"), dpi=300)
            plt.close()

    def generate_portfolio_plots(self):
        """Generates plots for the portfolio OOP showcase simulation."""
        processor = PortfolioData(n_points=500)
        df = processor.clean_data
        
        # Plot 1: Random Walk Simulation
        plt.figure(figsize=(10, 6))
        plt.plot(df['x'], df['y'], color='royalblue', linewidth=1.5)
        plt.title('Object-Oriented Data Simulation (Random Walk)', fontsize=14)
        plt.xlabel('Step Count')
        plt.ylabel('Cumulative Value')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "portfolio_simulation.png"), dpi=300)
        plt.close()
        
        # Plot 2: Distribution of steps
        plt.figure(figsize=(10, 6))
        steps = np.diff(df['y'])
        plt.hist(steps, bins=30, color='lightseagreen', edgecolor='white', alpha=0.8)
        plt.title('Distribution of Step Increments', fontsize=14)
        plt.xlabel('Increment Value')
        plt.ylabel('Frequency')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "portfolio_distribution.png"), dpi=300)
        plt.close()

    def run_all(self):
        """Executes all plotting routines and provides console feedback."""
        print("Starting plot generation...")
        self.generate_oecd_plots()
        print("- OECD plots generated.")
        self.generate_ca_plots()
        print("- California Earnings plots generated.")
        self.generate_portfolio_plots()
        print("- Portfolio showcase plots generated.")
        print("All visualizations completed successfully.")

if __name__ == "__main__":
    generator = StaticPlotGenerator()
    generator.run_all()
