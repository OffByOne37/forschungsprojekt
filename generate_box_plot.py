import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Step 1: Read the CSV files
file1 = 'students_data_zufriedenheit_1.csv'
file2 = 'students_data_zufriedenheit_2.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Convert numerical columns to int
for col in df1.columns[1:]:
    df1[col] = pd.to_numeric(df1[col], errors='coerce')
    df2[col] = pd.to_numeric(df2[col], errors='coerce')

# Step 2: Combine the dataframes for comparison
df1['Group'] = 'Auto. Zuordnung'
df2['Group'] = 'Freie Zuordnung'

combined_df = pd.concat([df1, df2])

# Remove the 'Zeitstempel' column for analysis
questions = df1.columns[1:-1]  # Adjust depending on the exact structure

# Step 3: Perform statistical tests
significant_diffs = []

for question in questions:
    t_stat, p_value = ttest_ind(df1[question], df2[question], nan_policy='omit')
    significant_diffs.append((question, p_value))

# Step 4: Create boxplots for each question and highlight significant differences
plt.figure(figsize=(20, 10))

for i, (question, p_value) in enumerate(significant_diffs, 1):
    plt.subplot(2, len(questions) // 2, i)
    sns.boxplot(x='Group', y=question, data=combined_df)
    plt.title(f'Question {i}')
    plt.xlabel('')
    plt.ylabel('')
    if p_value < 0.05:
        plt.gca().spines['top'].set_color('red')
        plt.gca().spines['top'].set_linewidth(2)
        plt.gca().spines['bottom'].set_color('red')
        plt.gca().spines['bottom'].set_linewidth(2)
        plt.gca().spines['left'].set_color('red')
        plt.gca().spines['left'].set_linewidth(2)
        plt.gca().spines['right'].set_color('red')
        plt.gca().spines['right'].set_linewidth(2)

plt.tight_layout()
plt.show()

# Highlight significant differences in the console
for question, p_value in significant_diffs:
    if p_value < 0.05:
        print(f'There is a significant difference in {question} (p-value = {p_value})')

# Optionally, if you want to save the results to a CSV file
results_df = pd.DataFrame(significant_diffs, columns=['Question', 'P-Value'])
results_df.to_csv('significant_differences.csv', index=False)
