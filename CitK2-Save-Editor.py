import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import re
import os
import shutil

class CITK2SaveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Crisis in the Kremlin 2 Save Editor")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)  # Set minimum size
        self.root.configure(bg="#8B0000")
        
        # Define variables and their display names
        self.variables = {
            "population": "Population (millions)",
            "defcon": "DEFCON Level",
            "politicalPower": "Political Power",
            "reserve": "Reserve",
            "refinancingRate": "Refinancing Rate (%)",
            "export": "Export",
            "healthCare": "Healthcare Funding",
            "education": "Education Funding",
            "ecology": "Ecology Funding",
            "militaryStaffLoyalty": "Military Leadership Loyalty",
            "armyStaffLoyalty": "Army Loyalty",
            "specialServicesLoyalty": "Special Services Loyalty",
            "specialServices": "Special Services Funding",
            "radicalsPower": "Radicals Power",
            "freedomLevel": "Civil Liberties",
            "liberalizationLevel": "Liberalization",
            "educationAccess": "Education Access",
            "healthCareAccess": "Health Care Access",
            "selfFulfillment": "Self Fulfillment",
            "luxuryGoodsLevel": "Luxury Goods Access",
            "orderLevel": "Law and Order Level",
            "firstNeedsGoods": "Essential Goods Access",
            "housingLevel": "Housing Level",
            "employmentLevel": "Employment Level",
            "agroEffectiveness": "Agro Effectiveness",
            "servicesEffectiveness": "Services Effectiveness",
            "lightIndustryEffectiveness": "Light Industry Power",
            "heavyIndustryEffectiveness": "Heavy Industry Power",
            "armyIndustryEffectiveness": "Military Industrial Complex Power",
            "intelligentsiaLoyalty": "Intelligentsia Loyalty",
            "spiritualContentment": "Spiritual Contentment",
            "unityLevel": "Consensus Unity",
            "forgeryLevel": "Forgery",
            "armyQuantityLevel": "Army Quantity",
            "warheadsQuantity": "Warhead Quantity",
            "combatability": "Combatability",
            "competitivenessLevel": "Competitiveness",
            "corruptionLevel": "Corruption",
            "americanArmyLevel": "American Army Combat Readiness",
            "americanEconomyLevel": "American Economy Stability",
            "americanPopularHappiness": "American Popular Satisfaction",
            "priceIndex": "Inflation",
            "usLoan": "US Loan",
            "fraLoan": "France Loan",
            "imfLoan": "IMF Loan"
        }
        
        # Identify integer variables
        self.int_vars = {
            "population", "defcon", "reserve", "refinancingRate", 
            "usLoan", "fraLoan", "imfLoan"
        }
        
        # Define complex attributes for countries and characters
        self.complex_country_attrs = {
            'pointOfInfluence': ['USA', 'France', 'USSR', 'China', 'Britain']
        }
        self.complex_character_attrs = {
            'charLevel': ['Diplomacy', 'Intrigue', 'Thrift'],
            'charExp': ['Diplomacy', 'Intrigue', 'Thrift']
        }
        
        # Define possible values for combo boxes
        self.country_options = ["Russia", "Ukraine", "Belarus", "Kazakhstan", "Uzbekistan", "Georgia", "Azerbaijan", "Lithuania", "Estonia", "Latvia", "Moldova", "Kyrgyzstan", "Tajikistan", "Armenia", "Turkmenistan"]
        self.position_options = ["ChairmanOfTheSupremeCouncil", "SecondSecretary", "ChairmanOfTheCouncilOfMinisters", "ForeignSecretary", "ChairmanOfTheKGB", "MinisterOfDefense", "MinisterOfIndustry", "MinisterForYouthAffairs", "MinisterOfFinance", "GRU", "MinisterOfAgriculture", "MinisterOfEducation", "MinisterOfInternalAffairs",None]
        self.status_options = ["Alive", "Dead", "Imprisoned", "Exiled", "Retired"]
        self.trait_options = ["ProReformist", "Compromise", "GlasnostActivist", "Schemer", "ProModerate", "Partocrat", "InefficientManager", "Atlantophobe", "Unambitious", "Uncompromising", "ProNationalDemocrat", "Monarchist", "Voluntarist", "Economical", "StrongArm", "Peoplefavorite", "EffectiveManager", "Hedonist", "Chauvinist", "ProMarket", "Ascetic", "Industrialist", "Idealist", "Peaceful", "Atlantophile", "ProLiberalDemocrat", "Technocrat", "Orientalist", "NuclearScientist", "ConspiracyTheorist", "Radical", "Intelligent", "ProConservative", "RocketBuilder", "ProNeostalinist", "ProSocialPatriot", "Dissident", "Maoist", "ProNeotrotskist"]
        
        # Create GUI elements
        self.create_widgets()
        self.current_file = None
        self.saved_games_path = os.path.join(
            os.environ['USERPROFILE'], 
            'AppData', 'LocalLow', 'Nostalgames', 'CrisisInTheKremlin2', 'saved_games'
        )
        self.data = None
        self.original_content = ""
        self.current_country = None
        self.current_character = None

    def create_widgets(self):
        # Configure styles
        self.configure_styles()
        
        # Create header frame
        header_frame = ttk.Frame(self.root, style="Gold.TFrame")
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Add title with hammer and sickle symbol
        title_label = ttk.Label(
            header_frame, 
            text="☭ CRISIS IN THE KREMLIN 2 SAVE EDITOR ☭", 
            style="Gold.TLabel",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create main tab for variables
        main_tab = ttk.Frame(notebook, style="Red.TFrame")
        notebook.add(main_tab, text="Main Variables")
        self.create_main_tab(main_tab)
        
        # Create countries tab
        countries_tab = ttk.Frame(notebook, style="Red.TFrame")
        notebook.add(countries_tab, text="Countries")
        self.create_countries_tab(countries_tab)
        
        # Create characters tab
        characters_tab = ttk.Frame(notebook, style="Red.TFrame")
        notebook.add(characters_tab, text="Characters")
        self.create_characters_tab(characters_tab)
        
        # Create button frame
        button_frame = ttk.Frame(self.root, style="Gold.TFrame")
        button_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        # Create buttons
        open_btn = ttk.Button(
            button_frame, 
            text="Open Save File", 
            command=self.open_file,
            style="Gold.TButton"
        )
        open_btn.pack(side="left", padx=20, pady=5, expand=True)
        
        save_btn = ttk.Button(
            button_frame, 
            text="Save Changes", 
            command=self.save_file,
            style="Gold.TButton"
        )
        save_btn.pack(side="left", padx=20, pady=5, expand=True)
        
        reset_btn = ttk.Button(
            button_frame, 
            text="Reset Values", 
            command=self.reset_values,
            style="Gold.TButton"
        )
        reset_btn.pack(side="left", padx=20, pady=5, expand=True)

    def create_main_tab(self, parent):
        # Create frame for action buttons
        action_frame = ttk.Frame(parent, style="Gold.TFrame")
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Add action buttons
        loyal_btn = ttk.Button(
            action_frame, 
            text="Loyal to the Cause", 
            command=self.loyal_to_cause,
            style="Gold.TButton",
            width=20
        )
        loyal_btn.pack(side="left", padx=5, pady=5, expand=True)
        
        clear_debt_btn = ttk.Button(
            action_frame, 
            text="Clear Debt", 
            command=self.clear_debt,
            style="Gold.TButton",
            width=20
        )
        clear_debt_btn.pack(side="left", padx=5, pady=5, expand=True)
        
        fall_usa_btn = ttk.Button(
            action_frame, 
            text="Fall of the USA", 
            command=self.fall_of_usa,
            style="Gold.TButton",
            width=20
        )
        fall_usa_btn.pack(side="left", padx=5, pady=5, expand=True)
        
        breakthrough_btn = ttk.Button(
            action_frame, 
            text="Scientific Breakthrough", 
            command=self.scientific_breakthrough,
            style="Gold.TButton",
            width=20
        )
        breakthrough_btn.pack(side="left", padx=5, pady=5, expand=True)
        
        # Create scrollable canvas
        canvas = tk.Canvas(parent, bg="#B22222", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas, style="Red.TFrame")
        
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")
        
        # Create entries for variables in 3 columns
        self.entries = {}
        num_columns = 3
        var_keys = list(self.variables.keys())
        items_per_col = (len(var_keys) // num_columns) + 1
        
        for col in range(num_columns):
            col_frame = ttk.Frame(scroll_frame, style="Gold.TFrame")
            col_frame.grid(row=0, column=col, padx=10, pady=10, sticky="n")
            
            # Add variables to this column
            start_index = col * items_per_col
            end_index = min((col + 1) * items_per_col, len(var_keys))
            
            for i in range(start_index, end_index):
                var_id = var_keys[i]
                display_name = self.variables[var_id]
                
                row_frame = ttk.Frame(col_frame, style="Red.TFrame")
                row_frame.pack(fill=tk.X, padx=5, pady=2)
                
                label = ttk.Label(
                    row_frame, 
                    text=f"{display_name}:", 
                    width=28, 
                    anchor="e",
                    style="Gold.TLabel"
                )
                label.pack(side="left", padx=(0, 5))
                
                entry = ttk.Entry(row_frame, width=12, style="Gold.TEntry")
                entry.pack(side="left", fill="x", expand=True)
                self.entries[var_id] = entry
                
                # Set validation based on variable type
                if var_id in self.int_vars:
                    vcmd = (self.root.register(self.validate_int), '%P')
                    entry.configure(validate="key", validatecommand=vcmd)
                else:
                    vcmd = (self.root.register(self.validate_float), '%P')
                    entry.configure(validate="key", validatecommand=vcmd)

    def create_countries_tab(self, parent):
        # Create paned window for country list and attributes
        paned_window = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Country list frame
        list_frame = ttk.Frame(paned_window, style="Gold.TFrame", width=200)
        paned_window.add(list_frame, weight=1)
        
        # Country list label and search bar
        search_frame = ttk.Frame(list_frame, style="Gold.TFrame")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            search_frame, 
            text="Search Countries:", 
            style="Gold.TLabel"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.country_search_var = tk.StringVar()
        country_search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.country_search_var,
            width=15,
            style="Gold.TEntry"
        )
        country_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        country_search_entry.bind("<KeyRelease>", self.filter_countries)
        
        ttk.Label(list_frame, text="Countries", style="Gold.TLabel", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        
        # Country listbox with scrollbar
        list_scroll = ttk.Scrollbar(list_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.country_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=list_scroll.set,
            bg="#DAA520", 
            fg="#8B0000",
            selectbackground="#8B0000",
            selectforeground="#FFD700",
            font=("Arial", 9),
            selectmode=tk.SINGLE
        )
        self.country_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        list_scroll.config(command=self.country_listbox.yview)
        
        # Bind single click instead of double click
        self.country_listbox.bind("<ButtonRelease-1>", self.on_country_select)
        self.country_listbox.bind("<Double-Button-1>", lambda e: "break")
        
        # Country attributes frame
        attr_frame = ttk.Frame(paned_window, style="Red.TFrame")
        paned_window.add(attr_frame, weight=3)
        
        # Attributes scrollable area
        attr_canvas = tk.Canvas(attr_frame, bg="#B22222", highlightthickness=0)
        attr_scroll = ttk.Scrollbar(attr_frame, orient="vertical", command=attr_canvas.yview)
        
        # Create a new frame inside the canvas for attributes
        self.country_attr_container = ttk.Frame(attr_canvas, style="Red.TFrame")
        attr_canvas.create_window((0, 0), window=self.country_attr_container, anchor="nw")
        
        self.country_attr_container.bind(
            "<Configure>",
            lambda e: attr_canvas.configure(scrollregion=attr_canvas.bbox("all"))
        )
        attr_canvas.configure(yscrollcommand=attr_scroll.set)
        
        attr_canvas.pack(side="left", fill="both", expand=True)
        attr_scroll.pack(side="right", fill="y")
        
        # Create frame for country action buttons (VERTICAL LAYOUT)
        country_actions_frame = ttk.Frame(attr_frame, style="Gold.TFrame")
        country_actions_frame.pack(side="right", fill=tk.Y, padx=(5, 0), pady=5)
        
        # Add country action buttons (packed vertically)
        diplo_btn = ttk.Button(
            country_actions_frame, 
            text="Diplomatic Superparty", 
            command=self.diplomatic_superparty,
            style="Gold.TButton"
        )
        diplo_btn.pack(fill=tk.X, padx=2, pady=2)
        
        mass_align_btn = ttk.Button(
            country_actions_frame, 
            text="Mass Alignment", 
            command=self.mass_alignment,
            style="Gold.TButton"
        )
        mass_align_btn.pack(fill=tk.X, padx=2, pady=2)
        
        liberal0_btn = ttk.Button(
            country_actions_frame, 
            text="Liberalization Vector 0", 
            command=self.liberalization_vector_0,
            style="Gold.TButton"
        )
        liberal0_btn.pack(fill=tk.X, padx=2, pady=2)
        
        liberal_res_btn = ttk.Button(
            country_actions_frame, 
            text="Liberal Resurrection",  
            command=self.liberalization_vector_100,
            style="Gold.TButton"
        )
        liberal_res_btn.pack(fill=tk.X, padx=2, pady=2)
        
        # Save country button
        save_btn = ttk.Button(
            country_actions_frame, 
            text="Save Country Changes", 
            command=self.save_country,
            style="Gold.TButton"
        )
        save_btn.pack(fill=tk.X, padx=2, pady=2)

    def create_characters_tab(self, parent):
        # Create paned window for character list and attributes
        paned_window = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Character list frame
        list_frame = ttk.Frame(paned_window, style="Gold.TFrame", width=200)
        paned_window.add(list_frame, weight=1)
        
        # Character list label and search bar
        search_frame = ttk.Frame(list_frame, style="Gold.TFrame")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            search_frame, 
            text="Search Characters:", 
            style="Gold.TLabel"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.character_search_var = tk.StringVar()
        character_search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.character_search_var,
            width=15,
            style="Gold.TEntry"
        )
        character_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        character_search_entry.bind("<KeyRelease>", self.filter_characters)
        
        ttk.Label(list_frame, text="Characters", style="Gold.TLabel", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        
        # Character listbox with scrollbar
        list_scroll = ttk.Scrollbar(list_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.character_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=list_scroll.set,
            bg="#DAA520", 
            fg="#8B0000",
            selectbackground="#8B0000",
            selectforeground="#FFD700",
            font=("Arial", 9),
            selectmode=tk.SINGLE
        )
        self.character_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        list_scroll.config(command=self.character_listbox.yview)
        
        # Bind single click instead of double click
        self.character_listbox.bind("<ButtonRelease-1>", self.on_character_select)
        self.character_listbox.bind("<Double-Button-1>", lambda e: "break")
        
        # Character attributes frame
        attr_frame = ttk.Frame(paned_window, style="Red.TFrame")
        paned_window.add(attr_frame, weight=3)
        
        # Attributes scrollable area
        attr_canvas = tk.Canvas(attr_frame, bg="#B22222", highlightthickness=0)
        attr_scroll = ttk.Scrollbar(attr_frame, orient="vertical", command=attr_canvas.yview)
        
        # Create a new frame inside the canvas for attributes
        self.character_attr_container = ttk.Frame(attr_canvas, style="Red.TFrame")
        attr_canvas.create_window((0, 0), window=self.character_attr_container, anchor="nw")
        
        self.character_attr_container.bind(
            "<Configure>",
            lambda e: attr_canvas.configure(scrollregion=attr_canvas.bbox("all"))
        )
        attr_canvas.configure(yscrollcommand=attr_scroll.set)
        
        attr_canvas.pack(side="left", fill="both", expand=True)
        attr_scroll.pack(side="right", fill="y")
        
        # Create frame for character action buttons (VERTICAL LAYOUT)
        char_actions_frame = ttk.Frame(attr_frame, style="Gold.TFrame")
        char_actions_frame.pack(side="right", fill=tk.Y, padx=(5, 0), pady=5)
        
        # Add character action buttons (packed vertically)
        assassinate_btn = ttk.Button(
            char_actions_frame, 
            text="Assassinate", 
            command=lambda: self.set_character_status("Dead"),
            style="Gold.TButton"
        )
        assassinate_btn.pack(fill=tk.X, padx=2, pady=2)
        
        imprison_btn = ttk.Button(
            char_actions_frame, 
            text="Imprison", 
            command=lambda: self.set_character_status("Imprisoned"),
            style="Gold.TButton"
        )
        imprison_btn.pack(fill=tk.X, padx=2, pady=2)
        
        exile_btn = ttk.Button(
            char_actions_frame, 
            text="Exile", 
            command=lambda: self.set_character_status("Exiled"),
            style="Gold.TButton"
        )
        exile_btn.pack(fill=tk.X, padx=2, pady=2)
        
        retire_btn = ttk.Button(
            char_actions_frame, 
            text="Retire", 
            command=lambda: self.set_character_status("Retired"),
            style="Gold.TButton"
        )
        retire_btn.pack(fill=tk.X, padx=2, pady=2)
        
        resurrect_btn = ttk.Button(
            char_actions_frame, 
            text="Resurrect", 
            command=lambda: self.set_character_status("Alive"),
            style="Gold.TButton"
        )
        resurrect_btn.pack(fill=tk.X, padx=2, pady=2)
        
        empower_btn = ttk.Button(
            char_actions_frame, 
            text="Empower", 
            command=lambda: self.set_character_power(100),
            style="Gold.TButton"
        )
        empower_btn.pack(fill=tk.X, padx=2, pady=2)
        
        isolate_btn = ttk.Button(
            char_actions_frame, 
            text="Isolate", 
            command=lambda: self.set_character_power(0),
            style="Gold.TButton"
        )
        isolate_btn.pack(fill=tk.X, padx=2, pady=2)
        
        # Save character button
        save_btn = ttk.Button(
            char_actions_frame, 
            text="Save Character Changes", 
            command=self.save_character,
            style="Gold.TButton"
        )
        save_btn.pack(fill=tk.X, padx=2, pady=2)

    def configure_styles(self):
        style = ttk.Style()
        
        # Background colors
        style.configure("Red.TFrame", background="#8B0000")
        style.configure("Gold.TFrame", background="#DAA520")
        
        # Label styles
        style.configure("Gold.TLabel", 
                       background="#DAA520", 
                       foreground="#8B0000",  # Dark red text
                       font=("Arial", 9))
        
        # Entry styles
        style.configure("Gold.TEntry", 
                       fieldbackground="#FFD700",  # Gold background
                       foreground="#8B0000",  # Dark red text
                       insertcolor="#8B0000")
        
        # Button styles
        style.configure("Gold.TButton", 
                       background="#DAA520", 
                       foreground="#8B0000",
                       font=("Arial", 10, "bold"),
                       borderwidth=2,
                       focusthickness=0,
                       focuscolor="#DAA520")
        style.map("Gold.TButton",
                 background=[('active', '#FFD700')],
                 foreground=[('active', '#8B0000')])
        
        # Checkbutton styles
        style.configure("Gold.TCheckbutton", 
                       background="#DAA520", 
                       foreground="#8B0000")
        
        # Combobox styles
        style.configure("Gold.TCombobox", 
                       fieldbackground="#FFD700", 
                       foreground="#8B0000",
                       selectbackground="#FFD700",
                       selectforeground="#8B0000")

    def validate_float(self, value):
        """Validate float input"""
        if value == "" or value == "-":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_int(self, value):
        """Validate integer input"""
        if value == "" or value == "-":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
        
    def filter_countries(self, event=None):
        """Filter country list based on search text"""
        if not hasattr(self, 'all_countries'):
            return
            
        search_text = self.country_search_var.get().lower()
        self.country_listbox.delete(0, tk.END)
        
        if not search_text:
            # Show all countries if search is empty
            for country in self.all_countries:
                self.country_listbox.insert(tk.END, country)
        else:
            # Filter countries that match search text
            for country in self.all_countries:
                if search_text in country.lower():
                    self.country_listbox.insert(tk.END, country)

    def filter_characters(self, event=None):
        """Filter character list based on search text"""
        if not hasattr(self, 'all_characters'):
            return
            
        search_text = self.character_search_var.get().lower()
        self.character_listbox.delete(0, tk.END)
        
        if not search_text:
            # Show all characters if search is empty
            for character in self.all_characters:
                self.character_listbox.insert(tk.END, character)
        else:
            # Filter characters that match search text
            for character in self.all_characters:
                if search_text in character.lower():
                    self.character_listbox.insert(tk.END, character)

    def open_file(self):
        """Open a CITK2 save file from default directory"""
        initial_dir = self.saved_games_path
        if not os.path.exists(initial_dir):
            initial_dir = os.path.expanduser("~")
        
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            filetypes=[("CITK2 Save Files", "*.citk2save"), ("All Files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract JSON-like data from the file
            match = re.search(r"({.*})", content, re.DOTALL)
            if not match:
                messagebox.showerror("Error", "Invalid save file format")
                return
                
            data = json.loads(match.group(1))
            self.data = data  # Store entire data
            self.original_content = content  # Store original content
            self.current_file = file_path
            
            # Populate main variables
            for var_id in self.variables:
                if var_id in data:
                    self.entries[var_id].delete(0, tk.END)
                    self.entries[var_id].insert(0, str(data[var_id]))
                # Handle potential typo in save files
                elif var_id == "warheadsQuantity" and "warheadQuantity" in data:
                    self.entries[var_id].delete(0, tk.END)
                    self.entries[var_id].insert(0, str(data["warheadQuantity"]))
            
            # Populate country list
            if "countries" in data:
                self.all_countries = list(data["countries"].keys())  # Store for filtering
                self.country_listbox.delete(0, tk.END)
                for country_tag in self.all_countries:
                    self.country_listbox.insert(tk.END, country_tag)
            
            # Populate character list
            if "characters" in data:
                self.all_characters = list(data["characters"].keys())  # Store for filtering
                self.character_listbox.delete(0, tk.END)
                for character_name in self.all_characters:
                    self.character_listbox.insert(tk.END, character_name)
            
            messagebox.showinfo("Success", "Comrade! File loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def save_file(self):
        """Save changes back to file with backup"""
        if not self.current_file:
            messagebox.showwarning("Warning", "No file loaded")
            return
            
        try:
            # Create backup
            backup_path = self.current_file + ".bak"
            shutil.copyfile(self.current_file, backup_path)
            
            # Update main variables in data
            for var_id, entry in self.entries.items():
                value = entry.get()
                if not value:
                    continue
                    
                if var_id in self.int_vars:
                    self.data[var_id] = int(value)
                else:
                    self.data[var_id] = float(value)
            
            # Convert data back to JSON
            new_json = json.dumps(self.data, separators=(',', ':'), indent=None)
            
            # Replace JSON portion in content
            new_content = re.sub(r"{.*}", new_json, self.original_content, flags=re.DOTALL)
            
            # Write back to file
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            messagebox.showinfo("Success", f"Comrade! File saved successfully!\nBackup created at {backup_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def reset_values(self):
        """Reset all entry fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def on_country_select(self, event):
        """Handle country selection from listbox"""
        # Clear previous attributes
        for widget in self.country_attr_container.winfo_children():
            widget.destroy()
        
        # Get selected country
        selection = self.country_listbox.curselection()
        if not selection:
            return
            
        country_tag = self.country_listbox.get(selection[0])
        # Only proceed if we have a valid country
        if not country_tag:
            return
            
        self.current_country = country_tag
        country_data = self.data["countries"][country_tag]
        
        # Create a new frame to hold all attributes
        self.country_attr_frame = ttk.Frame(self.country_attr_container, style="Red.TFrame")
        self.country_attr_frame.pack(fill="both", expand=True)
        
        # Display country tag
        tag_frame = ttk.Frame(self.country_attr_frame, style="Gold.TFrame")
        tag_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(
            tag_frame, 
            text=f"Editing: {country_tag}", 
            style="Gold.TLabel",
            font=("Arial", 11, "bold")
        ).pack()
        
        # Create attribute entries
        self.country_entries = {}
        for attr, value in country_data.items():
            # Skip complex attributes (handled separately)
            if attr in self.complex_country_attrs:
                continue
                
            # Create frame for this attribute
            frame = ttk.Frame(self.country_attr_frame, style="Red.TFrame")
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Create label
            label = ttk.Label(frame, text=f"{attr}:", width=25, anchor="e", style="Gold.TLabel")
            label.pack(side=tk.LEFT, padx=(0, 5))
            
            # Create entry based on value type
            if isinstance(value, bool):
                var = tk.BooleanVar(value=value)
                entry = ttk.Checkbutton(frame, variable=var, style="Gold.TCheckbutton")
                entry.var = var  # Store var for later access
            elif value is None:
                entry = ttk.Entry(frame, width=20, style="Gold.TEntry")
                entry.insert(0, "null")
            else:
                entry = ttk.Entry(frame, width=20, style="Gold.TEntry")
                entry.insert(0, str(value))
                
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.country_entries[attr] = entry
        
        # Add complex attributes
        for complex_attr, sub_attrs in self.complex_country_attrs.items():
            if complex_attr not in country_data:
                continue
                
            # Header for complex attribute
            complex_frame = ttk.Frame(self.country_attr_frame, style="Gold.TFrame")
            complex_frame.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(
                complex_frame, 
                text=f"{complex_attr}:", 
                style="Gold.TLabel",
                font=("Arial", 10, "bold")
            ).pack(anchor="w")
            
            # Create sub-attributes
            for sub_attr in sub_attrs:
                frame = ttk.Frame(self.country_attr_frame, style="Red.TFrame")
                frame.pack(fill=tk.X, padx=20, pady=2)
                
                # Create label
                label = ttk.Label(frame, text=f"{sub_attr}:", width=20, anchor="e", style="Gold.TLabel")
                label.pack(side=tk.LEFT, padx=(0, 5))
                
                # Create entry
                sub_value = country_data[complex_attr].get(sub_attr, 0.0)
                entry = ttk.Entry(frame, width=15, style="Gold.TEntry")
                entry.insert(0, str(sub_value))
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.country_entries[f"{complex_attr}_{sub_attr}"] = entry

    def save_country(self):
        """Save changes to the currently selected country"""
        if not self.current_country or not self.data:
            return
            
        try:
            country_data = self.data["countries"][self.current_country]
            
            # Update simple attributes
            for attr, entry in self.country_entries.items():
                # Skip complex sub-attributes
                if any(key in attr for key in self.complex_country_attrs):
                    continue
                    
                # Get value based on widget type
                if isinstance(entry, ttk.Checkbutton):
                    value = entry.var.get()
                else:
                    value_str = entry.get()
                    if value_str == "null":
                        value = None
                    elif value_str.lower() == "true":
                        value = True
                    elif value_str.lower() == "false":
                        value = False
                    else:
                        try:
                            value = int(value_str)
                        except ValueError:
                            try:
                                value = float(value_str)
                            except ValueError:
                                value = value_str
                
                # Update data
                country_data[attr] = value
            
            # Update complex attributes
            for complex_attr in self.complex_country_attrs:
                if complex_attr not in country_data:
                    continue
                    
                for sub_attr in self.complex_country_attrs[complex_attr]:
                    entry_key = f"{complex_attr}_{sub_attr}"
                    if entry_key not in self.country_entries:
                        continue
                        
                    try:
                        value = float(self.country_entries[entry_key].get())
                        country_data[complex_attr][sub_attr] = value
                    except ValueError:
                        pass  # Keep original value if invalid
            
            messagebox.showinfo("Success", f"{self.current_country} updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save country:\n{str(e)}")

    def on_character_select(self, event):
        """Handle character selection from listbox"""
        # Clear previous attributes
        for widget in self.character_attr_container.winfo_children():
            widget.destroy()
        
        # Get selected character
        selection = self.character_listbox.curselection()
        if not selection:
            return
            
        char_name = self.character_listbox.get(selection[0])
        # Only proceed if we have a valid character
        if not char_name:
            return
            
        self.current_character = char_name
        char_data = self.data["characters"][char_name]
        
        # Create a new frame to hold all attributes
        self.character_attr_frame = ttk.Frame(self.character_attr_container, style="Red.TFrame")
        self.character_attr_frame.pack(fill="both", expand=True)
        
        # Display character name
        name_frame = ttk.Frame(self.character_attr_frame, style="Gold.TFrame")
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(
            name_frame, 
            text=f"Editing: {char_name}", 
            style="Gold.TLabel",
            font=("Arial", 11, "bold")
        ).pack()
        
        # Create attribute entries
        self.character_entries = {}
        for attr, value in char_data.items():
            # Skip complex attributes (handled separately)
            if attr in self.complex_character_attrs:
                continue
                
            # Create frame for this attribute
            frame = ttk.Frame(self.character_attr_frame, style="Red.TFrame")
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Create label
            label = ttk.Label(frame, text=f"{attr}:", width=25, anchor="e", style="Gold.TLabel")
            label.pack(side=tk.LEFT, padx=(0, 5))
            
            # Create entry based on value type
            if isinstance(value, bool):
                var = tk.BooleanVar(value=value)
                entry = ttk.Checkbutton(frame, variable=var, style="Gold.TCheckbutton")
                entry.var = var  # Store var for later access
            elif attr == "homeLand":
                combo = ttk.Combobox(frame, width=18, style="Gold.TCombobox")
                combo['values'] = self.country_options
                combo.set(value if value else "")
                entry = combo
            elif attr == "desiredPosition":
                combo = ttk.Combobox(frame, width=18, style="Gold.TCombobox")
                combo['values'] = self.position_options
                combo.set(value if value else "")
                entry = combo
            elif attr == "status":
                combo = ttk.Combobox(frame, width=18, style="Gold.TCombobox")
                combo['values'] = self.status_options
                combo.set(value if value else "")
                entry = combo
            elif attr == "traits":
                # Skip here, handle separately below
                continue
            elif value is None:
                entry = ttk.Entry(frame, width=20, style="Gold.TEntry")
                entry.insert(0, "null")
            else:
                entry = ttk.Entry(frame, width=20, style="Gold.TEntry")
                entry.insert(0, str(value))
                
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.character_entries[attr] = entry
        
        # Add traits section with four combo boxes
        traits_frame = ttk.Frame(self.character_attr_frame, style="Gold.TFrame")
        traits_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(
            traits_frame, 
            text="Traits:", 
            style="Gold.TLabel",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")
        
        self.trait_combos = []
        traits = char_data.get("traits", [])
        
        # Ensure we have exactly 4 traits (pad with empty if needed)
        if len(traits) < 4:
            traits += [""] * (4 - len(traits))
        elif len(traits) > 4:
            traits = traits[:4]
        
        for i, trait in enumerate(traits, 1):
            frame = ttk.Frame(self.character_attr_frame, style="Red.TFrame")
            frame.pack(fill=tk.X, padx=20, pady=2)
            
            label = ttk.Label(frame, text=f"Trait {i}:", width=20, anchor="e", style="Gold.TLabel")
            label.pack(side=tk.LEFT, padx=(0, 5))
            
            combo = ttk.Combobox(frame, width=18, style="Gold.TCombobox")
            combo['values'] = self.trait_options
            combo.set(trait if trait else "")
            combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.trait_combos.append(combo)
        
        # Add complex attributes
        for complex_attr, sub_attrs in self.complex_character_attrs.items():
            if complex_attr not in char_data:
                continue
                
            # Header for complex attribute
            complex_frame = ttk.Frame(self.character_attr_frame, style="Gold.TFrame")
            complex_frame.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(
                complex_frame, 
                text=f"{complex_attr}:", 
                style="Gold.TLabel",
                font=("Arial", 10, "bold")
            ).pack(anchor="w")
            
            # Create sub-attributes
            for sub_attr in sub_attrs:
                frame = ttk.Frame(self.character_attr_frame, style="Red.TFrame")
                frame.pack(fill=tk.X, padx=20, pady=2)
                
                # Create label
                label = ttk.Label(frame, text=f"{sub_attr}:", width=20, anchor="e", style="Gold.TLabel")
                label.pack(side=tk.LEFT, padx=(0, 5))
                
                # Create entry
                sub_value = char_data[complex_attr].get(sub_attr, 0)
                entry = ttk.Entry(frame, width=15, style="Gold.TEntry")
                entry.insert(0, str(sub_value))
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.character_entries[f"{complex_attr}_{sub_attr}"] = entry

    def save_character(self):
        """Save changes to the currently selected character"""
        if not self.current_character or not self.data:
            return
            
        try:
            char_data = self.data["characters"][self.current_character]
            
            # Update simple attributes
            for attr, entry in self.character_entries.items():
                # Skip complex sub-attributes
                if any(key in attr for key in self.complex_character_attrs):
                    continue
                    
                # Special handling for traits (handled separately)
                if attr == "traits":
                    continue
                    
                # Get value based on widget type
                if isinstance(entry, ttk.Checkbutton):
                    value = entry.var.get()
                elif isinstance(entry, ttk.Combobox):
                    value = entry.get()
                    # Convert to appropriate type if needed
                    if value == "null":
                        value = None
                    elif value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False
                    elif value.isdigit():
                        value = int(value)
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            pass  # Keep as string
                else:  # Regular entry
                    value_str = entry.get()
                    if value_str == "null":
                        value = None
                    elif value_str.lower() == "true":
                        value = True
                    elif value_str.lower() == "false":
                        value = False
                    else:
                        try:
                            value = int(value_str)
                        except ValueError:
                            try:
                                value = float(value_str)
                            except ValueError:
                                value = value_str
                
                # Update data
                char_data[attr] = value
            
            # Update traits from combo boxes
            traits_list = []
            for combo in self.trait_combos:
                trait = combo.get().strip()
                if trait:  # Only add non-empty traits
                    traits_list.append(trait)
            char_data["traits"] = traits_list
            
            # Update complex attributes
            for complex_attr in self.complex_character_attrs:
                if complex_attr not in char_data:
                    continue
                    
                for sub_attr in self.complex_character_attrs[complex_attr]:
                    entry_key = f"{complex_attr}_{sub_attr}"
                    if entry_key not in self.character_entries:
                        continue
                        
                    try:
                        value = float(self.character_entries[entry_key].get())
                        char_data[complex_attr][sub_attr] = value
                    except ValueError:
                        pass  # Keep original value if invalid
            
            messagebox.showinfo("Success", f"{self.current_character} updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save character:\n{str(e)}")

    # ====== NEW FUNCTIONS FOR ACTION BUTTONS ======
    
    def loyal_to_cause(self):
        """Set loyalty variables to 100"""
        loyal_vars = [
            "specialServicesLoyalty", 
            "militaryStaffLoyalty", 
            "armyStaffLoyalty", 
            "intelligentsiaLoyalty"
        ]
        
        for var in loyal_vars:
            if var in self.entries:
                self.entries[var].delete(0, tk.END)
                self.entries[var].insert(0, "100")
        
        messagebox.showinfo("Loyal to the Cause", "Loyalty variables set to 100!")

    def clear_debt(self):
        """Set all loan variables to 0"""
        debt_vars = ["usLoan", "fraLoan", "imfLoan"]
        
        for var in debt_vars:
            if var in self.entries:
                self.entries[var].delete(0, tk.END)
                self.entries[var].insert(0, "0")
        
        messagebox.showinfo("Clear Debt", "All loans cleared!")

    def fall_of_usa(self):
        """Set American variables to 0"""
        usa_vars = [
            "americanArmyLevel", 
            "americanEconomyLevel", 
            "americanPopularHappiness"
        ]
        
        for var in usa_vars:
            if var in self.entries:
                self.entries[var].delete(0, tk.END)
                self.entries[var].insert(0, "0")
        
        messagebox.showinfo("Fall of the USA", "American variables set to 0!")
        
    def scientific_breakthrough(self):
        """Set all technology points to 1000"""
        if not self.data or "technologies" not in self.data:
            messagebox.showwarning("Warning", "No technology data available")
            return
            
        try:
            # Iterate through all technology categories
            for category, tech_list in self.data["technologies"].items():
                # Iterate through each technology level in the category
                for tech in tech_list:
                    # Set all point types to 1000
                    if "investedCost" in tech:
                        tech["investedCost"] = {
                            "militaryPoints": 1000,
                            "physicPoints": 1000,
                            "cyberneticPoints": 1000,
                            "civilPoints": 1000
                        }
            
            messagebox.showinfo("Scientific Breakthrough", 
                               "All technology points set to 1000!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update technologies:\n{str(e)}")

    def diplomatic_superparty(self):
        """Set relationshipWithPlayer to 100 for all active countries"""
        if not self.data or "countries" not in self.data:
            messagebox.showwarning("Warning", "No country data available")
            return
            
        count = 0
        for country_tag, country_data in self.data["countries"].items():
            if country_data.get("activeInGame", False):
                if "relationshipWithPlayer" in country_data:
                    country_data["relationshipWithPlayer"] = 100
                    count += 1
        
        messagebox.showinfo("Diplomatic Superparty", 
                           f"Set relationship to 100 for {count} active countries!")

    def mass_alignment(self):
        """Set foreignPolicyVector to 100 for all active countries"""
        if not self.data or "countries" not in self.data:
            messagebox.showwarning("Warning", "No country data available")
            return
            
        count = 0
        for country_tag, country_data in self.data["countries"].items():
            if country_data.get("activeInGame", False):
                if "foreignPolicyVector" in country_data:
                    country_data["foreignPolicyVector"] = 100
                    count += 1
        
        messagebox.showinfo("Mass Alignment", 
                           f"Set foreign policy to 100 for {count} active countries!")

    def liberalization_vector_0(self):
        """Set liberalizationVector to 0 for all active countries"""
        if not self.data or "countries" not in self.data:
            messagebox.showwarning("Warning", "No country data available")
            return
            
        count = 0
        for country_tag, country_data in self.data["countries"].items():
            if country_data.get("activeInGame", False):
                if "liberalizationVector" in country_data:
                    country_data["liberalizationVector"] = 0
                    count += 1
        
        messagebox.showinfo("Liberalization Vector 0", 
                           f"Set liberalization to 0 for {count} active countries!")
        
    def liberalization_vector_100(self):
        """Set liberalizationVector to 100 for all active countries"""
        if not self.data or "countries" not in self.data:
            messagebox.showwarning("Warning", "No country data available")
            return
            
        count = 0
        for country_tag, country_data in self.data["countries"].items():
            if country_data.get("activeInGame", False):
                if "liberalizationVector" in country_data:
                    country_data["liberalizationVector"] = 100
                    count += 1
        
        messagebox.showinfo("Liberalization Vector 190", 
                           f"Set liberalization to 100 for {count} active countries!")

    def set_character_status(self, status):
        """Set status for the selected character"""
        if not self.current_character or not self.data:
            messagebox.showwarning("Warning", "No character selected")
            return
            
        if "characters" not in self.data or self.current_character not in self.data["characters"]:
            messagebox.showwarning("Warning", "Character data not available")
            return
            
        # Update the status
        char_data = self.data["characters"][self.current_character]
        char_data["status"] = status
        
        # Update the UI if we're currently editing this character
        if "status" in self.character_entries:
            self.character_entries["status"].set(status)
        
        messagebox.showinfo("Status Changed", 
                           f"{self.current_character} status set to {status}!")

    def set_character_power(self, power_value):
        """Set power for the selected character"""
        if not self.current_character or not self.data:
            messagebox.showwarning("Warning", "No character selected")
            return
            
        if "characters" not in self.data or self.current_character not in self.data["characters"]:
            messagebox.showwarning("Warning", "Character data not available")
            return
            
        # Update the power
        char_data = self.data["characters"][self.current_character]
        char_data["power"] = power_value
        
        # Update the UI if we're currently editing this character
        if "power" in self.character_entries:
            self.character_entries["power"].delete(0, tk.END)
            self.character_entries["power"].insert(0, str(power_value))
        
        messagebox.showinfo("Power Changed", 
                           f"{self.current_character} power set to {power_value}!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CITK2SaveEditor(root)
    root.mainloop()