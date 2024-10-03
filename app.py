from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

# Load the Excel sheet with summaries (filtered_final_output.xlsx)
df = pd.read_excel('filtered_final_output.xlsx')

# Initialize a DataFrame to store evaluations
evaluation_data = []

# Define the rubric labels (corresponding to the rubric criteria)
rubric_columns = ['Summary Accuracy', 'Content Coverage', 'Conciseness', 'Coherence', 'Abstraction', 'Comments']

@app.route('/')
def index():
    # Show the first summary for evaluation
    return render_template('index.html', summary=df.iloc[0]['Summary'], entry_id=0)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    accuracy = request.form['accuracy']
    content_coverage = request.form['content_coverage']
    conciseness = request.form['conciseness']
    coherence = request.form['coherence']
    abstraction = request.form['abstraction']
    comments = request.form['comments']
    entry_id = int(request.form['entry_id'])
    
    # Store the evaluation in the evaluation_data list
    evaluation_data.append([accuracy, content_coverage, conciseness, coherence, abstraction, comments])
    
    # Check if there are more summaries to evaluate
    if entry_id + 1 < len(df):
        next_summary = df.iloc[entry_id + 1]['Summary']
        return render_template('index.html', summary=next_summary, entry_id=entry_id + 1)
    else:
        # Save evaluations to an Excel file after all summaries are evaluated
        evaluation_df = pd.DataFrame(evaluation_data, columns=rubric_columns)
        evaluation_df.to_excel('evaluation_results.xlsx', index=False)
        return "Evaluations are complete and saved to evaluation_results.xlsx"

if __name__ == '__main__':
    app.run(debug=True)
