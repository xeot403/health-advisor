# Smart Health Companion – AI Lifestyle Advisor
# Created for Class 12 CS Project
# Developer: Xeot403
# Libraries used: tkinter, pandas, matplotlib, datetime, random

import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import random
import os

# ------------------------------- Health Logic ----------------------------------

def calculate_health_score(sleep, water, steps, mood):
    score = 0

    # Sleep logic
    if 7 <= sleep <= 9:
        score += 25
    elif 5 <= sleep < 7 or 9 < sleep <= 10:
        score += 15
    else:
        score += 5

    # Water logic
    if 6 <= water <= 10:
        score += 25
    elif 3 <= water < 6 or 10 < water <= 12:
        score += 15
    else:
        score += 5

    # Steps logic
    if steps >= 7000:
        score += 25
    elif 4000 <= steps < 7000:
        score += 15
    else:
        score += 5

    # Mood logic
    if mood >= 8:
        score += 25
    elif 5 <= mood < 8:
        score += 15
    else:
        score += 5

    return score

# AI Health tips
def get_health_tip(score):
    tips = [
        "Remember to take small breaks every hour to stretch!",
        "Drink more water regularly to stay hydrated.",
        "Avoid screens 30 mins before bed for better sleep.",
        "A short walk can boost your mood instantly.",
        "Consistency is key — keep maintaining healthy habits!",
        "Deep breathing can help reduce stress in minutes."
    ]
    if score >= 85:
        return "🌟 Excellent! You’re in great shape. Keep it up!"
    elif score >= 65:
        return random.choice(tips)
    else:
        return "⚠️ You need to improve your habits! Start small but stay consistent."

# ------------------------------- File Handling ----------------------------------

def save_data(date, sleep, water, steps, mood, score):
    data = {
        "Date": [date],
        "Sleep Hours": [sleep],
        "Water (glasses)": [water],
        "Steps": [steps],
        "Mood (1-10)": [mood],
        "Health Score": [score]
    }
    df = pd.DataFrame(data)
    if not os.path.exists("health_data.csv"):
        df.to_csv("health_data.csv", index=False)
    else:
        df.to_csv("health_data.csv", mode='a', index=False, header=False)

# ------------------------------- Graph Plotting ----------------------------------

def show_progress_chart():
    if not os.path.exists("health_data.csv"):
        messagebox.showerror("No Data", "No data found. Add some entries first!")
        return

    df = pd.read_csv("health_data.csv")
    plt.figure(figsize=(8,5))
    plt.plot(df["Date"], df["Health Score"], marker='o', linewidth=2)
    plt.title("Health Progress Over Time", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Health Score")
    plt.xticks(rotation=30)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ------------------------------- GUI ----------------------------------

root = tk.Tk()
root.title("Smart Health Companion – AI Lifestyle Advisor")
root.geometry("600x580")
root.config(bg="#dce8f5")

title_label = tk.Label(root, text="🧠 Smart Health Companion", font=("Helvetica", 18, "bold"), bg="#dce8f5", fg="#3b3b98")
title_label.pack(pady=10)

desc_label = tk.Label(root, text="Your AI-based Daily Health Tracker", font=("Helvetica", 12), bg="#dce8f5", fg="#3b3b98")
desc_label.pack(pady=5)

# Frame
frame = tk.Frame(root, bg="#f1f2f6", bd=2, relief="groove")
frame.pack(pady=10, padx=20, fill="both", expand=True)

# Labels & Inputs
labels = ["Sleep Hours", "Water Intake (glasses)", "Steps Walked", "Mood Level (1-10)"]
entries = {}

for label in labels:
    lbl = tk.Label(frame, text=label, font=("Helvetica", 12), bg="#f1f2f6", anchor="w")
    lbl.pack(pady=5, padx=10, fill="x")
    entry = ttk.Entry(frame, font=("Helvetica", 11))
    entry.pack(pady=3, padx=10, fill="x")
    entries[label] = entry

# Result Label
result_label = tk.Label(root, text="", font=("Helvetica", 13, "bold"), bg="#dce8f5", fg="#2c2c54")
result_label.pack(pady=10)

tip_label = tk.Label(root, text="", wraplength=500, justify="center", font=("Helvetica", 11), bg="#dce8f5", fg="#218c74")
tip_label.pack(pady=10)

# ------------------------------- Button Functions ----------------------------------

def analyze():
    try:
        sleep = float(entries["Sleep Hours"].get())
        water = float(entries["Water Intake (glasses)"].get())
        steps = int(entries["Steps Walked"].get())
        mood = float(entries["Mood Level (1-10)"].get())

        score = calculate_health_score(sleep, water, steps, mood)
        today = datetime.now().strftime("%d-%m-%Y")

        save_data(today, sleep, water, steps, mood, score)

        emoji = "😄" if score >= 80 else ("🙂" if score >= 60 else "😐")
        result_label.config(text=f"Your Health Score: {score}/100 {emoji}")
        tip_label.config(text=get_health_tip(score))

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for all fields.")

# Buttons
btn_frame = tk.Frame(root, bg="#dce8f5")
btn_frame.pack(pady=20)

analyze_btn = ttk.Button(btn_frame, text="Analyze Health", command=analyze)
analyze_btn.grid(row=0, column=0, padx=10)

chart_btn = ttk.Button(btn_frame, text="View Progress Chart", command=show_progress_chart)
chart_btn.grid(row=0, column=1, padx=10)

exit_btn = ttk.Button(btn_frame, text="Exit", command=root.quit)
exit_btn.grid(row=0, column=2, padx=10)

footer_label = tk.Label(root, text="© 2025 Smart Health Companion | Created by Xeot403", font=("Helvetica", 9), bg="#dce8f5", fg="#6c5ce7")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
