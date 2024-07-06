import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🎬")
st.title("HDB dataset")
st.write(
    """
    This project delves into analyzing and visualizing trends in Singapore HDB resale prices spanning from 1990 to 2023, leveraging Streamlit to create interactive data/graph visualizations. The objective is to provide insightful data exploration tools for stakeholders including buyers, investors, agents, and policymakers, facilitating informed decision-making. Streamlit will serve as the primary platform for developing dynamic user interfaces with features like filtering by year, flat type, and town. These interactive capabilities will enable users to explore trends over time and across different property categories dynamically. With Streamlit, the project aims to transform static data into engaging narrative tools, enhancing user engagement and supporting comprehensive analysis in the Singapore HDB resale market context.

    The dataset selected for this analysis comprises comprehensive records of Singapore HDB resale prices from 1990 to 2023, available through sources like Kaggle. It includes detailed attributes such as transaction month, town, flat type (ranging from 1-room to multi-generation), flat model (e.g., New Generation, Improved), lease commencement date, storey range, floor area, remaining lease, and the resale price. This dataset offers a longitudinal perspective, spanning over three decades, enabling a thorough examination of trends in the HDB resale market. Its richness in data allows for in-depth analysis of factors influencing resale prices across different housing types, locations, and periods. Insights derived from this dataset are crucial for understanding market dynamics, and policy impacts, and informing strategic decisions for stakeholders in Singapore's housing market.

    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/elizabethjosephkoithara/Desktop/Kaplan/Mon_ICT305/Assg/01/HDB Dataset/resale-flat-prices-based-on-approval-date-1990-1999_locationdata.csv")
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
genres = st.multiselect(
    "Genres",
    df.genre.unique(),
    ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
)

# Show a slider widget with the years using `st.slider`.
years = st.slider("Years", 1986, 2006, (2000, 2016))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]
df_reshaped = df_filtered.pivot_table(
    index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="year", ascending=False)


# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year")},
)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
)
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("year:N", title="Year"),
        y=alt.Y("gross:Q", title="Gross earnings ($)"),
        color="genre:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
