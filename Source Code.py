

TANGINAMO LAZHAR!!!!!!!!!!!!!!!!











import sys
import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def generate_reference_string(length):
    return [random.randint(0, 9) for _ in range(length)]

def fifo(reference_string, num_frames):
    memory = []
    page_faults = 0
    steps = []
    order = []  # Tracks the order of insertion for FIFO

    for page in reference_string:
        if page not in memory:
            page_faults += 1
            if len(memory) < num_frames:
                memory.append(page)
                order.append(page)
            else:
                # Remove the oldest page (first in order)
                oldest = order.pop(0)
                memory.remove(oldest)
                memory.append(page)
                order.append(page)
            steps.append({"page": page, "memory": list(memory), "fault": True})
        else:
            steps.append({"page": page, "memory": list(memory), "fault": False})
    return page_faults, steps

def lru(reference_string, num_frames):
    memory = []
    page_faults = 0
    steps = []
    usage_order = []  # Tracks recent usage

    for page in reference_string:
        if page in memory:
            # Move to most recent
            usage_order.remove(page)
            usage_order.append(page)
            steps.append({"page": page, "memory": list(memory), "fault": False})
        else:
            page_faults += 1
            if len(memory) < num_frames:
                memory.append(page)
                usage_order.append(page)
            else:
                # Remove least recently used (first in usage_order)
                lru_page = usage_order.pop(0)
                memory.remove(lru_page)
                memory.append(page)
                usage_order.append(page)
            steps.append({"page": page, "memory": list(memory), "fault": True})
    return page_faults, steps

def opt(reference_string, num_frames):
    memory = []
    page_faults = 0
    steps = []

    for i in range(len(reference_string)):
        page = reference_string[i]
        if page not in memory:
            page_faults += 1
            if len(memory) < num_frames:
                memory.append(page)
            else:
                # Find page with farthest next use
                farthest = -1
                replace_page = None
                for p in memory:
                    try:
                        next_use = reference_string.index(p, i + 1)
                    except ValueError:
                        next_use = float('inf')
                    if next_use > farthest:
                        farthest = next_use
                        replace_page = p
                memory.remove(replace_page)
                memory.append(page)
            steps.append({"page": page, "memory": list(memory), "fault": True})
        else:
            steps.append({"page": page, "memory": list(memory), "fault": False})
    return page_faults, steps

class PageReplacementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Algorithms")
        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="Parameters")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Number of Frames:").grid(row=0, column=0, padx=5, pady=5)
        self.num_frames_entry = ttk.Entry(input_frame)
        self.num_frames_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Reference Length:").grid(row=1, column=0, padx=5, pady=5)
        self.ref_length_entry = ttk.Entry(input_frame)
        self.ref_length_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Reference String (optional):").grid(row=2, column=0, padx=5, pady=5)
        self.ref_string_entry = ttk.Entry(input_frame, width=40)
        self.ref_string_entry.grid(row=2, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Generate Reference String", command=self.generate_ref_string).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Run Algorithms", command=self.run_algorithms).grid(row=0, column=1, padx=5)

        self.results_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=25)
        self.results_area.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def generate_ref_string(self):
        try:
            length = int(self.ref_length_entry.get())
            ref_string = generate_reference_string(length)
            self.ref_string_entry.delete(0, tk.END)
            self.ref_string_entry.insert(0, ' '.join(map(str, ref_string)))
        except ValueError:
            messagebox.showerror("Error", "Invalid reference length!")

    def run_algorithms(self):
        try:
            num_frames = int(self.num_frames_entry.get())
            ref_str_input = self.ref_string_entry.get().strip()

            if ref_str_input:
                reference_string = list(map(int, ref_str_input.split()))
            else:
                length = int(self.ref_length_entry.get())
                reference_string = generate_reference_string(length)
                self.ref_string_entry.delete(0, tk.END)
                self.ref_string_entry.insert(0, ' '.join(map(str, reference_string)))

            self.results_area.delete(1.0, tk.END)
            self.results_area.insert(tk.END, f"Reference String: {' '.join(map(str, reference_string))}\n")
            self.results_area.insert(tk.END, f"Number of Frames: {num_frames}\n\n")

            # Run FIFO
            fifo_faults, fifo_steps = fifo(reference_string, num_frames)
            self.results_area.insert(tk.END, "\nFIFO Algorithm:\n")
            for step in fifo_steps:
                self.results_area.insert(tk.END, 
                    f"Page {step['page']}: Memory {step['memory']} | Fault: {'Yes' if step['fault'] else 'No'}\n")

            # Run LRU
            lru_faults, lru_steps = lru(reference_string, num_frames)
            self.results_area.insert(tk.END, "\nLRU Algorithm:\n")
            for step in lru_steps:
                self.results_area.insert(tk.END, 
                    f"Page {step['page']}: Memory {step['memory']} | Fault: {'Yes' if step['fault'] else 'No'}\n")

            # Run OPT
            opt_faults, opt_steps = opt(reference_string, num_frames)
            self.results_area.insert(tk.END, "\nOPT Algorithm:\n")
            for step in opt_steps:
                self.results_area.insert(tk.END, 
                    f"Page {step['page']}: Memory {step['memory']} | Fault: {'Yes' if step['fault'] else 'No'}\n")

            # Show total faults
            self.results_area.insert(tk.END, f"\nTotal FIFO Faults: {fifo_faults}\n")
            self.results_area.insert(tk.END, f"Total LRU Faults: {lru_faults}\n")
            self.results_area.insert(tk.END, f"Total OPT Faults: {opt_faults}\n")

        except ValueError:
            messagebox.showerror("Error", "Invalid input! Ensure all fields are correctly filled.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementApp(root)
    root.mainloop()
