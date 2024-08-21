import streamlit as st
import pandas as pd
import re

# Predefined subjects and options
compulsory_subjects = ["Innovation, Entrepreneurship and Start-ups (IES)", "Know yourself (KY)", "Professional Ethics (PE)"]
general_electives_1 = ["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"]
general_electives_2 = ["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"]
major_sectors = {
    "Sales and Marketing": ["Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)"],
    "Finance": ["Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)"],
    "Business Analytics and Operations": ["Programming for Analytics (PA)", "Data Mining and Visualization (DMV)", "AI and Machine Learning (AIML)"],
    "Media": ["Digital Media (DM)", "Media Production and Consumption (MPC)", "Media Research Tools and Analytics (MRTA)"],
    "HR": ["Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)"],
    "Logistics & Supply Chain": ["Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)"]
}
additional_subjects = [
    "Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)",
    "Marketing Analytics (Man)", "Strategic Brand Management (SBM)", "Financial Statement Analysis (FSA)",
    "Business Valuation (BussV)", "Security and Portfolio Management (SPM)", "International Finance (IF)",
    "Management of Banks (MoB)", "Programming for Analytics (PA)", "Text Mining and Sentiment Analytics (TM&SA)",
    "Data Mining and Visualization (DMV)", "Analytics for Service Operations (ASO)", "AI and Machine Learning (AIML)",
    "Digital Media (DM)", "Media Production and Consumption (MPC)", "Media and Sports Industry (MSI)",
    "Media Research Tools and Analytics (MRTA)", "Media Cost Management & Control (MCMC)", "Performance Management System (PMS)",
    "Talent Acquisition (TA)", "Learnings & Development (L&D)", "Compensation & Reward Management (C&RM)",
    "Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)",
    "Warehousing & Distribution Facilities Management (W&DFM)"
]

# Initialize profiles dictionary
if "profiles" not in st.session_state:
    st.session_state["profiles"] = {}

# Sidebar for navigation
st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to", ["Create Profile", "Generate Timetable"])

if pages == "Create Profile":
    st.title("Create Profile")
    name = st.text_input("Enter your name")
    enrollment_no = st.text_input("Enter your enrollment number")
    section = st.selectbox("Select your section", ["A", "B", "C"])

    st.subheader("Compulsory Subjects")
    for subject in compulsory_subjects:
        st.checkbox(subject, value=True, disabled=True)

    st.subheader("General Electives 1")
    elective_1 = st.selectbox("Choose one", general_electives_1)

    st.subheader("General Electives 2")
    elective_2 = st.selectbox("Choose one", general_electives_2)

    st.subheader("Major Sector")
    major_sector = st.selectbox("Choose a sector", list(major_sectors.keys()))
    for subject in major_sectors[major_sector]:
        st.checkbox(subject, value=True, disabled=True)

    st.subheader("Additional Subject")
    additional_subject = st.selectbox("Choose one", additional_subjects)

    if st.button("Save Profile"):
        st.session_state["profiles"][enrollment_no] = {
            "name": name,
            "section": section,
            "elective_1": elective_1,
            "elective_2": elective_2,
            "major_sector": major_sector,
            "additional_subject": additional_subject
        }
        st.success("Profile saved successfully!")

elif pages == "Generate Timetable":
    st.title("Generate Timetable")
    uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

    if uploaded_file:
        sheets = pd.read_excel(uploaded_file, sheet_name=None)
        timetable_sheet = sheets.get("MBA 2023-25_3RD SEMESTER")
        subjects_sheet = sheets.get("FACULTY DETAILS")

        if timetable_sheet is not None and subjects_sheet is not None:
            name = st.text_input("Enter your name to generate timetable")

            if name:
                # Find the profile based on the entered name
                profile = next((p for p in st.session_state["profiles"].values() if p["name"] == name), None)

                if profile:
                    # Extract selected subjects from profile
                    selected_subjects = [
                        profile["elective_1"],
                        profile["elective_2"],
                        *major_sectors[profile["major_sector"]],
                        profile["additional_subject"]
                    ]

                    selected_abbreviations = [sub.split('(')[-1].replace(')', '').strip() for sub in selected_subjects]

                    # Function to get the timetable for the selected section
                    def get_section_timetable(timetable_sheet, section):
                        section_start = {'A': 2, 'B': 16, 'C': 30}
                        start_row = section_start.get(section)
                        end_row = start_row + 12 if start_row is not None else None
                        if start_row is not None and end_row is not None:
                            return timetable_sheet.iloc[start_row:end_row]
                        return None

                    # Function to clean and filter timetable
                    def clean_cell_value(cell_value):
                        cell_value = re.sub(r'\[.*?\]', '', cell_value)
                        cell_value = re.sub(r'\(.*?\)', '', cell_value)
                        cell_value = cell_value.replace('/', ' ').strip()
                        return cell_value

                    def filter_and_blank_timetable_by_subjects(timetable, selected_subjects):
                        for index, row in timetable.iterrows():
                            for col in timetable.columns[1:]:  # Skip the first column (time slot)
                                cell_value = str(row[col]).strip()
                                cleaned_value = clean_cell_value(cell_value)
                                cell_subjects = cleaned_value.split()
                                if not any(sub in cell_subjects for sub in selected_subjects):
                                    timetable.at[index, col] = ""
                        return timetable

                    # Get the timetable for the user's section and filter it
                    section_timetable = get_section_timetable(timetable_sheet, profile["section"])

                    if section_timetable is not None:
                        personal_timetable = filter_and_blank_timetable_by_subjects(section_timetable, selected_abbreviations)
                        st.subheader("Your Personal Timetable")
                        st.dataframe(personal_timetable)
                    else:
                        st.error(f"Timetable for Section {profile['section']} not found.")
                else:
                    st.error("Profile not found for this name.")
        else:
            st.error("The required sheets are not found in the uploaded file.")
