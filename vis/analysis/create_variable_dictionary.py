import pandas as pd
import numpy as np

def create_dictionary(input_csv, output_md):
    # Load the dataset
    df = pd.read_csv(input_csv, low_memory=False)

    # Define short labels based on CPS documentation
    labels_map = {
        'hhid': 'Household ID',
        'intmonth': 'Interview Month',
        'stfips': 'State (FIPS/Alpha)',
        'weight': 'Earnings Weight',
        'earnwke': 'Weekly Earnings',
        'uhours': 'Usual Hours Worked',
        'grade92': 'Highest Education Level',
        'race': 'Race',
        'ethnic': 'Ethnicity/Hispanic Origin',
        'age': 'Age',
        'sex': 'Sex (1=M, 2=F)',
        'marital': 'Marital Status',
        'ownchild': 'Number of Own Children',
        'chldpres': 'Children Present in HH',
        'prcitshp': 'Citizenship Status',
        'state': 'Numeric State Code',
        'ind02': 'Industry Code (2002)',
        'occ2012': 'Occupation Code (2012)',
        'class': 'Worker Class',
        'unionmme': 'Union Member',
        'unioncov': 'Union Coverage',
        'lfsr94': 'Labor Force Status'
    }

    # Identify categorical variables and identifiers where math stats don't make sense
    categorical_vars = {
        'Unnamed: 0', 'hhid', 'intmonth', 'stfips', 'grade92', 'race', 'ethnic', 'sex', 
        'marital', 'chldpres', 'prcitshp', 'state', 'ind02', 
        'occ2012', 'class', 'unionmme', 'unioncov', 'lfsr94'
    }

    def fmt_val(val):
        if val == 'N/A':
            return 'N/A'
        if isinstance(val, (int, float, np.integer, np.floating)):
            if np.isnan(val): return 'N/A'
            return f'{val:.2f}'.rstrip('0').rstrip('.')
        return str(val)

    stats = []
    for col in df.columns:
        col_data = df[col]
        is_categorical = col in categorical_vars
        
        # Determine display type
        dtype = str(col_data.dtype)
        display_type = 'Categorical' if is_categorical else dtype
        if col == 'hhid' or col == 'Unnamed: 0':
            display_type = 'Identifier'
        
        coverage = col_data.notna().mean() * 100
        
        # Mode is always useful
        mode_val = col_data.mode()
        v_mode = mode_val[0] if not mode_val.empty else 'N/A'

        # Range and Mean - only if not categorical/identifier
        if not is_categorical and np.issubdtype(col_data.dtype, np.number):
            v_min = col_data.min()
            v_max = col_data.max()
            v_range = f'{fmt_val(v_min)} - {fmt_val(v_max)}'
            v_mean = col_data.mean()
        else:
            v_range = 'N/A'
            v_mean = 'N/A'

        stats.append({
            'varname': col,
            'label': labels_map.get(col, col),
            'type': display_type,
            'coverage': f'{coverage:.2f}%',
            'range': v_range,
            'mean': v_mean,
            'mode': v_mode
        })

    # Generate Markdown table
    md_lines = [
        '# Variable Dictionary - CPS MORG 2014 (California)',
        '',
        '| Varname | Label | Type | Coverage | Range | Mean | Mode |',
        '|:---|:---|:---|:---:|:---:|:---:|:---:|'
    ]

    for s in stats:
        row = [
            s['varname'],
            s['label'],
            s['type'],
            s['coverage'],
            s['range'],
            fmt_val(s['mean']),
            fmt_val(s['mode'])
        ]
        md_lines.append(f'| {" | ".join(row)} |')

    # Save to file
    with open(output_md, "w") as f:
        f.write("\n".join(md_lines))
    
    print(f"Successfully created {output_md}")

if __name__ == "__main__":
    create_dictionary('data/morg-2014-emp-state5.csv', 'variable_dictionary_detailed.md')
