# NLM-Scrubber-encoder
Helper tool for encoding text files so that the files are NLM-scrubber ready. As of scrubber.19.0411W, only ASCII-encoded files can be taken, but plans are being put in place so that UTF-8 can also be taken as input for teh scrubber.

# Instructions:
1. Select a directory/folder with all files the user wants encoded. (has to be .txt or .HL7)
2. Choose an output directory where the user wants the encoded files to be located.
3. Choose the encoding type, be it ASCII or UTF-8
4. Choose the file extension, be it .txt, .HL7, or both.
5. Execute program and wait for popup of output folder.
6. Use this output folder as the input directory of the NLM-scrubber.

# Program Statistics:
1. A list of the 90 encodings that this program can handle is found here in the documentation: https://charset-normalizer.readthedocs.io/en/latest/user/support.html#supported-encoding.
2. From tests I have run, carriage returns and newlines are preserved for both new ASCII or UTF-8 encoded files.
3. The conversion speed of a single text file of approximate size 5.117 megabytes took ~497 milliseconds.
4. Additional python packages necessary for running of encoder is found in lines 1-7
5. Greek characters like α are converted into alpha, and Α(capital alpha), is converted into Alpha, so there is case sensitivity.
6. Words(elements of a list created via .split() of the whole file's text content) are run through unidecode if setting is ASCII encoding.
   - This means that words not able to be converted into ASCII form will be turned into the string "[UNRECOGNIZED_WORD]"
   - Languages that do not use spaces, for example Chinese, could potentially have problems with whole sentences being converted to the string "[UNRECOGNIZED_WORD]".
7. Text run to convert into UTF-8 will have all non-UTF-8 characters deleted.
8. There is a executable version of the python file for ease of access, understandably be wary as executable files can contain malicious code.
   - Preferably when possible, use encoder.py
