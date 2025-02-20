import streamlit as st
import pandas as pd
import os
from  io import BytesIO 

st.set_page_config(page_title = "Data Sweeper" , layout = "wide")

st.markdown(
    """ 
    <style>
    .stApp{
        background-color : white;
        color:black;
        }
        </style>
        """,
        unsafe_allow_html=True

)
# Title and Introduction
st.title("🧠 Growth Mindset Journey by Kashaf Aman")
name = st.sidebar.text_input("👤 Enter Your Name:")
st.write("Welcome to the Growth Mindset Challenge! Every day is a new opportunity 💡 to learn and grow.")
st.write("Transform your files between CVS and Excel format")

# file uploader
uploaded_files = st.file_uploader("upload your files in CSV  ir Excel :" ,type=["cvs" ,"xlsx"], accept_multiple_files=(True))
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue
        # detail
        st.write("👉 Preview the head of the Dataframe")
        st.dataframe(df.head())
        # daa cleaning option 
        st.subheader("🚀Cleaning Data option")
        if st.checkbox(f"Clean Data from this file {file.name}"):
            col1 , col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Removed!")

            with col2:
                  if st.button(f"Missing file values: {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values! Values are not written")

        st.subheader("🔍 Select Columes to keep the Data")
        columns = st.multiselect(f"çhoose columns {file.name}", df.columns, default=df.columns)
        df = df[columns]
        # visualization 
        st.subheader("📝 Data Visualization")
        if st.checkbox(f"show visuaization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])
        
        # conversion
        st.subheader("🔄 Conversion Option")
        conversion_type = st.radio(f"convert {file.name} to :",["CVS" ,"Excel"],key=file.name)
        if st.button(f"convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CVS":
                df.to.csv(buffer,index = False)
                file_name = file.name.replace(file_ext ,".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                 df.to_excel(buffer,index = False)
                 file_name = file.name.replace(file_ext ,".xlsx")
                 mime_type = "application/vnd.openxmlformats-officedocuments.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data = buffer,
                file_name=file_name,
                mime=mime_type
            )
        st.success("Process Completed Successfully!🎯")
# Footer
st.write(" 👉 Stay consistent and keep challenging yourself every day!")
