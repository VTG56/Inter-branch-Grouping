#!/usr/bin/env python3
"""
Student Classroom Distribution Script
=====================================

This script distributes students from an Excel/CSV file into balanced classrooms
while maintaining gender ratios and branch diversity.

Usage:
    python group_students.py --file students.xlsx --classes 25
    python group_students.py --file students.csv --classrooms "AIML-CR001,AIML-CR002,BT-217"

Requirements:
    pip install pandas openpyxl

Author: AI Assistant
"""

import pandas as pd
import argparse
import sys
import os
from math import ceil
from collections import Counter, defaultdict


def validate_input_file(file_path):
    """
    Validate that the input file exists and has the required format.
    
    Args:
        file_path (str): Path to the input file
        
    Returns:
        pd.DataFrame: The loaded student data
        
    Raises:
        SystemExit: If file doesn't exist or required columns are missing
    """
    print(f"📂 Checking input file: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found!")
        sys.exit(1)
    
    # Read the file based on extension
    try:
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
            print("✅ CSV file loaded successfully")
        elif file_path.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
            print("✅ Excel file loaded successfully")
        else:
            print("❌ Error: File must be CSV (.csv) or Excel (.xlsx, .xls)")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)
    
    # Check for required columns (case-insensitive)
    # You can modify these lists to add more column name variations
    column_variations = {
        'name': ['name', 'student name', 'full name', 'student_name', 'fullname'],
        'admission_no': ['admission no', 'admission number', 'sap id', 'usn', 'student id', 
                        'admission_no', 'admission_number', 'sap_id', 'student_id', 'roll no', 'roll number'],
        'gender': ['gender', 'sex', 'male/female', 'm/f'],
        'branch': ['branch', 'department', 'course', 'stream', 'dept', 'program']
    }
    
    df_cols_lower = [col.lower().strip() for col in df.columns]
    
    missing_cols = []
    col_mapping = {}
    
    for req_col, variations in column_variations.items():
        found = False
        for variation in variations:
            for i, df_col in enumerate(df_cols_lower):
                if variation in df_col or df_col in variation:
                    col_mapping[req_col] = df.columns[i]
                    found = True
                    break
            if found:
                break
        if not found:
            missing_cols.append(req_col)
    
    if missing_cols:
        print(f"❌ Error: Missing required columns: {missing_cols}")
        print(f"Available columns: {list(df.columns)}")
        sys.exit(1)
    
    # Rename columns to standard names for processing
    standard_names = {'name': 'Name', 'admission_no': 'Admission_No', 'gender': 'Gender', 'branch': 'Branch'}
    rename_dict = {col_mapping[req]: standard_names[req] for req in col_mapping.keys()}
    df = df.rename(columns=rename_dict)
    
    print(f"✅ Found {len(df)} students with required columns")
    return df


def analyze_student_data(df):
    """
    Analyze the student data to understand distributions.
    
    Args:
        df (pd.DataFrame): Student dataframe
        
    Returns:
        dict: Analysis results
    """
    print("\n📊 Analyzing student data...")
    
    # Clean and standardize gender values
    df['Gender'] = df['Gender'].astype(str).str.strip().str.upper()
    gender_mapping = {'M': 'M', 'MALE': 'M', 'F': 'F', 'FEMALE': 'F'}
    df['Gender'] = df['Gender'].map(gender_mapping).fillna(df['Gender'])
    
    # Remove any rows with missing critical data
    original_count = len(df)
    df = df.dropna(subset=['Name', 'Admission_No', 'Gender', 'Branch'])
    if len(df) < original_count:
        print(f"⚠️  Removed {original_count - len(df)} rows with missing critical data")
    
    total_students = len(df)
    gender_counts = df['Gender'].value_counts()
    branch_counts = df['Branch'].value_counts()
    
    print(f"📈 Total students: {total_students}")
    print(f"📈 Gender distribution: {dict(gender_counts)}")
    print(f"📈 Branch distribution: {dict(branch_counts)}")
    
    return {
        'total_students': total_students,
        'gender_counts': gender_counts,
        'branch_counts': branch_counts,
        'dataframe': df
    }


def calculate_target_distributions(analysis, num_classes):
    """
    Calculate target distributions for each class.
    
    Args:
        analysis (dict): Results from analyze_student_data
        num_classes (int): Number of classes to create
        
    Returns:
        dict: Target distributions
    """
    print(f"\n🎯 Calculating target distributions for {num_classes} classes...")
    
    total_students = analysis['total_students']
    gender_counts = analysis['gender_counts']
    branch_counts = analysis['branch_counts']
    
    # Calculate target class size
    target_class_size = ceil(total_students / num_classes)
    
    # Calculate target gender distribution per class
    target_gender_per_class = {}
    remaining_students = total_students
    
    for gender in gender_counts.index:
        total_of_gender = gender_counts[gender]
        per_class = total_of_gender // num_classes
        remainder = total_of_gender % num_classes
        target_gender_per_class[gender] = [per_class + (1 if i < remainder else 0) for i in range(num_classes)]
    
    # Calculate target branch distribution per class
    target_branch_per_class = {}
    for branch in branch_counts.index:
        total_of_branch = branch_counts[branch]
        per_class = total_of_branch // num_classes
        remainder = total_of_branch % num_classes
        target_branch_per_class[branch] = [per_class + (1 if i < remainder else 0) for i in range(num_classes)]
    
    print(f"✅ Target class size: {target_class_size}")
    print(f"✅ Target gender distribution calculated")
    print(f"✅ Target branch distribution calculated")
    
    return {
        'target_class_size': target_class_size,
        'target_gender_per_class': target_gender_per_class,
        'target_branch_per_class': target_branch_per_class
    }


def distribute_students(df, targets, classroom_names):
    """
    Distribute students across classrooms using round-robin by branch and gender.
    
    Args:
        df (pd.DataFrame): Student dataframe
        targets (dict): Target distributions
        classroom_names (list): List of classroom names
        
    Returns:
        dict: Dictionary mapping classroom names to student dataframes
    """
    print("\n🔄 Distributing students across classrooms...")
    
    num_classes = len(classroom_names)
    
    # Initialize classroom assignments
    classrooms = {name: [] for name in classroom_names}
    class_counters = {name: {'total': 0, 'gender': defaultdict(int), 'branch': defaultdict(int)} 
                     for name in classroom_names}
    
    # Group students by branch and gender for systematic distribution
    branch_gender_groups = df.groupby(['Branch', 'Gender'])
    
    # Round-robin distribution within each branch-gender group
    for (branch, gender), group in branch_gender_groups:
        students = group.to_dict('records')
        print(f"   Distributing {len(students)} students from {branch} ({gender})")
        
        # Distribute this group across classes in round-robin fashion
        for i, student in enumerate(students):
            class_idx = i % num_classes
            classroom_name = classroom_names[class_idx]
            
            classrooms[classroom_name].append(student)
            class_counters[classroom_name]['total'] += 1
            class_counters[classroom_name]['gender'][gender] += 1
            class_counters[classroom_name]['branch'][branch] += 1
    
    # Convert lists to DataFrames
    classroom_dfs = {}
    for name, students in classrooms.items():
        if students:
            classroom_dfs[name] = pd.DataFrame(students)
        else:
            # Create empty DataFrame with same columns as original
            classroom_dfs[name] = pd.DataFrame(columns=df.columns)
    
    print("✅ Student distribution completed")
    return classroom_dfs, class_counters


def generate_summary(class_counters, classroom_names):
    """
    Generate a summary of the distribution.
    
    Args:
        class_counters (dict): Counters for each classroom
        classroom_names (list): List of classroom names
        
    Returns:
        pd.DataFrame: Summary dataframe
    """
    print("\n📋 Generating distribution summary...")
    
    summary_data = []
    
    for name in classroom_names:
        counters = class_counters[name]
        
        # Gender breakdown
        gender_str = ', '.join([f"{g}: {c}" for g, c in counters['gender'].items()])
        
        # Branch breakdown
        branch_str = ', '.join([f"{b}: {c}" for b, c in counters['branch'].items()])
        
        summary_data.append({
            'Classroom': name,
            'Total_Students': counters['total'],
            'Gender_Distribution': gender_str,
            'Branch_Distribution': branch_str
        })
    
    summary_df = pd.DataFrame(summary_data)
    print("✅ Summary generated")
    return summary_df


def write_output_file(classroom_dfs, summary_df, output_file):
    """
    Write the grouped students to an Excel file.
    
    Args:
        classroom_dfs (dict): Dictionary of classroom dataframes
        summary_df (pd.DataFrame): Summary dataframe
        output_file (str): Output file path
    """
    print(f"\n💾 Writing output to {output_file}...")
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Write summary sheet first
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Write each classroom to a separate sheet
            for classroom_name, df in classroom_dfs.items():
                # Clean sheet name (Excel sheet names have restrictions)
                sheet_name = str(classroom_name).replace('/', '-').replace('\\', '-')[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print("✅ Output file written successfully!")
        
    except Exception as e:
        print(f"❌ Error writing output file: {e}")
        sys.exit(1)


def main():
    """Main function to orchestrate the student grouping process."""
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Distribute students into balanced classrooms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python group_students.py --file students.xlsx --classes 25
  python group_students.py --file students.csv --classrooms "AIML-CR001,AIML-CR002,BT-217,BT-218"
        """
    )
    
    parser.add_argument('--file', required=True, help='Input Excel or CSV file path')
    
    # Mutually exclusive group for class specification
    class_group = parser.add_mutually_exclusive_group(required=True)
    class_group.add_argument('--classes', type=int, help='Number of classes to create')
    class_group.add_argument('--classrooms', type=str, help='Comma-separated list of classroom names')
    
    parser.add_argument('--output', default='grouped_students.xlsx', 
                       help='Output Excel file name (default: grouped_students.xlsx)')
    
    # Parse arguments
    args = parser.parse_args()
    
    print("🎓 Student Classroom Distribution Tool")
    print("=" * 40)
    
    # Validate and load input file
    df = validate_input_file(args.file)
    
    # Analyze student data
    analysis = analyze_student_data(df)
    
    # Determine classroom names
    if args.classes:
        classroom_names = [f"Class_{i+1:02d}" for i in range(args.classes)]
        num_classes = args.classes
    else:
        classroom_names = [name.strip() for name in args.classrooms.split(',')]
        num_classes = len(classroom_names)
    
    print(f"\n🏫 Creating {num_classes} classrooms:")
    for name in classroom_names:
        print(f"   - {name}")
    
    # Calculate target distributions
    targets = calculate_target_distributions(analysis, num_classes)
    
    # Distribute students
    classroom_dfs, class_counters = distribute_students(
        analysis['dataframe'], targets, classroom_names
    )
    
    # Generate summary
    summary_df = generate_summary(class_counters, classroom_names)
    
    # Display summary
    print("\n📊 Final Distribution Summary:")
    print("-" * 50)
    for _, row in summary_df.iterrows():
        print(f"{row['Classroom']}: {row['Total_Students']} students")
        print(f"   Gender: {row['Gender_Distribution']}")
        print(f"   Branch: {row['Branch_Distribution']}")
        print()
    
    # Write output file
    write_output_file(classroom_dfs, summary_df, args.output)
    
    print(f"🎉 Process completed! Check '{args.output}' for results.")
    print("\n📁 Output file contains:")
    print("   - Summary sheet with distribution statistics")
    print("   - Individual sheets for each classroom")
    print("   - All original columns preserved")


if __name__ == "__main__":
    main()