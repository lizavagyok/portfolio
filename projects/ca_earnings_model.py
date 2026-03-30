from base_model import BaseDataProcessor
from typing import List, Optional
import pandas as pd
import numpy as np

class CAEarningsProcessor(BaseDataProcessor):
    """
    Object-Oriented processor for California Earnings data (2014 CPS MORG).
    Demonstrates OOP principles: Inheritance, Encapsulation and Polymorphism.
    """
    
    # Static mapping for occupations
    OCC_MAP = {
        2310: "Elem/Mid School Teachers",
        5700: "Secretaries/Admin Assistants",
        3255: "Registered Nurses",
        430: "Managers, Other",
        4720: "Cashiers",
        4760: "Retail Salespersons",
        9130: "Drivers/Truck Drivers",
        4700: "First-line Retail Supervisors",
        4220: "Janitors/Building Cleaners",
        5240: "Customer Service Reps",
        3600: "Nursing/Health Aides",
        4110: "Waiters/Waitresses",
        4020: "Cooks",
        9620: "Laborers/Stock Movers",
        800: "Accountants/Auditors"
    }

    # Static list of education order
    EDU_ORDER = [
        "Less than High School", "High School Graduate", "Some College",
        "Associate Degree", "Bachelor's Degree", "Advanced Degree"
    ]

    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesses the CPS MORG data for California.
        
        Args:
            df: Raw DataFrame.
            
        Returns:
            Processed DataFrame.
        """
        if df.empty:
            return df

        # Education simplification logic
        def simplify_grade(g):
            if g < 39: return "Less than High School"
            if g == 39: return "High School Graduate"
            if g == 40: return "Some College"
            if g in [41, 42]: return "Associate Degree"
            if g == 43: return "Bachelor's Degree"
            if g >= 44: return "Advanced Degree"
            return "Other"

        if 'grade92' in df.columns:
            df['education'] = df['grade92'].apply(simplify_grade)
        
        if 'sex' in df.columns:
            df['gender'] = df['sex'].map({1: 'Male', 2: 'Female'})
        
        if 'unionmme' in df.columns:
            df['union'] = df['unionmme'].fillna('No')
        
        # Calculate hourly wage
        if 'uhours' in df.columns and 'earnwke' in df.columns:
            # Filter valid hours
            df = df[df['uhours'] > 0].copy()
            df['hourly_wage'] = df['earnwke'] / df['uhours']
        
        # Add occupation names
        if 'occ2012' in df.columns:
            df['occupation'] = df['occ2012'].map(self.OCC_MAP)
        
        return df

    def get_education_levels(self) -> List[str]:
        """Returns the sorted list of education levels."""
        return self.EDU_ORDER

    def get_occupations(self) -> List[str]:
        """Returns the list of top occupations used in the analysis."""
        return sorted([occ for occ in self.OCC_MAP.values()])

    def filter_by_education(self, levels: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Filters data by selected education levels.
        
        Args:
            levels: List of education level names to include.
            
        Returns:
            Filtered DataFrame.
        """
        if not levels:
            return self.clean_data
        return self.clean_data[self.clean_data['education'].isin(levels)]

    def get_earnings_by_edu_gender(self, education_filter: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Returns mean weekly earnings grouped by education and gender.
        
        Args:
            education_filter: Optional list of education levels to include.
            
        Returns:
            DataFrame with mean earnings.
        """
        df = self.clean_data
        if education_filter:
            df = df[df['education'].isin(education_filter)]
        
        if 'education' in df.columns and 'gender' in df.columns and 'earnwke' in df.columns:
            return df.groupby(['education', 'gender'])['earnwke'].mean().unstack()
        return pd.DataFrame()

    def get_gender_gap_by_union(self) -> pd.DataFrame:
        """
        Returns gender wage gap percentages by union membership.
        
        Returns:
            DataFrame with gender gap percentages.
        """
        if 'union' in self.clean_data.columns and 'gender' in self.clean_data.columns and 'earnwke' in self.clean_data.columns:
            union_gender = self.clean_data.groupby(['union', 'gender'])['earnwke'].mean().unstack()
            if 'Male' in union_gender.columns and 'Female' in union_gender.columns:
                union_gender['Gender Gap (%)'] = ((union_gender['Male'] - union_gender['Female']) / union_gender['Male']) * 100
                return union_gender
        return pd.DataFrame()

    def get_heatmap_data(self) -> pd.DataFrame:
        """
        Returns data formatted for the hourly wage heatmap.
        
        Returns:
            Reshaped DataFrame for heatmap visualization.
        """
        if 'occupation' not in self.clean_data.columns or 'education' not in self.clean_data.columns:
            return pd.DataFrame()

        # Filter only for the top occupations we have labels for
        df_top = self.clean_data[self.clean_data['occupation'].notna()].copy()
        
        # Shorten education names for heatmap display
        edu_short = {
            "Less than High School": "Less than HS",
            "High School Graduate": "HS Graduate",
            "Some College": "Some College",
            "Associate Degree": "Associate Deg",
            "Bachelor's Degree": "Bachelor's Deg",
            "Advanced Degree": "Advanced Deg"
        }
        df_top['education_short'] = df_top['education'].map(edu_short)
        edu_short_order = [edu_short[e] for e in self.EDU_ORDER if e in edu_short]
        
        if 'occupation' in df_top.columns and 'education_short' in df_top.columns and 'hourly_wage' in df_top.columns:
            heatmap_data = df_top.groupby(['occupation', 'education_short'])['hourly_wage'].mean().unstack()
            return heatmap_data.reindex(columns=edu_short_order)
        return pd.DataFrame()
