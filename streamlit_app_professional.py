import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Configure page with professional styling
st.set_page_config(
    page_title="Publication Trends Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional presentation style
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: white;
        color: black;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        color: #1f2937;
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #4b5563;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Control panel styling */
    .control-panel {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .control-title {
        color: #1f2937;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    /* Summary section styling */
    .summary-section {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    
    /* Ensure all text is black */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stRadio > div,
    .stSlider > div,
    .stMarkdown,
    p, h1, h2, h3, h4, h5, h6, span, div {
        color: #1f2937 !important;
    }
    
    /* Style the selectbox and multiselect widgets */
    .stSelectbox label,
    .stMultiSelect label,
    .stRadio label,
    .stSlider label {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(path="master_database_detailed.csv"):
    df = pd.read_csv(path)
    # Ensure correct dtypes
    df['Year'] = df['Year'].astype(int)
    df['Search_Topic_ID'] = df['Search_Topic_ID'].astype(int)
    df['Record_Count'] = df['Record_Count'].astype(int)
    return df

# Color and style helpers
def get_color_scheme():
    return {
        0: '#1f77b4',  # Blue
        1: '#ff7f0e',  # Orange
        2: '#2ca02c',  # Green
        3: '#d62728',  # Red
        4: '#9467bd',  # Purple
        5: '#8c564b'   # Brown
    }

def get_line_styles():
    return {
        'TS': 'solid',
        'KW': 'dash',
        'TI': 'dot'
    }

def hex_to_rgba(hex_color: str, alpha: float = 0.2) -> str:
    """Convert #RRGGBB hex string to an rgba(...) string with given alpha."""
    if not isinstance(hex_color, str):
        return hex_color
    h = hex_color.lstrip('#')
    if len(h) == 3:
        r, g, b = (int(h[i] * 2, 16) for i in range(3))
    elif len(h) >= 6:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
    else:
        return hex_color
    return f'rgba({r},{g},{b},{alpha})'

# Load data
with st.spinner("Loading publication data..."):
    df = load_data()

# Create mapping for topics
topic_map = df[['Search_Topic_ID', 'Search_Topic']].drop_duplicates().set_index('Search_Topic_ID')['Search_Topic'].to_dict()
# Ensure topics 0-5 present
for tid in range(6):
    if tid not in topic_map:
        topic_map[tid] = f"Topic {tid}"

# Header
st.markdown('<div class="main-header">Publication Trends Analysis (1975–2024)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Analysis of Research Publication Patterns by Topic and Search Strategy</div>', unsafe_allow_html=True)

# Main layout: Controls (1/3) and Graph (2/3)
col_controls, col_graph = st.columns([1, 2])

with col_controls:
    # Overview section
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown('<div class="control-title">Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    **Interactive analysis tool** for exploring publication trends in ionic liquid research for electrochemistry applications. 
    Please select topics, search strategies, and time periods to visualize research patterns and growth over the past 50 years.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown('<div class="control-title">Analysis Controls</div>', unsafe_allow_html=True)
    
    # Topic selection
    options = sorted(list(topic_map.keys()))
    if options:
        default_topics = [0] if 0 in options else [options[0]]
    else:
        default_topics = []

    selected_topics = st.multiselect(
        "**Research Topics**",
        options=options,
        format_func=lambda tid: f"{tid}: {topic_map.get(tid)}",
        default=default_topics,
        help="Select one or more research topics to analyze"
    )
    
    selected_topic_ids = selected_topics

    # Search level selection
    search_strategy_options = {
        'TS': 'Topic Search (TS) - Title + Abstract + Keywords',
        'TI': 'Title Only (TI) - Title search only',
        'KW': 'Keywords & Title (KW) - Title + Keywords'
    }
    
    selected_levels = st.multiselect(
        "**Search Strategies**", 
        options=list(search_strategy_options.keys()),
        format_func=lambda x: search_strategy_options[x],
        default=['TS'],
        help="Choose different search scopes: TS (broadest), TI (most specific), or KW (moderate scope)"
    )

    # Year range
    min_year = max(1975, int(df['Year'].min()))
    max_year = min(2024, int(df['Year'].max()))
    year_start, year_end = st.select_slider(
        "**Analysis Period**",
        options=list(range(min_year, max_year + 1)),
        value=(1975, 2024),
        help="Adjust the time period for analysis"
    )

    # Y-axis scale option
    y_scale = st.radio(
        "**Y-Axis Scale**", 
        options=['Linear', 'Log'], 
        index=0,
        help="Choose between linear or logarithmic scale"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_graph:
    # Validate selection
    if not selected_topic_ids:
        st.warning("⚠️ Please select at least one research topic from the controls panel.")
        st.stop()
    if not selected_levels:
        st.warning("⚠️ Please select at least one search strategy from the controls panel.")
        st.stop()

    # Filter data
    filtered = df[
        (df['Search_Topic_ID'].isin(selected_topic_ids)) &
        (df['Search_Level'].isin(selected_levels)) &
        (df['Year'] >= year_start) &
        (df['Year'] <= year_end)
    ].copy()

    if filtered.empty:
        st.info("ℹ️ No data available for this selection. Try adjusting the filters.")
        st.stop()

    # Aggregate data
    agg = filtered.groupby(['Year', 'Search_Topic_ID', 'Search_Topic', 'Search_Level'], as_index=False)['Record_Count'].sum()

    # Build Plotly figure with professional styling
    colors = get_color_scheme()
    line_styles = get_line_styles()
    fig = go.Figure()

    # Sort by total records for consistent layering
    totals = agg.groupby(['Search_Topic_ID', 'Search_Level'])['Record_Count'].sum().reset_index()
    totals = totals.sort_values('Record_Count', ascending=False)
    order = [(r['Search_Topic_ID'], r['Search_Level']) for _, r in totals.iterrows()]

    for (topic_id, level) in order:
        subset = agg[(agg['Search_Topic_ID'] == topic_id) & (agg['Search_Level'] == level)]
        if subset.empty:
            continue
        subset = subset.sort_values(by='Year')
        name = f"{topic_map.get(topic_id, topic_id)} ({level})"
        color = colors.get(topic_id, '#333333')
        dash = line_styles.get(level, 'solid')

        fig.add_trace(go.Scatter(
            x=subset['Year'],
            y=subset['Record_Count'],
            mode='lines',
            name=name,
            line=dict(color=color, width=3, dash=dash),
            fill='tozeroy',
            fillcolor=hex_to_rgba(color, alpha=0.15),
            hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Publications: %{y:,}<extra></extra>'
        ))

    # Professional figure styling
    fig.update_layout(
        title=dict(
            text=f"Publication Trends ({year_start}–{year_end})",
            x=0.5,
            font=dict(size=20, color='#1f2937', family='Arial Black')
        ),
        xaxis=dict(
            title=dict(text='Year', font=dict(size=14, color='#1f2937')),
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            linecolor='#1f2937',
            tickfont=dict(color='#1f2937')
        ),
        yaxis=dict(
            title=dict(text='Number of Publications', font=dict(size=14, color='#1f2937')),
            type='log' if y_scale == 'Log' else 'linear',
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            linecolor='#1f2937',
            tickfont=dict(color='#1f2937')
        ),
        hovermode='x unified',
        legend=dict(
            title=dict(text='Topic (Search Strategy)', font=dict(color='#1f2937')),
            font=dict(color='#1f2937'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#1f2937',
            borderwidth=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1f2937'),
        height=600
    )

    # Display the figure
    st.plotly_chart(fig, use_container_width=True)

# Summary section at the bottom
st.markdown('<div class="summary-section">', unsafe_allow_html=True)
st.markdown('<div class="control-title">Analysis Summary</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Selected Topics:**")
    for tid in selected_topic_ids:
        st.write(f"• {tid}: {topic_map.get(tid)}")

with col2:
    st.markdown("**Search Strategies:**")
    strategy_names = {
        'TS': 'Topic Search - Title + Abstract + Keywords',
        'TI': 'Title Only - Title search only', 
        'KW': 'Keywords & Title - Title + Keywords'
    }
    for level in selected_levels:
        st.write(f"• {strategy_names.get(level, level)}")

with col3:
    st.markdown("**Analysis Parameters:**")
    st.write(f"• Period: {year_start}–{year_end}")
    st.write(f"• Y-axis: {y_scale} scale")
    st.write(f"• Data points: {len(agg):,}")

# Top combinations table
if not agg.empty:
    st.markdown("**Top Publication Combinations:**")
    display_totals = totals.head(8).copy()
    display_totals['Topic_Name'] = display_totals['Search_Topic_ID'].map(topic_map)
    display_totals = display_totals[['Topic_Name', 'Search_Level', 'Record_Count']]
    display_totals.columns = ['Research Topic', 'Search Strategy', 'Total Publications']
    st.dataframe(display_totals, use_container_width=True, hide_index=True)

# Data download
if not agg.empty:
    csv = agg.to_csv(index=False)
    st.download_button(
        "📊 Download Filtered Data (CSV)",
        data=csv,
        file_name=f"publication_trends_{year_start}_{year_end}.csv",
        mime='text/csv'
    )

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"*Analysis generated on {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}*")
