import os
import shutil
from tkinter import Tk, filedialog, messagebox, Button, Label, Text, Scrollbar, Frame, Entry, Canvas
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
from venn import venn  # For handling 4-set Venn diagrams
import pandas as pd
from itertools import combinations


class VennDiagramTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Venn-Master")
        self.root.geometry("1200x700")
        self.root.config(bg="#3d3d5c")

        # Create a sliding window with canvas and scrollbar
        self.canvas = Canvas(root, bg="#3d3d5c")
        self.scrollbar = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#3d3d5c")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.data_entries = []
        self.text_widgets = []
        self.label_entries = []
        self.file_paths = []

        # Title
        self.title_label = Label(
            self.scrollable_frame,
            text="Venn-Master",
            font=("Arial", 20, "bold"),
            bg="#3d3d5c",
            fg="white",
        )
        self.title_label.pack(pady=10)

        # Add Data and Generate Buttons
        self.add_data_button = Button(
            self.scrollable_frame,
            text="Add Data Entry",
            command=self.add_data_entry,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 12),
        )
        self.add_data_button.pack(pady=10)

        self.plot_button = Button(
            self.scrollable_frame,
            text="Generate Venn Diagram and Table",
            command=self.plot_venn_and_generate_table,
            bg="#FF5733",
            fg="white",
            font=("Helvetica", 14),
        )
        self.plot_button.pack(pady=10)

        self.download_button = Button(
            self.scrollable_frame,
            text="Download Results",
            command=self.download_results,
            bg="#007BFF",
            fg="white",
            font=("Helvetica", 12),
            state="disabled",
        )
        self.download_button.pack(pady=10)

        # Add the first data entry by default
        self.add_data_entry()

    def add_data_entry(self):
        entry_frame = Frame(self.scrollable_frame, bg="#f0f0f0")
        entry_frame.pack(pady=5, fill="x")

        browse_button = Button(
            entry_frame,
            text="Upload File",
            command=lambda: self.browse_file(len(self.text_widgets)),
            bg="#FFC300",
            fg="white",
            font=("Helvetica", 10),
        )
        browse_button.grid(row=0, column=0, padx=10, pady=5)

        data_label = Label(
            entry_frame,
            text=f"Data Entry {len(self.text_widgets) + 1}:",
            font=("Helvetica", 10, "bold"),
            bg="#f0f0f0",
        )
        data_label.grid(row=0, column=1, padx=10, pady=5)

        text_widget = Text(entry_frame, height=5, width=50, font=("Helvetica", 10))
        text_widget.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        label_label = Label(
            entry_frame,
            text="Custom Label:",
            font=("Helvetica", 10, "bold"),
            bg="#f0f0f0",
        )
        label_label.grid(row=0, column=2, padx=10)

        label_entry = Entry(entry_frame, font=("Helvetica", 10))
        label_entry.grid(row=1, column=2, padx=10, pady=5)

        clear_button = Button(
            entry_frame,
            text="Clear Data",
            command=lambda: self.clear_data(text_widget, label_entry),
            bg="#FF6347",
            fg="white",
            font=("Helvetica", 10),
        )
        clear_button.grid(row=0, column=3, padx=10, pady=5)

        self.text_widgets.append(text_widget)
        self.label_entries.append(label_entry)
        self.file_paths.append(None)

    def browse_file(self, index):
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
        )
        if file_path:
            self.file_paths[index] = file_path
            messagebox.showinfo(
                "File Uploaded", f"File successfully uploaded for Entry {index + 1}."
            )

    def clear_data(self, text_widget, label_entry):
        text_widget.delete("1.0", tk.END)
        label_entry.delete(0, tk.END)
        messagebox.showinfo("Clear Data", "Data cleared successfully!")

    def collect_data(self):
        sets = []
        filenames = []

        for i, text_widget in enumerate(self.text_widgets):
            if self.file_paths[i]:
                with open(self.file_paths[i], "r") as f:
                    data_set = {line.strip() for line in f if line.strip()}
            else:
                content = text_widget.get("1.0", tk.END).strip().splitlines()
                data_set = {line.strip() for line in content if line.strip()}

            if data_set:
                sets.append(data_set)
                label = self.label_entries[i].get().strip()
                filenames.append(label if label else f"Data {i + 1}")

        return sets, filenames

    def generate_table(self, sets, filenames):
        n = len(sets)
        table_data = []
        value_occurances = {}

        for i, filename in enumerate(filenames):
            unique_values = sets[i] - set.union(*(sets[j] for j in range(n) if j != i))
            for value in unique_values:
                value_occurances[value] = (f"Unique to {filename}", 1)

        for r in range(2, n + 1):
            for subset_indices in combinations(range(n), r):
                subset_sets = [sets[i] for i in subset_indices]
                subset_filenames = [filenames[i] for i in subset_indices]
                subset_common_values = set.intersection(*subset_sets)
                subset_label = " & ".join(subset_filenames)
                for value in subset_common_values:
                    if value in value_occurances:
                        if value_occurances[value][1] < r:
                            value_occurances[value] = (f"Common to {subset_label}", r)
                    else:
                        value_occurances[value] = (f"Common to {subset_label}", r)

        for value, (category, _) in value_occurances.items():
            table_data.append({"Category": category, "Value": value})

        df = pd.DataFrame(table_data)
        table_path = "unique_and_common_values_analysis_report.xlsx"
        df.to_excel(table_path, index=False)
        return table_path

    def plot_venn_and_generate_table(self):
        sets, filenames = self.collect_data()
        num_files = len(sets)

        if num_files < 2:
            messagebox.showerror(
                "Error", "Please provide at least 2 data entries to create a Venn diagram."
            )
            return

        if num_files > 4:
            messagebox.showwarning(
                "Venn Diagram Limited",
                "Venn diagram supports a maximum of 4 datasets. The table will be generated for all datasets.",
            )

        plt.figure(figsize=(10, 10))
        if num_files == 2:
            venn2(sets[:2], set_labels=filenames[:2])
        elif num_files == 3:
            venn3(sets[:3], set_labels=filenames[:3])
        elif num_files == 4:
            venn_data = {filenames[i]: sets[i] for i in range(4)}
            venn(venn_data)
        else:
            plt.close()

        plt.title("Venn Diagram", fontsize=18)
        venn_path = "venn_diagram.png"
        if num_files <= 4:
            plt.savefig(venn_path, format="png")
            plt.show()

        table_path = self.generate_table(sets, filenames)
        messagebox.showinfo(
            "Success",
            f"Venn Diagram saved as {venn_path} (if applicable).\nUnique and Common Values Table saved as {table_path}.",
        )

        self.download_button.config(state="normal")

    def download_results(self):
        save_dir = filedialog.askdirectory(title="Select Download Location")
        if save_dir:
            venn_file = "venn_diagram.png"
            if os.path.exists(venn_file):
                venn_dest = os.path.join(save_dir, venn_file)
                shutil.copy(venn_file, venn_dest)
                messagebox.showinfo("File Downloaded", f"Venn diagram saved to: {venn_dest}")
            else:
                messagebox.showwarning("Missing File", "Venn diagram file not found.")

            table_file = "unique_and_common_values_analysis_report.xlsx"
            if os.path.exists(table_file):
                table_dest = os.path.join(save_dir, table_file)
                shutil.copy(table_file, table_dest)
                messagebox.showinfo("File Downloaded", f"Analysis table saved to: {table_dest}")
            else:
                messagebox.showwarning("Missing File", "Analysis table file not found.")
        else:
            messagebox.showwarning("No Directory Selected", "Please select a directory to save the files.")


if __name__ == "__main__":
    root = Tk()
    app = VennDiagramTool(root)
    root.mainloop()
