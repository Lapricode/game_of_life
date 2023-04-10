import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as sd
import turtle as t
import random as r
import os

class game_of_life():
    def __init__(self, root):
        self.root = root
        self.root.title("Game of Life")
        self.root.geometry("+0+0")
        self.root.resizable(True, True)
        self.grid_height = self.root.winfo_screenheight()
        self.grid_width = 1536 / 864 * self.grid_height
        self.colors_list_1 = ['#ffff00', '#efff00', '#dfff00', '#cfff00', '#bfff00', '#afff00', '#9fff00', '#8fff00', '#7fff00',
                            '#6fff00', '#5fff00', '#4fef00', '#3fdf00', '#2fcf00', '#1fbf00', '#1faf00', '#1f9f00', '#1f8f00',
                            '#1f7f00', '#1f6f00', '#1f5f00', '#006fff']
        self.colors_list_2 = ['#ffffff', '#efefff', '#dfdfff', '#cfcfff', '#bfbfff', '#afafff', '#9f9fff', '#8f8fff', '#7f7fff',
                            '#6f6fff', '#5f5fff', '#4f4fff', '#3f3fff', '#2f2fff', '#1f1fef', '#1f1fdf', '#1f1fcf', '#1f1fbf',
                            '#1f1faf', '#1f1f9f', '#1f1f8f', '#000000']
        self.colors_list = self.colors_list_1
        self.canvas_offset = 3
        self.simulation_state = 'stop_simulation'
        self.recording_state = 'stop_recording'
        self.recording_play_stop_state = 'stop'
        self.set_chosen_position = 'off'
        self.go_to_gen_mode = 'off'
        self.control_grid_limits_string = 'inside'
        self.recording_pointer = 0
        self.reminder_pointer = self.recording_pointer
        self.reminder_direction = 'forward'
        self.rows = 100
        self.columns = 100
        self.speed = 5000
        self.born_rules = [3]
        self.survive_rules = [2, 3]
        self.initial_gen_simulation_graf = 0
        self.final_gen_simulation_graf = 0
        self.start_interface()
    def start_interface(self):
        #------------Δημιουργία πλέγματος προσομοίωσης.-------------#
        self.grid_size = 0.75 * self.grid_height
        self.grid_labels_background = tk.Frame(self.root, bd = 5, relief = "raised")
        self.grid_labels_background.grid(row = 0, column = 0, rowspan = 4)
        self.grid_background = tk.Canvas(self.grid_labels_background, width = int(self.grid_size) + self.canvas_offset, height = int(self.grid_size) + self.canvas_offset, bg = "brown", bd = 0, relief = "solid")
        self.grid_background.grid(row = 0, column = 0, columnspan = 4, sticky = tk.NSEW)
        self.grid_cells = []
        self.appeared_rows = 30
        self.appeared_columns = 30
        self.left_column = int((self.columns - self.appeared_columns) / 2)
        self.right_column = int((self.columns + self.appeared_columns) / 2 - 1)
        self.up_row = int((self.rows - self.appeared_rows) / 2)
        self.down_row = int((self.rows + self.appeared_rows) / 2 - 1)
        self.button_size = self.grid_size / (self.down_row - self.up_row + 1)
        self.grid_information_string = tk.StringVar()
        self.grid_information = tk.Label(self.grid_labels_background, textvariable = self.grid_information_string, font = 'Arial 10 bold', bd = 2, relief = 'solid', width = 50)
        self.grid_information.grid(row = 1, column = 0, sticky = tk.NSEW)
        self.grid_colors_label = tk.Label(self.grid_labels_background, text = 'Colors:', font = 'Arial 15 bold', bg = 'grey', fg = 'black')
        self.grid_colors_label.grid(row = 1, column = 1, sticky = tk.NSEW)
        self.grid_colors_button = tk.Button(self.grid_labels_background, text = '◼', font = 'Arial 16 bold', bg = self.colors_list[-1], fg = self.colors_list[0], command = self.change_grid_colors)
        self.grid_colors_button.grid(row = 1, column = 2, sticky = tk.NSEW)
        self.cells_gap_label = tk.Label(self.grid_labels_background, text = 'Cells gap:', font = 'Arial 15 bold', bg = 'grey', fg = 'black')
        self.cells_gap_label.grid(row = 2, column = 1, sticky = tk.NSEW)
        self.cells_gap_scaler = tk.Scale(self.grid_labels_background, bg = "silver", from_ = 0, to = 10, resolution = 1, orient = "horizontal")
        self.cells_gap_scaler.grid(row = 2, column = 2, sticky = tk.NSEW)
        self.cells_gap_scaler.bind("<ButtonRelease-1>", self.adjust_pieces_gap)
        self.control_grid_limits_button = tk.Button(self.grid_labels_background, text = 'Control grid\nborders (disabled)', font = 'Arial 10 bold', bd = 2, bg = 'red', activeforeground = 'white', activebackground = 'black', relief = 'raised', command = self.turn_on_off_limits)
        self.control_grid_limits_button.grid(row = 2, column = 0, sticky = tk.NSEW)
        for i in range(self.rows):
            self.grid_cells_row = []
            for j in range(self.columns):
                self.grid_cells_row.append(button(self.grid_background, self.button_size, i * self.columns, i, j))
            self.grid_cells.append(self.grid_cells_row)
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid_cells[i][j].set_button_on_grid(i, j)
        self.grid_background.delete("all")
        for i in range(self.up_row, self.down_row + 1):
            for j in range(self.left_column, self.right_column + 1):
                self.grid_cells[i][j].set_button_on_grid(i - self.up_row, j - self.left_column)        
        self.graf_history = []
        
        #------------Δημιουργία μενού επιλογών παιχνιδιού.-------------#
        self.options_background = tk.Frame(self.root, bd = 2, relief = 'solid')
        self.options_background.grid(row = 2, column = 1, rowspan = 2)
            
            #------------Δημιουργία μενού επιλογών για την κίνηση του πλέγματος.-------------#
        self.grid_options_background = tk.Frame(self.options_background, bd = 5, relief = 'solid', bg = 'green')
        self.grid_options_background.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.move_grid_label = tk.Label(self.grid_options_background, text = 'Grid moves', font = 'Arial 20 italic', fg = 'white', bg = 'green')
        self.move_grid_label.grid(row = 0, column = 0, columnspan = 4, sticky = tk.NSEW)
        self.control_move_label = tk.Button(self.grid_options_background, text = 'Stable grid\nMoving observator', font = 'Arial 12 bold', fg = 'white', bg = 'green')
        self.control_move_label.grid(row = 1, column = 0, columnspan = 4, sticky = tk.NSEW)
        self.move_grid_up_button = tk.Button(self.grid_options_background, text = '⯅', font = 'Arial 13 bold', fg = 'black', bg = 'red', activeforeground = 'yellow', activebackground = 'red', command = self.grid_up)
        self.move_grid_up_button.grid(row = 2, column = 0, sticky = tk.NSEW)
        self.move_grid_down_button = tk.Button(self.grid_options_background, text = '⯆', font = 'Arial 13 bold', fg = 'black', bg = 'red', activeforeground = 'yellow', activebackground = 'red', command = self.grid_down)
        self.move_grid_down_button.grid(row = 3, column = 0, sticky = tk.NSEW)
        self.move_grid_left_button = tk.Button(self.grid_options_background, text = '⯇', font = 'Arial 13 bold', fg = 'black', bg = 'red', activeforeground = 'yellow', activebackground = 'red', command = self.grid_left)
        self.move_grid_left_button.grid(row = 2, column = 1, sticky = tk.NSEW)
        self.move_grid_right_button = tk.Button(self.grid_options_background, text = '⯈', font = 'Arial 13 bold', fg = 'black', bg = 'red', activeforeground = 'yellow', activebackground = 'red', command = self.grid_right)
        self.move_grid_right_button.grid(row = 3, column = 1, sticky = tk.NSEW)
        self.left_rotate_grid_button = tk.Button(self.grid_options_background, text = '⭯', font = 'Arial 14 bold', fg = 'black', bg = 'red', activeforeground = 'yellow', activebackground = 'red', command = lambda: self.grid_rotate('left'))
        self.left_rotate_grid_button.grid(row = 2, column = 2, sticky = tk.NSEW)
        self.right_rotate_grid_button = tk.Button(self.grid_options_background, text = '⭮', font = 'Arial 14 bold', fg = 'black', bg = 'red', activeforeground = 'yellow', activebackground = 'red', command = lambda: self.grid_rotate('right'))
        self.right_rotate_grid_button.grid(row = 3, column = 2, sticky = tk.NSEW)
        self.zoomin_grid_button = tk.Button(self.grid_options_background, text = 'zoom in', font = 'Arial 10 bold', fg = 'black', bg = 'lightblue', activeforeground = 'red', activebackground = 'lightblue', width = 15, command = self.grid_zoom_in)
        self.zoomin_grid_button.grid(row = 2, column = 3, sticky = tk.NSEW)
        self.zoomout_grid_button = tk.Button(self.grid_options_background, text = 'zoom out', font = 'Arial 10 bold', fg = 'black', bg = 'lightblue', activeforeground = 'red', activebackground = 'lightblue', width = 15, command = self.grid_zoom_out)
        self.zoomout_grid_button.grid(row = 3, column = 3, sticky = tk.NSEW)
            
            #------------Δημιουργία μενού επιλογών για τη λειτουργία της προσομοίωσης.-------------#
        self.simulation_options_background = tk.Frame(self.options_background, bd = 2, relief = 'solid', bg = 'lightblue')
        self.simulation_options_background.grid(row = 1, column = 0, sticky = tk.NSEW)
        self.simulation_options_label = tk.Label(self.simulation_options_background, text = 'Simulation', font = 'Arial 20 italic', fg = 'black', bg = 'lightblue')
        self.simulation_options_label.grid(row = 0, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.clear_button = tk.Button(self.simulation_options_background, text = 'Clear', font = 'Arial 15', fg = 'white', bg = 'brown', activeforeground = 'white', activebackground = 'black', command = self.clear_grid)
        self.clear_button.grid(row = 1, column = 0, sticky = tk.W)
        self.go_to_label = tk.Label(self.simulation_options_background, text = 'Go to\ngen:', width = 5, font = 'Arial 12 bold', fg = 'yellow', bg ='blue')
        self.go_to_label.grid(row = 1, column = 0, sticky = tk.E)
        self.go_to_gen_string = tk.Entry(self.simulation_options_background, width = 5, font = 'Arial 18 bold')
        self.go_to_gen_string.grid(row = 1, column = 1, sticky = tk.W)
        self.go_to_gen_string.bind("<Return>", self.go_to_gen)
        self.step_run_button = tk.Button(self.simulation_options_background, text = '>>', font = 'Arial 16 bold', fg = 'black', bg = 'green', activeforeground = 'white', activebackground = 'green', command = self.step_run)
        self.step_run_button.grid(row = 1, column = 1, sticky = tk.E)
        self.run_simulation_button = tk.Button(self.simulation_options_background, width = 6, text = 'Run', font = 'Arial 20 bold', fg = 'red', bg ='lightblue', activeforeground = 'red', activebackground = 'blue', command = self.run)
        self.run_simulation_button.grid(row = 2, column = 0, sticky = tk.NSEW)
        self.stop_simulation_button = tk.Button(self.simulation_options_background, width = 6, text = 'Stop', font = 'Arial 20 bold', fg = 'yellow', bg ='lightblue', activeforeground = 'yellow', activebackground = 'red', command = self.stop)
        self.stop_simulation_button.grid(row = 2, column = 1, sticky = tk.NSEW)
        self.speed_control_button_label = tk.Label(self.simulation_options_background, text = '  Speed:  ', font = 'Arial 20', fg = 'orange', bg = 'green', bd = 1, relief = 'solid')
        self.speed_control_button_label.grid(row = 3, column = 0, sticky = tk.NSEW)
        self.speed_control_button = tk.Scale(self.simulation_options_background, from_ = 1, to = 500, resolution = 1, orient = 'horizontal')
        self.speed_control_button.grid(row = 3, column = 1, sticky = tk.N)
        self.start_recording_button = tk.Button(self.simulation_options_background, text = 'Start\nrecording', font = 'Arial 12 bold', fg = 'navy', bg = 'turquoise', activeforeground = 'navy', activebackground = 'lime', command = self.start_recording)
        self.start_recording_button.grid(row = 4, column = 0, sticky = tk.NSEW)
        self.stop_recording_button = tk.Button(self.simulation_options_background, text = 'Stop\nrecording', font = 'Arial 12 bold', fg = 'deeppink', bg = 'turquoise', activeforeground = 'deeppink', activebackground = 'lime', command = self.stop_recording)
        self.stop_recording_button.grid(row = 4, column = 1, sticky = tk.NSEW)
        self.play_stop_button = tk.Button(self.simulation_options_background, text = '⯈', font = 'Arial 15 bold', fg = 'navy', bg = 'khaki', activeforeground = 'navy', activebackground = 'lime', command = self.play_stop_recording)
        self.play_stop_button.grid(row = 5, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.play_forward_button = tk.Button(self.simulation_options_background, text = '▶▶', font = 'Arial 15 bold', fg = 'black', bg = 'khaki', activeforeground = 'crimson', activebackground = 'lime', command = self.play_forward_recording)
        self.play_forward_button.grid(row = 5, column = 1, sticky = tk.NE)
        self.play_reverse_button = tk.Button(self.simulation_options_background, text = '◀◀', font = 'Arial 15 bold', fg = 'black', bg = 'khaki', activeforeground = 'crimson', activebackground = 'lime', command = self.play_reverse_recording)
        self.play_reverse_button.grid(row = 5, column = 0, sticky = tk.NW)
        self.save_recording_button = tk.Button(self.simulation_options_background, text = 'Save recording', font = 'Arial 12 bold', fg = 'purple', bg = 'khaki', activeforeground = 'purple', activebackground = 'springgreen', command = self.save_recording)
        self.save_recording_button.grid(row = 6, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.play_forward_recording()
            
            #------------Δημιουργία μενού πληροφοριών προσομοίωσης.-------------#
        self.grid_information_background = tk.Frame(self.options_background, bd = 2, relief = 'solid', bg = 'goldenrod')
        self.grid_information_background.grid(row = 2, column = 0, sticky = tk.NSEW)
        self.grid_information_label = tk.Label(self.grid_information_background, text = 'Information', font = 'Arial 20 italic', fg = 'black', bg = 'goldenrod')
        self.grid_information_label.grid(row = 0, column = 0, columnspan = 2, sticky = tk.NSEW)
        self.generations_label = tk.Label(self.grid_information_background, text = '     Gen:', font = 'Arial 15 bold', fg = 'darkgreen', bg = 'goldenrod')
        self.generations_label.grid(row = 1, column = 0, sticky = tk.NSEW)
        self.generations_string = tk.StringVar()
        self.generations = tk.Label(self.grid_information_background, width = 10, textvariable = self.generations_string, font = 'Arial 15 bold', fg = 'midnightblue', bg = 'goldenrod')
        self.generations.grid(row = 1, column = 1, sticky = tk.NSEW)
        self.first_cells_label = tk.Label(self.grid_information_background, text = '     Initially:', font = 'Arial 15 bold', fg = 'darkgreen', bg = 'goldenrod')
        self.first_cells_label.grid(row = 2, column = 0, sticky = tk.NSEW)
        self.first_cells_string = tk.StringVar()
        self.first_cells = tk.Label(self.grid_information_background, width = 10, textvariable = self.first_cells_string, font = 'Arial 15 bold', fg = 'midnightblue', bg = 'goldenrod')
        self.first_cells.grid(row = 2, column = 1, sticky = tk.NSEW)
        self.births_cells_label = tk.Label(self.grid_information_background, text = '     Births:', font = 'Arial 15 bold', fg = 'darkgreen', bg = 'goldenrod')
        self.births_cells_label.grid(row = 3, column = 0, sticky = tk.NSEW)
        self.birth_cells_string = tk.StringVar()
        self.birth_cells = tk.Label(self.grid_information_background, width = 10, textvariable = self.birth_cells_string, font = 'Arial 15 bold', fg = 'midnightblue', bg = 'goldenrod')
        self.birth_cells.grid(row = 3, column = 1, sticky = tk.NSEW)
        self.death_cells_label = tk.Label(self.grid_information_background, text = '     Deaths:', font = 'Arial 15 bold', fg = 'darkgreen', bg = 'goldenrod')
        self.death_cells_label.grid(row = 4, column = 0, sticky = tk.NSEW)
        self.death_cells_string = tk.StringVar()
        self.death_cells = tk.Label(self.grid_information_background, width = 10, textvariable = self.death_cells_string, font = 'Arial 15 bold', fg = 'midnightblue', bg = 'goldenrod')
        self.death_cells.grid(row = 4, column = 1, sticky = tk.NSEW)
        self.finally_cells_label = tk.Label(self.grid_information_background, text = '     Finally:', font = 'Arial 15 bold', fg = 'darkgreen', bg = 'goldenrod')
        self.finally_cells_label.grid(row = 5, column = 0, sticky = tk.NSEW)
        self.finally_cells_string = tk.StringVar()
        self.finally_cells = tk.Label(self.grid_information_background, width = 10, textvariable = self.finally_cells_string, font = 'Arial 15 bold', fg = 'midnightblue', bg = 'goldenrod')
        self.finally_cells.grid(row = 5, column = 1, sticky = tk.NSEW)
        self.reset_simulation_information_button = tk.Button(self.grid_information_background, text = 'Reset', font = 'Arial 12 bold', fg = 'red', bg = 'wheat', activeforeground = 'red', activebackground = 'orange', command = self.reset_cells_information)
        self.reset_simulation_information_button.grid(row = 6, column = 0, columnspan = 2, sticky = tk.NSEW)
            
        #------------Δημιουργία παραπάνω δυνατοτήτων.-------------#
        self.rules_set = ['B3/S23 Conway\'s Life (chaotic)', 'B36/S125 2x2 (chaotic)', 'B357/S1358 Amoeba (chaotic)', 'B35678/S5678 Diamobea (chaotic)',
                        'B36/S23 HighLife (chaotic)', 'B0123478/S34678 InverseLife (chaotic)', 'B357/S238 Pseudo life (chaotic)', 'B34/S34 34 Life (exploding)',
                        'B378/S235678 Coagulations (exploding)', 'B3/S45678 Coral (exploding)', 'B1/S1 Gnarl (exploding)', 'B3/S12345 Maze (exploding)',
                        'B3/S1234 Mazectric (exploding)', 'B1357/S1357 Replicator (exploding)', 'B2/S Seeds (exploding)', 'B234/S Serviettes (exploding)',
                        'B3/S012345678 Flakes (expanding)', 'B345/S4567 Assimilation (stable)', 'B3678/S34678 Day & Night (stable)', 'B345/S5 Long life (stable)',
                        'B368/S245 Move (stable)', 'B3678/S235678 Stains (stable)', 'B45678/S2345 WalledCities (stable)']
        self.rules_label = tk.Label(self.root, text = 'Rules:', font = 'Arial 18 bold', fg = '#000055', bg = '#00ff00', bd = 2, relief = 'solid')
        self.rules_label.grid(row = 0, column = 1, sticky = tk.NSEW)
        self.rules = ttk.Combobox(self.root, font = 'Calibri 15', state = 'normal', values = self.rules_set)
        self.rules.current(0)
        self.rules.grid(row = 1, column = 1, sticky = tk.NSEW)
        self.saved_positions_values = []
        for text_file in os.listdir(os.getcwd() + '\saved_positions'):
            if '_description.txt' not in text_file:
                self.saved_positions_values.append(text_file[:-4])
        self.saved_positions_values.append("RANDOM")
        self.saved_positions_label = tk.Label(self.root, text = 'Saved positions:', font = 'Arial 15 italic', fg = 'white', bg = 'green', bd = 2, relief = 'solid')
        self.saved_positions_label.grid(row = 0, column = 2, sticky = tk.NSEW)
        self.saved_positions = ttk.Combobox(self.root, font = 'Calibri 15', state = 'readonly', values = self.saved_positions_values)
        self.saved_positions.grid(row = 1, column = 2, sticky = tk.NSEW)
        self.saved_recordings_values = []
        for text_file in os.listdir(os.getcwd() + "\saved_recordings"):
            if '_description.txt' not in text_file:
                self.saved_recordings_values.append(text_file[:-4])
        self.saved_recordings_label = tk.Label(self.root, text = 'Saved recordings:', font = 'Arial 15 italic', fg = 'white', bg = 'green', bd = 2, relief = 'solid')
        self.saved_recordings_label.grid(row = 0, column = 3, sticky = tk.NSEW)
        self.saved_recordings = ttk.Combobox(self.root, font = 'Calibri 15', state = 'readonly', values = self.saved_recordings_values)
        self.saved_recordings.grid(row = 1, column = 3, sticky = tk.NSEW)
        self.root.option_add('*TCombobox*Listbox.font', 'Calibri 15')
        self.rules.bind('<<ComboboxSelected>>', self.change_rules)
        self.rules.bind('<Return>', self.change_rules)
        self.saved_positions.bind('<<ComboboxSelected>>', self.recall_positions)
        self.saved_recordings.bind('<<ComboboxSelected>>', self.recall_recordings)
        self.simulation_graf_background = tk.Frame(self.root, bd = 2, relief = 'solid')
        self.simulation_graf_background.grid(row = 2, column = 2, columnspan = 2, sticky = tk.N)
        self.simulation_graf_width = 580
        self.simulation_graf_height = 280
        self.simulation_graf = tk.Canvas(self.simulation_graf_background, width = int(self.simulation_graf_width), height = int(self.simulation_graf_height), bg = 'white')
        self.simulation_graf.grid(row = 0, column = 0, columnspan = 7, sticky = tk.NSEW)
        self.simulation_graf.bind("<Button-1>", self.show_gen_cells)
        self.simulation_graf.bind("<B1-Motion>", self.move_pointer_graf)
        self.simulation_graf.bind("<Button-3>", self.set_starting_point_focus_rectangle)
        self.simulation_graf.bind("<B3-Motion>", self.create_focus_rectangle)
        self.simulation_graf.bind("<B3-ButtonRelease>", self.zoom_in_simulation_graf)
        self.min_cells_string = tk.StringVar()
        self.times_min_string = tk.StringVar()
        self.max_cells_string = tk.StringVar()
        self.times_max_string = tk.StringVar()
        self.marked_gen_string = tk.StringVar()
        self.min_cells_label = tk.Label(self.simulation_graf_background, text = 'Min:\nTimes:', font = 'Calibri 15 italic', fg = 'black', bg = 'lightcoral')
        self.min_cells_label.grid(row = 1, column = 0, rowspan = 2, sticky = tk.NSEW)
        self.min_cells_string_label = tk.Label(self.simulation_graf_background, textvar = self.min_cells_string, font = 'Calibri 15 bold', fg = 'navy', bg = 'lightcoral')
        self.min_cells_string_label.grid(row = 1, column = 1, sticky = tk.NSEW)
        self.times_min_string_label = tk.Label(self.simulation_graf_background, textvar = self.times_min_string, font = 'Calibri 15 bold', fg = 'navy', bg = 'lightcoral')
        self.times_min_string_label.grid(row = 2, column = 1, sticky = tk.NSEW)
        self.max_cells_label = tk.Label(self.simulation_graf_background, text = 'Max:\nTimes:', font = 'Calibri 15 italic', fg = 'black', bg = 'springgreen')
        self.max_cells_label.grid(row = 1, column = 2, rowspan = 2, sticky = tk.NSEW)
        self.max_cells_string_label = tk.Label(self.simulation_graf_background, textvar = self.max_cells_string, font = 'Calibri 15 bold', fg = 'navy', bg = 'springgreen')
        self.max_cells_string_label.grid(row = 1, column = 3, sticky = tk.NSEW)
        self.times_max_string_label = tk.Label(self.simulation_graf_background, textvar = self.times_max_string, font = 'Calibri 15 bold', fg = 'navy', bg = 'springgreen')
        self.times_max_string_label.grid(row = 2, column = 3, sticky = tk.NSEW)
        self.present_gen_label = tk.Label(self.simulation_graf_background, text = 'Gen:', font = 'Calibri 15 italic', fg = 'black', bg = 'aquamarine')
        self.present_gen_label.grid(row = 1, column = 4, sticky = tk.NSEW)
        self.marked_gen_string_label = tk.Label(self.simulation_graf_background, textvar = self.marked_gen_string, font = 'Calibri 15 bold', fg = 'navy', bg = 'aquamarine')
        self.marked_gen_string_label.grid(row = 2, column = 4, sticky = tk.NSEW)
        self.show_progression_button = tk.Button(self.simulation_graf_background, text = 'Show progression', font = 'Arial 10 bold', fg = 'lightyellow', bg = 'deepskyblue', activeforeground = 'lightyellow', activebackground = 'dodgerblue', command = lambda: self.draw_graf(0, len(self.graf_history) - 1))
        self.show_progression_button.grid(row = 1, column = 5, sticky = tk.NSEW)
        self.reset_simulation_progression_button = tk.Button(self.simulation_graf_background, text = 'Reset', font = 'Arial 10 bold', fg = 'red', bg = 'wheat', activeforeground = 'red', activebackground = 'orange', command = self.reset_simulation_progression)
        self.reset_simulation_progression_button.grid(row = 2, column = 5, sticky = tk.NSEW)
        self.simulation_graf_mode_button = tk.Button(self.simulation_graf_background, text = 'Auto', font = 'Arial 10 bold', fg = 'red', bg = '#00aaaa', activeforeground = 'red', activebackground = '#00ffff', command = self.change_simulation_graf_mode)
        self.simulation_graf_mode_button.grid(row = 1, column = 6, rowspan = 2, sticky = tk.NSEW)
        self.grid_situation_reveal_background = tk.Frame(self.root, bd = 5, relief = 'ridge')
        self.grid_situation_reveal_background.grid(row = 3, column = 2, sticky = tk.N)
        self.grid_situation_reveal_width = 300
        self.grid_situation_reveal_height = 300
        self.grid_situation_reveal = tk.Canvas(self.grid_situation_reveal_background, width = int(self.grid_situation_reveal_width) + self.canvas_offset, height = int(self.grid_situation_reveal_height) + self.canvas_offset, bg = self.colors_list[-1])
        self.grid_situation_reveal.grid(row = 0, column = 0, columnspan = 3, sticky = tk.NSEW)
        self.grid_situation_reveal.bind("<Motion>", self.move_focus_area)
        self.grid_situation_reveal.bind("<Button-1>", self.zoom_in_revealed_grid)
        self.grid_situation_reveal.bind("<Button-3>", self.reveal_whole_grid)
        self.grid_situation_reveal.bind("<MouseWheel>", self.adjust_focus_area)
        self.adjust_from_grid_button = tk.Button(self.grid_situation_reveal_background, text = 'Adjust from grid', font = 'Arial 8 bold', fg = 'azure', bg = 'cornflowerblue', activeforeground = 'azure', activebackground = 'royalblue', command = self.adjust_from_grid)
        self.adjust_from_grid_button.grid(row = 1, column = 0, sticky = tk.NSEW)
        self.adjust_to_grid_button = tk.Button(self.grid_situation_reveal_background, text = 'Adjust to grid', font = 'Arial 8 bold', fg = 'azure', bg = 'cornflowerblue', activeforeground = 'azure', activebackground = 'royalblue', command = self.adjust_to_grid)
        self.adjust_to_grid_button.grid(row = 2, column = 0, sticky = tk.NSEW)
        self.save_grid_position_button = tk.Button(self.grid_situation_reveal_background, text = 'Save', font = 'Arial 10 bold', fg = 'yellow', bg = 'mediumseagreen', activeforeground = 'yellow', activebackground = 'seagreen', command = self.save_grid_position)
        self.save_grid_position_button.grid(row = 1, column = 1, sticky = tk.NSEW)
        self.reset_grid_position_button = tk.Button(self.grid_situation_reveal_background, text = 'Reset', font = 'Arial 10 bold', fg = 'red', bg = 'wheat', activeforeground = 'red', activebackground = 'orange', command = self.reset_grid_position)
        self.reset_grid_position_button.grid(row = 2, column = 1, sticky = tk.NSEW)
        self.grid_reveal_mode_button = tk.Button(self.grid_situation_reveal_background, text = 'Auto', font = 'Arial 10 bold', fg = 'red', bg = '#00aaaa', activeforeground = 'red', activebackground = '#00ffff', command = self.change_grid_reveal_mode)
        self.grid_reveal_mode_button.grid(row = 1, column = 2, rowspan = 2, sticky = tk.NSEW)
        self.information_box_background = tk.Frame(self.root, bd = 2, relief = 'solid')
        self.information_box_background.grid(row = 3, column = 3, sticky = tk.N)
        self.information_box = tk.Text(self.information_box_background, font = 'Calibri 10 bold', width = 38, height = 24)
        self.information_box.grid(row = 0, column = 0, sticky = tk.N)
        '''
	self.information_label_background = tk.Frame(self.root, bd = 2, relief = 'solid')
        self.information_label_background.grid(row = 3, column = 2, columnspan = 2, sticky = tk.NSEW)
        self.information_label = tk.Label(self.information_label_background, text = 'Στην πάνω περιοχή έχεις τη δυνατότητα να καταγράφεις τα δεδομένα της προσομοίωσης σε μορφή\nγραφήματος. Στην κάτω αριστερά περιοχή προβάλλεται μια μικρογραφία της κατάστασης ολόκληρου\nτου πλέγματος προσομοίωσης οποιαδήποτε στιγμή το επιθυμήσεις, ενώ στην κάτω δεξιά μπορείς\nνα ενημερώνεσαι για ό,τι συμβαίνει στο παιχνίδι κατά τη διάρκεια της περιήγησής σου σε αυτό.', font = 'Calibri 9 bold')
        self.information_label.grid(row = 0, column = 0, sticky = tk.NSEW)
	'''
            #------------Δημιουργία εφέ για τα κουμπιά.-------------#
        self.control_grid_limits_button.bind('<Enter>', self.control_grid_limits_button_turn_on)
        self.move_grid_left_button.bind('<Enter>', self.move_grid_left_button_turn_on)
        self.move_grid_up_button.bind('<Enter>', self.move_grid_up_button_turn_on)
        self.move_grid_right_button.bind('<Enter>', self.move_grid_right_button_turn_on)
        self.move_grid_down_button.bind('<Enter>', self.move_grid_down_button_turn_on)
        self.left_rotate_grid_button.bind('<Enter>', self.left_rotate_grid_button_turn_on)
        self.right_rotate_grid_button.bind('<Enter>', self.right_rotate_grid_button_turn_on)
        self.zoomin_grid_button.bind('<Enter>', self.zoomin_grid_button_turn_on)
        self.zoomout_grid_button.bind('<Enter>', self.zoomout_grid_button_turn_on)
        self.clear_button.bind('<Enter>', self.clear_button_turn_on)
        self.step_run_button.bind('<Enter>', self.step_run_button_turn_on)
        self.run_simulation_button.bind('<Enter>', self.run_simulation_button_turn_on)
        self.stop_simulation_button.bind('<Enter>', self.stop_simulation_button_turn_on)
        self.start_recording_button.bind('<Enter>', self.start_recording_button_turn_on)
        self.stop_recording_button.bind('<Enter>', self.stop_recording_button_turn_on)
        self.play_stop_button.bind('<Enter>', self.play_stop_button_turn_on)
        self.play_forward_button.bind('<Enter>', self.play_forward_button_turn_on)
        self.play_reverse_button.bind('<Enter>', self.play_reverse_button_turn_on)
        self.save_recording_button.bind('<Enter>', self.save_recording_button_turn_on)
        self.reset_simulation_information_button.bind('<Enter>', self.reset_simulation_information_button_turn_on)
        self.reset_grid_position_button.bind('<Enter>', self.reset_grid_position_button_turn_on)
        self.reset_simulation_progression_button.bind('<Enter>', self.reset_simulation_progression_button_turn_on)
        self.grid_reveal_mode_button.bind('<Enter>', self.grid_reveal_mode_button_turn_on)
        self.simulation_graf_mode_button.bind('<Enter>', self.simulation_graf_mode_button_turn_on)
        self.adjust_from_grid_button.bind('<Enter>', self.adjust_from_grid_button_turn_on)
        self.adjust_to_grid_button.bind('<Enter>', self.adjust_to_grid_button_turn_on)
        self.save_grid_position_button.bind('<Enter>', self.save_grid_position_button_turn_on)
        self.show_progression_button.bind('<Enter>', self.show_progression_button_turn_on)
        self.control_grid_limits_button.bind('<Leave>', self.buttons_turn_off)
        self.move_grid_left_button.bind('<Leave>', self.buttons_turn_off)
        self.move_grid_up_button.bind('<Leave>', self.buttons_turn_off)
        self.move_grid_right_button.bind('<Leave>', self.buttons_turn_off)
        self.move_grid_down_button.bind('<Leave>', self.buttons_turn_off)
        self.left_rotate_grid_button.bind('<Leave>', self.buttons_turn_off)
        self.right_rotate_grid_button.bind('<Leave>', self.buttons_turn_off)
        self.zoomin_grid_button.bind('<Leave>', self.buttons_turn_off)
        self.zoomout_grid_button.bind('<Leave>', self.buttons_turn_off)
        self.clear_button.bind('<Leave>', self.buttons_turn_off)
        self.step_run_button.bind("<Leave>", self.buttons_turn_off)
        self.run_simulation_button.bind('<Leave>', self.buttons_turn_off)
        self.stop_simulation_button.bind('<Leave>', self.buttons_turn_off)
        self.start_recording_button.bind('<Leave>', self.buttons_turn_off)
        self.stop_recording_button.bind('<Leave>', self.buttons_turn_off)
        self.play_stop_button.bind('<Leave>', self.buttons_turn_off)
        self.play_forward_button.bind('<Leave>', self.buttons_turn_off)
        self.play_reverse_button.bind('<Leave>', self.buttons_turn_off)
        self.save_recording_button.bind('<Leave>', self.buttons_turn_off)
        self.reset_simulation_information_button.bind('<Leave>', self.buttons_turn_off)
        self.reset_grid_position_button.bind('<Leave>', self.buttons_turn_off)
        self.reset_simulation_progression_button.bind('<Leave>', self.buttons_turn_off)
        self.adjust_from_grid_button.bind('<Leave>', self.buttons_turn_off)
        self.adjust_to_grid_button.bind('<Leave>', self.buttons_turn_off)
        self.grid_reveal_mode_button.bind('<Leave>', self.buttons_turn_off)
        self.simulation_graf_mode_button.bind('<Leave>', self.buttons_turn_off)
        self.save_grid_position_button.bind('<Leave>', self.buttons_turn_off)
        self.show_progression_button.bind('<Leave>', self.buttons_turn_off)
            
            #------------Αρχικές ενέργειες.-------------#
        self.stop_simulation_button.configure(state = 'disabled')
        self.stop_recording_button.configure(state = 'disabled')
        self.control_move_label.configure(state = 'disabled')
        self.grid_information_string_inform()
        self.reset_cells_information()
        self.reset_grid_position()
        self.reset_simulation_progression()
        self.reset_simulation_information()
        self.reveal_whole_grid()
    def grid_information_string_inform(self):
        self.grid_information_string.set('Whole grid: {} rows x {} columns.\nAppearing grid: {} rows x {} columns.\nSpecifically: {} row (up), {} column (left).'.format(self.rows,  self.columns, self.right_column - self.left_column + 1, self.right_column - self.left_column + 1, self.up_row + 1, self.left_column + 1))
    def change_grid_colors(self):
        if self.colors_list == self.colors_list_1:
            self.colors_list = self.colors_list_2
        else:
            self.colors_list = self.colors_list_1
        self.grid_colors_button.configure(bg = self.colors_list[-1], fg = self.colors_list[0])
        for i in range(self.up_row, self.down_row + 1):
            for j in range(self.left_column, self.right_column + 1):
                if self.grid_cells[i][j].control_press == 'unpressed':
                    self.grid_background.itemconfigure(self.grid_cells[i][j].button, fill = self.colors_list[-1])
                elif self.grid_cells[i][j].control_press == 'pressed':
                    self.grid_background.itemconfigure(self.grid_cells[i][j].button, fill = self.colors_list[self.grid_cells[i][j].choose_color])
        self.grid_situation_reveal.configure(bg = self.colors_list[-1])
        self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
    def adjust_pieces_gap(self, event = None):
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid_cells[i][j].button_width = self.cells_gap_scaler.get()
        self.update_grid()
    def turn_on_off_limits(self):
        if 'enabled' in self.control_grid_limits_button['text']:
            self.control_grid_limits_button.configure(text = 'Control grid\nborders (disabled)')
            self.control_grid_limits_button.configure(bg = 'red')
            self.control_grid_limits_string = 'inside'
        elif 'disabled' in self.control_grid_limits_button['text']:
            self.control_grid_limits_button.configure(text = 'Control grid\nborders (enabled)')
            self.control_grid_limits_button.configure(bg = 'green')
    #------------Εφέ κουμπιών.-------------#
    def control_grid_limits_button_turn_on(self, event):
        self.control_grid_limits_button.configure(fg = 'white')
    def move_grid_left_button_turn_on(self, event):
        self.move_grid_left_button.configure(fg = 'yellow')
    def move_grid_up_button_turn_on(self, event):
        self.move_grid_up_button.configure(fg = 'yellow')
    def move_grid_right_button_turn_on(self, event):
        self.move_grid_right_button.configure(fg = 'yellow')
    def move_grid_down_button_turn_on(self, event):
        self.move_grid_down_button.configure(fg = 'yellow')
    def left_rotate_grid_button_turn_on(self, event):
        self.left_rotate_grid_button.configure(fg = 'yellow')
    def right_rotate_grid_button_turn_on(self, event):
        self.right_rotate_grid_button.configure(fg = 'yellow')
    def zoomin_grid_button_turn_on(self, event):
        self.zoomin_grid_button.configure(fg = 'red')
    def zoomout_grid_button_turn_on(self, event):
        self.zoomout_grid_button.configure(fg = 'red')
    def clear_button_turn_on(self, event):
        if self.clear_button['state'] == 'normal':
            self.clear_button.configure(bg = 'black')
    def step_run_button_turn_on(self, event):
        if self.step_run_button['state'] == 'normal':
            self.step_run_button.configure(fg = 'white')
    def run_simulation_button_turn_on(self, event):
        if self.run_simulation_button['state'] == 'normal':
            self.run_simulation_button.configure(bg = 'blue')
    def stop_simulation_button_turn_on(self, event):
        if self.stop_simulation_button['state'] == 'normal':
            self.stop_simulation_button.configure(bg = 'red')
    def start_recording_button_turn_on(self, event):
        if self.start_recording_button['state'] == 'normal':
            self.start_recording_button.configure(bg = 'lime')
    def stop_recording_button_turn_on(self, event):
        if self.stop_recording_button['state'] == 'normal':
            self.stop_recording_button.configure(bg = 'lime')
    def play_stop_button_turn_on(self, event):
        if self.play_stop_button['state'] == 'normal':
            self.play_stop_button.configure(bg = 'lime')
    def play_forward_button_turn_on(self, event):
        if self.play_forward_button['state'] == 'normal':
            self.play_forward_button.configure(bg = 'lime')
    def play_reverse_button_turn_on(self, event):
        if self.play_reverse_button['state'] == 'normal':
            self.play_reverse_button.configure(bg = 'lime')
    def save_recording_button_turn_on(self, event):
        self.save_recording_button.configure(bg = 'springgreen')
    def reset_simulation_information_button_turn_on(self, event):
        self.reset_simulation_information_button.configure(bg = 'orange')
    def reset_grid_position_button_turn_on(self, event):
        self.reset_grid_position_button.configure(bg = 'orange')
    def reset_simulation_progression_button_turn_on(self, event):
        self.reset_simulation_progression_button.configure(bg = 'orange')
    def grid_reveal_mode_button_turn_on(self, event):
        self.grid_reveal_mode_button.configure(bg = '#00ffff')
    def simulation_graf_mode_button_turn_on(self, event):
        self.simulation_graf_mode_button.configure(bg = '#00ffff')
    def adjust_from_grid_button_turn_on(self, event):
        self.adjust_from_grid_button.configure(bg = 'royalblue')
    def adjust_to_grid_button_turn_on(self, event):
        self.adjust_to_grid_button.configure(bg = 'royalblue')
    def save_grid_position_button_turn_on(self, event):
        self.save_grid_position_button.configure(bg = 'seagreen')
    def show_progression_button_turn_on(self, event):
        self.show_progression_button.configure(bg = 'dodgerblue')
    def buttons_turn_off(self, event):
        self.control_grid_limits_button.configure(fg = 'black')
        self.move_grid_left_button.configure(fg = 'black')
        self.move_grid_up_button.configure(fg = 'black')
        self.move_grid_right_button.configure(fg = 'black')
        self.move_grid_down_button.configure(fg = 'black')
        self.left_rotate_grid_button.configure(fg = 'black')
        self.right_rotate_grid_button.configure(fg = 'black')
        self.zoomin_grid_button.configure(fg = 'black')
        self.zoomout_grid_button.configure(fg = 'black')
        self.clear_button.configure(bg = 'brown')
        self.step_run_button.configure(fg = 'black')
        self.run_simulation_button.configure(bg = 'lightblue')
        self.stop_simulation_button.configure(bg = 'lightblue')
        self.start_recording_button.configure(bg = 'turquoise')
        self.stop_recording_button.configure(bg = 'turquoise')
        self.play_stop_button.configure(bg = 'khaki')
        self.play_forward_button.configure(bg = 'khaki')
        self.play_reverse_button.configure(bg = 'khaki')
        self.save_recording_button.configure(bg = 'khaki')
        self.reset_simulation_information_button.configure(bg = 'wheat')
        self.reset_grid_position_button.configure(bg = 'wheat')
        self.reset_simulation_progression_button.configure(bg = 'wheat')
        self.grid_reveal_mode_button.configure(bg = '#00aaaa')
        self.simulation_graf_mode_button.configure(bg = '#00aaaa')
        self.adjust_from_grid_button.configure(bg = 'cornflowerblue')
        self.adjust_to_grid_button.configure(bg = 'cornflowerblue')
        self.save_grid_position_button.configure(bg = 'mediumseagreen')
        self.show_progression_button.configure(bg = 'deepskyblue')
    #------------Συνάρτηση για αλλαγή κανόνων παιχνιδιού.-------------#
    def change_rules(self, event = None):
        self.control_rule = True
        self.chosen_rule = self.rules.get()
        self.born_rules = []
        self.survive_rules = []
        self.rule_code = self.chosen_rule.split(' ')[0]
        try:
            if self.rule_code != '':
                if self.rule_code[0] == 'B':
                    self.index = 1
                    while self.index != len(self.rule_code) - 1 and self.rule_code[self.index] != '/':
                        if self.rule_code[self.index].isdigit() and int(self.rule_code[self.index]) in range(9) and self.born_rules.count(int(self.rule_code[self.index])) == 0:
                            self.born_rules.append(int(self.rule_code[self.index]))
                        else:
                            self.control_rule = False
                            break
                        self.index += 1
                else:
                    self.control_rule = False
                if self.rule_code[self.index + 1] == 'S':
                    for element in range(self.index + 2, len(self.rule_code)):
                        if self.rule_code[element].isdigit() and int(self.rule_code[element]) in range(9) and self.survive_rules.count(int(self.rule_code[element])) == 0:
                            self.survive_rules.append(int(self.rule_code[element]))
                        else:
                            self.control_rule = False
                else:
                    self.control_rule = False
            else:
                self.control_rule = False
            if self.control_rule == True:
                self.rules.set(self.rule_code)
                for element in self.rules_set:
                    if self.rule_code == element.split(' ')[0]:
                        self.rules.set(element)
                self.write_information_box('Game rule chosen', 'navy', '\n{}'.format(self.rules.get()))
            else:
                self.write_information_box('Warning', 'red', 'Ο κανόνας που εισαγάγατε δεν είναι έγκυρος. Πρέπει να ακολουθεί το πρότυπο \'R___.../S___...\', όπου τα δύο πεδία με τις παύλες θα περιέχουν διακριτούς αριθμούς από το 0 μέχρι το 8 σε κάθε πεδίο.\nThe rule you entered is not valid. It has to follow the pattern \'R___.../S___...\', where the two fields with the dashes must contain discrete numbers from 0 to 8.')
                self.rules.set(self.rules_set[0])
                self.change_rules()
        except:
            self.write_information_box('Warning', 'red', 'Ο κανόνας που εισαγάγατε δεν είναι έγκυρος. Πρέπει να ακολουθεί το πρότυπο \'R___.../S___...\', όπου τα δύο πεδία με τις παύλες θα περιέχουν διακριτούς αριθμούς από το 0 μέχρι το 8 σε κάθε πεδίο.\nThe rule you entered is not valid. It has to follow the pattern \'R___.../S___...\', where the two fields with the dashes must contain discrete numbers from 0 to 8.')
            self.rules.set(self.rules_set[0])
            self.change_rules()
    #------------Κινήσεις πλέγματος.-------------#
    def update_grid(self):
        self.grid_background.delete("all")
        for i in range(self.up_row, self.down_row + 1):
            for j in range(self.left_column, self.right_column + 1):
                self.grid_cells[i][j].set_button_on_grid(i - self.up_row, j - self.left_column)
                if self.grid_cells[i][j].control_press == 'pressed':
                    self.grid_background.itemconfigure(self.grid_cells[i][j].button, fill = self.colors_list[self.grid_cells[i][j].choose_color])
                else:
                    self.grid_background.itemconfigure(self.grid_cells[i][j].button, fill = self.colors_list[-1])
    def grid_up(self):
        if self.up_row != 0:
            self.up_row -= 1
            self.down_row -= 1
            self.update_grid()
            self.grid_information_string_inform()
    def grid_left(self):
        if self.left_column != 0:
            self.left_column -= 1
            self.right_column -= 1
            self.update_grid()
            self.grid_information_string_inform()
    def grid_right(self):
        if self.right_column != 99:
            self.left_column += 1
            self.right_column += 1
            self.update_grid()
            self.grid_information_string_inform()
    def grid_down(self):
        if self.down_row != 99:
            self.up_row += 1
            self.down_row += 1
            self.update_grid()
            self.grid_information_string_inform()
    def grid_rotate(self, rotation_direction):
        self.grid_cells_info = []
        for i in range(self.up_row, self.down_row + 1):
            self.grid_cells_info_row = []
            for j in range(self.left_column, self.right_column + 1):
                self.grid_cells_info_element = []
                self.grid_cells_info_element.append(self.grid_cells[i][j].control_press)
                self.grid_cells_info_element.append(self.grid_cells[i][j].choose_color)
                if self.grid_cells[i][j].control_press == "pressed":
                    self.grid_cells_info_element.append(self.colors_list[self.grid_cells[i][j].choose_color])
                else:
                    self.grid_cells_info_element.append(self.colors_list[-1])
                self.grid_cells_info_element.append(self.grid_cells[i][j].control_highlight)
                self.grid_cells_info_row.append(self.grid_cells_info_element)
            self.grid_cells_info.append(self.grid_cells_info_row)
        for i in range(self.up_row, self.down_row + 1):
            for j in range(self.left_column, self.right_column + 1):
                self.x_old = j - self.left_column
                self.y_old = i - self.up_row
                if rotation_direction == 'left':
                    self.x_new = int(i + (self.left_column + self.right_column - self.up_row - self.down_row) / 2)
                    self.y_new = int(-j + (self.left_column + self.right_column + self.up_row + self.down_row) / 2)
                elif rotation_direction == 'right':
                    self.x_new = int(-i + (self.left_column + self.right_column + self.up_row + self.down_row) / 2)
                    self.y_new = int(j + (- self.left_column - self.right_column + self.up_row + self.down_row) / 2)
                self.grid_cells[self.y_new][self.x_new].control_press = self.grid_cells_info[self.y_old][self.x_old][0]
                self.grid_cells[self.y_new][self.x_new].choose_color = self.grid_cells_info[self.y_old][self.x_old][1]
                self.grid_background.itemconfigure(self.grid_cells[self.y_new][self.x_new].button, fill = self.grid_cells_info[self.y_old][self.x_old][2])
                self.grid_cells[self.y_new][self.x_new].control_highlight = self.grid_cells_info[self.y_old][self.x_old][3]
        if self.grid_reveal_mode_button['text'] == 'Auto':
            self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
    def grid_zoom_in(self):
        if self.right_column - self.left_column != 1:
            self.left_column += 1
            self.right_column -= 1
            self.up_row += 1
            self.down_row -= 1
            self.new_button_size = self.grid_size / (self.right_column - self.left_column + 1)
            for i in range(self.rows):
                for j in range(self.columns):
                    self.grid_cells[i][j].button_size = self.new_button_size
            self.update_grid()
            self.grid_information_string_inform()
    def grid_zoom_out(self):
        if self.right_column - self.left_column != 99 and self.left_column != 0 and self.up_row != 0 and self.right_column != 99 and self.down_row != 99:
            self.left_column -= 1
            self.right_column += 1
            self.up_row -= 1
            self.down_row += 1
            self.new_button_size = self.grid_size / (self.right_column - self.left_column + 1)
            for i in range(self.rows):
                for j in range(self.columns):
                    self.grid_cells[i][j].button_size = self.new_button_size
            self.update_grid()
            self.grid_information_string_inform()
    #------------Λειτουργίες προσομοίωσης.-------------#
    def clear_grid(self):
        self.control_grid_limits_string = 'inside'
        self.reset_cells_information()
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid_cells[i][j].control_press == 'pressed':
                    self.grid_cells[i][j].button_pressed()
        self.recording_history = []
        self.recording_pointer = 0
        self.graf_history = []
        self.reset_simulation_information()
    def run(self):
        if self.go_to_gen_mode == 'off':
            if self.grid_reveal_mode_button['text'] == 'Auto':
                self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
            if self.simulation_graf_mode_button['text'] == 'Auto':
                self.reset_simulation_progression()
                self.draw_graf(0, len(self.graf_history) - 1)
        self.simulation_state = 'run_simulation'
        if int(self.generations_string.get()) == 0:
            self.graf_history.append(int(self.finally_cells_string.get()))
            if self.recording_state == 'run_recording':
                self.recording_history_element = []
                for i in range(self.rows):
                    for j in range(self.columns):
                        if self.grid_cells[i][j].control_press == 'pressed':
                            self.recording_history_element.append([i, j])
                self.recording_history.append(self.recording_history_element)
        self.step_run_button.configure(state = 'disabled')
        self.run_simulation_button.configure(state = 'disabled')
        self.clear_button.configure(state = 'disabled')
        self.stop_simulation_button.configure(state = 'normal')
        self.stop_recording_button.configure(state = 'disabled')
        self.switched_cells = []
        self.births = 0
        self.deaths = 0
        self.neighboors = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid_cells[i - 1][j - 1].control_press == 'pressed':
                    self.neighboors += 1
                if self.grid_cells[i - 1][j].control_press == 'pressed':
                    self.neighboors += 1
                if self.grid_cells[i - 1][(j + 1) % self.rows].control_press == 'pressed':
                    self.neighboors += 1
                if self.grid_cells[i][j - 1].control_press == 'pressed':
                    self.neighboors += 1
                if self.grid_cells[i][(j + 1) % self.rows].control_press == 'pressed':
                    self.neighboors += 1
                if self.grid_cells[(i + 1) % self.columns][j - 1].control_press == 'pressed':
                    self.neighboors += 1
                if self.grid_cells[(i + 1) % self.columns][j].control_press == 'pressed':
                    self.neighboors += 1
                if self.grid_cells[(i + 1) % self.columns][(j + 1) % self.rows].control_press == 'pressed':
                    self.neighboors += 1
                if self.grid_cells[i][j].control_press == 'unpressed' and self.neighboors in self.born_rules:
                    self.births = self.births + 1
                    self.switched_cells.append([i, j])
                elif self.grid_cells[i][j].control_press == 'pressed' and self.neighboors not in self.survive_rules:
                    self.deaths = self.deaths + 1
                    self.switched_cells.append([i, j])
                self.neighboors = 0
        if self.go_to_gen_mode == 'off':
            self.final_gen_simulation_graf += 1
            self.root.after(int(self.speed / self.speed_control_button.get()), self.switch_matrix_simulation)
        elif self.go_to_gen_mode == 'on':
            pass         
    def switch_matrix_simulation(self):
        if self.simulation_state == 'stop_simulation':
            pass
        elif self.simulation_state == 'run_simulation':
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.grid_cells[i][j].control_press == 'pressed':
                        if self.grid_cells[i][j].choose_color != len(self.colors_list) - 2:
                            self.grid_cells[i][j].choose_color += 1
                            self.grid_background.itemconfigure(self.grid_cells[i][j].button, fill = self.colors_list[self.grid_cells[i][j].choose_color])
            if 'enabled' in self.control_grid_limits_button['text']:
                for cell in self.switched_cells:
                    if cell[0] == 1 or cell[0] == self.rows - 2 or cell[1] == 1 or cell[1] == self.columns - 2:
                        self.write_information_box('Warning', 'red', 'Η προσομοίωση πηγαίνει να κινηθεί εκτός ορίων πλέγματος (πιθανότατα λόγω κάποιου glider), για αυτό διακόπηκε αυτόματα. Αν επιθυμείς να συνεχίσει απενεργοποίησε τον έλεγχο ορίων πλέγματος, οπότε η προσομοίωση θα κινείται σε σύμπαν τόρου.\nThe simulation is going to move out of the grid borders (probably due to some glider), so it was automatically stopped. If you want it to continue, disable the borders check, so the simulation will then move inside a torus universe.')
                        self.control_grid_limits_string = 'outside'
                        self.stop()
                        break
            if 'disabled' in self.control_grid_limits_button['text'] or ('enabled' in self.control_grid_limits_button['text'] and self.control_grid_limits_string == 'inside'):
                self.generations_string.set(int(self.generations_string.get()) + 1)
                self.birth_cells_string.set(int(self.birth_cells_string.get()) + self.births)
                self.death_cells_string.set(int(self.death_cells_string.get()) + self.deaths)
                self.finally_cells_string.set(int(self.finally_cells_string.get()) + self.births - self.deaths)
                for cell in self.switched_cells:
                    self.grid_cells[cell[0]][cell[1]].button_pressed()
                if self.recording_state == 'run_recording':
                    if self.switched_cells != []:
                        self.recording_history.append(self.switched_cells)
                self.graf_history.append(int(self.finally_cells_string.get()))
            if self.simulation_state == 'run_simulation' and self.go_to_gen_mode == 'off':
                self.run()
            elif self.go_to_gen_mode == 'on':
                pass
    def go_to_gen(self, event):
        if self.go_to_gen_string.get() != '':
            self.transfer_gen = int(self.go_to_gen_string.get())
            if self.transfer_gen <= int(self.generations_string.get()):
                self.write_information_box('Warning', 'red', 'Μπορείς να μεταφερθείς μόνο σε μεταγενέστερες γενιές!\nYou can only pass on to the next generations!')
            else:
                self.go_to_gen_mode = 'on'
                self.present_gen = int(self.generations_string.get())
                for i in range(self.transfer_gen - self.present_gen):
                    self.run()
                    self.switch_matrix_simulation()
                if self.grid_reveal_mode_button['text'] == 'Auto':
                    self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
                if self.simulation_graf_mode_button['text'] == 'Auto':
                    self.reset_simulation_progression()
                    self.draw_graf(0, len(self.graf_history) - 1)
                self.go_to_gen_mode = 'off'
                self.stop()
    def step_run(self):
        self.go_to_gen_mode = 'on'
        self.run()
        self.switch_matrix_simulation()
        self.go_to_gen_mode = 'off'
        self.stop()
        if self.grid_reveal_mode_button['text'] == 'Auto':
            self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
        if self.simulation_graf_mode_button['text'] == 'Auto':
            self.reset_simulation_progression()
            self.draw_graf(0, len(self.graf_history) - 1)
    def stop(self):
        self.simulation_state = 'stop_simulation'
        self.clear_button.configure(state = 'normal')
        self.stop_simulation_button.configure(state = 'disabled')
        self.step_run_button.configure(state = 'normal')
        self.run_simulation_button.configure(state = 'normal')
        if self.recording_state == 'run_recording':
            self.stop_recording_button.configure(state = 'normal')
    def start_recording(self):
        self.start_recording_button.configure(state = 'disabled')
        self.stop_recording_button.configure(state = 'normal')
        self.play_stop_button.configure(state = 'disabled')
        self.play_forward_button.configure(state = 'disabled')
        self.play_reverse_button.configure(state = 'disabled')
        self.recording_state = 'run_recording'
        self.recording_history = []
        self.write_information_box('Guide', 'orange', 'Για να ξεκινήσει η καταγραφή της προσομοίωσης πάτησε το "Run" και όποτε επιθυμήσεις να σταματήσεις πάτησε το "Stop" και το "Stop recording".\nTo start recording the simulation press "Run" and whenever you wish to stop press "Stop" and then "Stop recording".')
    def stop_recording(self):
        self.start_recording_button.configure(state = 'normal')
        self.stop_recording_button.configure(state = 'disabled')
        self.play_stop_button.configure(state = 'normal')
        self.play_forward_button.configure(state = 'normal')
        self.play_reverse_button.configure(state = 'normal')
        self.recording_state = 'stop_recording'
        if self.recording_history.count([]) != len(self.recording_history):
            self.write_information_box('Warning', 'red', 'Για τη διαχείριση της προσωρινώς αποθηκευμένης καταγραφής χρησιμοποίησε μόνο τα κουμπιά "play", "reverse", "forward" και όχι το "Run".\nTo manage the temporarily saved recording use only the "play", "reverse", "forward" buttons and not the "Run" button.')
        self.recording_pointer = len(self.recording_history) - 1
        self.reminder_pointer = self.recording_pointer
    def play_stop_recording(self):
        if self.play_stop_button['text'] == '⯈':
            self.recording_play_stop_state = 'play'
            self.play_stop_button.configure(text = '◼')
            self.play_forward_button.configure(state = 'disabled')
            self.play_reverse_button.configure(state = 'disabled')
            if self.recording_pointer != len(self.recording_history) - 1 and self.play_direction_state == 'forward':
                self.recording_pointer -= 1
            elif self.recording_pointer != 1 and self.play_direction_state == 'reverse':
                self.recording_pointer += 1
            self.play_next_frame()
        elif self.play_stop_button['text'] == '◼':
            self.recording_play_stop_state = 'stop'
            self.play_forward_button.configure(state = 'normal')
            self.play_reverse_button.configure(state = 'normal')
            self.play_stop_button.configure(text = '⯈')
            self.reminder_pointer = self.recording_pointer
            self.reminder_direction = self.play_direction_state
    def play_next_frame(self):
        try:
            if self.recording_play_stop_state == 'play':
                if self.play_direction_state == 'forward':
                    if self.recording_pointer == len(self.recording_history) - 1:
                        self.play_stop_recording()
                    else:
                        self.recording_pointer += 1
                        self.switched_cells = self.recording_history[self.recording_pointer]
                        if self.simulation_graf_mode_button['text'] == 'Auto':
                            self.reset_simulation_progression()
                            self.draw_graf(0, len(self.graf_history) - 1)
                        self.root.after(int(self.speed / self.speed_control_button.get()), self.switch_matrix_recording)
                elif self.play_direction_state == 'reverse':
                    if self.recording_pointer == 1:
                        self.play_stop_recording()                    
                    else:
                        self.recording_pointer -= 1
                        self.switched_cells = self.recording_history[self.recording_pointer]
                        if self.simulation_graf_mode_button['text'] == 'Auto':
                            self.reset_simulation_progression()
                            self.draw_graf(0, len(self.graf_history) - 1)
                        self.root.after(int(self.speed / self.speed_control_button.get()), self.switch_matrix_recording)
        except:
            pass
    def switch_matrix_recording(self):
        if self.recording_play_stop_state == 'stop':
            pass
        elif self.recording_play_stop_state == 'play':
            if self.play_direction_state == 'forward':
                self.generations_string.set(int(self.generations_string.get()) + 1)
            if self.play_direction_state == 'reverse':
                self.generations_string.set(int(self.generations_string.get()) - 1)
            for cell in self.switched_cells:
                self.grid_cells[cell[0]][cell[1]].button_pressed()
            if self.grid_reveal_mode_button['text'] == 'Auto':
                self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
            self.play_next_frame()
    def play_forward_recording(self):
        self.play_forward_button.configure(fg = 'crimson')
        self.play_reverse_button.configure(fg = 'black')
        self.play_direction_state = 'forward'
        try:
            if self.recording_pointer != len(self.recording_history) - 1 and self.recording_pointer != 1:
                if self.reminder_direction == 'reverse':
                    self.reminder_direction = 'forward'
                    self.recording_pointer = self.reminder_pointer + 1
        except:
            pass
    def play_reverse_recording(self):
        self.play_forward_button.configure(fg = 'black')
        self.play_reverse_button.configure(fg = 'crimson')
        self.play_direction_state = 'reverse'
        try:
            if self.recording_pointer != 1 and self.recording_pointer != len(self.recording_history) - 1:
                if self.reminder_direction == 'forward':
                    self.reminder_direction = 'reverse'
                    self.recording_pointer = self.reminder_pointer - 1
        except:
            pass
    def save_recording(self):
        if self.recording_history.count([]) != len(self.recording_history):
            self.ask_recording_name = sd.askstring(parent = self.root, title = 'Recording name', prompt = 'Give the name of the recording:')
            if self.ask_recording_name != None and self.ask_recording_name != "":
                if (self.ask_recording_name + '.txt') not in os.listdir(os.getcwd() + "/saved_recordings"):
                    self.recording_file = open(os.getcwd() + "/saved_recordings/{}.txt".format(self.ask_recording_name), "a+", encoding = "UTF-8")
                    for gen in self.recording_history:
                        for cell in gen:
                            self.recording_file.write(str(cell[0]) + ',')
                            self.recording_file.write(str(cell[1]) + ',')
                        self.recording_file.write('\n')
                    for cells in self.graf_history:
                        self.recording_file.write(str(cells) + ',')
                    self.recording_file.close()
                    self.saved_recordings_values.append(self.ask_recording_name)
                    self.saved_recordings['values'] = self.saved_recordings_values
                    self.ask_recording_description = sd.askstring(parent = self.root, title = 'Recording desription', prompt = 'Give the description of the recording:')
                    self.recording_description_file = open(os.getcwd() + "/saved_recordings/{}_description.txt".format(self.ask_recording_name), "w", encoding = "UTF-8")
                    if self.ask_recording_description != None and self.ask_recording_description != "":
                        self.recording_description_file.write(self.ask_recording_description)
                    else:
                        self.recording_description_file.write("Η καταγραφή δεν διαθέτει περιγραφή.\nThe recording does not include description.")
                    self.recording_description_file.close()
                else:
                    self.write_information_box('Warning', 'red', 'Το όνομα που πληκτρολόγησες χρησιμοποιείται ήδη για μια άλλη καταγραφή! Επίλεξε διαφορετικό όνομα!\nThe name you typed is already being used by another recording! Choose a different name!')
        else:
            self.write_information_box('Guide', 'orange', 'Δημιούργησε πρώτα μία καταγραφή με το "Start recording" και στη συνέχεια αποθήκευσέ την.\nFirst create a recording with "Start recording" and then save it.')
    #------------Παραπάνω λειτουργίες.-------------#
    def draw_graf(self, initial_gen, final_gen):
        if self.generations_string.get() == '0':
            self.write_information_box('Guide', 'orange', 'Πράσινη κουκίδα: μέγιστο, κόκκινη κουκίδα: ελάχιστο, μπλε κουκίδα: δείκτης χρονικής στιγμής της προσομοίωσης (χρησιμεύει κυρίως στις καταγραφές).\nGreen dot: maximum, red dot: minimum, blue dot: simulation time point (mainly used for recordings).')
        if self.graf_history.count(0) != len(self.graf_history):
            self.min_cells = min(self.graf_history)
            self.min_cells_count = self.graf_history.count(self.min_cells)
            self.max_cells = max(self.graf_history)
            self.max_cells_count = self.graf_history.count(self.max_cells)
            self.x_previous = (1 / (final_gen - initial_gen + 4)) * self.simulation_graf_width
            self.y_previous = - (self.graf_history[initial_gen] / (self.max_cells + 20) - 1) * self.simulation_graf_height
            if self.graf_history[initial_gen] == self.min_cells:
                self.simulation_graf.create_oval(self.x_previous - 3, self.y_previous - 3, self.x_previous + 3, self.y_previous + 3, fill = 'red')
            elif self.graf_history[initial_gen] == self.max_cells:
                self.simulation_graf.create_oval(self.x_previous - 3, self.y_previous - 3, self.x_previous + 3, self.y_previous + 3, fill = 'green')
            if self.max_cells != 0:
                for i in range(1, final_gen - initial_gen + 1):
                    self.x_after = ((i + 1) / (final_gen - initial_gen + 4)) * self.simulation_graf_width
                    self.y_after = - (self.graf_history[initial_gen + i] / (self.max_cells + 20) - 1) * self.simulation_graf_height
                    self.simulation_graf.create_line(self.x_previous, self.y_previous, self.x_after, self.y_after, fill = 'brown')
                    if self.graf_history[initial_gen + i] == self.min_cells:
                        self.simulation_graf.create_oval(self.x_after - 3, self.y_after - 3, self.x_after + 3, self.y_after + 3, fill = 'red')
                    elif self.graf_history[initial_gen + i] == self.max_cells:
                        self.simulation_graf.create_oval(self.x_after - 3, self.y_after - 3, self.x_after + 3, self.y_after + 3, fill = 'green')
                    self.x_previous = self.x_after
                    self.y_previous = self.y_after
                self.x_after = ((int(self.generations_string.get()) + 1) / (final_gen - initial_gen + 4)) * self.simulation_graf_width
                self.y_after = - (self.graf_history[int(self.generations_string.get())] / (self.max_cells + 20) - 1) * self.simulation_graf_height
                self.simulation_graf.create_oval(self.x_after - 3, self.y_after - 3, self.x_after + 3, self.y_after + 3, fill = 'blue')
                self.max_cells_string.set(self.max_cells)
                self.times_max_string.set(self.max_cells_count)
                self.min_cells_string.set(self.min_cells)
                self.times_min_string.set(self.min_cells_count)
        else:
            self.write_information_box('Warning', 'red', "Δεν υπάρχουν δεδομένα προσομοίωσης!\nThere are no simulation data!")
    def show_gen_cells(self, event):
        if self.marked_gen_string.get().isdigit() and int(self.marked_gen_string.get()) >= 0:
            try:
                self.write_information_box('Noted generation', 'purple', "{} ({} cells)".format(self.marked_gen_string.get(), self.graf_history[int(self.marked_gen_string.get())]))
            except:
                self.write_information_box('Warning', 'red', "Δεν υπάρχουν δεδομένα για τη συγκεκριμένη γενιά!\nThere are no data for this generation!")
    def move_pointer_graf(self, event):
        try:
            self.simulation_graf.delete(self.pointer_graf)
        except:
            pass
        self.pointer_graf = self.simulation_graf.create_line(event.x, 0, event.x, self.simulation_graf_height, fill = 'brown', dash = 5)
        self.marked_gen_string.set(self.initial_gen_simulation_graf + int(event.x / self.simulation_graf_width * (self.final_gen_simulation_graf - self.initial_gen_simulation_graf + 4)) - 1)
    def set_starting_point_focus_rectangle(self, event):
        self.xcor2 = event.x
        self.ycor2 = event.y
    def create_focus_rectangle(self, event):
        try:
            self.simulation_graf.delete(self.focus_rectangle)
        except:
            pass
        try:
            self.xcor3 = event.x
            self.ycor3 = event.y
        except:
            pass
        self.initial_gen_simulation_graf = self.initial_gen_simulation_graf + int(self.xcor2 / self.simulation_graf_width * (self.final_gen_simulation_graf - self.initial_gen_simulation_graf + 4)) - 1
        self.final_gen_simulation_graf = self.initial_gen_simulation_graf + int(self.xcor3 / self.simulation_graf_width * (self.final_gen_simulation_graf - self.initial_gen_simulation_graf + 4)) - 1
        self.focus_rectangle = self.simulation_graf.create_rectangle(self.xcor2, self.ycor2, self.xcor3, self.ycor3, outline = 'black')
    def zoom_in_simulation_graf(self, event):
        self.reset_simulation_progression()
        self.draw_graf(int(self.xcor2 / self.simulation_graf_width * (len(self.graf_history) + 3) - 1), int(self.xcor3 / self.simulation_graf_width * (len(self.graf_history) + 3) - 1))
    def scan_grid(self, left_column, right_column, up_row, down_row):
        self.reset_grid_position()
        self.size_x = self.grid_situation_reveal_width / (right_column - left_column + 1)
        self.size_y = self.grid_situation_reveal_height / (down_row - up_row + 1)
        self.semiside_focus_area = 1 + self.size_x / 2
        for row in range(up_row, down_row + 1):
            for column in range(left_column, right_column + 1):
                if self.grid_cells[row % self.rows][column % self.columns].control_press == 'pressed':
                    self.x = (column - left_column + 0.5) * self.size_x + self.canvas_offset
                    self.y = (row - up_row + 0.5) * self.size_y + self.canvas_offset
                    self.grid_situation_reveal.create_rectangle(self.x - self.size_x / 2, self.y - self.size_y / 2, self.x + self.size_x / 2, self.y + self.size_y / 2, fill = self.colors_list[self.grid_cells[row % self.rows][column % self.columns].choose_color], outline = self.colors_list[self.grid_cells[row % self.rows][column % self.columns].choose_color], activefill = 'red')
                    self.saved_grid_position.append([row, column])
    def adjust_from_grid(self):
        self.revealed_left_column = self.left_column
        self.revealed_right_column = self.right_column
        self.revealed_up_row = self.up_row
        self.revealed_down_row = self.down_row
        self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
    def adjust_to_grid(self):
        self.left_column = self.revealed_left_column
        self.right_column = self.revealed_right_column
        self.up_row = self.revealed_up_row
        self.down_row = self.revealed_down_row
        self.new_button_size = self.grid_size / (self.right_column - self.left_column + 1)
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid_cells[i][j].button_size = self.new_button_size
        self.update_grid()
        self.grid_information_string_inform()
    def reveal_whole_grid(self, event = None):
        self.revealed_left_column = 0
        self.revealed_right_column = self.columns - 1
        self.revealed_up_row = 0
        self.revealed_down_row = self.rows - 1
        self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
    def zoom_in_revealed_grid(self, event):
        self.centre_column = int(event.x / self.size_x)
        self.centre_row = int(event.y / self.size_y)
        self.rows_columns_number = int(2 * (self.semiside_focus_area - 0.5) / self.size_x)
        if self.rows_columns_number % 2 != 0:
            self.revealed_left_column += self.centre_column - int((self.rows_columns_number - 1) / 2)
            self.revealed_right_column = self.revealed_left_column + self.rows_columns_number - 1
            self.revealed_up_row += self.centre_row - int((self.rows_columns_number - 1) / 2)
            self.revealed_down_row = self.revealed_up_row + self.rows_columns_number - 1
        else:
            self.revealed_left_column += self.centre_column - int(self.rows_columns_number / 2)
            self.revealed_right_column = self.revealed_left_column + self.rows_columns_number - 1
            self.revealed_up_row += self.centre_row - int(self.rows_columns_number / 2)
            self.revealed_down_row = self.revealed_up_row + self.rows_columns_number - 1
        self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
        self.write_information_box('Appearing grid', 'brown', '\n Grid size: {}x{}\nRows: {} - {}\nColumns: {} - {}'.format(self.rows_columns_number, self.rows_columns_number, self.revealed_up_row + 1, self.revealed_down_row + 1, self.revealed_left_column + 1, self.revealed_right_column + 1))
    def move_focus_area(self, event = None):
        try:
            self.grid_situation_reveal.delete(self.focus_area)
        except:
            pass
        try:
            self.xcor = event.x
            self.ycor = event.y
        except:
            pass
        self.focus_area = self.grid_situation_reveal.create_rectangle(self.xcor - self.semiside_focus_area, self.ycor - self.semiside_focus_area, self.xcor + self.semiside_focus_area, self.ycor + self.semiside_focus_area, width = 2, outline = 'lime')
    def adjust_focus_area(self, event):
        if event.delta == 120:
            self.semiside_focus_area += self.size_x / 2
            self.move_focus_area()
        elif event.delta == -120:
            self.semiside_focus_area -= self.size_x / 2
            self.move_focus_area()
    def save_grid_position(self):
        if self.saved_grid_position != []:
            self.ask_position_name = sd.askstring(parent = self.root, title = 'Position name', prompt = 'Give the name of the position:')
            if self.ask_position_name != None and self.ask_position_name != "":
                if (self.ask_position_name + '.txt') not in os.listdir(os.getcwd() + "/saved_positions"):
                    self.position_file = open(os.getcwd() + "/saved_positions/{}.txt".format(self.ask_position_name), "a+")
                    for cell in self.saved_grid_position:
                        self.position_file.write(str(cell[0]) + ',')
                    self.position_file.write('\n')
                    for cell in self.saved_grid_position:
                        self.position_file.write(str(cell[1]) + ',')
                    self.position_file.close()
                    self.saved_positions_values.append(self.ask_position_name)
                    self.saved_positions['values'] = self.saved_positions_values
                    self.ask_position_description = sd.askstring(parent = self.root, title = 'Position desription', prompt = 'Give the description of the position:')
                    self.position_description_file = open(os.getcwd() + "/saved_positions/{}_description.txt".format(self.ask_position_name), "w", encoding = "UTF-8")
                    if self.ask_position_description != None and self.ask_position_description != "":
                        self.position_description_file.write(self.ask_position_description)
                    else:
                        self.position_description_file.write("Η θέση δεν διαθέτει περιγραφή.\nThe position does not include description.")                        
                    self.position_description_file.close()
                else:
                    self.write_information_box('Warning', 'red', 'Το όνομα που πληκτρολόγησες χρησιμοποιείται ήδη για μια άλλη θέση! Επίλεξε διαφορετικό όνομα!\nThe name you typed is already being used by another position! Choose a different name!')
        else:
            self.write_information_box('Guide', 'orange', 'Αφού δημιουργήσεις μια διάταξη στο πλέγμα προσομοίωσης, κάνε δεξί κλικ στον χώρο αριστερά, ώστε να εμφανιστεί η θέση (μεγέθυνε αν είναι αναγκαίο) και στη συνέχεια πάτησε το "Save" (για να την αποθηκεύσεις).\nAfter creating a configuration in the simulation grid, right-click in the space on the left to display the position (zoom in if necessary) and then press "Save".')
    def write_information_box(self, note, note_color, message):
        self.text_pointer = self.information_box.index('end')
        self.information_box.insert('end', "\n********************************************\n{}: {}".format(note, message))
        self.information_box.tag_add('{}'.format(note), str(float(self.text_pointer) + 1.0), format(float(self.text_pointer) + 1.00 + float(len(note) / 100), ".2f"))
        self.information_box.tag_configure('{}'.format(note), foreground = note_color, font = 'Arial 10 bold italic')
        self.information_box.see('end')
    def recall_positions(self, event = None):
        if self.saved_positions.get() == "RANDOM":
            self.clear_grid()
            self.ask_percentage = sd.askinteger(parent = self.root, title = 'Random position', prompt = 'Give the percentage of the initial living cells on the grid (%):')
            self.ask_grid_part = sd.askinteger(parent = self.root, title = 'Random position', prompt = 'Give the dimension of the centre square grid where the random position will be appeared:')
            for i in range(int((self.rows - self.ask_grid_part) / 2), int((self.rows + self.ask_grid_part) / 2)):
                for j in range(int((self.columns - self.ask_grid_part) / 2), int((self.columns + self.ask_grid_part) / 2)):
                    self.random_number = r.random()
                    if self.random_number <= self.ask_percentage / 100:
                        self.grid_cells[i][j].button_pressed()
        else:
            self.set_chosen_position = 'on'
            self.chosen_position = []
            with open(os.getcwd() + "/saved_positions/{}.txt".format(self.saved_positions.get()), "r", encoding = "UTF-8") as file_position:
                for line in file_position:
                    self.chosen_position.append(line)
            self.chosen_position_xcors = self.chosen_position[0].split(',')[:-1]
            self.chosen_position_ycors = self.chosen_position[1].split(',')[:-1]
            self.chosen_position_description = (open(os.getcwd() + "/saved_positions/{}_description.txt".format(self.saved_positions.get()), "r", encoding = "UTF-8")).read()
            self.write_information_box('Position description of "{}"'.format(self.saved_positions.get()), 'blue', '\n' + self.chosen_position_description)
            self.write_information_box('Guide', 'orange', 'Τοποθέτησε την επιλεγμένη θέση όπου επιθυμείς μέσα στο πλέγμα και πάτησε το "Run" για να τρέξεις την προσοομοίωση.\nPlace the selected position wherever you wish within the grid and press "Run" to run the simulation.')
    def set_position_in_grid(self, chosen_cell_xcor, chosen_cell_ycor):
        if self.generations_string.get() == '0':
            self.set_chosen_position = 'off'
            self.control_recording = 'inside'
            self.x_move = int(self.chosen_position_xcors[0]) - chosen_cell_xcor
            self.y_move = int(self.chosen_position_ycors[0]) - chosen_cell_ycor
            for i in range(len(self.chosen_position_xcors)):
                self.chosen_position_xcors[i] = (int(self.chosen_position_xcors[i]) - self.x_move) % self.columns
                self.chosen_position_ycors[i] = (int(self.chosen_position_ycors[i]) - self.y_move) % self.rows
            try:
                for row in self.recording_history:
                    for cell in row:
                        cell[0] = cell[0] - self.x_move
                        cell[1] = cell[1] - self.y_move
            except:
                pass
            for i in range(len(self.chosen_position_xcors)):
                if self.grid_cells[self.chosen_position_xcors[i]][self.chosen_position_ycors[i]].control_press == 'unpressed':
                    self.grid_cells[self.chosen_position_xcors[i]][self.chosen_position_ycors[i]].button_pressed()
            if self.grid_reveal_mode_button['text'] == 'Auto':
                self.scan_grid(self.revealed_left_column, self.revealed_right_column, self.revealed_up_row, self.revealed_down_row)
        else:
            self.write_information_box('Guide', 'orange', 'Αν επιθυμείς να ξεκινήσεις μια καινούρια προσομοίωση τροποποιώντας την τρέχουσα θέση, πάτα πρώτα το "Reset" των πληροφοριών και στη συνέχεια προχώρησε σε αλλαγές στη διάταξη του πλέγματος. Τυχόν προσωρινώς αποθηκευμένα δεδομένα καταγραφής ή εξέλιξης προσομοίωσης θα διαγραφούν.\nIf you desire to start a new simulation by modifying the current position, first press the "Reset" button of the information menu and then proceed with changes to the grid layout. Any temporarily stored recording or simulation progress data will be deleted.')
    def recall_recordings(self, event = None):
        self.set_chosen_position = 'on'
        self.recording_pointer = 1
        self.reminder_pointer = self.recording_pointer
        self.chosen_recording = []
        with open(os.getcwd() + "/saved_recordings/{}.txt".format(self.saved_recordings.get()), "r", encoding = "UTF-8") as file_recording:
            for line in file_recording:
                self.chosen_recording_gen = line.split(',')[:-1]
                self.chosen_recording.append([])
                for i in range(int(len(self.chosen_recording_gen) / 2)):
                    self.chosen_recording[-1].append([int(self.chosen_recording_gen[2 * i]), int(self.chosen_recording_gen[2 * i + 1])])
        self.recording_history = self.chosen_recording[:-1]
        self.graf_history = []
        for item in self.chosen_recording[-1]:
            self.graf_history.append(item[0])
            self.graf_history.append(item[1])
        self.chosen_position_xcors = []
        self.chosen_position_ycors = []
        for cell in self.recording_history[0]:
            self.chosen_position_xcors.append(cell[0])
            self.chosen_position_ycors.append(cell[1])
        self.chosen_recording_description = (open(os.getcwd() + "/saved_recordings/{}_description.txt".format(self.saved_recordings.get()), "r", encoding = "UTF-8")).read()
        self.write_information_box('Recording description of "{}"'.format(self.saved_recordings.get()), 'blue', '\n' + self.chosen_recording_description)
        self.write_information_box('Guide', 'orange', 'Τοποθέτησε την πρώτη θέση της επιλεγμένης καταγραφής όπου επιθυμείς μέσα στο πλέγμα, και πάτησε το "forward" και το "play" για να τρέξεις την καταγραφή.\nPlace the first position of the selected recording wherever you wish within the grid, and press "forward" followed by "play" to run the recording.')
    def change_grid_reveal_mode(self):
        if self.grid_reveal_mode_button['text'] == 'Auto':
            self.grid_reveal_mode_button.configure(text = 'Manual')
        elif self.grid_reveal_mode_button['text'] == 'Manual':
            self.grid_reveal_mode_button.configure(text = 'Auto')
    def change_simulation_graf_mode(self):
        if self.simulation_graf_mode_button['text'] == 'Auto':
            self.simulation_graf_mode_button.configure(text = 'Manual')
        elif self.simulation_graf_mode_button['text'] == 'Manual':
            self.simulation_graf_mode_button.configure(text = 'Auto')
    def reset_cells_information(self):
        self.generations_string.set('0')
        self.birth_cells_string.set('0')
        self.first_cells_string.set('0')
        self.death_cells_string.set('0')
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid_cells[i][j].control_press == 'pressed':
                    self.first_cells_string.set(int(game_of_life.first_cells_string.get()) + 1)
        self.finally_cells_string.set(self.first_cells_string.get())
        self.recording_history = []
        self.graf_history = []
        self.reset_simulation_information()
    def reset_grid_position(self):
        self.saved_grid_position = []
        self.grid_situation_reveal.delete("all")
    def reset_simulation_progression(self):
        self.simulation_graf.delete("all")
        self.initial_gen_simulation_graf = 0
    def reset_simulation_information(self):    
        self.min_cells_string.set('-')
        self.times_min_string.set('-')
        self.max_cells_string.set('-')
        self.times_max_string.set('-')
        self.marked_gen_string.set('-')

class button():
    enter_button_state = 'highlight'
    continuous_paint_state = 'mark'
    canvas_offset = 3
    def __init__(self, grid_background, button_size, number, row, column):
        self.grid_background = grid_background
        self.row = row
        self.column = column
        self.number = number
        self.button_size = button_size
        self.button_width = 0
        self.choose_color = 0
        self.control_highlight = 0
        self.control_press = 'unpressed'
    def set_button_on_grid(self, row, column):
        self.button = self.grid_background.create_rectangle([column * self.button_size + button.canvas_offset, row * self.button_size + button.canvas_offset, (column + 1) * self.button_size + button.canvas_offset, (row + 1) * self.button_size + button.canvas_offset], fill = "#006fff", width = self.button_width, outline = "orange", tags = f"button_{self.number}_{self.row}_{self.column}")
        self.grid_background.tag_bind(f"button_{self.number}_{self.row}_{self.column}", "<Button-1>", self.button_pressed)
        self.grid_background.tag_bind(f"button_{self.number}_{self.row}_{self.column}", "<Button-2>", self.change_enter_button_mode)
        self.grid_background.tag_bind(f"button_{self.number}_{self.row}_{self.column}", "<Button-3>", self.change_continuous_paint_state)
        self.grid_background.tag_bind(f"button_{self.number}_{self.row}_{self.column}", "<Enter>", self.highlight_button_paint_continuously)
        self.grid_background.tag_bind(f"button_{self.number}_{self.row}_{self.column}", "<Leave>", self.unhighlight_button)
    def change_enter_button_mode(self, event):
        if button.enter_button_state == 'highlight':
            button.enter_button_state = 'paint'
        elif button.enter_button_state == 'paint':
            button.enter_button_state = 'highlight'
    def change_continuous_paint_state(self, event):
        if button.continuous_paint_state == 'mark':
            button.continuous_paint_state = 'erase'
        elif button.continuous_paint_state == 'erase':
            button.continuous_paint_state = 'mark'
    def button_pressed(self, event = None):
        try:
            if game_of_life.generations_string.get() != '0' and game_of_life.simulation_state == 'stop_simulation' and game_of_life.recording_play_stop_state == 'stop':
                game_of_life.write_information_box('Guide', 'orange', 'Αν επιθυμείς να ξεκινήσεις μια καινούρια προσομοίωση τροποποιώντας την τρέχουσα θέση, πάτα πρώτα το "Reset" των πληροφοριών και στη συνέχεια προχώρησε σε αλλαγές στη διάταξη του πλέγματος. Τυχόν προσωρινώς αποθηκευμένα δεδομένα καταγραφής ή εξέλιξης προσομοίωσης θα διαγραφούν.\nIf you desire to start a new simulation by modifying the current position, first press the "Reset" button of the information menu and then proceed with changes to the grid layout. Any temporarily stored recording or simulation progress data will be deleted.')
            else:
                if game_of_life.set_chosen_position == 'on':
                    game_of_life.set_position_in_grid(self.row, self.column)
                else:
                    if self.control_press == 'unpressed':
                        self.choose_color = 0
                        self.grid_background.itemconfigure(self.button, fill = game_of_life.colors_list[0])
                        self.control_highlight = 1
                        self.control_press = 'pressed'
                        if game_of_life.simulation_state == 'stop_simulation' and game_of_life.recording_play_stop_state == 'stop':
                            if game_of_life.grid_reveal_mode_button['text'] == 'Auto':
                                game_of_life.scan_grid(game_of_life.revealed_left_column, game_of_life.revealed_right_column, game_of_life.revealed_up_row, game_of_life.revealed_down_row)
                        if game_of_life.generations_string.get() == '0' and game_of_life.recording_play_stop_state == 'stop':
                            game_of_life.first_cells_string.set(int(game_of_life.first_cells_string.get()) + 1)
                            game_of_life.finally_cells_string.set(int(game_of_life.finally_cells_string.get()) + 1)
                        if game_of_life.recording_play_stop_state == 'play':
                            game_of_life.finally_cells_string.set(int(game_of_life.finally_cells_string.get()) + 1)
                            game_of_life.birth_cells_string.set(0)
                            game_of_life.death_cells_string.set(0)
                    elif self.control_press == 'pressed':
                        self.choose_color = 0
                        self.grid_background.itemconfigure(self.button, fill = game_of_life.colors_list[-1])
                        self.control_highlight = 0
                        self.control_press = 'unpressed'
                        if game_of_life.simulation_state == 'stop_simulation' and game_of_life.recording_play_stop_state == 'stop':
                            if game_of_life.grid_reveal_mode_button['text'] == 'Auto':
                                game_of_life.scan_grid(game_of_life.revealed_left_column, game_of_life.revealed_right_column, game_of_life.revealed_up_row, game_of_life.revealed_down_row)
                        if game_of_life.generations_string.get() == '0' and game_of_life.recording_play_stop_state == 'stop':
                            game_of_life.first_cells_string.set(int(game_of_life.first_cells_string.get()) - 1)
                            game_of_life.finally_cells_string.set(int(game_of_life.finally_cells_string.get()) - 1)
                        if game_of_life.recording_play_stop_state == 'play':
                            game_of_life.finally_cells_string.set(int(game_of_life.finally_cells_string.get()) - 1)
                            game_of_life.birth_cells_string.set(0)
                            game_of_life.death_cells_string.set(0)
        except:
            pass
    def highlight_button_paint_continuously(self, event):
        if button.enter_button_state == 'highlight':
            try:
                if game_of_life.set_chosen_position == 'on':
                    self.grid_background.itemconfigure(self.button, fill = "lime")
                else:
                    self.grid_background.itemconfigure(self.button, fill = "red")
            except:
                pass
        elif button.enter_button_state == 'paint':
            if button.continuous_paint_state == 'mark':
                if self.control_press == 'unpressed':
                    self.button_pressed()
                else:
                    pass
            elif button.continuous_paint_state == 'erase':
                if self.control_press == 'pressed':
                    self.button_pressed()
                else:
                    pass
    def unhighlight_button(self, event):
        try:
            if self.control_highlight == 0:
                self.grid_background.itemconfigure(self.button, fill = game_of_life.colors_list[-1])
            elif self.control_highlight == 1:
                self.grid_background.itemconfigure(self.button, fill = game_of_life.colors_list[self.choose_color])
        except:
            pass

root = tk.Tk()
game_of_life = game_of_life(root)             
root.mainloop()