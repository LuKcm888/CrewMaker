import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import random

# A comprehensive list of roles
ALL_ROLES = [
    "DIRECTOR",
    "PRODUCER",
    "ASSOCIATE PRODUCER",
    "EXECUTIVE PRODUCER",
    "WRITER",
    "SCREENWRITER",
    "STORY DEVELOPER",
    "DP",
    "CAMERAMAN",
    "GAFFER",
    "BEST BOY",
    "GRIP",
    "KEY GRIP",
    "ELECTRICIAN",
    "SOUND MIXER",
    "SOUND DESIGNER",
    "SOUND RECORDIST",
    "MAKEUP ARTIST",
    "HAIR STYLIST",
    "COSTUME DESIGNER",
    "COSTUMER",
    "ACTOR",
    "SUPPORTING ACTOR",
    "EXTRA",
    "SCRIPT SUPERVISOR",
    "ART DIRECTOR",
    "PRODUCTION DESIGNER",
    "SET DECORATOR",
    "LOCATION MANAGER",
    "PRODUCTION ASSISTANT",
    "STUNT COORDINATOR",
    "CHOREOGRAPHER",
    "VISUAL EFFECTS SUPERVISOR",
    "EDITOR",
    "POST-PRODUCTION SUPERVISOR",
    "COLORIST",
    "COMPOSER",
    "MUSIC SUPERVISOR",
    "CREW"
]


class AutocompleteCombobox(ttk.Combobox):
    """
    A ttk.Combobox with autocomplete functionality.
    As the user types, the drop-down list is filtered to show matching roles.
    If no match is found, a placeholder ("No match found") is shown.
    """
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault("state", "normal")
        super().__init__(master, **kwargs)
        self._completion_list = []
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list

    def handle_keyrelease(self, event):
        if event.keysym in ("Left", "Right", "Up", "Down", "Return", "Escape", "Tab"):
            return
        text = self.get()
        if text == "":
            self['values'] = self._completion_list
        else:
            filtered = [item for item in self._completion_list if text.lower() in item.lower()]
            if filtered:
                self['values'] = filtered
            else:
                self['values'] = ["No match found"]


class PersonRow(tk.Frame):
    """A row widget representing one person with an editable name and a searchable role dropdown."""
    def __init__(self, master, remove_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.remove_callback = remove_callback
        self.name_var = tk.StringVar()
        self.role_var = tk.StringVar(value="CREW")

        self.entry_name = tk.Entry(self, textvariable=self.name_var, width=25, font=("Helvetica", 10))
        self.entry_name.grid(row=0, column=0, padx=5, pady=5)

        self.combobox_role = AutocompleteCombobox(self, textvariable=self.role_var, width=20, font=("Helvetica", 10))
        self.combobox_role.set_completion_list(ALL_ROLES)
        self.combobox_role.grid(row=0, column=1, padx=5, pady=5)

        self.remove_button = ttk.Button(self, text="Remove", command=self.remove_self)
        self.remove_button.grid(row=0, column=2, padx=5, pady=5)

    def remove_self(self):
        if messagebox.askyesno("Remove Person", "Are you sure you want to remove this person?"):
            self.remove_callback(self)

    def get_data(self):
        return {
            "name": self.name_var.get().strip(),
            "role": self.role_var.get().strip()
        }


class GroupingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Group Generator")
        self.geometry("1200x900")  # Larger default window size.

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("TCombobox", font=("Helvetica", 10))
        style.configure("TLabelframe.Label", font=("Helvetica", 12, "bold"))

        self.person_rows = []
        # Variables for mandatory role rules:
        self.require_writer = tk.IntVar(value=1)
        self.require_dp = tk.IntVar(value=1)
        self.generated_groups = None  # Will store the latest groups.

        self.setup_gui()

    def setup_gui(self):
        # ---------- Main layout with two columns ----------
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)
        # Make columns 0 & 1 expand horizontally
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # ---------- Left column: Group Settings at top, Persons below ----------
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_frame.rowconfigure(0, weight=0)  # Group settings
        left_frame.rowconfigure(1, weight=1)  # Persons fill leftover space

        # Group Settings (top)
        settings_frame = ttk.Labelframe(left_frame, text="Group Settings", padding=(10, 10))
        settings_frame.grid(row=0, column=0, sticky="new", padx=5, pady=(0, 5))

        tk.Label(settings_frame, text="Number of Groups (2-10):", font=("Helvetica", 10)) \
            .grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.groups_spinbox = tk.Spinbox(settings_frame, from_=2, to=10, width=5, font=("Helvetica", 10))
        self.groups_spinbox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(settings_frame, text="Minimum Group Size (min 2):", font=("Helvetica", 10)) \
            .grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.group_size_spinbox = tk.Spinbox(settings_frame, from_=2, to=100, width=5, font=("Helvetica", 10))
        self.group_size_spinbox.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(settings_frame, text="Require one WRITER per group:", font=("Helvetica", 10)) \
            .grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Radiobutton(settings_frame, text="Enabled", variable=self.require_writer, value=1, font=("Helvetica", 10)) \
            .grid(row=1, column=1, padx=5, pady=5)
        tk.Radiobutton(settings_frame, text="Disabled", variable=self.require_writer, value=0, font=("Helvetica", 10)) \
            .grid(row=1, column=2, padx=5, pady=5)

        tk.Label(settings_frame, text="Require one DP per group:", font=("Helvetica", 10)) \
            .grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Radiobutton(settings_frame, text="Enabled", variable=self.require_dp, value=1, font=("Helvetica", 10)) \
            .grid(row=2, column=1, padx=5, pady=5)
        tk.Radiobutton(settings_frame, text="Disabled", variable=self.require_dp, value=0, font=("Helvetica", 10)) \
            .grid(row=2, column=2, padx=5, pady=5)

        ttk.Button(settings_frame, text="Generate Groups", command=self.generate_groups) \
            .grid(row=0, column=4, rowspan=3, padx=10, pady=5)

        # Persons Section (fills leftover space)
        persons_frame = ttk.Labelframe(left_frame, text="Persons", padding=(10, 10))
        persons_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        persons_frame.rowconfigure(0, weight=1)
        persons_frame.columnconfigure(0, weight=1)

        # Buttons at the top of the persons frame
        button_frame = tk.Frame(persons_frame)
        button_frame.pack(fill="x", pady=(0, 5))
        ttk.Button(button_frame, text="Import CSV", command=self.import_csv).pack(side="left", padx=5)
        ttk.Button(button_frame, text="+ Add Person", command=self.add_person_row).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all_people).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save CSV", command=self.save_csv).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Load CSV", command=self.load_csv).pack(side="left", padx=5)

        # Scrollable persons list
        persons_scroll_frame = tk.Frame(persons_frame)
        persons_scroll_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(persons_scroll_frame, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(persons_scroll_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self.rows_container = tk.Frame(self.canvas)
        self.rows_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.rows_container, anchor="nw")

        # ---------- Right column: "Generated Groups" section ----------
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Let row=1 expand
        right_frame.rowconfigure(0, weight=0)  # label
        right_frame.rowconfigure(1, weight=1)  # main area
        right_frame.rowconfigure(2, weight=0)  # bottom buttons
        right_frame.columnconfigure(0, weight=1)

        # Title
        groups_label = ttk.Label(right_frame, text="Generated Groups", font=("Helvetica", 14, "bold"))
        groups_label.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        # (IMPORTANT) Make this frame a class attribute: self.small_groups_frame
        self.small_groups_frame = tk.Frame(right_frame, bg="lightgray")
        self.small_groups_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Inside that frame, the scrollable canvas
        self.groups_canvas = tk.Canvas(self.small_groups_frame, borderwidth=0, highlightthickness=0)
        self.groups_canvas.pack(side="left", fill="both", expand=True)

        groups_scrollbar = ttk.Scrollbar(self.small_groups_frame, orient="vertical", command=self.groups_canvas.yview)
        groups_scrollbar.pack(side="right", fill="y")

        self.groups_canvas.configure(yscrollcommand=groups_scrollbar.set)
        self.groups_canvas.bind("<Enter>", lambda e: self.groups_canvas.bind_all("<MouseWheel>", self._on_groups_mousewheel))
        self.groups_canvas.bind("<Leave>", lambda e: self.groups_canvas.unbind_all("<MouseWheel>"))

        self.groups_display_container = ttk.Frame(self.groups_canvas)
        self.groups_display_container.bind(
            "<Configure>",
            lambda e: self.groups_canvas.configure(scrollregion=self.groups_canvas.bbox("all"))
        )
        self.groups_canvas.create_window((0, 0), window=self.groups_display_container, anchor="nw")

        # Buttons for Export and Clear Groups at row=2
        bottom_buttons_frame = ttk.Frame(right_frame)
        bottom_buttons_frame.grid(row=2, column=0, pady=5, sticky="ew")
        self.export_button = ttk.Button(bottom_buttons_frame, text="Export Groups", command=self.export_groups)
        self.export_button.pack(side="left", padx=5)
        self.clear_groups_button = ttk.Button(bottom_buttons_frame, text="Clear Groups", command=self.clear_generated_groups)
        self.clear_groups_button.pack(side="left", padx=5)

        # Footer
        footer = ttk.Label(self, text="© 2025 Max MacKoul Software", anchor="center", font=("Helvetica", 8))
        footer.pack(side="bottom", fill="x", padx=10, pady=5)

        # Example: set an sv_ttk theme if you want
        # sv_ttk.set_theme("dark")

    # ---------------- MOUSE WHEEL HELPERS ----------------
    def _on_mousewheel(self, event):
        """Scroll the persons canvas."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_groups_mousewheel(self, event):
        """Scroll the generated groups canvas."""
        self.groups_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---------------- PERSONS ACTIONS ----------------
    def add_person_row(self):
        row = PersonRow(self.rows_container, remove_callback=self.remove_person_row)
        row.pack(fill="x", pady=2)
        self.person_rows.append(row)

    def remove_person_row(self, row):
        row.destroy()
        self.person_rows.remove(row)

    def clear_all_people(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to remove all persons?"):
            for row in self.person_rows[:]:
                row.destroy()
            self.person_rows.clear()

    # ---------------- CSV IMPORT/EXPORT ----------------
    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if not row:
                            continue
                        name = row[0].strip() if len(row) > 0 else ""
                        role = row[1].strip() if len(row) > 1 else ""
                        if role == "" or role not in ALL_ROLES:
                            role = "CREW"
                        new_row = PersonRow(self.rows_container, remove_callback=self.remove_person_row)
                        new_row.name_var.set(name)
                        new_row.role_var.set(role)
                        new_row.pack(fill="x", pady=2)
                        self.person_rows.append(new_row)
            except Exception as e:
                messagebox.showerror("Import Error", f"An error occurred while importing the CSV:\n{e}")

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for row in self.person_rows:
                        data = row.get_data()
                        writer.writerow([data["name"], data["role"]])
                messagebox.showinfo("Save Successful", "The persons list has been saved successfully.")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving the CSV:\n{e}")

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            self.clear_all_people()
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if not row:
                            continue
                        name = row[0].strip() if len(row) > 0 else ""
                        role = row[1].strip() if len(row) > 1 else ""
                        if role == "" or role not in ALL_ROLES:
                            role = "CREW"
                        new_row = PersonRow(self.rows_container, remove_callback=self.remove_person_row)
                        new_row.name_var.set(name)
                        new_row.role_var.set(role)
                        new_row.pack(fill="x", pady=2)
                        self.person_rows.append(new_row)
                messagebox.showinfo("Load Successful", "The persons list has been loaded successfully.")
            except Exception as e:
                messagebox.showerror("Load Error", f"An error occurred while loading the CSV:\n{e}")

    # ---------------- GROUP GENERATION ----------------
    def generate_groups(self):
        random.seed()
        self.generated_groups = None
        persons = [row.get_data() for row in self.person_rows if row.get_data()["name"]]
        if not persons:
            messagebox.showerror("Input Error", "No persons added.")
            return

        try:
            num_groups = int(self.groups_spinbox.get())
            min_group_size = int(self.group_size_spinbox.get())
        except ValueError:
            messagebox.showerror("Parameter Error", "Invalid group parameters.")
            return

        if min_group_size < 2:
            messagebox.showerror("Parameter Error", "Minimum group size must be at least 2.")
            return

        total_people = len(persons)
        needed = num_groups * min_group_size
        if needed > total_people:
            feasible_num_groups = total_people // min_group_size
            if feasible_num_groups < 1:
                messagebox.showerror(
                    "Parameter Error",
                    f"Not enough people to form even one group of size {min_group_size}."
                )
                return
            num_groups = feasible_num_groups
            messagebox.showinfo(
                "Info",
                f"Not enough people to form {self.groups_spinbox.get()} groups "
                f"of size {min_group_size}. Reducing to {num_groups} groups."
            )

        require_writer = self.require_writer.get()
        require_dp = self.require_dp.get()

        writers = [p for p in persons if p["role"] == "WRITER"]
        dps = [p for p in persons if p["role"] == "DP"]

        if require_writer and len(writers) < num_groups:
            feasible_num_groups = len(writers)
            if feasible_num_groups < 1:
                messagebox.showerror("Input Error", "No WRITERS available to form a group.")
                return
            if feasible_num_groups < num_groups:
                messagebox.showinfo(
                    "Info",
                    f"Not enough WRITERs to fill {num_groups} groups. "
                    f"Reducing to {feasible_num_groups} groups."
                )
                num_groups = feasible_num_groups

        if require_dp and len(dps) < num_groups:
            feasible_num_groups = len(dps)
            if feasible_num_groups < 1:
                messagebox.showerror("Input Error", "No DPs available to form a group.")
                return
            if feasible_num_groups < num_groups:
                messagebox.showinfo(
                    "Info",
                    f"Not enough DPs to fill {num_groups} groups. "
                    f"Reducing to {feasible_num_groups} groups."
                )
                num_groups = feasible_num_groups

        groups = [[] for _ in range(num_groups)]
        remaining = persons.copy()

        if require_writer:
            random.shuffle(writers)
            for i in range(num_groups):
                assigned = writers.pop()
                groups[i].append(assigned)
                remaining.remove(assigned)

        if require_dp:
            random.shuffle(dps)
            for i in range(num_groups):
                assigned = dps.pop()
                groups[i].append(assigned)
                remaining.remove(assigned)

        for i in range(num_groups):
            while len(groups[i]) < min_group_size and remaining:
                candidate_found = False
                for j in range(len(remaining)):
                    candidate = remaining[j]
                    if require_dp and candidate["role"] == "DP":
                        dp_count = sum(1 for mem in groups[i] if mem["role"] == "DP")
                        if dp_count >= 2:
                            continue
                    groups[i].append(remaining.pop(j))
                    candidate_found = True
                    break
                if not candidate_found and remaining:
                    groups[i].append(remaining.pop(0))

        i = 0
        while remaining:
            groups[i % num_groups].append(remaining.pop(0))
            i += 1

        self.generated_groups = groups
        self.display_groups(groups)

    def display_groups(self, groups):
        # If no groups, do nothing or hide the frame
        if not groups:
            self.clear_generated_groups()
            return

        # Show the frame in case it was hidden
        self.small_groups_frame.grid()

        # Clear old content
        for widget in self.groups_display_container.winfo_children():
            widget.destroy()

        # Build new frames
        for i, group in enumerate(groups, start=1):
            group_frame = ttk.Labelframe(self.groups_display_container, text=f"Group {i}", padding=(10, 10))
            group_frame.pack(fill="x", padx=5, pady=5)
            for person in group:
                ttk.Label(group_frame, text=f"{person['name']} - {person['role']}").pack(anchor="w")

    def export_groups(self):
        if not self.generated_groups:
            messagebox.showerror("Export Error", "No groups to export. Please generate groups first.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    for i, group in enumerate(self.generated_groups, start=1):
                        f.write(f"Group {i}:\n")
                        for person in group:
                            f.write(f"{person['name']} - {person['role']}\n")
                        f.write("\n")
                messagebox.showinfo("Export Successful", "The groups have been exported successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred while exporting the groups:\n{e}")

    def clear_generated_groups(self):
        # Remove the group frames from the container
        for widget in self.groups_display_container.winfo_children():
            widget.destroy()
        self.generated_groups = None

        # Hide the frame so you don't see the gray area
        self.small_groups_frame.grid_remove()


if __name__ == "__main__":
    app = GroupingApp()
    app.mainloop()
