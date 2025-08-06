import pdfplumber
import os
from PyPDF2 import PdfWriter, PdfReader
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def pdf_splitter(pdfPath, outputFolder, ordnerName):

    if not (pdfPath):
        messagebox.showerror("Fehler", "Keine Datei ausgewählt")
        return

    if not outputFolder:
        outputFolder = os.path.join(os.path.dirname(pdfPath))

    if not ordnerName:
        ordnerName = "Lohnabrechnungen"

    outputFolder = os.path.join(outputFolder, ordnerName)
    os.makedirs(outputFolder, exist_ok=True)
    
    if os.path.exists(outputFolder):
        ordnerinhalt_loeschen(outputFolder)

    try:
        reader = PdfReader(pdfPath)

        with pdfplumber.open(pdfPath) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                textlines = text.splitlines()
                prefix = textlines[0].replace("Lohnabrechnung - ","Lohnabrechnung_").replace("/", "_")
                vorname = re.search(r"##DIALPERSVORNAME##\s*([^\s,\.]+)", text)
                nachname = re.search(r"##DIALPERSNACHNAME##\s*([^\s,\.]+)", text)
                fullname = prefix + "_" + vorname.group(1) + "_" + nachname.group(1)
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                output_path = os.path.join(outputFolder, f"{fullname}.pdf")

                with open(output_path, "wb") as f_out:
                    writer.write(f_out)

        messagebox.showinfo("Erledigt", f"Aufteilung abgeschlossen.\nDateien im Ordner:\n{outputFolder}")

    except Exception as e:
        messagebox.showerror("Fehler", str(e))
        
def ordnerinhalt_loeschen(ordner):
    for eintrag in os.listdir(ordner):
        pfad = os.path.join(ordner, eintrag)
        os.remove(pfad)

def datei_auswaehlen():
    filepath = filedialog.askopenfilename(title="PDF auswählen", filetypes=[("PDF Dateien", "*.pdf")])
    if filepath:
        eingabeFeld.delete(0, tk.END)
        eingabeFeld.insert(0, filepath)

def ordner_auswaehlen():
    folderpath = filedialog.askdirectory(title="Zielordner auswählen")
    if folderpath:
        eingabeOrdner.delete(0, tk.END)
        eingabeOrdner.insert(0, folderpath)

# GUI starten
fenster = tk.Tk()
fenster.title("MagicPDFEdit")
fenster.geometry("550x300")

#PDF Datei auswählen
tk.Label(fenster, text="PDF auswählen:").pack(pady=5)
eingabeFeld = tk.Entry(fenster, width=20)
eingabeFeld.pack()
tk.Button(fenster, text="Durchsuchen...", command=datei_auswaehlen).pack()

# Ordnername
# StringVar mit Standardwert
vorgabeText = tk.StringVar()
vorgabeText.set("Lohnabrechnungen")
tk.Label(fenster, text="Name des Unterordners eingeben:").pack(pady=4)
ordnerName = tk.Entry(fenster, textvariable=vorgabeText, width=20)
ordnerName.pack()

#Zielordner auswählen
tk.Label(fenster, text="Speicherort auswählen:").pack(pady=5)
eingabeOrdner = tk.Entry(fenster, width=20)
eingabeOrdner.pack()
tk.Button(fenster, text="Ordner auswählen...", command=ordner_auswaehlen).pack(pady=5)

# Button-Frame (horizontale Anordnung)
button_frame = tk.Frame(fenster)
button_frame.pack(pady=10)

# Ausführen-Button
tk.Button(button_frame, text="Ausführen", command=lambda: pdf_splitter(eingabeFeld.get(), eingabeOrdner.get(),ordnerName.get()), bg="lightblue").pack(side=tk.LEFT, padx=10)

# Beenden-Button
tk.Button(
    button_frame,
    text="Beenden",
    command=fenster.destroy,
    bg="lightgray"
).pack(side=tk.LEFT)

fenster.mainloop()