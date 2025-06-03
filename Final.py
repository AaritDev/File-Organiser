import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import google.generativeai as genai
import ttkbootstrap as tb
from openpyxl import Workbook
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def scan_and_organize():
    folder_path = filedialog.askdirectory(title="Select Folder to Scan")
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Invalid folder path!")
        return

    progress_label.config(text="Scanning...")
    root.update_idletasks()

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

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "File Scan Results"

    headers = ["Drive", "Directory", "Filename", "File Type"]
    sheet.append(headers)

    for row in file_data:
        sheet.append(row)

    output_dir = os.path.dirname(folder_path)
    excel_path = os.path.join(output_dir, "scan_results.xlsx")
    workbook.save(excel_path)

    prompt_lines = ["| Drive | Directory | Filename | File Type |",
                    "|-------|-----------|----------|-----------|"]
    for drive, directory, name, ftype in file_data:
        prompt_lines.append(f"| {drive} | {directory} | {name} | {ftype} |")

    prompt = "Organize the following files into a table neatly and explain briefly if needed:\n" + "\n".join(prompt_lines)

    try:
        progress_label.config(text="Talking to Gemini...")
        root.update_idletasks()
        response = model.generate_content(prompt)
        output_text = response.text
    except Exception as e:
        messagebox.showerror("API Error", str(e))
        return

    show_output_window(output_text)

    progress_label.config(text=f"Done! Excel saved at:\n{excel_path}")


def show_output_window(output_text):
    output_win = tb.Toplevel(title="Organized Output")
    output_win.geometry("800x500")

    text_area = tk.Text(output_win, wrap=tk.WORD, font=("Consolas", 11))
    scrollbar = ttk.Scrollbar(output_win, command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)

    text_area.insert(tk.END, output_text)
    text_area.configure(state="disabled")

    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def detect_file_type(filename):
    ext = filename.split('.')[-1].lower()
    types = {
        'txt': 'Text File',
        'rtf': 'Rich Text Format',
        'md': 'Markdown Document',
        'doc': 'Microsoft Word Document',
        'docx': 'Microsoft Word Document',
        'odt': 'OpenDocument Text',
        'xls': 'Excel Spreadsheet',
        'xlsx': 'Excel Spreadsheet',
        'ods': 'OpenDocument Spreadsheet',
        'csv': 'Comma-Separated Values',
        'ppt': 'PowerPoint Presentation',
        'pptx': 'PowerPoint Presentation',
        'odp': 'OpenDocument Presentation',
        'pdf': 'PDF Document',
        'epub': 'eBook (EPUB)',
        'mobi': 'eBook (MOBI)',
        'tex': 'LaTeX Document',
        'py': 'Python Script',
        'java': 'Java Source Code',
        'c': 'C Source Code',
        'cpp': 'C++ Source Code',
        'h': 'C/C++ Header',
        'cs': 'C# Source Code',
        'vb': 'Visual Basic File',
        'js': 'JavaScript Source Code',
        'ts': 'TypeScript Source Code',
        'php': 'PHP Script',
        'html': 'HTML Document',
        'htm': 'HTML Document',
        'css': 'Cascading Style Sheet',
        'go': 'Go Source Code',
        'rb': 'Ruby Script',
        'swift': 'Swift Source Code',
        'rs': 'Rust Source Code',
        'kt': 'Kotlin Source Code',
        'sh': 'Shell Script',
        'bat': 'Batch Script',
        'pl': 'Perl Script',
        'lua': 'Lua Script',
        'r': 'R Script',
        'csproj': 'C# Project',
        'sln': 'Visual Studio Solution',
        'vcxproj': 'Visual C++ Project',
        'makefile': 'Makefile',
        'cmake': 'CMake Script',
        'gradle': 'Gradle Build Script',
        'xcodeproj': 'Xcode Project',
        'json': 'JSON Data',
        'xml': 'XML Data',
        'yaml': 'YAML Data',
        'yml': 'YAML Data',
        'ini': 'Configuration File',
        'toml': 'TOML Config File',
        'env': 'Environment Config File',
        'db': 'Database File',
        'sqlite': 'SQLite Database',
        'log': 'Log File',
        'mp3': 'MP3 Audio',
        'wav': 'WAV Audio',
        'ogg': 'OGG Audio',
        'flac': 'FLAC Audio',
        'm4a': 'M4A Audio',
        'aac': 'AAC Audio',
        'mp4': 'MP4 Video',
        'mkv': 'Matroska Video',
        'avi': 'AVI Video',
        'mov': 'QuickTime Video',
        'wmv': 'Windows Media Video',
        'webm': 'WebM Video',
        'jpg': 'JPEG Image',
        'jpeg': 'JPEG Image',
        'png': 'PNG Image',
        'bmp': 'Bitmap Image',
        'gif': 'GIF Image',
        'webp': 'WebP Image',
        'ico': 'Icon File',
        'tiff': 'TIFF Image',
        'svg': 'Scalable Vector Graphic',
        'fbx': '3D Model (FBX)',
        'obj': '3D Model (OBJ)',
        'stl': '3D Model (STL)',
        'blend': 'Blender Project',
        'dae': 'Collada 3D Model',
        'skp': 'SketchUp Model',
        'dwg': 'AutoCAD Drawing',
        'dxf': 'Drawing Exchange Format',
        'zip': 'ZIP Archive',
        'rar': 'RAR Archive',
        '7z': '7-Zip Archive',
        'tar': 'TAR Archive',
        'gz': 'Gzip Compressed',
        'bz2': 'Bzip2 Compressed',
        'xz': 'XZ Compressed',
        'iso': 'ISO Disk Image',
        'exe': 'Windows Executable',
        'msi': 'Windows Installer',
        'apk': 'Android Package',
        'app': 'MacOS App Bundle',
        'bin': 'Binary File',
        'dll': 'Dynamic Link Library',
        'so': 'Shared Object Library (Linux)',
        'deb': 'Debian Package',
        'rpm': 'Red Hat Package',
        'vdi': 'VirtualBox Disk Image',
        'vmdk': 'VMware Disk Image',
        'ova': 'Open Virtual Appliance',
        'ovf': 'Open Virtual Format',
        'qcow2': 'QEMU Disk Image',
        'img': 'Disk Image',
        'dockerfile': 'Docker Build File',
        'ttf': 'TrueType Font',
        'otf': 'OpenType Font',
        'woff': 'Web Open Font Format',
        'woff2': 'Web Open Font Format 2',
        'psd': 'Photoshop Document',
        'ai': 'Adobe Illustrator',
        'xd': 'Adobe XD Design File',
        'sketch': 'Sketch Design File',
        'torrent': 'Torrent File',
        'pem': 'PEM Certificate',
        'crt': 'Certificate File',
        'key': 'Key File',
        'cfg': 'Configuration File',
    }
    return types.get(ext, "Unknown")

root = tb.Window(themename="darkly") 
root.title("Gemini File Organizer")
root.geometry("500x300")

title = tb.Label(root, text="Gemini File Organizer", font=("Helvetica", 20, "bold"))
title.pack(pady=20)

desc = tb.Label(root, text="Select a folder to scan and organize with Gemini AI.", font=("Helvetica", 12))
desc.pack(pady=5)

start_button = tb.Button(root, text="Choose Folder & Start", bootstyle="primary", command=scan_and_organize)
start_button.pack(pady=20)

progress_label = tb.Label(root, text="", font=("Helvetica", 10, "italic"))
progress_label.pack(pady=10)

root.mainloop()
