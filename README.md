# NLM-Scrubber-encoder
Helper tool for encoding text files so that the files are NLM-scrubber ready. As of scrubber.19.0411W, only ASCII-encoded files can be taken, but plans are being put in place so that UTF-8 can also be taken as input.

# Instructions:
1. Select a directory/folder with all files the user wants encoded. (has to be .txt or .HL7)
2. Choose an output directory where the user wants the encoded files to be located.
3. Choose the encoding type, be it ASCII or UTF-8
4. Choose the file extension, be it .txt, .HL7, or both.
5. Execute program and wait for popup of output folder.
6. Profit!

# Program Statistics:
1. A list of the 90 encodings that this program can handle is found here in the documentation: https://charset-normalizer.readthedocs.io/en/latest/user/support.html#supported-encoding.
2. From tests I have run, carriage returns and newlines are preserved for both new ASCII or UTF-8 encoded files.
3. The conversion speed of a single text file of size 2730 kilobytes(2.7 megabytes) took 0.030041199999686796 seconds(0.03 seconds), according to a timer module I used.
4. Additional packages will need to be installed as not all packages used are in the standard Python library; all packages necessary for the program to run are found in lines 1-7.


