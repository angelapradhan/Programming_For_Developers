import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import math
import matplotlib.pyplot as plt
import itertools
import time

# 1. DATA LOADING
def load_data():
    try:
        with open('sample_tourist_spots.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "JSON file 'sample_tourist_spots.json' bhetiyena!")
        return []

# 2. DISTANCE CALCULATION (Euclidean)
def calculate_dist(p1_lat, p1_long, p2_lat, p2_long):
    return math.sqrt((p2_lat - p1_lat)**2 + (p2_long - p1_long)**2) * 100

# 3. HEURISTIC OPTIMIZATION (Greedy Strategy)
def heuristic_optimization(data, budget, available_time, interest):
    start_time = time.time()
    selected = []
    total_cost = 0
    total_time = 0

    sorted_spots = sorted(data, key=lambda x: (interest in x['tags']), reverse=True)
    
    for spot in sorted_spots:
        if (interest in spot['tags']) or (interest == ""):
            if (total_cost + spot['entry_fee'] <= budget) and \
               (total_time + spot['visit_time'] <= available_time):
                selected.append(spot)
                total_cost += spot['entry_fee']
                total_time += spot['visit_time']
                
    execution_time = time.time() - start_time
    return selected, total_cost, total_time, execution_time

# 4. BRUTE-FORCE SOLUTION
def brute_force_optimization(data, budget, available_time, interest):
    start_time = time.time()
    best_combination = []
    max_spots = 0
    
    for i in range(1, len(data) + 1):
        for combo in itertools.combinations(data, i):
            c_cost = sum(s['entry_fee'] for s in combo)
            c_time = sum(s['visit_time'] for s in combo)
            c_match = all(interest in s['tags'] for s in combo) if interest else True
            
            if c_cost <= budget and c_time <= available_time and c_match:
                if len(combo) > max_spots:
                    max_spots = len(combo)
                    best_combination = combo
                    
    execution_time = time.time() - start_time
    return list(best_combination), execution_time

# 5. UI LOGIC & VISUALIZATION
def run_planner():
    data = load_data()
    if not data: return
    
    try:
        u_budget = float(entry_budget.get())
        u_time = float(entry_time.get())
        u_interest = entry_interest.get().lower()
        
        h_res, h_cost, h_duration, h_exec = heuristic_optimization(data, u_budget, u_time, u_interest)
        
        b_res, b_exec = brute_force_optimization(data, u_budget, u_time, u_interest)
        
        display_results(h_res, h_cost, h_duration, h_exec, b_res, b_exec)
        
        if h_res:
            show_path_map(h_res)
            
    except ValueError:
        messagebox.showerror("Input Error", "Budget ra Time ma number lekhnu hola.")

def display_results(h_res, h_cost, h_duration, h_exec, b_res, b_exec):
    result_box.delete(1.0, tk.END)
    report = f"--- SUGGESTED ITINERARY (HEURISTIC) ---\n"
    if not h_res:
        report += "No spots match your criteria.\n"
    else:
        for i, s in enumerate(h_res):
            report += f"{i+1}. {s['name']} (Fee: Rs.{s['entry_fee']}, Time: {s['visit_time']}h)\n"
            report += f"   - Justification: High interest match within constraints.\n"
        
        report += f"\nTotal Cost: Rs.{h_cost}\n"
        report += f"Total Time Spent: {h_duration} hours\n"
        
    report += f"\n--- PERFORMANCE COMPARISON ---\n"
    report += f"Heuristic Spots Found: {len(h_res)} (Time: {h_exec:.6f}s)\n"
    report += f"Brute-Force Spots Found: {len(b_res)} (Time: {b_exec:.6f}s)\n"
    report += f"Discussion: Brute-force ensures maximum spots but execution time increases exponentially with data size."
    
    result_box.insert(tk.END, report)

def show_path_map(spots):
    names = [s['name'] for s in spots]
    lats = [s['lat'] for s in spots]
    longs = [s['long'] for s in spots]
    
    plt.figure(figsize=(8, 5))
    plt.plot(longs, lats, marker='o', linestyle='-', color='#007bff', linewidth=2)
    for i, name in enumerate(names):
        plt.annotate(f"{i+1}. {name}", (longs[i], lats[i]), xytext=(5,5), textcoords='offset points')
    
    plt.title("Visit Sequence Map (Euclidean Path)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, alpha=0.3)
    plt.show()

# 6. GUI DESIGN
root = tk.Tk()
root.title("Kathmandu Tourist Path Optimizer")
root.geometry("500x700")
root.configure(bg="#ffffff")

tk.Label(root, text="TOURIST OPTIMIZER", font=("Arial", 20, "bold"), fg="#1a2a6c", bg="#ffffff").pack(pady=20)

form = tk.Frame(root, bg="#ffffff")
form.pack(pady=10)

def create_field(label_text):
    tk.Label(form, text=label_text, font=("Arial", 10), bg="#ffffff").pack(anchor="w")
    entry = tk.Entry(form, width=35, font=("Arial", 11), bd=1, relief="solid")
    entry.pack(pady=(2, 12), ipady=5)
    return entry

entry_time = create_field("Total Time Available (Hours):")
entry_budget = create_field("Maximum Budget (Rs):")
entry_interest = create_field("Interest (nature, culture, adventure):")

btn_plan = tk.Button(root, text="GENERATE ITINERARY", command=run_planner, 
                     bg="#007bff", fg="white", font=("Arial", 12, "bold"), 
                     width=25, pady=10, cursor="hand2", relief="flat")
btn_plan.pack(pady=20)

result_box = scrolledtext.ScrolledText(root, width=55, height=12, font=("Arial", 10), bd=1, relief="solid")
result_box.pack(pady=10, padx=20)

root.mainloop()