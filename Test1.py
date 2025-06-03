import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def scan_and_organize():
    root = tk.Tk()
    root.withdraw()

    folder_path = simpledialog.askstring("Folder Input", "Enter folder path to scan:")
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Invalid folder path!")
        return

    messagebox.showinfo("scanning", "Scanning\n...")
    
    file_data = []

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            drive, tail = os.path.splitdrive(full_path)
            relative_dir = os.path.relpath(dirpath, start=drive)
            file_type = detect_file_type(filename)

            file_data.append((drive.strip(":\\"), relative_dir, filename, file_type))

    if not file_data:
        messagebox.showinfo("Empty", "No files found in this folder.")
        return

    prompt_lines = ["| Drive | Directory | Filename | File Type |",
                    "|-------|-----------|----------|-----------|"]
    for drive, directory, name, ftype in file_data:
        prompt_lines.append(f"| {drive} | {directory} | {name} | {ftype} |")

    prompt = "Organize the following files into a table neatly and explain briefly if needed:\n" + "\n".join(prompt_lines)

    try:
        response = model.generate_content(prompt)
        output_text = response.text
    except Exception as e:
        messagebox.showerror("API Error", str(e))
        return

    output_path = os.path.join(os.path.dirname(folder_path), "organised.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    messagebox.showinfo("Success", f"Organized file saved as:\n{output_path}")

def detect_file_type(filename):
    ext = filename.split('.')[-1].lower()
    types = {
        'txt': 'Text',
        'doc': 'Document',
        'docx': 'Document',
        'jpg': 'Image',
        'jpeg': 'Image',
        'png': 'Image',
        'csv': 'CSV',
        'xlsx': 'Spreadsheet',
        'pdf': 'PDF',
        'py': 'Python Script',
        'exe': 'Executable',
        'mp3': 'Audio',
        'mp4': 'Video',
        'zip': 'Archive',
        'rar': 'Archive',
        'ico': 'Icon',
        'html': 'HTML Document',
        'cs': 'C# Source Code',
        'cpp': 'C++ Source Code',
        'js': 'JavaScript Source Code',
        'wav': 'Audio',
        'ogg': 'Audio',
        'bat': 'Batch Script',
        'json': 'JSON Data',
        'fbx': '3D Model',
        'csproj': 'C# Project',
        'dll': 'data for an executable',
        'avif': 'Image',
        'gif': 'Low quality video'
    }
    return types.get(ext, "Unknown")

if __name__ == "__main__":
    scan_and_organize()



