import pandas as pd

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
    elif home_office is False:
        filtered_df = filtered_df[filtered_df['job_work_from_home'] == False]
    else:
        raise ValueError("Entrada inválida para Home-Office.")

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

    jobs_by_month = df['job_posted_date'].dt.month_name().value_counts()

    months = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']
    jobs_by_month = jobs_by_month.reindex(months, fill_value=0)

    df_months = jobs_by_month.reset_index()
    df_months.columns = ['month', 'total_jobs']

    return df_months

def get_top_skills(df, limit=20):

    if type(limit) != int or limit < 1:
        raise ValueError("Limite inválido.")

    if df.empty:
        return pd.DataFrame(columns=["skill", "total_jobs"])

    df_explode = df.explode('job_skills')
    top_skills = df_explode.value_counts('job_skills').head(limit)
    top_skills = top_skills.reset_index()
    top_skills.columns = ['skill', 'total_jobs']

    return top_skills

def get_salary_metrics(df, salary_type):

    if salary_type not in ['salary_year_avg', 'salary_hour_avg']:
        raise ValueError("Tipo de salário inválido.")

    salary_type = df[salary_type].dropna()

    metrics = {
        'salary_count': salary_type.shape[0],
        'salary_min': salary_type.min(),
        'salary_max': salary_type.max(),
        'salary_mean': salary_type.mean(),
        'salary_median': salary_type.median()
    }

    return metrics