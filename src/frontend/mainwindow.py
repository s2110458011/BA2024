import ttkbootstrap as ttk

app = ttk.Window()
app.geometry("800x600")

label = ttk.Label(app, text="Contact information")
label.pack(pady=30)
label.config(font=("Arial", 20, "bold"))

name_frame = ttk.Frame(app)
name_frame.pack(padx=10, pady=15, fill="x")
ttk.Label(name_frame, text="Name").pack(side="left", padx=5)
ttk.Entry(name_frame).pack(side="left", fill="x", expand=True, padx=5)

app.mainloop()