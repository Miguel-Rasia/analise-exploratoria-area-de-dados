import data_analysis as da
from matplotlib import pyplot as plt

def plot_jobs_by_month(df):
    data = da.get_jobs_by_month(df)
    fig, ax = plt.subplots()
    ax.plot(data['month'], data['total_jobs'])
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Jobs')
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_title("Total Jobs per month")

    return fig

def plot_top_skills(df):

    data = da.get_top_skills(df)

    fig, ax = plt.subplots()
    ax.barh(data['skill'], data['total_jobs'])
    ax.invert_yaxis()
    ax.set_xlabel('Total Jobs')
    ax.set_ylabel('Skill')
    ax.set_title("Most demanded skills")

    return fig

def plot_salary_distribution(df):
    pass