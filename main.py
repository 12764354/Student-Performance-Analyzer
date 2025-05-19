import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend
import matplotlib.pyplot as plt
import os

# Define subjects
SUBJECTS = ["Machine Learning", "UHV", "DMGT", "DBMS", "OT", "ES"]
CSV_FILE = "student_data.csv"

def initialize_csv():
    """Initialize CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Name"] + SUBJECTS)
        df.to_csv(CSV_FILE, index=False)
    else:
        # Ensure existing CSV has all required columns
        try:
            df = pd.read_csv(CSV_FILE)
            for sub in SUBJECTS:
                if sub not in df.columns:
                    df[sub] = 0  # Initialize missing columns with 0
            df.to_csv(CSV_FILE, index=False)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["Name"] + SUBJECTS)
            df.to_csv(CSV_FILE, index=False)

def add_student():
    """Add a new student record"""
    print("\n--- Add Student ---")
    name = input("Enter student name: ")
    marks = []
    
    for sub in SUBJECTS:
        while True:
            try:
                mark = int(input(f"Enter {sub} marks (out of 100): "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                else:
                    print("Marks should be between 0 and 100!")
            except ValueError:
                print("Please enter a valid number!")
    
    # Create new student data
    new_student = {"Name": name}
    new_student.update({sub: mark for sub, mark in zip(SUBJECTS, marks)})
    
    # Read existing data or create new DataFrame
    if os.path.exists(CSV_FILE) and os.stat(CSV_FILE).st_size > 0:
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["Name"] + SUBJECTS)
    
    # Append new student
    df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    print("Student added successfully!")

def calculate_percentage(row):
    """Calculate percentage for a single student"""
    try:
        total = sum(row[sub] for sub in SUBJECTS)
        return round((total / (len(SUBJECTS) * 100)) * 100, 2)
    except KeyError:
        print(f"Warning: Missing subject data for {row['Name']}")
        return 0.0

def assign_grade(percentage):
    """Assign grade based on percentage"""
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

def analyze_performance():
    """Analyze and visualize student performance"""
    try:
        # Check if file exists and has data
        if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
            print("No data found! Add students first.")
            return
        
        # Read and validate data
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            print("No student records found!")
            return
            
        # Ensure all subject columns exist
        for sub in SUBJECTS:
            if sub not in df.columns:
                df[sub] = 0
        
        # Calculate performance metrics
        df['Percentage'] = df.apply(calculate_percentage, axis=1)
        df['Grade'] = df['Percentage'].apply(assign_grade)
        
        while True:
            print("\n--- Performance Analysis ---")
            print("1. View All Students")
            print("2. Subject-wise Averages")
            print("3. Find Topper and Duller")
            print("4. Class Statistics")
            print("5. Back to Main Menu")
            choice = input("Enter choice (1-5): ")
            
            if choice == "1":
                print("\nAll Students:")
                print(df[['Name'] + SUBJECTS + ['Percentage', 'Grade']].to_string(index=False))
            
            elif choice == "2":
                avg_marks = df[SUBJECTS].mean().round(2)
                plt.figure(figsize=(10, 5))
                bars = plt.bar(avg_marks.index, avg_marks.values, color='skyblue')
                plt.title("Subject-wise Average Marks", pad=20)
                plt.ylabel("Average Marks")
                plt.xticks(rotation=45, ha='right')
                
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2, height,
                            f'{height}',
                            ha='center', va='bottom')
                
                plt.tight_layout()
                plt.savefig('subject_averages.png')
                print("Graph saved as 'subject_averages.png'")
                plt.close()
            
            elif choice == "3":
                if len(df) > 0:
                    topper = df.loc[df['Percentage'].idxmax()]
                    duller = df.loc[df['Percentage'].idxmin()]
                    
                    print("\n--- TOPPER ---")
                    print(f"Name: {topper['Name']}")
                    print(f"Percentage: {topper['Percentage']}%")
                    print(f"Grade: {topper['Grade']}")
                    
                    print("\n--- DULLER ---")
                    print(f"Name: {duller['Name']}")
                    print(f"Percentage: {duller['Percentage']}%")
                    print(f"Grade: {duller['Grade']}")
                else:
                    print("No students to analyze!")
            
            elif choice == "4":
                if len(df) > 0:
                    class_avg = df['Percentage'].mean().round(2)
                    highest_avg = df[SUBJECTS].mean().max().round(2)
                    lowest_avg = df[SUBJECTS].mean().min().round(2)
                    
                    print(f"\nClass Average Percentage: {class_avg}%")
                    print(f"Class Overall Grade: {assign_grade(class_avg)}")
                    print(f"Highest Subject Average: {highest_avg}")
                    print(f"Lowest Subject Average: {lowest_avg}")
                    
                    grade_counts = df['Grade'].value_counts().sort_index()
                    plt.figure(figsize=(8, 8))
                    plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%',
                           startangle=140, colors=['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#FF5722', '#F44336'])
                    plt.title("Grade Distribution", pad=20)
                    plt.savefig('grade_distribution.png')
                    print("Grade distribution chart saved as 'grade_distribution.png'")
                    plt.close()
                else:
                    print("No students to analyze!")
            
            elif choice == "5":
                break
            
            else:
                print("Invalid choice! Please enter 1-5")
    
    except Exception as e:
        print(f"An error occurred during analysis: {str(e)}")

def main():
    """Main program loop"""
    initialize_csv()
    print("\nSTUDENT PERFORMANCE ANALYZER")
    
    while True:
        print("\nMAIN MENU")
        print("1. Add Student")
        print("2. Analyze Performance")
        print("3. Exit")
        choice = input("Enter choice (1-3): ")
        
        if choice == "1":
            add_student()
        elif choice == "2":
            analyze_performance()
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Please enter 1-3")

if __name__ == "__main__":
    main()
