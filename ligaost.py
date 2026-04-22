import tkinter as tk
from tkinter import messagebox
import subprocess
import os

import ligaost_round_manager

def load_config():
    config = {}

    with open("config.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # skip empty lines or comments
            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    # convert types
    config["k"] = int(config["k"])
    config["accuracy"] = int(config["accuracy"])

    return config

def neue_runde():
    cfg = load_config()

    ligaost_round_manager.write_round(
        player_file=cfg["player_file"],
        round_file=cfg["round_file"],
        accuracy=cfg["accuracy"]
    )

    print("new round created, play the rounds and then change the score in the file")
    return None

def runden_ende_rating_change():
    cfg = load_config()

    ligaost_round_manager.update_ratings_from_round(
        player_file=cfg["player_file"],
        round_file=cfg["round_file"],
        k=cfg["k"]
    )

    print("round ended and ratings changed, now add new players if needed and start new round")
    return None

# neue_runde()

# runden_ende_rating_change()

def open_readme():
    try:
        if os.name == "nt":  # Windows
            os.startfile("README.txt")
        else:
            subprocess.call(["open", "README.txt"])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open README: {e}")

def create_ui():
    root = tk.Tk()
    root.title("LigaOst Manager")
    root.geometry("350x200")

    label = tk.Label(
        root,
        text="LigaOst Tournament Manager\n\nChoose an action:",
        justify="center"
    )
    label.pack(pady=15)

    btn_readme = tk.Button(root, text="Open README", command=open_readme)
    btn_readme.pack(pady=5)

    btn_new_round = tk.Button(root, text="New Round", command=neue_runde)
    btn_new_round.pack(pady=5)

    btn_finish_round = tk.Button(
        root,
        text="Finish Round (Update Ratings)",
        command=runden_ende_rating_change
    )
    btn_finish_round.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    create_ui()