from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Example orthopaedic surgeries
surgeries = [
    {"id": 1, "duration": 120, "surgeon": "Dr. Smith", "type": "Orthopaedic"},
    {"id": 2, "duration": 90,  "surgeon": "Dr. Lee",   "type": "Orthopaedic"},
    {"id": 3, "duration": 60,  "surgeon": "Dr. Smith", "type": "Orthopaedic"},
    {"id": 4, "duration": 180, "surgeon": "Dr. Patel", "type": "Orthopaedic"},
    {"id": 5, "duration": 45,  "surgeon": "Dr. Lee",   "type": "Orthopaedic"},
]

# Only include orthopaedic surgeries
surgeries = [s for s in surgeries if s["type"] == "Orthopaedic"]

# Set up theatres and scheduling parameters
THEATRE_TIME = 540  # 9 hours
theatres = {"Theatre 1": [], "Theatre 2": []}

def schedule_surgeries(surgeries, theatres):
    surgeries = sorted(surgeries, key=lambda x: -x["duration"])
    remaining_time = {t: THEATRE_TIME for t in theatres}
    
    for s in surgeries:
        for t in theatres:
            if s["duration"] <= remaining_time[t]:
                theatres[t].append(s)
                remaining_time[t] -= s["duration"]
                break
        else:
            print(f"WARNING: Surgery {s['id']} could not be scheduled.")
    return theatres

# Schedule them
final_schedule = schedule_surgeries(surgeries, theatres)

# Plotting function with color gradient by duration
def plot_schedule_vertical(theatres):
    fig, ax = plt.subplots(figsize=(8, 6))
    x_ticks, x_labels = [], []
    x_pos = 0

    # Extract all durations for color scaling
    all_durations = [s["duration"] for lst in theatres.values() for s in lst]
    norm = mcolors.Normalize(vmin=min(all_durations), vmax=max(all_durations))
    cmap = cm.get_cmap("viridis")

    for theatre, surgeries in theatres.items():
        current_time = 0
        for s in surgeries:
            color = cmap(norm(s["duration"]))
            ax.broken_barh([(x_pos, 5)], (current_time, s["duration"]), facecolors=color)
            ax.text(x_pos + 2.5, current_time + s["duration"] / 2, 
                    f"ID {s['id']}\n{s['surgeon']}", 
                    va='center', ha='center', color='white', fontsize=8)
            current_time += s["duration"]
        x_ticks.append(x_pos + 2.5)
        x_labels.append(theatre)
        x_pos += 10

    ax.set_ylabel("Time (minutes from start of day)")
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels)
    ax.set_title("Orthopaedic Surgery Schedule (Color-Coded by Duration)")
    ax.set_ylim(0, THEATRE_TIME)
    ax.invert_yaxis()
    plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label="Duration (min)")
    plt.tight_layout()
    plt.show()

# Plot it
plot_schedule_vertical(final_schedule)
