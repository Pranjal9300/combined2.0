import streamlit as st
import pandas as pd
import re

# Predefined subjects
compulsory_subjects = ["Innovation, Entrepreneurship and Start-ups (IES)", "Know yourself (KY)", "Professional Ethics (PE)"]
general_electives_1 = ["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"]
general_electives_2 = ["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"]
major_sectors = {
    "Sales and Marketing": ["Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)"],
    "Finance": ["Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)"],
    "Business Analytics and Operations": ["Programing for Analytics (PA)", "Data Mining and Visualization (DMV)", "AI and Machine Learning (AIML)"],
    "Media": ["Digital Media (DM)", "Media Production and Consumption (MPC)", "Media Research Tools and Analytics (MRTA)"],
    "HR": ["Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)"],
    "Logistics & Supply Chain": ["Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)"]
}
additional_subjects = [
    "Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)",
    "Marketing Analytics (Man)", "Strategic Brand Management (SBM)", "Financial Statement Analysis (FSA)",
    "Business Valuation (BussV)", "Security and Portfolio Management (SPM)", "International Finance (IF)",
    "Management of Banks (MoB)", "Programing for Analytics (PA)", "Text Mining and Sentiment Analytics (TM&SA)",
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

# Load Excel files
def load_excel(file):
    # Load the entire Excel file
    return pd.read_excel(file, sheet_name=None)

def get_section_timetable(timetable_sheet, section):
    # Define where each section starts based on the section name
    section_start = {
        'A': 2,
        'B': 16,
        'C': 30
    }
    
    start_row = section_start.get(section)
    end_row = start_row + 12 if start_row is not None else None

    if start_row is not None and end_row is not None:
        section_timetable = timetable_sheet.iloc[start_row:end_row]
        return section_timetable
    else:
        return None

def clean_cell_value(cell_value):
    # Remove text within brackets and split by '/'
    cell_value = re.sub(r'\[.*?\]', '', cell_value)  # Remove text within square brackets
    cell_value = re.sub(r'\(.*?\)', '', cell_value)  # Remove text within round brackets
    cell_value = cell_value.replace('/', ' ').strip()  # Replace '/' with space and strip
    return cell_value

def filter_and_blank_timetable_by_subjects(timetable, selected_subjects):
    for index, row in timetable.iterrows():
        for col in timetable.columns[1:]:  # Skip the first column (time slot)
            cell_value = str(row[col]).strip()
            cleaned_value = clean_cell_value(cell_value)

            # Split the cleaned cell value into abbreviations
            cell_subjects = cleaned_value.split()

            # If none of the selected subjects match the cell subjects, blank it out
            if not any(sub in cell_subjects for sub in selected_subjects):
                timetable.at[index, col] = ""

    return timetable

def main():
    st.sidebar.title("Navigation")
    pages = st.sidebar.radio("Go to", ["Create/Edit Profile", "Generate Timetable"])

    if pages == "Create/Edit Profile":
        st.title("Create or Edit Profile")
        profile_action = st.radio("Select Action", ["Create Profile", "Edit/Delete Profile"])

        if profile_action == "Create Profile":
            st.subheader("Create New Profile")
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

        elif profile_action == "Edit/Delete Profile":
            st.subheader("Edit or Delete Profile")
            enrollment_no = st.text_input("Enter your enrollment number to search")

            if enrollment_no in st.session_state["profiles"]:
                profile = st.session_state["profiles"][enrollment_no]
                st.write(f"Name: {profile['name']}")
                st.write(f"Section: {profile['section']}")
                st.write(f"Elective 1: {profile['elective_1']}")
                st.write(f"Elective 2: {profile['elective_2']}")
                st.write(f"Major Sector: {profile['major_sector']}")
                st.write(f"Additional Subject: {profile['additional_subject']}")

                if st.button("Delete Profile"):
                    del st.session_state["profiles"][enrollment_no]
                    st.success("Profile deleted successfully!")

                if st.button("Edit Profile"):
                    st.session_state["profiles"][enrollment_no] = {
                        "name": st.text_input("Enter your name", value=profile['name']),
                        "section": st.selectbox("Select your section", ["A", "B", "C"], index=["A", "B", "C"].index(profile['section'])),
                        "elective_1": st.selectbox("Choose one", general_electives_1, index=general_electives_1.index(profile['elective_1'])),
                        "elective_2": st.selectbox("Choose one", general_electives_2, index=general_electives_2.index(profile['elective_2'])),
                        "major_sector": st.selectbox("Choose a sector", list(major_sectors.keys()), index=list(major_sectors.keys()).index(profile['major_sector'])),
                        "additional_subject": st.selectbox("Choose one", additional_subjects, index=additional_subjects.index(profile['additional_subject']))
                    }
                    st.success("Profile edited successfully!")

            else:
                st.info("No profile found for this enrollment number.")

    elif pages == "Generate Timetable":
        st.title("Personal Timetable Generator")

        uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

        if uploaded_file:
            sheets = load_excel(uploaded_file)
            timetable_sheet = sheets.get("MBA 2023-25_3RD SEMESTER")
            subjects_sheet = sheets.get("FACULTY DETAILS")

            if timetable_sheet is not None and subjects_sheet is not None:
                selected_enrollment_no = st.selectbox("Select your Enrollment Number", list(st.session_state["profiles"].keys()))

                if selected_enrollment_no:
                    profile = st.session_state["profiles"][selected_enrollment_no]
                    selected_section = profile["section"]
                    
                    st.subheader("Selected Subjects from Profile")
                    st.write(f"Elective 1: {profile['elective_1']}")
                    st.write(f"Elective 2: {profile['elective_2']}")
                    st.write(f"Major Sector: {profile['major_sector']}")
                    st.write(f"Additional Subject: {profile['additional_subject']}")

                    # Prepare subject list from the profile
                    selected_subjects = [
                        profile['elective_1'],
                        profile['elective_2'],
                        *major_sectors[profile['major_sector']],
                        profile['additional_subject']
                    ]

                    # Extract just the abbreviations to filter the timetable
                    selected_abbreviations = [sub.split('(')[-1].replace(')', '').strip() for sub in selected_subjects]

                    # Get the timetable for the selected section
                    section_timetable = get_section_timetable(timetable_sheet, selected_section)

                    if section_timetable is not None:
                        # Filter the timetable cell-wise and blank out unselected subjects
                        personal_timetable = filter_and_blank_timetable_by_subjects(section_timetable, selected_abbreviations)
                        st.subheader("Your Personal Timetable")
                        st.dataframe(personal_timetable)
                    else:
                        st.error(f"Timetable for Section {selected_section} not found.")
            else:
                st.error("The required sheets are not found in the uploaded file.")

if __name__ == "__main__":
    main()
