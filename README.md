# EA SPORTS FC 25 Player Scouting & Performance Dashboard

## Overview
An interactive football analytics dashboard built with **Python**, **Pandas**, **Plotly**, and **Streamlit**.  
It analyzes player data from the **EA SPORTS FC 25** database, allowing users to explore, compare, and scout players based on performance metrics.

The project demonstrates practical applications of data analysis and visualization in sports, helping users uncover insights and identify top-performing young players.

---

## Features
- **Player Explorer:** Filter and sort players by league, team, nationality, position, and attributes.  
- **Player Comparison:** Compare two players side-by-side using visual charts.  
- **Scouting Mode:** Identify young talents (≤ 25 years) ranked by a custom *Potential Index*.  
- **Interactive Visuals:** Built with Plotly for dynamic and responsive charts.  

---

## Custom Potential Index
Since the dataset lacks a “Potential” column, a custom metric was created:

```python
Potential_Index = OVR + 0.3*Pace + 0.3*Dribbling + 0.3*Passing - 0.1*Age
```

## Tech Stack

- **Python** – core programming language  
- **Pandas** – data cleaning and analysis  
- **Plotly Express** – data visualization  
- **Streamlit** – web app framework  
