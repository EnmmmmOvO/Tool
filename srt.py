import re
from datetime import datetime, timedelta

# Open original and new SRT files
with open('1_1_otter_ai.srt', 'r') as f_in, open('shifted1.srt', 'w') as f_out:
    # Define the time shift (90 minutes)
    time_shift = timedelta(minutes=90)

    # Starting index
    index = 620

    # Regex to match SRT timestamps
    timestamp_regex = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")

    for line in f_in:
        # Check if line is index
        if line.strip().isdigit():
            # Increment index and write new index to file
            index += 1
            f_out.write(f"{index}\n")
        else:
            match = timestamp_regex.match(line)
            if match:
                # Extract start and end timestamps
                start, end = match.groups()

                # Convert to datetime objects
                start_time = datetime.strptime(start, "%H:%M:%S,%f")
                end_time = datetime.strptime(end, "%H:%M:%S,%f")

                # Add time shift
                start_time_shifted = start_time + time_shift
                end_time_shifted = end_time + time_shift

                # Write shifted timestamps to new SRT file
                f_out.write(f"{start_time_shifted.strftime('%H:%M:%S,%f')[:-3]} --> {end_time_shifted.strftime('%H:%M:%S,%f')[:-3]}\n")
            else:
                # Write line to new SRT file without modification
                f_out.write(line)
