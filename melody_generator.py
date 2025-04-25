import random
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from music21 import scale, meter, stream, note, midi
import customtkinter as ctk

# ------------------ Core Functions ------------------ #
def get_scale(key):
    """Get the notes of a scale for the given key."""
    if 'minor' in key.lower():
        sc = scale.MinorScale(key.split()[0])
    else:
        sc = scale.MajorScale(key.split()[0])
    return [p.nameWithOctave for p in sc.getPitches()]

def generate_melody(key, time_signature, notes_per_2bars):
    """Generate a random melody based on user input."""
    scale_notes = get_scale(key)
    numerator, denominator = map(int, time_signature.split('/'))
    total_duration = 2 * numerator  # total duration for 2 bars (in quarter notes)

    start_times = []
    current_time = 0.0
    for _ in range(notes_per_2bars):
        space = (total_duration / notes_per_2bars) * random.uniform(0.5, 1.5)
        current_time += space
        start_times.append(current_time)

    scaling_factor = total_duration / max(start_times)
    start_times = [t * scaling_factor for t in start_times]

    melody_stream = stream.Stream()
    melody_stream.timeSignature = meter.TimeSignature(time_signature)

    for i in range(len(start_times)):
        note_pitch = random.choice(scale_notes)
        note_velocity = random.randint(64, 127)
        duration = (start_times[i + 1] - start_times[i]
                    if i < len(start_times) - 1 else total_duration - start_times[i])
        n = note.Note(note_pitch)
        n.volume.velocity = note_velocity
        n.duration.quarterLength = duration
        melody_stream.insert(start_times[i], n)

    return melody_stream

def get_unique_filename(base_filename, output_folder):
    """Generate a unique filename in the specified output folder."""
    filename, ext = os.path.splitext(base_filename)
    counter = 1
    while True:
        new_filename = f"{filename}_{counter}{ext}" if counter > 1 else f"{filename}{ext}"
        full_path = os.path.join(output_folder, new_filename)
        if not os.path.exists(full_path):
            return full_path
        counter += 1

def export_midi(melody_stream, base_filename, output_folder):
    """Export the melody as a MIDI file in the specified folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    unique_filename = get_unique_filename(base_filename, output_folder)
    melody_stream.write('midi', fp=unique_filename)
    return unique_filename

# ------------------ GUI Helper Functions ------------------ #
def browse_folder_control():
    folder = filedialog.askdirectory()
    if folder:
        control_output_entry.delete(0, tk.END)
        control_output_entry.insert(0, folder)

def browse_folder_random():
    folder = filedialog.askdirectory()
    if folder:
        random_output_entry.delete(0, tk.END)
        random_output_entry.insert(0, folder)

# ------------------ Generation Functions ------------------ #
def on_generate_control():
    """Generate melodies using user-specified inputs (Control Mode)."""
    try:
        key = key_entry.get()
        time_signature = time_signature_entry.get()
        notes_per_2bars = int(notes_entry.get())
        quantity = int(quantity_entry.get())
        output_folder = control_output_entry.get()

        if not output_folder:
            raise ValueError("Output folder must be specified")
        if not 1 <= quantity <= 50:
            raise ValueError("Quantity must be between 1 and 50")

        generated_count = 0
        for _ in range(quantity):
            melody_stream = generate_melody(key, time_signature, notes_per_2bars)
            base_filename = f"{key.replace(' ', '_')}_melody.mid"
            export_midi(melody_stream, base_filename, output_folder)
            generated_count += 1

        messagebox.showinfo("Success", f"Successfully generated {generated_count} melodies in:\n{output_folder}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_generate_random():
    """Generate melodies with random key, time signature, and note count for each melody."""
    try:
        quantity = int(random_quantity_entry.get())
        output_folder = random_output_entry.get()

        if not output_folder:
            raise ValueError("Output folder must be specified")
        if not 1 <= quantity <= 50:
            raise ValueError("Quantity must be between 1 and 50")

        keys = ["C Major", "G Major", "D Major", "A Major", "E Major", "F Major",
                "Bb Major", "Ab Major", "C Minor", "A Minor", "D Minor", "E Minor"]
        time_signatures = ["4/4", "3/4", "6/8", "2/4"]

        generated_count = 0
        for _ in range(quantity):
            key = random.choice(keys)
            time_signature = random.choice(time_signatures)
            notes_per_2bars = random.randint(4, 12)
            melody_stream = generate_melody(key, time_signature, notes_per_2bars)
            base_filename = f"{key.replace(' ', '_')}_melody.mid"
            export_midi(melody_stream, base_filename, output_folder)
            generated_count += 1

        messagebox.showinfo("Success", f"Successfully generated {generated_count} melodies in:\n{output_folder}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ------------------ Navigation ------------------ #
def show_control():
    random_frame.forget()
    control_frame.pack(fill="both", expand=True)
    control_nav_button.configure(fg_color="#4e4e4e", text_color="#ffffff")
    random_nav_button.configure(fg_color="#4e4e4e", text_color="#ffffff")

def show_random():
    control_frame.forget()
    random_frame.pack(fill="both", expand=True)
    control_nav_button.configure(fg_color="#4e4e4e", text_color="#ffffff")
    random_nav_button.configure(fg_color="#4e4e4e", text_color="#ffffff")

# ------------------ Setup CustomTkinter ------------------ #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Melody Generator v1")
root.configure(bg="#2e2e2e")

# Create a big container box with rounded corners that will hold everything.
# Increase the overall window size by 15 pixels on each side via padding.
container = ctk.CTkFrame(root, fg_color="#2e2e2e", corner_radius=20)
container.pack(padx=15, pady=15, fill="both", expand=True)

# ------------------ Header ------------------ #
header_label = ctk.CTkLabel(container,
                            text="Melody Generator v1",
                            font=("Helvetica", 28, "bold"),
                            text_color="#ffffff",
                            bg_color="#2e2e2e")
header_label.pack(pady=(20, 10))

# ------------------ Navigation Bar ------------------ #
nav_frame = ctk.CTkFrame(container, fg_color="#2e2e2e", corner_radius=0)
nav_frame.pack(pady=(0, 10))
control_nav_button = ctk.CTkButton(nav_frame,
                                   text="Control",
                                   command=show_control,
                                   width=120,
                                   corner_radius=10,
                                   fg_color="#4e4e4e",
                                   text_color="#ffffff",
                                   font=("Helvetica", 20, "bold"))
control_nav_button.grid(row=0, column=0, padx=10)
random_nav_button = ctk.CTkButton(nav_frame,
                                  text="Random",
                                  command=show_random,
                                  width=120,
                                  corner_radius=10,
                                  fg_color="#4e4e4e",
                                  text_color="#ffffff",
                                  font=("Helvetica", 20, "bold"))
random_nav_button.grid(row=0, column=1, padx=10)
nav_frame.grid_columnconfigure(0, weight=1)
nav_frame.grid_columnconfigure(1, weight=1)

# ------------------ Control Mode ------------------ #
control_frame = ctk.CTkFrame(container, fg_color="#2e2e2e", corner_radius=0)
ctk.CTkLabel(control_frame,
             text="Key (e.g., 'C Major', 'A Minor'):",
             font=("Helvetica", 16, "bold"),
             text_color="#ffffff",
             bg_color="#2e2e2e").grid(row=0, column=0, padx=10, pady=10, sticky="w")
key_entry = ctk.CTkEntry(control_frame,
                         placeholder_text="C Major",
                         font=("Helvetica", 14),
                         corner_radius=8)
key_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkLabel(control_frame,
             text="Time Signature (e.g., '4/4'):",
             font=("Helvetica", 16, "bold"),
             text_color="#ffffff",
             bg_color="#2e2e2e").grid(row=1, column=0, padx=10, pady=10, sticky="w")
time_signature_entry = ctk.CTkEntry(control_frame,
                                    placeholder_text="4/4",
                                    font=("Helvetica", 14),
                                    corner_radius=8)
time_signature_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkLabel(control_frame,
             text="Notes per 2 Bars:",
             font=("Helvetica", 16, "bold"),
             text_color="#ffffff",
             bg_color="#2e2e2e").grid(row=2, column=0, padx=10, pady=10, sticky="w")
notes_entry = ctk.CTkEntry(control_frame,
                           placeholder_text="8",
                           font=("Helvetica", 14),
                           corner_radius=8)
notes_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkLabel(control_frame,
             text="Quantity (1-50):",
             font=("Helvetica", 16, "bold"),
             text_color="#ffffff",
             bg_color="#2e2e2e").grid(row=3, column=0, padx=10, pady=10, sticky="w")
quantity_entry = ctk.CTkEntry(control_frame,
                              placeholder_text="1",
                              font=("Helvetica", 14),
                              corner_radius=8)
quantity_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkLabel(control_frame,
             text="Output Folder:",
             font=("Helvetica", 16, "bold"),
             text_color="#ffffff",
             bg_color="#2e2e2e").grid(row=4, column=0, padx=10, pady=10, sticky="w")
control_output_entry = ctk.CTkEntry(control_frame,
                                    placeholder_text="Select folder",
                                    font=("Helvetica", 14),
                                    corner_radius=8)
control_output_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
browse_btn_control = ctk.CTkButton(control_frame,
                                   text="Browse",
                                   command=browse_folder_control,
                                   corner_radius=8,
                                   fg_color="#4e4e4e",
                                   text_color="#ffffff",
                                   font=("Helvetica", 14, "bold"))
browse_btn_control.grid(row=4, column=2, padx=10, pady=10)
generate_btn_control = ctk.CTkButton(control_frame,
                                     text="Generate Melodies",
                                     command=on_generate_control,
                                     font=("Helvetica", 16, "bold"),
                                     corner_radius=10,
                                     fg_color="#4e4e4e",
                                     text_color="#ffffff")
generate_btn_control.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
control_frame.columnconfigure(1, weight=1)
control_frame.pack(fill="both", expand=True)

# ------------------ Random Mode ------------------ #
random_frame = ctk.CTkFrame(container, fg_color="#2e2e2e", corner_radius=0)
ctk.CTkLabel(random_frame,
             text="Quantity (1-50):",
             font=("Helvetica", 16, "bold"),
             text_color="#ffffff",
             bg_color="#2e2e2e").grid(row=0, column=0, padx=10, pady=10, sticky="w")
random_quantity_entry = ctk.CTkEntry(random_frame,
                                     placeholder_text="1",
                                     font=("Helvetica", 14),
                                     corner_radius=8)
random_quantity_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
ctk.CTkLabel(random_frame,
             text="Output Folder:",
             font=("Helvetica", 16, "bold"),
             text_color="#ffffff",
             bg_color="#2e2e2e").grid(row=1, column=0, padx=10, pady=10, sticky="w")
random_output_entry = ctk.CTkEntry(random_frame,
                                   placeholder_text="Select folder",
                                   font=("Helvetica", 14),
                                   corner_radius=8)
random_output_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
browse_btn_random = ctk.CTkButton(random_frame,
                                  text="Browse",
                                  command=browse_folder_random,
                                  corner_radius=8,
                                  fg_color="#4e4e4e",
                                  text_color="#ffffff",
                                  font=("Helvetica", 14, "bold"))
browse_btn_random.grid(row=1, column=2, padx=10, pady=10)
generate_btn_random = ctk.CTkButton(random_frame,
                                    text="Generate Melodies",
                                    command=on_generate_random,
                                    font=("Helvetica", 16, "bold"),
                                    corner_radius=10,
                                    fg_color="#4e4e4e",
                                    text_color="#ffffff")
generate_btn_random.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
random_frame.columnconfigure(1, weight=1)

# Show Control mode by default
control_frame.tkraise()

# ------------------ Resize Window to Fit Contents ------------------ #
root.update_idletasks()
req_width = root.winfo_reqwidth()
req_height = root.winfo_reqheight() + 30  # add extra 30 pixels vertically
root.geometry(f"{req_width}x{req_height}")

root.mainloop()
