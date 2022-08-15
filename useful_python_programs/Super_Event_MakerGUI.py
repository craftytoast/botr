#By Wendell08, Writes super event code

import tkinter as tk
from tkinter import filedialog, Text
import shutil
import os
import re

get_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

print(get_path)

super_event_gui_effect = os.path.join(get_path, r"common\scripted_effects\TNO_super_events_scripted_effect.txt")
super_event_gui_scripted_loc = os.path.join(get_path, r"common\scripted_localisation\TNO_super_events_scripted_loc.txt")
super_event_gfx_file = os.path.join(get_path, r"interface\TNO_SG_Super_Event.gfx")
super_event_loc_file = os.path.join(get_path, r"localisation\english\TNO_Super_Events_l_english.yml")

class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.select_image_file = ""
		self.select_music_file = ""
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.run_script = tk.Button(self)
		self.run_script["text"] = "Run Program"
		self.run_script["command"] = self.run_app
		self.run_script.pack(side="top")

		self.entry1text = tk.Label(self)
		self.entry1text["text"] = "Super Event ID"
		self.entry1text["wraplength"] = 170
		self.entry1text.pack(side="top")

		self.entry1 = tk.Entry(self)
		self.entry1.insert(0, "german_civil_war")
		self.entry1.pack(side="top")

		self.select_image_button = tk.Button(self)
		self.select_image_button["text"] = "Select Super Event Image\n(.dds or .tga)"
		self.select_image_button["command"] = self.select_image_path
		self.select_image_button.pack(side="top")

		self.image_image = tk.Label(self)
		self.image_image["text"] = f"\nCurrent Image File:\n{self.select_image_file}\n"
		self.image_image["wraplength"] = 250
		self.image_image.pack(side="top")

		self.entry_music_text = tk.Label(self)
		self.entry_music_text["text"] = "Music Silence Timer(25, 30, 40, 45, 60 and 80 are the acceptable values)"
		self.entry_music_text["wraplength"] = 170
		self.entry_music_text.pack(side="top")

		self.entry_music = tk.Entry(self)
		self.entry_music.insert(0, "30")
		self.entry_music.pack(side="top")

		self.select_audio_button = tk.Button(self)
		self.select_audio_button["text"] = "Select Super Event Music(.wav)"
		self.select_audio_button["command"] = self.select_music_path
		self.select_audio_button.pack(side="top")

		self.music_label = tk.Label(self)
		self.music_label["text"] = f"\nCurrent Music File:\n{self.select_music_file}\n"
		self.music_label["wraplength"] = 250
		self.music_label.pack(side="top")

		self.entry2text = tk.Label(self)
		self.entry2text["text"] = "Super Event Quote"
		self.entry2text["wraplength"] = 170
		self.entry2text.pack(side="top")

		self.entry2 = tk.Entry(self)
		self.entry2.pack(side="top")

		self.entry3text = tk.Label(self)
		self.entry3text["text"] = "Super Event Quote Author"
		self.entry3text["wraplength"] = 170
		self.entry3text.pack(side="top")

		self.entry3 = tk.Entry(self)
		self.entry3.pack(side="top")

		self.entry4text = tk.Label(self)
		self.entry4text["text"] = "Super Event Option"
		self.entry4text["wraplength"] = 170
		self.entry4text.pack(side="top")

		self.entry4 = tk.Entry(self)
		self.entry4.pack(side="top")

	def select_image_path(self):
		self.select_image_file = filedialog.askopenfilename(initialdir=os.path.join(get_path,r"gfx\superevent_pictures"))
		self.image_image["text"] = f"\nCurrent Image File:\n{self.select_image_file}\n"

	def select_music_path(self):
		self.select_music_file = filedialog.askopenfilename(initialdir=os.path.join(get_path,r"sound\superevents"))
		self.music_label["text"] = f"\nCurrent Music File:\n{self.select_music_file}\n"

	def run_app(self):
		super_event_name = self.entry1.get()
		super_event_quote = self.entry2.get()
		super_event_author = self.entry3.get()
		super_event_option = self.entry4.get()

		music_silence = self.entry_music.get()

		_, super_event_image = os.path.split(self.select_image_file)
		_, super_event_music =  os.path.split(self.select_music_file)
		
		try:
			shutil.copy(self.select_image_file, os.path.join(get_path, r"gfx\superevent_pictures"))
		except:
			print("Image file already in Folder")
			pass
		try:
			shutil.copy(self.select_music_file, os.path.join(get_path, r"sound\superevents"))
		except:
			print("Music file already in Folder")
			pass


		#--------------------

	
		with open(super_event_gui_effect, "r") as inpt:
			event_id = re.compile(r"limit = { check_variable = { TNO_temp_super_event = ([0-9]+) } }")
			lines = inpt.read()
			super_event_ids = event_id.findall(lines)
			old_id = super_event_ids[-1]
		with open(super_event_gui_effect, "r") as inp:
			bracket = 0
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				bracket += line_item.count("{")
				bracket -= line_item.count("{")
				if f"check_variable = {{ TNO_temp_super_event = {old_id} }}" in line_item:
					print(line_item)
					super_event_id = int(old_id)+1
					line_list[i+3] += f'''			else_if = {{
				limit = {{ check_variable = {{ TNO_temp_super_event = {super_event_id} }} }}
				scoped_sound_effect = "{super_event_music[:-4]}"
				if = {{ limit = {{ has_global_flag = silence_on_SE }} scoped_play_song = "silence_{music_silence}" }}
			}}
'''
			with open(super_event_gui_effect, "w") as out:
				for line_to_write in line_list:
					out.write(line_to_write)

		#--------------------

		with open(super_event_gui_scripted_loc, "r") as inp:
			line_list = inp.readlines()
			scripted_loc = 0
			for i, line_item in enumerate(line_list):
				if f"check_variable = {{ TNO_super_event = {old_id} }}" in line_item:
					scripted_loc += 1
					print(scripted_loc, line_item)
					if scripted_loc == 1:
						write_line = f"\"GFX_superevent_{super_event_name}\""
					elif scripted_loc == 2:
						write_line = f"SE_{super_event_name.upper()}_T"
					elif scripted_loc == 3:
						write_line = f"SE_{super_event_name.upper()}_A"
					elif scripted_loc == 4:
						write_line = f"SE_{super_event_name.upper()}_D"
					line_list[i+2] += f'''	text = {{
		trigger = {{ check_variable = {{ TNO_super_event = {super_event_id} }} }}
		localization_key = {write_line}
	}}
'''
			with open(super_event_gui_scripted_loc, "w") as out:
				for line_to_write in line_list:
					out.write(line_to_write)

		#--------------------

		with open(super_event_gfx_file) as inp:
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				if "SUPER_EVENT_MAKER_GUI" in line_item:
					line_list[i] = f'''	spriteType = {{
		name = "GFX_superevent_{super_event_name}"
		textureFile = "gfx/superevent_pictures/{super_event_image}"
	}}
	##USE SUPER_EVENT_MAKER_GUI IN USEFUL PYTHON PROGRAMS TO MAKE NEW SUPER EVENTS##
'''
			with open(super_event_gfx_file, "w") as out:
				for line_to_write in line_list:
					out.write(line_to_write)

		#--------------------

		with open(super_event_loc_file, "a+") as out:
			out.write(f'''
SE_{super_event_name.upper()}_T: "{super_event_name.upper().replace("_", " ")}"
SE_{super_event_name.upper()}_D: "{super_event_quote}\\n- {super_event_author}"
SE_{super_event_name.upper()}_A: "{super_event_option}"
''')

		#--------------------

		with open(os.path.join(get_path, r"sound\tno_sound.asset"), "r") as inp:
			music_file_found = False
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				if super_event_music in line_item:
					print("Music file already defined in tno_sound.asset")
					music_file_found = True
					break
				if "SUPER_EVENT_MAKER_GUI" in line_item:
					line_list[i] = f'''sound = {{
	name = "{super_event_music[:-4]}"
	file = "superevents/{super_event_music}"
	always_load = no
}}

##USE SUPER_EVENT_MAKER_GUI IN USEFUL PYTHON PROGRAMS TO MAKE NEW SUPER EVENTS##'''
			if music_file_found == False:
				with open(os.path.join(get_path, r"sound\tno_sound.asset"), "w") as out:
					for line_to_write in line_list:
						out.write(line_to_write)

		#--------------------

		with open(os.path.join(get_path, r"sound\gui\tno_gui_sound_effects.asset"), "r") as inp:
			music_file_found = False
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				if super_event_music in line_item:
					print("Music file already defined in gui/tno_gui_sound_effects.asset")
					music_file_found = True
					break
				if "SUPER_EVENT_MAKER_GUI" in line_item:
					line_list[i] = f'''soundeffect = {{
	name = "{super_event_music[:-4]}"
	sounds = {{
		sound = {super_event_music[:-4]}
	}}
	volume = 0.75
}}

##USE SUPER_EVENT_MAKER_GUI IN USEFUL PYTHON PROGRAMS TO MAKE NEW SUPER EVENTS##'''
			if music_file_found == False:
				with open(os.path.join(get_path, r"sound\gui\tno_gui_sound_effects.asset"), "w") as out:
					for line_to_write in line_list:
						out.write(line_to_write)

		#--------------------

		with open(os.path.join(get_path, r"sound\tno.asset"), "r") as inp:
			music_file_found = False
			line_list = inp.readlines()
			for i, line_item in enumerate(line_list):
				if super_event_music in line_item:
					print("Music file already defined in tno.asset")
					music_file_found = True
					break
				if "SUPER_EVENT_MAKER_GUI" in line_item:
					line_list[i] = f"\t\t{super_event_music[:-4]}\n\t\t##USE SUPER_EVENT_MAKER_GUI IN USEFUL PYTHON PROGRAMS TO MAKE NEW SUPER EVENTS##\n"
			if music_file_found == False:
				with open(os.path.join(get_path, r"sound\tno.asset"), "w") as out:
					for line_to_write in line_list:
						out.write(line_to_write)

		print("Finished superevent script execution")

root = tk.Tk()
root.geometry("260x540")
root.title("Super Event Maker")
app = App(master=root)
app.mainloop()
