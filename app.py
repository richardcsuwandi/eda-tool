import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Page layout
    st.set_page_config(page_title="EDA Tool",
    initial_sidebar_state="expanded")
    st.set_option("deprecation.showPyplotGlobalUse", False)

    # Main title
    st.title("Exploratory Data Analysis (EDA) Tool 📈")
    st.sidebar.title("Exploratory Data Analysis (EDA) Tool 📈")
    st.markdown("### By [Richard Cornelius Suwandi](https://github.com/richardcsuwandi)")
    st.sidebar.markdown("By [Richard Cornelius Suwandi](https://github.com/richardcsuwandi)")
    st.sidebar.markdown("[![View on GitHub](https://img.shields.io/badge/GitHub-View_on_GitHub-blue?logo=GitHub)](https://github.com/richardcsuwandi/eda-tool)")

    # App description
    st.markdown("### An exploratory analysis tool that provides various summaries and visualizations on the uploaded data.")

    # Upload file
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type="csv")

    st.info("Upload a CSV file to get started")
    if uploaded_file is not None:
        st.success("File sucessfully uploaded!")
        df = pd.read_csv(uploaded_file)
        numerical_col = df.select_dtypes(include=np.number).columns.tolist()
        categorical_col = df.drop(numerical_col, axis=1).columns

        # Show raw data
        if st.sidebar.checkbox("Show raw data", False):
            st.write(df)

        activity_list = ["Basic Exploratory Analysis", "Data Vizualizations"]
        activity = st.sidebar.selectbox("Choose activity", activity_list)

        if activity == "Basic Exploratory Analysis":
            # Show head
            if st.sidebar.checkbox("Head", key="head"):
                st.subheader("DataFrame's Head")
                st.write(df.head())

            # Show tail
            if st.sidebar.checkbox("Tail", key="tail"):
                st.subheader("DataFrame's Tail")
                st.write(df.tail())

            # Show description
            if st.sidebar.checkbox("Describe", key="desc"):
                st.subheader("DataFrame's Description")
                st.write(df.describe())

            # Show missing values
            if st.sidebar.checkbox("Missing Values", key="mv"):
                st.subheader("DataFrame's Missing Values")
                st.write(df.isnull().sum())

            # Show unique values
            if st.sidebar.checkbox("Unique Values", key="unique"):
                col = st.sidebar.selectbox("Choose a column", df.columns)
                st.subheader(f"{col}'s Unique Values")
                st.write(df[col].value_counts())

        elif activity == "Data Visualizations":
            # Relation plot
            if st.sidebar.checkbox("Relational Plot", key="rel"):
                st.subheader("Relational Plot")
                if len(numerical_col) > 1:
                    x = st.sidebar.selectbox("Choose a column", numerical_col)
                    del numerical_col[numerical_col.index(x)]
                    y = st.sidebar.selectbox("Choose another column", numerical_col)
                    kind = st.sidebar.radio("Kind", ["scatter", "line"])
                    hue = st.sidebar.selectbox("Hue (Optional)", categorical_col.insert(0, None))
                    sns.relplot(x=x, y=y, data=df, kind=kind, hue=hue)
                    st.pyplot()
                else:
                    st.warning("Not enough columns to create plot")

            # Categorical plot
            if st.sidebar.checkbox("Categorical Plot", key="cat"):
                if (len(numerical_col) and len(categorical_col)) > 1:
                    x = st.sidebar.selectbox("Choose a column", categorical_col, key="cat_1")
                    y = st.sidebar.selectbox("Choose another column", numerical_col, key="cat_2")
                    kind_list = ["strip", "swarm", "box", "violin", "boxen", "point", "bar"]
                    kind = st.sidebar.selectbox("Kind", kind_list, key="cat_3")
                    st.subheader(f"{kind.capitalize()} Plot")
                    hue = st.sidebar.selectbox("Hue (Optional)", categorical_col.insert(0, None), key="cat_4")
                    sns.catplot(x=x, y=y, data=df, kind=kind, hue=hue)
                    st.pyplot()
                else:
                    st.warning("Not enough columns to create plot")

            # Count plot
            if st.sidebar.checkbox("Count Plot", False, key="count"):
                if len(categorical_col) > 1:
                    col = st.sidebar.selectbox("Choose a column", categorical_col, key="count")
                    st.subheader(f"{col}'s Count Plot'")
                    sns.countplot(x=col, data=df)
                    st.pyplot()
                else:
                    st.warning("Not enough columns to create plot")

            # Distribution plot
            if st.sidebar.checkbox("Distribution Plot", False, key="dist"):
                if len(numerical_col) > 1:
                    col = st.sidebar.selectbox("Choose a column", numerical_col,  key="dist")
                    st.subheader(f"{col}'s Distribution Plot")
                    sns.distplot(df[col])
                    plt.grid(True)
                    st.pyplot()
                else:
                    st.warning("Not enough columns to create plot")

            # Heatmap
            if st.sidebar.checkbox("Correlation Heatmap", False, key="heatmap"):
                st.subheader(f"Correlation Heatmap")
                sns.heatmap(df.corr(), annot=True)
                st.pyplot()

            # Pairplot
            if st.sidebar.checkbox("Pairplot", False, key="pairplot"):
                st.subheader(f"Pairplot")
                hue = st.sidebar.selectbox("Hue (Optional)", categorical_col.insert(0, None))
                sns.pairplot(df, hue=hue)
                st.pyplot()

if __name__ == "__main__":
    main()
