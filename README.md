  ## PROJECT NAME
  Google Play Store Apps Bubble Chart Analysis using Python, Plotly & Streamlit

## Project Description

This project analyzes Google Play Store application data using Python, Pandas, Plotly, and Streamlit.

It combines app information with user review data to create an interactive Bubble Chart showing the relationship between **App Size (MB)** and **Average Rating**, where the bubble size represents the **Number of Installs**.

Multiple filters are applied to provide meaningful insights, and the application is deployed on **Streamlit Community Cloud**.

---

## Dataset

The project uses two CSV files:

- **googleplaystore.csv** – Contains application details.
- **googleplay_users_reviews.csv** – Contains user review data.

---

## Features

- Interactive Bubble Chart using Plotly
- App Size (MB) vs Average Rating visualization
- Bubble size represents Number of Installs
- Category-wise color mapping
- Dashboard available only between **5:00 PM and 7:00 PM IST**

### Filters Applied

- Rating > 3.5
- Reviews > 500
- Sentiment Subjectivity > 0.5
- Installs > 50,000
- Selected Categories only
- App name should not contain the letter **"S"**
- Category translation (Hindi, Tamil, German)
- Custom color mapping for categories

---

## Tools Used

- Python
- Pandas
- Plotly Express
- Streamlit
- GitHub
- Streamlit Community Cloud
- Visual Studio Code

---

## How to Run

1. Open the hosted Streamlit application using the provided Website URL.
2. Wait for the dashboard to load.
3. The Bubble Chart will be displayed only between **5:00 PM and 7:00 PM IST**.
4. Hover over any bubble to view the App Name, App Size, Rating, Installs, and Category.
5. Explore the interactive visualization to analyze the relationship between App Size, Rating, and Number of Installs.

---

## Live Demo

**Website:** 
- https://app-playstore-bubble-chart-qsge9tqslyj6asem6236pv.streamlit.app/

**GitHub Repository:**  
- https://github.com/ritesh-72/google-playstore-bubble-chart.git

**Dataset (Google Drive):** 
- https://drive.google.com/drive/folders/1r6bUkfvJVi4bI5z9fIhD5L5rytQvbBu3?usp=sharing
