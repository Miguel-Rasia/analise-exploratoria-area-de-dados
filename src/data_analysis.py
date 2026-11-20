import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import data_loader as dl

def filter_jobs(df, country=None, title=None, schedule=None, home_office=None):
    filtered_df = df.copy()

    if not country:
        pass
    else:
       filtered_df = filtered_df[filtered_df['job_country'].isin(country)]

    if not title:
        pass
    else:
       filtered_df = filtered_df[filtered_df['job_title_short'].isin(title)]

    if not schedule:
        pass
    else:
       filtered_df = filtered_df[filtered_df['job_schedule_type'].isin(schedule)]

    if home_office is None:
        pass
    elif home_office is True:
        filtered_df = filtered_df[filtered_df['job_work_from_home'] == True]
    else:
        filtered_df = filtered_df[filtered_df['job_work_from_home'] == False]

    return filtered_df


def get_job_metrics(df):

    if df.empty:
        metrics = {
            'total_jobs': 0,
            'total_countries': 0,
            'total_companies': 0,
            'remote_jobs': 0,
            'remote_percentage': 0
        }        
        
    else:
        total_jobs = df.shape[0]
        total_countries = df['job_country'].nunique()
        total_companies = df['company_name'].nunique()
        remote_jobs = df[df['job_work_from_home'] == True].shape[0]
        remote_percentage = round((remote_jobs / total_jobs) * 100, 2)

        metrics = {
            'total_jobs': total_jobs,
            'total_countries': total_countries,
            'total_companies': total_companies,
            'remote_jobs': remote_jobs,
            'remote_percentage': remote_percentage
        }

    return metrics

def get_jobs_by_month(df):
    pass

def get_top_skills(df, limit=20):
    pass

def get_salary_metrics(df, salary_type):
    pass