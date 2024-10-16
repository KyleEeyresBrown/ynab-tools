#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 18:43:22 2022

@author: MacBookPro
"""
import pandas as pd

source = "Aspiration" #Input options: "Aspiration" or "Discover"

#INPUTS
def check_for_files():
    today = pd.to_datetime("today")
    if source == "Aspiration" :
        print("Reformatting Aspiration input file")
        asp_input_file = pd.read_csv("/Users/MacBookPro/Downloads/1160422_spend_20240109.csv")
        ynab_format = asp_input_file[['Transaction date','Description','Pending/posted','Amount']]
        ynab_format.rename(columns = {'Transaction date': 'Date',
                                    'Description':'Payee',
                                    'Pending/posted':'Memo'}, inplace = True)

    else:
        print("Reformatting Discover input file")
        disc_input_file = pd.read_csv("/Users/MacBookPro/Downloads/Discover-RecentActivity-20230424.csv")
        ynab_format = disc_input_file[['Trans. Date','Description','Category','Amount']]
        ynab_format.rename(columns = {'Trans. Date': 'Date',
                                    'Description':'Payee',
                                    'Category':'Memo'}, inplace = True)

    amount_mask = ynab_format['Amount'] > 0 
    ynab_format['Outflow'] = abs(ynab_format['Amount'].mask(amount_mask))
    ynab_format['Inflow'] = ynab_format['Amount'].mask(~amount_mask)
    ynab_import = ynab_format[["Date", "Payee", "Memo", "Outflow", "Inflow"]]

    print("Printing YNAB Import CSV")
    ynab_csv = ynab_import.to_csv('ynab_import_' + str(today) + '.csv', index = False)

if __name__ == "__main__":
    check_for_files()