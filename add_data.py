import streamlit as st
import pandas as pd

def addData():
    # Read CSV
    df=pd.read_csv("data/data.csv")
    # Create Add Data Form
    with st.form("formAddData", clear_on_submit=True):
        col1, col2=st.columns(2)
        order_date=col1.date_input("Order Date")
        region=col2.selectbox("Region", df["Region"].unique()) # label, data

        col11, col22=st.columns(2)
        city=col11.selectbox("City", df["City"].unique())
        category = col22.selectbox("Category", df["Category"].unique())

        col111, col222,col333= st.columns(3)
        product = col111.selectbox("Product", df["Product"].unique())
        quantity =  col222.number_input("Quantity", step=1, min_value=0) # step=1 biar input angkanya dari integer 1 mulainya, tidak desimal
        unit_price= col333.number_input("Unit Price", min_value=0.0, step=0.01)
        # Submit Button
        btn = st.form_submit_button("Add Data", type="primary")

        # Form Validation
        if btn:
            if order_date=="" or region=="" or city=="" or category=="" or product=="" or quantity==0 or unit_price==0.00:
                st.error("All fields are required")
                return False
            else:
                # Insert Data
                df=pd.concat([df, pd.DataFrame.from_records([{
                    'OrderDate' :order_date,
                    'Region':region,
                    'City':city,
                    'Category':category,
                    'Product':product,
                    'Quantity':quantity,
                    'UnitPrice':unit_price,
                    'TotalPrice':float(quantity) * float(unit_price)
                    
                }])])
            # handle exceptions
            try:
                df.to_csv("data/data.csv", index=False)
                st.success(product+" Has been added successfully !")
                return True
            except:
                st.warning("Unable to write, Please close Excel file")
                return False
        



addData()