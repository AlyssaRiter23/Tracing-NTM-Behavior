import pandas as pd
import re
# path the the file and function to write txt file as a csv file
def parse_file_to_table(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # split sections by 'Input string' as this determines what goes into each row
    sections = content.strip().split("\nInput string:")
    
    data = []
    for section in sections:
        if not section.strip():
            continue
        
        # extract basic info using regular expressions 
        input_match = re.search(r"Input string:\s*(.*)", section)
        machine_match = re.search(r"Machine Name:\s*(.*)", section)
        accepted_match = re.search(r"(String accepted|Input rejected).*", section)
        transitions_match = re.search(r"in\s*(\d+)\s*transitions", section)
        depth_match = re.search(r"Depth of tree:\s*(\d+)", section)
        configs_match = re.search(r"Configurations explored:\s*(\d+)", section)
        nondet_match = re.search(r"Average Non-determinism:\s*([\d.]+)", section)
        
        input_string = input_match.group(1) if input_match else None
        machine_name = machine_match.group(1) if machine_match else None
        result = accepted_match.group(0) if accepted_match else None
        transitions = int(transitions_match.group(1)) if transitions_match else None
        depth = int(depth_match.group(1)) if depth_match else None
        configs = int(configs_match.group(1)) if configs_match else None
        nondet = float(nondet_match.group(1)) if nondet_match else None
        
        data.append({
            "Input String": input_string,
            "Machine Name": machine_name,
            "Result": result,
            "Transitions": transitions,
            "Tree Depth": depth,
            "Configurations Explored": configs,
            "Average Non-determinism": nondet,
        })
    
    # convert to a DataFrame
    df = pd.DataFrame(data)
    return df

# path to file
file_path = "output.txt"
table = parse_file_to_table(file_path)

# display the table to the terminal 
print(table)

# save to CSV 
table.to_csv("table_NTM.csv", index=False)