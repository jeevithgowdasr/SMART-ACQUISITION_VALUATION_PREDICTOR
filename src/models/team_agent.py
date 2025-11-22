import json
from typing import Dict, Any, Union, List
import pandas as pd
import os
import numpy as np
import math

class TeamAgent:
    def __init__(self):
        # Load company data for competitor/acquisition lookup
        self.companies_df = None
        self.acquisitions_df = None
        self._load_datasets()
    
    def _load_datasets(self):
        """Load datasets for company and acquisition lookup"""
        try:
            if os.path.exists("datasets/objects.csv"):
                # Load more data for better coverage, but limit for performance
                self.companies_df = pd.read_csv("datasets/objects.csv", nrows=5000)
            if os.path.exists("datasets/acquisitions.csv"):
                # Load more acquisition data to increase chances of finding matches
                self.acquisitions_df = pd.read_csv("datasets/acquisitions.csv", nrows=5000)
        except Exception as e:
            print(f"Warning: Could not load datasets - {e}")
    
    def transform(self, team_json: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(team_json, str):
            team_data = json.loads(team_json)
        else:
            team_data = team_json
            
        founders = team_data.get('founders', [])
        founder_count = len(founders)
        
        # Enhanced team data collection
        total_experience = 0
        exits_count = 0
        team_size = team_data.get('estimated_team_size', 0)
        
        # Collect detailed founder information
        founder_details = []
        experience_levels = []
        
        for founder in founders:
            experience = founder.get('experience_years', 0)
            has_exit = founder.get('has_exit', False)
            role = founder.get('role', 'Founder')
            education = founder.get('education', '')
            
            total_experience += experience
            if has_exit:
                exits_count += 1
                
            # Categorize experience level
            if experience < 3:
                exp_level = "Junior"
            elif experience < 7:
                exp_level = "Mid-level"
            elif experience < 15:
                exp_level = "Senior"
            else:
                exp_level = "Executive"
                
            experience_levels.append(exp_level)
                
            founder_details.append({
                'experience': experience,
                'experience_level': exp_level,
                'has_exit': has_exit,
                'role': role,
                'education': education
            })
        
        avg_experience = 0.0 if founder_count == 0 else total_experience / founder_count
        
        # Enhanced team strength calculation with more sophisticated metrics
        team_strength_score = self._calculate_team_strength(
            founder_count, avg_experience, exits_count, team_size, experience_levels
        )
        
        # Calculate experience distribution
        experience_distribution = {
            'junior': experience_levels.count('Junior'),
            'mid_level': experience_levels.count('Mid-level'),
            'senior': experience_levels.count('Senior'),
            'executive': experience_levels.count('Executive')
        }
        
        return {
            'team_strength_score': float(team_strength_score),
            'founder_count': founder_count,
            'avg_experience': float(avg_experience),
            'exits_count': exits_count,
            'estimated_team_size': team_size,
            'founder_details': founder_details,
            'experience_distribution': experience_distribution,
            'team_composition_score': float(self._calculate_team_composition_score(experience_distribution, team_size))
        }
    
    def _calculate_team_strength(self, founder_count: int, avg_experience: float, 
                                exits_count: int, team_size: int, experience_levels: List[str]) -> float:
        """Calculate enhanced team strength score with more sophisticated metrics"""
        # Base factors
        founder_factor = founder_count * 0.2
        experience_factor = avg_experience * 0.5
        exit_factor = exits_count * 1.0
        team_size_factor = min(team_size / 100, 2.0) if team_size > 0 else 0
        
        # Experience diversity factor (more diverse experience levels are better)
        unique_levels = len(set(experience_levels))
        diversity_factor = unique_levels * 0.3 if unique_levels > 1 else 0
        
        # Senior leadership factor (more senior/executive team members are better)
        senior_count = experience_levels.count('Senior') + experience_levels.count('Executive')
        senior_factor = senior_count * 0.4
        
        return founder_factor + experience_factor + exit_factor + team_size_factor + diversity_factor + senior_factor
    
    def _calculate_team_composition_score(self, experience_distribution: Dict[str, int], team_size: int) -> float:
        """Calculate a score based on optimal team composition"""
        if team_size <= 0:
            return 0.0
            
        # Ideal distribution percentages (based on startup best practices)
        ideal_distribution = {
            'junior': 0.4,   # 40% junior talent for execution
            'mid_level': 0.35,  # 35% mid-level for stability
            'senior': 0.2,   # 20% senior for leadership
            'executive': 0.05   # 5% executive for vision
        }
        
        # Calculate how close the actual distribution is to ideal
        score = 0.0
        for level, ideal_pct in ideal_distribution.items():
            actual_pct = experience_distribution.get(level, 0) / team_size
            # Score based on how close we are to ideal (0 to 1, where 1 is perfect match)
            level_score = 1.0 - abs(actual_pct - ideal_pct)
            score += level_score * ideal_pct  # Weight by importance
            
        return score * 10  # Scale to 0-10
    
    def find_competitors(self, company_name: str, industry: str = None) -> list:
        """Find competitors based on company name and industry"""
        if self.companies_df is None:
            return []
            
        try:
            # Filter by industry if provided
            if industry:
                competitors = self.companies_df[
                    (self.companies_df['category_code'] == industry) &
                    (self.companies_df['name'].str.contains(company_name, case=False, na=False) == False)
                ].head(10)  # Increase to 10 results
            else:
                competitors = self.companies_df[
                    self.companies_df['name'].str.contains(company_name, case=False, na=False) == False
                ].head(10)  # Increase to 10 results
                
            # Convert to JSON-serializable format
            result = []
            for _, row in competitors.iterrows():
                # Handle NaN values
                funding_total = row.get('funding_total_usd', 0)
                if pd.isna(funding_total) or np.isinf(funding_total):
                    funding_total = 0.0
                else:
                    funding_total = float(funding_total)
                
                result.append({
                    'name': row['name'],
                    'permalink': row['permalink'],
                    'domain': row.get('domain', ''),
                    'funding_total_usd': funding_total,
                    'category_code': row.get('category_code', '')
                })
            return result
        except Exception as e:
            print(f"Warning: Could not find competitors - {e}")
            return []
    
    def find_acquisition_targets(self, acquirer_name: str) -> list:
        """Find potential acquisition targets based on acquirer history"""
        if self.acquisitions_df is None or self.companies_df is None:
            return []
            
        try:
            # Find acquirer ID - use more flexible matching
            acquirer_matches = self.companies_df[
                self.companies_df['name'].str.contains(acquirer_name, case=False, na=False)
            ].head(5)
            
            if acquirer_matches.empty:
                return []
                
            # Use the first match
            acquirer_id = acquirer_matches.iloc[0]['id']
            
            # Find past acquisitions by this company
            acquisitions = self.acquisitions_df[
                self.acquisitions_df['acquiring_object_id'] == acquirer_id
            ].head(10)  # Increase to 10 results
            
            # Get acquired company details
            targets = []
            for _, acquisition in acquisitions.iterrows():
                acquired_id = acquisition['acquired_object_id']
                acquired_company = self.companies_df[
                    self.companies_df['id'] == acquired_id
                ]
                
                if not acquired_company.empty:
                    company_row = acquired_company.iloc[0]
                    
                    # Handle NaN values for price_amount
                    price_amount = acquisition.get('price_amount', 0)
                    if pd.isna(price_amount) or np.isinf(price_amount):
                        price_amount = 0.0
                    else:
                        price_amount = float(price_amount)
                    
                    targets.append({
                        'name': company_row['name'],
                        'permalink': company_row['permalink'],
                        'domain': company_row.get('domain', ''),
                        'price_amount': price_amount,
                        'price_currency_code': acquisition.get('price_currency_code', 'USD'),
                        'acquired_at': acquisition.get('acquired_at', ''),
                        'category_code': company_row.get('category_code', '')
                    })
                    
            return targets
        except Exception as e:
            print(f"Warning: Could not find acquisition targets - {e}")
            return []
    
    def convert_to_rupees(self, usd_amount: float) -> float:
        """Convert USD amount to INR (using approximate exchange rate)"""
        # Approximate exchange rate: 1 USD = 83 INR (as of 2024)
        exchange_rate = 83.0
        return usd_amount * exchange_rate
    
    @classmethod
    def load(cls) -> 'TeamAgent':
        return cls()