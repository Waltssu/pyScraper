import tkinter as tk
from tkinter import scrolledtext, filedialog, font
from pyScraper import scrape_events_within_days, url
from create_ics import save_events_to_ics_file

def run_scraper(days=None):
    events = scrape_events_within_days(url, days)
    text_area.delete('1.0', tk.END)
    for event in events:
        text_area.insert(tk.END, event + '\n')

def save_ics_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("ICS Files", "*.ics")])
    if file_path:
        events = text_area.get('1.0', tk.END).strip().split('\n')
        save_events_to_ics_file(events, file_path)

# Set up the root window
root = tk.Tk()
root.title("Event Scraper")
root.geometry('600x400')

# Define some styles
button_font = font.Font(family='Helvetica', size=12, weight='bold')
text_area_font = font.Font(family='Consolas', size=10)  # Monospaced font for better text alignment
button_bg = '#0078D7'
button_fg = 'white'
text_area_bg = 'white'
text_area_fg = 'black'

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=0, sticky='ew')

# Create Buttons with styles
btn_all = tk.Button(button_frame, text="Scrape All", command=lambda: run_scraper(), font=button_font, bg=button_bg, fg=button_fg)
btn_30_days = tk.Button(button_frame, text="Next 30 Days", command=lambda: run_scraper(30), font=button_font, bg=button_bg, fg=button_fg)
btn_60_days = tk.Button(button_frame, text="Next 60 Days", command=lambda: run_scraper(60), font=button_font, bg=button_bg, fg=button_fg)
btn_save_ics = tk.Button(button_frame, text="Save as ICS", command=save_ics_file, font=button_font, bg=button_bg, fg=button_fg)

# Place buttons in the button frame
buttons = [btn_all, btn_30_days, btn_60_days, btn_save_ics]
for i, btn in enumerate(buttons):
    btn.grid(row=0, column=i, padx=5, pady=5, sticky='ew')

# Configure the button frame column weights to equally distribute the buttons
for i in range(len(buttons)):
    button_frame.grid_columnconfigure(i, weight=1)

# Create a scrollable text area for displaying results with styles
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=text_area_font, bg=text_area_bg, fg=text_area_fg)
text_area.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

# Configure the grid to resize with the window
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Optional: Set a minimum size for the window to prevent it from being too small
root.minsize(600, 400)

# Run the application
root.mainloop()