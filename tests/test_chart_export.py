import os
import sys


sys.stdout.reconfigure(encoding="utf-8")

import plotly.graph_objects as go

from src.report_generator import (
    save_plotly_chart
)


figure = go.Figure()

figure.add_trace(
    go.Scatter(
        x=[
            "Day 1",
            "Day 2",
            "Day 3",
            "Day 4",
            "Day 5"
        ],
        y=[
            1000,
            1200,
            1100,
            1350,
            1500
        ],
        mode="lines+markers",
        name="Revenue"
    )
)

output_path = (
    "reports/test_chart.png"
)

save_plotly_chart(
    figure,
    output_path
)

assert os.path.exists(
    output_path
)

assert os.path.getsize(
    output_path
) > 1000

print(
    "✅ PLOTLY CHART EXPORT TEST PASSED"
)