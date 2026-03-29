import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Add the current directory to sys.path to import models
sys.path.append(os.path.dirname(__file__))

from ds_model import OECDDataProcessor
from ca_earnings_model import CAEarningsProcessor
from data_model import PortfolioData

def generate_oecd_plots():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "alc_tob.csv")
    processor = OECDDataProcessor(csv_path)
    df = processor.clean_data
    
    # Ensure images directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), "images"), exist_ok=True)
    
    # Plot 1: Alcohol Consumption Trends for select countries
    plt.figure(figsize=(10, 6))
    countries = ['United States', 'France', 'Germany', 'United Kingdom', 'Japan']
    for country in countries:
        country_df = df[(df['country'] == country) & (df['measure'] == 'Alcohol consumption')]
        if not country_df.empty:
            plt.plot(country_df['year'], country_df['value'], label=country, marker='o', markersize=4)
    
    plt.title('Alcohol Consumption Trends (Liters per capita)', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('Liters per capita')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "images", "oecd_alcohol_trends.png"), dpi=300)
    plt.close()
    
    # Plot 2: Obesity rates comparison (latest year)
    plt.figure(figsize=(10, 6))
    obese_df = df[df['measure'] == 'Obese'].sort_values('year', ascending=False)
    latest_year = obese_df['year'].max()
    latest_obese = obese_df[obese_df['year'] == latest_year].sort_values('value', ascending=False).head(15)
    
    plt.bar(latest_obese['country'], latest_obese['value'], color='salmon')
    plt.title(f'Top 15 Countries by Obesity Rate ({latest_year})', fontsize=14)
    plt.xlabel('Country')
    plt.ylabel('Percentage of population')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "images", "oecd_obesity_comparison.png"), dpi=300)
    plt.close()

def generate_ca_plots():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "ca_earnings.csv")
    processor = CAEarningsProcessor(csv_path)
    
    # Ensure images directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), "images"), exist_ok=True)
    
    # Plot 1: Earnings by Education and Gender
    plt.figure(figsize=(12, 7))
    edu_gender_df = processor.get_earnings_by_edu_gender()
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
    plt.savefig(os.path.join(os.path.dirname(__file__), "images", "ca_earnings_by_edu.png"), dpi=300)
    plt.close()
    
    # Plot 2: Gender Gap by Union Membership
    plt.figure(figsize=(10, 6))
    gap_df = processor.get_gender_gap_by_union()
    
    # Sort by Gender Gap percentage
    gap_df = gap_df.sort_values('Gender Gap (%)', ascending=False)
    
    plt.bar(gap_df.index, gap_df['Gender Gap (%)'], color='mediumpurple')
    plt.title('Gender Wage Gap by Union Membership (California 2014)', fontsize=14)
    plt.xlabel('Union Member (Yes/No)')
    plt.ylabel('Gender Wage Gap (%)')
    plt.ylim(0, max(gap_df['Gender Gap (%)']) * 1.2)
    # Add labels on bars
    for i, v in enumerate(gap_df['Gender Gap (%)']):
        plt.text(i, v + 0.5, f"{v:.1f}%", ha='center', fontweight='bold')
        
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "images", "ca_gender_gap_union.png"), dpi=300)
    plt.close()

def generate_portfolio_plots():
    processor = PortfolioData(n_points=500)
    df = processor.clean_data
    
    # Ensure images directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), "images"), exist_ok=True)
    
    # Plot 1: Random Walk Simulation
    plt.figure(figsize=(10, 6))
    plt.plot(df['x'], df['y'], color='royalblue', linewidth=1.5)
    plt.title('Object-Oriented Data Simulation (Random Walk)', fontsize=14)
    plt.xlabel('Step Count')
    plt.ylabel('Cumulative Value')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "images", "portfolio_simulation.png"), dpi=300)
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
    plt.savefig(os.path.join(os.path.dirname(__file__), "images", "portfolio_distribution.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_oecd_plots()
    print("OECD plots generated.")
    generate_ca_plots()
    print("California Earnings plots generated.")
    generate_portfolio_plots()
    print("Portfolio showcase plots generated.")
