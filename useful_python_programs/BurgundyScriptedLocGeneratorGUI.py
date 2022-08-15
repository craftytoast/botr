import os
import tkinter as tk
from tkinter import filedialog, Text
#by uncountably and Wendell
this_path = os.path.realpath(__file__)
focus_list = []

class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.file_path = ""
		self.loc_file_name = ""
		self.scripted_loc_file_name = ""
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.run_script = tk.Button(self)
		self.run_script["text"] = "Run Program"
		self.run_script["command"] = self.run_app
		self.run_script.pack(side = "top")

		self.output_label = tk.Label(self)
		self.output_label["text"] = f"Current Focus Path:{self.file_path}"
		self.output_label["wraplength"] = 550
		self.output_label.pack(side = "top")
		
		self.file_select_focus = tk.Button(self)
		self.file_select_focus["text"] = "Select a focus path"
		self.file_select_focus["command"] = self.select_file_path
		self.file_select_focus.pack(side = "top")

		self.output_label_loc = tk.Label(self)
		self.output_label_loc["text"] = f"Current Loc File:{self.loc_file_name}"
		self.output_label_loc["wraplength"] = 550
		self.output_label_loc.pack(side = "top")
		
		self.file_select_loc = tk.Button(self)
		self.file_select_loc["text"] = "Select a loc file"
		self.file_select_loc["command"] = self.select_file_path_loc
		self.file_select_loc.pack(side = "top")

		self.output_label_scripted_loc = tk.Label(self)
		self.output_label_scripted_loc["text"] = f"Current Scripted Loc File:{self.scripted_loc_file_name}"
		self.output_label_scripted_loc["wraplength"] = 550
		self.output_label_scripted_loc.pack(side = "top")
		
		self.file_select_scripted_loc = tk.Button(self)
		self.file_select_scripted_loc["text"] = "Select a scripted loc file"
		self.file_select_scripted_loc["command"] = self.select_file_path_scripted_loc
		self.file_select_scripted_loc.pack(side = "top")
		
		self.instructions = tk.Label(self)
		self.instructions["text"] = "Select a folder containing one or more focus files using the first button, and select an output file for loc and scripted loc with the second and third. Click the \"Run Program\" button afterwards and then copy the output into the correct files."
		self.instructions["wraplength"] = 550
		self.instructions.pack(side = "top")

	def select_file_path(self):		
		self.file_path = filedialog.askdirectory(initialdir=this_path, title="Select Focus Path")
		self.output_label["text"] = f"Current Focus Path:{self.file_path}"

	def select_file_path_loc(self):		
		self.loc_file_name = filedialog.askopenfilename(initialdir=this_path, title="Select Loc File", filetypes=[("loc files", "*.yml")])
		self.output_label_loc["text"] = f"Current Loc File:{self.loc_file_name}"

	def select_file_path_scripted_loc(self):		
		self.scripted_loc_file_name = filedialog.askopenfilename(initialdir=this_path, title="Select Scripted Loc File", filetypes=[("scripted loc files", "*localisation.txt")])
		self.output_label_scripted_loc["text"] = f"Current Scripted Loc File:{self.scripted_loc_file_name}"

	def run_app(self):
		for file in os.listdir(self.file_path):
			if "_shared.txt" in file:
				process_one_file(self.file_path, file)
	
def process_one_file(filepath, filename):
	focus_list = []
	fullpath = os.path.join(filepath, filename)
	for line in open(fullpath, "r").readlines():
		if "	id = " in line and not "		" in line:
			focus_list.append(line[6:-1])
	
	with open(app.scripted_loc_file_name, "a+") as scripted_loc:	
		scripted_loc.write(f"\n\n\n\n{filename}\n\n")
		for focus in focus_list:
			print(focus)
			if "blankfocus" not in focus:
				print(focus)
				focus2 = focus[4:].title()
				scripted_loc.write("\ndefined_text = {")
				scripted_loc.write("\n	name = GetBRGFocus"+focus2)
				scripted_loc.write("\n	text = {")
				scripted_loc.write("\n		trigger = {")
				scripted_loc.write("\n			BRG = {")
				scripted_loc.write("\n				is_ai = no")
				scripted_loc.write("\n			}")
				scripted_loc.write("\n		}")
				scripted_loc.write("\n		localization_key = "+focus+"_text")
				scripted_loc.write("\n	}")
				scripted_loc.write("\n	text = {")
				scripted_loc.write("\n		trigger = {")
				scripted_loc.write("\n			BRG = {")
				scripted_loc.write("\n				is_ai = yes")
				scripted_loc.write("\n			}")
				scripted_loc.write("\n		}")
				scripted_loc.write("\n		localization_key = BRG_redacted")
				scripted_loc.write("\n	}")
				scripted_loc.write("\n}\n")	
				
	
	with open(app.loc_file_name, "a+") as loc:
		loc.write(f"\n\n\n\n{filename}\n\n")
		for focus in focus_list:
			focus2 = focus[4:].title()
			loc.write(f"\n{focus}: \"[Root.GetBRGFocus{focus2}]\"")
		loc.write("\n")
		for focus in focus_list:
			focus_name = focus.replace("_", " ")[4:].title()
			loc.write(f"\n{focus}_text: \"{focus_name}\"")
		loc.write("\n")
		for focus in focus_list:
			loc.write(f"\n{focus}_desc: \"\"")	
		loc.write("\n")




root = tk.Tk()
root.geometry("600x300")
root.title("Burgundy Scripted Loc Generator")
app = App(master=root)
app.mainloop()
