# import tkinter as tk
# from tkinter import messagebox
# from tkinter import ttk
# from algorithms import PageReplacement
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # --- Professional Color Palette (Subtle Blue/Gray) ---
# BG_COLOR = "#E0E8F0"  # Light blue-gray background
# TEXT_COLOR = "#333333"  # Dark gray text
# PRIMARY_COLOR = "#6495ED"  # Cornflower blue (for primary actions)
# SECONDARY_COLOR = "#A9A9A9"  # Dark gray (for accents, borders)
# ACCENT_COLOR = "#3CB371"  # Medium sea green (for positive feedback)
# ERROR_COLOR = "#FF6347"  # Tomato (for errors)

# def run_simulation():
#     ref_string = entry_ref.get().split()
#     try:
#         ref_string = list(map(int, ref_string))
#         frame_size = int(entry_frames.get())
#         algo = algo_var.get()
#         sim = PageReplacement(frame_size, ref_string)
#         if algo == "FIFO":
#             result = sim.fifo()
#         elif algo == "LRU":
#             result = sim.lru()
#         elif algo == "Optimal":
#             result = sim.optimal()
#         else:
#             messagebox.showerror("Error", "Invalid Algorithm", parent=root)
#             return
#         style.configure('Success.TLabel', foreground=ACCENT_COLOR)
#         result_label.config(text=f"Page Faults using {algo}: {result}", style='Success.TLabel')
#     except ValueError:
#         messagebox.showerror("Error", "Invalid input for Reference String or Frame Size. Please enter space-separated integers.", parent=root)

# def show_comparison():
#     reference_string = [int(x) for x in entry_ref.get().split()]
#     try:
#         frame_size = int(entry_frames.get())
#         sim = PageReplacement(frame_size, reference_string)
#         results = {
#             "FIFO": sim.fifo(),
#             "LRU": sim.lru(),
#             "Optimal": sim.optimal()
#         }

#         plot_window = tk.Toplevel(root, bg=BG_COLOR)
#         plot_window.title("Algorithm Comparison")

#         figure = plt.Figure(figsize=(6, 4), dpi=100, facecolor=BG_COLOR)
#         subplot = figure.add_subplot(111, facecolor=BG_COLOR)
#         bars = subplot.bar(results.keys(), results.values(), color=[PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR])
#         subplot.set_xlabel("Algorithm", color=TEXT_COLOR)
#         subplot.set_ylabel("Page Faults", color=TEXT_COLOR)
#         subplot.set_title("Page Replacement Algorithm Comparison", color=TEXT_COLOR)
#         subplot.tick_params(axis='x', colors=TEXT_COLOR)
#         subplot.tick_params(axis='y', colors=TEXT_COLOR)
#         subplot.spines['bottom'].set_color(SECONDARY_COLOR)
#         subplot.spines['top'].set_color(SECONDARY_COLOR)
#         subplot.spines['left'].set_color(SECONDARY_COLOR)
#         subplot.spines['right'].set_color(SECONDARY_COLOR)

#         canvas = FigureCanvasTkAgg(figure, master=plot_window)
#         canvas_widget = canvas.get_tk_widget()
#         canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
#         canvas.draw()

#     except ValueError:
#         messagebox.showerror("Error", "Invalid input for Reference String or Frame Size.", parent=root)

# root = tk.Tk()
# root.title("Page Replacement Simulator")
# root.config(bg=BG_COLOR)

# style = ttk.Style(root)
# style.theme_use('clam')

# # Configure global style for labels
# style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, font=('Arial', 11))

# # Configure style for entry fields
# style.configure('TEntry', background="white", foreground=TEXT_COLOR, insertcolor=TEXT_COLOR, font=('Arial', 11))

# # Configure style for buttons
# style.configure('TButton', background=PRIMARY_COLOR, foreground="white", font=('Arial', 11, 'bold'), padding=10, relief='raised', borderwidth=1)
# style.map('TButton',
#     background=[('active', '#4169E1')],  # Slightly darker blue on hover
#     foreground=[('active', 'white')]
# )

# # Configure style for OptionMenu
# style.configure('TMenubutton', background="white", foreground=TEXT_COLOR, font=('Arial', 11), padding=8, relief='raised', borderwidth=1)
# style.map('TMenubutton',
#     background=[('active', '#D3D3D3')],  # Light gray on hover
#     foreground=[('active', TEXT_COLOR)]
# )

# # --- Vertical Layout ---
# label_ref = ttk.Label(root, text="Reference String:")
# label_ref.pack(padx=10, pady=5, anchor="w")
# entry_ref = ttk.Entry(root, width=40)
# entry_ref.pack(padx=10, pady=5, fill="x")

# label_frames = ttk.Label(root, text="Frame Size:")
# label_frames.pack(padx=10, pady=5, anchor="w")
# entry_frames = ttk.Entry(root, width=10)
# entry_frames.pack(padx=10, pady=5, fill="x")

# label_algo = ttk.Label(root, text="Algorithm:")
# label_algo.pack(padx=10, pady=5, anchor="w")
# algo_var = tk.StringVar(value="FIFO")
# algo_menu = ttk.OptionMenu(root, algo_var, "FIFO", "FIFO", "LRU", "Optimal", style='TMenubutton')
# algo_menu.pack(padx=10, pady=5, fill="x")

# run_button = ttk.Button(root, text="Run Simulation", command=run_simulation, style='TButton')
# run_button.pack(padx=10, pady=15, fill="x")

# result_label = ttk.Label(root, text="Page Faults: ")
# result_label.pack(padx=10, pady=10, anchor="center")

# compare_button = ttk.Button(root, text="Show Comparison Plot", command=show_comparison, style='TButton')
# compare_button.pack(padx=10, pady=15, fill="x")

# root.mainloop()

# if __name__ == "__main__":
#     pass

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from algorithms import PageReplacement  # Assuming this is a separate module
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.font as tkfont

# --- Professional Color Palette ---
BG_COLOR = "#E0E8F0"  
TEXT_COLOR = "#333333"  
PRIMARY_COLOR = "#6495ED"  
SECONDARY_COLOR = "#A9A9A9"  
ACCENT_COLOR = "#3CB371"  
ERROR_COLOR = "#FF6347"  

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
        y += self.widget.winfo_rooty() + 25
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

class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Simulator")
        self.root.config(bg=BG_COLOR)
        self.root.geometry("400x550")
        
        self.setup_styles()
        self.create_widgets()
        self.root.resizable(False, False)

    def setup_styles(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, 
                           font=('Arial', 11))
        self.style.configure('TEntry', fieldbackground="white", foreground=TEXT_COLOR, 
                           font=('Arial', 11))
        self.style.configure('TButton', background=PRIMARY_COLOR, foreground="white", 
                           font=('Arial', 11, 'bold'), padding=10)
        self.style.map('TButton', background=[('active', '#4169E1')])
        self.style.configure('TMenubutton', background="white", foreground=TEXT_COLOR, 
                           font=('Arial', 11), padding=8)
        self.style.configure('Success.TLabel', foreground=ACCENT_COLOR, 
                           font=('Arial', 11, 'bold'))
        self.style.configure('Title.TLabel', font=('Arial', 14, 'bold'))

    def create_widgets(self):
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10)
        ttk.Label(title_frame, text="Page Replacement Simulator", 
                 style='Title.TLabel').pack()

        # Input Frame
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill="x", padx=10)

        # Reference String
        ttk.Label(input_frame, text="Reference String:").grid(row=0, column=0, 
                                                             sticky="w", pady=5)
        self.entry_ref = ttk.Entry(input_frame, width=30)
        self.entry_ref.grid(row=0, column=1, pady=5, sticky="ew")
        ToolTip(self.entry_ref, "Enter space-separated page numbers (e.g., 1 2 3 4)")

        # Frame Size
        ttk.Label(input_frame, text="Frame Size:").grid(row=1, column=0, 
                                                       sticky="w", pady=5)
        self.entry_frames = ttk.Entry(input_frame, width=10)
        self.entry_frames.grid(row=1, column=1, pady=5, sticky="w")
        ToolTip(self.entry_frames, "Enter number of frames (e.g., 3)")

        # Algorithm Selection
        ttk.Label(input_frame, text="Algorithm:").grid(row=2, column=0, 
                                                      sticky="w", pady=5)
        self.algo_var = tk.StringVar(value="FIFO")
        algo_menu = ttk.OptionMenu(input_frame, self.algo_var, "FIFO", "FIFO", 
                                 "LRU", "Optimal")
        algo_menu.grid(row=2, column=1, pady=5, sticky="w")

        # Buttons Frame
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill="x", padx=10)

        self.run_button = ttk.Button(button_frame, text="Run Simulation", 
                                   command=self.run_simulation)
        self.run_button.pack(fill="x", pady=5)

        self.compare_button = ttk.Button(button_frame, text="Show Comparison", 
                                       command=self.show_comparison)
        self.compare_button.pack(fill="x", pady=5)

        self.reset_button = ttk.Button(button_frame, text="Reset", 
                                     command=self.reset_fields)
        self.reset_button.pack(fill="x", pady=5)

        # Results Frame
        result_frame = ttk.Frame(self.root, padding=10)
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
        except ValueError as e:
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
            result = {"FIFO": sim.fifo, "LRU": sim.lru, "Optimal": sim.optimal}[algo]()
            self.result_label.config(text=f"Page Faults using {algo}: {result}", 
                                   style='Success.TLabel')
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}", 
                               parent=self.root)

    def show_comparison(self):
        ref_string, frame_size = self.validate_inputs()
        if ref_string is None:
            return

        sim = PageReplacement(frame_size, ref_string)
        results = {
            "FIFO": sim.fifo(),
            "LRU": sim.lru(),
            "Optimal": sim.optimal()
        }

        plot_window = tk.Toplevel(self.root, bg=BG_COLOR)
        plot_window.title("Algorithm Comparison")
        plot_window.geometry("600x450")

        figure = plt.Figure(figsize=(6, 4), dpi=100, facecolor=BG_COLOR)
        subplot = figure.add_subplot(111, facecolor=BG_COLOR)
        bars = subplot.bar(results.keys(), results.values(), 
                         color=[PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR])
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            subplot.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom',
                        color=TEXT_COLOR)

        subplot.set_xlabel("Algorithm", color=TEXT_COLOR)
        subplot.set_ylabel("Page Faults", color=TEXT_COLOR)
        subplot.set_title("Algorithm Comparison", color=TEXT_COLOR)
        subplot.tick_params(axis='both', colors=TEXT_COLOR)
        for spine in subplot.spines.values():
            spine.set_color(SECONDARY_COLOR)

        canvas = FigureCanvasTkAgg(figure, master=plot_window)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        canvas.draw()

    def reset_fields(self):
        self.entry_ref.delete(0, tk.END)
        self.entry_frames.delete(0, tk.END)
        self.algo_var.set("FIFO")
        self.result_label.config(text="Page Faults: -", style='TLabel')

def main():
    root = tk.Tk()
    app = PageReplacementSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()