#!/usr/bin/env python3
#
# Generate C source files for wavetables
#

def saw(omega, highestFreq):
    # FIXME: Band limit to highestFreq at 48 kHz
    return omega

def note2hz(note):
    # Get frequency of MIDI note number (note 69 is middle A @ 440 Hz)
    return 2**((note - 69) / 12) * 440

def make_tables(function, firstNote, notesPerTable, tableCount, tableLength):
    output = "{\n"
    for tableNum in range(tableCount):
        highestFreq = note2hz(firstNote + (tableNum + 1) * notesPerTable)
        data = list(map(lambda s: function(s/tableLength, 1), range(tableLength)))

        output += "    { // notes %d - %d, up to %.2f Hz" % (firstNote + tableNum * notesPerTable,
                                                             firstNote + (tableNum+1) * notesPerTable - 1,
                                                             highestFreq)
        for i in range(len(data)):
            if not i % 8:
                output += "\n        "
            output += "%.06f, " % data[i]
            
        output += "\n    },\n"

    output += "}"
    return output            

if __name__ == "__main__":
    t = make_tables(saw, 8, 12, 10, 16)
    print("""/*
 * Saw wavetable generated by make_wavetable.py
 */
""")
    print("#define WT_TABLES 12")
    print("#define WT_LENGTH 16")
    print("#define WT_FIRST_NOTE 8")
    print("#define WT_NOTES_PER_TABLE 8")
    print("static const float wtSaw[WT_TABLES][WT_LENGTH] = %s;\n" % t)

