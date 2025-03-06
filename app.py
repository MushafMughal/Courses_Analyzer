import json
import time
from dotenv import load_dotenv
import os
import PIL.Image
import pandas as pd
from google import genai
import streamlit as st
st.set_page_config(page_title="Course Data Extractor", layout="wide")

# load_dotenv() # Uncomment this line if you have a .env file
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Uncomment this line if you have a .env file

@st.cache_data
def initializing_dataframe():
    columns = [
    "Source File",  # New column for the source file name
    "Course name", "Course duration", "Course start date", 
    "Class day", "Course fee", "Fee type", "Course Outline / Summary"
    ]
    return pd.DataFrame(columns=columns)

df = initializing_dataframe()

@st.cache_data
def extract_course_data(image_path):
    prompt = f"""**Role**: You are a Senior Academic Data Extraction Specialist with 20+ years of experience in educational content analysis.
    
    **Task**: Analyze the following course advertisement image text and extract structured information with 99.9% accuracy. Do not infer or hallucinate any data beyond what is explicitly provided. If a field is ambiguous or missing, set its value to null.
    **Required Fields**:
    1. "Course name": Extract the official program title only (exclude any institution names).
    2. "Course duration": Extract the total length and its unit exactly as given. 
    3. "Course start date": Extract the start date in YYYY-MM-DD format. 
        - If year is missing, return date in MM-DD format.  
        - Otherwise, if no clear start date is provided, return null. 
    4. "Class day": Extract the weekday names (e.g., "Monday, Wednesday") from the schedule grid as a comma-separated string.
    5. "Course fee": Extract only the numerical value of the fee. Remove any currency symbols or non-numeric characters. Dont mix free demo or free trial with course fee. Make you dont make course fees free based on free orientation or demo.
    6. "Fee type": Extract exactly one of the following values based on the text: "One-time", "Monthly", "Weekly", or "Free". If none is explicitly mentioned, return null.
    7. "Course Outline / Summary": All relevent key modules/topics from curriculum section/outline/headlines. iF no bullet points or module list are given, but there is descriptive text about the course's goals or content, include that text as the outline. If there is no relevant descriptive text, return null.


    **Additional Format Rules**:
    - Output only a valid JSON object with the keys listed above.
    - If a field is ambiguous or not present, return null for that field.
    - Clean any text artifacts, watermarks, or logos from the image.
    - Remove any irrelevant information not related to the course content.
    - Dont include any information that is not explicitly mentioned in the image.
    - Remove any special characters or symbols from the extracted text.

    **Image Context**:
    - Academic brochure/flyer format.
    - Common sections: Title, Schedule, Fees, Curriculum.


    **Output**:
    """

    img = PIL.Image.open(image_path)
    response = client_gemini.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt, img]
    )

    try:
        # return json.loads(response.choices[0].message.content.replace('```json', '').replace('```', '').strip())
        return json.loads(response.text.replace('```json', '').replace('```', '').strip())
    except json.JSONDecodeError:
        print("Error parsing JSON, implementing fallback...")
        return {
            "Course name": None,
            "Course duration": None,
            "Course start date": None,
            "Class day": None,
            "Course fee": None,
            "Fee type": None,
            "Course Outline / Summary": None
        }

if "GEMINI_API_KEY" not in st.session_state:
    st.session_state["GEMINI_API_KEY"] = None

container = st.empty()

if not st.session_state["GEMINI_API_KEY"]:
    with container.container(border=True):
        GEMINI_API_KEY = st.text_input("Enter your Gemini API Key", type="password")
        if not GEMINI_API_KEY:
            st.stop()
        st.session_state["GEMINI_API_KEY"] = GEMINI_API_KEY

if st.session_state["GEMINI_API_KEY"]:
    container.empty()
    client_gemini = genai.Client(api_key=st.session_state["GEMINI_API_KEY"])

    # Streamlit UI setup
    a,b,c = st.columns([8, 1,1])
    with a:
        st.markdown(
        '<h1 style="text-align: left; margin-top: -1.8rem; letter-spacing: 1px; display: inline-block; width: 100%;">📚 Course Data Extractor from Images</h1>',
        unsafe_allow_html=True
        )
    with c:
        if st.button("Update Key"):
            st.session_state["GEMINI_API_KEY"] = None
            st.rerun()

    # File uploader
    data_type = st.radio("Courses Images", options=["Upload Images", "Use test data" ],horizontal=True)

    if data_type == "Use test data":
        uploaded_files = []
        test_data_dir = "test_data"  
        if os.path.exists(test_data_dir) and os.path.isdir(test_data_dir):
            for file_name in os.listdir(test_data_dir):
                file_path = os.path.join(test_data_dir, file_name)
                if os.path.isfile(file_path):
                    uploaded_files.append(file_path)

    if data_type == "Upload Images":
        uploaded_files = st.file_uploader("Upload Course Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_files:
        st.write("### Extracted Course Details")
        
        # Pagination setup
        total_courses = len(uploaded_files)
        
        colb, cola = st.columns([9, 1])
        with cola:
            page_size = st.selectbox("Courses Per Page", options=[5, 10, 25, 50], index=1)
        
        total_pages = max(1, (total_courses + page_size - 1) // page_size)
        
        with colb:
            page = st.selectbox("Show Page", options=list(range(1, total_pages + 1)), index=min(st.session_state.get('page', 1) - 1, total_pages - 1))

            st.session_state.page = page

        col1, col2, = st.columns([13,1])
        with col2:
            st.write(f"**Page {st.session_state.get('page', 1)} of {total_pages}**")
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        for uploaded_file in uploaded_files[start_idx:end_idx]:
            
            if data_type == "Use test data":
                file_name = os.path.basename(uploaded_file)
            
            if data_type == "Upload Images":
                file_name = uploaded_file.name

            with st.spinner(f"Processing {file_name}..."):
                image = PIL.Image.open(uploaded_file)
                extracted_data = extract_course_data(uploaded_file)
                extracted_data["Source File"] = file_name
                df = pd.concat([df, pd.DataFrame([extracted_data])], ignore_index=True)
            
            # Display each image and its extracted data in a bordered container
            with st.container():
                col1, col2 = st.columns([1, 2])
                
                # Display image
                with col1:
                    st.image(image, caption=file_name, use_column_width=True)
                
                # Display extracted data
                with col2:
                    st.write(f"**Course Name:** {extracted_data['Course name']}")
                    st.write(f"**Duration:** {extracted_data['Course duration']}")
                    st.write(f"**Start Date:** {extracted_data['Course start date']}")
                    st.write(f"**Class Days:** {extracted_data['Class day']}")
                    st.write(f"**Fee:** {extracted_data['Course fee']}")
                    st.write(f"**Fee Type:** {extracted_data['Fee type']}")
                    st.write(f"**Outline/Summary:** {extracted_data['Course Outline / Summary']}")
            # Add some space between results
            time.sleep(3)
            
            # Add some space between results
            st.markdown("---")
        
        # Download extracted data as CSV
        csv_data = df.to_csv(index=False)
        st.download_button("Download Extracted Data as CSV", csv_data, "extracted_courses.csv", "text/csv", key="download-csv")

        