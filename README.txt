Student Grouping Tool - Complete Setup & Usage Guide
🚀 Quick Setup (Copy-Paste Commands)
Step 1: Install Required Packages
bashpip install pandas openpyxl
Step 2: Save the Script

Copy the entire group_students.py script from the artifact above
Save it as group_students.py in your desired folder
Make sure your student data file is in the same folder (or note the full path)

Step 3: Prepare Your Data File
Your Excel/CSV file must have these columns (any names work, case doesn't matter):

Name (or Student Name, Full Name, etc.)
Admission No (or Admission Number, ID, Student ID, etc.)
Gender (or Sex - accepts M/Male/F/Female)
Branch (or Department, Stream, Course, etc.)

Note: Extra columns like Phone, Email, Address will be preserved in output

📋 Usage Commands (Copy-Paste Ready)
Option 1: Create Numbered Classes
bash# For 10 classes named Class_01, Class_02, etc.
python group_students.py --file students.xlsx --classes 10

# For 25 classes
python group_students.py --file students.xlsx --classes 25

# With CSV file
python group_students.py --file students.csv --classes 15
Option 2: Use Custom Classroom Names
bash# Multiple custom classroom names
python group_students.py --file students.xlsx --classrooms "AIML-CR001,AIML-CR002,BT-217,BT-218,CSE-A,CSE-B"

# With spaces in names (use quotes)
python group_students.py --file students.xlsx --classrooms "Room 101,Room 102,Lab A,Lab B"
Option 3: Specify Custom Output File
bash# Custom output filename
python group_students.py --file students.xlsx --classes 10 --output my_classes_2024.xlsx

# Full path output
python group_students.py --file students.xlsx --classes 8 --output "C:/Results/grouped_students.xlsx"

📁 File Structure Examples
Before Running:
📁 Your Folder/
├── group_students.py
├── students.xlsx        ← Your input file
└── (other files...)
After Running:
📁 Your Folder/
├── group_students.py
├── students.xlsx
├── grouped_students.xlsx    ← Generated output
└── (other files...)

🎯 Sample Command Flows
Scenario 1: Engineering College with 400 students, 25 classes
bashcd "C:/StudentData"
python group_students.py --file engineering_students_2024.xlsx --classes 25
Scenario 2: Medical College with specific room assignments
bashpython group_students.py --file medical_batch.csv --classrooms "Room-A1,Room-A2,Room-B1,Room-B2,Lab-1,Lab-2"
Scenario 3: Multiple batches (run separately)
bash# Batch 1
python group_students.py --file batch1.xlsx --classes 10 --output batch1_grouped.xlsx

# Batch 2  
python group_students.py --file batch2.xlsx --classes 12 --output batch2_grouped.xlsx

📊 Expected Output
Console Output Example:
🎓 Student Classroom Distribution Tool
========================================
📂 Checking input file: students.xlsx
✅ Excel file loaded successfully
✅ Found 400 students with required columns

📊 Analyzing student data...
📈 Total students: 400
📈 Gender distribution: {'M': 250, 'F': 150}
📈 Branch distribution: {'CSE': 120, 'ECE': 100, 'MECH': 80, 'CIVIL': 100}

🏫 Creating 10 classrooms:
   - Class_01
   - Class_02
   - ...

🔄 Distributing students across classrooms...
   Distributing 60 students from CSE (M)
   Distributing 60 students from CSE (F)
   ...

📋 Generating distribution summary...

📊 Final Distribution Summary:
Class_01: 40 students
   Gender: M: 25, F: 15
   Branch: CSE: 12, ECE: 10, MECH: 8, CIVIL: 10

💾 Writing output to grouped_students.xlsx...
✅ Output file written successfully!
🎉 Process completed! Check 'grouped_students.xlsx' for results.
Excel Output Structure:

Summary Sheet: Overview of all classes
Class_01 Sheet: Students assigned to Class 1
Class_02 Sheet: Students assigned to Class 2
... (one sheet per classroom)


🛠️ Troubleshooting
Common Errors & Fixes:
❌ "File not found"
bash# Make sure file exists and path is correct
python group_students.py --file "C:/full/path/to/students.xlsx" --classes 10
❌ "Missing required columns"

Check your Excel/CSV has: Name, Admission No, Gender, Branch columns
Column names are flexible (case doesn't matter)

❌ "Permission denied" when writing output

Close Excel if output file is open
Check write permissions in the folder

❌ "Module not found"
bash# Reinstall packages
pip install --upgrade pandas openpyxl

📋 Edge Cases Covered
✅ Data Quality Issues:

Missing data: Automatically removes rows with missing critical info
Inconsistent gender values: Maps "Male"→"M", "Female"→"F", handles case variations
Extra whitespace: Strips whitespace from all text fields
Mixed case columns: Case-insensitive column matching
Special characters: Handles names with special characters and unicode

✅ Distribution Challenges:

Uneven numbers: If 403 students ÷ 10 classes, distributes as 41,41,41,40,40,40,40,40,40,40
Gender imbalance: If only 5 girls in 400 students, ensures no class gets 0 girls
Branch imbalance: Distributes minority branches evenly (e.g., 7 BioTech students across 10 classes)
Small class sizes: Handles edge case of more classes than students in a branch
Zero students: Creates empty sheets if somehow a class gets no students

✅ File Format Issues:

Excel versions: Supports .xlsx and .xls formats
CSV encodings: Handles UTF-8, Windows encoding automatically
Large files: Uses pandas chunking for memory efficiency
Corrupted files: Graceful error handling with clear messages

✅ Output Issues:

Sheet name restrictions: Excel sheet names cleaned (removes /, , limited to 31 chars)
Duplicate classroom names: Handles duplicates automatically
File permissions: Checks write access before processing
Existing output files: Overwrites existing output files safely

✅ Input Validation:

Invalid class numbers: Checks for positive integers
Empty classroom lists: Validates classroom name list isn't empty
File extensions: Only accepts .xlsx, .xls, .csv files
Column variations: Accepts "Admission Number", "Student ID", "Reg No", etc.


❌ Multiple Files NOT Supported
Important Note: The current script processes ONE file at a time.
For multiple files, you need to run separate commands:
bash# Process each file separately
python group_students.py --file batch1.xlsx --classes 10 --output batch1_groups.xlsx
python group_students.py --file batch2.xlsx --classes 10 --output batch2_groups.xlsx
python group_students.py --file batch3.xlsx --classes 10 --output batch3_groups.xlsx
Alternative: Merge all files into one Excel/CSV first, then run the script once.

🔄 Quick Reference Commands
bash# Basic usage
python group_students.py --file [YOUR_FILE] --classes [NUMBER]

# Custom rooms
python group_students.py --file [YOUR_FILE] --classrooms "Room1,Room2,Room3"

# Custom output
python group_students.py --file [YOUR_FILE] --classes [NUMBER] --output [OUTPUT_NAME].xlsx

# Help
python group_students.py --help
