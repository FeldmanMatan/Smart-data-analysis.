import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import pandas as pd
import plotly.express as px
from data_processing import show_graph, show_average, show_count, show_dates
from data_model import DataModel
from export import export_to_html, export_to_csv, export_to_excel, export_to_json
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class CSVLoaderApp:
    def __init__(self, root):

        self.root = root

        self.root.title("CSV to DataFrame Viewer")
        self.root.geometry("1200x700")
        # Initialize data model
        self.data_model = DataModel()


        # Create main menu
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load CSV/Excel", command=self.load_csv)
        self.file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        self.file_menu.add_command(label="Export to Excel", command=self.export_to_excel)
        self.file_menu.add_command(label="Export to JSON", command=self.export_to_json)
        self.file_menu.add_command(label="Export to HTML", command=self.export_to_html)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Clear Filters", command=self.clear_filters)
        self.view_menu.add_command(label="Query History", command=self.show_history)

        # יצירת מסגרת לכפתורים עליונים
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill=tk.X, pady=5)

        # שורת פעולות מרכזיות
        self.load_button = tk.Button(self.top_frame, text="Load Data File", command=self.load_csv,
                                     bg="#4CAF50", fg="white", padx=10)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.clear_filters_button = tk.Button(self.top_frame, text="Clear Filters", command=self.clear_filters,
                                              bg="#2196F3", fg="white", padx=10)
        self.clear_filters_button.pack(side=tk.LEFT, padx=5)

        self.export_html_button = tk.Button(self.top_frame, text="Export HTML", command=self.export_to_html,
                                            bg="#FF9800", fg="white", padx=10)
        self.export_html_button.pack(side=tk.LEFT, padx=5)

        # הצגת שם הקובץ הנוכחי
        self.current_file_label = tk.Label(self.top_frame, text="No file loaded", fg="gray")
        self.current_file_label.pack(side=tk.RIGHT, padx=10)

        # לעדכן את עיצוב שורת החיפוש
        query_frame = tk.Frame(self.root)
        query_frame.pack(fill=tk.X, pady=5, padx=10)

        self.query_label = tk.Label(query_frame, text="Query:", font=("Arial", 10, "bold"))
        self.query_label.pack(side=tk.LEFT, padx=5)

        self.query_entry = tk.Entry(query_frame, width=50, font=("Arial", 10))
        self.query_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.query_entry.bind("<Return>", self.handle_query)

        self.query_button = tk.Button(query_frame, text="Run Query", command=lambda: self.handle_query(),
                                      bg="#673AB7", fg="white", padx=10)
        self.query_button.pack(side=tk.RIGHT, padx=5)

        # הוספת tooltips לאלמנטים
        self.create_tooltip(self.load_button, "Load CSV or Excel file")
        self.create_tooltip(self.clear_filters_button, "Remove all applied filters")
        self.create_tooltip(self.query_entry,
                            "Enter query like 'plot with Column1 and Column2' or 'average of Column1'")

        # Table frame
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview with Scrollbars
        self.tree = ttk.Treeview(self.table_frame, show="headings", style="Custom.Treeview")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_x = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scroll_x.pack(fill=tk.X)

        self.tree.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.current_directory = None



        # Configure style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview", rowheight=25)
        style.configure("Custom.Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Custom.Treeview", borderwidth=1, relief="solid")
        style.layout("Custom.Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    def create_tooltip(self, widget, text):
        """Create a tooltip for a given widget"""

        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20

            # יצירת חלון עליון להצגת הטקסט
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")

            label = tk.Label(self.tooltip, text=text, justify=tk.LEFT,
                             background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                             font=("Arial", "9", "normal"))
            label.pack(ipadx=3, ipady=2)

        def leave(event):
            if hasattr(self, "tooltip"):
                self.tooltip.destroy()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def load_csv(self):
        """Loads CSV or Excel file and displays data"""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx;*.xls")])
        if file_path:
            try:
                logging.info(f"Loading file: {file_path}")
                #שמירת מיקום הקובץ
                print(f"file_path = {file_path}")
                temp = file_path.replace(file_path.split('/')[-1],"")
                self.current_directory = temp # os.path.dirname(temp)
                self.data_model.load_data(file_path)
                self.display_dataframe()
                self.current_file_label.config(text=f"Current file: {file_path.split('/')[-1]}")
                messagebox.showinfo("Success", f"File loaded successfully: {file_path}")
            except Exception as e:
                logging.error(f"Error loading file: {str(e)}")
                messagebox.showerror("Error", f"Error loading file: {e}")

    # def load_csv(self):
    #     """Loads CSV or Excel file and displays data"""
    #     file_path = filedialog.askopenfilename(
    #         filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx;*.xls")])
    #     if file_path:
    #         try:
    #             logging.info(f"Loading file: {file_path}")
    #
    #             # שמירת מיקום הקובץ
    #             self.current_directory = os.path.dirname(file_path)
    #
    #             self.data_model.load_data(file_path)
    #             self.display_dataframe()
    #             self.current_file_label.config(text=f"Current file: {file_path.split('/')[-1]}")
    #             messagebox.showinfo("Success", f"File loaded successfully: {file_path}")
    #         except Exception as e:
    #             logging.error(f"Error loading file: {str(e)}")
    #             messagebox.showerror("Error", f"Error loading file: {e}")

    def display_dataframe(self):
        """Displays the dataframe in the treeview"""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.data_model.filtered_df.columns)

        # Setup column headers with context menus
        for col in self.data_model.filtered_df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", width=150, minwidth=100, stretch=True)

            # Bind right-click event to headers
            self.tree.heading(col, command=lambda c=col: self.show_column_menu(c))

        # Display rows in table (max 200 rows to prevent crashes)
        for i, (_, row) in enumerate(self.data_model.filtered_df.head(200).iterrows()):
            values = list(row)
            self.tree.insert("", "end", values=values, iid=i)

        # Update scrollbar to ensure it's working after populating the tree
        self.tree.yview_moveto(0)

        # Log the action
        logging.info(
            f"Displayed dataframe with {len(self.data_model.filtered_df)} rows and {len(self.data_model.filtered_df.columns)} columns")

    def show_column_menu(self, column):
        """Shows the column context menu for filtering and sorting"""
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()

        # Create popup menu
        popup = tk.Menu(self.root, tearoff=0)
        popup.add_command(label=f"Filter {column}...", command=lambda: self.apply_filter(column))
        popup.add_command(label="Sort Ascending", command=lambda: self.sort_column(column, True))
        popup.add_command(label="Sort Descending", command=lambda: self.sort_column(column, False))

        # Show menu at current mouse position
        popup.tk_popup(x, y)

    def sort_column(self, column, ascending=True):
        """Sort the dataframe by column and redisplay"""
        try:
            self.data_model.sort_by(column, ascending)
            self.display_dataframe()
        except Exception as e:
            messagebox.showerror("Sorting Error", str(e))

    def apply_filter(self, column):
        """Applies filter to a column"""
        if self.data_model.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return

        # Ask for filter type
        filter_type = simpledialog.askstring("Filter Type",
                                             "Enter filter type (greater, less, equal, contains):",
                                             initialvalue="contains")
        if not filter_type:
            return

        filter_value = simpledialog.askstring(f"Filter {column}", f"Enter value to filter {column}:")
        if filter_value:
            try:
                self.data_model.apply_filter(column, filter_type, filter_value)
                self.display_dataframe()
            except Exception as e:
                messagebox.showerror("Filter Error", str(e))

    def clear_filters(self):
        """Clears all filters and redisplays the data"""
        self.data_model.clear_filters()
        self.display_dataframe()

    def show_history(self):
        """Shows the query history in a new window"""
        history = self.data_model.get_history()
        if not history:
            messagebox.showinfo("Query History", "No queries in history.")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Query History")
        history_window.geometry("500x300")

        history_list = tk.Listbox(history_window, width=80, height=15)
        history_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for i, query in enumerate(history):
            history_list.insert(tk.END, f"{i + 1}. {query}")

    def handle_query(self, event=None):
        """Handles query input"""
        query_text = self.query_entry.get()
        if not query_text:
            return

        #logging.info(f"Running query: {query_text}")

        try:
            intent, result = self.data_model.process_query(query_text)
            logging.info(f"Query: {query_text} - Intent: {intent} - Result: {result}")

            # intent, columns = self.data_model.process_query(query_text)

            # פעולות בהתאם לכוונה (intent) שזוהתה
            if intent == "plot":
                fig = show_graph(self.data_model.filtered_df, query_text,path=self.current_directory)
                # הצגת הגרף בחלון נפרד או שמירתו
                export_to_html(self.data_model.filtered_df,path=self.current_directory) # , path=fig
                messagebox.showinfo("Graph", "Graph was created and saved to plot_output.html")

            elif intent == "average":
                result = show_average(self.data_model.filtered_df, query_text)
                messagebox.showinfo("Average", result)

            elif intent == "count":
                if isinstance(result, dict):  # Check if result is conditions dict
                    count = self.data_model.count_occurrences(result)
                    messagebox.showinfo("Count", f"Number of matching rows: {count}")
                else:
                    messagebox.showerror("Error", "Invalid query for count operation.")
                # result = show_count(self.data_model.filtered_df, columns)
                # messagebox.showinfo("Count", result)

            elif intent == "when":
                result = show_dates(self.data_model.filtered_df, columns)
                messagebox.showinfo("when", result)

            else:
                messagebox.showinfo("Query", "Unknown query type. Try asking for plot, average, count, or dates.")
        except ValueError as e:
            logging.error(f"Query failed: {query_text} - Error: {str(e)}")
            messagebox.showerror("Query Error", str(e))
        except Exception as e:
            logging.exception(f"Unexpected error handling query: {query_text}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        # except Exception as e:
        #     messagebox.showerror("Query Error", str(e))

    # פונקציות ייצוא
    def export_to_csv(self):
        """Export data to CSV"""
        if self.data_model.filtered_df is None:
            messagebox.showwarning("No Data", "Please load a data file first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            export_to_csv(self.data_model.filtered_df, path=self.current_directory)
            messagebox.showinfo("Success", f"File exported successfully to {file_path}")

    def export_to_excel(self):
        """Export data to Excel"""
        if self.data_model.filtered_df is None:
            messagebox.showwarning("No Data", "Please load a data file first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            export_to_excel(self.data_model.filtered_df, path=self.current_directory)
            messagebox.showinfo("Success", f"File exported successfully to {file_path}")

    def export_to_json(self):
        """Export data to JSON"""
        if self.data_model.filtered_df is None:
            messagebox.showwarning("No Data", "Please load a data file first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            export_to_json(self.data_model.filtered_df, path=self.current_directory)
            messagebox.showinfo("Success", f"File exported successfully to {file_path}")

    def export_to_html(self):
        """Export data to HTML"""
        if self.data_model.filtered_df is None:
            messagebox.showwarning("No Data", "Please load a data file first.")
            return

        table_path, _ = export_to_html(self.data_model.filtered_df, path=self.current_directory) #, path=self.current_directory
        messagebox.showinfo("Success", f"Data exported successfully to {table_path}")


# # Main entry point
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CSVLoaderApp(root)
#     root.mainloop()