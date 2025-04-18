# Crew Maker

**A Python desktop application** (written with Tkinter) that creates random groups of people, each with specific role requirements (like *at least one Writer* or *one DP* per group). Great for film/crew projects or other creative collaboration tasks.

![image](https://github.com/user-attachments/assets/62958889-5ef2-4327-af5a-1e99194ca723)

---

## Features

- **Add, Edit, and Remove Persons**  
  Each person has a **Name** and a **Role** (selected from a large list of film/production roles).

- **Random Group Generation**  
  - Specify the **Number of Groups** and **Minimum Group Size**.
  - Optionally require **at least one Writer** and/or **at least one DP** in each group.
  - Distribute any extra people randomly among the groups.

- **CSV Import/Export**  
  - Import a list of persons from a CSV file.
  - Export the current persons list to a CSV file.

- **Standalone EXE (Optional)**  
  - Use [PyInstaller](https://pyinstaller.org/) to bundle Python and your script into a *single* executable.
  - No Python installation needed on the target machine.

- **Export Final Groups**  
  - Save the final, generated groups as a text file.

---

## Requirements

- *Python 3.10+*  
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (usually bundled with Python on most platforms)  
- [sv_ttk (optional)](https://github.com/rdbende/Sun-Valley-ttk-theme) for a modern UI theme  
- [PyInstaller (optional)](https://pypi.org/project/PyInstaller/) for building a standalone EXE  

---

## Installation and Usage

1. **Clone this repository** or download the source:

   ```bash
   git clone https://github.com/YourUser/YourRepo.git
   cd YourRepo
