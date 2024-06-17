import csv

# Define the mapping for "Bewerten Sie Ihr Verständnis für das Thema HTML und JavaScript."
knowledge_mapping = {
    "unter 10 Stunden": 2,
    "zwischen 10 und 20 Stunden": 4,
    "zwischen 21 und 30 Stunden": 6,
    "zwischen 31 und 40 Stunden": 8,
    "über 40 Stunden": 10
}

# Indices of the columns needed for calculations
name_index = 1
gender_index = 2
html_js_index = 3
websites_index = 4
hours_index = 5
e_indices = [6, 7, 8, 9]
i_indices = [10, 11, 12, 13]
s_indices = [14, 15, 16, 17]
n_indices = [18, 19, 20, 21]
t_indices = [22, 23, 24, 25]
f_indices = [26, 27, 28, 29]
j_indices = [30, 31, 32, 33]
p_indices = [34, 35, 36, 37]
preference_index = 38
grade_index = 39

def calculate_sum(row, indices):
    return sum(1 for i in indices if row[i].strip().lower() == "ja")

def process_row(row):
    name = row[1]
    gender = row[2]
    hours = knowledge_mapping.get(row[hours_index], 0)
    websites = int(row[websites_index])
    html_js = int(row[html_js_index])
    grade = float(row[grade_index].strip(' "'))  # Remove leading/trailing spaces and quotes
 
    wissen = 0.5 *grade + 0.5 * ((websites + hours + html_js)/3)

    assert(wissen >=0 and wissen <=10)

    e = calculate_sum(row, e_indices)
    i = calculate_sum(row, i_indices)
    s = calculate_sum(row, s_indices)
    n = calculate_sum(row, n_indices)
    t = calculate_sum(row, t_indices)
    f = calculate_sum(row, f_indices)
    j = calculate_sum(row, j_indices)
    p = calculate_sum(row, p_indices)

    preferences = row[preference_index].split(",") if row[preference_index] else [None, None, None]
    preference_1 = preferences[0].strip() if len(preferences) > 0 else None
    preference_2 = preferences[1].strip() if len(preferences) > 1 else None
    preference_3 = preferences[2].strip() if len(preferences) > 2 else None

    return [name, gender, wissen, e, i, s, n, t, f, j, p, preference_1, preference_2, preference_3]

def process_csv(input_csv, output_csv):
    with open(input_csv, mode='r', encoding='utf-8') as infile, open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        new_header = [
            "Bitte gib deinen Namen an:", "Bitte gib dein Geschlecht an:", "Wissen",
            "E", "I", "S", "N", "T", "F", "J", "P",
            "preference_1", "preference_2", "preference_3"
        ]
        writer.writerow(new_header)

        for row in reader:
            new_row = process_row(row)
            writer.writerow(new_row)

