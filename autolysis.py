#!/usr/bin/env python3
import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import requests
import json

def json_serializable_dict(d):
    """
    Convert a dictionary with non-JSON serializable values to a JSON-friendly format.
    """
    serializable_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            serializable_dict[k] = json_serializable_dict(v)
        elif isinstance(v, list):
            serializable_dict[k] = [
                json_serializable_dict(elem) if isinstance(elem, dict) else
                elem.item() if isinstance(elem, (np.integer, np.floating)) else
                elem for elem in v
            ]
        elif isinstance(v, np.ndarray):
            serializable_dict[k] = v.tolist()
        elif isinstance(v, (np.integer, np.floating)):
            serializable_dict[k] = v.item()
        elif pd.isna(v):
            serializable_dict[k] = None
        else:
            try:
                json.dumps(v)
                serializable_dict[k] = v
            except TypeError:
                serializable_dict[k] = str(v)
    return serializable_dict

class DataAnalyzer:
    def __init__(self, csv_path):
        """
        Initialize the data analyzer with the given CSV file.
        """
        self.csv_path = csv_path
        self.dataset_name = os.path.splitext(os.path.basename(csv_path))[0]  # Always set dataset_name

        try:
            encoding = 'utf-8'  # Default encoding
            try:
                import chardet
                with open(csv_path, 'rb') as f:
                    detected = chardet.detect(f.read())
                    encoding = detected.get('encoding', 'utf-8')
                    print(f"Detected encoding: {encoding}")
            except ImportError:
                print("chardet library not installed, defaulting to utf-8.")

            self.df = pd.read_csv(csv_path, encoding=encoding)
        except UnicodeDecodeError as e:
            print(f"Encoding issue with file: {e}")
            print("Trying with 'latin1' encoding...")
            try:
                self.df = pd.read_csv(csv_path, encoding='latin1')
            except Exception as fallback_e:
                print(f"Fallback failed: {fallback_e}")
                sys.exit(1)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            sys.exit(1)

    def get_ai_summary(self, analysis_summary):
        """
        Get AI-powered summary and insights using AI Proxy.
        """
        api_token = input("Please enter API token:")
        if not api_token:
            raise ValueError("API token is required.")

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
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error getting AI summary: {e}")
            return "Unable to generate AI summary."

    def analyze_data(self):
        """
        Perform comprehensive data analysis.
        """
        analysis = {
            'basic_info': {
                'total_rows': len(self.df),
                'columns': list(self.df.columns),
                'column_types': {col: str(dtype) for col, dtype in self.df.dtypes.items()}
            },
            'missing_data': self.df.isnull().sum().to_dict(),
            'summary_statistics': {}
        }

        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        numeric_stats = self.df[numeric_columns].describe()
        analysis['summary_statistics'] = json_serializable_dict(numeric_stats.to_dict())

        if len(numeric_columns) > 1:
            correlation_matrix = self.df[numeric_columns].corr()
            analysis['correlation_matrix'] = json_serializable_dict(correlation_matrix.to_dict())

        return analysis

    def create_visualizations(self, analysis):
        """
        Create visualizations based on the dataset.
        """
        os.makedirs(self.dataset_name, exist_ok=True)

        if 'correlation_matrix' in analysis:
            plt.figure(figsize=(10, 8))
            correlation_df = pd.DataFrame(analysis['correlation_matrix'])
            sns.heatmap(correlation_df, annot=True, cmap='coolwarm', center=0)
            plt.title(f'Correlation Heatmap - {self.dataset_name.capitalize()}')
            plt.tight_layout()
            plt.savefig(f'{self.dataset_name}/correlation_heatmap.png')
            plt.close()

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
                print(f"Could not create bar chart for {col}: {e}")

    def generate_readme(self, analysis, ai_summary):
        """
        Generate README.md with analysis insights.
        """
        readme_content = f"""# Data Analysis Report: {self.dataset_name.capitalize()}

## Dataset Overview
{ai_summary}

## Technical Analysis

### Basic Information
- Total Rows: {analysis['basic_info']['total_rows']}
- Columns: {', '.join(analysis['basic_info']['columns'])}
- Column Types: {analysis['basic_info']['column_types']}

### Missing Data
{'\n'.join([f"- {col}: {count} missing values" for col, count in analysis['missing_data'].items() if count > 0])}

### Summary Statistics
{'\n'.join([f"#### {col}\n{json.dumps(stats, indent=2)}" for col, stats in analysis['summary_statistics'].items()])}

## Visualizations
- [Correlation Heatmap](correlation_heatmap.png)
{'\n'.join([f"- [Top Categories - {col}]({col}_top_categories.png)" for col in self.df.select_dtypes(include=['object']).columns])}

## Recommendations
{ai_summary.split('Recommendations:')[-1] if 'Recommendations:' in ai_summary else 'No specific recommendations could be generated.'}
"""
        with open(f'{self.dataset_name}/README.md', 'w') as f:
            f.write(readme_content)

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run autolysis.py <path_to_csv_file>")
        sys.exit(1)

    csv_path = sys.argv[1]
    analyzer = DataAnalyzer(csv_path)

    analysis = analyzer.analyze_data()
    analysis_summary = json.dumps(json_serializable_dict(analysis), indent=2)
    ai_summary = analyzer.get_ai_summary(analysis_summary)
    analyzer.create_visualizations(analysis)
    analyzer.generate_readme(analysis, ai_summary)

if __name__ == '__main__':
    main()
