import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="📊 Sales Dashboard", page_icon="💰", layout="wide")

# Custom CSS for attractive UI
st.markdown("""
    <style>
        .main {
            background-color: #f4f6fb;
        }
        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 2.5rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        .stMetric {
            background: #ffffff;
            padding: 18px;
            border-radius: 14px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.08);
            text-align: center;
            margin-bottom: 1rem;
        }
        .stButton>button, .stDownloadButton>button {
            color: white;
            background: linear-gradient(90deg, #4f8cff 0%, #38b6ff 100%);
            border: none;
            border-radius: 8px;
            padding: 0.5em 2em;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            min-width: 180px;
        }
        .st-expanderHeader {
            font-weight: 600;
            color: #4f8cff;
        }
        /* Responsive metrics, charts, tables, and buttons */
        @media (max-width: 1200px) {
            .block-container {
                max-width: 98vw;
                padding-left: 1.2rem;
                padding-right: 1.2rem;
            }
        }
        @media (max-width: 900px) {
            section[data-testid="stHorizontalBlock"] > div {
                flex-direction: column !important;
            }
            .stMetric {
                margin-bottom: 1.5rem;
            }
            .stButton>button, .stDownloadButton>button {
                width: 100% !important;
                min-width: unset;
            }
        }
        @media (max-width: 700px) {
            .block-container {
                padding-left: 0.7rem;
                padding-right: 0.7rem;
            }
            .stMetric {
                font-size: 1rem;
                padding: 12px;
            }
            .stButton>button, .stDownloadButton>button {
                font-size: 1rem;
                width: 100% !important;
            }
            .stDataFrame, .stTable {
                font-size: 0.95rem !important;
            }
        }
        @media (max-width: 500px) {
            .block-container {
                padding-left: 0.3rem;
                padding-right: 0.3rem;
            }
            .stMetric {
                font-size: 0.95rem;
                padding: 8px;
            }
            .stButton>button, .stDownloadButton>button {
                font-size: 0.95rem;
                width: 100% !important;
            }
            .stDataFrame, .stTable {
                font-size: 0.9rem !important;
            }
        }
        /* Make plotly charts responsive */
        .element-container:has(.js-plotly-plot) {
            width: 100% !important;
            min-width: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/sales-performance.png", width=80)
    st.title("💰 Sales Dashboard")
    st.markdown("Upload your sales CSV and explore interactive analytics.")
    st.markdown("---")
    st.info("Tip: Columns should include **City**, **Product**, **Sales**, **Quantity**.")

# Main Title
st.markdown("<h2 style='color:#4f8cff;'>📊 Interactive Sales Dashboard</h2>", unsafe_allow_html=True)

# File uploader
file = st.file_uploader("📂 Upload your Sales Data (CSV)", type=["csv"])

if file:
    df = pd.read_csv(file)
    # Normalize column names for consistency
    df.columns = df.columns.str.strip().str.lower()

    # Data Preview
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Summary Statistics
    with st.expander("📈 Summary Statistics"):
        st.write(df.describe())

    # City Filter
    if "city" in df.columns:
        cities = df["city"].dropna().unique()
        selected_city = st.selectbox("🏙️ Filter by City", sorted(cities))
        filtered_df = df[df["city"] == selected_city]

        st.markdown(f"<h4 style='color:#38b6ff;'>📍 Data for {selected_city}</h4>", unsafe_allow_html=True)
        st.dataframe(filtered_df, use_container_width=True)

        # KPIs
        # Fix KPI metrics visibility
        st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        color: black !important;   /* Value ka color */
        font-weight: 700 !important;
        opacity: 1 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #333333 !important; /* Label ka color */
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #008000 !important; /* Delta green */
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

        # st.markdown("<h4 style='color:#4f8cff;'>📊 Key Metrics</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)


        # Check for required columns
        if "sales" in filtered_df.columns and "quantity" in filtered_df.columns:
            with col1:
                st.metric("Total Sales 💰", f"${filtered_df['sales'].sum():,.0f}")
            with col2:
                st.metric("Total Quantity 📦", f"{filtered_df['quantity'].sum():,}")
            with col3:
                st.metric("Average Sales 🏷️", f"${filtered_df['sales'].mean():,.2f}")
        else:
            st.warning("⚠️ 'Sales' or 'Quantity' column not found.")

        # Charts
        st.markdown("<h4 style='color:#1236bb;'>📊 Visualizations</h4>", unsafe_allow_html=True)
        chart1, chart2 = st.columns(2)

        # Bar Chart: Sales by Product
        with chart1:
            if "product" in filtered_df.columns and "sales" in filtered_df.columns:
                fig = px.bar(
                    filtered_df,
                    x="product",
                    y="sales",
                    color="product",
                    title=f"Sales by Product in {selected_city}",
                    text_auto=True,
                    color_discrete_sequence=px.colors.qualitative.Plotly  # High-contrast, colorblind-friendly
                )
                fig.update_layout(
                    plot_bgcolor="#3B4D7A",
                    paper_bgcolor="#E8908D",
                    font=dict(color="#222"),
                    title_font=dict(size=19, color="#000000")
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Bar chart: 'Product' or 'Sales' column missing.")

        # Pie Chart: Sales Share by Product
        with chart2:
            if "product" in filtered_df.columns and "sales" in filtered_df.columns:
                fig = px.pie(
                    filtered_df,
                    names="product",
                    values="sales",
                    title=f"Sales Share by Product in {selected_city}",
                    color_discrete_sequence=px.colors.qualitative.Safe  # Colorblind-safe palette
                )
                fig.update_traces(textinfo='percent+label')
                fig.update_layout(
                    plot_bgcolor="#3B4D7A",
                    paper_bgcolor="#F5A19E",
                    font=dict(color="#222"),
                    title_font=dict(size=18, color="#01070a")
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Pie chart: 'Product' or 'Sales' column missing.")

        # Download filtered data
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Filtered Data", data=csv, file_name="filtered_sales.csv", mime="text/csv")
    else:
        st.warning("⚠️ 'City' column not found in the uploaded data.")
else:
    st.info("👆 Upload a CSV file to see your sales dashboard.")


