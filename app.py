import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Main title
    st.title("Exploratory Data Analysis (EDA) Tool")
    st.sidebar.title("Exploratory Data Analysis (EDA) Tool")
    st.markdown("### By [Richard Cornelius Suwandi](https://github.com/richardcsuwandi)")
    st.sidebar.markdown("By [Richard Cornelius Suwandi](https://github.com/richardcsuwandi)")

    # Upload file
    uploaded_file = st.sidebar.file_uploader("Upload file here", type="csv")

    if uploaded_file is None:
        st.info("Upload a CSV file to get started")
    else:
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

        elif activity == "Data Vizualizations":
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

            if st.sidebar.checkbox("Categorical Plot", key="cat"):
                if (len(numerical_col) and len(categorical_col)) > 1:
                    x = st.sidebar.selectbox("Choose a column", categorical_col)
                    y = st.sidebar.selectbox("Choose another column", numerical_col)
                    kind_list = ["strip", "swarm", "box", "violin", "boxen", "point", "bar"]
                    kind = st.sidebar.selectbox("Kind", kind_list)
                    st.subheader(f"{kind.capitalize()} Plot")
                    hue = st.sidebar.selectbox("Hue (Optional)", categorical_col.insert(0, None))
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
                    st.subheader(f"{col}'s Distribution Plot'")
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