import os
from io import BytesIO
from html import escape
import pandas as pd
import streamlit as st

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="IEEMG Success Advisor Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# GLOBAL STYLES (MAROON THEME + LIGHT YELLOW BACKGROUND)
# ============================================================================
st.markdown(
    """
    <style>
    :root {
        --primary-maroon: #7A0000;
        --primary-maroon-soft: #A51C1C;
        --secondary-maroon: #5C0000;
        --accent-gold: #D4AF37;
        /* VERY LIGHT YELLOW BACKGROUND */
        --bg-color: #FFFDF2;
        --card-bg: #FFFFFF;
        --text-color: #111827;
        --muted-text: #6B7280;
        --border-color: #E5E7EB;
        --shadow-soft: 0 3px 8px rgba(15, 23, 42, 0.10);
    }

    .stApp {
        background-color: #FFF8DC;
        background-image:
            radial-gradient(ellipse at top left, rgba(255, 232, 158, 0.52), transparent 48%),
            linear-gradient(135deg, #FFF8DC 0%, #FFFDF2 52%, #FFF1C2 100%);
        color: var(--text-color);
        font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
    }

    /* TOP ROLE HEADER */
    .top-banner {
        background: linear-gradient(95deg, var(--primary-maroon), var(--primary-maroon-soft));
        color: white;
        padding: 1.0rem 1.5rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 22px rgba(0,0,0,0.25);
    }
    .top-banner-left {
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
    }
    .top-banner .sub-title {
        font-size: 0.7rem;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        font-weight: 600;
        opacity: 0.9;
    }
    .top-banner h1 {
        font-size: 1.35rem;
        margin: 0.15rem 0;
        font-weight: 700;
        letter-spacing: 0.2px;
    }
    .top-banner-description {
        font-size: 0.8rem;
        color: #FFECEC;
    }
    .role-badge {
        background: #FFFFFF;
        color: var(--primary-maroon);
        padding: 0.35rem 1.0rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.74rem;
        letter-spacing: 0.55px;
        text-transform: uppercase;
        box-shadow: 0 3px 9px rgba(0,0,0,0.20);
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        border: 1px solid rgba(122, 0, 0, 0.18);
    }

    .program-bar {
        background-color: #FFFFFF;
        padding: 0.85rem 1.1rem;
        border-radius: 10px;
        border: 1px solid var(--border-color);
        margin-bottom: 1.3rem;
        font-size: 0.9rem;
        color: var(--muted-text);
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: var(--shadow-soft);
    }
    .program-bar-title {
        font-weight: 600;
        color: var(--text-color);
    }
    .program-instance-badge,
    .instance-badge {
        display: inline-block;
        background: linear-gradient(135deg, #5C0000, #A51C1C);
        color: #FFFFFF;
        border: 1px solid #5C0000;
        border-radius: 8px;
        padding: 0.35rem 0.7rem;
        font-weight: 500;
        line-height: 1.4;
        box-shadow: none;
    }
    .program-instance-badge {
        margin-left: 0.35rem;
    }
    .active-instances {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.55rem;
        margin: 0.5rem 0 0.9rem;
        color: var(--text-color);
    }
    .program-tag {
        background-color: #FFF4D6;
        border-radius: 999px;
        padding: 0.15rem 0.8rem;
        font-size: 0.75rem;
        color: var(--primary-maroon);
        font-weight: 600;
        border: 1px solid #FCD34D;
    }

    /* CARDS */
    .card {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 0.9rem 1.0rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-soft);
        margin-bottom: 0.8rem;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .card:hover {
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.13);
        transform: translateY(-1px);
    }
    .card-header {
        font-size: 0.9rem;
        font-weight: 700;
        color: var(--primary-maroon);
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }
    .card-subtitle {
        font-size: 0.8rem;
        color: var(--muted-text);
        margin-bottom: 0.35rem;
    }

    /* Metric tiles */
    div[data-testid="stMetric"] {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-top: 4px solid var(--primary-maroon);
        padding: 14px 13px;
        border-radius: 10px;
        box-shadow: var(--shadow-soft);
    }
    div[data-testid="stMetric"] label {
        color: var(--muted-text) !important;
        font-weight: 600;
        font-size: 0.75rem !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--primary-maroon);
        font-weight: 700;
        font-size: 1.9rem !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 0.78rem !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.55rem;
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-bottom: 0 !important;
        border-radius: 14px;
        padding: 0.55rem;
        margin: 0.25rem 0 1rem;
        box-shadow: none;
    }
    .stTabs [role="tab"] {
        background: #FFFFFF !important;
        border-radius: 9px;
        padding: 0.65rem 1.1rem;
        font-weight: 600;
        border: 1px solid #D1D5DB;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        opacity: 1 !important;
        font-size: 0.92rem;
        box-shadow: none !important;
        outline: none !important;
        border-bottom: 0 !important;
    }
    .stTabs [role="tab"] *,
    .stTabs [role="tab"] p {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        opacity: 1 !important;
    }
    .stTabs [role="tab"]:hover {
        background: #FFFFFF !important;
        border-color: #D1D5DB !important;
        box-shadow: none !important;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background: #7A0000 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-color: #7A0000 !important;
        box-shadow: none !important;
        outline: none !important;
        border-bottom: 0 !important;
    }
    .stTabs [role="tab"][aria-selected="true"] *,
    .stTabs [role="tab"][aria-selected="true"] p {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
    }
    .stTabs [role="tablist"]::after,
    .stTabs [role="tablist"]::before,
    .stTabs [role="tab"]::after,
    .stTabs [role="tab"]::before,
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"],
    .stTabs [role="tab"][aria-selected="true"]::after,
    .stTabs [role="tab"][aria-selected="true"]::before {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        opacity: 0 !important;
        visibility: hidden !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }
    .stTabs [role="tablist"] {
        border-bottom: 0 !important;
    }
    .stTabs [role="tablist"] > div[aria-hidden="true"] {
        display: none !important;
        height: 0 !important;
        background: transparent !important;
        border: 0 !important;
    }
    .stTabs [role="tablist"] {
        border-bottom: 0 !important;
        box-shadow: none !important;
    }
    .stApp button:focus,
    .stApp button:focus-visible,
    .stApp button:active,
    .stApp input:focus,
    .stApp textarea:focus,
    .stApp select:focus,
    .stApp [role="combobox"]:focus,
    .stApp [role="combobox"]:focus-within,
    .stApp [role="checkbox"]:focus,
    .stApp [role="radio"]:focus,
    .stApp [data-baseweb="select"]:focus-within,
    .stApp [data-testid="stSelectbox"]:focus-within,
    .stApp [data-testid="stTextInput"]:focus-within,
    .stApp [data-testid="stTextArea"]:focus-within,
    .stApp [data-testid="stNumberInput"]:focus-within,
    .stApp [data-testid="stCheckbox"]:focus-within,
    .stApp [data-testid="stRadio"]:focus-within,
    .stApp [data-testid="stFileUploader"]:focus-within,
    .stApp [data-testid="stDateInput"]:focus-within,
    .stApp [data-testid="stTimeInput"]:focus-within {
        outline: none !important;
        box-shadow: none !important;
    }
    .stApp input:focus,
    .stApp textarea:focus,
    .stApp select:focus,
    .stApp [data-baseweb="select"]:focus-within {
        border-color: #D1D5DB !important;
    }
    .student-id-badge {
        display: inline-block;
        margin-left: 0.35rem;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        background: linear-gradient(135deg, #5C0000, #A51C1C);
        color: #FFFFFF;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        vertical-align: middle;
        box-shadow: 0 2px 5px rgba(92, 0, 0, 0.18);
    }
    /* Buttons */
    .stButton>button {
        background-color: var(--primary-maroon);
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: 600;
        padding: 0.4rem 1.0rem;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 2px 4px rgba(0,0,0,0.16);
        font-size: 0.83rem;
    }
    .stButton>button:hover {
        background-color: var(--secondary-maroon);
        color: white;
        transform: translateY(-1px);
    }

    h2, h3, h4 {
        color: var(--primary-maroon);
        font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
    }
    h2 {
        font-size: 1.05rem;
        margin-top: 0.55rem;
        margin-bottom: 0.35rem;
    }
    h3 {
        font-size: 0.98rem;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }

    .stDataFrame {
        border-radius: 8px;
        box-shadow: var(--shadow-soft);
    }

    /* Stage chips */
    .stage-chip {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        margin-right: 0.2rem;
        margin-bottom: 0.2rem;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .stage-chip-completed {
        background-color: #F0FDF4;
        color: #166534;
        border: 1px solid #86EFAC;
    }
    .stage-chip-progress {
        background-color: #FEF9C3;
        color: #92400E;
        border: 1px solid #FACC15;
    }
    .stage-chip-pending {
        background-color: #E5E7EB;
        color: #374151;
        border: 1px solid #D1D5DB;
    }
    .progress-section {
        background: linear-gradient(135deg, #FFFFFF, #FFF9E9);
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--accent-gold);
        border-radius: 12px;
        padding: 0.9rem 1rem 0.6rem;
        margin: 0.25rem 0 1rem;
    }
    .progress-section-title {
        color: var(--primary-maroon);
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    /* Risk badges */
    .risk-badge {
        display: inline-block;
        padding: 0.22rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .risk-badge-high {
        background-color: #FEE2E2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
    }
    .risk-badge-normal {
        background-color: #DBEAFE;
        color: #1D4ED8;
        border: 1px solid #93C5FD;
    }

    /* Footer */
    .footer-note {
        margin-top: 2.0rem;
        padding-top: 0.8rem;
        border-top: 1px solid var(--border-color);
        font-size: 0.75rem;
        color: var(--muted-text);
        text-align: left;
    }

    /* Sidebar background match */
    [data-testid="stSidebar"] {
        background-color: #FFFDF2 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# DATA LOADING - CSV ONLY
# ============================================================================
@st.cache_data
def load_default_csvs():
    required_files = [
        "students_roster.csv",
        "advisors_directory.csv",
        "enrollment_trends.csv",
    ]
    data_dir = os.path.dirname(os.path.abspath(__file__))
    missing = [
        filename
        for filename in required_files
        if not os.path.exists(os.path.join(data_dir, filename))
    ]
    if missing:
        st.error(
            "The following CSV files are missing beside `app.py`: "
            + ", ".join(missing)
            + ". Please place them in the same directory."
        )
        st.stop()
    students_df = pd.read_csv(os.path.join(data_dir, required_files[0]))
    advisers_df = pd.read_csv(os.path.join(data_dir, required_files[1]))
    history_df = pd.read_csv(os.path.join(data_dir, required_files[2]))
    return students_df, advisers_df, history_df


if "students_df" not in st.session_state:
    df_default, advisers_default, history_default = load_default_csvs()
    st.session_state["students_df"] = df_default
    st.session_state["advisers_df"] = advisers_default
    st.session_state["history_df"] = history_default

df = st.session_state["students_df"]
advisers_df = st.session_state["advisers_df"]
history_df = st.session_state["history_df"]

# Ensure required columns exist
required_cols = [
    "Student ID", "Student Name", "Cohort", "Advisor", "Risk",
    "Coursework", "Comp_Exam", "Capstone",
    "Time_In_Stage_Days", "Last_Updated"
]
for col in required_cols:
    if col not in df.columns:
        df[col] = ""


def get_stage_state(status):
    normalized_status = "" if pd.isna(status) else str(status).strip().casefold()
    if normalized_status in {
        "complete",
        "completed",
        "pass",
        "passed",
        "defended",
        "defended for completion",
    }:
        return "✅", "Complete"
    if "in-progress" in normalized_status or "ongoing" in normalized_status:
        return "🟡", "In progress"
    if "cancelled" in normalized_status or "incomplete" in normalized_status:
        return "⚠️", "Needs attention"
    return "⚪", "Not started"


def get_student_progress(student):
    stages = (
        (student.get("Coursework", ""), {"complete", "completed"}),
        (student.get("Comp_Exam", ""), {"pass", "passed", "complete", "completed"}),
        (
            student.get("Capstone", ""),
            {"defended", "defended for completion", "complete", "completed"},
        ),
    )
    completed = sum(
        ("" if pd.isna(status) else str(status).strip().casefold()) in completion_terms
        for status, completion_terms in stages
    )
    return round(completed / len(stages) * 100)


# ============================================================================
# SESSION STATE DEFAULTS
# ============================================================================
if "kpi_total_enrolled" not in st.session_state:
    st.session_state["kpi_total_enrolled"] = True
if "kpi_graduation" not in st.session_state:
    st.session_state["kpi_graduation"] = True
if "kpi_completion" not in st.session_state:
    st.session_state["kpi_completion"] = True
if "kpi_remaining" not in st.session_state:
    st.session_state["kpi_remaining"] = True
if "kpi_risk" not in st.session_state:
    st.session_state["kpi_risk"] = True
current_program = "Master of Management Engineering (MEM)"
legacy_program_names = (
    "Master of Management Engineering (IEEMG)",
    "Master of Management Engineering (MEM) - School of Industrial Engineering & "
    "Engineering Management (IE-EMG)",
)
if "cloned_instances" not in st.session_state:
    st.session_state["cloned_instances"] = [current_program]
if "active_program" not in st.session_state:
    st.session_state["active_program"] = current_program
if current_program not in st.session_state["cloned_instances"]:
    st.session_state["cloned_instances"].insert(0, current_program)
if st.session_state["active_program"] in legacy_program_names:
    st.session_state["active_program"] = current_program
st.session_state["cloned_instances"] = list(
    dict.fromkeys(
        current_program if program in legacy_program_names else program
        for program in st.session_state["cloned_instances"]
    )
)

KPI_STATE_KEYS = (
    "kpi_total_enrolled",
    "kpi_graduation",
    "kpi_completion",
    "kpi_remaining",
    "kpi_risk",
)

if "_default_csv_workspace" not in st.session_state:
    default_students_df, default_advisers_df, default_history_df = load_default_csvs()
    st.session_state["_default_csv_workspace"] = {
        "students_df": default_students_df.copy(deep=True),
        "advisers_df": default_advisers_df.copy(deep=True),
        "history_df": default_history_df.copy(deep=True),
        "kpi_settings": {key: True for key in KPI_STATE_KEYS},
    }


def capture_program_workspace():
    return {
        "students_df": st.session_state["students_df"].copy(deep=True),
        "advisers_df": st.session_state["advisers_df"].copy(deep=True),
        "history_df": st.session_state["history_df"].copy(deep=True),
        "kpi_settings": {
            key: st.session_state[key] for key in KPI_STATE_KEYS
        },
    }


if "_program_workspaces" not in st.session_state:
    st.session_state["_program_workspaces"] = {}

default_workspace = st.session_state["_default_csv_workspace"]
if current_program not in st.session_state["_program_workspaces"]:
    st.session_state["_program_workspaces"][current_program] = {
        "students_df": default_workspace["students_df"].copy(deep=True),
        "advisers_df": default_workspace["advisers_df"].copy(deep=True),
        "history_df": default_workspace["history_df"].copy(deep=True),
        "kpi_settings": default_workspace["kpi_settings"].copy(),
    }

if st.session_state["active_program"] not in st.session_state["_program_workspaces"]:
    st.session_state["_program_workspaces"][st.session_state["active_program"]] = (
        capture_program_workspace()
    )

default_workspace = st.session_state["_program_workspaces"][current_program]
for program in st.session_state["cloned_instances"]:
    if program not in st.session_state["_program_workspaces"]:
        st.session_state["_program_workspaces"][program] = {
            "students_df": default_workspace["students_df"].copy(deep=True),
            "advisers_df": default_workspace["advisers_df"].copy(deep=True),
            "history_df": default_workspace["history_df"].copy(deep=True),
            "kpi_settings": default_workspace["kpi_settings"].copy(),
        }


def save_active_program_workspace():
    st.session_state["_program_workspaces"][st.session_state["active_program"]] = (
        capture_program_workspace()
    )


def activate_program(program):
    save_active_program_workspace()
    workspace = st.session_state["_program_workspaces"][program]
    st.session_state["students_df"] = workspace["students_df"].copy(deep=True)
    st.session_state["advisers_df"] = workspace["advisers_df"].copy(deep=True)
    st.session_state["history_df"] = workspace["history_df"].copy(deep=True)
    for key, value in workspace["kpi_settings"].items():
        st.session_state[key] = value
    st.session_state["active_program"] = program
    st.rerun()


# ============================================================================
# HEADER HELPER
# ============================================================================
def render_header(role_text: str, description: str):
    program_name = escape(str(st.session_state["active_program"]))
    st.markdown(
        f"""
        <div class="top-banner">
            <div class="top-banner-left">
                <div class="sub-title">MAPÚA UNIVERSITY · IEEMG</div>
                <h1>IEEMG Success Advisor Dashboard — {program_name}</h1>
                <div class="top-banner-description">{description}</div>
            </div>
            <div>
                <span class="role-badge">● {role_text}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="program-bar">
            <div>
                <span class="program-bar-title">Program instance:</span>
                <span class="program-instance-badge">{escape(str(st.session_state["active_program"]))}</span>
            </div>
            <div>
                <span class="program-tag">Data Source: Local CSV Files (Offline, No SQL)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_tiles():
    total_students = len(df)
    at_risk_count = len(df[df["Risk"] == "AT RISK"])
    remaining = len(df[df["Capstone"] != "Defended for Completion"])
    last_completion = (
        str(history_df["Overall Completion Rate"].iloc[-1])
        if not history_df.empty and "Overall Completion Rate" in history_df.columns
        else "–"
    )
    last_grad = (
        str(history_df["On-Time Graduation Rate"].iloc[-1])
        if not history_df.empty and "On-Time Graduation Rate" in history_df.columns
        else "–"
    )

    kpi_row = st.columns(5)
    kpi_values = (
        ("kpi_total_enrolled", "Total Enrolled", str(total_students), None, "off"),
        ("kpi_graduation", "On-Time Graduation Rate", last_grad, "vs. last term", "normal"),
        ("kpi_completion", "Overall Completion %", last_completion, "Change vs. last term", "normal"),
        ("kpi_remaining", "Remaining Students", str(remaining), None, "normal"),
        ("kpi_risk", "Students At Risk", str(at_risk_count), "Overdue stages", "inverse"),
    )
    for column, (key, label, value, delta, delta_color) in zip(kpi_row, kpi_values):
        with column:
            if st.session_state[key]:
                st.metric(label, value, delta, delta_color=delta_color)
            else:
                st.metric(label, "Hidden")


# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Overview",
        "Roster",
        "Student Profile",
        "Admin Configuration",
    ]
)

# ============================================================================
# TAB 1: DEAN VIEW
# ============================================================================
with tab1:
    render_header(
        "Dean View",
        "High-level outcomes, completion rates, and risk profile for the IEEMG program.",
    )

    total_students = len(df)
    render_kpi_tiles()

    if st.session_state["kpi_completion"]:
        st.markdown(
            """
            <div class="progress-section">
                <div class="progress-section-title">🧭 Program milestone tracker</div>
                <div class="card-subtitle">Share of students who have completed each academic milestone.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        milestone_columns = st.columns(3)
        milestone_data = (
            ("📚 Coursework", "Coursework", {"complete", "completed"}),
            ("📝 Comprehensive exam", "Comp_Exam", {"pass", "passed", "complete", "completed"}),
            (
                "🎓 Capstone defended",
                "Capstone",
                {"defended", "defended for completion", "complete", "completed"},
            ),
        )
        for column, (label, field, completion_terms) in zip(
            milestone_columns, milestone_data
        ):
            completed_count = sum(
                ("" if pd.isna(status) else str(status).strip().casefold()) in completion_terms
                for status in df[field]
            )
            completion_rate = completed_count / total_students if total_students else 0
            with column:
                st.caption(f"{label} · {completed_count}/{total_students} students")
                st.progress(completion_rate)

    if st.session_state["kpi_completion"]:
        c1, c2 = st.columns((1.3, 1))
        with c1:
            st.markdown(
                """
                <div class="card">
                    <div class="card-header">Cohort Distribution by Lifecycle Stage</div>
                    <div class="card-subtitle">Shows how students are distributed across key milestones.</div>
                """,
                unsafe_allow_html=True,
            )
            stage_counts = {
                "Coursework Completed": len(df[df["Coursework"] == "Completed"]),
                "Comprehensive Exam In Progress": len(df[df["Comp_Exam"] == "In-Progress"]),
                "Capstone In Progress": len(df[df["Capstone"] == "In-Progress"]),
                "Capstone Defended / Completed": len(
                    df[df["Capstone"] == "Defended for Completion"]
                ),
            }
            stage_chart_df = (
                pd.DataFrame(
                    {"Lifecycle Stage": list(stage_counts.keys()), "Students": list(stage_counts.values())}
                )
                .set_index("Lifecycle Stage")
            )
            st.bar_chart(stage_chart_df, height=310, color="#A51C1C")
            st.caption("Columns indicate how many students are in each lifecycle band.")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown(
                """
                <div class="card">
                    <div class="card-header">Overall Completion Rate — Term Trend</div>
                    <div class="card-subtitle">Completion rate progression by term.</div>
                """,
                unsafe_allow_html=True,
            )
            if (
                not history_df.empty
                and "Term" in history_df.columns
                and "Overall Completion Rate" in history_df.columns
            ):
                trend_chart_df = history_df.copy()
                trend_chart_df["Overall Completion Rate"] = (
                    trend_chart_df["Overall Completion Rate"]
                    .astype(str)
                    .str.rstrip("%")
                    .astype(float)
                )
                trend_chart_df = trend_chart_df.set_index("Term")
                st.line_chart(
                    trend_chart_df["Overall Completion Rate"],
                    height=310,
                    color="#D4AF37",
                )
            else:
                st.info("Trend data not fully available in enrollment_trends.csv.")
            st.markdown("</div>", unsafe_allow_html=True)

    # At-risk table
    if st.session_state["kpi_risk"]:
        st.markdown(
            """
            <div class="card">
                <div class="card-header">Students At Risk — Escalation List</div>
                <div class="card-subtitle">Students flagged as AT RISK for immediate follow-up.</div>
            """,
            unsafe_allow_html=True,
        )
        risk_view_df = df[df["Risk"] == "AT RISK"].copy()
        if not risk_view_df.empty:
            risk_view_df = risk_view_df[
                [
                    "Student ID",
                    "Student Name",
                    "Cohort",
                    "Advisor",
                    "Coursework",
                    "Comp_Exam",
                    "Capstone",
                    "Time_In_Stage_Days",
                    "Last_Updated",
                ]
            ]
            st.dataframe(risk_view_df, use_container_width=True, hide_index=True)
        else:
            st.success("There are currently no students flagged as AT RISK.")
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TAB 2: PROGRAM CHAIR / ADVISOR VIEW
# ============================================================================
with tab2:
    render_header(
        "Program Chair / Advisor View",
        "Monitor cohort health, filter the roster, and view IEEMG faculty advisers.",
    )

    st.markdown(
        """
        <div class="card">
            <div class="card-header">Program Snapshot</div>
        """,
        unsafe_allow_html=True,
    )
    snapshot_metrics = [
        ("Cohorts Represented", df["Cohort"].nunique()),
        ("Active Advisors", df["Advisor"].nunique()),
    ]
    if st.session_state["kpi_completion"]:
        snapshot_metrics.append(
            ("Capstone Completed", len(df[df["Capstone"] == "Defended for Completion"]))
        )
    for column, (label, value) in zip(
        st.columns(len(snapshot_metrics)), snapshot_metrics
    ):
        with column:
            st.metric(label, value)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="card-header">Management Engineering Student Roster</div>
            <div class="card-subtitle">Filter by cohort, advisor, risk status, or search by name/ID.</div>
        """,
        unsafe_allow_html=True,
    )

    risk_filter_enabled = st.session_state["kpi_risk"]
    filter_columns = st.columns(4 if risk_filter_enabled else 3)
    with filter_columns[0]:
        sel_cohort = st.selectbox(
            "Cohort",
            ["All Cohorts"] + sorted(df["Cohort"].dropna().unique().tolist()),
        )
    with filter_columns[1]:
        sel_advisor = st.selectbox(
            "Advisor",
            ["All Advisors"] + sorted(df["Advisor"].dropna().unique().tolist()),
        )
    if risk_filter_enabled:
        with filter_columns[2]:
            sel_status = st.selectbox("Risk Status", ["All", "Normal", "AT RISK"])
    else:
        sel_status = "All"
    search_column = filter_columns[3] if risk_filter_enabled else filter_columns[2]
    with search_column:
        search_query = st.text_input(
            "Search Name or ID",
            placeholder="Type student name or ID...",
        )

    roster_filtered = df.copy()
    if sel_cohort != "All Cohorts":
        roster_filtered = roster_filtered[roster_filtered["Cohort"] == sel_cohort]
    if sel_advisor != "All Advisors":
        roster_filtered = roster_filtered[roster_filtered["Advisor"] == sel_advisor]
    if risk_filter_enabled and sel_status != "All":
        roster_filtered = roster_filtered[roster_filtered["Risk"] == sel_status]
    if search_query:
        mask = (
            roster_filtered["Student Name"].astype(str)
            .str.contains(search_query, case=False, na=False)
        ) | (
            roster_filtered["Student ID"].astype(str)
            .str.contains(search_query, case=False, na=False)
        )
        roster_filtered = roster_filtered[mask]

    roster_columns = [
        "Student ID",
        "Student Name",
        "Cohort",
        "Advisor",
        "Coursework",
        "Comp_Exam",
        "Capstone",
        "Last_Updated",
    ]
    if risk_filter_enabled:
        roster_columns.append("Risk")
    roster_display = roster_filtered[roster_columns].copy()
    if st.session_state["kpi_completion"]:
        roster_display.insert(
            7,
            "Progress",
            roster_filtered.apply(get_student_progress, axis=1).astype(str) + "%",
        )
    if risk_filter_enabled:
        roster_display["Risk"] = roster_display["Risk"].map(
            lambda risk: "🔴 AT RISK"
            if str(risk).strip().upper() == "AT RISK"
            else "🟢 Normal"
            if str(risk).strip().casefold() == "normal"
            else "⚪ Unknown"
        )
    st.dataframe(
        roster_display,
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="card-header">IEEMG Faculty Advisors</div>
            <div class="card-subtitle">List of program faculty and their advising assignments.</div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(advisers_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TAB 3: FACULTY / PROGRAM ADVISOR VIEW
# ============================================================================
with tab3:
    render_header(
        "Faculty / Program Advisor View",
        "View an individual student’s progress, risk level, and record notes for advising sessions.",
    )

    st.markdown(
        """
        <div class="card">
            <div class="card-header">Student Profile Viewer</div>
            <div class="card-subtitle">Filter by advisor and then select a student.</div>
        """,
        unsafe_allow_html=True,
    )

    filter_col1, filter_col2 = st.columns([1.4, 1])
    with filter_col1:
        advisor_filter = st.selectbox(
            "Filter by Advisor",
            ["All Advisors"] + sorted(df["Advisor"].dropna().unique().tolist()),
        )
    filtered_for_select = df.copy()
    if advisor_filter != "All Advisors":
        filtered_for_select = filtered_for_select[
            filtered_for_select["Advisor"] == advisor_filter
        ]

    with filter_col2:
        if filtered_for_select.empty:
            st.warning("No students found for that advisor. Showing all students.")
            filtered_for_select = df
        options = (
            filtered_for_select["Student ID"].astype(str)
            + " — "
            + filtered_for_select["Student Name"].astype(str)
        ).tolist()
        selected_student = st.selectbox("Select Student", options)

    st.markdown("</div>", unsafe_allow_html=True)

    # Student details
    s_id = selected_student.split(" — ")[0]
    student_record = df[df["Student ID"].astype(str) == s_id].iloc[0]
    student_name_html = escape(str(student_record["Student Name"]))
    student_id_html = escape(str(student_record["Student ID"]))

    st.markdown(
        f"""
        <div class="card">
            <div class="card-header">Student Overview</div>
            <div style="font-size:0.95rem; font-weight:600; margin-bottom:0.3rem;">
                {student_name_html} <span class="student-id-badge">{student_id_html}</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

    p_info1, p_info2, p_info3 = st.columns(3)
    with p_info1:
        st.write("**Cohort:**", student_record.get("Cohort", ""))
    with p_info2:
        st.write("**Advisor:**", student_record.get("Advisor", ""))
    with p_info3:
        if st.session_state["kpi_risk"]:
            risk_flag = student_record.get("Risk", "")
            time_days = student_record.get("Time_In_Stage_Days", "")
            if risk_flag == "AT RISK":
                risk_html = f'<span class="risk-badge risk-badge-high">AT RISK · {time_days} days in stage</span>'
            else:
                risk_html = f'<span class="risk-badge risk-badge-normal">Normal · {time_days} days in stage</span>'
            st.markdown(risk_html, unsafe_allow_html=True)

    if st.session_state["kpi_completion"]:
        st.markdown("#### 🧭 Student Progress Tracker")

        cw_status = "" if pd.isna(student_record.get("Coursework")) else str(student_record.get("Coursework"))
        ce_status = "" if pd.isna(student_record.get("Comp_Exam")) else str(student_record.get("Comp_Exam"))
        cp_status = "" if pd.isna(student_record.get("Capstone")) else str(student_record.get("Capstone"))
        last_updated = student_record.get("Last_Updated", "")

        student_progress = get_student_progress(student_record)
        st.progress(student_progress / 100)
        st.caption(f"Overall milestone completion · {student_progress}%")
        stage_columns = st.columns(3)
        for column, label, status in zip(
            stage_columns,
            ("📚 Coursework", "📝 Comprehensive exam", "🎓 Capstone"),
            (cw_status, ce_status, cp_status),
        ):
            icon, state = get_stage_state(status)
            with column:
                st.markdown(f"**{label}**")
                st.write(f"{icon} {status or 'Not started'}")
                st.caption(state)
        st.caption(f"Last lifecycle update recorded on: {last_updated}")

    st.markdown("#### Advisor Notes & Actions (Local Only)")
    st.caption(
        "Use this space to jot down advising notes for this session. Notes are not saved permanently in this prototype."
    )
    note_input = st.text_area(
        "Add New Progress Note",
        placeholder="Type meeting notes, action items, or observations...",
        height=120,
    )
    save_col1, _ = st.columns([0.25, 1])
    with save_col1:
        if st.button("Save Note"):
            if note_input.strip():
                st.success(
                    f"Note captured locally for {student_record['Student Name']} (not stored permanently)."
                )
            else:
                st.warning("Please enter note content before saving.")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TAB 4: IT / ADMIN VIEW
# ============================================================================
with tab4:
    render_header(
        "IT / Admin View",
        f"Manage program instances, KPI tiles, and CSV data sources for "
        f"{escape(str(st.session_state['active_program']))}.",
    )
    clone_generation = st.session_state.setdefault("_clone_generation", 0)

    st.markdown(
        """
        <div class="card">
            <div class="card-header">Program Instances</div>
            <div class="card-subtitle">Clone the current configuration for a new cohort or program variant.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("**Active Instances**")
    st.caption(
        "Select an instance to open its saved data and dashboard settings. "
        "Cloning copies the current data; each instance then keeps its own changes for this session."
    )
    for index, program in enumerate(st.session_state["cloned_instances"]):
        if st.button(
            program,
            key=f"activate_program_{index}",
            use_container_width=True,
        ) and program != st.session_state["active_program"]:
            activate_program(program)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="card-header">Overview KPI Visibility</div>
            <div class="card-subtitle">Control the KPI tiles and related progress or risk details shown on the Overview tab.</div>
        """,
        unsafe_allow_html=True,
    )
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.checkbox("Total Enrolled", key="kpi_total_enrolled")
    with k2:
        st.checkbox("On-Time Graduation Rate", key="kpi_graduation")
    with k3:
        st.checkbox("Overall Completion %", key="kpi_completion")
    with k4:
        st.checkbox("Remaining Students", key="kpi_remaining")
    with k5:
        st.checkbox("Students At Risk", key="kpi_risk")
    st.info(
        "These toggles control the KPI tiles and related sections in Overview only. Settings reset after restarting the app."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="card-header">Current Instance Data</div>
            <div class="card-subtitle">Preview the saved CSV datasets for the selected instance.</div>
        """,
        unsafe_allow_html=True,
    )

    for key, title in (
        ("students_df", "students_roster"),
        ("advisers_df", "advisors_directory"),
        ("history_df", "enrollment_trends"),
    ):
        with st.expander(
            f"{title} — {st.session_state['active_program']}",
            expanded=False,
        ):
            preview_df = st.session_state[key]
            st.caption(f"{len(preview_df):,} rows")
            st.dataframe(
                preview_df,
                use_container_width=True,
                hide_index=True,
                height=350,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="card-header">Clone Configuration</div>
            <div class="card-subtitle">Name the new instance and upload all three CSV datasets. The previewed data will be saved to the new instance and loaded into the dashboard.</div>
        """,
        unsafe_allow_html=True,
    )
    new_prog_name = st.text_input(
        "New Program Instance Name",
        value="",
        placeholder="Enter a program instance name",
        key=f"new_program_instance_name_{clone_generation}",
    )
    clone_col1, clone_col2, clone_col3 = st.columns(3)
    with clone_col1:
        students_file = st.file_uploader(
            "Students roster CSV",
            type=["csv"],
            key=f"clone_students_csv_{clone_generation}",
        )
    with clone_col2:
        advisers_file = st.file_uploader(
            "Advisors directory CSV",
            type=["csv"],
            key=f"clone_advisers_csv_{clone_generation}",
        )
    with clone_col3:
        history_file = st.file_uploader(
            "Enrollment trends CSV",
            type=["csv"],
            key=f"clone_history_csv_{clone_generation}",
        )

    clone_uploads = {
        "students_df": students_file,
        "advisers_df": advisers_file,
        "history_df": history_file,
    }
    clone_csvs = {}
    csv_errors = {}
    for key, upload in clone_uploads.items():
        if upload is None:
            continue
        try:
            clone_csvs[key] = pd.read_csv(BytesIO(upload.getvalue()))
        except (
            pd.errors.EmptyDataError,
            pd.errors.ParserError,
            UnicodeDecodeError,
            ValueError,
        ) as error:
            csv_errors[key] = str(error)

    if any(upload is not None for upload in clone_uploads.values()):
        st.markdown("##### New Instance CSV Preview")
        for key, title in (
            ("students_df", "Students roster"),
            ("advisers_df", "Advisors directory"),
            ("history_df", "Enrollment trends"),
        ):
            if key not in clone_csvs:
                continue
            preview_df = clone_csvs[key]
            with st.expander(
                f"{title} · {len(preview_df):,} rows",
                expanded=True,
            ):
                st.dataframe(
                    preview_df,
                    use_container_width=True,
                    hide_index=True,
                    height=350,
                )
    for key, error in csv_errors.items():
        st.error(f"Could not read {key} CSV: {error}")

    if st.button("+ Clone Configuration for New Instance"):
        if not new_prog_name:
            st.warning("Please enter a name for the new program instance.")
        elif new_prog_name.strip() != new_prog_name:
            st.warning("Remove leading or trailing spaces from the instance name.")
        elif new_prog_name in st.session_state["cloned_instances"]:
            st.warning(f"Instance `{new_prog_name}` already exists.")
        elif csv_errors:
            st.warning("Fix the CSV read errors above before cloning.")
        elif any(upload is None for upload in clone_uploads.values()):
            st.warning("Upload all three CSV files before cloning this instance.")
        else:
            save_active_program_workspace()
            current_workspace = st.session_state["_program_workspaces"][
                st.session_state["active_program"]
            ]
            cloned_workspace = {
                "students_df": current_workspace["students_df"].copy(deep=True),
                "advisers_df": current_workspace["advisers_df"].copy(deep=True),
                "history_df": current_workspace["history_df"].copy(deep=True),
                "kpi_settings": current_workspace["kpi_settings"].copy(),
            }
            for key, dataframe in clone_csvs.items():
                cloned_workspace[key] = dataframe.copy(deep=True)
            st.session_state["cloned_instances"].append(new_prog_name)
            st.session_state["_program_workspaces"][new_prog_name] = cloned_workspace
            st.session_state["active_program"] = new_prog_name
            workspace = st.session_state["_program_workspaces"][new_prog_name]
            st.session_state["students_df"] = workspace["students_df"].copy(deep=True)
            st.session_state["advisers_df"] = workspace["advisers_df"].copy(deep=True)
            st.session_state["history_df"] = workspace["history_df"].copy(deep=True)
            st.session_state["_clone_generation"] = clone_generation + 1
            st.session_state["_clone_created_notice"] = new_prog_name
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    created_program = st.session_state.pop("_clone_created_notice", None)
    if created_program:
        st.success(
            f"Created and opened `{created_program}` with its uploaded CSV datasets."
        )

# ============================================================================
# FOOTER
# ============================================================================
st.markdown(
    f"""
    <div class="footer-note">
        IEEMG Success Advisor Dashboard · Prototype for {escape(str(st.session_state["active_program"]))} ·
        Data source: Local CSV files · Rendered using Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)