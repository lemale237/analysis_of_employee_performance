import tkinter as tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import sqlite3

class EmployeePerformanceAnalyzer:
    def __init__(self, master):
        self.master = master
        master.title("Analyse de performances des employés")

        # Création des widgets d'interface utilisateur
        self.filename_label = tk.Label(master, text="Sélectionner le fichier de base de données :")
        self.filename_label.grid(row=0, column=0)

        self.filename_entry = tk.Entry(master, width=50)
        self.filename_entry.grid(row=0, column=1)

        self.browse_button = tk.Button(master, text="Parcourir...", command=self.browse_file)
        self.browse_button.grid(row=0, column=2)

        self.tech_skills_checkbox = tk.Checkbutton(master, text="Compétences techniques")
        self.tech_skills_checkbox.grid(row=1, column=0)

        self.behavioral_skills_checkbox = tk.Checkbutton(master, text="Compétences comportementales")
        self.behavioral_skills_checkbox.grid(row=2, column=0)

        self.results_checkbox = tk.Checkbutton(master, text="Résultats")
        self.results_checkbox.grid(row=3, column=0)

        self.teamwork_checkbox = tk.Checkbutton(master, text="Capacité à travailler en équipe")
        self.teamwork_checkbox.grid(row=4, column=0)

        self.decision_making_checkbox = tk.Checkbutton(master, text="Capacité à prendre des décisions")
        self.decision_making_checkbox.grid(row=5, column=0)

        self.analyze_button = tk.Button(master, text="Analyser", command=self.analyze_performance)
        self.analyze_button.grid(row=6, column=1)

        self.results_label = tk.Label(master, text="Résultats de l'analyse :")
        self.results_label.grid(row=7, column=0)

        self.results_text = tk.Text(master, width=50, height=10)
        self.results_text.grid(row=8, column=0, columnspan=3)

    def browse_file(self):
        # Affichage de la boîte de dialogue pour sélectionner le fichier
        filename = askopenfilename(filetypes=[("CSV Files", "*.csv"), ("SQL Files", "*.db")])
        # Affichage du nom du fichier sélectionné dans la zone de texte
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(tk.END, filename)

    def analyze_performance(self):
        # Lecture des données sur les employés à partir du fichier de base de données
        filename = self.filename_entry.get()

        if filename.endswith(".csv"):
            data = pd.read_csv(filename)
        elif filename.endswith(".db"):
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            data = cursor.fetchall()
            conn.close()
        else:
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert(tk.END, "Le fichier sélectionné n'est pas un fichier CSV ou une base de données SQLite.")
            return

        # Analyse des performances des employés
        selected_columns = []
        if self.tech_skills_checkbox.get():
            selected_columns.append("tech_skills")
        if self.behavioral_skills_checkbox.get():
            selected_columns.append("behavioral_skills")
        if self.results_checkbox.get():
            selected_columns.append("results")
        if self.teamwork_checkbox.get():
            selected_columns.append("teamwork")
        if self.decision_making_checkbox.get():
            selected_columns.append("decision_making")

        if len(selected_columns) == 0:
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert(tk.END, "Veuillez sélectionner au moins une performance à évaluer.")
        else:
            employee_performance = analyze_employee_performance(data, selected_columns)

            # Affichage des résultats de l'analyse dans la zone de texte
            self.results_text.delete('1.0', tk.END)
            self.results_text.insert(tk.END, employee_performance)

def analyze_employee_performance(data, selected_columns):
    # Calcul de la performance globale des employés
    data['performance'] = data[selected_columns].mean(axis=1)

    # Tri des employés par ordre de performance décroissant
    data = data.sort_values(by='performance', ascending=False)

    # Création d'une chaîne de caractères contenant le classement des employés
    employee_performance = ""
    for index, row in data.iterrows():
        employee_performance += f"{row['name']} - Performance : {row['performance']:.2f}\n"
        employee_performance += "\nClassement des employés :\n"
        employee_performance += "Nom\t\tPerformance\n"
        employee_performance += "-------------------------------------\n"
        for index, row in data.iterrows():
            employee_performance += f"{row['name']}\t\t{row['performance']:.2f}\n"
        return employee_performance

    # Création de la fenêtre principale de l'application
    root = tk.Tk()
    my_gui = EmployeePerformanceAnalyzer(root)
    root.mainloop()