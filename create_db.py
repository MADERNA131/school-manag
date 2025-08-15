import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()


c.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    matricule TEXT UNIQUE,
    mot_de_passe TEXT,
    classe TEXT,
    faculte TEXT
)
""")

#Ajout d'exemples d'utilisateurs
users = [
    ("Jean Koffi", "INF101", "1234", "Info1", "Informatique"),
    ("Awa Diallo", "GEN101", "0000", "Genie1", "Génie Civil"),
    ("Ali Koné", "INF102", "abcd", "Info2", "Informatique")
]

c.executemany("INSERT INTO utilisateurs (nom, matricule, mot_de_passe, classe, faculte) VALUES (?, ?, ?, ?, ?)", users)

conn.commit()
conn.close()
