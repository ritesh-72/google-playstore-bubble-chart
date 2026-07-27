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

## Task 1: Google Play Store Bubble Chart

### Objective

The objective of Task 1 is to analyze the relationship between **App Size (in MB)** and **Average Rating**, while using the **number of installs as the bubble size**.

### Filters Applied

The bubble chart displays apps based on the following conditions:

* Rating greater than 3.5
* Reviews greater than 500
* Installs greater than 50,000
* Sentiment Subjectivity greater than 0.5
* Apps belonging to selected categories:

  * Game
  * Beauty
  * Business
  * Comics
  * Communication
  * Dating
  * Entertainment
  * Social
  * Events
* App names containing the letter "S" are excluded

### Visualization

The bubble chart represents:

* **X-axis:** App Size in MB
* **Y-axis:** Average Rating
* **Bubble Size:** Number of Installs
* **Bubble Color:** App Category

The **Game** category is highlighted using a pink color, while other categories are displayed using different colors.

Some category names are also translated for visualization:

* Beauty → सौंदर्य
* Business → வணிகம்
* Dating → Partnersuche

### Time Condition

Task 1 is available only between **5:00 PM and 7:00 PM IST**.

---

## Task 2: Interactive Choropleth Map

### Objective

The objective of Task 2 is to visualize the **top 5 app categories based on total installs** using an interactive Choropleth map.

### Data Processing

The following data processing steps were performed:

* Converted the Installs column into numeric format
* Removed missing values
* Excluded categories starting with:

  * A
  * C
  * G
  * S
* Grouped the data by Category
* Calculated total installs for each category
* Selected the top 5 categories based on total installs

### Visualization

The Choropleth map represents:

* **Country:** Geographic location displayed on the map
* **Category:** Top 5 app categories
* **Installs:** Total installs of each selected category
* **Status:** Indicates whether total installs are above or below 1 million

Categories with more than **1 million installs** are highlighted separately from categories below 1 million installs.

### Time Condition

Task 2 is available only between **6:00 PM and 8:00 PM IST**.


## Technologies Used

* Python
* Pandas
* Plotly Express
* Streamlit
* GitHub
* Streamlit Cloud

## How to Run the Project

1. Clone or download the GitHub repository.
2. Install the required Python libraries.
3. Open the project folder in VS Code or another Python IDE.
4. Run the Streamlit application using:

```bash
python -m streamlit run app.py
```

5. Open the local Streamlit URL in your web browser.

## Live Dashboard

The project is deployed using Streamlit Cloud.

[Add your Streamlit Cloud link here]

## GitHub Repository

[Add your GitHub repository link here]


## Live Demo

**Website:** 
- https://app-playstore-bubble-chart-qsge9tqslyj6asem6236pv.streamlit.app/

**GitHub Repository:**  
- https://github.com/ritesh-72/google-playstore-bubble-chart.git

**Dataset (Google Drive):** 
- https://drive.google.com/drive/folders/1r6bUkfvJVi4bI5z9fIhD5L5rytQvbBu3?usp=sharing
