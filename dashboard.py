import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Play Store Advanced Analytics",
    page_icon="📱",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("googleplaystore.csv")

    df['Rating'] = df['Rating'].fillna(df['Rating'].median())
    df['Type'] = df['Type'].fillna(df['Type'].mode()[0])

    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

    df['Installs'] = (
        df['Installs']
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.replace('+', '', regex=False)
    )

    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

    df['Price'] = (
        df['Price']
        .astype(str)
        .str.replace('$', '', regex=False)
    )

    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    df['Revenue'] = df['Price'] * df['Installs']

    df['Last Updated'] = pd.to_datetime(
        df['Last Updated'],
        errors='coerce'
    )

    df.drop_duplicates(inplace=True)

    return df

df = load_data()

def convert_size(x):
    try:
        x = str(x)

        if "M" in x:
            return float(x.replace("M", ""))

        elif "k" in x:
            return float(x.replace("k", "")) / 1024

        return np.nan

    except:
        return np.nan

df["Size_MB"] = df["Size"].apply(convert_size)

df['Android_Num'] = (
    df['Android Ver']
    .astype(str)
    .str.extract(r'(\d+\.\d+)')[0]
)

df['Android_Num'] = pd.to_numeric(
    df['Android_Num'],
    errors='coerce'
)

ist = pytz.timezone("Asia/Kolkata")
hour = datetime.now(ist).hour

st.title(" Play Store Advanced Analytics Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Task 1",
        "Task 2",
        "Task 3",
        "Task 4",
        "Task 5",
        "Task 6"
    ]
)

# ---------------- TASK 1 ----------------

if page == "Task 1":

    if 15 <= hour < 17:

        st.header("Task 1")

        temp = df.copy()

        # Rating >= 4
        temp = temp[
            temp['Rating'] >= 4.0
        ]

        # Size > 10 MB
        temp = temp[
            temp['Size_MB'] > 10
        ]

        # January updates only
        temp = temp[
            temp['Last Updated'].dt.month == 1
        ]

        # Top 10 categories by installs
        top_cat = (
            temp.groupby('Category')['Installs']
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .index
        )

        temp = temp[
            temp['Category'].isin(top_cat)
        ]

        result = (
            temp.groupby('Category')
            .agg({
                'Rating':'mean',
                'Reviews':'sum'
            })
            .reset_index()
        )

        fig, ax = plt.subplots(
            figsize=(12,6)
        )

        x = np.arange(len(result))

        width = 0.4

        ax.bar(
            x-width/2,
            result['Rating'],
            width,
            label='Average Rating'
        )

        ax.bar(
            x+width/2,
            result['Reviews']/100000,
            width,
            label='Total Reviews (Lakhs)'
        )

        ax.set_xticks(x)

        ax.set_xticklabels(
            result['Category'],
            rotation=45
        )

        ax.set_title(
            "Average Rating vs Reviews"
        )

        ax.legend()

        st.pyplot(fig)

    else:

        st.warning(
            "Task 1 visible only between 3 PM and 5 PM IST"
        )
# ---------------- TASK 2 ----------------

elif page == "Task 2":

    if True:

        st.header("Task 2")

        temp = df.copy()

        installs = (
            temp.groupby("Category")["Installs"]
            .sum()
            .reset_index()
        )

        installs = installs[
            installs["Installs"] > 1000000
        ]

        installs = installs[
            ~installs["Category"]
            .str.startswith(
                ("A", "C", "G", "S"),
                na=False
            )
        ]

        installs = installs.sort_values(
            "Installs",
            ascending=False
        ).head(5)

        fig = px.choropleth(
            installs,
            locations="Category",
            locationmode="country names",
            color="Installs",
            hover_name="Category",
            title="Top Categories by Installs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "Task 2 visible only between 6 PM and 8 PM IST"
        )
# ---------------- TASK 3 ----------------

elif page == "Task 3":

    if True:

        st.header("Task 3")

        temp = df.copy()

        # Revenue column create
        temp["Revenue"] = (
            temp["Installs"] *
            temp["Price"]
        )

        # Android Version Numeric
        temp["Android_Num"] = (
            temp["Android Ver"]
            .astype(str)
            .str.extract(r'(\d+\.?\d*)')[0]
        )

        temp["Android_Num"] = pd.to_numeric(
            temp["Android_Num"],
            errors="coerce"
        )

        # Filters
        temp = temp[
            (temp["Installs"] >= 10000) &
            (temp["Revenue"] >= 10000) &
            (temp["Android_Num"] > 4.0) &
            (temp["Size_MB"] > 15)
        ]

        temp = temp[
            temp["Content Rating"] == "Everyone"
        ]

        temp = temp[
            temp["App"].str.len() <= 30
        ]

        # Top 3 categories
        top3 = (
            temp.groupby("Category")["Installs"]
            .sum()
            .sort_values(ascending=False)
            .head(3)
            .index
        )

        temp = temp[
            temp["Category"].isin(top3)
        ]

        summary = (
            temp.groupby(
                ["Category", "Type"]
            )
            .agg({
                "Installs": "mean",
                "Revenue": "mean"
            })
            .reset_index()
        )

        fig, ax1 = plt.subplots(
            figsize=(12, 6)
        )

        sns.barplot(
            data=summary,
            x="Category",
            y="Installs",
            hue="Type",
            ax=ax1
        )

        ax1.set_ylabel(
            "Average Installs"
        )

        ax2 = ax1.twinx()

        ax2.plot(
            summary["Category"],
            summary["Revenue"],
            marker="o",
            linewidth=3
        )

        ax2.set_ylabel(
            "Revenue ($)"
        )

        plt.title(
            "Average Installs vs Revenue"
        )

        st.pyplot(fig)

    else:

        st.warning(
            "Task 3 visible only between 1 PM and 2 PM IST"
        )

# ---------------- TASK 4 ----------------

elif page == "Task 4":

    if True:

        st.header("Task 4")

        temp = df.copy()

        # Reviews > 500
        temp = temp[
            temp["Reviews"] > 500
        ]

        # App name should not start with X,Y,Z
        temp = temp[
            ~temp["App"].str.startswith(
                ("X", "Y", "Z"),
                na=False
            )
        ]

        # App name should not contain S
        temp = temp[
            ~temp["App"].str.contains(
                "S",
                case=False,
                na=False
            )
        ]

        # Categories allowed
        temp = temp[
            temp["Category"].isin(
                [
                    "BEAUTY",
                    "BUSINESS",
                    "DATING"
                ]
            )
        ]

        # Category translation
        temp["Category"] = (
            temp["Category"]
            .replace({
                "BEAUTY": "सौंदर्य",
                "BUSINESS": "வணிகம்",
                "DATING": "Dating(DE)"
            })
        )

        # Convert date
        temp["Last Updated"] = pd.to_datetime(
            temp["Last Updated"],
            errors="coerce"
        )

        trend = (
            temp.groupby(
                ["Last Updated", "Category"]
            )["Installs"]
            .sum()
            .reset_index()
        )

        fig, ax = plt.subplots(
            figsize=(12,6)
        )

        for cat in trend["Category"].unique():

            data_cat = trend[
                trend["Category"] == cat
            ]

            ax.plot(
                data_cat["Last Updated"],
                data_cat["Installs"],
                marker="o",
                label=cat
            )

        ax.set_title(
            "Installs Trend Over Time"
        )

        ax.set_xlabel(
            "Date"
        )

        ax.set_ylabel(
            "Total Installs"
        )

        ax.legend()

        st.pyplot(fig)

    else:

        st.warning(
            "Task 4 visible only between 6 PM and 9 PM IST"
        )
# ---------------- TASK 5 ----------------

elif page == "Task 5":

    if True:

        st.header("Task 5")

        temp = df.copy()

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

        temp = temp[
            temp["Category"]
            .isin(categories)
        ]

        temp = temp[
            temp["Rating"] > 3.5
        ]

        temp = temp[
            temp["Reviews"] > 500
        ]

        temp = temp[
            temp["Installs"] > 50000
        ]

        temp = temp[
            ~temp["App"]
            .str.contains(
                "S",
                case=False,
                na=False
            )
        ]

        temp["Category"] = (
            temp["Category"]
            .replace({
                "BEAUTY": "सौंदर्य",
                "BUSINESS": "வணிகம்",
                "DATING": "Dating(DE)"
            })
        )

        fig = px.scatter(
            temp,
            x="Size_MB",
            y="Rating",
            size="Installs",
            color="Category",
            hover_name="App",
            title="Bubble Chart"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "Task 5 visible only between 5 PM and 7 PM IST"
        )
# ---------------- TASK 6 ----------------

elif page == "Task 6":

    if True:

        st.header("Task 6")

        temp = df.copy()

        # Rating >= 4.2
        temp = temp[
            temp["Rating"] >= 4.2
        ]

        # Reviews > 1000
        temp = temp[
            temp["Reviews"] > 1000
        ]

        # Size between 20 and 80 MB
        temp = temp[
            temp["Size_MB"].between(
                20,
                80
            )
        ]

        # Category starts with T or P
        temp = temp[
            temp["Category"].str.startswith(
                ("T", "P"),
                na=False
            )
        ]

        # App name should not contain numbers
        temp = temp[
            ~temp["App"].str.contains(
                r"\d",
                regex=True,
                na=False
            )
        ]

        # Category Translation
        temp["Category"] = (
            temp["Category"]
            .replace({
                "TRAVEL_AND_LOCAL": "Voyage",
                "PRODUCTIVITY": "Productividad",
                "PHOTOGRAPHY": "写真"
            })
        )

        # Create Month Column
        temp["Month"] = (
            temp["Last Updated"]
            .dt.to_period("M")
            .astype(str)
        )

        pivot = temp.pivot_table(
            values="Installs",
            index="Month",
            columns="Category",
            aggfunc="sum",
            fill_value=0
        )

        fig, ax = plt.subplots(
            figsize=(14,7)
        )

        ax.stackplot(
            pivot.index,
            pivot.T.values,
            labels=pivot.columns
        )

        ax.set_title(
            "Cumulative Installs by Category"
        )

        ax.set_xlabel(
            "Month"
        )

        ax.set_ylabel(
            "Installs"
        )

        ax.legend(
            loc="upper left"
        )

        plt.xticks(
            rotation=45
        )

        st.pyplot(fig)

    else:

        st.warning(
            "Task 6 visible only between 4 PM and 6 PM IST"
        )
