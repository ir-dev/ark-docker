from flask import Flask, send_file, render_template, request, jsonify
import plotly.graph_objects as go
import plotly.express as px # Still useful for other charts, even if not directly used for gauge here
import plotly.io as pio
import pandas as pd
import io
import numpy as np
import random
from datetime import datetime
import tempfile
import os
import traceback
from io import BytesIO

app = Flask(__name__)

# --- Helper function to generate and serve Plotly images ---
def serve_plotly_image(fig, base_filename="chart.png", width=800, height=500, scale=1):
    """
    Generates a Plotly figure, saves it to a temporary PNG file, and then serves it.
    The temporary file is automatically deleted after sending.
    """
    # temp_file = tempfile.NamedTemporaryFile(suffix=f"_{base_filename}", delete=False)
    # temp_filepath = temp_file.name
    # temp_file.close()
    #output_filepath = os.path.join(os.getcwd(), base_filename)
    output_filepath = f"./{base_filename}"

    try:
        pio.write_image(fig, output_filepath, format='png', width=width, height=height, scale=scale)
        print(f"Chart saved to: {output_filepath}")
        response = send_file(output_filepath, mimetype='image/png', download_name=base_filename, as_attachment=False)
        return response
    finally:
        #if os.path.exists(temp_filepath):
        #    os.remove(temp_filepath)
        print(f"File {output_filepath} persists after serving.")


# --- Root Endpoint to display images ---
@app.route('/')
def index():
    return render_template('index.html', now=datetime.now().timestamp())

# --- API Endpoint for Layered Bar Chart (unchanged) ---
@app.route('/layered-bar-chart-image')
def layered_bar_chart_image():
    # Dynamic Data for Layered Bar Chart
    categories = ['Category A', 'Category B', 'Category C', 'Category D']
    sub_categories = ['Series 1', 'Series 2', 'Series 3']

    data = []
    for cat in categories:
        for sub_cat in sub_categories:
            data.append({
                'Category': cat,
                'Sub_Category': sub_cat,
                'Value': random.randint(10, 50) + random.random()
            })
    df = pd.DataFrame(data)

    fig = px.bar(df,
                 x='Category',
                 y='Value',
                 color='Sub_Category',
                 title='Dynamic Layered Bar Chart Report',
                 labels={'Value': 'Amount', 'Category': 'Main Category'},
                 barmode='stack')

    fig.update_layout(
        xaxis_title="Product Category",
        yaxis_title="Total Sales (Units)",
        font=dict(family="Arial", size=12, color="RebeccaPurple"),
        title_font_size=20,
        margin=dict(l=50, r=50, t=80, b=50),
        legend_title_text='Data Series'
    )

    return serve_plotly_image(fig, base_filename="layered_bar_chart.png", width=900, height=600, scale=1.5)

# --- API Endpoint for Gauge Report with Custom Annotations as Legend ---
@app.route('/gauge-report-image', methods=['POST'])
def gauge_report_image():
    data = request.get_json()
    current_value = round(random.uniform(0, 100), 1)

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = current_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "<b>Performance Metric</b><br><span style='font-size:0.8em;color:gray'>Target: 80%</span>", 'font': {'size': 24}},
        delta = {'reference': 80, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkcyan"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "lightgreen"},
                {'range': [75, 100], 'color': "lightblue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90 # The threshold line will appear at this value
            }
        }
    ))

    # --- Add Custom Annotations for Legend ---
    # Annotations are positioned relative to the plot's paper (figure) in 'paper' coordinates (0 to 1)
    # x=1.05, y=0.8 means 5% to the right of the plot, 80% down from the top
    legend_x_pos = 0.95 # Slightly right of center
    legend_y_start = 0.8 # Starting high up

    # Legend Title
    # fig.add_annotation(
    #     x=legend_x_pos, y=legend_y_start + 0.1, # Position above the legend items
    #     text="<b>Legend</b>",
    #     xref="paper", yref="paper",
    #     showarrow=False,
    #     font=dict(size=14, color="black"),
    #     xanchor="left", yanchor="top"
    # )

    # Low Range
    fig.add_annotation(
        x=legend_x_pos, y=legend_y_start,
        text="<span style='color:lightgray; font-size:20px;'>&#9632;</span> 0-50% (Low)", # &#9632; is a square symbol
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=12, color="gray"),
        xanchor="left", yanchor="top"
    )

    # Medium Range
    fig.add_annotation(
        x=legend_x_pos, y=legend_y_start - 0.05, # Adjust y position for spacing
        text="<span style='color:lightgreen; font-size:20px;'>&#9632;</span> 50-75% (Medium)",
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=12, color="gray"),
        xanchor="left", yanchor="top"
    )

    # High Range
    fig.add_annotation(
        x=legend_x_pos, y=legend_y_start - 0.1,
        text="<span style='color:lightblue; font-size:20px;'>&#9632;</span> 75-100% (High)",
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=12, color="gray"),
        xanchor="left", yanchor="top"
    )


    fig.update_layout(
        height=400,
        margin=dict(l=20, r=120, t=50, b=20), # Increase right margin to make space for annotations
        paper_bgcolor="white",
        font=dict(color="darkblue", family="Arial"),
        showlegend=False, # Make sure standard legend is OFF
    )

    return serve_plotly_image(fig, base_filename="gauge_report.png", width=600, height=450, scale=1.5)

@app.route('/gauge-report/<wapp_reqid>', methods=['POST'])
def gauge_report_wapp(wapp_reqid):
    # Get JSON data from the request body
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    # Extract parameters with default values
    current_value = data.get('current_value', 75.0)
    max_value = data.get('max_value', 100.0)
    threshold_value = data.get('threshold_value', 90.0)
    report_title = data.get('report_title', "Performance Metric")
    target_text = data.get('target_text', "Target: 80%")

    # Optional: Custom steps/colors from JSON
    # Example structure: [{"range_end": 50, "color": "lightgray"}, ...]
    custom_steps = data.get('steps', [
        {"range_end": 50, "color": "lightgray", "label": "Yesterday"},
        {"range_end": 75, "color": "lightgreen", "label": "Today"},
        {"range_end": 100, "color": "lightblue", "label": "Tomorrow"}
    ])

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = current_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"<b>{report_title}</b><br><span style='font-size:0.8em;color:gray'>{target_text}</span>", 'font': {'size': 24}},
        delta = {'reference': 80, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkcyan"},
            'steps': [
                {'range': [0, step['range_end']], 'color': step['color']}
                for step in custom_steps
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold_value
            }
        }
    ))

    # Add Custom Annotations for Legend based on custom_steps
    legend_x_pos = 1
    legend_y_start = 1

    # fig.add_annotation(
    #     x=legend_x_pos, y=legend_y_start + 0.1,
    #     text="<b>Legend</b>",
    #     xref="paper", yref="paper",
    #     showarrow=False,
    #     font=dict(size=14, color="black"),
    #     xanchor="left", yanchor="top"
    # )

    for i, step in enumerate(custom_steps):
        fig.add_annotation(
            x=legend_x_pos, y=legend_y_start - (i * 0.05),
            text=f"<span style='color:{step['color']}; font-size:20px;'>&#9632;</span> {step.get('label', step['range_end'])}",
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=12, color="gray"),
            xanchor="left", yanchor="top"
        )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=120, t=50, b=20),
        paper_bgcolor="white",
        font=dict(color="darkblue", family="Arial"),
        showlegend=False,
    )

    return serve_plotly_image(fig, base_filename=f"{wapp_reqid}.png", width=600, height=450, scale=1.5)

@app.route('/gantt-report/<wapp_reqid>', methods=['POST'])
def generate_gantt(wapp_reqid):
    try:
        data = request.get_json()

        # Validate input
        #if not isinstance(data, list):
        #    return jsonify({"error": "Payload must be a list of task objects"}), 400

        # Convert to DataFrame
        df = pd.DataFrame(data['maintenances'])

        # Parse datetimes
        df['Start'] = pd.to_datetime(df['start'])
        df['Finish'] = pd.to_datetime(df['end'])

        # Basic error check
        if df.empty or 'machine_name' not in df or 'reason' not in df:
            return jsonify({"error": "Missing required fields"}), 400

        # Assign unique Y-axis based on machine name
        df["Y"] = df["machine_name"]

        # Create unique color for each reason
        unique_reasons = df["reason"].unique()
        color_palette = px.colors.qualitative.Plotly
        color_map = {reason: color_palette[i % len(color_palette)] for i, reason in enumerate(unique_reasons)}

        fig = go.Figure()

        for _, row in df.iterrows():
            fig.add_trace(go.Scatter(
                x=[row["Start"], row["Finish"]],
                y=[row["Y"], row["Y"]],
                mode='lines',
                line=dict(color=color_map.get(row["reason"], "gray"), width=20),
                hoverinfo='text',
                text=f"{row['reason']}: {row['Start']} → {row['Finish']}",
                showlegend=False
            ))

        fig.update_layout(
            title=data['title'],
            xaxis=dict(
                type='date',
                title=data['x-title'],
                tickformat='%Y-%m-%d\n%H:%M',
                range=[
                    df["Start"].min() - pd.Timedelta(hours=1),
                    df["Finish"].max() + pd.Timedelta(hours=1)
                ]
            ),
            yaxis=dict(
                title=data['y-title'],
                tickvals=df["Y"].unique(),
                autorange='reversed'
            ),
            height=400 + len(df["Y"].unique()) * 30,
            margin=dict(l=100, r=20, t=50, b=50)
        )

        # Output as PNG
        #buffer = io.BytesIO()
        #fig.write_image(buffer, format='png')
        #buffer.seek(0)

        #return send_file(buffer, mimetype='image/png', download_name='machine_gantt.png')
        return serve_plotly_image(fig, base_filename=f"{wapp_reqid}.png", width=600, height=450, scale=1)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/db-report/<wapp_reqid>', methods=['POST'])
def generate_dumbbell_image(wapp_reqid):
    data = request.get_json()
    # Convert to DataFrame
    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['qty'] = pd.to_numeric(df['qty'])
    
    # Verify we have exactly two dates for comparison
    dates = sorted(df['date'].unique(), reverse=True)[:2]
    date1, date2 = dates[0], dates[1]

    df = df[df['date'].isin([date1, date2])]
    
    # Pivot data correctly
    pivot_df = df.pivot(index='machine_name', columns='date', values='qty')
    
    # Create figure
    fig = go.Figure()
    
    # Add dumbbell lines
    for machine in pivot_df.index:
        fig.add_trace(go.Scatter(
            x=[pivot_df.loc[machine, date1], pivot_df.loc[machine, date2]],
            y=[machine, machine],
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add markers for each date
    colors = ['#636EFA', '#EF553B']  # Distinct colors for each date
    
    for i, date in enumerate([date1, date2]):
        fig.add_trace(go.Scatter(
            x=pivot_df[date],
            y=pivot_df.index,
            mode='markers',
            marker=dict(size=12, color=colors[i]),
            name=str(date),  # Date-only in legend
            hovertemplate=(
                "<b>Machine:</b> %{y}<br>"
                "<b>Date:</b> " + str(date) + "<br>"
                "<b>Quantity:</b> %{x}<extra></extra>"
            )
        ))
    
    # Customize layout
    fig.update_layout(
        title=f'{data["title"]}: {date1} vs {date2}',
        xaxis_title=f'{data["x-title"]}',
        yaxis_title=f'{data["y-title"]}',
        plot_bgcolor='white',
        legend_title_text='Date',
        hovermode='closest'
    )

    return serve_plotly_image(fig, base_filename=f"{wapp_reqid}.png", width=600, height=450, scale=1)

@app.route('/hb-report/<wapp_reqid>', methods=['POST'])
def generate_horizontal_bar(wapp_reqid):
    data = request.get_json()
    # Convert to DataFrame
    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['qty'] = pd.to_numeric(df['qty'])
    
    # Sort by quantity for better visualization
    df = df.sort_values('qty', ascending=True)
    
    # Create horizontal bar chart
    fig = px.bar(
        df,
        x='qty',
        y='machine_name',
        orientation='h',
        color='date',
        color_continuous_scale='Blues',
        title=f'{data["title"]}',
        labels={'qty': f'{data["x-title"]}', 'machine_name': f'{data["y-title"]}', 'date': 'Date'},
        text_auto=True  # Show values on bars
    )
    
    # Customize layout
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_title='Production Quantity',
        yaxis_title='Machine',
        coloraxis_showscale=False,  # Hide color scale
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    
    # Adjust bar appearance
    fig.update_traces(
        textfont_size=12,
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5
    )
    
    return serve_plotly_image(fig, base_filename=f"{wapp_reqid}.png", height=450, scale=1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)