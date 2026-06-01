import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- DATABASE ----------------

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")
conn.commit()

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Play Store Analytics",
    page_icon="📱",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

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

    df.drop_duplicates(inplace=True)
    return df

df = load_data()

# ---------------- SESSION ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN PAGE ----------------

if not st.session_state.logged_in:
    st.markdown(
        "<h1 style='text-align:center;color:cyan;'>📱 Play Store Analytics</h1>",
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
            data = cursor.fetchone()
            if data:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    with tab2:
        st.subheader("Sign Up")
        new_user = st.text_input("Create Username")
        new_pwd = st.text_input("Create Password", type="password")

        if st.button("Create Account"):
            cursor.execute("SELECT * FROM users WHERE username=?", (new_user,))
            data = cursor.fetchone()
            if data:
                st.error("Username already exists")
            else:
                cursor.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_pwd))
                conn.commit()
                st.success("Account Created Successfully")

# ---------------- DASHBOARD ----------------

else:
    st.title("📊 Google Play Store Dashboard")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "KPI Dashboard",
            "Category Analysis",
            "Rating Analysis",
            "Installs Analysis",
            "Reviews Analysis",
            "Price Analysis",
            "Content Rating",
            "Genres Analysis",
            "Top Installed Apps",
            "Top Rated Apps",
            "Category Wise Rating",
            "Reviews Distribution",
            "Correlation Analysis",
            "Free vs Paid",
            "Data Table",
            "About"
        ]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # HOME
    if page == "Home":
        st.title("📱 Google Play Store Analytics")
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg",
            width=300
        )
        st.markdown("""
        ### Features
        ✅ Login & Signup
        ✅ KPI Dashboard
        ✅ 15+ Visualizations
        ✅ Category Analysis
        ✅ Rating Analysis
        ✅ Installs Analysis
        ✅ Reviews Analysis
        ✅ Correlation Heatmap
        ✅ Data Explorer
        ✅ Download Clean Dataset
        """)

    # KPI
    elif page == "KPI Dashboard":
        total_apps = len(df)
        avg_rating = round(df['Rating'].mean(), 2)
        total_categories = df['Category'].nunique()
        total_installs = int(df['Installs'].sum())
        total_reviews = int(df['Reviews'].sum())
        free_apps = len(df[df['Type'] == "Free"])
        paid_apps = len(df[df['Type'] == "Paid"])
        highest_rating = round(df['Rating'].max(), 2)

        c1, c2, c3, c4 = st.columns(4)
        c5, c6, c7, c8 = st.columns(4)

        c1.metric("Total Apps", total_apps)
        c2.metric("Avg Rating", avg_rating)
        c3.metric("Categories", total_categories)
        c4.metric("Installs", f"{total_installs:,}")
        c5.metric("Reviews", f"{total_reviews:,}")
        c6.metric("Free Apps", free_apps)
        c7.metric("Paid Apps", paid_apps)
        c8.metric("Highest Rating", highest_rating)

    # CATEGORY
    elif page == "Category Analysis":
        st.subheader("Top Categories")
        fig, ax = plt.subplots(figsize=(10, 5))
        top_cat = df['Category'].value_counts().head(10)
        sns.barplot(x=top_cat.values, y=top_cat.index, ax=ax)
        st.pyplot(fig)

    # RATING
    elif page == "Rating Analysis":
        st.subheader("Rating Distribution")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df['Rating'], bins=20, ax=ax)
        st.pyplot(fig)

    # INSTALLS
    elif page == "Installs Analysis":
        st.subheader("Top Installs")
        fig, ax = plt.subplots(figsize=(10, 5))
        install_data = df.groupby('Category')['Installs'].sum().sort_values(ascending=False).head(10)
        sns.barplot(x=install_data.values, y=install_data.index, ax=ax)
        st.pyplot(fig)

    # REVIEWS
    elif page == "Reviews Analysis":
        st.subheader("Reviews vs Rating")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(data=df, x='Reviews', y='Rating', ax=ax)
        st.pyplot(fig)

    # FREE VS PAID
    elif page == "Free vs Paid":
        st.subheader("Free vs Paid Apps")
        fig, ax = plt.subplots(figsize=(7, 7))
        type_count = df['Type'].value_counts()
        ax.pie(type_count.values, labels=type_count.index, autopct='%1.1f%%')
        st.pyplot(fig)

    # PRICE
    elif page == "Price Analysis":
        st.subheader("Price Distribution")
        paid = df[df['Price'] > 0]
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(paid['Price'], bins=20, ax=ax)
        st.pyplot(fig)

    # CONTENT RATING
    elif page == "Content Rating":
        st.subheader("Content Rating Analysis")
        fig, ax = plt.subplots(figsize=(10, 5))
        content = df['Content Rating'].value_counts()
        sns.barplot(x=content.index, y=content.values, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # GENRES
    elif page == "Genres Analysis":
        st.subheader("Top Genres")
        fig, ax = plt.subplots(figsize=(10, 5))
        genres = df['Genres'].value_counts().head(10)
        sns.barplot(x=genres.values, y=genres.index, ax=ax)
        st.pyplot(fig)

    # TOP INSTALLED
    elif page == "Top Installed Apps":
        st.subheader("Top Installed Apps")
        top_apps = df.nlargest(10, 'Installs')
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=top_apps, x='Installs', y='App', ax=ax)
        st.pyplot(fig)

    # TOP RATED
    elif page == "Top Rated Apps":
        st.subheader("Top Rated Apps")
        top_rating = df.sort_values(by='Rating', ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=top_rating, x='Rating', y='App', ax=ax)
        st.pyplot(fig)

    # CATEGORY WISE RATING
    elif page == "Category Wise Rating":
        st.subheader("Average Rating by Category")
        avg_rating = df.groupby('Category')['Rating'].mean().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=avg_rating.values, y=avg_rating.index, ax=ax)
        st.pyplot(fig)

    # REVIEWS DISTRIBUTION
    elif page == "Reviews Distribution":
        st.subheader("Reviews Distribution")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df['Reviews'], bins=30, ax=ax)
        st.pyplot(fig)

    # CORRELATION
    elif page == "Correlation Analysis":
        st.subheader("Correlation Heatmap")
        numeric_df = df.select_dtypes(include='number')
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # DATA TABLE
    elif page == "Data Table":
        st.subheader("Dataset Explorer")
        st.dataframe(df)
        st.download_button(
            "Download Dataset",
            df.to_csv(index=False),
            "playstore_cleaned.csv",
            "text/csv"
        )

    # ABOUT
    elif page == "About":
        st.subheader("Project Information")
        st.write("""
        Project: Google Play Store Analytics

        Technologies:
        - Python
        - Streamlit
        - Pandas
        - Matplotlib
        - Seaborn
        - SQLite

        Developer:
        Yuvraj Mahajan
        """)