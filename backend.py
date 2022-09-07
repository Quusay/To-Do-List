import sqlite3


class BackEnd:
    def __init__(self):
        self.project_list = sqlite3.connect('Projects.db')

        self.pl = self.project_list.cursor()

        self.pl.execute("""CREATE TABLE IF NOT EXISTS projects (
            name text,
            prog_language text,
            date_started text,
            date_target text,
            completed text
        )""")

    def insertProjectName(self, title, lang, d_start, d_target, completed):
        self.pl.execute("""INSERT INTO projects VALUES (:title, :lang, :start, :target, :completed)""", {'title':title, 'lang':lang, 'start':d_start, 'target':d_target, 'completed':completed})
        self.project_list.commit()

    def showProjects(self):
        self.pl.execute("""SELECT *, oid FROM projects""")
        records = self.pl.fetchall()
        self.project_list.commit()
        return records

    def deleteProjects(self, id):
        self.pl.executemany("""DELETE FROM projects WHERE oid = ?""", [(a,) for a in id])
        self.project_list.commit()

    def updateProject(self, title, lang, d_start, d_target, completed, id):
        self.pl.execute("""UPDATE projects SET (name, prog_language, date_started, date_target, completed) = (?,?,?,?,?) WHERE oid = ?""", (title, lang, d_start, d_target, completed, id))
        self.project_list.commit()

    def completedProject(self, id):
        self.pl.executemany("""UPDATE projects SET completed = "Yes" WHERE oid = ?""", [(a,) for a in id])
        self.project_list.commit()

    def incompletedProject(self, id):
        self.pl.executemany("""UPDATE projects SET completed = "No" WHERE oid = ?""", [(a,) for a in id])
        self.project_list.commit()

# if __name__ == "__main__":
#     projectDatabase = BackEnd()
#     projectDatabase.run()
