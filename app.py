import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================================
# CURRENT TIME - INDIA (IST)
# ==========================================================

current_time = datetime.now(ZoneInfo("Asia/Kolkata"))

# Task 1: 5 PM to 7 PM IST
show_task1 = 17 <= current_time.hour < 19

# Task 2: 6 PM to 8 PM IST
show_task2 = 17 <= current_time.hour < 20


# ==========================================================
# LOAD CSV FILES
# ==========================================================

apps = pd.read_csv("googleplaystore.csv")
reviews = pd.read_csv("googleplay_users_reviews..csv")


# ==========================================================
# MERGE DATASETS
# ==========================================================

df = pd.merge(
    apps,
    reviews,
    on="App",
    how="inner"
)


# ==========================================================
# CONVERT SIZE TO MB
# ==========================================================

def convert_size(size):

    size = str(size)

    if size.endswith("M"):
        return float(size[:-1])

    elif size.endswith("k"):
        return float(size[:-1]) / 1024

    else:
        return None


df["Size_MB"] = df["Size"].apply(convert_size)


# ==========================================================
# CONVERT INSTALLS TO NUMERIC
# ==========================================================

df["Installs"] = (
    df["Installs"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("+", "", regex=False)
)

df["Installs"] = pd.to_numeric(
    df["Installs"],
    errors="coerce"
)


# ==========================================================
# CONVERT NUMERIC COLUMNS
# ==========================================================

df["Rating"] = pd.to_numeric(
    df["Rating"],
    errors="coerce"
)

df["Reviews"] = pd.to_numeric(
    df["Reviews"],
    errors="coerce"
)

df["Sentiment_Subjectivity"] = pd.to_numeric(
    df["Sentiment_Subjectivity"],
    errors="coerce"
)


# ==========================================================
# TASK 1 : BUBBLE CHART
# ==========================================================

categories = [
    "GAME",
    "BEAUTY",
    "BUSINESS",
    "COMICS",
    "COMMUNICATION",
    "DATING",
    "ENTERTAINMENT",
    "SOCIAL",
    "EVENTS"
]


# Apply Task 1 Filters
filtered = df[
    (df["Rating"] > 3.5) &
    (df["Reviews"] > 500) &
    (df["Sentiment_Subjectivity"] > 0.5) &
    (df["Installs"] > 50000) &
    (df["Category"].isin(categories)) &
    (~df["App"].str.contains("S", case=False, na=False))
].copy()


# Translate Categories
filtered["Category"] = filtered["Category"].replace({

    "BEAUTY": "सौंदर्य",

    "BUSINESS": "வணிகம்",

    "DATING": "Partnersuche"
})


# Color Mapping
color_map = {

    "GAME": "pink",

    "सौंदर्य": "gold",

    "வணிகம்": "green",

    "COMICS": "orange",

    "COMMUNICATION": "red",

    "Partnersuche": "purple",

    "ENTERTAINMENT": "blue",

    "SOCIAL": "cyan",

    "EVENTS": "gray"
}


# Display Task 1
if show_task1:

    st.title(
        "Task 1 : Google Play Store Bubble Chart"
    )

    if len(filtered) == 0:

        st.warning(
            "No data available after applying filters."
        )

    else:

        fig1 = px.scatter(

            filtered,

            x="Size_MB",

            y="Rating",

            size="Installs",

            size_max=150,

            color="Category",

            color_discrete_map=color_map,

            hover_name="App",

            title=(
                "Bubble Chart: "
                "App Size (MB) vs Average Rating"
            ),

            labels={

                "Size_MB":
                "App Size (MB)",

                "Rating":
                "Average Rating"
            }
        )

        fig1.update_layout(

            width=1000,

            height=700
        )

        st.plotly_chart(

            fig1,

            use_container_width=True
        )

else:

    st.info(
        "Task 1 graph is available only "
        "between 5 PM and 7 PM IST."
    )


# ==========================================================
# TASK 2 : INTERACTIVE CHOROPLETH MAP
# ==========================================================

if show_task2:

    st.title(
        "Task 2 : Global Installs by Category"
    )


    # Read Dataset
    df2 = pd.read_csv(
        "googleplaystore.csv"
    )


    # Convert Installs to Numeric
    df2["Installs"] = (

        df2["Installs"]

        .astype(str)

        .str.replace(
            ",",
            "",
            regex=False
        )

        .str.replace(
            "+",
            "",
            regex=False
        )
    )


    df2["Installs"] = pd.to_numeric(

        df2["Installs"],

        errors="coerce"
    )


    # Remove Missing Values
    df2 = df2.dropna(

        subset=[
            "Category",
            "Installs"
        ]
    )


    # Remove Categories Starting with
    # A, C, G and S
    df2 = df2[

        ~df2["Category"]

        .str.upper()

        .str.startswith(

            (
                "A",
                "C",
                "G",
                "S"
            ),

            na=False
        )
    ]


    # Top 5 Categories by Total Installs
    top5 = (

        df2

        .groupby(

            "Category",

            as_index=False
        )["Installs"]

        .sum()

        .sort_values(

            "Installs",

            ascending=False
        )

        .head(5)
    )


    # Check Top 5 Categories
    if len(top5) < 5:

        st.warning(

            "Not enough categories available "
            "to create the Choropleth map."
        )


    else:

        # --------------------------------------------------
        # NOTE:
        # Original dataset does not contain Country data.
        # Sample countries are assigned only for visualization.
        # --------------------------------------------------

        countries = [

            "India",

            "United States",

            "Brazil",

            "Germany",

            "Australia"
        ]


        top5["Country"] = countries


        # Highlight Categories Above 1 Million Installs
        top5["Status"] = top5[

            "Installs"

        ].apply(

            lambda x:

            "Above 1 Million"

            if x > 1000000

            else "Below 1 Million"
        )


        # Create Choropleth Map
        fig2 = px.choropleth(

            top5,

            locations="Country",

            locationmode="country names",

            color="Status",

            hover_name="Category",

            hover_data={

                "Installs": True,

                "Country": True,

                "Status": True
            },

            color_discrete_map={

                "Above 1 Million":
                "red",

                "Below 1 Million":
                "lightblue"
            },

            title=(
                "Global Installs "
                "by Top 5 Categories"
            )
        )


        fig2.update_layout(

            width=1000,

            height=650
        )


        st.plotly_chart(

            fig2,

            use_container_width=True
        )


else:

    st.info(

        "Task 2 graph is available only "
        "between 6 PM and 8 PM IST."
    )
