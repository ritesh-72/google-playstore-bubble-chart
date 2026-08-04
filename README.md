# 📊 Google Play Store Data Analytics Dashboard

## 📌 Project Overview

This project is an interactive **Google Play Store Data Analytics Dashboard** developed using **Python, Pandas, Plotly, and Streamlit**.

The dashboard analyzes Google Play Store application data through multiple interactive visualizations. It provides insights into app ratings, reviews, installs, categories, app size, sentiment, growth trends, and Free vs Paid applications.

The project contains **6 analytical tasks**, each with specific filters and time-based graph availability.

---

## 🚀 Project Features

- Interactive Google Play Store data analysis
- Interactive Plotly visualizations
- Bubble Chart
- Choropleth Map
- Time Series Line Chart
- Stacked Area Chart
- Grouped Bar Chart
- Dual-Axis Chart
- Rating and review analysis
- Install analysis
- App category analysis
- Sentiment analysis
- Free vs Paid app comparison
- Revenue analysis
- Multilingual category labels
- Time-based graph visibility using IST

---

## 📈 Tasks & Visualizations

### Task 1 — Bubble Chart

A Bubble Chart is used to analyze the relationship between **App Size (MB)** and **Average Rating**, with bubble size representing the number of installs.

#### Filters

- Rating > 3.5
- Reviews > 500
- Installs > 50,000
- Sentiment Subjectivity > 0.5
- App name should not contain the letter `S`
- Categories:
  - Game
  - Beauty
  - Business
  - Comics
  - Communication
  - Dating
  - Entertainment
  - Social
  - Event
- Game category is highlighted in pink
- Category translations:
  - Beauty → Hindi
  - Business → Tamil
  - Dating → German

#### Availability

**5 PM – 7 PM IST**

---

### Task 2 — Interactive Choropleth Map

An interactive **Plotly Choropleth Map** is used to visualize installs by app category.

#### Filters

- Top 5 app categories
- Categories starting with `A`, `C`, `G`, or `S` are excluded
- Categories with installs exceeding 1 million are highlighted

#### Availability

**6 PM – 8 PM IST**

---

### Task 3 — Time Series Line Chart

A Time Series Line Chart is used to show the trend of total installs over time, segmented by app category.

#### Filters

- Reviews > 500
- App name should not start with:
  - X
  - Y
  - Z
- App name should not contain `S`
- App category should start with:
  - E
  - C
  - B
- Beauty → Hindi
- Business → Tamil
- Dating → German
- Areas with more than 20% month-over-month growth are highlighted

#### Availability

**6 PM – 9 PM IST**

---

### Task 4 — Stacked Area Chart

A Stacked Area Chart is used to visualize the cumulative number of installs over time for each app category.

#### Filters

- Average Rating >= 4.2
- App name should not contain numbers
- App category should start with:
  - T
  - P
- Reviews > 1,000
- App Size between 20 MB and 80 MB

#### Category Translation

- Travel & Local → French
- Productivity → Spanish
- Photography → Japanese

Months where installs increased by more than 25% month-over-month are highlighted.

#### Availability

**4 PM – 6 PM IST**

---

### Task 5 — Grouped Bar Chart

A Grouped Bar Chart is used to compare **Average Rating** and **Total Review Count** for the top 10 app categories by number of installs.

#### Filters

- Average Rating >= 4.0
- App Size >= 10 MB
- Last Updated month = January
- Top 10 categories are selected based on total installs

#### Availability

**3 PM – 5 PM IST**

---

### Task 6 — Dual-Axis Chart

A Dual-Axis Chart is used to compare **Average Installs** and **Revenue** for Free vs Paid apps within the top 3 app categories.

#### Filters

- Installs >= 10,000
- Revenue >= $10,000 for paid apps
- Android Version > 4.0
- App Size > 15 MB
- Content Rating = Everyone
- App name length <= 30 characters
- Spaces and special characters are included in the character count
- Top 3 categories are selected based on installs
- Free vs Paid applications are compared

#### Availability

**1 PM – 2 PM IST**

---

## 🛠️ Technologies Used

- **Python**
- **Pandas**
- **Plotly**
- **Streamlit**
- **Git**
- **GitHub**

---

## 📂 Datasets

This project uses two CSV datasets:

### 1. Google Play Store Dataset

**File:** `googleplaystore.csv`

Contains information such as:

- App
- Category
- Rating
- Reviews
- Size
- Installs
- Type
- Price
- Content Rating
- Last Updated
- Android Version

### 2. Google Play Store User Reviews Dataset

**File:** `googleplay_users_reviews.csv`

Contains:

- App
- Translated Review
- Sentiment
- Sentiment Polarity
- Sentiment Subjectivity

### 🔗 Dataset Link

**Google Drive – Datasets:**  
https://drive.google.com/drive/folders/1r6bUkfvJVi4bI5z9fIhD5L5rytQvbBu3?usp=sharing

---

## 💻 Source Code

The complete source code is available on GitHub.

**GitHub Repository:**  
https://github.com/ritesh-72/google-playstore-bubble-chart.git

---

## 🌐 Live Demo

The project is deployed using Streamlit.

**Live Dashboard:**  
https://app-playstore-bubble-chart-qsge9tqslyj6asem6236pv.streamlit.app/

---

## ⚙️ How to Run the Project Locally

### Step 1 — Clone the Repository

```bash
git clone https://github.com/ritesh-72/google-playstore-bubble-chart.git
