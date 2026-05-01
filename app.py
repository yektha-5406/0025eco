import streamlit as st
import numpy as np

st.title("📊 Smart Investment Decision App")

num_projects = st.number_input("Number of Projects", min_value=1, max_value=3)

projects = []

for i in range(int(num_projects)):
    st.subheader(f"Project {i+1}")
    
    name = st.text_input(f"Project Name {i+1}", key=f"name{i}")
    cost = st.number_input(f"Initial Cost {i+1}", key=f"cost{i}")
    rate = st.number_input(f"Interest Rate (%) {i+1}", key=f"rate{i}")
    years = st.number_input(f"Years {i+1}", min_value=1, key=f"years{i}")

    cash_flows = []
    for y in range(int(years)):
        cf = st.number_input(f"Year {y+1} Cash Flow (Project {i+1})", key=f"cf{i}{y}")
        cash_flows.append(cf)

    projects.append({
        "name": name,
        "cost": cost,
        "rate": rate,
        "cash_flows": cash_flows
    })

def npv(rate, cash_flows, cost):
    rate = rate / 100
    total = -cost
    for i, cf in enumerate(cash_flows):
        total += cf / ((1 + rate) ** (i + 1))
    return total

def irr(cash_flows, cost):
    try:
        return np.irr([-cost] + cash_flows) * 100
    except:
        return None

def payback(cash_flows, cost):
    total = 0
    for i, cf in enumerate(cash_flows):
        total += cf
        if total >= cost:
            return i + 1
    return None

if st.button("Calculate"):
    results = []

    for p in projects:
        results.append({
            "name": p["name"],
            "npv": npv(p["rate"], p["cash_flows"], p["cost"]),
            "irr": irr(p["cash_flows"], p["cost"]),
            "payback": payback(p["cash_flows"], p["cost"])
        })

    best = max(results, key=lambda x: x["npv"])

    for r in results:
        st.write(f"### {r['name']}")
        st.write(f"NPV: ₹ {round(r['npv'],2)}")
        st.write(f"IRR: {round(r['irr'],2) if r['irr'] else 'N/A'} %")
        st.write(f"Payback: {r['payback']} years")

    st.success(f"Best Project: {best['name']}")
