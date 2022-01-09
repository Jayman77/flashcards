import random  # Library used to create a shuffled deck
import tkinter as tk  # tkinter package used for GUI
import PIL.ImageTk as itk  # PIL used for ImageTk for PhotoImage to get images
from tkinter import simpledialog  # Used for dialog input from menu in addCard()
from tkinter import messagebox  # Used for dialog output


class Card:
    # 3 instance variables
    key = ""  # String for key
    definition = ""  # String for definition
    isKeyVis = True  # Boolean to determine which text is visible

    def __init__(self, k, d, iKV):  # Initialization of variables when Card object is created
        self.key = k  # Sets all instance variables to 3 input parameters
        self.definition = d
        self.isKeyVis = iKV

    def returnText(self):  # returns the primary text based on isKeyVis variable
        if self.isKeyVis:  # if key is the visible string...
            return self.key  # returns the key string
        else:  # if key is not the visible string...
            return self.definition  # returns the definition string


isShuffled = False
isKeyAnswer = True
cards = []  # initialization of list of Card objects, appended to in initCards()
orderedCards = []  # list of Card objects in order
shuffledCards = []  # list of shuffled Card objects, shuffled in initCards()
visIndex = 0  # index of visible card
myFont = 'Verdana'  # font used throughout GUI for visible text
isWorking = False  # boolean used for 'edit' checkbutton


def initCards():
    global orderedCards
    choice = int(input('Would you like to import a set of keys and definitions?\n1: Yes\n2: No\n'))
    if choice == 1:
        print('\nFormatting:\nKey and definition should be delimited by a semicolon(;) \nEach key and definition '
              'combo should be on a new line.\nInsert the data into the file named flashData.txt\n')
        input("Press any key to continue...")  # Waits for user input before getting input from file
        inputFile = open('flashData.txt', 'r')  # open(filename, mode) -> mode 'r' == read -> opens file to read
        if inputFile.mode == 'r':  # if file is in 'read' mode...
            data = inputFile.readlines()  # creates list 'data' from all the lines in inputFile
            for x in data:  # loops through data[], x represent each line
                keyDef = x.split(';', 1)  # splits at semicolon 1 time, guarantees a size-2 keyDef[] list
                cards.append(Card(keyDef[0], keyDef[1], True))  # appends Card object made from data, default iKV val
        inputFile.close()
    else:
        i = int(input("How many cards do you want to add?\t"))  # Gets input for number of key/def combos to add to list
        for x in range(1, i + 1):  # loops through 'i' times, 1(inclus) to i+1(exclus)
            tempKey = input(str(x) + '.\tKey:\t')  # Gets input for Key, then Def.
            tempDef = input("\tDef:\t")
            cards.append(Card(tempKey, tempDef, True))  # appends Card object made from data, default iKV val
    orderedCards = cards
    count = len(cards) - 1
    while count >= 0:  # loop to create shuffled deck
        tempIndex = random.randint(0, count)  # random number generated to represent index
        shuffledCards.append(cards[tempIndex])  # adds card at random index to shuffled list
        count -= 1  # decreases count by 1 to avoid infinite loop


initCards()  # get all Cards initialized before GUI
root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=550)
canvas.pack()

# menu for GUI
menuBar = tk.Menu(root)
oMenu = tk.Menu(menuBar, tearoff=0)
helpMenu = tk.Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Options', menu=oMenu)
oMenu.add_command(label='Add Card', command=lambda: addCard())
oMenu.add_command(label='Delete Card', command=lambda: deleteCard())
oMenu.add_command(label='Edit Card', command=lambda: editCard())
oMenu.add_checkbutton(label='Shuffle', onvalue=1, offvalue=0, variable=isShuffled, command=lambda: shuffleToggle())
oMenu.add_checkbutton(label='Answer with Key', onvalue=1, offvalue=0, variable=isKeyAnswer, command=lambda: keyToggle())
oMenu.add_separator()
oMenu.add_command(label='Save', command=lambda: saveToFile())
oMenu.add_command(label='Exit', command=lambda: end())
root.bind('<Escape>', lambda x: end())
menuBar.add_cascade(label='Help', menu=helpMenu)
helpMenu.add_command(label='Help', command=lambda: helpMsg())
helpMenu.add_command(label='About', command=lambda: aboutMsg())

# creation of PhotoImage objects from 'png' files in C:\Users\jayjs\PycharmProjects\flashcards
firstCard = itk.PhotoImage(file='firstcardGUI.png')
midCard = itk.PhotoImage(file='cardGUI.png')
lastCard = itk.PhotoImage(file='lastcardGUI.png')
nextCard = itk.PhotoImage(file='nextCard.png')
prevCard = itk.PhotoImage(file='prevCard.png')
flipCard = itk.PhotoImage(file='flipCard.png')
editCard = itk.PhotoImage(file='editCard.png')

# StringVars for nonstatic text in Labels in GUI
vStr = tk.StringVar(root)  # StringVar for visible string on flashcard
vStr.set(cards[0].returnText())  # Initialized to the text of the first card
indStr = tk.StringVar(root)  # StringVar for the number of the card shown
indStr.set(str(visIndex + 1) + ' / ' + str(len(cards)))  # index + 1(starts at 0 + 1) out of total number

nC = tk.Button(text='', image=nextCard, command=lambda: buttonPressed('next'))  # button to advance to next card
nC_window = canvas.create_window(750, 520, window=nC)  # window of button added to canvas
nC_id = canvas.create_window(750, 520, window=nC)  # id created to toggle state (hide/vis)
root.bind('<Right>', lambda x: buttonPressed('next'))  # bound button to right arrow key

pC = tk.Button(text='', image=prevCard, command=lambda: buttonPressed('prev'))  # button to go back to previous card
pC_window = canvas.create_window(50, 520, window=pC)  # window of button added to canvas
pC_id = canvas.create_window(50, 520, window=pC)  # id created to toggle state (hide/vis)
canvas.itemconfigure(pC_id, state='hidden')  # default state is hidden in canvas
root.bind('<Left>', lambda x: buttonPressed('prev'))  # button bounded to left arrow key

fC = tk.Button(text='', image=flipCard, command=lambda: buttonPressed('flip'))  # button to flip card (swap key and def)
fC_window = canvas.create_window(400, 520, window=fC)  # window of button added to canvas
fC_id = canvas.create_window(400, 520, window=fC)  # id created to toggle state (hide/vis)
root.bind('<Down>', lambda x: buttonPressed('flip'))  # button bounded to down arrow key
root.bind('<Up>', lambda x: buttonPressed('flip'))  # button bounded to up arrow key
root.bind('<space>', lambda x: buttonPressed('flip'))  # button bounded to down arrow key

ind = tk.Label(textvariable=indStr, anchor='c', font=myFont, bg='white')  # Label of the index that user is on
ind.place(x=370, y=20)  # Label placed at given x,y value

txt = tk.Label(width=50, height=15, textvariable=vStr, anchor='c', font=myFont)  # Label of text on card
txt.place(x=140, y=140)  # Label placed at given x,y value
txt.bind('<Button-1>', lambda x: buttonPressed('flip'))     # When button pressed on label, flips card


def addCard():
    global orderedCards
    global cards
    global shuffledCards
    keyDef = simpledialog.askstring(title="Add Card", prompt="Insert key and definition, separated by a semicolon(;)")
    if ";" in keyDef:
        kD = keyDef.split(';', 1)
        c = Card(kD[0], kD[1], True)
        orderedCards.insert(len(cards), c)
        index = random.randint(0, len(cards) - 1)
        shuffledCards.insert(index, c)
        if isShuffled:
            cards = shuffledCards
        else:
            cards = orderedCards
        indStr.set(str(visIndex + 1) + ' / ' + str(len(cards)))


def deleteCard():
    global orderedCards
    global cards
    global shuffledCards
    global visIndex
    cards.remove(cards[visIndex])
    if isShuffled:
        shuffledCards = cards
    else:
        orderedCards = cards
    if visIndex != 0:
        visIndex -= 1
    else:
        visIndex += 1
    vStr.set(cards[visIndex].returnText())
    indStr.set(str(visIndex + 1) + ' / ' + str(len(cards)))


def editCard():
    global orderedCards
    global cards
    global shuffledCards
    newStr = simpledialog.askstring(title='Edit Card', prompt="What would you like to change the current value to?")
    if newStr is None or newStr == '':  # If user presses 'Cancel' instead of 'Ok' or enters no value...
        newStr = vStr.get()             # Keeps original value
    if cards[visIndex].isKeyVis:  # if key is visible... sets key value to string in Entry
        cards[visIndex].key = newStr
    else:  # if key isn't visible... sets def value to string in Entry
        cards[visIndex].definition = newStr
    vStr.set(newStr)



def shuffleToggle():
    global isShuffled
    global cards
    global orderedCards
    isShuffled = not isShuffled
    if isShuffled:
        cards = shuffledCards
    else:
        cards = orderedCards
    vStr.set(cards[visIndex].returnText())


def keyToggle():
    global isKeyAnswer
    global cards
    global orderedCards
    global shuffledCards
    isKeyAnswer = not isKeyAnswer
    for x in cards:
        x.isKeyVis = not x.isKeyVis
    if isShuffled:
        shuffledCards = cards
    else:
        orderedCards = cards
    vStr.set(cards[visIndex].returnText())


def saveToFile():
    inputFile = open('flashData.txt', 'w')  # opens file in write-only mode ('w'), clears its contents
    for x in orderedCards:
        inputFile.writelines(x.key + ';' + x.definition)
    inputFile.close()


def end():
    confirm = messagebox.askyesno("Quit Program", "Are you sure?")
    if confirm:
        root.destroy()


def helpMsg():
    messagebox.showinfo("Help", "Press the right arrow button or the right key to advanced to the next card.\nPress "
                                "the left arrow button or the left key to go to previous card.\nPress the flip button "
                                "or the spacebar, up, or down key to see the opposite side.\nTo edit card, "
                                "go to Options->Edit Card and enter, type in a new value, and press 'OK'.\nTo add "
                                "card, go to Options-> Add Card and enter the key and definition, separated by a "
                                "semicolon.\n To save any changes made to cards to the dataFile, go to Options-> Save "
                                "Changes.\nTo close the flashcard tool, go to Options->Exit or press Escape.")


def aboutMsg():
    messagebox.showinfo("About", "Flashcard Tool\nJay Upadhyaya")


def cardChange():  # Method to change what is shown on card
    indStr.set(str(visIndex + 1) + ' / ' + str(len(cards)))  # changes indStr to new index value
    vStr.set(cards[visIndex].returnText())  # sets vStr to the visible text of Card at index value


def buttonPressed(button):  # Method for when button is pressed
    global visIndex  # Globalizes variable to get value outside method
    if 0 <= visIndex <= len(cards):  # if index val is between range 0 and len of cards..
        if button == 'next' and visIndex < len(cards) - 1:  # if next and in range (won't go past last card)...
            visIndex += 1  # increases index by 1
        elif button == 'next':  # if next and not in range...
            visIndex = 0  # cycles forward to first card (at index 0)
        elif button == 'prev' and visIndex > 0:  # if prev and in range (won't go behind 1st card)...
            visIndex -= 1  # decreases index by 1
        elif button == 'prev':  # if prev and not in range...
            visIndex = len(cards) - 1  # cycles back to last card
        elif button == 'flip':  # if card is flipped...
            cards[visIndex].isKeyVis = not cards[visIndex].isKeyVis  # swaps iKV var to swap which string is visible

        if visIndex != 0 and visIndex < len(cards) - 1:  # if index isn't the 1st or last card...
            canvas.create_image(0, 0, image=midCard, anchor='nw')  # creates img of middle card
        elif visIndex == 0:  # if index is 1st card...
            canvas.create_image(0, 0, image=firstCard, anchor='nw')  # creates img of first card
        elif visIndex == len(cards) - 1:  # if index is last card...
            canvas.create_image(0, 0, image=lastCard, anchor='nw')  # creates img of last card
        cardChange()  # changes card based on changes made in this method


canvas.create_image(0, 0, image=firstCard, anchor='nw')  # creates firstCard image for initial GUI
root.config(menu=menuBar)  # adds menuBar to root
root.resizable(0, 0)  # makes GUI non-resizable (0 pixels in x AND y direction)
root.mainloop()
