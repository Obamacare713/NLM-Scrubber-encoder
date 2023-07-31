import os
from tkinter import filedialog
import tkinter as tk
from datetime import datetime
from charset_normalizer import detect
import time
from timeit import default_timer as timer

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

# Change encoding
def change_encoding(path, new_encoding, file_type, out_path):
    start = timer()
    input_folder = path.split("/")[-1]

    # Creates new folder names uniquely based on time, contains detail of encoding
    new_folder_name = input_folder + now.strftime("-%Y-%m-%d-time-%H-%M-%S") + f"-{new_encoding}_encoded"
    os.mkdir(f"{out_path}/{new_folder_name}")
    
    # Iterates through all files
    for file in os.listdir(path):

        # Chosen file extension is both .txt and .HL7
        if file_type == "Both .txt and .HL7":
            if (os.path.isfile(f"{path}/{file}") and file.endswith(".txt")) or (os.path.isfile(f"{path}/{file}") and file.endswith(".HL7")):

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

                # New file is created with chosen encoding, either ASCII or UTF-8
                with open(f"{out_path}/{new_folder_name}/{file}", 'w', encoding=new_encoding) as f:
                    f.write(content)

        # Chosen file extension is .txt
        elif file_type == ".txt":
            if (os.path.isfile(f"{path}/{file}") and file.endswith(".txt")):

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
                
                # New file is created with chosen encoding, either ASCII or UTF-8
                with open(f"{out_path}/{new_folder_name}/{file}", 'w', encoding=new_encoding) as f:
                    f.write(content)

        # Chosen file extension is .HL7
        elif file_type == ".HL7":
            if (os.path.isfile(f"{path}/{file}") and file.endswith(".HL7")):

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
                
                # New file is created with chosen encoding, either ASCII or UTF-8
                with open(f"{out_path}/{new_folder_name}/{file}", 'w', encoding=new_encoding) as f:
                    f.write(content)

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