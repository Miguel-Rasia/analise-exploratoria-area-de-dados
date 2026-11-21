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
    plt.show()

    return fig

def plot_top_skills(df):
    pass

def plot_salary_distribution(df):
    pass