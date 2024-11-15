import pandas as pd

possible_words = []
grey_letters = []
yellow_letters = []
word = [0, 0, 0, 0, 0]

current_word = list("tales")
won = False
tries = 0

game_type = input("U for unlimited, N for normal wordle: ")
if(game_type == "N"):
    df =  df = pd.read_csv('/Users/nathanmills/Code/Personal/wordle/WORDS_converted.csv')
    possible_words = df["0"].tolist()
else:
    df = pd.read_csv('/Users/nathanmills/Code/Personal/wordle/sgb_words_converted.csv')
    possible_words = df["WORD"].tolist()

#First represents a, second b, thid c, etc
scores = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
def update_scores(list):
    global scores
    scores = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for w in list:
        for letter in set(w):
            scores[ord(letter)-97] += 1

def get_score(word):
    s=0 
    used_letters = set()
    for l in word:
        if l not in used_letters:
            s += scores[ord(l)-97]
            used_letters.add(l)
        else:
            s += scores[ord(l)-97]/2
    return s

while((not won) and (tries < 6)):
    print("Guess:", ''.join(current_word))

    #Have the user input the color for each letter
    L_1 = input("First letter color: ")
    L_2 = input("Second letter color: ")
    L_3 = input("Third letter color: ")
    L_4 = input("Fourth letter color: ")
    L_5 = input("Fifth letter color: ")
    correctness = [L_1, L_2, L_3, L_4, L_5]

    if (correctness == ["g", "g", "g", "g", "g"]):
        won = True
        break

    #sorts the letters from the last word into the green yellow or grey lists
    #these needs to be seperate loops because of how I am deleting old letters from their lists
        #this is imortant for a word with a repete letter that are two different colors 
    for i in range(5):
        if (correctness[i] == "g"):
            word[i]=current_word[i]
            #removes a letter from list of yellow letters upon being found as green
            for n in range(5):
                if [word[i], n] in yellow_letters:
                    yellow_letters.remove([word[i], n])
    for i in range(5):
        if correctness[i] == "b":
            grey_letters.append(current_word[i])
    for i in range(5):
        if (correctness[i] == "y"):
            yellow_letters.append([current_word[i],i])
            #removes a letter from list of grey letters upon being found as yellow
            #super not great code here but it works cause there's no 5 letter word thats all the same letter
                #And if there was then it would just have gotten it right
            if current_word[i] in grey_letters:
                grey_letters.remove(current_word[i])
            if current_word[i] in grey_letters:
                grey_letters.remove(current_word[i])
            if current_word[i] in grey_letters:
                grey_letters.remove(current_word[i])

    #Loops through all possible words and figures out which ones are still possible 
    # given the current green, yellow, and grey letter lists
    new_possible_words = []
    for w in possible_words:
    # TODO make this not three nested for loops lol; make it better
        not_possible = False

        for l in range(5):
            #Checks to make sure that all the letters in the word are in line with the known green letters
            if ((word[l] != 0) and w[l] != word[l]):
                not_possible = True
            #Checks to see if the letter is a known yellow letter in its impossible spot
            for i in yellow_letters:
                if (w[l] == i[0] and i[1] == l):
                    not_possible = True
            #Checks to see if the letter is any of the known grey letters
            for g in grey_letters:
                if (w[l] == g):
                    #makes sure that the grey letter isn't actually green
                    if (w[l] != word[l]):
                        not_possible = True

        #Makes sure that every yellow letter is used somewhere in the word
        for y in yellow_letters:
            has_yellow_letter = False
            for l in range(5):
                if (y[0] == w[l]):
                    has_yellow_letter = True
            if(has_yellow_letter == False):
                not_possible = True

        #If the word is possible adds it to a list which will then replace possible_words
        if (not_possible == False):
            new_possible_words.append(w)

    possible_words = new_possible_words

    update_scores(possible_words)

    top_score = 0
    best_word = ""
    for w in possible_words:
        if get_score(w)>top_score:
            top_score = get_score(w)
            best_word = w

    if (len(possible_words) > 0):
        current_word = list(best_word)
        if(len(possible_words) == 1):
            print("I think this is it!")
    else:
        print("Either you imputed something wrong, or the word isn't one that I have been given")
        tries = 8
    tries = tries + 1


if (tries > 5):
    print("You Lost!")
elif (won == True):
    print("You Won!")