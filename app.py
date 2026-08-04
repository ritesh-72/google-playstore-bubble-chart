import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================================
# CURRENT TIME - INDIA (IST)
# ==========================================================

current_time = datetime.now(ZoneInfo("Asia/Kolkata"))

# Task 1: 5 PM to 7 PM IST
show_task1 = 17 <= current_time.hour < 24

# Task 2: 6 PM to 8 PM IST
show_task2 = 18 <= current_time.hour < 24

# Task 3: 6 PM to 9 PM IST
show_task3 = 18 <= current_time.hour < 24

# Task 4: 4 PM to 6 PM IST
show_task4 = 16 <= current_time.hour < 18


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


# ----------------------------------------------------------
# TASK 1 FILTERS
# ----------------------------------------------------------

filtered = df[
    (df["Rating"] > 3.5) &
    (df["Reviews"] > 500) &
    (df["Sentiment_Subjectivity"] > 0.5) &
    (df["Installs"] > 50000) &
    (df["Category"].isin(categories)) &
    (~df["App"].str.contains("S", case=False, na=False))
].copy()


# ----------------------------------------------------------
# TRANSLATE CATEGORIES
# ----------------------------------------------------------

filtered["Category"] = filtered["Category"].replace({

    "BEAUTY": "सौंदर्य",

    "BUSINESS": "வணிகம்",

    "DATING": "Partnersuche"

})


# ----------------------------------------------------------
# COLOR MAPPING
# ----------------------------------------------------------

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


# ----------------------------------------------------------
# DISPLAY TASK 1
# ----------------------------------------------------------

if show_task1:

    st.title(
        "Task 1 : Google Play Store Bubble Chart"
    )

    if filtered.empty:

        st.warning(
            "No data available after applying Task 1 filters."
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
                "Average Rating",

                "Installs":
                "Number of Installs"

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


    # ------------------------------------------------------
    # READ DATASET
    # ------------------------------------------------------

    df2 = pd.read_csv(
        "googleplaystore.csv"
    )


    # ------------------------------------------------------
    # CONVERT INSTALLS TO NUMERIC
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # REMOVE MISSING VALUES
    # ------------------------------------------------------

    df2 = df2.dropna(

        subset=[
            "Category",
            "Installs"
        ]

    )


    # ------------------------------------------------------
    # REMOVE CATEGORIES STARTING WITH
    # A, C, G AND S
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # TOP 5 CATEGORIES BY TOTAL INSTALLS
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # CHECK TOP 5
    # ------------------------------------------------------

    if len(top5) < 5:

        st.warning(

            "Not enough categories available "
            "to create the Choropleth map."

        )

    else:

        # --------------------------------------------------
        # NOTE:
        # Original dataset does not contain Country data.
        # Sample countries are assigned for visualization.
        # --------------------------------------------------

        countries = [

            "India",

            "United States",

            "Brazil",

            "Germany",

            "Australia"

        ]


        top5["Country"] = countries


        # --------------------------------------------------
        # HIGHLIGHT INSTALLS ABOVE 1 MILLION
        # --------------------------------------------------

        top5["Status"] = top5[

            "Installs"

        ].apply(

            lambda x:

            "Above 1 Million"

            if x > 1000000

            else "Below 1 Million"

        )


        # --------------------------------------------------
        # CREATE CHOROPLETH MAP
        # --------------------------------------------------

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


# ==========================================================
# TASK 3 : TIME SERIES LINE CHART
# ==========================================================

if show_task3:

    st.title(
        "Task 3 : Time Series Install Trend"
    )


    st.caption(
        "Task 3 uses the Last Updated month as the "
        "available time field in the dataset."
    )


    # ------------------------------------------------------
    # LOAD TASK 3 DATA
    # ------------------------------------------------------

    df3 = pd.read_csv(
        "googleplaystore.csv"
    )


    # ------------------------------------------------------
    # CONVERT INSTALLS TO NUMERIC
    # ------------------------------------------------------

    df3["Installs"] = (

        df3["Installs"]

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

    df3["Installs"] = pd.to_numeric(

        df3["Installs"],

        errors="coerce"

    )


    # ------------------------------------------------------
    # CONVERT REVIEWS TO NUMERIC
    # ------------------------------------------------------

    df3["Reviews"] = pd.to_numeric(

        df3["Reviews"],

        errors="coerce"

    )


    # ------------------------------------------------------
    # CONVERT LAST UPDATED TO DATE
    # ------------------------------------------------------

    df3["Last Updated"] = pd.to_datetime(

        df3["Last Updated"],

        errors="coerce"

    )


    # ------------------------------------------------------
    # REMOVE MISSING VALUES
    # ------------------------------------------------------

    df3 = df3.dropna(

        subset=[

            "App",

            "Category",

            "Installs",

            "Reviews",

            "Last Updated"

        ]

    )


    # ------------------------------------------------------
    # APPLY TASK 3 FILTERS
    # ------------------------------------------------------

    df3 = df3[

        # Reviews > 500
        (df3["Reviews"] > 500)

        &

        # App name should NOT start with X, Y or Z
        (~df3["App"]

         .str.upper()

         .str.startswith(

             ("X", "Y", "Z"),

             na=False

         ))

        &

        # App name should NOT contain letter S
        (~df3["App"]

         .str.contains(

             "S",

             case=False,

             na=False

         ))

        &

        # Category should start with E, C or B
        (df3["Category"]

         .str.upper()

         .str.startswith(

             ("E", "C", "B"),

             na=False

         ))

    ].copy()


    # ------------------------------------------------------
    # CHECK FILTERED DATA
    # ------------------------------------------------------

    if df3.empty:

        st.warning(

            "No data available after applying "
            "Task 3 filters."

        )

    else:

        # --------------------------------------------------
        # TRANSLATE CATEGORIES
        # --------------------------------------------------

        df3["Category"] = df3["Category"].replace({

            "BEAUTY":
            "सौंदर्य",

            "BUSINESS":
            "வணிகம்",

            "DATING":
            "Partnersuche"

        })


        # --------------------------------------------------
        # CREATE MONTH COLUMN
        # --------------------------------------------------

        df3["Month"] = (

            df3["Last Updated"]

            .dt.to_period("M")

            .dt.to_timestamp()

        )


        # --------------------------------------------------
        # GROUP BY MONTH AND CATEGORY
        # --------------------------------------------------

        monthly_data = (

            df3

            .groupby(

                [

                    "Month",

                    "Category"

                ],

                as_index=False

            )["Installs"]

            .sum()

            .sort_values(

                [

                    "Category",

                    "Month"

                ]

            )

        )


        # --------------------------------------------------
        # CALCULATE MONTH-OVER-MONTH GROWTH
        # --------------------------------------------------

        monthly_data["MoM_Growth"] = (

            monthly_data

            .groupby(

                "Category"

            )["Installs"]

            .pct_change()

            .mul(100)

        )


        # --------------------------------------------------
        # CREATE MAIN LINE CHART
        # --------------------------------------------------

        fig3 = px.line(

            monthly_data,

            x="Month",

            y="Installs",

            color="Category",

            markers=True,

            title=(

                "Time Series Trend of Total Installs "

                "by App Category"

            ),

            labels={

                "Month":
                "Month",

                "Installs":
                "Total Installs",

                "Category":
                "App Category"

            }

        )


        # --------------------------------------------------
        # FIND PERIODS WITH >20% GROWTH
        # --------------------------------------------------

        growth_data = monthly_data[

            monthly_data["MoM_Growth"] > 20

        ].copy()


        # --------------------------------------------------
        # HIGHLIGHT SIGNIFICANT GROWTH
        # --------------------------------------------------

        if not growth_data.empty:

            first_growth_trace = True


            for category in growth_data["Category"].unique():

                category_all = monthly_data[

                    monthly_data["Category"] == category

                ].sort_values(

                    "Month"

                )


                category_growth = growth_data[

                    growth_data["Category"] == category

                ].sort_values(

                    "Month"

                )


                for _, row in category_growth.iterrows():

                    current_month = row["Month"]

                    current_index = category_all.index[
                        category_all["Month"] == current_month
                    ].tolist()


                    if not current_index:

                        continue


                    current_position = (
                        category_all.index.get_loc(
                            current_index[0]
                        )
                    )


                    # Need previous month data
                    if current_position == 0:

                        continue


                    previous_row = category_all.iloc[
                        current_position - 1
                    ]


                    # Create a two-point shaded region
                    shade_x = [

                        previous_row["Month"],

                        current_month,

                        current_month,

                        previous_row["Month"]

                    ]


                    shade_y = [

                        0,

                        0,

                        row["Installs"],

                        previous_row["Installs"]

                    ]


                    fig3.add_trace(

                        go.Scatter(

                            x=shade_x,

                            y=shade_y,

                            fill="toself",

                            fillcolor=(
                                "rgba(255, 165, 0, 0.20)"
                            ),

                            line=dict(

                                width=0

                            ),

                            mode="lines",

                            name=(
                                "Growth > 20%"
                                if first_growth_trace
                                else category
                            ),

                            legendgroup="growth",

                            showlegend=first_growth_trace,

                            hoverinfo="skip"

                        )

                    )


                    first_growth_trace = False


        # --------------------------------------------------
        # GRAPH SETTINGS
        # --------------------------------------------------

        fig3.update_layout(

            width=1000,

            height=700,

            xaxis_title="Month",

            yaxis_title="Total Installs",

            legend_title="App Category",

            hovermode="x unified"

        )


        # --------------------------------------------------
        # DISPLAY GRAPH
        # --------------------------------------------------

        st.plotly_chart(

            fig3,

            use_container_width=True

        )


        # --------------------------------------------------
        # DISPLAY GROWTH TABLE
        # --------------------------------------------------

        if not growth_data.empty:

            st.subheader(

                "Periods with More Than 20% "
                "Month-over-Month Growth"

            )


            display_growth = growth_data[

                [

                    "Month",

                    "Category",

                    "Installs",

                    "MoM_Growth"

                ]

            ].copy()


            display_growth["MoM_Growth"] = (

                display_growth["MoM_Growth"]

                .round(2)

                .astype(str)

                + "%"

            )


            st.dataframe(

                display_growth,

                use_container_width=True

            )

        else:

            st.info(

                "No period with more than 20% "
                "Month-over-Month growth was found."

            )


else:

    st.info(

        "Task 3 graph is available only "
        "between 6 PM and 9 PM IST."

    )

# ==========================================================
# TASK 4 : STACKED AREA CHART
# ==========================================================

if show_task4:

    st.title(
        "Task 4 : Cumulative Installs by App Category"
    )

    # ------------------------------------------------------
    # LOAD TASK 4 DATA
    # ------------------------------------------------------

    df4 = pd.read_csv(
        "googleplaystore.csv"
    )

    # ------------------------------------------------------
    # CONVERT NUMERIC COLUMNS
    # ------------------------------------------------------

    df4["Rating"] = pd.to_numeric(
        df4["Rating"],
        errors="coerce"
    )

    df4["Reviews"] = pd.to_numeric(
        df4["Reviews"],
        errors="coerce"
    )

    # ------------------------------------------------------
    # CONVERT SIZE TO MB
    # ------------------------------------------------------

    df4["Size_MB"] = df4["Size"].apply(convert_size)

    # ------------------------------------------------------
    # CONVERT INSTALLS TO NUMERIC
    # ------------------------------------------------------

    df4["Installs"] = (
        df4["Installs"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("+", "", regex=False)
    )

    df4["Installs"] = pd.to_numeric(
        df4["Installs"],
        errors="coerce"
    )

    # ------------------------------------------------------
    # CONVERT LAST UPDATED TO DATE
    # ------------------------------------------------------

    df4["Last Updated"] = pd.to_datetime(
        df4["Last Updated"],
        errors="coerce"
    )

    # ------------------------------------------------------
    # TASK 4 FILTERS
    # ------------------------------------------------------

    df4 = df4[
        # Average Rating >= 4.2
        (df4["Rating"] >= 4.2)

        &

        # App name must NOT contain any numbers
        (~df4["App"]
         .astype(str)
         .str.contains(
             r"\d",
             regex=True,
             na=False
         ))

        &

        # Category starts with T or P
        (df4["Category"]
         .astype(str)
         .str.upper()
         .str.startswith(
             ("T", "P"),
             na=False
         ))

        &

        # Reviews > 1,000
        (df4["Reviews"] > 1000)

        &

        # App size between 20 MB and 80 MB
        (df4["Size_MB"] >= 20)

        &

        (df4["Size_MB"] <= 80)

    ].copy()

    # ------------------------------------------------------
    # REMOVE MISSING VALUES
    # ------------------------------------------------------

    df4 = df4.dropna(
        subset=[
            "App",
            "Category",
            "Installs",
            "Last Updated"
        ]
    )

    # ------------------------------------------------------
    # CHECK FILTERED DATA
    # ------------------------------------------------------

    if df4.empty:

        st.warning(
            "No data available after applying Task 4 filters."
        )

    else:

        # --------------------------------------------------
        # CREATE MONTH COLUMN
        # --------------------------------------------------

        df4["Month"] = (
            df4["Last Updated"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        # --------------------------------------------------
        # MONTHLY INSTALLS BY CATEGORY
        # --------------------------------------------------

        monthly4 = (
            df4
            .groupby(
                [
                    "Month",
                    "Category"
                ],
                as_index=False
            )["Installs"]
            .sum()
            .sort_values(
                [
                    "Category",
                    "Month"
                ]
            )
        )

        # --------------------------------------------------
        # CONVERT TO WIDE FORMAT
        # --------------------------------------------------

        pivot4 = (
            monthly4
            .pivot(
                index="Month",
                columns="Category",
                values="Installs"
            )
            .fillna(0)
            .sort_index()
        )

        # --------------------------------------------------
        # CUMULATIVE INSTALLS
        # --------------------------------------------------

        cumulative4 = pivot4.cumsum()

        # --------------------------------------------------
        # MONTH-OVER-MONTH GROWTH
        # A month is highlighted if ANY category grows >25%
        # --------------------------------------------------

        growth4 = pivot4.pct_change()

        highlight_months4 = growth4.index[
            (growth4 > 0.25).any(axis=1)
        ]

        # --------------------------------------------------
        # TRANSLATE LEGEND CATEGORY NAMES
        # --------------------------------------------------

        category_translation4 = {
            "Travel & Local": "Voyage et Local",
            "Productivity": "Productividad",
            "Photography": "写真"
        }

        cumulative4_display = cumulative4.rename(
            columns=category_translation4
        )

        # --------------------------------------------------
        # CREATE STACKED AREA CHART
        # --------------------------------------------------

        fig4 = go.Figure()

        for category in cumulative4.columns:

            display_category = category_translation4.get(
                category,
                category
            )

            fig4.add_trace(
                go.Scatter(
                    x=cumulative4.index,
                    y=cumulative4[category],
                    mode="lines",
                    name=display_category,
                    stackgroup="one",
                    line=dict(width=1.5),
                    hovertemplate=(
                        f"<b>{display_category}</b><br>"
                        "Month: %{x|%b %Y}<br>"
                        "Cumulative Installs: %{y:,.0f}"
                        "<extra></extra>"
                    )
                )
            )

        # --------------------------------------------------
        # HIGHLIGHT MONTHS WITH >25% MOM GROWTH
        # The stronger overlay visually increases intensity
        # for significant-growth months.
        # --------------------------------------------------

        first_highlight = True

        for month in highlight_months4:

            fig4.add_vrect(
                x0=month,
                x1=month + pd.DateOffset(months=1),
                fillcolor="rgba(255, 140, 0, 0.32)",
                line_width=0,
                layer="above",
                annotation_text=(
                    "Growth > 25%"
                    if first_highlight
                    else None
                ),
                annotation_position="top",
                annotation_font_size=10
            )

            first_highlight = False

        # --------------------------------------------------
        # GRAPH SETTINGS
        # --------------------------------------------------

        fig4.update_layout(
            width=1000,
            height=700,
            title=(
                "Cumulative Number of Installs "
                "Over Time by App Category"
            ),
            xaxis_title="Month",
            yaxis_title="Cumulative Installs",
            legend_title="App Category",
            hovermode="x unified"
        )

        # --------------------------------------------------
        # DISPLAY GRAPH
        # --------------------------------------------------

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

        st.caption(
            "Highlighted months indicate that at least one "
            "category increased by more than 25% "
            "month-over-month."
        )

else:

    st.info(
        "Task 4 graph is available only "
        "between 4 PM and 6 PM IST."
    )
