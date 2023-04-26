import difflib
import tkinter as tk
from tkinter import ttk, filedialog

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def compare_files(file1_path, file2_path, mode):
    file1_lines = read_file(file1_path)
    file2_lines = read_file(file2_path)

    if mode == "Unified":
        diff = list(difflib.unified_diff(file1_lines, file2_lines, lineterm=''))
    elif mode == "Context":
        diff = list(difflib.context_diff(file1_lines, file2_lines, lineterm=''))
    else:
        d = difflib.Differ()
        diff = list(d.compare(file1_lines, file2_lines))

    return diff

def browse_file(entry, status_bar):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    status_bar.config(text=f"Selected file: {file_path}")

def save_comparison_result(output_text, status_bar):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as file:
            file.write(output_text.get(1.0, tk.END))
        status_bar.config(text=f"Comparison result saved to: {file_path}")

def compare_button_click(file1_entry, file2_entry, output_text, status_bar, mode_var):
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()
    mode = mode_var.get()

    differences = compare_files(file1_path, file2_path, mode)

    output_text.delete(1.0, tk.END)
    for line in differences:
        if line.startswith('+'):
            output_text.insert(tk.END, line + '\n', "added")
        elif line.startswith('-'):
            output_text.insert(tk.END, line + '\n', "removed")
        else:
            output_text.insert(tk.END, line + '\n')

    status_bar.config(text="Comparison complete")

def main():
    root = tk.Tk()
    root.title("Text Comparison Tool")

    file1_label = tk.Label(root, text="File 1:")
    file1_label.grid(row=0, column=0)

    file1_entry = tk.Entry(root, width=50)
    file1_entry.grid(row=0, column=1)

    file1_button = tk.Button(root, text="Browse", command=lambda: browse_file(file1_entry, status_bar))
    file1_button.grid(row=0, column=2)

    file2_label = tk.Label(root, text="File 2:")
    file2_label.grid(row=1, column=0)

    file2_entry = tk.Entry(root, width=50)
    file2_entry.grid(row=1, column=1)

    file2_button = tk.Button(root, text="Browse", command=lambda: browse_file(file2_entry, status_bar))
    file2_button.grid(row=1, column=2)

    mode_label = tk.Label(root, text="Comparison mode:")
    mode_label.grid(row=2, column=0)

    mode_var = tk.StringVar()
    mode_var.set("Unified")

    mode_combobox = ttk.Combobox(root, textvariable=mode_var, values=["Unified", "Context"], state="readonly", width=47)
    mode_combobox.grid(row=2, column=1)
    compare_button = tk.Button(root, text="Compare", command=lambda: compare_button_click(file1_entry, file2_entry, output_text, status_bar, mode_var))
    compare_button.grid(row=3, column=1, pady=10)

    output_text = tk.Text(root, wrap=tk.WORD, bg="white", fg="black", width=80, height=20)
    output_text.grid(row=4, column=0, columnspan=3)

    output_text.tag_configure("added", foreground="green")
    output_text.tag_configure("removed", foreground="red")

    save_button = tk.Button(root, text="Save", command=lambda: save_comparison_result(output_text, status_bar))
    save_button.grid(row=5, column=1, pady=10)

    status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.grid(row=6, column=0, columnspan=3, sticky=tk.W+tk.E)

    root.mainloop()

if __name__ == "__main__":
    main()