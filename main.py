# Ezra Brauner's submission for Kargo's 2020 software engineering internship assessment

from sys import argv

def populate_freq_dict(str):
    freqDict = {}
    for char in str:
        if char not in freqDict:
            # if previously unencountered character found in str, add to freqDict
            freqDict[char] = 1
        else:
            freqDict[char] += 1
    return freqDict

def populate_freq_of_freq_array(dict):
    freqOfFreqArray = []
    maxFreq = 1

    # determine the necessary size for the array of frequencies' frequencies
    for freq in dict.values():
        if freq > maxFreq:
            maxFreq = freq

    for i in range(0, maxFreq):
        freqOfFreqArray.append(0)

    # populate array with number of times each frequency is found in input dictionary
    for j in dict.values():
        freqOfFreqArray[j - 1] += 1
    return freqOfFreqArray

def char_mapping_exists(s1, s2):
    # there cannot be a valid mapping unless the strings are of equal length
    if len(s1) != len(s2):
        print("false")
        return

    # populate a dictionary for each input string containing the frequencies of each character
    s1FreqDict = populate_freq_dict(s1)
    s2FreqDict = populate_freq_dict(s2)

    # if s1 has fewer distinct characters than s2,
    # then it will be impossible to map each character in s1 to a distinct character in s2
    if len(s1FreqDict.keys()) < len(s2FreqDict.keys()):
        print("false")
        return

    # populate an array for each string, with the integer at index i equal to the number of times
    # frequency (i - 1) is found in the string
    s1FreqOfFreq = populate_freq_of_freq_array(s1FreqDict)
    s2FreqOfFreq = populate_freq_of_freq_array(s2FreqDict)

    # ensure that each frequency of frequencies array contains the same number of values
    if len(s1FreqOfFreq) < len(s2FreqOfFreq):
        for i in range(0, len(s2FreqOfFreq) - len(s1FreqOfFreq)):
            s1FreqOfFreq.append(0)
    elif len(s2FreqOfFreq) < len(s1FreqOfFreq):
        for i in range(0, len(s1FreqOfFreq) - len(s2FreqOfFreq)):
            s2FreqOfFreq.append(0)

    # check that each set consisting of all instances of a single character in s1 can be mapped to a set in s2,
    # starting with the most frequent frequency
    for freq in range(len(s1FreqOfFreq) - 1, -1, -1):
        freq1 = s1FreqOfFreq[freq]
        freq2 = s2FreqOfFreq[freq]
        # if s1 has more groups of frequency i than s2,
        # then the members of that group must map to at least two distinct characters in s2
        if freq2 < freq1:
            print("false")
            return
        # if there are not enough sets of characters equal in length to the set in s2,
        # then sets of smaller lengths are mapped to the set in s2
        elif freq2 > freq1:
            numLettersS2 = s2FreqOfFreq[freq] * (freq + 1)
            i = freq + 1
            # frequencies are compared with the number of characters in s2 to combine them such that every character
            # in the set in s2 is mapped to one in s1
            while numLettersS2 > 0 and i >= 0:
                i -= 1
                if s1FreqOfFreq[i] == 0:
                    continue
                # find how many groups of frequencies (i + 1) can be mapped to the set in s2
                numLettersS1 = s1FreqOfFreq[i] * (i + 1)
                s1GroupsUsed = min(numLettersS2 // (i + 1), numLettersS1 // (i + 1))
                numLettersS2 -= s1GroupsUsed * (i + 1)
                # update the number of available sets of frequency (i + 1)
                s1FreqOfFreq[i] -= s1GroupsUsed
            # if numLettersS2 is negative, then smaller sets from s1 could not be combined evenly
            if numLettersS2 < 0:
                print("false")
                return
    print("true")

# check number of arguments
if len(argv) != 3:
    print("false")
    exit()

# declare string variables from command line, per https://docs.python.org/3/tutorial/stdlib.html#command-line-arguments
s1 = argv[1]
s2 = argv[2]

char_mapping_exists(s1, s2)