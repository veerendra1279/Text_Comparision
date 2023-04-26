import difflib
import tkinter as tk
from tkinter import filedialog

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def compare_files(file1_path, file2_path):
    file1_lines = read_file(file1_path)
    file2_lines = read_file(file2_path)

    d = difflib.Differ()
    diff = list(d.compare(file1_lines, file2_lines))

    return diff

def print_differences(diff):
    result = []
    for line in diff:
        if line.startswith('+'):
            result.append(("added", line))
        elif line.startswith('-'):
            result.append(("removed", line))
        else:
            result.append(("same", line))

    return result

def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def compare_button_click(file1_entry, file2_entry, output_text):
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()

    differences = compare_files(file1_path, file2_path)
    formatted_diff = print_differences(differences)

    output_text.delete(1.0, tk.END)
    for status, line in formatted_diff:
        if status == "added":
            output_text.insert(tk.END, line, "added")
        elif status == "removed":
            output_text.insert(tk.END, line, "removed")
        else:
            output_text.insert(tk.END, line)

def main():
    root = tk.Tk()
    root.title("Text Comparison Tool")

    file1_label = tk.Label(root, text="File 1:")
    file1_label.grid(row=0, column=0)

    file1_entry = tk.Entry(root, width=50)
    file1_entry.grid(row=0, column=1)

    file1_button = tk.Button(root, text="Browse", command=lambda: browse_file(file1_entry))
    file1_button.grid(row=0, column=2)

    file2_label = tk.Label(root, text="File 2:")
    file2_label.grid(row=1, column=0)

    file2_entry = tk.Entry(root, width=50)
    file2_entry.grid(row=1, column=1)

    file2_button = tk.Button(root, text="Browse", command=lambda: browse_file(file2_entry))
    file2_button.grid(row=1, column=2)

    compare_button = tk.Button(root, text="Compare", command=lambda: compare_button_click(file1_entry, file2_entry, output_text))
    compare_button.grid(row=2, column=1, pady=10)

    output_text = tk.Text(root, wrap=tk.WORD, bg="white", fg="black", width=80, height=20)
    output_text.grid(row=3, column=0, columnspan=3)

    output_text.tag_configure("added", foreground="green")
    output_text.tag_configure("removed", foreground="red")

    root.mainloop()

if __name__ == "__main__":
    main()