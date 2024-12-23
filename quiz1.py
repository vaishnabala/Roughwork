import random
import tkinter as tk
from tkinter import messagebox
import pygame

# Function to read match the following questions and answers from a text file
def read_match_the_following(file_path):
    questions = []
    answers = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                q, a = line.split('-')
                questions.append(q.strip())
                answers.append(a.strip())
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
        btn = tk.Button(question_frame, text=q, width=20, height=2, font=("Arial", 14), fg="white", relief="raised", bd=5)
        btn.pack(pady=10)
        btn.config(bg='#0000FF', activebackground='#0000FF')
        question_buttons.append(btn)

    # Create buttons for answers with white background and black text
    answer_buttons = []
    for a in shuffled_answers:
        btn = tk.Button(answer_frame, text=a, width=20, height=2, font=("Arial", 14), bg="white", fg="black", relief="raised", bd=5)
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
    reset_button = tk.Button(root, text="Reset", width=10, height=2, font=("Arial", 14), bg="#FF5722", fg="white", relief="raised", bd=5, command=reset_game)
    reset_button.pack(pady=20)

    root.mainloop()

# Path to the input text file
file_path = 'input.txt'

# Read questions and answers from the text file
questions, answers = read_match_the_following(file_path)

# Create flash card tiles with match the following functionality and more graphics
create_flash_cards(questions, answers)