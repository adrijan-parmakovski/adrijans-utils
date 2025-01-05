import tkinter as tk
from tkinter import EXTENDED, Listbox, filedialog, messagebox

import PyPDF2


def select_pdfs(listbox):
    file_types = [("PDF Files", "*.pdf"), ("All Files", "*.*")]
    file_paths = filedialog.askopenfilenames(
        title="Select PDF files", filetypes=file_types
    )
    for path in file_paths:
        listbox.insert(tk.END, path)


def remove_selected_pdfs(listbox):
    selected_indices = listbox.curselection()
    for i in reversed(selected_indices):
        listbox.delete(i)


def merge_pdfs(listbox):
    paths = listbox.get(0, tk.END)
    if not paths:
        messagebox.showwarning(
            "No PDF files selected", "Please selected one or more files"
        )
        return None

    try:
        merger = PyPDF2.PdfMerger()
        for path in paths:
            merger.append(path)

        output_pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if not output_pdf_path:
            return

        merger.write(output_pdf_path)
        merger.close()
        messagebox.showinfo("Success", "The PDF files have been successfully merged")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured: {e}")


def gui():
    # set up the main window
    root = tk.Tk()
    root.title("Merge PDFs")
    root.geometry("800x600")

    # Listbox to display the files
    listbox = tk.Listbox(root, selectmode=EXTENDED)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # scrollbar
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # buttons to select
    select_button = tk.Button(
        root, text="Select PDF files", command=select_pdfs(listbox)
    )
    select_button.pack(fill=tk.X)
    # remove button
    remove_button = tk.Button(
        root, text="Remove selected PDF files", command=remove_selected_pdfs(listbox)
    )
    remove_button.pack(fill=tk.X)
    # merge button
    merge_button = tk.Button(root, text="Merge PDFs", command=merge_pdfs(listbox))
    merge_button.pack(fill=tk.X)

    root.mainloop()
