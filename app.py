from flask import Flask, render_template_string
import json
import os
import analyze  # Imports your analyze.py script

app = Flask(__name__)

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return []

# Helper function to count sentiments for the chart
def get_sentiment_counts(data):
    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for row in data:
        s = row.get('sentiment', 'Neutral')
        if s in counts:
            counts[s] += 1
        else:
            counts["Neutral"] += 1
    return counts

# --- DASHBOARD TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Feedback Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root { --primary: #4F46E5; --bg: #F3F4F6; --card-bg: #FFFFFF; --text: #1F2937; --border: #E5E7EB; }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding: 40px; }
        
        .layout { max-width: 1000px; margin: 0 auto; display: grid; gap: 20px; }
        
        /* HEADER & STATS */
        .header-card { background: var(--card-bg); padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        h1 { margin: 0; font-size: 1.5rem; }
        
        .btn { background: var(--primary); color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: 500; border: none; cursor: pointer; }
        .btn:hover { background: #4338ca; }
        .btn.loading { opacity: 0.7; cursor: wait; }

        /* CHART SECTION */
        .chart-container {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            height: 300px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* TABLE SECTION */
        .table-card { background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th { text-align: left; padding: 12px; border-bottom: 2px solid var(--border); color: #6B7280; font-size: 0.85rem; text-transform: uppercase; cursor: pointer; user-select: none; }
        th:hover { color: var(--primary); background: #f9fafb; }
        th::after { content: ' ↕'; font-size: 0.7em; opacity: 0.5; }
        td { padding: 14px 12px; border-bottom: 1px solid var(--border); }
        
        /* BADGES */
        .badge { padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
        .pos { background: #D1FAE5; color: #065F46; }
        .neg { background: #FEE2E2; color: #991B1B; }
        .neu { background: #F3F4F6; color: #374151; }
        .category-tag { background: #EEF2FF; color: #4F46E5; padding: 4px 8px; border-radius: 6px; font-weight: 500; font-size: 0.85rem;}
    </style>
</head>
<body>

    <div class="layout">
        <div class="header-card">
            <div>
                <h1>📊 Dashboard</h1>
                <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9em;">Overview of user feedback</p>
            </div>
            <a href="/run" class="btn" onclick="this.classList.add('loading'); this.innerHTML='Running...';">
                🔄 Run Analysis
            </a>
        </div>

        <div class="chart-container">
            <div style="width: 400px; height: 100%;">
                <canvas id="sentimentChart"></canvas>
            </div>
        </div>

        <div class="table-card">
            <table id="dataTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">ID</th>
                        <th onclick="sortTable(1)">Comment</th>
                        <th onclick="sortTable(2)">Category</th>
                        <th onclick="sortTable(3)">Sentiment</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in data %}
                    <tr>
                        <td data-val="{{ row.id }}" style="color: #9CA3AF;">#{{ row.id }}</td>
                        <td>{{ row.text }}</td>
                        <td><span class="category-tag">{{ row.category }}</span></td>
                        
                        {% if row.sentiment == 'Positive' %}
                            <td data-val="3"><span class="badge pos">Positive</span></td>
                        {% elif row.sentiment == 'Negative' %}
                            <td data-val="1"><span class="badge neg">Negative</span></td>
                        {% else %}
                            <td data-val="2"><span class="badge neu">Neutral</span></td>
                        {% endif %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // --- 1. CHART LOGIC ---
        // We get the data passed from Python directly into JS
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        const sentimentData = {{ counts | tojson }}; // Pass Python dict to JS
        
        new Chart(ctx, {
            type: 'doughnut', // 'pie' or 'doughnut'
            data: {
                labels: ['Positive', 'Negative', 'Neutral'],
                datasets: [{
                    data: [sentimentData.Positive, sentimentData.Negative, sentimentData.Neutral],
                    backgroundColor: ['#10B981', '#EF4444', '#9CA3AF'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right' },
                    title: { display: true, text: 'Sentiment Distribution' }
                }
            }
        });

        // --- 2. SORTING LOGIC (FIXED) ---
        function sortTable(n) {
            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            table = document.getElementById("dataTable");
            switching = true;
            dir = "asc"; 
            
            while (switching) {
                switching = false;
                rows = table.rows;
                
                for (i = 1; i < (rows.length - 1); i++) {
                    shouldSwitch = false;
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    
                    // GET THE RAW VALUE
                    // If data-val exists (for ID and Sentiment), use it. Otherwise use text.
                    var xVal = x.getAttribute('data-val') ? parseFloat(x.getAttribute('data-val')) : x.innerHTML.toLowerCase();
                    var yVal = y.getAttribute('data-val') ? parseFloat(y.getAttribute('data-val')) : y.innerHTML.toLowerCase();

                    if (dir == "asc") {
                        if (xVal > yVal) { shouldSwitch = true; break; }
                    } else if (dir == "desc") {
                        if (xVal < yVal) { shouldSwitch = true; break; }
                    }
                }
                
                if (shouldSwitch) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount ++; 
                } else {
                    if (switchcount == 0 && dir == "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    data = load_data()
    counts = get_sentiment_counts(data)
    # We pass 'counts' to the template so the Chart can use it
    return render_template_string(HTML_TEMPLATE, data=data, counts=counts)

@app.route('/run')
def run_analysis():
    try:
        analyze.analyze_all()
    except Exception as e:
        print(f"Error: {e}")
    return index()

if __name__ == '__main__':
    app.run(debug=True)