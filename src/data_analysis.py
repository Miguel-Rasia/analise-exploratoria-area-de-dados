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
    pass

def get_jobs_by_month(df):
    pass

def get_top_skills(df, limit=20):
    pass

def get_salary_metrics(df, salary_type):
    pass