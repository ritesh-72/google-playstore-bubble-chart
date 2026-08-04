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
show_task1 = 17 <= current_time.hour < 19 # 5 PM–7 PM IST

# Task 2: 6 PM to 8 PM IST
show_task2 = 18 <= current_time.hour < 20  # 6 PM–8 PM IST

# Task 3: 6 PM to 9 PM IST
show_task3 = 18 <= current_time.hour < 21  # 6 PM–9 PM IST

# Task 4: 4 PM to 6 PM IST
show_task4 = 16 <= current_time.hour < 18  # 4 PM–6 PM IST

# Task 5: 3 PM to 5 PM IST
show_task5 = 15 <= current_time.hour < 17  # 3 PM–5 PM IST

# Task 6: 1 PM to 2 PM IST
show_task6 = 13 <= current_time.hour < 14  # 1 PM–2 PM IST


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


# Task 2 uses the available dataset fields; the source CSV has no country field.
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
            "TRAVEL_AND_LOCAL": "Voyage et Local",
            "PRODUCTIVITY": "Productividad",
            "PHOTOGRAPHY": "写真"
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

        for month in highlight_months4:

            fig4.add_vrect(
                x0=month,
                x1=month + pd.DateOffset(months=1),
                fillcolor="rgba(255, 140, 0, 0.22)",
                line_width=0,
                layer="below"
            )

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

# ==========================================================
# TASK 5 : GROUPED BAR CHART
# ==========================================================

if show_task5:

    st.title(
        "Task 5 : Average Rating vs Total Reviews"
    )

    # ------------------------------------------------------
    # LOAD TASK 5 DATA
    # ------------------------------------------------------

    df5 = pd.read_csv(
        "googleplaystore.csv"
    )

    # ------------------------------------------------------
    # CONVERT NUMERIC COLUMNS
    # ------------------------------------------------------

    df5["Rating"] = pd.to_numeric(
        df5["Rating"],
        errors="coerce"
    )

    df5["Reviews"] = pd.to_numeric(
        df5["Reviews"],
        errors="coerce"
    )

    # ------------------------------------------------------
    # CONVERT SIZE TO MB
    # ------------------------------------------------------

    df5["Size_MB"] = df5["Size"].apply(convert_size)

    # ------------------------------------------------------
    # CONVERT INSTALLS TO NUMERIC
    # ------------------------------------------------------

    df5["Installs"] = (
        df5["Installs"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("+", "", regex=False)
    )

    df5["Installs"] = pd.to_numeric(
        df5["Installs"],
        errors="coerce"
    )

    # ------------------------------------------------------
    # CONVERT LAST UPDATED TO DATE
    # ------------------------------------------------------

    df5["Last Updated"] = pd.to_datetime(
        df5["Last Updated"],
        errors="coerce"
    )

    # ------------------------------------------------------
    # TASK 5 FILTERS
    # ------------------------------------------------------

    df5 = df5[
        # Average Rating must be at least 4.0
        (df5["Rating"] >= 4.0)

        &

        # App Size must be at least 10 MB
        (df5["Size_MB"] >= 10)

        &

        # Last Updated month must be January
        (df5["Last Updated"].dt.month == 1)

    ].copy()

    # ------------------------------------------------------
    # REMOVE MISSING VALUES
    # ------------------------------------------------------

    df5 = df5.dropna(
        subset=[
            "Category",
            "Installs",
            "Rating",
            "Reviews"
        ]
    )

    # ------------------------------------------------------
    # CHECK FILTERED DATA
    # ------------------------------------------------------

    if df5.empty:

        st.warning(
            "No data available after applying Task 5 filters."
        )

    else:

        # --------------------------------------------------
        # TOP 10 CATEGORIES BY TOTAL INSTALLS
        # --------------------------------------------------

        top10_categories5 = (
            df5
            .groupby(
                "Category",
                as_index=False
            )
            .agg(
                Total_Installs=("Installs", "sum"),
                Average_Rating=("Rating", "mean"),
                Total_Reviews=("Reviews", "sum")
            )
            .sort_values(
                "Total_Installs",
                ascending=False
            )
            .head(10)
        )

        # --------------------------------------------------
        # CREATE GROUPED BAR CHART
        # --------------------------------------------------

        fig5 = go.Figure()

        # Average Rating bars
        fig5.add_trace(
            go.Bar(
                x=top10_categories5["Category"],
                y=top10_categories5["Average_Rating"],
                name="Average Rating",
                yaxis="y",
                offsetgroup="rating",
                width=0.32,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Average Rating: %{y:.2f}"
                    "<extra></extra>"
                )
            )
        )

        # Total Review Count bars
        fig5.add_trace(
            go.Bar(
                x=top10_categories5["Category"],
                y=top10_categories5["Total_Reviews"],
                name="Total Review Count",
                yaxis="y2",
                offsetgroup="reviews",
                width=0.32,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Total Reviews: %{y:,.0f}"
                    "<extra></extra>"
                )
            )
        )

        # --------------------------------------------------
        # GRAPH SETTINGS
        # --------------------------------------------------

        fig5.update_layout(
            barmode="group",
            width=1000,
            height=700,
            title=(
                "Top 10 App Categories by Installs: "
                "Average Rating vs Total Review Count"
            ),
            xaxis=dict(
                title="App Category",
                tickangle=-35
            ),
            yaxis=dict(
                title="Average Rating",
                range=[0, 5.2]
            ),
            yaxis2=dict(
                title="Total Review Count",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            legend_title="Metric",
            hovermode="x unified"
        )

        # --------------------------------------------------
        # DISPLAY GRAPH
        # --------------------------------------------------

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

        st.caption(
            "Filters: Average Rating >= 4.0, "
            "Size >= 10 MB, and Last Updated in January. "
            "Top 10 categories are selected by total installs. "
            "Average Rating and Total Reviews use separate y-axes."
        )

else:

    st.info(
        "Task 5 graph is available only "
        "between 3 PM and 5 PM IST."
    )

# ==========================================================
# TASK 6 : DUAL-AXIS CHART
# ==========================================================

if show_task6:

    st.title(
        "Task 6 : Average Installs vs Revenue — Free vs Paid"
    )

    # ------------------------------------------------------
    # LOAD TASK 6 DATA
    # ------------------------------------------------------

    df6 = pd.read_csv(
        "googleplaystore.csv"
    )

    # ------------------------------------------------------
    # CONVERT NUMERIC COLUMNS
    # ------------------------------------------------------

    df6["Rating"] = pd.to_numeric(
        df6["Rating"],
        errors="coerce"
    )

    df6["Installs"] = (
        df6["Installs"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("+", "", regex=False)
    )

    df6["Installs"] = pd.to_numeric(
        df6["Installs"],
        errors="coerce"
    )

    # ------------------------------------------------------
    # CLEAN SIZE
    # ------------------------------------------------------

    df6["Size_MB"] = df6["Size"].apply(convert_size)

    # ------------------------------------------------------
    # ANDROID VERSION
    # Extract the first numeric version from values such
    # as "4.1 and up".
    # ------------------------------------------------------

    df6["Android_Version_Num"] = pd.to_numeric(
        df6["Android Ver"]
        .astype(str)
        .str.extract(r"(\d+(?:\.\d+)?)")[0],
        errors="coerce"
    )

    # ------------------------------------------------------
    # CLEAN PRICE AND CALCULATE REVENUE
    # Revenue = installs × price for paid apps.
    # Free apps have revenue = 0.
    # ------------------------------------------------------

    df6["Price_Num"] = (
        df6["Price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )

    df6["Price_Num"] = pd.to_numeric(
        df6["Price_Num"],
        errors="coerce"
    )

    df6["Price_Num"] = df6["Price_Num"].fillna(0)

    df6["App_Type"] = df6["Type"].astype(str).str.strip().str.title()

    df6["App_Type"] = df6["App_Type"].where(
        df6["App_Type"].isin(["Free", "Paid"]),
        "Unknown"
    )

    df6["Revenue"] = (
        df6["Installs"] * df6["Price_Num"]
    )

    # ------------------------------------------------------
    # TASK 6 FILTERS
    # ------------------------------------------------------

    df6 = df6[
        # At least 10,000 installs
        (df6["Installs"] >= 10000)

        &

        # Android version > 4.0
        (df6["Android_Version_Num"] > 4.0)

        &

        # Size > 15 MB
        (df6["Size_MB"] > 15)

        &

        # Content Rating must be Everyone
        (df6["Content Rating"].astype(str).str.strip() == "Everyone")

        &

        # App name <= 30 characters, including spaces
        # and special characters
        (df6["App"].astype(str).str.len() <= 30)

        &

        # Only Free and Paid apps
        (df6["App_Type"].isin(["Free", "Paid"]))

    ].copy()

    # ------------------------------------------------------
    # REVENUE FILTER
    #
    # Free apps naturally have $0 direct price revenue.
    # To preserve the requested Free-vs-Paid comparison,
    # the $10,000 revenue threshold is applied to paid apps.
    # Free apps remain eligible because their direct revenue
    # is $0 by definition.
    # ------------------------------------------------------

    df6 = df6[
        (df6["App_Type"] == "Free")
        |
        (
            (df6["App_Type"] == "Paid")
            & (df6["Revenue"] >= 10000)
        )
    ].copy()

    # ------------------------------------------------------
    # REMOVE MISSING VALUES
    # ------------------------------------------------------

    df6 = df6.dropna(
        subset=[
            "Category",
            "Installs",
            "Revenue"
        ]
    )

    # ------------------------------------------------------
    # TOP 3 CATEGORIES BY TOTAL INSTALLS
    # ------------------------------------------------------

    top3_categories6 = (
        df6
        .groupby(
            "Category",
            as_index=False
        )["Installs"]
        .sum()
        .sort_values(
            "Installs",
            ascending=False
        )
        .head(3)["Category"]
        .tolist()
    )

    df6 = df6[
        df6["Category"].isin(top3_categories6)
    ].copy()

    # ------------------------------------------------------
    # CHECK FILTERED DATA
    # ------------------------------------------------------

    if df6.empty or len(top3_categories6) == 0:

        st.warning(
            "No data available after applying Task 6 filters."
        )

    else:

        # --------------------------------------------------
        # AGGREGATE BY CATEGORY AND FREE/PAID
        # --------------------------------------------------

        summary6 = (
            df6
            .groupby(
                [
                    "Category",
                    "App_Type"
                ],
                as_index=False
            )
            .agg(
                Average_Installs=("Installs", "mean"),
                Total_Revenue=("Revenue", "sum")
            )
        )

        # Ensure both Free and Paid appear for each category
        # when data exists; missing combinations are filled
        # with zero for chart readability.
        complete_index6 = pd.MultiIndex.from_product(
            [
                top3_categories6,
                ["Free", "Paid"]
            ],
            names=["Category", "App_Type"]
        )

        summary6 = (
            summary6
            .set_index(["Category", "App_Type"])
            .reindex(complete_index6, fill_value=0)
            .reset_index()
        )

        # --------------------------------------------------
        # CREATE DUAL-AXIS GROUPED BAR CHART
        # --------------------------------------------------

        fig6 = go.Figure()

        # Average installs: left y-axis
        for app_type in ["Free", "Paid"]:

            data_type = summary6[
                summary6["App_Type"] == app_type
            ]

            fig6.add_trace(
                go.Bar(
                    x=data_type["Category"],
                    y=data_type["Average_Installs"],
                    name=f"{app_type} - Average Installs",
                    offsetgroup=app_type,
                    yaxis="y",
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        f"Type: {app_type}<br>"
                        "Average Installs: %{y:,.0f}"
                        "<extra></extra>"
                    )
                )
            )

        # Revenue: right y-axis
        for app_type in ["Free", "Paid"]:

            data_type = summary6[
                summary6["App_Type"] == app_type
            ]

            fig6.add_trace(
                go.Bar(
                    x=data_type["Category"],
                    y=data_type["Total_Revenue"],
                    name=f"{app_type} - Revenue",
                    offsetgroup=f"{app_type}_revenue",
                    yaxis="y2",
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        f"Type: {app_type}<br>"
                        "Revenue: $%{y:,.2f}"
                        "<extra></extra>"
                    )
                )
            )

        # --------------------------------------------------
        # GRAPH SETTINGS
        # --------------------------------------------------

        fig6.update_layout(
            barmode="group",
            width=1000,
            height=700,
            title=(
                "Top 3 App Categories: "
                "Average Installs vs Revenue"
            ),
            xaxis=dict(
                title="App Category"
            ),
            yaxis=dict(
                title="Average Installs",
                side="left"
            ),
            yaxis2=dict(
                title="Revenue (USD)",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            legend_title="App Type / Metric",
            hovermode="x unified"
        )

        # --------------------------------------------------
        # DISPLAY GRAPH
        # --------------------------------------------------

        st.plotly_chart(
            fig6,
            use_container_width=True
        )

        st.caption(
            "Free apps have $0 price-derived revenue; the $10,000 revenue threshold is therefore applied to paid apps. "
            "Filters: installs >= 10,000, paid-app revenue >= "
            "$10,000, Android version > 4.0, size > 15 MB, "
            "Content Rating = Everyone, and app name length "
            "<= 30 characters. Top 3 categories are selected "
            "by total installs."
        )

else:

    st.info(
        "Task 6 graph is available only "
        "between 1 PM and 2 PM IST."
    )
