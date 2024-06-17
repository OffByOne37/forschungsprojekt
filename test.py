import os
import tkinter as tk
from tkinter import filedialog
from functools import partial
import numpy as np
import pandas as pd
from process_initial_csv import process_csv

# Import your existing functions
def read_student_data(file_path):
    processed_csv = "processed_data_1_2_3_4.csv"
    process_csv(file_path, processed_csv)
    data = pd.read_csv(processed_csv)

    # Delete the processed CSV file after reading
    if os.path.exists(processed_csv):
        os.remove(processed_csv)

    return data


def calculate_compatibility_indices(data):
    """
    Calculates a compatibility matrix where indices represent compatibility scores between students.
    """
    n = len(data)
    compatibility_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                wissen_diff = abs(data.at[i, 'Wissen'] - data.at[j, 'Wissen'])
                personality_diff = sum(abs(data.at[i, trait] - data.at[j, trait]) for trait in ['E', 'I', 'S', 'N', 'T', 'F', 'J', 'P'])
                personality_diff = (personality_diff / 32) * 10  # normalize it
                gender_bonus = -0.2 if data.at[i, 'Bitte gib dein Geschlecht an:'] == data.at[j, 'Bitte gib dein Geschlecht an:'] else 0
                compatibility_score = 0.5 * wissen_diff + 0.5 * personality_diff + gender_bonus

                # Adjust compatibility score based on preferences
                student1_name = data.at[i, 'Bitte gib deinen Namen an:']
                student2_name = data.at[j, 'Bitte gib deinen Namen an:']

                if data.at[i, "preference_1"] == student2_name:
                    compatibility_score -= 0.5
                if data.at[i, "preference_2"] == student2_name:
                    compatibility_score -= 0.3
                if data.at[i, "preference_3"] == student2_name:
                    compatibility_score -= 0.1


                compatibility_matrix[i, j] = compatibility_score

    return compatibility_matrix

def rank_preferences(compatibility_matrix):
    """
    Creates a preference list for each student based on the compatibility indices.
    """
    n = compatibility_matrix.shape[0]
    preferences = []

    for i in range(n):
        sorted_indices = np.argsort(compatibility_matrix[i])[::-1]  # Sort in descending order
        preferences.append([ind for ind in sorted_indices if ind != i])  # Exclude own index

    return preferences

def gale_shapley(n, preferences, compatibility_matrix, data):
    """
    Implements the Gale-Shapley algorithm to find a stable matching.
    """
    free_students = list(range(n))
    engaged_pairs = [-1] * n
    proposals = np.zeros(n, dtype=int)

    if n % 2 == 0:
        # Even number of students
        while free_students:
            student = free_students.pop(0)
            if not preferences[student]:  # Check if preferences list is empty
                continue
            
            preferred = preferences[student][min(proposals[student], len(preferences[student]) - 1)]
            
            if preferred == student:
                continue  # Skip if student tries to propose to themselves
            
            if engaged_pairs[preferred] == -1:
                engaged_pairs[preferred] = student
            else:
                current_partner = engaged_pairs[preferred]
                current_partner_rank = preferences[preferred].index(current_partner)
                new_partner_rank = preferences[preferred].index(student)
                
                if new_partner_rank < current_partner_rank:
                    engaged_pairs[preferred] = student
                    free_students.append(current_partner)
                else:
                    free_students.append(student)
            
            proposals[student] += 1

    else:
        # Odd number of students
        while len(free_students) > 1:
            student = free_students.pop(0)
            if not preferences[student]:  # Check if preferences list is empty
                continue
            
            preferred = preferences[student][min(proposals[student], len(preferences[student]) - 1)]
            
            if preferred == student:
                continue  # Skip if student tries to propose to themselves
            
            if engaged_pairs[preferred] == -1:
                engaged_pairs[preferred] = student
            else:
                current_partner = engaged_pairs[preferred]
                current_partner_rank = preferences[preferred].index(current_partner)
                new_partner_rank = preferences[preferred].index(student)
                
                if new_partner_rank < current_partner_rank:
                    engaged_pairs[preferred] = student
                    free_students.append(current_partner)
                else:
                    free_students.append(student)
            
            proposals[student] += 1


    return [(partner, student, compatibility_matrix[partner, student]) for partner, student in enumerate(engaged_pairs) if student != -1]

def create_stable_pairs(file_path, output_text):
    data = read_student_data(file_path)
    compatibility_matrix = calculate_compatibility_indices(data)
    preferences = rank_preferences(compatibility_matrix)
    pairs = gale_shapley(len(data), preferences, compatibility_matrix, data)

    paired_students = set()
    printed = set()
    output_text.delete(1.0, tk.END)  # Clear previous content
    for student1, student2, score in pairs:
        if (student1, student2) not in paired_students and (student2, student1) not in paired_students:
            name1 = data.at[student1, 'Bitte gib deinen Namen an:']
            name2 = data.at[student2, 'Bitte gib deinen Namen an:']
            output_text.insert(tk.END, f"Pair: {name1} and {name2}, Compatibility Score: {score:.2f}\n")
            paired_students.add((student1, student2))
            printed.add(student1)
            printed.add(student2)

    unpaired_students = []
    for i in range(len(data)):
        if i not in printed:
            unpaired_students.append(data.at[i, 'Bitte gib deinen Namen an:'])

    if unpaired_students:
        output_text.insert(tk.END, f"Unpaired Student: {', '.join(unpaired_students)}\n")
    else:
        output_text.insert(tk.END, "All students are paired.\n")

# GUI setup
def run_algorithm(file_path_entry, output_text):
    file_path = file_path_entry.get()
    create_stable_pairs(file_path, output_text)

def browse_files(file_path_entry):
    filename = filedialog.askopenfilename(initialdir="/", title="Select a CSV file",
                                          filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, filename)

root = tk.Tk()
root.title("Stable Pairing Algorithm")

# Frame to hold widgets
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

# File path entry and browse button
entry_frame = tk.Frame(frame)
entry_frame.pack(pady=10)

tk.Label(entry_frame, text="CSV File Path:", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
file_path_entry = tk.Entry(entry_frame, width=50, font=("Arial", 12))
file_path_entry.pack(side=tk.LEFT, padx=10)

browse_button = tk.Button(entry_frame, text="Browse", font=("Arial", 12), command=partial(browse_files, file_path_entry))
browse_button.pack(side=tk.LEFT, padx=10)

# Output text area
output_text = tk.Text(frame, height=10, width=80, font=("Arial", 12))
output_text.pack(pady=10)

# Run button
run_button = tk.Button(frame, text="Run Algorithm", font=("Arial", 14), command=partial(run_algorithm, file_path_entry, output_text))
run_button.pack(pady=10)

root.mainloop()
