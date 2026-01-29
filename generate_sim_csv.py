
import csv

log_file = r"D:/VLSI/Traffic light controller\simulation/modelsim/msim_transcript"
csv_file = r"D:/VLSI/Traffic light controller/sim_data.csv"

data_lines = []
capture = False

with open(log_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith("# TIME | STATE | TIMER | NS | EW"):
            capture = True
            continue
        if line.startswith("# ** Note: $stop"):
            capture = False
        if capture:
            if line.startswith("#"):
                line_data = line[1:].strip()  # remove leading #
                parts = [p.strip() for p in line_data.split('|')]
                if len(parts) == 5:
                    data_lines.append(parts)

# Write to CSV
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['TIME', 'STATE', 'TIMER', 'NS', 'EW'])
    writer.writerows(data_lines)

print(f"CSV generated with {len(data_lines)} rows at: {csv_file}")
