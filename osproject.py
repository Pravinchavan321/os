# class PageReplacement:
#     def __init__(self, frame_size, reference_string):
#         self.frame_size = frame_size
#         self.reference_string = reference_string
#         self.page_faults = 0

#     def fifo(self):
#         frame = []
#         page_faults = 0
#         for page in self.reference_string:
#             if page not in frame:
#                 if len(frame) < self.frame_size:
#                     frame.append(page)
#                 else:
#                     frame.pop(0)
#                     frame.append(page)
#                 page_faults += 1
#         return page_faults

#     def lru(self):
#         frame = []
#         page_faults = 0
#         for page in self.reference_string:
#             if page not in frame:
#                 if len(frame) < self.frame_size:
#                     frame.append(page)
#                 else:
#                     frame.pop(0)
#                     frame.append(page)
#                 page_faults += 1
#             else:
#                 frame.remove(page)
#                 frame.append(page) # Move to the most recently used
#         return page_faults

#     def optimal(self):
#         frame = []
#         page_faults = 0
#         for i, page in enumerate(self.reference_string):
#             if page not in frame:
#                 if len(frame) < self.frame_size:
#                     frame.append(page)
#                 else:
#                     future_use = {p: self.reference_string[i+1:].index(p) if p in self.reference_string[i+1:] else float('inf') for p in frame}
#                     victim = max(future_use, key=future_use.get)
#                     frame.remove(victim)
#                     frame.append(page)
#                 page_faults += 1
#         return page_faults

import tkinter as tk
from tkinter import messagebox
from algorithms import PageReplacement

def run_simulation():
    ref_string = entry_ref.get().split()
    try:
        ref_string = list(map(int, ref_string)) # Convert to integers
        frame_size = int(entry_frames.get())
        algo = algo_var.get()
        sim = PageReplacement(frame_size, ref_string)
        if algo == "FIFO":
            result = sim.fifo()
        elif algo == "LRU":
            result = sim.lru()
        elif algo == "Optimal":
            result = sim.optimal()
        else:
            messagebox.showerror("Error", "Invalid Algorithm")
            return
        messagebox.showinfo("Result", f"Page Faults using {algo}: {result}")
    except ValueError:
        messagebox.showerror("Error", "Invalid input for Reference String or Frame Size. Please enter space-separated integers.")

root = tk.Tk()
root.title("Page Replacement Simulator")

tk.Label(root, text="Reference String:").grid(row=0, column=0)
entry_ref = tk.Entry(root)
entry_ref.grid(row=0, column=1)

tk.Label(root, text="Frame Size:").grid(row=1, column=0)
entry_frames = tk.Entry(root)
entry_frames.grid(row=1, column=1)

tk.Label(root, text="Algorithm:").grid(row=2, column=0)
algo_var = tk.StringVar(value="FIFO")
tk.OptionMenu(root, algo_var, "FIFO", "LRU", "Optimal").grid(row=2, column=1)

tk.Button(root, text="Run", command=run_simulation).grid(row=3, column=0, columnspan=2)

root.mainloop()

import matplotlib.pyplot as plt
from algorithms import PageReplacement

def compare_algorithms(reference_string, frame_size):
    sim = PageReplacement(frame_size, reference_string)
    results = {
        "FIFO": sim.fifo(),
        "LRU": sim.lru(),
        "Optimal": sim.optimal()
    }
    plt.bar(results.keys(), results.values(), color=['blue', 'green', 'red'])
    plt.xlabel("Algorithm")
    plt.ylabel("Page Faults")
    plt.title("Page Replacement Algorithm Comparison")
    plt.show()

if __name__ == "__main__":
    reference_string = [7, 0, 1, 2, 0, 3, 4, 2, 3, 0, 3, 2]
    frame_size = 3
    compare_algorithms(reference_string, frame_size)