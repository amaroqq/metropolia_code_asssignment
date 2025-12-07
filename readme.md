# 📊 AI Feedback Intelligence Dashboard

A Python-based tool that automatically analyzes student course feedback using **Mistral AI**. It classifies comments into categories (e.g., "Course Content", "Facilities") and determines sentiment (Positive, Negative, Neutral), visualizing the results in an interactive web dashboard.

## ✨ Features

* **AI-Powered Analysis:** Uses the Mistral API to intelligently categorize text and detect sentiment.
* **Interactive Dashboard:** A clean Flask web interface to view results.
* **Data Visualization:** Dynamic Doughnut and Pie charts (using Chart.js) to visualize sentiment distribution per category.
* **Smart Sorting:** Sort feedback by ID, Category, or Sentiment (logically ordered: Negative → Neutral → Positive).
* **Exportable Data:** Saves all analysis to a local `data.json` file.

## 🛠️ Prerequisites

* Python 3.8+
* A **Mistral AI** API Key (Get one [here](https://console.mistral.ai/))

## 🚀 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/amaroqq/metropolia_code_asssignment.git](https://github.com/amaroqq/metropolia_code_asssignment.git)
    cd REPO_NAME
    ```

2.  **Create a Virtual Environment** (Recommended)
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration

**Important:** Never share your API key publicly.

1.  Open `analyze.py`.
2.  Find the line `API_KEY = ...`.
3.  **Option A (Quick Test):** Paste your key directly (Do NOT commit this to GitHub).
4.  **Option B (Secure):** Use an environment variable:
    
    ```python
    import os
    API_KEY = os.environ.get("MISTRAL_API_KEY")
    ```
    
    *Then set it in your terminal:*
    * Windows: `set MISTRAL_API_KEY=your_actual_key`
    * Mac/Linux: `export MISTRAL_API_KEY=your_actual_key`

## 🏃‍♂️ Usage

1.  **Start the Web Server:**
    ```bash
    python app.py
    ```

2.  **Open the Dashboard:**
    Open your web browser and go to: `http://127.0.0.1:5000`

3.  **Run Analysis:**
    Click the **"🔄 Run New Analysis"** button on the dashboard. This will:
    * Send comments from `analyze.py` to Mistral AI.
    * Update `data.json`.
    * Refresh the page with new charts and tables.

## 📂 Project Structure

* `app.py`: The Flask application that renders the web dashboard.
* `analyze.py`: The logic script that connects to Mistral AI and processes text.
* `data.json`: Stores the analyzed feedback data.
* `requirements.txt`: List of Python dependencies.
