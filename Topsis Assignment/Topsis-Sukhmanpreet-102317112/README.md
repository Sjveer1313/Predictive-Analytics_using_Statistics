# Topsis-Sukhmanpreet-102317112

--- 

## What is TOPSIS?

TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) is a multi-criteria decision-making method. It ranks a set of alternatives by identifying the solution that is closest to the Ideal Best and farthest from the Ideal Worst.

---

## Installation
You can install this package via PyPi:

Bash
``` pip install Topsis-Sukhmanpreet-102317112 ```

Usage
The package can be executed directly from the command line:

Bash
``` python <program.py> <InputDataFile> <Weights> <Impacts> <OutputResultFileName>```

Example
Bash
```python topsis.py data.csv "1,1,1,1,1" "+,+,+,+,+" result.csv```

---

## Input Requirements

File Format: The input file must be a .csv.

Structure: The file must contain three or more columns.

Data Type: From the 2nd column to the last, all values must be numeric.

Parameters:
 - Weights: Must be numeric and separated by commas.
 - Impacts: Must be either + (for maximization) or - (for minimization), separated by commas.
 - Matching: The number of weights, impacts, and numeric columns must be identical.

Error Handling
 - The package includes robust validation and will show appropriate messages for:
 - Incorrect number of parameters.
 - "File Not Found" exceptions.
 - Non-numeric values in criteria columns.
 - Mismatch between weights, impacts, and criteria count.

Output
 - The result is saved as a new .csv file containing all original data plus two additional columns:

Topsis Score: The calculated performance score.

Rank: The final ranking of the alternatives.

---

## License

© 2026 Sukhmanpreet Singh

This repository is licensed under the MIT license.
See LICENSE for  details.