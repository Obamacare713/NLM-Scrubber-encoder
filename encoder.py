import os
from tkinter import filedialog
import tkinter as tk
from datetime import datetime
from charset_normalizer import detect
import time
from unidecode import unidecode

# Custom function for translating greek characters to their english pronounciations, with case-sensitivity.
def greek(text):
    greek_alphabet = {
        '\u0391': 'Alpha',
        '\u0392': 'Beta',
        '\u0393': 'Gamma',
        '\u0394': 'Delta',
        '\u0395': 'Epsilon',
        '\u0396': 'Zeta',
        '\u0397': 'Eta',
        '\u0398': 'Theta',
        '\u0399': 'Iota',
        '\u039A': 'Kappa',
        '\u039B': 'Lamda',
        '\u039C': 'Mu',
        '\u039D': 'Nu',
        '\u039E': 'Xi',
        '\u039F': 'Omicron',
        '\u03A0': 'Pi',
        '\u03A1': 'Rho',
        '\u03A3': 'Sigma',
        '\u03A4': 'Tau',
        '\u03A5': 'Upsilon',
        '\u03A6': 'Phi',
        '\u03A7': 'Chi',
        '\u03A8': 'Psi',
        '\u03A9': 'Omega',
        '\u03B1': 'alpha',
        '\u03B2': 'beta',
        '\u03B3': 'gamma',
        '\u03B4': 'delta',
        '\u03B5': 'epsilon',
        '\u03B6': 'zeta',
        '\u03B7': 'eta',
        '\u03B8': 'theta',
        '\u03B9': 'iota',
        '\u03BA': 'kappa',
        '\u03BB': 'lamda',
        '\u03BC': 'mu',
        '\u03BD': 'nu',
        '\u03BE': 'xi',
        '\u03BF': 'omicron',
        '\u03C0': 'pi',
        '\u03C1': 'rho',
        '\u03C3': 'sigma',
        '\u03C4': 'tau',
        '\u03C5': 'upsilon',
        '\u03C6': 'phi',
        '\u03C7': 'chi',
        '\u03C8': 'psi',
        '\u03C9': 'omega',
    }
    temp_keys = list(greek_alphabet.keys())

    # Converts all the greek characters in the text
    for i in range(len(greek_alphabet)):
        text = text.replace(temp_keys[i], greek_alphabet[temp_keys[i]])

    return text

# Tkinter window setup
root = tk.Tk()
root.title("NLM Scrubber Encoding Tool")
root.geometry("550x400")
root.minsize(width=550, height=400)
root.maxsize(width=550, height=400)

# Current time for unique folder name
now = datetime.now()

# Quick fix for binding the encoding section together in x direction movement
delta=100

# Label for instructions on choosing encoding
encode_label = tk.Label(root, 
        text="""Choose an encoding for\n outputted files to be in:""",
        justify = tk.LEFT,
        padx = 20)
encode_label.place(x=20+delta, y=200)

# Choose the encoding
radio_choice = tk.IntVar()
R1 = tk.Radiobutton(root, text="ASCII", variable=radio_choice, value=1).place(x=35+delta, y=240)
R2 = tk.Radiobutton(root, text="UTF-8", variable=radio_choice, value=2).place(x=35+delta, y=260)

#####################################################################################################################################################################
# Input text for directory
inputtxt = tk.Text(root,
                   height = 1,
                   width = 30, font=("Helvetica", 15))
inputtxt.place(x=20,y=20)

# Browse for Input Directory
input_text = tk.StringVar()
input_btn = tk.Button(root, textvariable=input_text, command=lambda:input_dir(), font="Raleway", bg="#20bebe", fg="black", height=1, width=15).place(x=370,y=15)
input_text.set("Input Directory")

# Output text for directory
outputtxt = tk.Text(root,
                   height = 1,
                   width = 30, font=("Helvetica", 15))
outputtxt.place(x=20,y=120)

# Browse for Output Directory
output_text = tk.StringVar()
output_btn = tk.Button(root, textvariable=output_text, command=lambda:output_dir(), font="Raleway", bg="#20bebe", fg="black", height=1, width=15).place(x=370,y=115)
output_text.set("Output Directory")

#####################################################################################################################################################################
def helper_encoding(path, file, out_path, new_folder_name, new_encoding):
    # Detects encoding of original file
    with open(f"{path}/{file}", 'rb') as f:
        result = detect(f.read())
        if result['encoding'] is None:
            tk.messagebox.showerror(title="Encoding Error!", message="File's encoding could not be detected. File possibly corrupted.\n Program closing in 5 seconds")
            time.sleep(5)
            root.destroy()

        old_encoding = result['encoding']

    # Opens original file via detected encoding from above, then reads all content
    with open(f"{path}/{file}", 'r', encoding=old_encoding) as f:
        content = f.read()

    # If the new encoding chosen is UTF-8, all non-UTF-8 characters are erased
    if new_encoding == "utf-8":
        with open(f"{out_path}/{new_folder_name}/{file}", 'w', encoding=new_encoding) as f:
            f.write((content.encode(new_encoding, 'ignore').decode(new_encoding, 'ignore')))
    
    # If the new encoding chosen is ASCII, unidecode() tries its best to convert words with non-ASCII into ASCII form, if it cannot "[UNRECOGNIZED_WORD]" is returned
    elif new_encoding == "ascii":
        with open(f"{out_path}/{new_folder_name}/{file}", 'w', encoding=new_encoding) as f:
            
            # Very crude way of differentiating what a "word" is, should work for most Western languages. Words separated by space assumed
            content = greek(content).split()
            for i in range(len(content)):
                try:
                    content[i] = unidecode(content[i], errors="strict")
                except:
                    content[i] = "[UNRECOGNIZED_WORD]"
            # Joins together all the words into one text again, and writes it to the new file
            f.write(" ".join(content))

# Change encoding
def change_encoding(path, new_encoding, file_type, out_path):
    input_folder = path.split("/")[-1]

    # Creates new folder names uniquely based on time, contains detail of encoding
    new_folder_name = input_folder + now.strftime("-%Y-%m-%d-time-%H-%M-%S") + f"-{new_encoding}_encoded"
    os.mkdir(f"{out_path}/{new_folder_name}")
    
    # Iterates through all files
    for file in os.listdir(path):

        # Chosen file extension is both .txt and .HL7
        if file_type == "Both .txt and .HL7":
            if (os.path.isfile(f"{path}/{file}") and file.endswith(".txt")) or (os.path.isfile(f"{path}/{file}") and file.endswith(".HL7")):
                helper_encoding(path, file, out_path, new_folder_name, new_encoding)
                    
        # Chosen file extension is .txt
        elif file_type == ".txt":
            if (os.path.isfile(f"{path}/{file}") and file.endswith(".txt")):
                helper_encoding(path, file, out_path, new_folder_name, new_encoding)

        # Chosen file extension is .HL7
        elif file_type == ".HL7":
            if (os.path.isfile(f"{path}/{file}") and file.endswith(".HL7")):
                helper_encoding(path, file, out_path, new_folder_name, new_encoding)

    return (out_path + '/' + new_folder_name)

# When clicking to browse for input_directory, chosen directory from folder-browser overwrites all text content originally within text_box
def input_dir():
    input_text.set("loading...")
    global folder
    folder = filedialog.askdirectory()
    if folder:
        input_text.set("Input Directory")
    else:
        input_text.set("Input Directory")
    inputtxt.delete("1.0", "end")
    inputtxt.insert("1.0", folder)


# When clicking to browse for output_directory, chosen directory from folder-browser overwrites all text content originally within text_box
def output_dir():
    output_text.set("loading...")
    global folder2
    folder2 = filedialog.askdirectory()
    if folder2:
        output_text.set("Output Directory")
    else:
        output_text.set("Output Directory")
    outputtxt.delete("1.0", "end")
    outputtxt.insert("1.0", folder2)

# Check for errors; if no error continue proper execution
def error_check(var_status):
    input_path = inputtxt.get("1.0","end").strip().replace(f"\n", "")
    output_path = outputtxt.get("1.0","end").strip().replace(f"\n", "")

    # Ensuring chosen paths are actually valid paths
    if not (os.path.exists(input_path)):
        tk.messagebox.showerror(title="Path Warning!", message="The input path you entered is not valid.")
    elif not (os.path.exists(output_path)):
        tk.messagebox.showerror(title="Path Warning!", message="The output path you entered is not valid.")
    
    # Making sure user chooses an encoding
    elif var_status == 0:
        tk.messagebox.showerror(title="Encoding Warning!", message="Please choose an encoding for output files to be encoded in.")

    # Making sure user chooses a file extension
    elif clicked.get() == "SELECT":
        tk.messagebox.showerror(title="File Extension Warning!", message="Please choose the file extension of the input files.")

    # Depending on chosen encoding, the change_encoding function will get varying inputs
    elif var_status == 1:
        ending_path = change_encoding(input_path, "ascii", clicked.get(), output_path)

        # Opens up resulting path
        os.startfile(ending_path)

    elif var_status == 2:

        ending_path = change_encoding(input_path, "utf-8", clicked.get(), output_path)

        # Opens up resulting path
        os.startfile(ending_path)

# Execute the program with all given parameters; this is mostly styling and placement of button
execute_text = tk.StringVar()
execute_btn = tk.Button(root, textvariable=execute_text, font="Raleway", bg="#22dd22", fg="black", height=2, width=20, command=lambda:error_check(radio_choice.get()))
execute_text.set("Create encoded files")
execute_btn.place(x=175,y=340)

# Options for the menu
extension_label = tk.Label(root, 
        text="""Choose file extension \nof the input files""",
        justify = tk.LEFT,
        padx = 20)
extension_label.place(x=350, y=200)

# Getting the chosen option
clicked = tk.StringVar()

# Options for file extensions
options = ["SELECT",".txt", ".HL7" , "Both .txt and .HL7"]

# Initial menu text
clicked.set("SELECT")
  
# Create Dropdown menu
drop = tk.OptionMenu( root , clicked , *options ).place(x=370,y=235)

# Run Tkinter window
root.mainloop()
