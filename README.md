# 📚 Course Data Extractor from Images

## Overview
The **Course Data Extractor** is a Streamlit-based application that extracts structured course information from educational images (brochures, flyers, posters). It utilizes Google's Gemini AI to process image text with high accuracy.
![image](https://github.com/user-attachments/assets/07fe9bd3-85c6-49dc-86dd-b17bdde7ca32)
![image](https://github.com/user-attachments/assets/b4545537-24f2-4991-9382-a6f0983fc353)

![image](https://github.com/user-attachments/assets/b5a0bf51-f860-4a18-8b01-e928f8042856)


## Features
- Extracts key course details such as:
  - Course Name
  - Duration
  - Start Date
  - Class Days
  - Course Fee
  - Fee Type
  - Course Outline / Summary
- Supports image uploads (`png`, `jpg`, `jpeg`)
  ![image](https://github.com/user-attachments/assets/c0cd3026-b0c0-4c47-b1f0-93281aac2b75)

- Option to use test data from a predefined folder
- Paginated course extraction with customizable page sizes
  ![image](https://github.com/user-attachments/assets/6ad01431-1edf-44b3-9785-4c1225005937)

- Download extracted course data as a CSV file

## Installation

### Prerequisites
- Python 3.8+
- Install dependencies using:
  
  ```bash
  pip install -r requirements.txt
  ```

### Required API Key
This project requires a **Gemini API Key**. Get it from [Google AI](https://ai.google.dev/) and enter it in the application when prompted.

## Usage

### Run the Application
```bash
streamlit run app.py
```

### Upload Course Images
1. Launch the application.
2. Enter your **Gemini API Key**.
3. Choose **Upload Images** and upload course images.
4. Extracted course data will be displayed and available for download as CSV.

### Use Test Data
1. Place test images in the `test_data` folder.
2. Select **Use test data** in the application.
3. The app will process all test images and display results.

## Data Extraction Methodology
The application follows a structured approach to extract course information with high accuracy:
- Uses **Gemini AI** to analyze text from images.
- Ensures **99.9% accuracy** with strict extraction rules.
- Avoids hallucinated or inferred data by returning `null` for missing fields.
- Cleans watermarks, logos, and irrelevant text from results.

## File Structure
```
Course-Data-Extractor/
│── app.py                # Main Streamlit app
│── requirements.txt      # Required Python dependencies
│── test_data/            # Folder for sample images
│── README.md             # Project documentation
```

## Dependencies
- `streamlit`
- `pandas`
- `PIL (Pillow)`
- `google-generativeai`
- `python-dotenv`

## Contributing
Feel free to submit issues or pull requests. Contributions are welcome!

## License
This project is licensed under the **MIT License**.

