import sys
import pandas as pd
import numpy as np
import os

def main():
    # 1. Check for correct number of parameters
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters.")
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
        return

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]

    # 2. Handling "File not Found" exception
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    try:
        # Load the dataset
        data = pd.read_csv(input_file)

        # 3. Input file must contain three or more columns
        if data.shape[1] < 3:
            print("Error: Input file must contain three or more columns (ID + at least 2 criteria).")
            return

        # 4. From 2nd to last columns must contain numeric values only
        for col in data.columns[1:]:
            if not np.issubdtype(data[col].dtype, np.number):
                print(f"Error: Column '{col}' contains non-numeric values.")
                return

        # 5. Parse weights and impacts
        try:
            weights = [float(w) for w in weights_str.split(',')]
        except ValueError:
            print("Error: Weights must be numeric and separated by commas.")
            return

        impacts = impacts_str.split(',')

        # 6. Check if number of weights, impacts, and numeric columns are the same
        num_criteria = data.shape[1] - 1
        if len(weights) != num_criteria or len(impacts) != num_criteria:
            print(f"Error: Expected {num_criteria} weights and impacts, but received {len(weights)} weights and {len(impacts)} impacts.")
            return

        # 7. Impacts must be either + or -
        if not all(i in ['+', '-'] for i in impacts):
            print("Error: Impacts must be either '+' or '-'.")
            return

        # --- TOPSIS ALGORITHM ---
        # Extract numeric criteria
        matrix = data.iloc[:, 1:].values.astype(float)

        # Step 1: Normalize the matrix
        norm_matrix = matrix / np.sqrt((matrix**2).sum(axis=0))

        # Step 2: Calculate weighted normalized matrix
        weighted_matrix = norm_matrix * weights

        # Step 3: Identify ideal best and ideal worst
        ideal_best = []
        ideal_worst = []
        for i in range(len(impacts)):
            if impacts[i] == '+':
                ideal_best.append(max(weighted_matrix[:, i]))
                ideal_worst.append(min(weighted_matrix[:, i]))
            else:
                ideal_best.append(min(weighted_matrix[:, i]))
                ideal_worst.append(max(weighted_matrix[:, i]))

        # Step 4: Calculate Euclidean distances from ideal best and worst
        s_best = np.sqrt(((weighted_matrix - ideal_best)**2).sum(axis=1))
        s_worst = np.sqrt(((weighted_matrix - ideal_worst)**2).sum(axis=1))

        # Step 5: Calculate Topsis Score
        scores = s_worst / (s_best + s_worst)

        # Step 6: Assign Score and Rank to the dataframe
        data['Topsis Score'] = scores
        data['Rank'] = data['Topsis Score'].rank(ascending=False).astype(int)

        # Save to output file
        data.to_csv(output_file, index=False)
        print(f"Success: Results saved to {output_file}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

