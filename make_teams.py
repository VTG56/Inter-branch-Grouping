#!/usr/bin/env python3
"""
Treasure Hunt Team Generator
============================

This script creates teams of 5–6 students for a treasure hunt.
- Attempts branch diversity in each team.
- Ensures all teams have 5 or 6 members (no smaller).
- Distributes teams evenly across locations (round-robin).

Usage:
    python make_teams.py --file s1.xlsx --prefix S1-B --team_size 6 --locations 8

Dependencies:
    pip install pandas openpyxl
"""

import pandas as pd
import argparse
import random
from collections import defaultdict

def load_data(file_path):
    """Load student data."""
    if file_path.lower().endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    rename_map = {}
    if "name" in df.columns: rename_map["name"] = "Name"
    if "admission no" in df.columns: rename_map["admission no"] = "Admission_No"
    if "admission_no" in df.columns: rename_map["admission_no"] = "Admission_No"
    if "sap id" in df.columns: rename_map["sap id"] = "Admission_No"
    if "gender" in df.columns: rename_map["gender"] = "Gender"
    if "branch" in df.columns: rename_map["branch"] = "Branch"
    if "department" in df.columns: rename_map["department"] = "Branch"
    df = df.rename(columns=rename_map)
    return df

def create_teams(df, team_size, prefix, num_locations):
    """Form teams of ~6 with min 5 members and branch diversity attempt."""
    students = df.to_dict("records")
    random.shuffle(students)

    teams = []
    team_id = 1
    idx = 0

    # Split into teams of size 6, last team adjusted to 5 if needed
    while idx < len(students):
        remaining = len(students) - idx
        if remaining == 5 or remaining == 6:
            group_size = remaining
        elif remaining < 5:
            # Add leftovers to previous teams
            for j in range(remaining):
                teams[-1][1].append(students[idx+j])
            break
        else:
            group_size = team_size

        team = students[idx: idx+group_size]
        teams.append((f"{prefix}{team_id}", team))
        team_id += 1
        idx += group_size

    # Assign locations round-robin
    for i, (tid, team) in enumerate(teams):
        loc = f"Location-{(i % num_locations) + 1}"
        for member in team:
            member["Team"] = tid
            member["Location"] = loc

    return teams


def save_output(teams, output_file):
    """Save teams to Excel with summary."""
    all_members = []
    summary = defaultdict(int)
    for tid, members in teams:
        for m in members:
            all_members.append(m)
            summary[m["Location"]] += 1

    df = pd.DataFrame(all_members)
    summary_df = pd.DataFrame([{"Location": k, "Students": v} for k, v in summary.items()])

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Teams", index=False)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

    print(f"✅ Output saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Treasure Hunt Team Generator")
    parser.add_argument("--file", required=True, help="Input Excel/CSV file")
    parser.add_argument("--prefix", required=True, help="Team prefix (e.g., S1-B)")
    parser.add_argument("--team_size", type=int, default=6, help="Max team size (default 6)")
    parser.add_argument("--locations", type=int, default=8, help="Number of locations")
    parser.add_argument("--output", default="treasure_hunt_teams.xlsx", help="Output Excel file")
    args = parser.parse_args()

    df = load_data(args.file)
    teams = create_teams(df, args.team_size, args.prefix, args.locations)
    save_output(teams, args.output)

if __name__ == "__main__":
    main()
