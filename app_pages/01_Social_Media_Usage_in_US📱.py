import streamlit as st
import pandas as pd
import numpy as np
import requests
import openpyxl
from io import StringIO, BytesIO
## zy add
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



# def load_excel(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return pd.read_csv(StringIO(response.text))
#     else:
#         st.error("Failed to load data from GitHub.")


#################################################### Original Data ####################################################
## Read data from GitHub
### % of U.S. adults who say they ever use ... by ...
us_usage_by_group_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/data/Social_Media_Usage_pivoted.xlsx"
response1 = requests.get(us_usage_by_group_url)
if response1.status_code == 200:
    us_usage_by_group = pd.read_excel(BytesIO(response1.content), header=0, engine='openpyxl')
else:
    st.error("Failed to load data from GitHub.")

### % of U.S. adults who say they ever use … (Polls from 2012-2021)
us_popular_platforms_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/data/which_social_media_platforms_are_most_popular_data_2024-01-31.csv"
response2 = requests.get(us_popular_platforms_url)
if response2.status_code == 200:
    us_popular_platforms = pd.read_csv(StringIO(response2.text), skiprows=3, delimiter=',', header=0)
else:
    st.error("Failed to load data from GitHub.")
us_popular_platforms = us_popular_platforms.iloc[:-3, :]

us_popular_platforms.rename(columns={'\t\t\tYear': 'Year'}, inplace=True)
us_popular_platforms['Year'] = us_popular_platforms['Year'].str.replace('\t\t', '')
us_popular_platforms['Year'] = pd.to_datetime(us_popular_platforms['Year'])




#################################################### Streamlit ####################################################
st.header("American's Social Media Usage Dashboard")
link1 = "https://www.pewresearch.org/internet/2024/01/31/americans-social-media-use/"
st.write("You can find the related report [here](%s)"%link1)
st.subheader("Original Data")
ori_on = st.toggle("Would you like to see the original data?", False)

def placeholder(lines):
    for _ in range(lines):
        st.markdown("\n")

if ori_on:
    
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        dim_option = st.selectbox("Please select a dimension you want to check",
                                    ('All', 'Age', 'Gender', 'Income', 'Political Affiliation', 'Race & Ethnicity'))
        if dim_option == 'All':
            st.markdown(f"% of U.S. adults who say they ever use ... by ...")
            st.dataframe(us_usage_by_group)
        else:
            st.markdown(f"% of U.S. adults who say they ever use ... by {dim_option}")
            st.dataframe(us_usage_by_group[us_usage_by_group['Dimension'] == dim_option])

    with col2:
        placeholder(5)
        st.markdown(f"% of U.S. adults who say they ever use ...(Polls from 2012-2021)")
        st.write(us_popular_platforms)


st.subheader("Reproduction 📊")


## LJM add
st.markdown("#### 1.Platform Popularity Changing Recent Years in U.S.")
def clean_us_social_media_data(df):
    # Melt the dataframe
    us_social_media_tidy = df.melt(id_vars=["Year"], var_name="Platform", value_name="Percentage")

    # Transform year to datetime tyoe
    us_social_media_tidy["Year"] = pd.to_datetime(us_social_media_tidy["Year"], errors='coerce')

    # Remove the % sign and transform to float type
    us_social_media_tidy["Percentage"] = us_social_media_tidy["Percentage"].str.replace('%', '').astype(float)
    
    us_social_media_tidy.dropna(subset=['Year', 'Percentage'], inplace=True)

    return us_social_media_tidy

# clean data
us_social_media_tidy = clean_us_social_media_data(us_popular_platforms)


# Create plot
def create_social_media_popularity_plot(data):
    fig = px.line(
        data, 
        x="Year", 
        y="Percentage", 
        color="Platform",
        title="Which Social Media Platform Is More Popular",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Set the scale of y axis and add % sign on axis
    fig.update_yaxes(range=[0, 100], ticksuffix="%")

    # Add vertical line 
    fig.add_vline(
        x='2022-01-01',  
        line_width=2,
        line_color="gray"
    )

    # Add annotation for vertical line
    fig.add_annotation(
        x='2022-01-01',
        y=95,  
        text="Change in survey mode --",
        showarrow=False,
        font=dict(size=12, color="gray"),
        xanchor='left', 
        xshift=-130
    )

    # Set the format of interactive label
    fig.update_traces(
        hovertemplate='%{x|%d-%m-%Y} <br> %{fullData.name}: %{y} <extra></extra>', 
        marker=dict(size=8)
    )

    # Set the scale of x axis
    fig.update_xaxes(range=['2012-07-01', '2023-12-31'])

    return fig
    
# Create plot
fig = create_social_media_popularity_plot(us_social_media_tidy)
st.plotly_chart(fig, use_container_width=True)

st.markdown("##### :blue[* Improve the visualization by using the animation]")
# Embad code
flourish_embed_code = """
<div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/20240242">
    <script src="https://public.flourish.studio/resources/embed.js"></script>
    <noscript>
        <img src="https://public.flourish.studio/visualisation/20240242/thumbnail" width="100%" alt="bar-chart-race visualization" />
    </noscript>
</div>
"""

# Show animation
st.components.v1.html(flourish_embed_code, height=600)


### ZY add
st.markdown("#### 2.Age Range Distribution Across Different Platforms")

# Convert percentage values and clean data function

def clean_and_prepare_data(df):
    # Filter data for age dimension
    usage_by_age = df[df['Dimension'] == 'Age'].copy()

    # Convert percentage column values
    def convert_percentage(value):
        if value == '<1':
            return 0
        try:
            return float(value)
        except ValueError:
            return None
    
    usage_by_age['Percentage'] = usage_by_age['Percentage'].apply(convert_percentage)

    # Standardize platform names
    usage_by_age['Platform'] = usage_by_age['Platform'].replace({
        'Tik Tok': 'TikTok',
        'Twitter (X)': 'Twitter',
        'You Tube': 'YouTube'
    })

    # Standardize age group names
    usage_by_age['Category'] = usage_by_age['Category'].replace({'Ages 18-29': '18-29'})

    # Calculate the difference between the usage percentages for age groups 18-29 and 65+
    age_gap_diff = usage_by_age.pivot(index='Platform', columns='Category', values='Percentage')
    age_gap_diff['Youngest - oldest DIFF'] = age_gap_diff['18-29'] - age_gap_diff['65+']
    
    # Reset index and drop rows where Platform is "Be Real"
    age_gap_diff = age_gap_diff.reset_index()
    age_gap_diff = age_gap_diff[age_gap_diff['Platform'] != 'Be Real']
    
    # Define platforms and age groups for later use
    platforms = age_gap_diff['Platform'].unique()
    age_groups = ['18-29', '30-49', '50-64', '65+']

    # Define colors for age groups
    age_colors = {
        '18-29': '#003366',  # Dark blue
        '30-49': '#336699',  # Mid blue
        '50-64': '#99CC99',  # Light green
        '65+': '#99CC33'     # Dark green
    }

    # Melt the DataFrame for visualization
    df_long = age_gap_diff.melt(
        id_vars=['Platform', 'Youngest - oldest DIFF'],
        value_vars=age_groups,
        var_name='Age Group',
        value_name='Percentage'
    )
    df_long['Age Group'] = pd.Categorical(df_long['Age Group'], categories=age_groups, ordered=True)

    return usage_by_age, age_gap_diff, df_long, age_colors

# Apply the cleaning and preparation function to the loaded data
usage_by_age, age_gap_diff, df_long, age_colors = clean_and_prepare_data(us_usage_by_group)

# 使用处理好的数据绘制图表的函数
def create_age_gap_scatter_plot(df_long, age_gap_diff, age_colors):
    # 创建散点图
    fig = px.scatter(
        df_long,
        x='Percentage',
        y='Platform',
        color='Age Group',
        color_discrete_map=age_colors,
        labels={'Percentage': 'Percentage(%)'},
        hover_data={'Percentage': True, 'Platform': True, 'Age Group': True},
        size_max=10  # 设置最大标记大小
    )

    # 添加每个平台的最小和最大百分比之间的连接线
    for platform in df_long['Platform'].unique():
        platform_data = df_long[df_long['Platform'] == platform]
        percentages = platform_data['Percentage'].dropna()
        if len(percentages) >= 2:
            min_percentage = percentages.min()
            max_percentage = percentages.max()
            fig.add_trace(go.Scatter(
                x=[min_percentage, max_percentage],
                y=[platform, platform],
                mode='lines',
                line=dict(color='gray', width=7),
                opacity=0.15,
                showlegend=False
            ))

    # 在每个点上方添加百分比标签
    for i, row in df_long.iterrows():
        fig.add_annotation(
            x=row['Percentage'],
            y=row['Platform'],
            text=f"{int(row['Percentage'])}%",
            showarrow=False,
            yshift=10,  # 调整标签的垂直位置
            font=dict(size=12, color=age_colors[row['Age Group']])
        )

    # 在右侧添加差值标签，灰色背景
    for i, row in age_gap_diff.iterrows():
        diff_value = row['Youngest - oldest DIFF']
        diff_text = f"+{int(diff_value)}" if not np.isnan(diff_value) else 'N/A'
        fig.add_annotation(
            x=105,
            y=row['Platform'],
            text=diff_text,
            showarrow=False,
            xanchor='left',
            bgcolor='lightgray',
            font=dict(size=10, color='black')
        )

    # 更新布局样式
    fig.update_layout(
        title='Age Gaps in Social Media Usage Across Platforms',
        xaxis_title='Percentage of U.S. adults in each age group who say they ever use',
        xaxis=dict(range=[0, 110], tickvals=np.arange(0, 101, 20)),
        yaxis_title='',
        plot_bgcolor='white',
        legend_title_text='Age Groups',
        legend_traceorder='reversed',
        width=1000,
        height=800
    )

    # 移除网格线并调整边距
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_layout(margin=dict(l=100, r=200, t=100, b=100))

    return fig

# 创建并显示图表
fig = create_age_gap_scatter_plot(df_long, age_gap_diff, age_colors)
st.plotly_chart(fig)

st.markdown("##### :blue[* Improve the visualization by using the stack diagram]")

def clean_age_gap_stack_plot_data(usage_by_age):
    # Normalize the percentages for each platform to ensure they sum up to 100%
    usage_by_age['Percentage_scaled'] = usage_by_age.groupby('Platform')['Percentage'].transform(lambda x: (x / x.sum()) * 100)
    
    # Pivot the DataFrame so that age categories become columns
    usage_by_age_scaled = usage_by_age.pivot(index='Platform', columns='Category', values='Percentage_scaled').reset_index()
    
    return usage_by_age_scaled

usage_by_age_scaled = clean_age_gap_stack_plot_data(usage_by_age)

def create_age_gap_stack_plot(usage_by_age_scaled):
    age_groups = ['18-29', '30-49', '50-64', '65+']
    # Melt the dataframe to long format for Plotly
    usage_by_age_scaled_long = usage_by_age_scaled.melt(id_vars='Platform', value_vars=age_groups,
                                                        var_name='Age Group', value_name='Percentage')
    
    # Create the stacked bar plot using Plotly Express
    fig = px.bar(usage_by_age_scaled_long, 
                 x='Platform', 
                 y='Percentage', 
                 color='Age Group', 
                 title="Stacked Age Distribution by Social Media Platform",
                 labels={'Percentage': 'Percentage (%)'},
                 color_discrete_map=age_colors,  # Apply custom colors for age groups
                 height=600)
    
    # Update layout to match the original Matplotlib plot
    fig.update_layout(barmode='stack',
                      xaxis_title="Platform",
                      yaxis_title="Percentage (%)",
                      legend_title="Age Group",
                      legend=dict(title="Age Group", x=1.05, y=1, traceorder='normal', orientation='v')
                      )
    
    return fig

# Creat the stack plot
fig = create_age_gap_stack_plot(usage_by_age_scaled)
st.plotly_chart(fig, use_container_width=True)

## NMY add
st.markdown("#### 3.Demographic differences in use of online platforms")
st.markdown("###### How use of online platforms differs among some U.S. demographic groups")
st.markdown("###### - such as Facebook, Instagram or TikTok - ")

def clean_and_prepare_heatmap_data(existing_df):
    # 定义手动输入的数据
    categories = ['Total', 'HS or less', 'Some college', 'College+', 'Urban', 'Suburban', 'Rural']
    platforms = ['YouTube', 'Facebook', 'Instagram', 'Pinterest', 'TikTok', 'LinkedIn', 'WhatsApp', 'Snapchat', 'Twitter', 'Reddit', 'BeReal']
    percentages = [
        [83, 68, 47, 35, 33, 30, 29, 27, 22, 22, 3],
        [74, 63, 37, 26, 35, 10, 25, 26, 15, 14, 3],
        [85, 71, 50, 42, 38, 28, 23, 32, 24, 23, 4],
        [89, 70, 55, 38, 26, 53, 39, 23, 29, 30, 4],
        [85, 66, 53, 31, 36, 31, 38, 29, 25, 29, 4],
        [85, 68, 49, 36, 31, 36, 30, 26, 26, 24, 4],
        [77, 70, 38, 36, 33, 18, 20, 27, 13, 14, 2]
    ]

    # 创建新的 DataFrame
    new_data = {
        'Platform': [],
        'Dimension': [],
        'Category': [],
        'Percentage': []
    }

    for category, percentage_list in zip(categories, percentages):
        dimension = 'Education' if category in ['HS or less', 'Some college', 'College+'] else 'Residence' if category != 'Total' else ' '
        
        for platform, percentage in zip(platforms, percentage_list):
            new_data['Platform'].append(platform)
            new_data['Dimension'].append(dimension)
            new_data['Category'].append(category)
            new_data['Percentage'].append(percentage)

    new_df = pd.DataFrame(new_data)

    # 合并新数据和现有数据
    df = pd.concat([existing_df, new_df], ignore_index=True)

    # 数据清理和标准化
    df['Percentage'] = df['Percentage'].replace('<1', 0.5).astype(float)
    df['Platform'] = df['Platform'].replace({
        'You Tube': 'YouTube',
        'Be Real': 'BeReal',
        'Linked In': 'LinkedIn',
        'Tik Tok': 'TikTok',
        'Twitter (X)': 'Twitter',
        'Whats App': 'WhatsApp'
    })
    df['Category'] = df['Category'].replace({
        'Ages 18-29': '18-29',
        'Asian*': 'Asian',
        '$100,000+': 'More than $100K',
        'Less than $30,000': 'Less than $30K',
        '$30,000- $69,999': '$30K-$69,999',
        '$70,000- $99,999': '$70K-$99,999'
    })

    # 按照各个维度分组数据
    grouped_data = {
        'Total': df[df['Dimension'] == ' '].pivot_table(index='Category', columns='Platform', values='Percentage'),
        'Gender': df[df['Dimension'] == 'Gender'].pivot_table(index='Category', columns='Platform', values='Percentage'),
        'Race & Ethnicity': df[df['Dimension'] == 'Race & Ethnicity'].pivot_table(index='Category', columns='Platform', values='Percentage'),
        'Age': df[df['Dimension'] == 'Age'].pivot_table(index='Category', columns='Platform', values='Percentage'),
        'Income': df[df['Dimension'] == 'Income'].pivot_table(index='Category', columns='Platform', values='Percentage'),
        'Education': df[df['Dimension'] == 'Education'].pivot_table(index='Category', columns='Platform', values='Percentage'),
        'Residence': df[df['Dimension'] == 'Residence'].pivot_table(index='Category', columns='Platform', values='Percentage'),
        'Political Affiliation': df[df['Dimension'] == 'Political Affiliation'].pivot_table(index='Category', columns='Platform', values='Percentage')
    }
    
    return grouped_data

# 调用清理函数
grouped_data = clean_and_prepare_heatmap_data(us_usage_by_group)

# 创建热力图的函数，带有数值注释和自定义颜色条位置和长度
def create_annotated_heatmap(data):
    fig = go.Figure(
        data=go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index,
            colorscale='Blues',
            zmin=0,
            zmax=100,
            text=data.values,  # 将数值添加为注释
            texttemplate="%{text}",  
            textfont={"size": 15},  # 调整字体大小
            colorbar=dict(
                title='% of U.S. adults who say they ever use...',
                titleside='top',
                orientation='h',  # 切换到水平颜色条
                thickness=20,
                x=0.5,
                y=1.5,  # 将颜色条在图表顶部的位置上调
                len=0.6
            )
        )
    )
    
    cell_width=150
    cell_height=50
    
    fig.update_layout(
        width= cell_width * len(data.columns) +300,
        height= cell_height * len(data.index) +200,
        margin=dict(l=10, r=10, t=0, b=0),  # 增加顶部边距以容纳颜色条的标题
        xaxis=dict(side='top'),
        yaxis=dict(autorange="reversed")
    )

    return fig


def create_annotated_bar(df):
    # 创建条形图
    fig = go.Figure()

    # 遍历每个类别并添加到图表中
    for category in df.index:
        fig.add_trace(go.Bar(
            x=df.columns,  # 平台名称
            y=df.loc[category],  # 对应的值
            name=category  # 类别名称
        ))

    # 更新布局
    fig.update_layout(
        xaxis_title='Platform',
        yaxis_title='% of U.S. adults who say they ever use...',
        barmode='group',  # 显示分组的条形图
        width=900,  # 设置图像宽度
        height=500,  # 设置图像高度
        legend=dict(
            orientation="h",  # 横向布局颜色条
            x=0.5,
            xanchor="center",
            y=1.1,
            yanchor="bottom"
        ),
    )
    
    return fig


hm_url = "https://raw.githubusercontent.com/heyyyjiaming/DSS5201-SocialMediaUsage-Dashboard/refs/heads/main/img/heatmap.png"
st.image(hm_url)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("##### :blue[* Improve the visualization with the user-friendly select box]")
st.markdown("<br>", unsafe_allow_html=True)

dim_op = st.selectbox("Please select a dimension you want to check",
                                    ('Total', 'Gender', 'Race & Ethnicity', 'Age', 'Income', 'Residence',  'Education', 'Political Affiliation'))

catglist = grouped_data[f'{dim_op}'].index.tolist()
catglist.insert(0, '*All')

catg_op = '*All'
if dim_op and (dim_op != 'Total'):
    catg_op = st.selectbox("Please select a category you want to check", catglist)

data = grouped_data[dim_op]
if (catg_op != '*All'):
    data = data.loc[[catg_op]] 


st.markdown(f"###### Social Media Usage by {dim_op} group")

st.markdown(f"Heatmap")
heatmap_fig = create_annotated_heatmap(data)
st.plotly_chart(heatmap_fig, use_container_width=True)
    

st.markdown(f"Bar Chart")
bar_fig = create_annotated_bar(data)
st.plotly_chart(bar_fig, use_container_width=True)
