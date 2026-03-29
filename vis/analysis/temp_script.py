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

    # Identify categorical variables based on documentation
    categorical_vars = {
        'intmonth', 'stfips', 'grade92', 'race', 'ethnic', 'sex', 
        'marital', 'chldpres', 'prcitshp', 'state', 'ind02', 
        'occ2012', 'class', 'unionmme', 'unioncov', 'lfsr94'
    }

    import calendar
    month_to_num = {name: num for num, name in enumerate(calendar.month_name) if name}
    num_to_month = {num: name for num, name in enumerate(calendar.month_name) if name}

    stats = []
    for col in df.columns:
        col_data = df[col]
        is_categorical = col in categorical_vars
        
        # Determine display type
        dtype = str(col_data.dtype)
        display_type = "Categorical" if is_categorical else dtype
        
        coverage = col_data.notna().mean() * 100
        
        # Special handling for 'intmonth'
        is_month = col == 'intmonth'
        if is_month:
            calc_data = col_data.map(month_to_num)
        else:
            calc_data = col_data

        # Numeric stats
        if np.issubdtype(calc_data.dtype, np.number):
            v_min = calc_data.min()
            v_max = calc_data.max()
            v_mean = calc_data.mean() if not is_categorical else "N/A"
        else:
            v_min = calc_data.min() if not is_categorical else "N/A"
            v_max = calc_data.max() if not is_categorical else "N/A"
            v_mean = "N/A"
        
        # Mode
        mode_val = calc_data.mode()
        v_mode = mode_val[0] if not mode_val.empty else "N/A"
        
        # For intmonth, we convert min/max/mode back to names for the stats record
        if is_month:
            if isinstance(v_min, (int, float, np.integer, np.floating)) and not np.isnan(v_min):
                v_min = num_to_month.get(int(v_min), v_min)
            if isinstance(v_max, (int, float, np.integer, np.floating)) and not np.isnan(v_max):
                v_max = num_to_month.get(int(v_max), v_max)
            if isinstance(v_mode, (int, float, np.integer, np.floating)) and not np.isnan(v_mode):
                v_mode = num_to_month.get(int(v_mode), v_mode)

        stats.append({
            'varname': col,
            'label': labels_map.get(col, col),
            'type': display_type,
            'coverage': f"{coverage:.2f}%",
            'min': v_min,
            'max': v_max,
            'mean': v_mean,
            'mode': v_mode
        })

    # Generate Markdown table
    md_lines = [
        "# Variable Dictionary - CPS MORG 2014 (California)",
        "",
        "| Varname | Label | Type | Coverage | Min | Max | Mean | Mode |",
        "|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|"
    ]

    for s in stats:
        def fmt(val):
            if val == "N/A":
                return "N/A"
            if isinstance(val, (int, float, np.integer, np.floating)):
                if np.isnan(val): return "N/A"
                return f"{val:.2f}".rstrip('0').rstrip('.')
            return str(val)

        row = [
            s['varname'],
            s['label'],
            s['type'],
            s['coverage'],
            fmt(s['min']),
            fmt(s['max']),
            fmt(s['mean']),
            fmt(s['mode'])
        ]
        md_lines.append(f"| {' | '.join(row)} |")

    # Save to file
    with open(output_md, 'w') as f:
        f.write("\n".join(md_lines))
    
    print(f"Successfully created {output_md}")

if __name__ == "__main__":
    create_dictionary('data/morg-2014-emp-state5.csv', 'variable_dictionary_detailed.md')
