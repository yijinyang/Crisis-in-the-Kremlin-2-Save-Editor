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
        self.root.geometry("1200x700")
        self.root.configure(bg="#8B0000")
        
        # Define variables and their display names
        self.variables = {
            "population": "Population (millions)",
            "defcon": "DEFCON Level",
            "politicalPower": "Political Power",
            "reserve": "Reserve",
            "refinancingRate": "Refinancing Rate (%)",
            "export": "Export (billion rubles)",
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
        
        # Create GUI elements
        self.create_widgets()
        self.current_file = None
        self.saved_games_path = os.path.join(
            os.environ['USERPROFILE'], 
            'AppData', 'LocalLow', 'Nostalgames', 'CrisisInTheKremlin2', 'saved_games'
        )

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
        
        # Create main frame
        main_frame = ttk.Frame(self.root, style="Red.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create scrollable canvas
        canvas = tk.Canvas(main_frame, bg="#B22222", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas, style="Red.TFrame")
        
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")
        
        # Create entries for variables in 3 columns
        self.entries = {}
        num_columns = 3
        var_keys = list(self.variables.keys())
        items_per_col = (len(var_keys) // num_columns) + 1
        
        for col in range(num_columns):
            col_frame = ttk.Frame(self.scroll_frame, style="Gold.TFrame")
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
            self.current_file = file_path
            
            # Populate entries with data
            for var_id in self.variables:
                if var_id in data:
                    self.entries[var_id].delete(0, tk.END)
                    self.entries[var_id].insert(0, str(data[var_id]))
                # Handle potential typo in save files
                elif var_id == "warheadsQuantity" and "warheadQuantity" in data:
                    self.entries[var_id].delete(0, tk.END)
                    self.entries[var_id].insert(0, str(data["warheadQuantity"]))
            
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
            
            # Read original file content
            with open(self.current_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find the JSON portion
            match = re.search(r"({.*})", content, re.DOTALL)
            if not match:
                messagebox.showerror("Error", "Invalid save file format")
                return
                
            # Update only the specified values
            data = json.loads(match.group(1))
            for var_id, entry in self.entries.items():
                value = entry.get()
                if not value:
                    continue
                    
                if var_id in self.int_vars:
                    data[var_id] = int(value)
                else:
                    data[var_id] = float(value)
            
            # Replace JSON portion in content with original formatting
            new_json = json.dumps(data, separators=(',', ':'), indent=None)
            new_content = content.replace(match.group(1), new_json)
            
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

if __name__ == "__main__":
    root = tk.Tk()
    app = CITK2SaveEditor(root)
    root.mainloop()