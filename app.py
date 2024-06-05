import pandas as pd 
import numpy as np 
import streamlit as st 
import seaborn as sns 
import matplotlib.pyplot as plt 

st.set_page_config(layout='wide')

st.header ("E-commerce Product Analysis Dashboard @Tejas_sarode ")
df=pd.read_csv("Car Accessories.csv")
df1=pd.read_csv("Car and Bike Care.csv")
df2=pd.read_csv("Car Electronics.csv")

data= pd.concat([df,df1,df2], ignore_index=True)



data.isnull().sum()
data.duplicated().sum()



data.info()

data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')
data['no_of_ratings'] = pd.to_numeric(data['no_of_ratings'], errors='coerce')
data['discount_price']=data['discount_price'].str.replace('₹', '').str.replace(',', '').astype(float)
data ["actual_price"]=data['actual_price'].str.replace('₹', '').str.replace(',', '').astype(float)

data.info()

data.drop_duplicates()


data['ratings'] = data['ratings'].fillna(data['ratings'].median())
data['no_of_ratings'] = data['no_of_ratings'].fillna(data['no_of_ratings'].median())
data['discount_price'] = data['discount_price'].fillna(data['discount_price'].median())
data['actual_price'] = data['actual_price'].fillna(data['actual_price'].median())

data.info()



# Filters 
st.sidebar.header("Filters")

# Category Multiselect
selected_categories = st.sidebar.multiselect(
    label="Explore Category",
    options=data["sub_category"].unique(),
    default=["Car Accessories"]  # Default to all categories
)

# Price Range Slider
price_range = st.sidebar.slider(
    label="Price Range",
    min_value=float(data["actual_price"].min()),
    max_value=float(data["actual_price"].max()),
    value=(float(data["actual_price"].min()), float(data["actual_price"].max()))  # Default to full range
)

# Rating Range Slider
rating_range = st.sidebar.slider(
    label="Rating Range",
    min_value=0.0,
    max_value=5.0,
    value=(0.0, 5.0), 
    step=0.1
)

# Filter data based on selections
filtered_data = data[
    (data["sub_category"].isin(selected_categories)) &
    (data["actual_price"].between(price_range[0], price_range[1])) &
    (data["ratings"].between(rating_range[0], rating_range[1]))
]

# Calculate metrics
filtered_data['discount_percentage'] = ((filtered_data['actual_price'] - filtered_data['discount_price']) / filtered_data['actual_price']) * 100
metrics = filtered_data.groupby('sub_category').agg(
    total_revenue=pd.NamedAgg(column='discount_price', aggfunc='sum'),
    avg_discount_percentage=pd.NamedAgg(column='discount_percentage', aggfunc=lambda x: round(x.mean(), 1)),
    avg_rating=pd.NamedAgg(column='ratings', aggfunc=lambda x: round(x.mean(), 1))
).reset_index()




# Calculate overall metrics
total_sales_revenue = filtered_data['discount_price'].sum()
average_prices = round(filtered_data['actual_price'].mean(), 1)
customer_engagement = round(filtered_data['ratings'].mean(), 1)
top_products = filtered_data.nlargest(2, 'discount_price')

# Display KPIs
st.subheader("Key Performance Indicators (KPIs)")

# Define CSS for KPI cards
st.markdown(
    """
    <style>
    .card {
        background-color: #f1f1f1;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        margin: 10px;
    }
    .card h2 {
        font-size: 24px;
        margin: 0;
    }
    .card p {
        font-size: 20px;
        margin: 5px 0 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="card">
            <h2>Total Sales Revenue</h2>
            <p>₹{total_sales_revenue:,.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="card">
            <h2>Average Prices</h2>
            <p>₹{average_prices:,.1f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="card">
            <h2>Customer Engagement </h2>
            <p>{customer_engagement:.1f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="card">
            <h2>Top Products</h2>
        """,
        unsafe_allow_html=True
    )

    # Check if there are at least two top products
    if len(top_products) >= 2:
        st.markdown(
            f"""
            <p>{top_products.iloc[0]['name']}</p>
            <p>{top_products.iloc[1]['name']}</p>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown("<p>No top products available</p>", unsafe_allow_html=True)

st.subheader("Filtered Data")
st.write(filtered_data)

# Check if filtered data is empty
if filtered_data.empty:
    st.write("No data available for the selected filters.")
else:
    # Display metrics
    st.subheader("Sales Metrics by Category")
    st.write(metrics)
data['discount_percentage'] = ((data['actual_price'] - data['discount_price']) / data['actual_price']) * 100

# Group by main_category and sub_category to calculate total sales
sales_data = data.groupby(['main_category', 'sub_category'])['discount_price'].sum().reset_index()

# Group by main_category to calculate average ratings
avg_rating_data = data.groupby('main_category')['ratings'].mean().reset_index()

# Group by main_category to calculate average discount percentage
avg_discount_data = data.groupby('main_category')['discount_percentage'].mean().reset_index()



# Filter data based on selections
filtered_data = data[data["sub_category"].isin(selected_categories)]

# Customer Engagement
st.header("Customer Engagement")

# Rating Distribution
st.subheader("Rating Distribution (Histogram)")
fig, ax = plt.subplots()
sns.histplot(filtered_data['ratings'], bins=20, kde=True, ax=ax)
ax.set_xlabel("Rating")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Rating vs. Sales
st.subheader("Rating vs. Sales (Scatter Plot)")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x='ratings', y='no_of_ratings', ax=ax)
ax.set_xlabel("Rating")
ax.set_ylabel("Number of Ratings")
ax.set_title("Rating vs. Number of Ratings")
st.pyplot(fig)

# Category Performance
st.header("Category Performance")

# Sales by Category
st.subheader("Sales by Category")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=sales_data, x='discount_price', y='sub_category', hue='main_category', ax=ax)
ax.set_xlabel("Total Sales")
ax.set_ylabel("Sub Category")
ax.set_title("Total Sales by Main Category and Sub Category")
st.pyplot(fig)

# Average Rating by Category
st.subheader("Average Rating by Category")
fig, ax = plt.subplots()
sns.barplot(data=avg_rating_data, x='main_category', y='ratings', ax=ax)
ax.set_xlabel("Main Category")
ax.set_ylabel("Average Rating")
ax.set_title("Average Rating by Main Category")
st.pyplot(fig)

# Discount Analysis
st.header("Discount Analysis")

# Discount Impact
st.subheader("Discount Impact")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x='discount_percentage', y='no_of_ratings', ax=ax)
ax.set_xlabel("Discount Percentage")
ax.set_ylabel("Number of Ratings")
ax.set_title("Discount Percentage vs. Number of Ratings")
st.pyplot(fig)

# Average Discount Percentage by Category
st.subheader("Average Discount Percentage by Category")
fig, ax = plt.subplots()
sns.barplot(data=avg_discount_data, x='main_category', y='discount_percentage', ax=ax)
ax.set_xlabel("Main Category")
ax.set_ylabel("Average Discount Percentage")
ax.set_title("Average Discount Percentage by Main Category")
st.pyplot(fig)