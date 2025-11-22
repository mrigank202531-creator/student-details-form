import streamlit as st
import pandas as pd
import os

# 1. CONFIGURATION
st.set_page_config(page_title="Student Details Form", page_icon="📝")

# File path for the simple database (CSV)
FILE_PATH = "student_data.csv"

# 2. TITLE AND INSTRUCTIONS
st.title("📝 Student Update Form")
st.write("Please fill in the details below to update the student record.")

# 3. THE FORM
# We use st.form so the page doesn't reload on every keystroke
with st.form("entry_form", clear_on_submit=True):
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name")
        roll_no = st.number_input("Roll Number", min_value=1, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
    with col2:
        student_class = st.selectbox("Class/Grade", ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"])
        section = st.text_input("Section (Optional)")
        dob = st.date_input("Date of Birth")

    address = st.text_area("Residential Address")
    
    # Submit Button
    submitted = st.form_submit_button("Save Data")

# 4. HANDLE SUBMISSION
if submitted:
    if not name or not address:
        st.error("⚠️ Please fill in at least the Name and Address fields.")
    else:
        # Create a dictionary for the new data
        new_data = {
            "Name": name,
            "Roll No": roll_no,
            "Gender": gender,
            "Class": student_class,
            "Section": section,
            "DOB": dob,
            "Address": address
        }
        
        # Convert to DataFrame
        new_df = pd.DataFrame([new_data])
        
        # Save/Append to CSV
        if os.path.exists(FILE_PATH):
            # Append without header
            new_df.to_csv(FILE_PATH, mode='a', header=False, index=False)
        else:
            # Create new with header
            new_df.to_csv(FILE_PATH, index=False)
            
        st.success(f"✅ Details for {name} saved successfully!")

# 5. DISPLAY DATA (Admin View)
st.divider()
st.subheader("📊 Current Records")

if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
    st.dataframe(df, use_container_width=True)
    
    # Allow user to download the data (Crucial for Cloud apps)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="student_records.csv",
        mime="text/csv",
    )
else:
    st.info("No data submitted yet.")