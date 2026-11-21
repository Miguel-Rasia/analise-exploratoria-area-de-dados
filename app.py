from pathlib import Path
import sys

import plotly.express as px
import streamlit as st
from huggingface_hub import hf_hub_download


# Keep the current project structure: app.py at the root and modules in src/.
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
DATASET_PATH = BASE_DIR / "dataset" / "data_jobs.csv"
HF_DATASET_REPO = "lukebarousse/data_jobs"
HF_DATASET_REVISION = "ed776e5a0a8c40ea9d5efbd800772ae52e140f3e" 

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import data_analysis as da
import data_loader as dl
import translations


LANGUAGES = {
    "pt": translations.pt,
    "en": translations.en,
}

ERROR_TRANSLATIONS = {
    "invalid_home_office": "invalid_home_office",
    "invalid_limit": "invalid_limit",
    "invalid_salary_type": "invalid_salary_type",
    "missing_values": "missing_values",
}

MONTHS_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]

MONTHS_EN = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


@st.cache_data(show_spinner=False)
def load_data(path: str):
    return dl.load_dataset(path)


def format_number(value, decimals=0):
    if value is None:
        return "—"

    try:
        if value != value:
            return "—"
    except TypeError:
        pass

    if decimals:
        formatted = f"{value:,.{decimals}f}"
    else:
        formatted = f"{value:,.0f}"

    if st.session_state.get("language", "pt") == "pt":
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")

    return formatted


def format_currency(value, language):
    if value is None:
        return "—"

    try:
        if value != value:
            return "—"
    except TypeError:
        pass

    formatted = f"${value:,.2f}"
    if language == "pt":
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")

    return formatted


def show_error(error, text):
    error_identifier = str(error).split(":", 1)[0].strip()
    error_key = ERROR_TRANSLATIONS.get(error_identifier, "unknown_error")
    st.error(text[error_key])


def normalize_language(value):
    aliases = {
        "pt": "pt",
        "en": "en",
        "português": "pt",
        "portugues": "pt",
        "portuguese": "pt",
        "inglês": "en",
        "ingles": "en",
        "english": "en",
    }
    return aliases.get(str(value).strip().casefold(), "pt")


def sorted_options(series):
    values = series.dropna().astype(str).unique().tolist()
    return sorted(values, key=str.casefold)


def clear_filter_state():
    st.session_state["filter_country"] = []
    st.session_state["filter_job_title"] = []
    st.session_state["filter_schedule"] = []
    st.session_state["filter_home_office"] = "all"


# Streamlit page configuration must be the first Streamlit command.
initial_language = st.session_state.get("language", "pt")
initial_text = LANGUAGES.get(initial_language, translations.pt)

st.set_page_config(
    page_title=initial_text["app_title"],
    page_icon="📊",
    layout="wide",
)


if "language" not in st.session_state:
    st.session_state.language = "pt"

language = normalize_language(st.session_state.get("language", "pt"))
st.session_state.language = language
text = LANGUAGES[language]


# Header and language selector.
header_col, language_col = st.columns(
    [0.88, 0.12],
    vertical_alignment="top"
)

with header_col:
    st.title(text["app_title"])
    st.caption(text["app_subtitle"])

with language_col:
    with st.popover(
        "PT" if language == "pt" else "EN",
        help=text["language"],
        use_container_width=True
    ):
        selected_language = st.radio(
            text["language"],
            options=["pt", "en"],
            index=0 if language == "pt" else 1,
            format_func=lambda code: (
                text["portuguese"] if code == "pt"
                else text["english"]
            ),
            label_visibility="collapsed",
            key="language_choice_v2",
        )

        if selected_language != language:
            st.session_state.language = selected_language
            st.rerun()


st.divider()


# Resolve the dataset locally when present; otherwise download it from Hugging Face.
@st.cache_data(show_spinner=False)
def get_dataset_path():
    if DATASET_PATH.is_file():
        return str(DATASET_PATH)

    return hf_hub_download(
        repo_id=HF_DATASET_REPO,
        filename="data_jobs.csv",
        repo_type="dataset",
        revision=HF_DATASET_REVISION,
    )


# Download (if needed), prepare, and cache the dataset.
try:
    with st.spinner(text["app_subtitle"]):
        dataset_path = get_dataset_path()
        jobs_df = load_data(dataset_path)

except Exception as error:
    show_error(error, text)
    st.stop()


# Sidebar filters.
with st.sidebar:
    st.header(text["filters_title"])

    selected_countries = st.multiselect(
        text["filter_country"],
        options=sorted_options(jobs_df["job_country"]),
        placeholder=text["filter_all"],
        key="filter_country",
    )

    selected_titles = st.multiselect(
        text["filter_job_title"],
        options=sorted_options(jobs_df["job_title_short"]),
        placeholder=text["filter_all"],
        key="filter_job_title",
    )

    selected_schedules = st.multiselect(
        text["filter_schedule"],
        options=sorted_options(jobs_df["job_schedule_type"]),
        placeholder=text["filter_all"],
        key="filter_schedule",
    )

    home_office_options = ["all", "yes", "no"]

    selected_home_office = st.selectbox(
        text["filter_home_office"],
        options=home_office_options,
        format_func=lambda option: {
            "all": text["filter_all"],
            "yes": text["filter_yes"],
            "no": text["filter_no"],
        }[option],
        key="filter_home_office",
    )

    st.button(
        text["clear_filters"],
        use_container_width=True,
        on_click=clear_filter_state,
    )


home_office_value = {
    "all": None,
    "yes": True,
    "no": False,
}[selected_home_office]


# Apply filters.
try:
    filtered_df = da.filter_jobs(
        jobs_df,
        country=selected_countries or None,
        title=selected_titles or None,
        schedule=selected_schedules or None,
        home_office=home_office_value,
    )

except ValueError as error:
    show_error(error, text)
    st.stop()


# KPIs update with the active filters.
metrics = da.get_job_metrics(filtered_df)
metric_columns = st.columns(5)

metric_definitions = [
    ("total_jobs", format_number(metrics["total_jobs"])),
    ("total_countries", format_number(metrics["total_countries"])),
    ("total_companies", format_number(metrics["total_companies"])),
    ("remote_jobs", format_number(metrics["remote_jobs"])),
    (
        "remote_percentage",
        f"{format_number(metrics['remote_percentage'], 2)}%"
    ),
]

for column, (label_key, value) in zip(metric_columns, metric_definitions):
    column.metric(text[label_key], value)


st.divider()


# Download the currently filtered rows.
with st.sidebar:
    st.download_button(
        label=text["download_csv"],
        data=lambda: filtered_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="filtered_job_postings.csv",
        mime="text/csv",
        disabled=filtered_df.empty,
        use_container_width=True,
        key="download_filtered_data",
    )


if filtered_df.empty:
    st.info(text["no_results"])
    st.stop()


# Monthly postings and most demanded skills.
monthly_col, skills_col = st.columns(2, gap="large")

with monthly_col:
    st.subheader(text["jobs_by_month"])

    monthly_data = da.get_jobs_by_month(filtered_df)
    month_labels = MONTHS_PT if language == "pt" else MONTHS_EN
    monthly_data = monthly_data.copy()
    monthly_data["month"] = month_labels

    monthly_fig = px.line(
        monthly_data,
        x="month",
        y="total_jobs",
        markers=True,
        category_orders={"month": month_labels},
        labels={
            "month": text["month"],
            "total_jobs": text["number_of_jobs"],
        },
    )
    monthly_fig.update_layout(
        title=text["jobs_by_month"],
        margin=dict(l=20, r=20, t=55, b=20),
        xaxis=dict(tickangle=-45),
    )

    st.plotly_chart(
        monthly_fig,
        theme="streamlit",
        width="stretch",
        config={"displayModeBar": False},
    )


with skills_col:
    st.subheader(text["top_skills"])

    skills_limit = st.slider(
        text["skills_limit"],
        min_value=5,
        max_value=252,
        value=20,
        step=1,
        key="skills_limit",
    )

    skills_data = da.get_top_skills(filtered_df, limit=skills_limit)

    skills_fig = px.bar(
        skills_data,
        x="total_jobs",
        y="skill",
        orientation="h",
        labels={
            "total_jobs": text["number_of_jobs"],
            "skill": text["skill"],
        },
    )
    skills_fig.update_layout(
        title=text["top_skills"],
        yaxis={"autorange": "reversed"},
        margin=dict(l=20, r=20, t=55, b=20),
    )
    skills_fig.update_yaxes(automargin=True)
    skills_fig.update_layout(height=max(400, len(skills_data) * 30))

    st.plotly_chart(
        skills_fig,
        theme="streamlit",
        width="stretch",
        config={"displayModeBar": False},
    )


st.divider()


# Salary analysis keeps annual and hourly salaries separate.
st.subheader(text["salary_distribution"])

salary_type_label = st.radio(
    text["salary_type"],
    options=["salary_year_avg", "salary_hour_avg"],
    index=0,
    format_func=lambda value: (
        text["yearly_salary"]
        if value == "salary_year_avg"
        else text["hourly_salary"]
    ),
    horizontal=True,
    key="salary_type_choice_v2",
)

salary_metrics = da.get_salary_metrics(filtered_df, salary_type_label)

salary_metric_columns = st.columns(5)
salary_metric_items = [
    ("salary_count", format_number(salary_metrics["salary_count"])),
    ("salary_min", format_currency(salary_metrics["salary_min"], language)),
    ("salary_max", format_currency(salary_metrics["salary_max"], language)),
    ("salary_mean", format_currency(salary_metrics["salary_mean"], language)),
    ("salary_median", format_currency(salary_metrics["salary_median"], language)),
]

for column, (label_key, value) in zip(salary_metric_columns, salary_metric_items):
    column.metric(text[label_key], value)


if salary_metrics["salary_count"] == 0:
    st.info(text["no_salary_data"])
else:
    salary_data = filtered_df[[salary_type_label]].dropna()

    salary_unit = (
        "USD/ano"
        if language == "pt" and salary_type_label == "salary_year_avg"
        else "USD/hora"
        if language == "pt"
        else "USD/year"
        if salary_type_label == "salary_year_avg"
        else "USD/hour"
    )

    salary_fig = px.histogram(
        salary_data,
        x=salary_type_label,
        nbins=30,
        labels={salary_type_label: f"{text['salary']} ({salary_unit})"},
    )
    salary_fig.update_layout(
        title=text["salary_distribution"],
        yaxis_title=text["frequency"],
        xaxis_tickprefix="$",
        xaxis_tickformat=",.0f",
        margin=dict(l=20, r=20, t=55, b=20),
    )

    st.plotly_chart(
        salary_fig,
        theme="streamlit",
        width="stretch",
        config={"displayModeBar": False},
    )
