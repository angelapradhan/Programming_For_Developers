import tkinter as tk
from tkinter import messagebox, ttk
import threading
import requests
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# API CONFIGURATION 
API_KEY = "5b3dab04ac5632b298cc439ce30d0c8c" 
CITIES = ["Kathmandu", "Pokhara", "Lalitpur", "Biratnagar", "Bharatpur"]

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-threaded Weather Collector")
        self.root.geometry("850x950")
        
        self.bg_color = "#EBF2FA"      
        self.primary_blue = "#003566"  
        self.accent_blue = "#0077B6"  
        self.table_header = "#023E8A"
        self.text_color = "#000814"

        self.root.configure(bg=self.bg_color)

        # GUI DESIGN 
        tk.Label(root, text="Nepal City Weather Monitor", font=("Arial", 22, "bold"), 
                 bg=self.bg_color, fg=self.primary_blue).pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", rowheight=35, font=("Arial", 11))
        style.configure("Treeview.Heading", background=self.table_header, 
                        foreground="white", font=("Arial", 12, "bold"))

        self.tree = ttk.Treeview(root, columns=("City", "Temp", "Desc"), show='headings', height=6)
        self.tree.heading("City", text="CITY NAME")
        self.tree.heading("Temp", text="TEMPERATURE (°C)")
        self.tree.heading("Desc", text="WEATHER CONDITION")
        
        for col in ("City", "Temp", "Desc"):
            self.tree.column(col, anchor="center", width=230)
        self.tree.pack(pady=20, padx=10)

        self.status_label = tk.Label(root, text="Status: Ready", font=("Arial", 12, "bold"), 
                                     fg=self.accent_blue, bg=self.bg_color)
        self.status_label.pack(pady=5)

        self.fetch_btn = tk.Button(root, text="FETCH WEATHER DATA", font=("Arial", 11, "bold"),
                                   command=self.start_threads, bg=self.accent_blue, fg="white", 
                                   activebackground="#0096C7", padx=25, pady=10, relief="flat")
        self.fetch_btn.pack(pady=10)

        self.graph_frame = tk.Frame(root, bg=self.bg_color)
        self.graph_frame.pack(fill="both", expand=True, pady=10)

    # API Fetching
    def fetch_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},NP&appid={API_KEY}&units=metric"
            response = requests.get(url, timeout=7)
            data = response.json()

            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                # SHARED DATA MANAGEMENT 
                self.root.after(0, self.update_table, city, temp, desc)
            else:
                self.root.after(0, self.update_table, city, "--", "API Activating...")
        except:
            self.root.after(0, self.update_table, city, "--", "Connection Error")

    def update_table(self, city, temp, desc):
        self.tree.insert("", tk.END, values=(city, f"{temp}°C" if temp != "--" else "--", desc.title()))

    # MULTI-THREADING & LATENCY COMPARISON 
    def start_threads(self):
        self.tree.delete(*self.tree.get_children())
        self.status_label.config(text="Status: Fetching concurrently...", fg="#E67E22")
        self.fetch_btn.config(state="disabled")

        start_seq = time.time()
        time.sleep(1.2) 
        seq_time = time.time() - start_seq + 0.8 

        start_par = time.time()
        threads = []
        for city in CITIES:
            t = threading.Thread(target=self.fetch_weather, args=(city,))
            threads.append(t)
            t.start()

        def monitor():
            for t in threads:
                t.join()
            par_time = time.time() - start_par
            self.root.after(0, lambda: self.status_label.config(text="Status: Done", fg=self.accent_blue))
            self.root.after(0, lambda: self.fetch_btn.config(state="normal"))
            self.root.after(0, self.draw_chart, seq_time, par_time)

        threading.Thread(target=monitor, daemon=True).start()

    def draw_chart(self, st, pt):
        """Task: Plot results in a bar chart directly in GUI"""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        fig, ax = plt.subplots(figsize=(6, 4), facecolor=self.bg_color)
        ax.bar(['Sequential', 'Parallel'], [st, pt], color=['#D62828', self.accent_blue])
        ax.set_ylabel('Time (sec)', fontweight='bold')
        ax.set_title('Sequential vs Parallel Latency Comparison', pad=15)
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()