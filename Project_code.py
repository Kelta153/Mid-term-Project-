import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from streamlit_extras.metric_cards import style_metric_cards
import time

st.set_page_config(page_title="Super-store sale", page_icon="🌍", layout="wide")

# Load Custom CSS with Color Scheme
st.markdown("""
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    .center-table {
        width: 80%;
    }
    [data-testid=metric-container] {
        box-shadow: 0 0 4px #686664;
        padding: 10px;
        background-color: #314b60;
        color: #ffffff;
    }
    .plot-container>div {
        box-shadow: 0 0 2px #070505;
        padding: 5px;
        border-color: #000000;
        background-color: #314b60;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.2rem;
        color: #000000;
        border-color: #000000;
    }
    .sidebar-content {
        color: white;
    }
    [data-testid=stSidebar] {
        background-color: #314b60;
        color: white;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #99ff99, #FFFF00);
    }
    body {
        background-color: #ffffff;
        color: #000002;
    }
    .section {
        margin: 40px 0;
    }
    .section img {
        width: 100%;
        height: auto;
        border-radius: 10px;
    }
    .section h2 {
        color: #9900ad;
    }
    .section p {
        color: #000000;
        font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Dashboard"],
        icons=["house", "bar-chart"],
        menu_icon="cast",
        default_index=0
    )

if selected == "Home":
    st.markdown("""
        <h2 style='text-align: center; color: #9900ad;'>Welcome to the Superstore Sales Dashboard</h2>
        <p style='text-align: center;'>Analyze and predict future sales for Furniture, Office Supplies, and Technology categories with our interactive dashboard.</p>
        """, unsafe_allow_html=True)

    
    # Introduction to Time-Series Analysis Section
    st.markdown("""
    <div class="section">
        <div style="display: flex; align-items: center;">
            <div style="flex: 1; padding-right: 20px;">
                <h2>Understanding Time-Series Analysis</h2>
                <p>Time-series analysis involves analyzing a sequence of data points collected over time to identify patterns, trends, and seasonal variations. It's widely used in various fields such as finance, economics, environmental studies, and retail.</p>
                <p>With time-series analysis, businesses can make data-driven decisions by forecasting future trends based on historical data. This helps in inventory management, demand planning, and strategic decision-making.</p>
            </div>
            <div style="flex: 1;">
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8ZGF0YSUyMHNjaWVuY2V8ZW58MHx8MHx8fDA%3D" alt="Time-Series Analysis">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # About the App Section
    st.markdown("""
    <div class="section">
        <div style="display: flex; align-items: center; flex-direction: row-reverse;">
            <div style="flex: 1; padding-left: 20px;">
                <h2>About This App</h2>
                <p>This application leverages advanced time-series forecasting models to provide accurate sales predictions for your Superstore's key product categories. Whether you are a business owner or a data analyst, our intuitive dashboard offers valuable insights to help you make informed decisions.</p>
            </div>
            <div style="flex: 1;">
                <img src="https://images.unsplash.com/photo-1591696205602-2f950c417cb9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8ZGF0YSUyMHNjaWVuY2V8ZW58MHx8MHx8fDA%3D" alt="About This App">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

     # Features Section
    st.markdown("""
    <div class="feature-section">
        <h2 style='text-align: center; color: #9900ad;'>Key Features</h2>
        <ul style='font-size: 50px;'>
            <li>📈 Interactive and user-friendly dashboard</li>
            <li>🔍 Detailed time-series analysis for different product categories</li>
            <li>💡 Insights and trends to optimize your business strategy</li>
            <li>📊 Visualizations including line charts, bar graphs, and pie charts</li>
            <li>🧠 Advanced forecasting models for accurate predictions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("""
    <div class="section">
        <div style="text-align: center;">
            <h2>Get Started</h2>
            <p>Navigate to the <strong>Dashboard</strong> tab to explore the sales predictions and insights. Start optimizing your business strategy today!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Title and Description
    dash_1 = st.container()
    with dash_1:
        st.markdown("<h2 style='text-align: center; color: #9900ad;'>Superstore Sales Dashboard</h2>", unsafe_allow_html=True)
        st.write("This application allows you to predict future sales for Furniture, Office Supplies, and Technology categories. Please enter the number of months for the sales prediction below and click on 'Predict' to see the forecasted sales.")

    # Load models
    with open('fb_furniture_model.pkl', 'rb') as file:
        fb_furniture_model = joblib.load(file) 

    with open('sarimax_office_model.pkl', 'rb') as file:
        sarimax_office_model = joblib.load(file)

    with open('fb_tech_model.pkl', 'rb') as file:
        fb_tech_model = joblib.load(file)

    # User input for number of months
    num_of_months = st.number_input('Enter Number of Months of Sales Prediction', min_value=1, step=1)

    # Prediction button
    if st.button("Predict"):
        # Load datasets
        monthly_furniture_df = pd.read_csv('furniture_data.csv')
        monthly_office_supplies_df = pd.read_csv('office_supplies_data.csv')
        monthly_technology_df = pd.read_csv('technology_data.csv')
        
        # Convert date column to datetime and set as index
        monthly_furniture_df['Order Date'] = pd.to_datetime(monthly_furniture_df['Order Date'])
        monthly_office_supplies_df['Order Date'] = pd.to_datetime(monthly_office_supplies_df['Order Date'])
        monthly_technology_df['Order Date'] = pd.to_datetime(monthly_technology_df['Order Date'])
        
        monthly_furniture_df.set_index('Order Date', inplace=True)
        monthly_office_supplies_df.set_index('Order Date', inplace=True)
        monthly_technology_df.set_index('Order Date', inplace=True)
        
        # Find the last date in the datasets
        last_date_furniture = monthly_furniture_df.index[-1]
        last_date_office = monthly_office_supplies_df.index[-1]
        last_date_tech = monthly_technology_df.index[-1]
        
        # Increment the last date by one month to get the start date for forecasting
        start_date_furniture = last_date_furniture + pd.DateOffset(months=1)
        start_date_office = last_date_office + pd.DateOffset(months=1)
        start_date_tech = last_date_tech + pd.DateOffset(months=1)
        
        # Create DataFrames with future dates
        future_furniture = pd.DataFrame({'ds': pd.date_range(start=start_date_furniture, periods=num_of_months, freq='MS')})
        future_tech = pd.DataFrame({'ds': pd.date_range(start=start_date_tech, periods=num_of_months, freq='MS')})
        forecast_end_date_office = start_date_office + pd.DateOffset(months=num_of_months-1)

        # Generate forecasts
        furniture_pred = fb_furniture_model.predict(future_furniture)
        office_pred = sarimax_office_model.predict(start=start_date_office, end=forecast_end_date_office)
        technology_pred = fb_tech_model.predict(future_tech)
        
        # Rename columns and set index
        furniture_pred = furniture_pred.rename(columns={'ds': 'Order Date'})
        technology_pred = technology_pred.rename(columns={'ds': 'Order Date'})
        furniture_pred.set_index('Order Date', inplace=True)
        technology_pred.set_index('Order Date', inplace=True)
        furniture_pred['Furniture'] = furniture_pred['yhat']
        
        # Combine predictions
        sales_prediction = furniture_pred['Furniture']
        combined_predictions = pd.concat([sales_prediction, office_pred, technology_pred['yhat']], axis=1)
        combined_predictions.columns = ['Furniture', 'Office', 'Technology']

        # Display predictions in a centered format with a pie chart beside it
        dash_2 = st.container()
        with dash_2:
            col_center, col_pie = st.columns([2, 4])
            with col_center:
                st.markdown("<h3 style='color: #9900ad;'>Predicted Sales</h3>", unsafe_allow_html=True)
                st.markdown("<div class='center'><div class='center-table'>", unsafe_allow_html=True)
                st.dataframe(combined_predictions)
                st.markdown("</div></div>", unsafe_allow_html=True)

            with col_pie:
                total_sales = combined_predictions.sum()
                sales_distribution = pd.DataFrame({'Category': total_sales.index, 'Sales': total_sales.values})
                fig_pie = px.pie(sales_distribution, values='Sales', names='Category', title='Sales Distribution by Category', color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_pie)

        # Container for bar graph and line graph side by side
        dash_3 = st.container()
        with dash_3:
            col1, col2 = st.columns(2)
            with col1:
                # Line graph for forecasted store sales
                fig_line = px.line(combined_predictions, 
                                x=combined_predictions.index, 
                                y=['Furniture', 'Office', 'Technology'],
                                labels={'value': 'Sales', 'Order Date': 'Order Date'},
                                title='Forecasted Store Sales')
                fig_line.update_layout(title_font=dict(color='#9900ad'), plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font=dict(color='#000002'))
                st.plotly_chart(fig_line)
            
            with col2:
                # Bar graph for sales comparison by category
                fig_bar = px.bar(sales_distribution, x='Category', y='Sales', title='Sales Comparison by Category')
                fig_bar.update_layout(title_font=dict(color='#9900ad'), plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font=dict(color='#000002'))
                st.plotly_chart(fig_bar)

        # Container for additional box plots
        dash_4 = st.container()
        with dash_4:
            col3, col4, col5 = st.columns(3)
            with col3:
                # Box plot for Furniture Sales
                fig_box_furniture = px.box(combined_predictions, y='Furniture', title='Box Plot of Furniture Sales')
                fig_box_furniture.update_layout(title_font=dict(color='#9900ad'), plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font=dict(color='#000002'))
                st.plotly_chart(fig_box_furniture)
            
            with col4:
                # Box plot for Office Sales
                fig_box_office = px.box(combined_predictions, y='Office', title='Box Plot of Office Sales')
                fig_box_office.update_layout(title_font=dict(color='#9900ad'), plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font=dict(color='#000002'))
                st.plotly_chart(fig_box_office)

            with col5:
                # Box plot for Technology Sales
                fig_box_tech = px.box(combined_predictions, y='Technology', title='Box Plot of Technology Sales')
                fig_box_tech.update_layout(title_font=dict(color='#9900ad'), plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font=dict(color='#000002'))
                st.plotly_chart(fig_box_tech)

        # Container for scatter plots side by side
        dash_5 = st.container()
        with dash_5:
            col6, col7 = st.columns(2)
            with col6:
                fig_scatter_furniture = px.scatter(combined_predictions.reset_index(), 
                                                x='index', y='Furniture', 
                                                title='Furniture Sales Trends', 
                                                labels={'index': 'Order Date', 'Furniture': 'Sales'})
                fig_scatter_furniture.update_layout(title_font=dict(color='#9900ad'), plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font=dict(color='#000002'))
                st.plotly_chart(fig_scatter_furniture)
            
            with col7:
                fig_scatter_office = px.scatter(combined_predictions.reset_index(), 
                                                x='index', y='Office', 
                                                title='Office Supplies Sales Trends', 
                                                labels={'index': 'Order Date', 'Office': 'Sales'})
                fig_scatter_office.update_layout(title_font=dict(color='#9900ad'), plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font=dict(color='#000002'))
                st.plotly_chart(fig_scatter_office)
        
        fig_scatter_technology = px.scatter(combined_predictions.reset_index(), 
                                            x='index', y='Technology', 
                                            title='Technology Sales Trends', 
                                            labels={'index': 'Order Date', 'Technology': 'Sales'})
        fig_scatter_technology.update_layout(title_font=dict(color='#9900ad'), plot_bgcolor='#ffffff', paper_bgcolor='#ffffff', font=dict(color='#000002'))
        st.plotly_chart(fig_scatter_technology)

        # Container for highest and lowest sales month per category
        dash_6 = st.container()
        with dash_6:
            st.markdown("<h3 style='text-align: center; color: #9900ad;'>Highest and Lowest Sales Month</h3>", unsafe_allow_html=True)
            col8, col9, col10 = st.columns(3)
            
            def create_bar_chart(df, category):
                max_month = df[category].idxmax()
                min_month = df[category].idxmin()
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=[max_month, min_month],
                    y=[df.loc[max_month, category], df.loc[min_month, category]],
                    text=[df.loc[max_month, category], df.loc[min_month, category]],
                    textposition='auto',
                    name=category
                ))
                fig.update_layout(
                    title=f'Highest and Lowest Sales Month for {category}',
                    title_font=dict(color='#9900ad'),
                    xaxis_title='Month',
                    yaxis_title='Sales',
                    plot_bgcolor='#ffffff',
                    paper_bgcolor='#ffffff',
                    font=dict(color='#000002')
                )
                return fig

            with col8:
                st.plotly_chart(create_bar_chart(combined_predictions, 'Furniture'))
            
            with col9:
                st.plotly_chart(create_bar_chart(combined_predictions, 'Office'))
            
            with col10:
                st.plotly_chart(create_bar_chart(combined_predictions, 'Technology'))

        # Additional Information section
        with st.expander("View Data Sources"):
            col11, col12, col13 = st.columns(3)

            with col11:
                st.write("### Furniture Data")
                st.dataframe(monthly_furniture_df)
        
            with col12:
                st.write("### Office Supplies Data")
                st.dataframe(monthly_office_supplies_df)
        
            with col13:
                st.write("### Technology Data")
                st.dataframe(monthly_technology_df)

# Hide Streamlit style elements
st.markdown("""
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>
    """, unsafe_allow_html=True)
