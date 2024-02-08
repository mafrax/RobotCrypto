import pandas as pd
import os
from datetime import datetime


class DailyReportManager:
    def __init__(self):
        self.filename = self.get_report_filename()

    def get_report_filename(self):
        today = datetime.now().strftime('%d_%m_%Y')
        return f'avax_report_{today}.xlsx'

    def check_create_report(self):
        # Check if the file exists
        if not os.path.exists(self.filename):
            # Create a new DataFrame with headers for the report
            df = pd.DataFrame(columns=['Token Address', 'Symbol', 'Liquidity', 'Has ABI', 'Potential Honeypot'])
            # Save the new DataFrame as an Excel file
            df.to_excel(self.filename, index=False, engine='openpyxl')

    def add_pair_to_report(self, pair_info):
        # Load the existing report into a DataFrame
        df = pd.read_excel(self.filename, engine='openpyxl')
        # Append new row for the non-WAVAX token in the pair
        new_row = {
            'Token Address': pair_info['address'],
            'Symbol': pair_info['symbol'],
            'Liquidity': pair_info['liquidity'],
            'Has ABI': 'Yes' if pair_info['has_abi'] else 'No',
            'Potential Honeypot': 'Yes' if pair_info['is_potential_honeypot'] else 'No'
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Save the updated DataFrame back to the Excel file
        df.to_excel(self.filename, index=False, engine='openpyxl')
