import data_analysis as da
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter as ff

def plot_jobs_by_month(df):
    data = da.get_jobs_by_month(df)
    fig, ax = plt.subplots()
    ax.plot(data['month'], data['total_jobs'])
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Jobs')
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_title("Total Jobs per month")

    return fig

def plot_top_skills(df, limit=20):

    if type(limit) != int or limit < 1:
        raise ValueError("Limite inválido.")

    data = da.get_top_skills(df, limit=limit)

    fig, ax = plt.subplots()
    ax.barh(data['skill'], data['total_jobs'])
    ax.invert_yaxis()
    ax.set_xlabel('Total Jobs')
    ax.set_ylabel('Skill')
    ax.set_title("Most demanded skills")

    return fig

def plot_salary_distribution(df, salary_type):

    if salary_type not in ['salary_year_avg', 'salary_hour_avg']:
        raise ValueError("Tipo de salário inválido.")

    data = df[salary_type].dropna()

    fig, ax = plt.subplots()
    ax.hist(data, bins=30)
    if salary_type == 'salary_year_avg':
        ax.set_title('Average Yearly Salary')
        ax.set_xlabel('$USD/year')
    else:
        ax.set_title('Average Hourly Salary')
        ax.set_xlabel('$USD/hour')
    ax.xaxis.set_major_formatter(ff(lambda x, pos: f"${x:,.0f}"))
    ax.set_ylabel('Frequency')

    return fig