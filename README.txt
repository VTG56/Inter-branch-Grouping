# 🎓 Student Grouping Tool – Complete Setup & Usage Guide  

A Python tool to automatically group students into balanced classrooms based on **gender, branch, and admission number.**  
Generates an **Excel file with one sheet per classroom + a summary sheet.**  

This tool was used to group students into batches for classroom activities and treasure hunt during SIP 2025.

---

## 🚀 Quick Setup  

### Step 1: Install Required Packages  
- `pip install pandas openpyxl`

### Step 2: Save the Script  
- Copy the entire `group_students.py` script from the artifact.  
- Save it as `group_students.py` in your desired folder.  
- Place your student data file (`.xlsx` or `.csv`) in the same folder (or note the full path).  

### Step 3: Prepare Your Data File  
Your **Excel/CSV** must include these columns (case-insensitive, flexible names):  
- **Name** → accepts `Name`, `Student Name`, `Full Name`, etc.  
- **Admission No** → accepts `Admission Number`, `ID`, `Student ID`, etc.  
- **Gender** → accepts `M`, `Male`, `F`, `Female`.  
- **Branch** → accepts `Department`, `Stream`, `Course`, etc.  

Extra columns like Phone, Email, Address will be **preserved**.  

---

## 📋 Usage Commands  

### Option 1: Create Numbered Classes  
- For 10 classes named Class_01, Class_02, ...  
  - `python group_students.py --file students.xlsx --classes 10`  
- For 25 classes  
  - `python group_students.py --file students.xlsx --classes 25`  
- With CSV file  
  - `python group_students.py --file students.csv --classes 15`  

### Option 2: Use Custom Classroom Names  
- Multiple custom classroom names  
  - `python group_students.py --file students.xlsx --classrooms "AIML-CR001,AIML-CR002,BT-217,BT-218,CSE-A,CSE-B"`  
- With spaces in names (use quotes)  
  - `python group_students.py --file students.xlsx --classrooms "Room 101,Room 102,Lab A,Lab B"`  

### Option 3: Specify Custom Output File  
- Custom output filename  
  - `python group_students.py --file students.xlsx --classes 10 --output my_classes_2024.xlsx`  
- Full path output  
  - `python group_students.py --file students.xlsx --classes 8 --output "C:/Results/grouped_students.xlsx"`  

---

## 📁 File Structure Examples  

**Before Running:**  
- `group_students.py`  
- `students.xlsx` ← Your input file  
- (other files...)  

**After Running:**  
- `group_students.py`  
- `students.xlsx`  
- `grouped_students.xlsx` ← Generated output  
- (other files...)  

---

## 📊 Expected Output  

**Console Example:**  
- 🎓 Student Classroom Distribution Tool  
- 📂 Checking input file: students.xlsx  
- ✅ Excel file loaded successfully  
- ✅ Found 400 students with required columns  
- 📊 Analyzing student data...  
- 📈 Total students: 400  
- 📈 Gender distribution: {'M': 250, 'F': 150}  
- 📈 Branch distribution: {'CSE': 120, 'ECE': 100, 'MECH': 80, 'CIVIL': 100}  
- 🏫 Creating 10 classrooms: Class_01, Class_02, ...  
- 🔄 Distributing students across classrooms...  
- 📋 Generating distribution summary...  
- 📊 Final Distribution Summary: Class_01: 40 students (Gender: M: 25, F: 15; Branch: CSE: 12, ECE: 10, MECH: 8, CIVIL: 10)  
- 💾 Writing output to grouped_students.xlsx...  
- ✅ Output file written successfully!  
- 🎉 Process completed!  

**Excel Output Structure:**  
- **Summary Sheet**: Overview of all classes  
- **Class_01 Sheet**: Students in Class 1  
- **Class_02 Sheet**: Students in Class 2  
- ... one sheet per classroom  

---

## 🛠️ Troubleshooting  

- **❌ "File not found"**  
  - `python group_students.py --file "C:/full/path/to/students.xlsx" --classes 10`  

- **❌ "Missing required columns"**  
  - Ensure Excel/CSV has: Name, Admission No, Gender, Branch.  

- **❌ "Permission denied" when writing output**  
  - Close Excel if output file is open.  
  - Check write permissions.  

- **❌ "Module not found"**  
  - `pip install --upgrade pandas openpyxl`  

---

## 📋 Edge Cases Covered  

- ✅ **Data Quality**: Missing data removed, whitespace trimmed, inconsistent gender fixed.  
- ✅ **Distribution**: Balances uneven gender/branch counts, ensures fairness.  
- ✅ **File Formats**: Supports `.xlsx`, `.xls`, `.csv` with multiple encodings.  
- ✅ **Output**: Handles empty classes, duplicate names, sheet restrictions.  
- ✅ **Validation**: Checks input types, prevents invalid configs.  

- ❌ **Multiple Files NOT Supported**  
  - Run separately for each batch:  
    - `python group_students.py --file batch1.xlsx --classes 10 --output batch1_groups.xlsx`  
    - `python group_students.py --file batch2.xlsx --classes 10 --output batch2_groups.xlsx`  
    - `python group_students.py --file batch3.xlsx --classes 10 --output batch3_groups.xlsx`  
  - Or merge files first and run once.  

---

## 🔄 Quick Reference Commands  

- Basic usage  
  - `python group_students.py --file [YOUR_FILE] --classes [NUMBER]`  

- Custom rooms  
  - `python group_students.py --file [YOUR_FILE] --classrooms "Room1,Room2,Room3"`  

- Custom output  
  - `python group_students.py --file [YOUR_FILE] --classes [NUMBER] --output [OUTPUT_NAME].xlsx`
