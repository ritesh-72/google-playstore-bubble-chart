import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime

# Browser me graph open karne ke liye
pio.renderers.default = "browser"

# -----------------------------
# Time Condition (5 PM to 7 PM)
# -----------------------------
current_time = datetime.now()

if not (17 <= current_time.hour < 19):
   print("Graph is available only between 5 PM and 7 PM.")
   exit()

# -----------------------------
# Load CSV files
# -----------------------------
apps = pd.read_csv("googleplaystore.csv")
reviews = pd.read_csv("googleplay_users_reviews..csv")   # <-- ek hi dot

# -----------------------------
# Merge datasets
# -----------------------------
df = pd.merge(apps, reviews, on="App", how="inner")

# -----------------------------
# Convert Size to MB
# -----------------------------
def convert_size(size):
    size = str(size)

    if size.endswith("M"):
        return float(size[:-1])

    elif size.endswith("k"):
        return float(size[:-1]) / 1024

    else:
        return None

df["Size_MB"] = df["Size"].apply(convert_size)

# -----------------------------
# Convert Installs
# -----------------------------
df["Installs"] = (
    df["Installs"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("+", "", regex=False)
)

df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

# -----------------------------
# Numeric Columns
# -----------------------------
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
df["Sentiment_Subjectivity"] = pd.to_numeric(
    df["Sentiment_Subjectivity"], errors="coerce"
)

# -----------------------------
# Categories
# -----------------------------
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

# -----------------------------
# Filters
# -----------------------------
filtered = df[
    (df["Rating"] > 3.5) &
    (df["Reviews"] > 500) &
    (df["Sentiment_Subjectivity"] > 0.5) &
    (df["Installs"] > 50000) &
    (df["Category"].isin(categories)) &
    (~df["App"].str.contains("S", case=False, na=False))
].copy()

print("Filtered Records:", len(filtered))

# -----------------------------
# Translate Categories
# -----------------------------
filtered["Category"] = filtered["Category"].replace({
    "BEAUTY": "सौंदर्य",
    "BUSINESS": "வணிகம்",
    "DATING": "Dating"
})

# -----------------------------
# Colors
# -----------------------------
color_map = {
    "GAME": "pink",
    "सौंदर्य": "gold",
    "வணிகம்": "green",
    "COMICS": "orange",
    "COMMUNICATION": "red",
    "Dating": "purple",
    "ENTERTAINMENT": "blue",
    "SOCIAL": "cyan",
    "EVENTS": "gray"
}

# -----------------------------
# Bubble Chart
# -----------------------------
if len(filtered) == 0:
    print("No data available after applying filters.")
else:

    fig = px.scatter(
        filtered,
        x="Size_MB",
        y="Rating",
        size="Installs",
        size_max=150,
        color="Category",
        color_discrete_map=color_map,
        hover_name="App",
        title="Bubble Chart: App Size (MB) vs Average Rating",
        labels={
            "Size_MB": "App Size (MB)",
            "Rating": "Average Rating"
        }
    )

    fig.update_layout(width=1000, height=700)

    fig.show()
