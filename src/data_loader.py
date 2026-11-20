import pandas as pd
import ast

def load_dataset(path):
    dataframe = pd.read_csv(path)
    dataframe = validate_dataset(dataframe)
    dataframe = prepare_dataset(dataframe)
    return dataframe

def validate_dataset(dataframe):

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

    missing_columns = [column for column in required_columns if column not in dataframe.columns]

    if missing_columns:
        raise ValueError (f"Dados incompletos: {missing_columns}")

    return dataframe

def prepare_dataset(dataframe):

    df = dataframe.copy()

    df["job_posted_date"] = pd.to_datetime(df["job_posted_date"])

    df['job_skills'] = df['job_skills'].apply(parse_skills)

    return df

def parse_skills(skill):

    if isinstance(skill, list):
        return skill
    elif isinstance(skill, str):
        return ast.literal_eval(skill)
    elif pd.isna(skill):
        return skill