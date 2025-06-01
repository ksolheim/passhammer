import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests
import datetime as dt
import webbrowser

# setup database
conn = sqlite3.connect('data/offices.db')
c = conn.cursor()

# dict to hold branch and branch_public_id
branch_name_ids = {}
c.execute('SELECT branch_name, branch_public_id FROM Branches')
for row in c.fetchall():
  branch_name_ids[row[0]] = row[1]

# dict to hold service and service_id
service_name_ids = {}
c.execute('SELECT service_name, service_public_id FROM Services')
for row in c.fetchall():
  service_name_ids[row[0]] = row[1]

conn.close()

# Generate list of dates from start_date to end_date
def generate_dates(start_date, end_date):
    dates = []
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    n_days = (end_date - start_date).days + 1
    
    for i in range(n_days):
        dates.append((start_date + dt.timedelta(days=i)).strftime('%Y-%m-%d'))
    return dates

#Get selected branches and return dictionary of branch names and branch_public_ids
def get_selected_branch_ids():
    branch_public_ids = {}
    for branch in branch_listbox.curselection():
        branch_public_ids[branch_listbox.get(branch)] = branch_name_ids[branch_listbox.get(branch)]
    return branch_public_ids

# Update info labels
def update_info_label1():
    info_label1.config(text=f'Last run: {dt.datetime.now().strftime("%H:%M:%S")} \n Next run: {(dt.datetime.now() + dt.timedelta(minutes=int(check_interval_entry.get()))).strftime("%H:%M:%S")}')

def update_info_label2():
    label_branches = [branch_listbox.get(i) for i in branch_listbox.curselection()]
    info_label2.config(text=f'Selected branches:\n {'\n'.join(label_branches)}')

# Submit logic
def on_submit():
    selected_branc_name_and_id = get_selected_branch_ids()
    selected_service_id = service_name_ids[service_var.get()]
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    dates = generate_dates(start_date, end_date)
    update_info_label1()
    update_info_label2()
    def check_urls():
        for date in dates:
            for branch_name, branch_id in selected_branc_name_and_id.items():
                url = f'https://pass-og-id.politiet.no/qmaticwebbooking/rest/schedule/branches/{branch_id}/dates/{date}/times;servicePublicId={selected_service_id};customSlotLength=10'
                response = requests.get(url)
                current_branch_and_date = response.json()
                # if current_branch_and_date > 0 alert the user and ask if they want to open the url
                if len(current_branch_and_date) > 0:
                    root.bell()
                    root.lift()
                    root.focus_force()
                    
                    # new dialog window instead of messagebox
                    dialog = tk.Toplevel(root)
                    dialog.title("Alert")
                    dialog.geometry("300x150")
                    dialog.attributes('-topmost', True)  
                    dialog.transient(root)  
                    dialog.grab_set()  
                    
                    # center dialog on screen
                    dialog.update_idletasks()
                    screen_width = dialog.winfo_screenwidth()
                    screen_height = dialog.winfo_screenheight()
                    x = (screen_width - dialog.winfo_width()) // 2
                    y = (screen_height - dialog.winfo_height()) // 2
                    dialog.geometry(f"+{x}+{y}")
                    
                    label = tk.Label(dialog, text=f'Found available time at {branch_name} on {date}.', wraplength=250)
                    label.pack(pady=10)
                    
                    def open_url():
                        webbrowser.open(f'https://pass-og-id.politiet.no/timebestilling/index.html#/preselect/branch/{branch_id}?preselectFilters=off')
                        dialog.destroy()
                    
                    def close_dialog():
                        dialog.destroy()
                    
                    button_frame = tk.Frame(dialog)
                    button_frame.pack(pady=10)
                    
                    yes_button = tk.Button(button_frame, text="Open URL", command=open_url)
                    yes_button.pack(side=tk.LEFT, padx=5)
                    
                    no_button = tk.Button(button_frame, text="Close", command=close_dialog)
                    no_button.pack(side=tk.LEFT, padx=5)
        root.after(int(check_interval_entry.get()) * 60 * 1000, check_urls)
    check_urls()

# Main window
root = tk.Tk()
root.title("Passhammer")
root.geometry('400x600')

# Branches Listbox
branch_var = tk.StringVar()
branch_listbox = tk.Listbox(root, listvariable=branch_var, selectmode=tk.EXTENDED, exportselection=False)
branch_listbox.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

scrollbar = tk.Scrollbar(branch_listbox, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
branch_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=branch_listbox.yview)

for branch in branch_name_ids.keys():
    branch_listbox.insert(tk.END, branch)

# Information Labels
info_label1 = tk.Label(root, text='')
info_label1.pack(pady=5, padx=10)
info_label2 = tk.Label(root, text='')
info_label2.pack(pady=5, padx=10)

# Services Dropdown
service_var = tk.StringVar()
service_var.set('Choose a service')
service_dropdown = tk.OptionMenu(root, service_var, *service_name_ids.keys())
service_dropdown.pack(fill=tk.X, pady=5, padx=10)

# Start Date Entry
start_date_label = tk.Label(root, text='Start date (YYYY-MM-DD)')
start_date_label.pack(pady=5, padx=10)
start_date_entry = tk.Entry(root)
start_date_entry.insert(0, f'{dt.datetime.now().strftime("%Y-%m-%d")}')
start_date_entry.pack(fill=tk.X, pady=5, padx=10)

# End Date Entry
end_date_label = tk.Label(root, text='End date (YYYY-MM-DD)')
end_date_label.pack(pady=5, padx=10)
end_date_entry = tk.Entry(root)
end_date_entry.insert(0, f'{dt.datetime.now().strftime("%Y-%m-")}')
end_date_entry.pack(fill=tk.X, pady=5, padx=10)

# Check Interval Entry
check_interval_label = tk.Label(root, text='Check interval (minutes)')
check_interval_label.pack(pady=5, padx=10)
check_interval_entry = tk.Entry(root)
check_interval_entry.insert(0, '5')
check_interval_entry.pack(fill=tk.X, pady=5, padx=10)

# Submit Button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)


root.mainloop()