import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from update import DatabaseUpdate

class Transpose:
    
    def __init__(self):
    
        self.Music_Pitch_System = pd.read_excel(r'C:\Users\wesle\Desktop\2020\Code\main\Easy Transpose\easy-transpose-master\datasets\music notes dataset.xlsx')
        
        self.instruments_IntervalPairs_pitchwise = {
        'Double Bass': [-12,12],
        'Guitar': [-12,12],
        'Piccolo': [12,-12],
        'Flute in C': [12,-12],
        'Alto Flute': [-5,5],
        'English Horn': [-7,7],
        'Bb Clarinet': [-2,2],
        'Eb Clarinet': [-9,9],
        'A Clarinet': [-3, 3],
        'Bb Bass Clarinet': [-14,14],
        'Contrabassoon': [-12,12],
        'Bb Soprano Saxophone': [-2,2],
        'Eb Alto Saxophone': [-9,9],
        'Bb Tenor Saxophone': [-14,14],
        'Eb Baritone Saxophone': [-21,21],
        'French Horn': [-7,7],
        'Bb Trumpet': [-2,2],
        'Glockenspiel': [24,-24],
        'Xylophone': [12,-12],
        'Celesta': [12, -12]}
        
        self.instruments_IntervalPairs_stepwise = {
        'Double Bass': [-7,7],
        'Guitar': [-7,7],
        'Piccolo': [7,-7],
        'Flute in C' : [7,-7],
        'Alto Flute': [-3,3],
        'English Horn': [-4,4],
        'Bb Clarinet': [-1,1],
        'Eb Clarinet': [-5,5],
        'A Clarinet': [-2, 2],
        'Bb Bass Clarinet': [-7,7],
        'Contrabassoon': [-7,7],
        'Bb Soprano Saxophone': [-1,1],
        'Eb Alto Saxophone': [-5,5],
        'Bb Tenor Saxophone': [-7,7],
        'Eb Baritone Saxophone': [-12,12],
        'French Horn': [-4,4],
        'Bb Trumpet': [-1,1],
        'Glockenspiel': [14,-14],
        'Xylophone': [7,-7],
        'Celesta': [7,-7]}

        self.database_connect = True    
        self.all_notes = None 
    
    
    
    def instrument_transposition_intervals(self, user_instrument):
        
        """ 
        Instrument name taken as string input
        Fetches transposition intervals for specefied instrument
        Returns two interval pairs (0 = Pitchwise, 1 = Stepwise)
        Needs more instruments in database
        """ 
        
        #Transposition Intervals
        #(0)Written -> Concert Pitch
        #(1)Concert Pitch -> Written
        instrument_pair_pitchwise = self.instruments_IntervalPairs_pitchwise[user_instrument]
        instrument_pair_stepwise = self.instruments_IntervalPairs_stepwise[user_instrument]

        return instrument_pair_pitchwise, instrument_pair_stepwise
    
    
    

    def starting_direction(self, user_direction):
        """
        Takes string as input (Written/Concert Pitch)
        Returns 0 if starting with written, 1 if starting with concert
        Overall this 0 or 1 is used to represent whether a user is starting with written or concert pitch
        """
        if user_direction == "Written":
            direction = 0
        elif user_direction == "Concert":
            direction = 1
        return direction

        
     

    def calculate_ground_truth_pitch(self, user_pitch):
        
        """
        Takes string as input, which is the user starting pitch. ex C#2, Dbb7, E#6
        This code transforms user starting pitch string, 
        into an array of all the possible note names for that specific pitch.
        This also creates a ground truth pitch integer for the user start pitch (row number in Music Pitch System)
        This ground truth pitch integer will be used in transposition calculation.
        """
     
        # Calculate user pitch ID
        #user_pitch_ID = (pitchClassFlats.index(userStartPitch))
        user_pitch_full = np.column_stack([self.Music_Pitch_System[col].str.contains(user_pitch, na=False) for col in self.Music_Pitch_System])

        # Fetch ground_truth list
        user_pitch_list = self.Music_Pitch_System.loc[user_pitch_full.any(axis=1)]

        # Fetch ground_truth_pitch_ID (Number ID used for caclulations)
        pitch_index_string = str(user_pitch_list.index)
        step_1 = pitch_index_string.replace("Int64Index([","")
        step_2 = step_1.replace("], dtype='int64')","")

        ground_truth_pitch_ID = int(step_2)

        return user_pitch_list, ground_truth_pitch_ID
      
        
    # Takes user start pitch as input (string),
    # Returns step_note (A,B,C,D,E,F,G 1-10) and step_ID (used for stepwise transposition calculation)

    def initial_step(self, user_pitch):
        
        steps = ['C0','D0','E0','F0','G0','A0','B0',
           'C1','D1','E1','F1','G1','A1','B1',
           'C2','D2','E2','F2','G2','A2','B2',
           'C3','D3','E3','F3','G3','A3','B3',
           'C4','D4','E4','F4','G4','A4','B4',
           'C5','D5','E5','F5','G5','A5','B5',
           'C6','D6','E6','F6','G6','A6','B6',
           'C7','D7','E7','F7','G7','A7','B7',
           'C8','D8','E8','F8','G8','A8','B8',
           'C9','D9','E9','F9','G9','A9','B9',
           'C10','D10','E10','F10','G10','A10','B10',
           'C11','D11','E11','F11','G11','A11','B11',
           'C12','D11','E12','F12','G12','A12','B12']
        
        if ("b") in user_pitch:
            step_note = user_pitch.replace("b","")
        elif ("bb") in user_pitch:
            step_note = user_pitch.replace("bb","")
        elif ("#") in user_pitch:
            step_note = user_pitch.replace("#","")
        elif ("X") in user_pitch:
            step_note = user_pitch.replace("X","")
        else:
            step_note = user_pitch
            
        step_ID = steps.index(step_note)

        return step_note, step_ID
        
        
    # Takes as inputs:
    # (1) ground truth pitch ID (integer). This is the transformed version of users original starting pitch
    # (2) user instrument (String)
    # (3) user starting direction (0 = Written, 1 = Concert)

    # Returns ground truth pitch ID of transposed note!

    def transpose_pitchwise(self, ground_truth_pitch_ID, userInstrument,user_direction):

        intervals = self.instrument_transposition_intervals(userInstrument)

        #print(intervals[0])

        pitchwise_interval = intervals[0]
        #print(pitchwise_interval[0])

        # Written
        if user_direction == 0:
            x = int(pitchwise_interval[0])

        # Concert
        if user_direction == 1:
            x = int(pitchwise_interval[1])

        transposed_pitch_ID = ground_truth_pitch_ID + x

        return transposed_pitch_ID
   
    # Transpose Stepwise

    # Takes as inputs:
    # (1) ground truth pitch ID (integer). This is the transformed version of users original starting pitch
    # (2) user instrument (String)
    # (3) user starting direction (0 = Written, 1 = Concert)

    # Returns ground truth step ID of transposed note!

    def transpose_stepwise(self, ground_truth_pitch_ID, user_instrument,user_direction):

        intervals = self.instrument_transposition_intervals(user_instrument)

        pitchwise_interval = intervals[1]
        # Written
        if user_direction == 0:
            transposed_step_ID = (ground_truth_pitch_ID + pitchwise_interval[0])

        # Concert
        if user_direction == 1:
            transposed_step_ID = (ground_truth_pitch_ID + pitchwise_interval[1])

        return transposed_step_ID
        
        
    # Return name of transposed note, given step_name

    def FinalNote(self, ground_truth_final_pitch_int,step_name):
        
        # Search Music Pitch System to fetch array of possible pitch names
        user_pitch_full = self.Music_Pitch_System.query(str(ground_truth_final_pitch_int))

        note_0 = str(self.Music_Pitch_System.iloc[ground_truth_final_pitch_int, 0])
        note_1 = str(self.Music_Pitch_System.iloc[ground_truth_final_pitch_int, 1])
        note_2 = str(self.Music_Pitch_System.iloc[ground_truth_final_pitch_int, 2])
        note_3 = str(self.Music_Pitch_System.iloc[ground_truth_final_pitch_int, 3])
        note_4 = str(self.Music_Pitch_System.iloc[ground_truth_final_pitch_int, 4])
        note_5 = str(self.Music_Pitch_System.iloc[ground_truth_final_pitch_int, 5])

        notes = [note_0,note_1,note_2,note_3,note_4,note_5]
        #print(notes)
        itr = 0
        for i in notes:
        
            if ("b") in i:
                i = i.replace("b","")
            if ("bb") in i:
                i = i.replace("bb","")
            if ("#") in i:
                i = i.replace("#","")
            if ("X") in i:
                i = i.replace("X","")
            true_false = i == step_name
            if true_false == True:
                final = (notes[itr])
                break
            else:
                itr = itr+1

            # see if note_iter shares characters with step_name
            # look at each value in note_iter and decide whether it is similar to step_name

        return final

    def transpose(self, user_instrument,user_pitch,user_direction):
        
        # this is the master function, which utilizes all methods above to transpose a given query     
        # Fetch transposition intervals for instrument (pitchwise, stepwise)
        self.instrument_pair_pitchwise, self.instrument_pair_stepwise = self.instrument_transposition_intervals(user_instrument)
        #print("- Pitchwise Interval Pair: ",instrument_pair_pitchwise,"\n"+"- Stepwise Interval Pair: ", instrument_pair_stepwise)

        # Start direction (0 = written, 1 = concert)
        direction = self.starting_direction(user_direction)
        #print("- Starting direction: ",direction,"(0 = written, 1 = concert)")

        # Fetch ground_truth_list & ground_truth_pitch_ID
        ground_truth_list, ground_truth_pitch_ID = self.calculate_ground_truth_pitch(user_pitch)
        #print("- Ground Truth Pitch List: ","\n")
        #print(ground_truth_list)
        #print("\n")

        # Fetch Pitch ID
        #print("Ground Truth Pitch ID:",ground_truth_pitch_ID) 

        # Fetch user_start_pitch Step
        step_note, step_ID = self.initial_step(user_pitch)
        #print("Ground Truth Step ID: ",step_note, step_ID)
        #print("Direction:",direction,"(0 = written, 1 = concert)")

        # Pitchwise Transposition, Return ground_truth_list for new, transposed pitch
        transposed_pitch_ID = self.transpose_pitchwise(ground_truth_pitch_ID, user_instrument,direction)
    #print("Transposed Pitch ID: ",transposed_pitch_ID)
    
        # Calculate Transposed Step ID 
        transposed_step_ID = self.transpose_stepwise(step_ID, user_instrument,direction)
        #print("Transposed Step ID: ",transposed_step_ID,)
        
        steps = ['C0','D0','E0','F0','G0','A0','B0',
           'C1','D1','E1','F1','G1','A1','B1',
           'C2','D2','E2','F2','G2','A2','B2',
           'C3','D3','E3','F3','G3','A3','B3',
           'C4','D4','E4','F4','G4','A4','B4',
           'C5','D5','E5','F5','G5','A5','B5',
           'C6','D6','E6','F6','G6','A6','B6',
           'C7','D7','E7','F7','G7','A7','B7',
           'C8','D8','E8','F8','G8','A8','B8',
           'C9','D9','E9','F9','G9','A9','B9',
           'C10','D10','E10','F10','G10','A10','B10',
           'C11','D11','E11','F11','G11','A11','B11',
           'C12','D11','E12','F12','G12','A12','B12']
        
        # Use Transposed Step to select proper note. Identify the note in the list that matches the step note
        step_name = steps[transposed_step_ID]

        #print("Step name:",step_name)

        # Remove numbers from Step

         # Use official_Step to search groundtruth list
        Final_Note = self.FinalNote(transposed_pitch_ID,step_name) 

        # This is your final note!
        # Print on screen using notation
        # Print with MIDI
        
        # update MySQL database 
        if self.database_connect == True:
            db = DatabaseUpdate()
            db.transpose_table(user_pitch, Final_Note, user_direction, user_instrument)     
        # if no database connection, pass
        else:
            pass
        
        return Final_Note
