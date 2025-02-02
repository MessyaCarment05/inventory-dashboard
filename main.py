import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt
from matplotlib import pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_option_menu import option_menu

# config the page width
st.set_page_config(page_title="Business Dashboard", page_icon="", layout="wide")
st.subheader("Business Analytics Dashboard")
#  import dari add_data.py
# from add_data import *

# read data
df=pd.read_csv("data/data.csv")
# st.dataframe(df, use_container_width=True)

# side bar
st.sidebar.image("images/mc_logo.png")

# sidebar data picker for filter
with st.sidebar:
    st.title("Select Date Range")
    start_date=st.date_input(label="Start Date")

with st.sidebar:
    end_date=st.date_input(label="End Date")

# filter date range
df_selection=df[(df["OrderDate"]>=str(start_date)) & (df["OrderDate"]<=str(end_date))]

# Message selected data range
st.error("You have choosen analytics from : " + str(start_date) + " to " +str(end_date))

# Home Page
def home_page():
    # Filter dataset
    def filter_dataset():
        # Filter dataframe
        with st.expander("Filter Excel Data"):
            filtered_df=dataframe_explorer(df_selection, case=False)
            st.dataframe(filtered_df, use_container_width=True)

    filter_dataset()

    def top_part():
        #  bar chart
        a1,a2=st.columns(2)
        with a1:
            st.subheader("Product & Quantities", divider='rainbow' )
            source = df_selection
            bar_chart=alt.Chart(source).mark_bar().encode(
                x="sum(Quantity):Q",
                y=alt.Y("Product:N", sort="-x")# - x artinya ngesort yang bawah paling kecil
            )
            st.altair_chart(bar_chart, use_container_width=True)

        #metrics
        with a2:
            st.subheader("Data Metrics", divider="rainbow")
            col1, col2=st.columns(2)
            col1.metric("All number of Products", value=df_selection.Product.nunique(), delta="All Products in Dataset") # nununique hitung produk nya aja jadi kayak groupby tidak duplikat
            col2.metric("Sum of Product Total Price USD ($)", value=f"{df_selection.TotalPrice.sum():,.0f}", delta=df_selection.TotalPrice.median())

            c11,c22,c33=st.columns(3)
            c11.metric("Maximum Total Price", value=f"{df_selection.TotalPrice.max():,.0f}", delta="High Price")
            c22.metric("Minimum Total Price", value=f"{df_selection.TotalPrice.min():,.0f}", delta="Low Price")
            c33.metric("Price Range", value=f"{df_selection.TotalPrice.max()-df_selection.TotalPrice.min():,.0f}", delta="Range")
            style_metric_cards(background_color="#071021", border_left_color="#1f66bd")
    top_part()


    def middle_part():
        b1,b2=st.columns(2)
        with b1:
            st.subheader("Products & Total Price", divider="rainbow")
            source=df_selection
            chart=alt.Chart(source).mark_circle().encode(
                x="Product",
                y="TotalPrice",
                color="Category"
            ).interactive()
            st.altair_chart(chart, use_container_width=True)

        with b2:
            st.subheader("Product & Unit Price", divider="rainbow")
            energy_source=df_selection
            bar_chart=alt.Chart(energy_source).mark_bar().encode(
                x="month(OrderDate):O",
                y="sum(UnitPrice):Q",
                color="Product:N"
            )
            st.altair_chart(bar_chart, use_container_width=True)
    middle_part()

    def bottom_part():
        c1,c2=st.columns(2)
        with c1:
            st.subheader("Product vs Unit Price", divider="rainbow")
            feature_x=st.selectbox("Select X (Qualitative Data)", df_selection.select_dtypes("object").columns)
            feature_y=st.selectbox("Select Y (Quantitative Data)", df_selection.select_dtypes("number").columns)

            fig, ax=plt.subplots()
            sns.scatterplot(data=df_selection, x=feature_x, y=feature_y, hue=df_selection.Product, ax = ax)

            st.pyplot(fig)
        with c2:
            st.subheader("Features by Frequency", divider="rainbow")
            feature=st.selectbox("Select only Qualitative Data", df_selection.select_dtypes("object").columns)
            fig, ax =plt.subplots()
            ax.hist(df_selection[feature], bins=20)
            ax.set_title(f"Histogram of {feature}")
            ax.set_xlabel(feature)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
    bottom_part()

# Menu
with st.sidebar:
    selected_menu=option_menu(
        menu_title="Dashboard Menu",
        options=["Home", "Add Data"],
        icons=["house", "plus"],
        menu_icon='cast',
        default_index=0,
        orientation="vertical"
    )

if selected_menu=="Home":
    home_page()
else :
    from add_data import *
    addData()
