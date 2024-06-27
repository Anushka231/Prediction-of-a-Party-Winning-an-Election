#!/usr/bin/env python
# coding: utf-8

# # FINAL CODE

# # System Working Properly

# In[1]:


import pandas as pd
import tkinter as tk
from tkinter import messagebox, StringVar, IntVar, Entry, OptionMenu
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import string
import csv
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import burst

# Load the election dataset
csv_file = 'New_dataset_Elections - New_dataset_Electionss (2).csv'
data = pd.read_csv(csv_file)

# Function to generate a random password
def generate_password():
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(10))

# Function to save user credentials to a file
def save_credentials(filename, username, password):
    with open(filename, "a") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

# Function to log user access
def log_user_access(username):
    with open("user_access.log", "a") as file:
        file.write(f"User {username} accessed the system.\n")



# Function for admin login
def admin_login(username, password):
    if username == "admin" and password == "admin_password":
        messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
        admin_window = tk.Tk()
        admin_window.title("Admin Dashboard")
        admin_window.configure(bg="light yellow")
        screen_width = admin_window.winfo_screenwidth()
        screen_height = admin_window.winfo_screenheight()
        admin_window.geometry(f"{screen_width}x{screen_height}+0+0")

        # Function to display state with maximum votes as a pie chart using Burst
        # Function for admin login
# Function for admin login
def admin_login(username, password):
    if username == "admin" and password == "admin_password":
        messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
        admin_window = tk.Toplevel()
        admin_window.title("Admin Dashboard")
        admin_window.configure(bg="light yellow")
        screen_width = admin_window.winfo_screenwidth()
        screen_height = admin_window.winfo_screenheight()
        admin_window.geometry(f"{screen_width}x{screen_height}+0+0")

        # Function to display state with maximum votes as a pie chart
        def display_max_votes_pie_chart():
            state_votes = data.groupby('State_Name')['TOTAL_VOTES'].sum().reset_index()
            max_votes_state = state_votes.loc[state_votes['TOTAL_VOTES'].idxmax()]
            labels = [max_votes_state['State_Name'], 'Other States']
            sizes = [max_votes_state['TOTAL_VOTES'], state_votes['TOTAL_VOTES'].sum() - max_votes_state['TOTAL_VOTES']]
            explode = (0.1, 0)
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
            ax1.axis('equal')
            plt.title('State with Maximum Votes')
            max_votes_label = f"{max_votes_state['State_Name']}: {max_votes_state['TOTAL_VOTES']} votes"
            plt.text(0, -1.2, max_votes_label, fontsize=12, ha='center')
            pie_chart_window = tk.Toplevel(admin_window)
            pie_chart_window.title("State with Maximum Votes")
            pie_chart_window.geometry(f"{screen_width}x{screen_height}+0+0")
            canvas = FigureCanvasTkAgg(fig1, master=pie_chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            pie_chart_window.mainloop()

        # Function to display total votes per state as a pie chart
        def display_total_votes_pie_chart():
            state_votes = data.groupby('State_Name')['TOTAL_VOTES'].sum().reset_index()
            fig2, ax2 = plt.subplots()
            patches, texts, _ = ax2.pie(state_votes['TOTAL_VOTES'], labels=state_votes['State_Name'], autopct='%1.1f%%', shadow=True, startangle=140)
            ax2.axis('equal')
            plt.title('Total Votes per State')
            ax2.legend(patches, state_votes['State_Name'], loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            pie_chart_window = tk.Toplevel(admin_window)
            pie_chart_window.title("Total Votes per State")
            pie_chart_window.geometry(f"{screen_width}x{screen_height}+0+0")
            canvas = FigureCanvasTkAgg(fig2, master=pie_chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            pie_chart_window.mainloop()

        # Function to display election results pie chart
        def display_election_results():
            grouped_data = data.groupby('PARTY_NAME')['TOTAL_VOTES'].sum().reset_index()
            grouped_data = grouped_data.sort_values(by='TOTAL_VOTES', ascending=False)
            total_votes = grouped_data['TOTAL_VOTES'].sum()
            grouped_data['PERCENTAGE'] = (grouped_data['TOTAL_VOTES'] / total_votes) * 100
            top_parties = grouped_data.iloc[:5].copy()
            other_parties = grouped_data.iloc[5:].copy()
            other_votes = other_parties['TOTAL_VOTES'].sum()
            other_percentage = other_parties['PERCENTAGE'].sum()
            other_parties_df = pd.DataFrame({
                'PARTY_NAME': ['Other Parties'],
                'TOTAL_VOTES': [other_votes],
                'PERCENTAGE': [other_percentage]
            })
            top_parties = pd.concat([top_parties, other_parties_df], ignore_index=True)
            fig3, ax3 = plt.subplots(figsize=(10, 8))
            ax3.pie(top_parties['PERCENTAGE'], labels=top_parties['PARTY_NAME'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            plt.title('Election Results: Winner, Top 4 Runner-Up Parties, and Other Parties')
            ax3.axis('equal')
            pie_chart_window = tk.Toplevel(admin_window)
            pie_chart_window.title("Election Results")
            pie_chart_window.geometry(f"{screen_width}x{screen_height}+0+0")
            canvas = FigureCanvasTkAgg(fig3, master=pie_chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            pie_chart_window.mainloop()

        def logout():
            admin_window.destroy()
            login_window.deiconify()
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            selected_role.set(0)

        max_votes_button = tk.Button(admin_window, text="State with Maximum Votes", command=display_max_votes_pie_chart, font=("Times New Roman", 16))
        max_votes_button.pack(pady=20)
        total_votes_button = tk.Button(admin_window, text="Total Votes per State", command=display_total_votes_pie_chart, font=("Times New Roman", 16))
        total_votes_button.pack(pady=20)
        results_button = tk.Button(admin_window, text="Display Election Results", command=display_election_results, font=("Times New Roman", 16))
        results_button.pack(pady=20)
        logout_button = tk.Button(admin_window, text="Logout", command=logout, font=("Times New Roman", 16))
        logout_button.pack(pady=20)
        admin_window.mainloop()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
# Function to handle the login process
def handle_login():
    username = username_entry.get()
    password = password_entry.get()

    if selected_role.get() == 2:  # Admin role
        admin_login(username, password)
    else:  # User role
        user_login(username, password)

# Check if admin is already logged in (using saved credentials)
def saved_admin_credentials_exist():
    return os.path.exists("admin_credentials.csv")

def get_saved_admin_credentials():
    with open("admin_credentials.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            return row[0], row[1]

if saved_admin_credentials_exist():
    username, password = get_saved_admin_credentials()
    admin_login(username, password)

def register():
    username = username_entry.get()
    password = password_entry.get()
   
    # Check if both username and password are provided
    if not username or not password:
        messagebox.showerror("Registration Failed", "Username and password are required.")
        return
   
    if username in users:
        messagebox.showerror("Username Taken", "Username already exists. Please choose a different one.")
    else:
        users[username] = password
        save_credentials("user_credentials.csv", username, password)  # Save user credentials to file
        messagebox.showinfo("Registration Successful", "User registered successfully.")

# Function to display forget password option
def forget_password():
    username = username_entry.get()
    if username not in users:
        messagebox.showerror("Error", "Username not found.")
    else:
        password = generate_password()
        messagebox.showinfo("New Password", f"Your new password is: {password}")
        users[username] = password
        save_credentials("user_credentials.csv", username, password)

# Global dictionary to store user credentials
users = {}

def user_login(username, password):
    credentials_file = "user_credentials.csv"
    if not os.path.exists(credentials_file):
        messagebox.showerror("Login Failed", "No user credentials found. Please register first.")
        return

    with open(credentials_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 2 and row[0] == username and row[1] == password:
                messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
                log_user_access(username)
                select_state_and_constituency()
                return
    messagebox.showerror("Login Failed", "Invalid username or password")

def select_state_and_constituency():
    state_window = tk.Toplevel()  # Use Toplevel instead of Tk
    state_window.title("Select State and Constituency")
    state_window.configure(bg="light yellow")
    screen_width = state_window.winfo_screenwidth()
    screen_height = state_window.winfo_screenheight()
    state_window.geometry(f"{screen_width}x{screen_height}+0+0")
    main_frame = tk.Frame(state_window, bg="light yellow")
    main_frame.pack(expand=True, fill='both')

    # Box frame to hold state, constituency selection, and submit button
    box_frame = tk.Frame(main_frame, bg="light yellow", bd=2, relief="ridge")
    box_frame.place(relx=0.5, rely=0.5, anchor="center")

    # State Selection
    state_label = tk.Label(box_frame, bg="light yellow", text="Select State:", font=("Times New Roman", 18))
    state_label.grid(row=0, column=0, padx=10, pady=10)

    state_var = StringVar()
    state_menu = OptionMenu(box_frame, state_var, *data['State_Name'].unique())
    state_menu.grid(row=0, column=1, padx=10, pady=10)

    # Constituency Selection
    constituency_label = tk.Label(box_frame, bg="light yellow", text="Select Constituency:", font=("Times New Roman", 18))
    constituency_label.grid(row=1, column=0, padx=10, pady=10)

    constituency_var = StringVar()
    constituency_menu = OptionMenu(box_frame, constituency_var, "")
    constituency_menu.grid(row=1, column=1, padx=10, pady=10)

    # Function to update constituencies based on selected state
    def update_constituencies(selected_state):
        constituencies = data[data['State_Name'] == selected_state]['PC_NAME'].unique()
        constituency_menu['menu'].delete(0, 'end')
        for constituency in constituencies:
            constituency_menu['menu'].add_command(label=constituency, command=lambda c=constituency: constituency_var.set(c))

    # Update constituencies when state is selected
    def on_state_select(*args):
        selected_state = state_var.get()
        update_constituencies(selected_state)

    state_var.trace('w', on_state_select)

    # Submit Button
    submit_button = tk.Button(box_frame, bg="light yellow", text="Submit", font=("Times New Roman", 18),
                              command=lambda: display_candidates(state_var.get(), constituency_var.get(), state_window))
    submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

    state_window.mainloop()  # Ensure the state window remains open until closed

# Function to display candidates
def display_candidates(selected_state, selected_constituency, state_window):
    state_window.destroy()

    global candidates_window
    candidates_window = tk.Tk()
    candidates_window.title("Select Candidate")
    candidates_window.configure(bg="light yellow")
    screen_width = candidates_window.winfo_screenwidth()
    screen_height = candidates_window.winfo_screenheight()
    candidates_window.geometry(f"{screen_width}x{screen_height}+0+0")

    main_frame = tk.Frame(candidates_window, bg="light yellow")
    main_frame.pack(expand=True, fill='both')

    # Box frame to hold candidate selection and submit button
    box_frame = tk.Frame(main_frame, bg="light yellow", bd=2, relief="ridge")
    box_frame.place(relx=0.5, rely=0.1, anchor="n")

    # Candidate Selection
    candidates_label = tk.Label(box_frame, bg="light yellow", text="Select Candidate:", font=("Times New Roman", 18))
    candidates_label.grid(row=0, column=0, padx=10, pady=10)

    candidate_var = StringVar()
    candidate_menu = OptionMenu(box_frame, candidate_var, *data[(data['State_Name'] == selected_state) & (data['PC_NAME'] == selected_constituency)]['CANDIDATES_NAME'].unique())
    candidate_menu.grid(row=0, column=1, padx=10, pady=10)

    # Function to display candidate history
    def display_candidate_history():
        candidate_name = candidate_var.get()
        candidate_info = data[(data['State_Name'] == selected_state) & (data['PC_NAME'] == selected_constituency) & (data['CANDIDATES_NAME'] == candidate_name)].iloc[0]

        global history_frame
        history_frame = tk.Toplevel()
        history_frame.title(f"{candidate_name}'s History")
        history_frame.configure(bg="light yellow")
        screen_width = history_frame.winfo_screenwidth()
        screen_height = history_frame.winfo_screenheight()
        history_frame.geometry(f"{screen_width}x{screen_height}+0+0")
       
        history_text = f"Candidate Name: {candidate_info['CANDIDATES_NAME']}\n"
        history_text += f"Party Name: {candidate_info['PARTY_NAME']}\n"
        history_text += f"PARTY SYMBOL: {candidate_info['PARTY_SYMBOL']}\n"
        history_text += f"AGE: {candidate_info['AGE']}\n"
        history_text += f"SEX: {candidate_info['SEX']}\n"
        history_text += f"CATEGORY: {candidate_info['CATEGORY']}\n"
        history_text += f"Education: {candidate_info['Education']}\n"
        history_text += f"Political History: {candidate_info['Political_History']}\n"
        history_text += f"Politician Behavior: {candidate_info['Politican_Behavior']}\n"
        history_text += f"Work Done: {candidate_info['Work_Done']}\n"

        history_label = tk.Label(history_frame, bg="light yellow", text=history_text, font=("Times New Roman", 18))
        history_label.pack()

        # Create the Vote button
        vote_button = tk.Button(history_frame, text="Vote", command=lambda: cast_vote(candidate_name, selected_state, selected_constituency), font=("Times New Roman", 16))
        vote_button.pack(pady=10)

        history_frame.mainloop()

    # Submit Button
    submit_button = tk.Button(box_frame, bg="light yellow", text="Submit", font=("Times New Roman", 18), command=display_candidate_history)
    submit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    candidates_window.mainloop()

def cast_vote(candidate_name, selected_state, selected_constituency):
    # Update the main CSV file with the vote casted
    data.loc[(data['State_Name'] == selected_state) & (data['PC_NAME'] == selected_constituency) & (data['CANDIDATES_NAME'] == candidate_name), 'TOTAL_VOTES'] += 1
    data.to_csv(csv_file, index=False)
    messagebox.showinfo("Success", "Your vote has been cast successfully!")

   # Destroy the history frame
    if 'history_frame' in globals() and history_frame.winfo_exists():
        history_frame.destroy()
        
    if 'candidates_window' in globals() and candidates_window.winfo_exists():
        candidates_window.destroy()

    # Redirect to the login page
    login_window.deiconify()  # Show the login window
    selected_role.set(0)
    username_entry.delete(0, tk.END)  # Clear username entry field
    password_entry.delete(0, tk.END)

    # Logout the user and reset the login page
    def logout():
        try:
            history_frame.destroy()
        except NameError:
            pass
        login_window.deiconify()
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    logout()


# GUI for login
login_window = tk.Tk()
login_window.title("Login")
login_window.configure(bg="light yellow")  
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
login_window.geometry(f"{screen_width}x{screen_height}+0+0")

image = Image.open("election-commission.jpg")
window_width = login_window.winfo_screenwidth()
window_height = login_window.winfo_screenheight()
image = image.resize((window_width, window_height), Image.LANCZOS)
photo_image = ImageTk.PhotoImage(image)
background_label = tk.Label(login_window, image=photo_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Disclaimer message
disclaimer_label = tk.Label(login_window, text="This project is for educational purposes only. It is not intended for commercial use.", font=("Times New Roman", 18), bg="light green")
disclaimer_label.pack(pady=(100, screen_height//2))  # Adjust the y position to half of screen_height


login_frame = tk.Frame(login_window, bg="light yellow", bd=2, relief="ridge", padx=20, pady=10)
login_frame.pack(padx=50, pady=30)

selected_role = IntVar()

user_button = tk.Radiobutton(login_frame, text="User", variable=selected_role, value=1, font=("Times New Roman", 18), bg="light yellow")
user_button.pack()

admin_button = tk.Radiobutton(login_frame, text="Admin", variable=selected_role, value=2, font=("Times New Roman", 18), bg="light yellow")
admin_button.pack()

username_label = tk.Label(login_frame, bg="light yellow", text="Username:", font=("Times New Roman", 18))
username_label.pack()

username_entry = Entry(login_frame, bg="light yellow", font=("Times New Roman", 18))
username_entry.pack()

password_label = tk.Label(login_frame, bg="light yellow", text="Password:", font=("Times New Roman", 18))
password_label.pack()

password_entry = Entry(login_frame, bg="light yellow", show="*", font=("Times New Roman", 18))
password_entry.pack()

register_button = tk.Button(login_frame, bg="light yellow", text="Register", font=("Times New Roman", 18), command=register)
register_button.pack(fill="both", expand=True)

login_button = tk.Button(login_frame, bg="light yellow", text="Login", font=("Times New Roman", 18), command=handle_login)
login_button.pack(fill="both", expand=True)

forget_password_button = tk.Button(login_frame, bg="light yellow", text="Forget Password", font=("Times New Roman", 18), command=forget_password)
forget_password_button.pack(fill="both", expand=True)

# Centering login_frame within login_window
login_frame.place(relx=0.5, rely=0.5, anchor='center')
login_window.mainloop()



# In[ ]:





# In[ ]:




