# inv-differ

Programmatically determines what products need to be re-ordered, based on two CSV files that contain the current invetory and the desired re-order points for each product.

# Requirements

This software was developed on a 64-bit Windows 10 computer with at least 2GB of RAM. The Application.exe file will likely run on both slighter newer and slightly older computers, but this is not guaranteed.

Python 3.7 or newer is required to run the source code located in 'src/Application.py'. No python instance is required to run the Application.exe file, which has been compiled and therefore should be self-contained and self-sufficient.

# Quick Start

Note: unlike in the previous version, the files can be named whatever you want.

1. Double click on the file 'Application.exe'
  - The application window will have several rows of entry fields. Each row corresponds to the inventory of a specific van. You can select multiple pairs of inventory and requirements files, and the application will process them all in sequence
2. Click the left open file icon, and choose an inventory file
3. Click the right open file icon, and choose a requirements file
4. Set the 'van' field to a unique van number. This number will be used to name the resulting output file
5. Click the button labeled "Go"
4. A window will appear, informing you if the process was successful or if there was an error.
  - If successful, results will be saved to a file named 'reorder_vanXXX.csv', which will be placed in the 'data' folder (the XXX will be replaced with the van number)
  - If a failure, then no results will be saved, and a message will be placed in the window informing you of the error

# Algorithm Description

The algorithm that is followed can be described as so:
1. Load the inv.csv and req.csv files
2. Extract the names and current quantities from the inv.csv file
3. Extract the names and required quantities from the req.csv file
4. Remove all spaces from the inventory and re-order requirement names
5. Check to see if every product name extracted from req.csv is present in the list of names extracted from inv.csv
  - If a name is present in req.csv but not in inv.csv, then an entry is created in the inventory list for that name and its current quantity is set to 0. Proceed to step 6
  - If a name is present in both req.csv and inv.csv, then proceed to step 6 without issue
  - If a name is present in inv.csv but not in req.csv, then it is ignored. Proceed to step 6
6. Compare the required quantity of every name extracted from req.csv against the current quantity in the inventory list that was extracted from inv.csv (or for missing products, the quantity of 0 created in step 5)
  - If the current quantity is less than the required quantity, then add the name of the product to the reorder.csv file, as well as the quantity needed. The quantity needed is defined as the required quantity minus the current quantity
  - If the current quantity is greater than or equal to the required quantity, then this product name is ignored
7. The names and required quantities of each product that needs to be re-ordered will be saved in the file 'reorder.csv'

# File Structures

The CSV files that are processed in this application must follow a very specific structure for the algorithm to work correctly. The required structure for each file type is described in the following sub-sections.

The CSV formatting that this application follows is:
- Row separator: '\n' (aka the 'new line', which is equivalent to pressing the enter button)
- Column separator: ',' (a single comma)

## Inventory File Structure

This file only reads information from the first column. All other columns are ignored.

The information in the first column is expected to follow a repeating pattern, such that each row corresponds to a particular piece of information:
1. The first row contains the name of the product
2. The second row contains the current quantity of the product
3. The third row contains irrelevant data and is thus ignored
4. The fourth row contains irrelevant data and is thus ignored
5. The fifth row contains irrelevant data and is thus ignored

Once the fifth row has been reached, the pattern resets and is followed again for the next five rows.

The second row, which is supposed to contain the quantity, must be a positive integer. If anything else is given, the program stops, and an error message is displayed.

## Re-order Point Requirements File Structure

This file only reads information from the first and the second column. All other columns are ignored.

The columns contain the following information:
- 1 : The first column contains the name of the product
- 2 : The second column contains the required minimum quantity of the product

The second column, which is supposed to contain the minimum required quantity, must be a positive integer. If anything else is given, the program stops, and an error message is displayed.

# Recompiling

The source code is located in the 'src' folder, which has the following four files:
- Application.py : Contains the source code for the entry point and the business logic of the application
- Config.py : Contains python configuration values for the application
- UIGen.py : Contains the source code used to generate the user interface
- compile.py : A setup file used with the p2exe python library in order to compile the Application.py file into a .exe file

To compile into a .exe file for distribution onto Windows computers, you must have a local instance of Python installed (version 3.7 or higher).

I used py2exe, but you can use whatever you like. py2exe can be found here:
- https://www.py2exe.org
