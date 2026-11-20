import pandas as pd

def load_dataset(path):
    df = pd.read_csv(path)
    return validate_dataset(df)

def validate_dataset(df):

    required_columns = [
        'job_title_short',
        'job_title', 
        'job_location', 
        'job_via',
        'job_schedule_type', 
        'job_work_from_home', 
        'search_location',
        'job_posted_date', 
        'job_no_degree_mention', 
        'job_health_insurance',
        'job_country', 
        'salary_rate', 
        'salary_year_avg', 
        'salary_hour_avg',
        'company_name', 
        'job_skills', 
        'job_type_skills'
        ]

    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError (f"Dados incompletos: {missing_columns}")

    return df