#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "seaborn",
#   "pandas",
#   "matplotlib",
#   "httpx",
#   "chardet",
#   "numpy",
#   "requests",
#   "python-dotenv",
# ]
# ///

import os
import sys
import json
import logging
from typing import Dict, Any, Optional

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

class DataAnalysisError(Exception):
    """Custom exception for data analysis errors."""
    pass

class DataRecommendationGenerator:
    """Generate data-driven recommendations based on analysis."""
    
    @staticmethod
    def generate_recommendations(analysis: Dict[str, Any], df: pd.DataFrame) -> str:
        """
        Generate data-driven recommendations based on analysis.
        
        Args:
            analysis (Dict): Comprehensive dataset analysis
            df (pd.DataFrame): Original dataframe
        
        Returns:
            str: Generated recommendations
        """
        recommendations = []
        
        # Missing Data Recommendations
        missing_data = analysis.get('missing_data', {})
        missing_columns = [col for col, count in missing_data.items() if count > 0]
        if missing_columns:
            recommendations.append(f"Data Quality Alert: {len(missing_columns)} columns have missing data.")
            recommendations.append("Recommendations:")
            for col in missing_columns:
                missing_percent = (missing_data[col] / len(df)) * 100
                if missing_percent > 50:
                    recommendations.append(f"- Consider dropping column '{col}' due to high missing data ({missing_percent:.2f}%)")
                else:
                    recommendations.append(f"- Investigate and potentially impute missing values in '{col}'")
        
        # Correlation Recommendations
        correlation_matrix = analysis.get('correlation_matrix', {})
        if correlation_matrix:
            corr_df = pd.DataFrame(correlation_matrix)
            high_correlations = []
            
            for col1 in corr_df.columns:
                for col2 in corr_df.columns:
                    if col1 != col2:
                        corr_value = corr_df.loc[col1, col2]
                        if abs(corr_value) > 0.8:
                            high_correlations.append((col1, col2, corr_value))
            
            if high_correlations:
                recommendations.append("Correlation Insights:")
                for col1, col2, corr in high_correlations:
                    recommendations.append(f"- Strong correlation between {col1} and {col2} (r = {corr:.2f})")
                    recommendations.append(f"  Consider feature engineering or checking for multicollinearity")
        
        # Statistical Distribution Recommendations
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            skewness = df[col].skew()
            if abs(skewness) > 1:
                direction = "right" if skewness > 0 else "left"
                recommendations.append(f"- Column '{col}' shows significant {direction}-skewed distribution")
                recommendations.append(f"  Consider applying transformation (log, sqrt) to normalize")
        
        return "\n".join(recommendations) if recommendations else "No specific recommendations could be generated."

class DataAnalyzer:
    """Primary data analysis class with comprehensive analysis capabilities."""
    
    def __init__(self, csv_path: str, log_level: int = logging.INFO):
        """
        Initialize DataAnalyzer with logging and error handling.
        
        Args:
            csv_path (str): Path to input CSV file
            log_level (int): Logging level
        """
        logging.basicConfig(
            level=log_level, 
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.csv_path = csv_path
        self.dataset_name = os.path.splitext(os.path.basename(csv_path))[0]
        
        self._load_dataset()

    def _load_dataset(self) -> None:
        """
        Load dataset with robust encoding detection.
        
        Raises:
            DataAnalysisError: If dataset cannot be loaded
        """
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                self.df = pd.read_csv(self.csv_path, encoding=encoding)
                self.logger.info(f"Successfully loaded dataset using {encoding} encoding")
                return
            except Exception as e:
                self.logger.warning(f"Failed to load dataset with {encoding} encoding: {e}")
        
        raise DataAnalysisError("Could not load dataset with any known encoding")

    def analyze_data(self) -> Dict[str, Any]:
        """
        Perform comprehensive data analysis.
        
        Returns:
            Dict: Comprehensive dataset analysis
        """
        try:
            analysis = {
                'basic_info': self._get_basic_info(),
                'missing_data': self._get_missing_data(),
                'summary_statistics': self._get_summary_statistics(),
                'correlation_matrix': self._get_correlation_matrix()
            }
            return analysis
        except Exception as e:
            self.logger.error(f"Data analysis failed: {e}")
            raise

    def _get_basic_info(self) -> Dict[str, Any]:
        """Get basic dataset information."""
        return {
            'total_rows': len(self.df),
            'columns': list(self.df.columns),
            'column_types': {col: str(dtype) for col, dtype in self.df.dtypes.items()}
        }

    def _get_missing_data(self) -> Dict[str, int]:
        """Calculate missing data for each column."""
        return self.df.isnull().sum().to_dict()

    def _get_summary_statistics(self) -> Dict[str, Dict]:
        """Compute summary statistics for numeric columns."""
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        return self.df[numeric_columns].describe().to_dict()

    def _get_correlation_matrix(self) -> Optional[Dict]:
        """Compute correlation matrix for numeric columns."""
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 1:
            return self.df[numeric_columns].corr().to_dict()
        return None

    def create_visualizations(self, analysis: Dict[str, Any]) -> None:
        """
        Create visualizations based on dataset analysis.
        
        Args:
            analysis (Dict): Comprehensive dataset analysis
        """
        os.makedirs(self.dataset_name, exist_ok=True)
        
        # Correlation Heatmap
        if analysis.get('correlation_matrix'):
            plt.figure(figsize=(10, 8))
            correlation_df = pd.DataFrame(analysis['correlation_matrix'])
            sns.heatmap(correlation_df, annot=True, cmap='coolwarm', center=0)
            plt.title(f'Correlation Heatmap - {self.dataset_name.capitalize()}')
            plt.tight_layout()
            plt.savefig(f'{self.dataset_name}/correlation_heatmap.png')
            plt.close()
        
        # Categorical Column Distribution
        categorical_columns = self.df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            try:
                top_categories = self.df[col].value_counts().head(10)
                plt.figure(figsize=(10, 6))
                top_categories.plot(kind='bar')
                plt.title(f'Top 10 Categories - {col}')
                plt.xlabel(col)
                plt.ylabel('Count')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(f'{self.dataset_name}/{col}_top_categories.png')
                plt.close()
            except Exception as e:
                self.logger.warning(f"Could not create bar chart for {col}: {e}")

    def get_ai_summary(self, analysis_summary: str) -> str:
        """
        Fetch AI-powered summary via proxy.
        
        Args:
            analysis_summary (str): JSON-formatted analysis summary
        
        Returns:
            str: AI-generated summary
        """
        load_dotenv()
        api_token = os.getenv('AI_PROXY_TOKEN')
        
        if not api_token:
            self.logger.warning("No API token found. Skipping AI summary.")
            return "No AI summary available."

        url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a data storyteller. Provide a compelling narrative about the dataset, its insights, and potential implications."
                },
                {
                    "role": "user",
                    "content": f"Dataset Analysis Summary:\n{analysis_summary}"
                }
            ],
            "max_tokens": 1000
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            self.logger.error(f"Error getting AI summary: {e}")
            return "Unable to generate AI summary."

    def generate_readme(self, analysis: Dict[str, Any], ai_summary: str) -> None:
        """
        Generate comprehensive README.md for the analysis.
        
        Args:
            analysis (Dict): Comprehensive dataset analysis
            ai_summary (str): AI-generated summary
        """
        recommendations = DataRecommendationGenerator.generate_recommendations(analysis, self.df)
        
        readme_content = f"""# Data Analysis Report: {self.dataset_name.capitalize()}

## Dataset Overview
{ai_summary}

## Technical Analysis

### Basic Information
- Total Rows: {analysis['basic_info']['total_rows']}
- Columns: {', '.join(analysis['basic_info']['columns'])}
- Column Types: {json.dumps(analysis['basic_info']['column_types'], indent=2)}

### Missing Data
{'\n'.join([f"- {col}: {count} missing values" for col, count in analysis['missing_data'].items() if count > 0])}

### Summary Statistics
{'\n'.join([f"#### {col}\n{json.dumps(stats, indent=2)}" for col, stats in analysis['summary_statistics'].items()])}

## Visualizations
- [Correlation Heatmap](correlation_heatmap.png)
{'\n'.join([f"- [Top Categories - {col}]({col}_top_categories.png)" for col in self.df.select_dtypes(include=['object']).columns])}

## Recommendations
{recommendations}
"""
        with open(f'{self.dataset_name}/README.md', 'w') as f:
            f.write(readme_content)

def main():
    """Main script entry point."""
    if len(sys.argv) < 2:
        print("Usage: python autolysis.py <path_to_csv_file>")
        sys.exit(1)

    csv_path = sys.argv[1]
    
    try:
        analyzer = DataAnalyzer(csv_path)
        analysis = analyzer.analyze_data()
        ai_summary = analyzer.get_ai_summary(json.dumps(analysis, indent=2))
        analyzer.create_visualizations(analysis)
        analyzer.generate_readme(analysis, ai_summary)
        print(f"Analysis complete. Check the {analyzer.dataset_name} directory.")
    except DataAnalysisError as e:
        print(f"Analysis failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
