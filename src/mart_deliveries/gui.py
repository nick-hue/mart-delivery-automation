from pathlib import Path
import os 
import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from mart_deliveries.editor import make_excel
from mart_deliveries.my_utils import load_config, resource_path

class MaxGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Max Stores Excel Maker")
        self.geometry("1000x500")
        # self.iconbitmap(resource_path("assets/app.ico"))

        self.log_queue = queue.Queue()
        self.worker_thread = None

        self.cfg = load_config(resource_path("assets/config.json"))
        
        self._build_ui()
        self.after(100, self._drain_log_queue)

    def _build_ui(self):
        frame = ttk.LabelFrame(self, text="Excel", padding=10)
        frame.pack(fill="x", padx=10, pady=10)

        # self.output_dir = tk.StringVar(value=self.cfg.out_dir_path)
        
        self.output_file_path: Path | None = None

        # self._path_row(frame, "Excel Εγκρίσεων:", self.output_dir, self._pick_output_dir)

        # ---- Controls ----
        controls = ttk.Frame(self)
        controls.pack(fill="x", padx=10)
        
        run_button_style = ttk.Style()
        run_button_style.configure("Big.TButton", padding=(6, 8), font=("Segoe UI", 14, 'bold'))

        self.run_btn = ttk.Button(controls, text="Make Excel", style="Big.TButton", command=self.start)
        self.run_btn.pack(side="left", pady=(10, 20))

        # ---- Log ----
        log_frame = ttk.LabelFrame(self, text="Log", padding=6)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log = tk.Text(log_frame, height=12)
        self.log.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log.yview)
        scrollbar.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=scrollbar.set)

    def _path_row(self, parent: ttk.LabelFrame, label: str, var: tk.StringVar, cmd: callable):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=label, width=22).pack(side="left")
        ttk.Entry(row, textvariable=var).pack(side="left", fill="x", expand=True, padx=10)
        ttk.Button(row, text="Browse", command=cmd).pack(side="left")

    def _pick_customer_excel(self):
        # file = filedialog.askopenfilename(filetypes=self.cfg.supported_filetypes, initialdir=self.cfg.customer_start_dir)
        # if file:
        #     self.customer_excel_filename.set(file)
        pass
    
    def start(self):
        self.run_btn.config(state="disabled")
        self.log.delete("1.0", "end")
        
        self.worker_thread = threading.Thread(target=self._run, daemon=True)
        self.worker_thread.start()

    def _run(self):
        try:

            self._log(f"Τελικό excel : {str(self.output_dir)}")
            
            # if self.output_dir:
            #     self.after(0, self._show_success)


        except Exception as e:
            self._log(f"ERROR: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.run_btn.config(state="normal")

    def _log(self, msg):
        self.log_queue.put(msg)

    def _drain_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log.insert("end", msg + "\n")
                self.log.see("end")
        except queue.Empty:
            pass
        self.after(100, self._drain_log_queue)

def main():
    MaxGUI().mainloop()
    
def editor():
    # tmp_cfg = load_config(resource_path("assets/config.json"))
    # tmp = Path(__file__).resolve().parent
    # outfile = make_excel(customer_excel=tmp_cfg.customer_path, stock_excel=tmp_cfg.zagih_path, output_dir=tmp, config=tmp_cfg)

    pass
    # import os 
    # os.startfile(outfile)

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()


