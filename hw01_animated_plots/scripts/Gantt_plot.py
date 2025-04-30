import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib import patches
from matplotlib.backends.backend_pdf import PdfPages


event_abbreviations = {
    "Final deadline for submitting course withdrawal requests": "Final WD Deadline",
    "Final deadline for winter semester course withdrawal": "Winter WD Deadline",
    "Final deadline for submitting course withdrawal requests - summer": "Summer WD Deadline",
    "Final deadline for summer semester course withdrawal": "Summer WD Deadline",
    "Registration period for spring semester courses 2025/2026": "Spring Reg. Period",
    "Registration period for winter semester courses and full-year courses 2026/2027": "Winter Reg. Period",
    "Period for making all individual decisions on winter semester 2025/2026 completion": "Winter Decision Period",
    "Period for making all individual decisions on academic year 2025/2026 completion": "Yearly Decision Period",
    "Written foreign language certification exams - summer": "Lang. Cert. Exams",
    "Written foreign language certification exams - retakes": "Lang. Cert. Retakes",
}

# Change full names to abbreviations
def abbreviate_task(task_name):
    return event_abbreviations.get(task_name, task_name)

events = [
    # Semester 1 (Winter)
    {"Task": "WINTER SEMESTER", "Start": "2025-10-01", "End": "2026-02-15", "Type": "Semester"},
    {"Task": "Teaching classes (block I)", "Start": "2025-10-02", "End": "2025-11-02", "Type": "Classes"},
    {"Task": "Final deadline for submitting course withdrawal requests", "Start": "2025-10-21", "End": "2025-10-21", "Type": "Deadline"},
    {"Task": "Teaching classes (block II)", "Start": "2025-11-03", "End": "2025-12-07", "Type": "Classes"},
    {"Task": "Registration period for spring semester courses 2025/2026", "Start": "2025-10-01", "End": "2026-02-15", "Type": "Registration"},
    {"Task": "Teaching classes (block III)", "Start": "2025-12-08", "End": "2025-12-21", "Type": "Classes"},
    {"Task": "Winter holidays", "Start": "2025-12-22", "End": "2026-01-06", "Type": "Holiday"},
    {"Task": "Teaching classes (block III cont.)", "Start": "2026-01-07", "End": "2026-01-25", "Type": "Classes"},
    {"Task": "No classes (academic year inauguration)", "Start": "2025-10-01", "End": "2025-10-01", "Type": "No Classes"},
    {"Task": "No classes", "Start": "2025-11-10", "End": "2025-11-10", "Type": "No Classes"},
    {"Task": "Final deadline for winter semester course withdrawal", "Start": "2026-01-16", "End": "2026-01-16", "Type": "Deadline"},
    {"Task": "Winter examination session", "Start": "2026-01-26", "End": "2026-02-08", "Type": "Exams"},
    {"Task": "Written foreign language certification exams", "Start": "2026-01-26", "End": "2026-01-27", "Type": "Exams"},
    {"Task": "Inter-semester break", "Start": "2026-02-09", "End": "2026-02-15", "Type": "Break"},
    
    # Semester 2 (Summer)
    {"Task": "SUMMER SEMESTER", "Start": "2026-02-16", "End": "2026-09-30", "Type": "Semester"},
    {"Task": "Teaching classes (block I) - summer", "Start": "2026-02-23", "End": "2026-03-22", "Type": "Classes"},
    {"Task": "Winter semester retake exam session", "Start": "2026-02-16", "End": "2026-02-21", "Type": "Exams"},
    {"Task": "Written English B2 certification exams", "Start": "2026-02-21", "End": "2026-02-21", "Type": "Exams"},
    {"Task": "Period for making all individual decisions on winter semester 2025/2026 completion", "Start": "2026-03-02", "End": "2026-03-29", "Type": "Admin"},
    {"Task": "Final deadline for submitting course withdrawal requests - summer", "Start": "2026-03-13", "End": "2026-03-13", "Type": "Deadline"},
    {"Task": "Teaching classes (block II) - summer", "Start": "2026-03-23", "End": "2026-05-03", "Type": "Classes"},
    {"Task": "Spring holidays", "Start": "2026-04-02", "End": "2026-04-07", "Type": "Holiday"},
    {"Task": "Teaching classes (block III) - summer", "Start": "2026-05-04", "End": "2026-06-14", "Type": "Classes"},
    {"Task": "No classes - May", "Start": "2026-05-02", "End": "2026-05-02", "Type": "No Classes"},
    {"Task": "No classes (Student Festival)", "Start": "2026-05-08", "End": "2026-05-09", "Type": "No Classes"},
    {"Task": "No classes - June", "Start": "2026-06-05", "End": "2026-06-05", "Type": "No Classes"},
    {"Task": "Final deadline for summer semester course withdrawal", "Start": "2026-05-31", "End": "2026-05-31", "Type": "Deadline"},
    {"Task": "Registration period for winter semester courses and full-year courses 2026/2027", "Start": "2026-06-01", "End": "2026-09-30", "Type": "Registration"},
    {"Task": "Summer examination session", "Start": "2026-06-15", "End": "2026-06-28", "Type": "Exams"},
    {"Task": "Written foreign language certification exams - summer", "Start": "2026-06-08", "End": "2026-06-09", "Type": "Exams"},
    {"Task": "Summer holidays", "Start": "2026-06-29", "End": "2026-09-30", "Type": "Holiday"},
    {"Task": "Summer block I", "Start": "2026-07-06", "End": "2026-08-07", "Type": "Summer Block"},
    {"Task": "Summer block II", "Start": "2026-08-17", "End": "2026-09-11", "Type": "Summer Block"},
    {"Task": "Summer semester retake exam session", "Start": "2026-08-31", "End": "2026-09-13", "Type": "Exams"},
    {"Task": "Written foreign language certification exams - retakes", "Start": "2026-08-31", "End": "2026-09-01", "Type": "Exams"},
    {"Task": "Period for making all individual decisions on academic year 2025/2026 completion", "Start": "2026-09-14", "End": "2026-09-30", "Type": "Admin"}
]

# If task is in event_abbreviations, use abbreviation, otherwise use full name
for event in events:
    if event["Task"] in event_abbreviations:
        event["DisplayTask"] = event_abbreviations[event["Task"]]
        event["AbbreviatedTask"] = event["Task"]  # Store the original task for the legend
    else:
        event["DisplayTask"] = event["Task"]
        event["AbbreviatedTask"] = None  # No abbreviation

df = pd.DataFrame(events)

# Convert to datetime
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])

# Calculate duration in days
df['Duration'] = (df['End'] - df['Start']).dt.days + 1

# Assign unique index to each task for y-axis positioning
df['TaskID'] = range(1, len(df) + 1)

# Sort events 
df = df.sort_values(by=['Start', 'Type'])

# Define colors for each event type
color_dict = {
    'Semester': '#E6F3FF',      # Light blue
    'Classes': '#4CAF50',       # Green
    'Deadline': '#F44336',      # Red
    'Registration': '#42A5F5',  # Blue
    'Holiday': '#FFC107',       # Yellow
    'No Classes': '#9C27B0',    # Purple
    'Exams': '#FF5722',         # Orange
    'Break': '#607D8B',         # Grey
    'Admin': '#795548',         # Brown
    'Summer Block': '#8BC34A'   # Light green
}

# Define grayscale colors for each event type
gray_dict = {
    'Semester': '#F5F5F5',      # Very light gray
    'Classes': '#A0A0A0',       # Medium gray
    'Deadline': '#2A2A2A',      # Very dark gray
    'Registration': '#B8B8B8',  # Light medium gray
    'Holiday': '#D9D9D9',       # Light gray
    'No Classes': '#6B6B6B',    # Dark gray
    'Exams': '#3D3D3D',         # Dark gray 2
    'Break': '#919191',         # Medium gray 2
    'Admin': '#575757',         # Medium dark gray
    'Summer Block': '#C5C5C5'   # Light gray 2
}

# Create a list to store 2 color versions of the chart
versions = [
    {"name": "color", "colors": color_dict, "filename": "academic_calendar_color.pdf"},
    {"name": "bw", "colors": gray_dict, "filename": "academic_calendar_bw.pdf"}
]

# A4 dimensions in inches
a4_width_inches, a4_height_inches = 11.69, 8.27

legend_labels = {abbr: full for full, abbr in event_abbreviations.items() if abbr in [event["AbbreviatedTask"] for event in events]}

def create_gantt_chart(version):
    height = 0.8
    
    f, ax = plt.subplots(figsize=(a4_width_inches, a4_height_inches))
    
    # Legend for event types
    event_type_patches = []
    for event_type, color in version["colors"].items():
        patch = patches.Patch(
            facecolor=color, 
            edgecolor='black',
            label=event_type,
        )
        event_type_patches.append(patch)
    
    # Dictionary to track only abbreviated task handles for legend
    abbreviation_legend_entries = {}
    
    for idx, row in df.iterrows():
        task_id = row['TaskID']
        y0 = task_id - height / 2
        x0 = row.Start
        width = row.End - x0
        event_type = row.Type
        display_task = row.DisplayTask  # either the abbreviation or full name
        full_task = row.Task
        abbreviated_task = row.AbbreviatedTask  # Original task name if abbreviated

        if not width:
            width = pd.Timedelta(days=0.5)

        # Create the rectangle with appropriate color
        rect = patches.Rectangle(
            (x0, y0), width, height,
            facecolor=version["colors"][event_type],
            edgecolor='black',
            linewidth=0.5,
            label=full_task  # Use full task name for label
        )
        
        # Add to plot
        ax.add_patch(rect)
        
        # Store for abbreviation legend
        if abbreviated_task is not None:
            abbreviation_legend_entries[full_task] = rect

        # Add task name inside all bars
        mid_x = x0 + width / 2
        mid_y = y0 + height / 2
        
        # Fit text in the bar
        plt.text(mid_x, mid_y, display_task, horizontalalignment='center', verticalalignment='center', fontsize=7)

    # Format the x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# This ensures ALL tick labels get rotated correctly
    for label in ax.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment('right')

    # Add vertical month lines
    start_date = df.Start.min()
    end_date = df.End.max()
    current = start_date.replace(day=1)
    while current <= end_date:
        next_month = current.replace(day=28) + timedelta(days=4)
        next_month = next_month.replace(day=1)
        ax.axvline(x=current, color='gray', linestyle='-', linewidth=0.5)
        current = next_month

    # Chart title and labels
    ax.set_title('Academic Year Schedule 2025/2026', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=10, fontweight='bold')
    
    # Set y-axis range and remove tick labels
    ax.set_yticks([])  # No tick marks
    ax.set_ylim(0, len(df) + 1)
    
    # Add horizontal grid lines
    for i in range(1, len(df) + 1):
        ax.axhline(y=i, color='gray', linestyle='-', linewidth=0.2)
    
    event_type_leg = ax.legend(handles=event_type_patches, loc='lower right', ncol=5, fontsize=6)
    
    # Add the abbreviation legend on the same page
    ax.add_artist(event_type_leg)
    
    if abbreviation_legend_entries:        
        # Sort legend entries alphabetically
        sorted_abbr_tasks = sorted(abbreviation_legend_entries.keys())
        sorted_abbr_patches = [abbreviation_legend_entries[task] for task in sorted_abbr_tasks]
        
        # Create the legend with abbreviated task names and their full names
        abbr_labels = [f"{event_abbreviations[task]} - {task}" for task in sorted_abbr_tasks]
        
        abbr_legend = ax.legend(
            handles=sorted_abbr_patches,
            labels=abbr_labels,
            loc='upper left',
            title="Abbreviations Legend",
            fontsize=6
        )
        
        plt.tight_layout()
        
        # Save to PDF
        with PdfPages(version["filename"]) as pdf:
            pdf.savefig(f, bbox_inches='tight')
    
    plt.close(f)

# Create both versions of the chart
for version in versions:
    create_gantt_chart(version)