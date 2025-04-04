import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime
import numpy as np

# --- Professional Color Palette (Dark Monochromatic) ---
BG_COLOR = "#2C3E50"         # Dark blue-gray for background
TEXT_COLOR = "#ECEFF1"       # Light gray-white for text
PRIMARY_COLOR = "#3498DB"    # Bright blue for primary actions
SECONDARY_COLOR = "#7F8C8D"  # Medium gray for secondary elements
ACCENT_COLOR = "#1ABC9C"     # Vibrant teal for success
ERROR_COLOR = "#E74C3C"      # Bright red for errors
DROPDOWN_BG = "#3A536B"      # Slightly lighter dark blue-gray
DROPDOWN_TEXT = "#ECEFF1"
DROPDOWN_HOVER = "#2ECC71"   # Emerald green for dropdown hover
BORDER_COLOR = "#34495E"     # Darker blue-gray for borders
CHART_COLORS = ["#3498DB", "#E67E22", "#1ABC9C"]  # Blue, Orange, Teal for charts

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25  # Fixed: Use widget.winfo_rooty()
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#FFFFE0",
                         relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class PageReplacement:
    def __init__(self, frame_size, ref_string):
        self.frame_size = frame_size
        self.ref_string = ref_string
        self.steps = []
        self.faults_over_time = []
        self.hits = 0
        self.misses = 0
        self.frame_states = []

    def fifo(self):
        frames = []
        faults = 0
        self.steps = []
        self.faults_over_time = []
        self.hits = 0
        self.misses = 0
        self.frame_states = []

        for i, page in enumerate(self.ref_string):
            if page not in frames:
                faults += 1
                self.misses += 1
                if len(frames) >= self.frame_size:
                    frames.pop(0)
                frames.append(page)
                self.steps.append(f"Step {i+1}: Page {page} -> Fault, Frames: {frames}")
            else:
                self.hits += 1
                self.steps.append(f"Step {i+1}: Page {page} -> Hit, Frames: {frames}")
            self.faults_over_time.append(faults)
            self.frame_states.append(frames.copy())
        return faults

    def lru(self):
        frames = []
        faults = 0
        self.steps = []
        self.faults_over_time = []
        self.hits = 0
        self.misses = 0
        self.frame_states = []

        for i, page in enumerate(self.ref_string):
            if page not in frames:
                faults += 1
                self.misses += 1
                if len(frames) >= self.frame_size:
                    frames.pop(0)
                frames.append(page)
                self.steps.append(f"Step {i+1}: Page {page} -> Fault, Frames: {frames}")
            else:
                self.hits += 1
                frames.remove(page)
                frames.append(page)
                self.steps.append(f"Step {i+1}: Page {page} -> Hit, Frames: {frames}")
            self.faults_over_time.append(faults)
            self.frame_states.append(frames.copy())
        return faults

    def optimal(self):
        frames = []
        faults = 0
        self.steps = []
        self.faults_over_time = []
        self.hits = 0
        self.misses = 0
        self.frame_states = []

        for i, page in enumerate(self.ref_string):
            if page not in frames:
                faults += 1
                self.misses += 1
                if len(frames) >= self.frame_size:
                    future = self.ref_string[i+1:]
                    farthest = -1
                    page_to_remove = frames[0]
                    for frame in frames:
                        try:
                            dist = future.index(frame)
                            if dist > farthest:
                                farthest = dist
                                page_to_remove = frame
                        except ValueError:
                            page_to_remove = frame
                            break
                    frames.remove(page_to_remove)
                frames.append(page)
                self.steps.append(f"Step {i+1}: Page {page} -> Fault, Frames: {frames}")
            else:
                self.hits += 1
                self.steps.append(f"Step {i+1}: Page {page} -> Hit, Frames: {frames}")
            self.faults_over_time.append(faults)
            self.frame_states.append(frames.copy())
        return faults

    def get_fifo_steps(self):
        self.fifo()
        return self.steps

    def get_lru_steps(self):
        self.lru()
        return self.steps

    def get_optimal_steps(self):
        self.optimal()
        return self.steps

    def get_faults_over_time(self, algo):
        if algo == "FIFO":
            self.fifo()
        elif algo == "LRU":
            self.lru()
        elif algo == "Optimal":
            self.optimal()
        return self.faults_over_time

    def get_hit_miss_ratio(self):
        total = self.hits + self.misses
        return (self.hits / total * 100, self.misses / total * 100) if total > 0 else (0, 0)

    def get_frame_states(self):
        return self.frame_states

class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Simulator")
        self.root.config(bg=BG_COLOR)
        self.root.geometry("450x750")  # Increased height to accommodate the new graph
        self.root.resizable(True, True)  # Enable maximize/minimize

        self.setup_styles()
        self.create_widgets()
        self.simulation_details = None

    def setup_styles(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')

        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR,
                             font=('Helvetica', 11))
        self.style.configure('TEntry', fieldbackground="#FFFFFF", foreground=PRIMARY_COLOR,  # Input text is blue
                             font=('Helvetica', 11), bordercolor=BORDER_COLOR,
                             lightcolor=BORDER_COLOR, darkcolor=BORDER_COLOR)
        self.style.configure('TButton', background=PRIMARY_COLOR, foreground="white",
                             font=('Helvetica', 11, 'bold'), padding=10, borderwidth=1,
                             relief="flat")
        self.style.map('TButton', background=[('active', '#0652DD')],
                       foreground=[('active', 'white')])

        # Enhanced Dropdown Style
        self.style.configure('TMenubutton', background=DROPDOWN_BG,
                             foreground=DROPDOWN_TEXT, font=('Helvetica', 11, 'bold'),
                             padding=10, relief="raised", borderwidth=2,
                             bordercolor=PRIMARY_COLOR)
        self.style.map('TMenubutton',
                       background=[('active', DROPDOWN_HOVER), ('focus', DROPDOWN_HOVER)],
                       foreground=[('active', DROPDOWN_TEXT)],
                       bordercolor=[('active', ACCENT_COLOR)])
        self.style.configure('TMenu', background=DROPDOWN_BG, foreground=DROPDOWN_TEXT,
                             borderwidth=1, activebackground=PRIMARY_COLOR,
                             activeforeground="white")

        self.style.configure('Success.TLabel', foreground=ACCENT_COLOR,
                             font=('Helvetica', 11, 'bold'))
        self.style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'),
                             foreground=TEXT_COLOR)

    def create_widgets(self):
        title_frame = ttk.Frame(self.root, relief="flat", borderwidth=1)
        title_frame.pack(pady=15, padx=10, fill="x")
        ttk.Label(title_frame, text="Page Replacement Simulator",
                  style='Title.TLabel').pack(pady=5)

        input_frame = ttk.Frame(self.root, padding=15, relief="flat", borderwidth=1)
        input_frame.pack(fill="x", padx=10)

        ttk.Label(input_frame, text="Reference String:").grid(row=0, column=0,
                                                                 sticky="w", pady=8)
        self.entry_ref = ttk.Entry(input_frame, width=30)
        self.entry_ref.grid(row=0, column=1, pady=8, sticky="ew")
        ToolTip(self.entry_ref, "Enter space-separated page numbers (e.g., 1 2 3 4)")

        ttk.Label(input_frame, text="Frame Size:").grid(row=1, column=0,
                                                               sticky="w", pady=8)
        self.entry_frames = ttk.Entry(input_frame, width=10)
        self.entry_frames.grid(row=1, column=1, pady=8, sticky="w")
        ToolTip(self.entry_frames, "Enter number of frames (e.g., 3)")

        ttk.Label(input_frame, text="Algorithm:").grid(row=2, column=0,
                                                               sticky="w", pady=8)
        self.algo_var = tk.StringVar(value="FIFO")
        algo_menu = ttk.OptionMenu(input_frame, self.algo_var, "FIFO", "FIFO",
                                   "LRU", "Optimal", style='TMenubutton')
        algo_menu.grid(row=2, column=1, pady=8, sticky="w")

        button_frame = ttk.Frame(self.root, padding=15, relief="flat", borderwidth=1)
        button_frame.pack(fill="x", padx=10)

        self.run_button = ttk.Button(button_frame, text="Run Simulation",
                                     command=self.run_simulation)
        self.run_button.pack(fill="x", pady=5)

        self.compare_button = ttk.Button(button_frame, text="Show Comparisons",
                                         command=self.show_comparisons)
        self.compare_button.pack(fill="x", pady=5)

        self.details_button = ttk.Button(button_frame, text="Show Details",
                                         command=self.show_details, state="disabled")
        self.details_button.pack(fill="x", pady=5)

        self.ratio_button = ttk.Button(button_frame, text="Show Hit/Miss Ratio",
                                       command=self.show_hit_miss_ratio, state="disabled")
        self.ratio_button.pack(fill="x", pady=5)

        self.frames_button = ttk.Button(button_frame, text="Show Frame States",
                                        command=self.show_frame_states, state="disabled")
        self.frames_button.pack(fill="x", pady=5)

        self.save_button = ttk.Button(button_frame, text="Save Results",
                                      command=self.save_results, state="disabled")
        self.save_button.pack(fill="x", pady=5)

        self.reset_button = ttk.Button(button_frame, text="Reset",
                                       command=self.reset_fields)
        self.reset_button.pack(fill="x", pady=5)

        result_frame = ttk.Frame(self.root, padding=15, relief="flat", borderwidth=1)
        result_frame.pack(fill="x", padx=10)
        self.result_label = ttk.Label(result_frame, text="Page Faults: -")
        self.result_label.pack(anchor="center")

    def validate_inputs(self):
        try:
            ref_string = [int(x) for x in self.entry_ref.get().split()]
            frame_size = int(self.entry_frames.get())
            if not ref_string or frame_size <= 0:
                raise ValueError("Invalid input values")
            return ref_string, frame_size
        except ValueError:
            messagebox.showerror("Error",
                                 "Please enter valid space-separated integers for Reference String\nand a positive integer for Frame Size",
                                 parent=self.root)
            return None, None

    def run_simulation(self):
        ref_string, frame_size = self.validate_inputs()
        if ref_string is None:
            return

        algo = self.algo_var.get()
        sim = PageReplacement(frame_size, ref_string)

        try:
            algo_methods = {
                "FIFO": lambda: (sim.fifo(), sim.get_fifo_steps(), sim.get_faults_over_time("FIFO")),
                "LRU": lambda: (sim.lru(), sim.get_lru_steps(), sim.get_faults_over_time("LRU")),
                "Optimal": lambda: (sim.optimal(), sim.get_optimal_steps(), sim.get_faults_over_time("Optimal"))
            }
            faults, steps, faults_over_time = algo_methods[algo]()
            self.simulation_details = {
                "faults": faults, "steps": steps, "algo": algo,
                "ref_string": ref_string, "frame_size": frame_size,
                "hits": sim.hits, "misses": sim.misses, "frame_states": sim.frame_states,
                "faults_over_time": faults_over_time
            }
            self.result_label.config(text=f"Page Faults using {algo}: {faults}",
                                     style='Success.TLabel')
            self.details_button.config(state="normal")
            self.ratio_button.config(state="normal")
            self.frames_button.config(state="normal")
            self.save_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}",
                                 parent=self.root)

    def show_comparisons(self):
        ref_string, frame_size = self.validate_inputs()
        if ref_string is None:
            return

        sim = PageReplacement(frame_size, ref_string)
        algorithms = ["FIFO", "LRU", "Optimal"]
        faults_over_time = {algo: sim.get_faults_over_time(algo) for algo in algorithms}
        total_faults = {algo: faults_over_time[algo][-1] for algo in algorithms}

        plot_window = tk.Toplevel(self.root, bg=BG_COLOR)
        plot_window.title("Algorithm Comparisons")
        plot_window.geometry("1000x800")

        fig = plt.Figure(figsize=(10, 7), dpi=100, facecolor=BG_COLOR)

        # Line Chart
        ax1 = fig.add_subplot(311, facecolor="#FFFFFF")
        for algo, color in zip(algorithms, CHART_COLORS):
            ax1.plot(range(1, len(ref_string) + 1), faults_over_time[algo],
                     label=algo, color=color, marker='o',linewidth=2)
        ax1.set_title("Faults Over Time (Line)", color=TEXT_COLOR)
        ax1.set_xlabel("Position", color=TEXT_COLOR)
        ax1.set_ylabel("Cumulative Faults", color=TEXT_COLOR)
        ax1.tick_params(axis='both', colors=TEXT_COLOR)
        ax1.legend(facecolor=BG_COLOR, edgecolor=BORDER_COLOR)

        # Bar Chart
        ax2 = fig.add_subplot(312, facecolor="#FFFFFF")
        ax2.bar(algorithms, [total_faults[algo] for algo in algorithms],
                color=CHART_COLORS)
        ax2.set_title("Total Faults (Bar)", color=TEXT_COLOR)
        ax2.set_ylabel("Faults", color=TEXT_COLOR)
        ax2.tick_params(axis='both', colors=TEXT_COLOR)

        # Area Chart
        ax3 = fig.add_subplot(313, facecolor="#FFFFFF")
        for algo, color in zip(algorithms, CHART_COLORS):
            ax3.fill_between(range(1, len(ref_string) + 1), faults_over_time[algo],
                             label=algo, color=color, alpha=0.5)
        ax3.set_title("Faults Over Time (Area)", color=TEXT_COLOR)
        ax3.set_xlabel("Position", color=TEXT_COLOR)
        ax3.set_ylabel("Cumulative Faults", color=TEXT_COLOR)
        ax3.tick_params(axis='both', colors=TEXT_COLOR)
        ax3.legend(facecolor=BG_COLOR, edgecolor=BORDER_COLOR)

        fig.tight_layout(pad=3.0)
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        canvas.draw()

    def show_details(self):
        if not self.simulation_details:
            messagebox.showinfo("Info", "No simulation data available",
                                 parent=self.root)
            return

        details_window = tk.Toplevel(self.root, bg=BG_COLOR)
        details_window.title(f"{self.simulation_details['algo']} Simulation Details")
        details_window.geometry("900x700")

        # Text Area for Steps
        text_frame = ttk.Frame(details_window)
        text_frame.pack(padx=10, pady=10, fill="both", expand=True)
        text = tk.Text(text_frame, height=15, width=60, bg="#FFFFFF",
                         fg=PRIMARY_COLOR,  # Modified this line to set text color to blue
                         font=("Helvetica", 10), borderwidth=1,
                         relief="flat")
        text.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(text_frame, command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar.set)

        details = f"Algorithm: {self.simulation_details['algo']}\n"
        details += f"Reference String: {' '.join(map(str, self.simulation_details['ref_string']))}\n"
        details += f"Frame Size: {self.simulation_details['frame_size']}\n"
        details += f"Total Page Faults: {self.simulation_details['faults']}\n\n"
        details += "Simulation Steps:\n"
        for step in self.simulation_details["steps"]:
            details += f"{step}\n"
        text.insert(tk.END, details)
        text.config(state="disabled")

        # Faults Over Time Graph
        graph_frame = ttk.Frame(details_window)
        graph_frame.pack(padx=10, pady=10, fill="x")
        fig = plt.Figure(figsize=(8, 4), dpi=100, facecolor=BG_COLOR)
        ax = fig.add_subplot(111, facecolor="#FFFFFF")
        ax.plot(range(1, len(self.simulation_details['ref_string']) + 1),
                self.simulation_details['faults_over_time'],
                color=PRIMARY_COLOR, marker='o', linewidth=2)
        ax.set_title("Faults Over Time", color=TEXT_COLOR)
        ax.set_xlabel("Position in Reference String", color=TEXT_COLOR)
        ax.set_ylabel("Cumulative Faults", color=TEXT_COLOR)
        ax.tick_params(axis='both', colors=TEXT_COLOR)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas.draw()

    def show_hit_miss_ratio(self):
        if not self.simulation_details:
            messagebox.showinfo("Info", "No simulation data available",
                                 parent=self.root)
            return

        sim = PageReplacement(self.simulation_details['frame_size'],
                                 self.simulation_details['ref_string'])
        algo = self.simulation_details['algo']
        {"FIFO": sim.fifo, "LRU": sim.lru, "Optimal": sim.optimal}[algo]()
        hit_ratio, miss_ratio = sim.get_hit_miss_ratio()

        ratio_window = tk.Toplevel(self.root, bg=BG_COLOR)
        ratio_window.title(f"{algo} Hit/Miss Ratio")
        ratio_window.geometry("600x500")

        fig = plt.Figure(figsize=(5, 4), dpi=100, facecolor=BG_COLOR)
        ax = fig.add_subplot(111, facecolor="#FFFFFF")
        ax.pie([hit_ratio, miss_ratio], labels=['Hits', 'Misses'],
               colors=[ACCENT_COLOR, ERROR_COLOR], autopct='%1.1f%%',
               textprops={'color': TEXT_COLOR})
        ax.set_title(f"{algo} Hit/Miss Ratio", color=TEXT_COLOR)

        canvas = FigureCanvasTkAgg(fig, master=ratio_window)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        canvas.draw()

    def show_frame_states(self):
        if not self.simulation_details:
            messagebox.showinfo("Info", "No simulation data available",
                                 parent=self.root)
            return

        states_window = tk.Toplevel(self.root, bg=BG_COLOR)
        states_window.title(f"{self.simulation_details['algo']} Frame States")
        states_window.geometry("800x600")

        fig = plt.Figure(figsize=(8, 5), dpi=100, facecolor=BG_COLOR)
        ax = fig.add_subplot(111, facecolor="#FFFFFF")

        frame_states = self.simulation_details["frame_states"]
        steps = range(1, len(frame_states) + 1)
        frame_size = self.simulation_details["frame_size"]

        # Prepare data for stacked bar chart
        unique_pages = sorted(set(self.simulation_details["ref_string"]))
        colors = plt.colormaps.get_cmap('tab20')(np.linspace(0, 1, len(unique_pages)))  # Updated colormap access
        page_to_color = {page: colors[i % len(colors)] for i, page in enumerate(unique_pages)}

        bottom = np.zeros(len(steps))
        for i in range(frame_size):
            layer = [state[i] if i < len(state) else None for state in frame_states]
            values = [page if page is not None else 0 for page in layer]
            bars = ax.bar(steps, [1 if v != 0 else 0 for v in values], bottom=bottom,
                          color=[page_to_color.get(v, '#FFFFFF') for v in values],
                          edgecolor=BORDER_COLOR, width=0.8)
            for bar, value in zip(bars, values):
                if value != 0:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + bar.get_height()/2,
                            str(value), ha='center', va='center', color=TEXT_COLOR)
            bottom += [1 if v != 0 else 0 for v in values]

        ax.set_title(f"{self.simulation_details['algo']} Frame States", color=TEXT_COLOR)
        ax.set_xlabel("Step", color=TEXT_COLOR)
        ax.set_ylabel("Frame Position", color=TEXT_COLOR)
        ax.set_yticks(range(frame_size))
        ax.tick_params(axis='both', colors=TEXT_COLOR)

        canvas = FigureCanvasTkAgg(fig, master=states_window)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        canvas.draw()

    def save_results(self):
        if not self.simulation_details:
            messagebox.showinfo("Info", "No results to save", parent=self.root)
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Results",
            initialfile=f"simulation_{self.simulation_details['algo']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.simulation_details, f, indent=4)
            messagebox.showinfo("Success", "Results saved successfully",
                                 parent=self.root)

    def reset_fields(self):
        self.entry_ref.delete(0, tk.END)
        self.entry_frames.delete(0, tk.END)
        self.algo_var.set("FIFO")
        self.result_label.config(text="Page Faults: -", style='TLabel')
        self.simulation_details = None
        self.details_button.config(state="disabled")
        self.ratio_button.config(state="disabled")
        self.frames_button.config(state="disabled")
        self.save_button.config(state="disabled")

def main():
    root = tk.Tk()
    app = PageReplacementSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()