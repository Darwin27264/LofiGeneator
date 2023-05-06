# Python library for understanding music
from music21 import *
from collections import Counter

# Using numpy for array processing
import os
import numpy as np
# For visualizing the data
import matplotlib.pyplot as plt

#defining function to read MIDI files
def read_midi(file):
    
    print("Loading Music File:",file)
    
    notes=[]
    notes_to_parse = None
    
    #parsing a midi file
    midi = converter.parse(file)
  
    #grouping based on different instruments
    s2 = instrument.partitionByInstrument(midi)

    #Looping over all the instruments
    for part in s2.parts:
    
        #select elements of only piano
        if 'Piano' in str(part): 
        
            notes_to_parse = part.recurse() 
      
            #finding whether a particular element is note or a chord
            for element in notes_to_parse:
                
                #note
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                
                #chord
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))

    return np.array(notes)


def show_data_info():
    #converting 2D array into 1D array
    notes_ = [element for note_ in notes_array for element in note_]

    #No. of unique notes
    unique_notes = list(set(notes_))
    print(len(unique_notes))
    
    #computing frequency of each note
    freq = dict(Counter(notes_))

    #consider only the frequencies
    no=[count for _,count in freq.items()]

    #set the figure size
    plt.figure(figsize=(5,5))

    #plot
    plt.hist(no)


#specify the path
path = '/Users/dstu/Library/CloudStorage/OneDrive-Personal/MacOS/Code'

#read all the filenames
files = [i for i in os.listdir(path) if i.endswith(".mid")]

#reading each midi file
notes_array = np.array([read_midi(path+i) for i in files])