import random
import tkinter as tk
from tkinter import messagebox
import pygame
from tkinter import ttk

# Function to read match the following questions and answers from user input
def read_match_the_following():
    questions = []
    answers = []
    
    def submit_input():
        q = question_entry.get().strip()
        a = answer_entry.get().strip()
        if q and a:
            questions.append(q)
            answers.append(a)
            question_entry.delete(0, tk.END)
            answer_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter both question and answer.")
    
    def finish_input():
        input_window.destroy()
    
    input_window = tk.Tk()
    input_window.title("Input Questions and Answers")
    
    tk.Label(input_window, text="Enter question:", font=("Helvetica", 12)).pack(pady=5)
    question_entry = tk.Entry(input_window, width=50, font=("Helvetica", 12))
    question_entry.pack(pady=5)
    
    tk.Label(input_window, text="Enter answer:", font=("Helvetica", 12)).pack(pady=5)
    answer_entry = tk.Entry(input_window, width=50, font=("Helvetica", 12))
    answer_entry.pack(pady=5)
    
    submit_button = tk.Button(input_window, text="Submit", command=submit_input, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    submit_button.pack(pady=5)
    
    finish_button = tk.Button(input_window, text="Finish", command=finish_input, font=("Helvetica", 12), bg="#FF5722", fg="white")
    finish_button.pack(pady=5)
    
    input_window.mainloop()
    
    return questions, answers

# Function to create flash card tiles with more graphics
def create_flash_cards(questions, answers):
    # Initialize pygame mixer for sound effects
    pygame.mixer.init()

    # Load sound effects
    correct_sound = pygame.mixer.Sound("correct.wav")
    wrong_sound = pygame.mixer.Sound("wrong.wav")

    # Shuffle the answers to randomize their positions
    shuffled_answers = answers[:]
    random.shuffle(shuffled_answers)
    
    # Create a Tkinter window
    root = tk.Tk()
    root.title("Match the Following")

    # Set window size and background color
    root.geometry("800x600")
    root.configure(bg="black")

    # Create frames for questions and answers
    question_frame = tk.Frame(root, bg="black")
    question_frame.pack(side=tk.LEFT, padx=20, pady=20)
    answer_frame = tk.Frame(root, bg="black")
    answer_frame.pack(side=tk.RIGHT, padx=20, pady=20)

    # Create buttons for questions with blue gradient color and white text
    question_buttons = []
    for q in questions:
        btn = tk.Button(question_frame, text=q, width=20, height=2, font=("Helvetica", 14), fg="white", relief="raised", bd=5)
        btn.pack(pady=10)
        btn.config(bg='#0000FF', activebackground='#0000FF')
        question_buttons.append(btn)

    # Create buttons for answers with white background and black text
    answer_buttons = []
    for a in shuffled_answers:
        btn = tk.Button(answer_frame, text=a, width=20, height=2, font=("Helvetica", 14), bg="white", fg="black", relief="raised", bd=5)
        btn.pack(pady=10)
        answer_buttons.append(btn)

    # Function to handle button clicks
    def on_button_click(btn):
        selected_btns.append(btn)
        if len(selected_btns) == 2:
            q_btn, a_btn = selected_btns
            q_index = question_buttons.index(q_btn)
            a_index = answer_buttons.index(a_btn)
            if answers[q_index] == shuffled_answers[a_index]:
                q_btn.config(state=tk.DISABLED, bg="#66CC66", fg="white")  # Light green color with reduced intensity
                a_btn.config(state=tk.DISABLED, bg="#66CC66", fg="white")  # Light green color with reduced intensity
                correct_sound.play()
                selected_btns.clear()
                if all(btn['state'] == tk.DISABLED for btn in question_buttons):
                    messagebox.showinfo("Success", "All pairs matched correctly!")
            else:
                q_btn.config(bg="#CC6666", fg="white")  # Light red color with reduced intensity
                a_btn.config(bg="#CC6666", fg="white")  # Light red color with reduced intensity
                wrong_sound.play()
                selected_btns.clear()

    # Function to reset the game
    def reset_game():
        for btn in question_buttons:
            btn.config(state=tk.NORMAL, bg='#0000FF', fg='white')  # Reset question buttons to original color
        for btn in answer_buttons:
            btn.config(state=tk.NORMAL, bg='white', fg='black')  # Reset answer buttons to original color
        random.shuffle(shuffled_answers)
        for i, btn in enumerate(answer_buttons):
            btn.config(text=shuffled_answers[i])
        selected_btns.clear()

    # Bind button click events
    selected_btns = []
    for btn in question_buttons + answer_buttons:
        btn.config(command=lambda b=btn: on_button_click(b))

    # Create reset button
    reset_button = tk.Button(root, text="Reset", width=10, height=2, font=("Helvetica", 14), bg="#FF5722", fg="white", relief="raised", bd=5, command=reset_game)
    reset_button.pack(pady=20)

    root.mainloop()

# Get questions and answers from user input
questions, answers = read_match_the_following()

# Create flash card tiles with match the following functionality and more graphics
create_flash_cards(questions, answers)