import os
import sys
import time
import keyboard
import webbrowser
from pygame import mixer
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Base Values
wrapLimit = 100 # How many characters can be put onto one line before the program tries to wrap it.

storyNames = []

mixer.init()

# Initilising all story names. Important for search feature.
print("Loading (This could take a while)...")
for name in os.listdir("STORIES/"):
    storyNames.append(name)

def clearScreen(): # Clears the screen.
    for i in range(0, 10):
        print("\n\n\n\n\n\n\n\n\n")

def readStory(chapters, chapterNames, scrollSpeed, initialChapter, storyName):
    name = storyName
    isDone = False
    currentChapter = initialChapter
    currentParagraph = 0
    while not isDone:
        clearScreen()
        print("-----------------\nType 'END' to stop reading. Hit enter to proceed.\n-----------------")
        print("\n" + "Chapter " + str(currentChapter + 1) + ": " + chapterNames[currentChapter] + "\n")

        wordWrap = 0
        while keyboard.is_pressed("enter"):
            pass
        searchingCommand = False
        instantSkip = False
        commandEntered = ""
        for i in chapters[currentChapter][currentParagraph]:
            if searchingCommand and i != '}':
                commandEntered += i

            if i == "{":  # Command identified.
                searchingCommand = True
            elif i == "}":
                searchingCommand = False
                # Handling all commands:
                if commandEntered == "sf":
                    instantSkip = True
                elif commandEntered[0] == 'p':
                    commandContents = commandEntered.split(" ", 1)
                    time.sleep(float(commandContents[1]))
                    instantSkip = True
                elif commandEntered[0] == 'm':
                    commandContents = commandEntered.split(" ", 2)
                    instantSkip = True
                    if commandContents[1] == "STOP":
                        mixer.music.stop()
                    elif commandContents[1] == "FADE":
                        mixer.music.fadeout(int(float(commandContents[2]) * 1000))
                    else:
                        mixer.music.load("MUSIC/" + name + "/" + commandContents[1])
                        mixer.music.play(loops=-1)
                elif commandEntered[0] == 'i':
                    commandContents = commandEntered.split(" ", 1)
                    img = mpimg.imread('IMAGES/' + name + "/" + commandContents[1])
                    imgplot = plt.imshow(img)
                    plt.axis('off')
                    plt.show()
                    instantSkip = True
                commandEntered = ""

            if not searchingCommand and i != '}':
                if wordWrap < wrapLimit or i != " ":  # Handles word wrapping
                    sys.stdout.write(i)
                    wordWrap += 1
                else:
                    sys.stdout.write("\n")
                    wordWrap = 0
                if keyboard.is_pressed("enter"):
                    while keyboard.is_pressed("enter"):
                        pass
                    break
                time.sleep(scrollSpeed)

        print("\n")
        if not instantSkip:
            option = raw_input("> ")
            while keyboard.is_pressed("enter"):
                pass
            if option == "END":
                isDone = True
                mixer.music.stop()
        instantSkip = False

        currentParagraph += 1
        if (currentParagraph + 1) > len(chapters[currentChapter]):
            currentChapter += 1
            currentParagraph = 0
            if (currentChapter + 1) > len(chapterNames):
                isDone = True
                clearScreen()
                print("End of story. Press enter to continue.")
                raw_input("")
                mixer.music.stop()
    clearScreen()

def chapterSelect(chapters, chapterNames, scrollSpeed, storyName):
    clearScreen()
    isDone = False

    while not isDone:
        index = 1
        for i in chapterNames:
            if ("Chapter " + str(index) + ": ") in chapterNames[index - 1]:
                chapterNames[index - 1].replace(("Chapter" + str(index) + ": "), "")
            sys.stdout.write("Chapter " + str(index) + ": ")
            print(chapterNames[index - 1])
            index += 1

        print("\nType a chapter name to start reading from there.")
        print("Type |BACK| to go back.\n")
        chapter = raw_input("> ")

        if chapter == "|BACK|":
            isDone = True
        elif chapter in chapterNames:
            readStory(chapters, chapterNames, scrollSpeed, chapterNames.index(chapter), storyName)
            isDone = True
        else:
            print("Error - Unrecognisable command entered - " + chapter)

def editStory(storyName):
    isDone = False
    name = storyName
    chapterNames = []
    chapters = []
    tags = []
    scrollSpeed = 0.02
    description = ""

    f = open("STORIES/" + name + "/DESC.txt", "r")
    description = f.read()
    f.close()

    f = open("STORIES/" + name + "/TAGS.txt", "r")
    for i in f:
        tags.append(i.strip())
    f.close()

    f = open("STORIES/" + name + "/SETTINGS.txt", "r")
    scrollSpeed = float(f.read().strip())
    f.close()

    f = open("STORIES/" + name + "/STORY.txt", "r")

    chapterContents = []
    for i in f:
        if i.strip() == "":
            pass
        elif i[0] == "|":
            chapterNames.append(i.strip()[1:-1])
            if len(chapterContents) > 0:
                chapters.append(chapterContents)
                chapterContents = []
        else:
            chapterContents.append(i.strip())
    chapters.append(chapterContents)
    f.close()

    clearScreen()
    isDone = False
    while not isDone:
        print(name)
        print(description)
        print("\nPotential Options:\nedit name\nedit description\nedit tags\nedit scroll speed\nedit chapters\nback")
        command = raw_input("> ")
        if command == "edit name":
            clearScreen()
            print("Enter new name:")
            newName = raw_input()
            if newName in storyNames:
                print("Error - Name already taken.")
                raw_input()
            else:
                os.mkdir("STORIES/" + newName)
                f = open("STORIES/" + newName + "/DESC.txt", "w")
                f.write(description)
                f.close()

                f = open("STORIES/" + newName + "/TAGS.txt", "w")
                for i in tags:
                    f.write(i + "\n")
                f.close()

                f = open("STORIES/" + newName + "/SETTINGS.txt", "w")
                f.write(str(scrollSpeed))
                f.close()

                f = open("STORIES/" + newName + "/STORY.txt", "w")
                f1 = open("STORIES/" + name + "/STORY.txt", "r")
                for i in f1:
                    f.write(i)
                f.close()
                f1.close()

                os.remove("STORIES/" + name + "/DESC.txt")
                os.remove("STORIES/" + name + "/TAGS.txt")
                os.remove("STORIES/" + name + "/SETTINGS.txt")
                os.remove("STORIES/" + name + "/STORY.txt")
                os.rmdir("STORIES/" + name)
                storyNames[storyNames.index(name)] = newName
                name = newName
            clearScreen()
        elif command == "edit description":
            clearScreen()
            print("Enter new description:")
            newDesc = raw_input()
            description = newDesc
            f = open("STORIES/" + name + "/DESC.txt", "w")
            f.write(newDesc)
            f.close()
            clearScreen()
        elif command == "edit tags":
            isDone2 = False
            while not isDone2:
                clearScreen()
                print("Tags:")
                for i in tags:
                    print("-" + i)
                sys.stdout.write("\n")
                print("Enter a tag to remove it. Type in a new tag to add it to the list.")
                print("Type FIN to finish.")
                newTag = raw_input("> ")
                if newTag == "FIN":
                    isDone2 = True
                else:
                    if newTag in tags:
                        tags.remove(newTag)
                    else:
                        tags.append(newTag)

            f = open("STORIES/" + name + "/TAGS.txt", "w")
            for i in tags:
                f.write(i + "\n")
            f.close()
            clearScreen()
        elif command == "edit scroll speed":
            clearScreen()
            print("Enter new scroll speed (Originally " + str(scrollSpeed) + "):")
            try:
                newSS = float(raw_input())
                if newSS < 0:
                    print("Error: Invalid scroll speed.")
                    raw_input()
                else:
                    f = open("STORIES/" + name + "/SETTINGS.txt", "w")
                    f.write(str(newSS))
                    f.close()
                    scrollSpeed = newSS
            except ValueError:
                print("Error: Invalid scroll speed.")
                raw_input()
            clearScreen()
        elif command == "edit chapters":
            clearScreen()
            isDone3 = False
            while not isDone3:
                print("Chapters:")
                index = 1
                for i in chapterNames:
                    print("Chapter " + str(index) + ": " + i)
                    index += 1
                sys.stdout.write("\n")
                print("Enter the name of the chapter you want to edit or delete. Enter a new chapter to add it.")
                print("Enter FIN to finish.")
                cs = raw_input("> ")
                if cs == "FIN":
                    isDone3 = True
                elif cs == "":
                    print("Error - Invalid chapter.")
                    raw_input()
                else:
                    if cs in chapterNames:
                        clearScreen()
                        print("Enter an option for this chapter:\nedit\ndelete\nchange name")
                        cs2 = raw_input("> ")
                        if cs2 == "edit":
                            f = open("New Chapter.txt", "w")
                            for i in chapters[chapterNames.index(cs)]:
                                f.write(i + "\n\n")
                            f.close()
                            webbrowser.open("New Chapter.txt")
                            clearScreen()
                            print("Type in the chapter's contents in the opened notepad file.")
                            print("Click here and press enter when you are done.")
                            raw_input()
                            newChapterContents = []
                            f = open("New Chapter.txt", "r")
                            for i in f:
                                newChapterContents.append(i.strip())
                            f.close()
                            os.remove("New Chapter.txt")

                            finalisedContents = []
                            for i in newChapterContents:
                                if i != "":
                                    finalisedContents.append(i)

                            chapters[chapterNames.index(cs)] = finalisedContents
                            f = open("STORIES/" + name + "/STORY.txt", "w")
                            for i in chapters:
                                f.write("|" + chapterNames[chapters.index(i)] + "|\n")
                                for j in i:
                                    f.write(j + "\n\n")
                            f.close()

                            f = open("STORIES/" + name + "/STORY.txt", "r")

                            chapterContents = []
                            chapterNames = []
                            chapters = []
                            for i in f:
                                if i.strip() == "":
                                    pass
                                elif i[0] == "|":
                                    chapterNames.append(i.strip()[1:-1])
                                    if len(chapterContents) > 0:
                                        chapters.append(chapterContents)
                                        chapterContents = []
                                else:
                                    chapterContents.append(i.strip())
                            chapters.append(chapterContents)
                            f.close()

                            clearScreen()

                        elif cs2 == "delete":
                            clearScreen()
                            delOp = raw_input("Are you sure you want to delete this chapter (y or n)? ")
                            if delOp == "y":
                                chapters.remove(chapters[chapterNames.index(cs)])
                                chapterNames.remove(cs)

                                f = open("STORIES/" + name + "/STORY.txt", "w")
                                for i in chapters:
                                    f.write("|" + chapterNames[chapters.index(i)] + "|\n")
                                    for j in i:
                                        f.write(j + "\n\n")
                                f.close()
                            clearScreen()
                        elif cs2 == "change name":
                            newChapterName = raw_input("Enter a new name for the chapter: ")
                            chapterNames[chapterNames.index(cs)] = newChapterName
                            f = open("STORIES/" + name + "/STORY.txt", "w")
                            for i in chapters:
                                f.write("|" + chapterNames[chapters.index(i)] + "|\n")
                                for j in i:
                                    f.write(j + "\n\n")
                            f.close()
                            clearScreen()
                        else:
                            print("Error - Invalid option.")
                            raw_input()
                    else:
                        f = open("New Chapter.txt", "w")
                        f.close()
                        webbrowser.open("New Chapter.txt")
                        clearScreen()
                        print("Type in the new chapter's contents in the opened notepad file.")
                        print("Click here and press enter when you are done.")
                        raw_input()
                        newChapterContents = []
                        f = open("New Chapter.txt", "r")
                        for i in f:
                            newChapterContents.append(i.strip())
                        f.close()
                        os.remove("New Chapter.txt")

                        f = open("STORIES/" + name + "/STORY.txt", "a")
                        f.write("\n\n|" + cs + "|\n")

                        for i in newChapterContents:
                            f.write(i + "\n")
                        f.close()

                        f = open("STORIES/" + name + "/STORY.txt", "r")

                        chapterContents = []
                        chapterNames = []
                        chapters = []
                        for i in f:
                            if i.strip() == "":
                                pass
                            elif i[0] == "|":
                                chapterNames.append(i.strip()[1:-1])
                                if len(chapterContents) > 0:
                                    chapters.append(chapterContents)
                                    chapterContents = []
                            else:
                                chapterContents.append(i.strip())
                        chapters.append(chapterContents)
                        f.close()

                        clearScreen()
            clearScreen()
        elif command == "back":
            clearScreen()
            isDone = True
        else:
            print("Error - Unrecognisable command entered - " + command)
    return name

def showStory(storyName):
    isDone = False
    name = storyName
    chapterNames = []
    chapters = []
    tags = []
    scrollSpeed = 0.02
    description = ""

    f = open("STORIES/" + name + "/DESC.txt", "r")
    description = f.read()
    f.close()

    f = open("STORIES/" + name + "/TAGS.txt", "r")
    for i in f:
        tags.append(i.strip())
    f.close()

    f = open("STORIES/" + name + "/SETTINGS.txt", "r")
    scrollSpeed = float(f.read().strip())
    f.close()

    f = open("STORIES/" + name + "/STORY.txt", "r")

    chapterContents = []
    for i in f:
        if i.strip() == "":
            pass
        elif i[0] == "|":
            chapterNames.append(i.strip()[1:-1])
            if len(chapterContents) > 0:
                chapters.append(chapterContents)
                chapterContents = []
        else:
            chapterContents.append(i.strip())
    chapters.append(chapterContents)
    f.close()

    clearScreen()
    isDone = False

    while not isDone:
        print(name)
        print(description)
        print("\nPotential Options:\nread story\nchapter select\nedit story\nfinish")
        command = raw_input("> ")

        if command == "read story":
            readStory(chapters, chapterNames, scrollSpeed, 0, name)
        elif command == "chapter select":
            chapterSelect(chapters, chapterNames, scrollSpeed, name)
        elif command == "edit story":
            name = editStory(name)
            chapterNames = []
            chapters = []
            tags = []
            scrollSpeed = 0.02
            description = ""

            f = open("STORIES/" + name + "/DESC.txt", "r")
            description = f.read()
            f.close()

            f = open("STORIES/" + name + "/TAGS.txt", "r")
            for i in f:
                tags.append(i.strip())
            f.close()

            f = open("STORIES/" + name + "/SETTINGS.txt", "r")
            scrollSpeed = float(f.read().strip())
            f.close()

            f = open("STORIES/" + name + "/STORY.txt", "r")

            chapterContents = []
            for i in f:
                if i.strip() == "":
                    pass
                elif i[0] == "|":
                    chapterNames.append(i.strip()[1:-1])
                    if len(chapterContents) > 0:
                        chapters.append(chapterContents)
                        chapterContents = []
                else:
                    chapterContents.append(i.strip())
            chapters.append(chapterContents)
            f.close()
        elif command == "finish":
            clearScreen()
            isDone = True
        else:
            print("Error - Unrecognisable command entered - " + command)

def getInput():
    command = raw_input("> ")
    if command == "help":
        print("Commands:")
        print("\"help\": Displays all usable commands.")
        print("\"create story\": Creates a new story.")
        print("\"browse\": Browse all stories you have created.")
        print("\"delete\": Delete a selected story.")
        print("\"instructions\": Instructions on how to use commands in your stories.")
        print("\"quit\": Exit the program.")
    elif command == "create story":
        clearScreen()
        name = raw_input("Enter the name of your story: ")
        description = raw_input("Enter a description for your story: ")

        tags = []
        print("\nEntering tags - Enter a tag and hit enter to confirm. Type FIN to finish: ")
        isDone = False
        while not isDone:
            tag = raw_input("> ")
            if tag == "FIN":
                isDone = True
            else:
                tags.append(tag)

        if name == "" or description == "":
            print("Error - Missing information")
        else:
            successful = False
            try:
                os.mkdir("STORIES/" + name)
                os.mkdir("MUSIC/" + name)
                os.mkdir("IMAGES/" + name)
                f = open("STORIES/" + name + "/DESC.txt", "w")
                f.write(description)
                f.close()
                storyNames.append(name)

                f = open("STORIES/" + name + "/TAGS.txt", "w")
                for i in tags:
                    f.write(i + "\n")
                f.close()

                f = open("STORIES/" + name + "/SETTINGS.txt", "w")
                f.write("0.02")
                f.close()

                f = open("STORIES/" + name + "/STORY.txt", "w")
                f.close()
                
                successful = True
            except WindowsError:
                print("Error - Story already exists.\n")

            if successful:
                showStory(name)
    elif command == "browse":
        print("Select an option to browse stories by:\nall\nname\ntag")
        browseOp = raw_input("> ")
        clearScreen()
        if browseOp == "all":
            for i in storyNames:
                print("-" + i)
            print("\nEnter the name of the story you want to view.")
            selectedStory = raw_input("> ")
            clearScreen()
            if not selectedStory in storyNames:
                print("Error - Unrecognisable story.")
                raw_input()
            else:
                showStory(selectedStory)
        elif browseOp == "name":
            searchCriteria = raw_input("Enter the string you want to search stories by:\n> ")
            clearScreen()
            displayedEntries = 0
            for i in storyNames:
                if searchCriteria in i:
                    print("-" + i)
                    displayedEntries += 1
            if displayedEntries <= 0:
                print("No stories matched your search criteria.")
                raw_input()
            else:
                print("\nEnter the name of the story you want to view.")
                selectedStory = raw_input("> ")
                clearScreen()
                if not selectedStory in storyNames:
                    print("Error - Unrecognisable story.")
                    raw_input()
                else:
                    showStory(selectedStory)
        elif browseOp == "tag":
            searchCriteria = raw_input("Enter the tag you want to search stories by:\n> ")
            clearScreen()
            displayedEntries = 0
            for i in storyNames:
                f = open("STORIES/" + i + "/TAGS.txt", "r")
                foundTags = []
                for j in f:
                    foundTags.append(j.strip())
                if searchCriteria in foundTags:
                    print("-" + i)
                    displayedEntries += 1
                f.close()
            if displayedEntries <= 0:
                print("No stories matched your search criteria.")
                raw_input()
            else:
                print("\nEnter the name of the story you want to view.")
                selectedStory = raw_input("> ")
                clearScreen()
                if not selectedStory in storyNames:
                    print("Error - Unrecognisable story.")
                    raw_input()
                else:
                    showStory(selectedStory)
        else:
            print("Error - Unrecognisable command.")
            raw_input()
    elif command == "delete":
        clearScreen()
        for i in storyNames:
            print("-" + i)
        print("\nEnter the name of the story you want to delete.")
        selectedStory = raw_input("> ")
        if selectedStory in storyNames:
            confirmation = raw_input("Are you sure you want to delete this story. It cannot be undone (y or n): ")
            if confirmation == "y":
                os.remove("STORIES/" + selectedStory + "/DESC.txt")
                os.remove("STORIES/" + selectedStory + "/SETTINGS.txt")
                os.remove("STORIES/" + selectedStory + "/STORY.txt")
                os.remove("STORIES/" + selectedStory + "/TAGS.txt")
                os.rmdir("STORIES/" + selectedStory)
                storyNames.remove(selectedStory)
                clearScreen()
        else:
            print("Error - Unrecognisable story.")
            raw_input()
    elif command == "instructions":
        clearScreen()
        webbrowser.open("Comamnds.txt")
    elif command == "quit":
        sys.exit()
    else:
        print("Error - Unrecognisable command entered - " + command)
    getInput()

clearScreen()
print("--- Story Writer V0.1 ---")
print("--- Made by Alexander Nair ---")
print("\n---Type help for all commands---")

getInput()
mixer.quit()
