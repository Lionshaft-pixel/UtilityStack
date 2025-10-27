import fitz
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class PDFMarginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Margin Tool")
        self.root.geometry("650x750")
        
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.mode = tk.StringVar(value="all")
        
        self.setup_gui()
    
    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(main_frame, text="PDF Margin Adjuster", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        self.create_file_section(main_frame)
        self.create_mode_selector(main_frame)
        self.create_margin_frames(main_frame)
        self.create_action_buttons(main_frame)
    
    def create_file_section(self, parent):
        file_frame = ttk.LabelFrame(parent, text="PDF Files")
        file_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(file_frame, text="Input PDF:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(file_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="Output PDF:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(file_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)
    
    def create_mode_selector(self, parent):
        mode_frame = ttk.LabelFrame(parent, text="Adjustment Mode")
        mode_frame.pack(fill=tk.X, pady=10)
        
        modes = [
            ("All Pages", "all"),
            ("Odd/Even Pages", "oddeven"),
            ("Selected Pages", "selected"),
            ("Page Groups", "groups")
        ]
        
        for i, (text, value) in enumerate(modes):
            ttk.Radiobutton(mode_frame, text=text, variable=self.mode, 
                           value=value, command=self.on_mode_change).grid(row=0, column=i, padx=10, pady=10)
    
    def create_margin_frames(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.all_frame = self.create_margin_tab("All Pages")
        self.oddeven_frame = self.create_oddeven_tab()
        self.selected_frame = self.create_selected_tab()
        self.groups_frame = self.create_groups_tab()
        
        self.notebook.add(self.all_frame, text="All Pages")
        self.notebook.add(self.oddeven_frame, text="Odd/Even")
        self.notebook.add(self.selected_frame, text="Selected")
        self.notebook.add(self.groups_frame, text="Groups")
    
    def create_margin_tab(self, title):
        frame = ttk.Frame(self.notebook)
        
        ttk.Label(frame, text=f"Margins for {title}").pack(pady=10)
        
        margin_frame = ttk.Frame(frame)
        margin_frame.pack(pady=10)
        
        margins = [
            ("Left:", "left_all"),
            ("Top:", "top_all"), 
            ("Right:", "right_all"),
            ("Bottom:", "bottom_all")
        ]
        
        for i, (label, var_name) in enumerate(margins):
            setattr(self, var_name, tk.StringVar(value="20"))
            ttk.Label(margin_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            ttk.Entry(margin_frame, textvariable=getattr(self, var_name), width=10).grid(row=i, column=1, padx=5, pady=5)
        
        return frame
    
    def create_oddeven_tab(self):
        frame = ttk.Frame(self.notebook)
        
        odd_frame = ttk.LabelFrame(frame, text="Odd Pages")
        odd_frame.pack(fill=tk.X, pady=5)
        
        even_frame = ttk.LabelFrame(frame, text="Even Pages")
        even_frame.pack(fill=tk.X, pady=5)
        
        odd_margins = [
            ("Left:", "left_odd"),
            ("Top:", "top_odd"),
            ("Right:", "right_odd"),
            ("Bottom:", "bottom_odd")
        ]
        
        even_margins = [
            ("Left:", "left_even"),
            ("Top:", "top_even"),
            ("Right:", "right_even"),
            ("Bottom:", "bottom_even")
        ]
        
        for i, (label, var_name) in enumerate(odd_margins):
            setattr(self, var_name, tk.StringVar(value="30"))
            ttk.Label(odd_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(odd_frame, textvariable=getattr(self, var_name), width=10).grid(row=i, column=1, padx=5, pady=2)
        
        for i, (label, var_name) in enumerate(even_margins):
            setattr(self, var_name, tk.StringVar(value="15"))
            ttk.Label(even_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(even_frame, textvariable=getattr(self, var_name), width=10).grid(row=i, column=1, padx=5, pady=2)
        
        return frame
    
    def create_selected_tab(self):
        frame = ttk.Frame(self.notebook)
        
        ttk.Label(frame, text="Page Numbers (e.g., 1,3,5-8,12)").pack(pady=5)
        self.selected_pages_var = tk.StringVar(value="1,3,5-8")
        ttk.Entry(frame, textvariable=self.selected_pages_var, width=40).pack(pady=5)
        
        margin_frame = ttk.Frame(frame)
        margin_frame.pack(pady=10)
        
        margins = [
            ("Left:", "left_sel"),
            ("Top:", "top_sel"),
            ("Right:", "right_sel"),
            ("Bottom:", "bottom_sel")
        ]
        
        for i, (label, var_name) in enumerate(margins):
            setattr(self, var_name, tk.StringVar(value="25"))
            ttk.Label(margin_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Entry(margin_frame, textvariable=getattr(self, var_name), width=10).grid(row=i, column=1, padx=5, pady=2)
        
        return frame
    
    def create_groups_tab(self):
        frame = ttk.Frame(self.notebook)
        
        ttk.Label(frame, text="Page Groups - Format: start-end margins").pack(pady=5)
        
        self.groups_text = tk.Text(frame, height=8, width=50)
        self.groups_text.pack(pady=5, fill=tk.BOTH, expand=True)
        self.groups_text.insert(tk.END, "1-10 20 20 20 20\n11-20 10 10 10 10\n21-30 15 15 15 15")
        
        ttk.Label(frame, text="Example: '1-5 10 15 10 15' means pages 1-5 with margins left=10, top=15, right=10, bottom=15").pack(pady=5)
        
        return frame
    
    def create_action_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Apply Margins", command=self.apply_margins).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=10)
    
    def browse_input(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.input_path.set(filename)
            if not self.output_path.get():
                base, ext = os.path.splitext(filename)
                self.output_path.set(f"{base}_margins{ext}")
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.output_path.set(filename)
    
    def on_mode_change(self):
        mode_index = {"all": 0, "oddeven": 1, "selected": 2, "groups": 3}
        self.notebook.select(mode_index[self.mode.get()])
    
    def clear_all(self):
        self.input_path.set("")
        self.output_path.set("")
        for var in [self.left_all, self.top_all, self.right_all, self.bottom_all]:
            var.set("20")
    
    def parse_page_range(self, page_input):
        selected_pages = set()
        for part in page_input.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                selected_pages.update(range(start, end + 1))
            else:
                selected_pages.add(int(part))
        return selected_pages
    
    def parse_groups(self, groups_text):
        group_margins = {}
        for line in groups_text.strip().split('\n'):
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) >= 5:
                page_range = parts[0]
                margins = tuple(map(int, parts[1:5]))
                if '-' in page_range:
                    start, end = map(int, page_range.split('-'))
                    group_margins[(start, end)] = margins
        return group_margins
    
    def set_page_margins(self, page, margins):
        rect = page.rect
        new_rect = fitz.Rect(
            rect.x0 + margins[0],
            rect.y0 + margins[1],
            rect.x1 - margins[2],
            rect.y1 - margins[3]
        )
        page.set_mediabox(new_rect)
    
    def apply_margins(self):
        if not self.input_path.get() or not self.output_path.get():
            messagebox.showerror("Error", "Please select input and output PDF files")
            return
        
        try:
            doc = fitz.open(self.input_path.get())
            mode = self.mode.get()
            
            if mode == "all":
                margins = (int(self.left_all.get()), int(self.top_all.get()), 
                          int(self.right_all.get()), int(self.bottom_all.get()))
                for page in doc:
                    self.set_page_margins(page, margins)
            
            elif mode == "oddeven":
                margins_odd = (int(self.left_odd.get()), int(self.top_odd.get()),
                              int(self.right_odd.get()), int(self.bottom_odd.get()))
                margins_even = (int(self.left_even.get()), int(self.top_even.get()),
                               int(self.right_even.get()), int(self.bottom_even.get()))
                for i, page in enumerate(doc):
                    if (i + 1) % 2 == 1:
                        self.set_page_margins(page, margins_odd)
                    else:
                        self.set_page_margins(page, margins_even)
            
            elif mode == "selected":
                selected_pages = self.parse_page_range(self.selected_pages_var.get())
                margins = (int(self.left_sel.get()), int(self.top_sel.get()),
                          int(self.right_sel.get()), int(self.bottom_sel.get()))
                for i, page in enumerate(doc):
                    if (i + 1) in selected_pages:
                        self.set_page_margins(page, margins)
            
            elif mode == "groups":
                group_margins = self.parse_groups(self.groups_text.get("1.0", tk.END))
                for i, page in enumerate(doc):
                    page_num = i + 1
                    for (start, end), margins in group_margins.items():
                        if start <= page_num <= end:
                            self.set_page_margins(page, margins)
            
            doc.save(self.output_path.get())
            doc.close()
            messagebox.showinfo("Success", f"PDF saved successfully!\n{self.output_path.get()}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process PDF:\n{str(e)}")

def main():
    root = tk.Tk()
    app = PDFMarginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()