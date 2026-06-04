# Google Play Store Advanced Analytics Dashboard

## Project Overview

This project is an Advanced Google Play Store Analytics Dashboard developed using Python and Streamlit. The dashboard performs data cleaning, preprocessing, filtering, and visualization on the Google Play Store dataset. It provides multiple analytical views through interactive charts and applies custom business rules, category filtering, translation logic, and time-based visualization controls.

## Objectives

The main objective of this project is to analyze Google Play Store applications and generate meaningful insights related to app ratings, installs, reviews, revenue, categories, and user engagement through advanced visualizations.

## Technologies Used

Python

Streamlit

Pandas

NumPy

Matplotlib

Seaborn

Plotly

SQLite

Pytz

## Dataset

Dataset Name: Google Play Store Dataset

File Used: googleplaystore.csv

The dataset contains information about applications available on the Google Play Store including:

App Name

Category

Rating

Reviews

Installs

Price

Size

Content Rating

Genres

Android Version

Last Updated Date

## Features

Data Cleaning and Preprocessing

Missing Value Handling

Duplicate Record Removal

Install Count Conversion

Price Conversion

Size Conversion to MB

Date Conversion

Revenue Calculation

Android Version Extraction

Interactive Dashboard Navigation

Advanced Filtering

Time-Based Graph Visibility

Category Translation Features

Downloadable Processed Dataset

## Implemented Tasks

### Task 1

Grouped Bar Chart comparing:

Average Rating

Total Reviews

Filters Applied:

Average Rating ≥ 4.0

Size > 10 MB

January Updates Only

Top 10 Categories by Installs

Visible only between 3 PM and 5 PM IST

### Task 2

Interactive Choropleth Visualization for Global Installs

Filters Applied:

Top 5 Categories

Installs > 1 Million

Category should not start with A, C, G, or S

Visible only between 6 PM and 8 PM IST

### Task 3

Dual Axis Chart comparing:

Average Installs

Revenue

Filters Applied:

Top 3 Categories

Installs ≥ 10,000

Revenue ≥ $10,000

Android Version > 4.0

Size > 15 MB

Content Rating = Everyone

App Name Length ≤ 30 Characters

Visible only between 1 PM and 2 PM IST

### Task 4

Time Series Install Trend Analysis

Filters Applied:

Reviews > 500

Category starts with B, C, or E

App Name should not start with X, Y, or Z

App Name should not contain S

Category Translation Applied

Beauty → Hindi

Business → Tamil

Dating → German

Visible only between 6 PM and 9 PM IST

### Task 5

Bubble Chart Analysis

Filters Applied:

Rating > 3.5

Installs > 50,000

Reviews > 500

Sentiment Subjectivity > 0.5

Selected Categories Only

Special Category Translation Applied

Game Category Highlighted

Visible only between 5 PM and 7 PM IST

### Task 6

Stacked Area Chart

Filters Applied:

Rating ≥ 4.2

Reviews > 1000

Size between 20 MB and 80 MB

Category starts with T or P

App Name should not contain numbers

Category Translation Applied

Travel & Local → French

Productivity → Spanish

Photography → Japanese

Visible only between 4 PM and 6 PM IST

## How to Run

Install Required Packages

pip install -r requirements.txt

Run the Application

streamlit run dashboard.py

## Project Structure

playstore_project/

dashboard.py

googleplaystore.csv

requirements.txt

README.md

users.db

## Developer

Yuvraj Mahajan

## Conclusion

This project demonstrates data cleaning, feature engineering, exploratory data analysis, advanced visualization techniques, business-rule implementation, and dashboard development using Streamlit. The dashboard provides meaningful insights into Google Play Store application data through interactive and time-controlled analytics.

