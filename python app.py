from flask import Flask, request, render_template_string
import numpy as np

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Investment App</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        h1 { color: #333; }
        .card { background: white; padding: 15px; margin: 10px 0; border-radius: 10px; }
        .best { color: green; font-weight: bold; }
    </style>
</head>
<body>

<h1>📊 Smart Investment Decision App</h1>

<form method="POST">
    <label>Number of Projects:</label>
    <input type="number" name="num_projects" id="num_projects" min="1" max="3" required>
    <button type="button" onclick="generateFields()">Generate</button>

    <div id="projects"></div><br>

    <button type="submit">Calculate</button>
</form>

{% if results %}
<h2>Results</h2>

{% for r in results %}
<div class="card">
    <h3>{{ r.name }}</h3>
    <p>NPV: ₹ {{ r.npv }}</p>
    <p>IRR: {{ r.irr }} %</p>
    <p>Payback: {{ r.payback }} years</p>
</div>
{% endfor %}

<h2 class="best">Best Project: {{ best.name }}</h2>
{% endif %}

<script>
function generateFields() {
    let n = document.getElementById("num_projects").value;
    let container = document.getElementById("projects");
    container.innerHTML = "";

    for (let i = 0; i < n; i++) {
        container.innerHTML += `
        <h3>Project ${i+1}</h3>
        Name: <input name="name${i}" required><br>
        Cost: <input name="cost${i}" type="number" required><br>
        Rate (%): <input name="rate${i}" type="number" required><br>
        Years: <input name="years${i}" type="number" id="years${i}" onchange="addCF(${i})" required><br>
        <div id="cf${i}"></div><br>
        `;
    }
}

function addCF(i) {
    let years = document.getElementById("years"+i).value;
    let div = document.getElementById("cf"+i);
    div.innerHTML = "";

    for (let y = 0; y < years; y++) {
        div.innerHTML += `Year ${y+1} Cash Flow:
        <input name="cf${i}_${y}" type="number" required><br>`;
    }
}
</script>

</body>
</html>
"""

# 🔹 Calculations
def npv(rate, cash_flows, cost):
    rate = rate / 100
    total = -cost
    for i, cf in enumerate(cash_flows):
        total += cf / ((1 + rate) ** (i + 1))
    return round(total, 2)

def irr(cash_flows, cost):
    try:
        return round(np.irr([-cost] + cash_flows) * 100, 2)
    except:
        return "N/A"

def payback(cash_flows, cost):
    total = 0
    for i, cf in enumerate(cash_flows):
        total += cf
        if total >= cost:
            return i + 1
    return "Not recovered"

@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        n = int(request.form["num_projects"])

        for i in range(n):
            name = request.form[f"name{i}"]
            cost = float(request.form[f"cost{i}"])
            rate = float(request.form[f"rate{i}"])
            years = int(request.form[f"years{i}"])

            cash_flows = []
            for y in range(years):
                cash_flows.append(float(request.form[f"cf{i}_{y}"]))

            results.append({
                "name": name,
                "npv": npv(rate, cash_flows, cost),
                "irr": irr(cash_flows, cost),
                "payback": payback(cash_flows, cost)
            })

        best = max(results, key=lambda x: x["npv"])
        return render_template_string(HTML, results=results, best=best)

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
