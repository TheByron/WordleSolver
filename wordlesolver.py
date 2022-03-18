### Author: Byron Himes
### Date Started: March 17, 2022
### Notes:  No explicit optimization has been performed,
###         this is just the "see if it works" version.
### Issues off the top of my head:
### 1. Sorting suggestions by word frequency needed (e.g. "dogies" should
###     not be suggested before "movies")
### 2. I haven't done any extensive testing or looked for edge cases

# TODO: add more/better documentation
# TODO: reformat code to < 80 chars per line
# TODO: use english corpus word frequencies to make more common words suggested first

def wordscore(word):
    return sum([freq[c] for c in word])


# COMPILE DICT OF LETTER FREQUENCIES
freqfile = open("freq.txt", "r").read().splitlines(keepends=False)
freq = dict()
for line in freqfile:
    line = line.split()
    freq[line[0].lower()] = float(line[1]) / 100

# COMPILE DICT OF WORD FREQUENCIES (does not include all words at this time, sadly)
# TODO: uncomment this section when I get around to it
# wordfreqfile = open("wordfreqs.txt", "r").read().splitlines(keepends=False)
# wordfreq = dict()
# for line in wordfreqfile:
#     line = line.split()
#     wordfreq[line[0].lower()] = int(line[1])

# GET STARTING INFORMATION
wordsraw = open("words.txt", "r").read().splitlines(keepends=False)
length = int(input("How long is the word?\n").strip())
repeats = -1
while repeats not in ("0", "1"):
    repeats = input("Are repeats allowed?\n0 = no, 1 = yes\n").strip()
repeats = bool(int(repeats))

# COMPILE LIST OF USABLE WORDS
words = list()
if not repeats:
    words = [w for w in filter(lambda x: len(set(x)) == len(x) and len(set(x)) == length, wordsraw)]
else:
    words = [w for w in filter(lambda x: len(x) == length, wordsraw)]

# SORT BASED ON SCORE AND DIVERSITY
# TODO: delete bottom version, uncomment top version when word frequencies implemented
# words.sort(key=lambda x: (len(set(x)), wordscore(x), wordfreq[x]), reverse=True)
words.sort(key=lambda x: (len(set(x)), wordscore(x)), reverse=True)

# START ATTEMPTS CYCLE
answer = ["" for x in range(length)]
scored = 0  # number of characters correctly guessed
tries = 0  # starts at 1 because start word already used
guess = ""
invalid = "n"
rightspot = "r"
wrongspot = "w"
wrongspots = list()
while scored < length and tries < 6:
    checkoutcomes = False  # used when repeats allowed and multiple letters exist in guess
    if guess != "" and guess in words:
        words.remove(guess)

    if len(words) == 1:
        print("The word is", words[0])
        answer = list(words[0])
        break

    # SHOW SUGGESTIONS
    more = ""
    istart = 0
    while more != "0":
        limit = min(istart + 3, len(words))
        print("SUGGESTIONS:", *[words[i] for i in range(istart, limit)])
        more = input("Display more suggestions? 0 = no, anything else = yes\n").strip()
        istart = limit - 1

    # TAKE INPUT FOR GUESS
    guess = ""
    while guess not in words:
        guess = input("GUESSES REMAINING: " + str(6 - tries) +
                      "\nType chosen word (doesn't have to be from list).\n").strip().lower()

    outcomes = list()  # to track feedback for letters when repeats allowed

    # EXAMINE FEEDBACK FOR EACH LETTER OF CURRENT GUESSWORD
    for i in range(0, length):
        if answer[i] != "":
            continue
        print("\nFeedback for letter:", guess[i].upper(), "in position", i + 1)
        feedback = ""
        while feedback not in (invalid, rightspot, wrongspot):
            feedback = input("N: Not used.\n"
                             "R: Right spot.\n"
                             "W: Used, but wrong spot.\n").strip().lower()
        if feedback == rightspot:
            answer[i] = guess[i]
            words = [w for w in filter(lambda x: x[i] == guess[i], words)]
            scored += 1
            if guess[i] in wrongspots:
                wrongspots.remove(guess[i])

        elif feedback == wrongspot:
            words = [w for w in filter(lambda x: guess[i] in x and x[i] != guess[i], words)]
            wrongspots.append(guess[i])
            outcomes.append((guess[i], wrongspot))

        elif feedback == invalid:
            if guess.count(guess[i]) == 1:
                # as long as no repeats allowed, remove all words with that letter
                words = [w for w in filter(lambda x: guess[i] not in x, words)]
            else:
                checkoutcomes = True
                outcomes.append((guess[i], invalid))
                words = [w for w in filter(lambda x: x[i] != guess[i], words)]
    if checkoutcomes:
        for letter in set(guess):
            if letter in [outcome[0] for outcome in outcomes]:
                candelete = (letter not in answer)
                for outcome in [x for x in outcomes if x[0] == letter]:
                    if outcome[1] != invalid:
                        candelete = False
                if candelete:
                    words = [w for w in filter(lambda x: guess[i] not in x, words)]
    tries += 1

print("Tries:", tries, "\tword:", ''.join(answer).upper())
