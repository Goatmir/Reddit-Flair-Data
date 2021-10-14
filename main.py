# Code Created by Goatmir
# Reachable at @Princess Goatmir#5757 (discord)
# © Copyright 2021, Goatmir, All Rights Reserved
# Fair Usage

#  GGGGGG     OOOOOO        AAA     TTTTTTTTTT   MMM       MMM   IIIIIIII   RRRRRRR
# GG         OO    OO      AA AA        TT       MMMM     MMMM      II      RR    RR
# GG  GGGG   OO    OO     AAAAAAA       TT       MM MM   MM MM      II      RRRRRRR
# GG    GG   OO    OO    AA     AA      TT       MM  MM MM  MM      II      RR  RR
#  GGGGGG     OOOOOO    AA       AA     TT       MM   MMM   MM   IIIIIIII   RR    RR

# - - - - - - INFO - - - - - -
# This script gets X amount of posts in a subreddits Hot, It then gets their flair
# It gets how many times each flair appeared (for all submissions)
# Then it displays a pie chart for what percentage of the posts had each flair
# if something is double quoted in comments "like this" then it is an object
# Extension files needed:
# secrets.json  -  Contains client_id and client_secret of reddit application


import praw
import json
import matplotlib.pyplot as plt

# List of colours (uses HEX codes) Add your own!
ColorList = ['#FFD700', '#800000', '#FFFF00', '#dea5a4', '#D43790', '#FF0000', '#40e0d0', '#A020F0', '#808080',
             '#0000FF', '#89CFF0']


def init(sub):
    # Opens and loads Reddit credentials
    with open("../jsons/secrets/TIAFC_secrets.json") as r:
        creds = json.load(r)
    # (Makes "Reddit" global so we don't have to import it everywhere)
    # (You might want to change it to a return and import it into modules using it)
    global reddit
    reddit = praw.Reddit(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        user_agent=creds["user_agent"],
    )
    # Creates a global variable for "subreddit", which is then set to PRAWs subreddit
    global subreddit
    subreddit = reddit.subreddit(sub)


def getflairs(x):
    # Checks if "x" is an int, if it cant identify it, it raises an Exception
    if type(x) is not int:
        raise Exception("Number input is not an integer")

    if type(x) is int:
        # Creates a list to store the flairs in
        flairlist = []
        # for "x" number of posts from subreddit's new
        for submission in subreddit.hot(limit=x):
            # Gets posts flair and adds it to "FlairList"
            # If flair is None, flair will equal "None"
            flair = submission.link_flair_text
            flairlist.append(flair)
        # If no flairs were gathered it raises an Exception
        if len(flairlist) == 0:
            raise Exception("Was not able to get flairs")

        # Returns the list of flairs
        return flairlist

    else:
        raise Exception("Failure to identify input")


def flairOrganize(flairs):
    FlairList = []
    FlairDict = {}
    total = 0
    for flair in flairs:
        # if the post doesn't have a flair it gives it the "None" flair
        if flair is None:
            flair = 'None'
        # If not already in the list of Flairs it adds it
        if flair not in FlairList:
            FlairList.append(flair)
        # Tries to add 1 to the count each flair has mentioned
        try:
            FlairDict[flair] += 1
            total += 1
        except KeyError:
            FlairDict[flair] = 1

    for flair in FlairDict:
        # Gets the percentage instead of just raw count
        num = FlairDict[flair]
        num = num / total
        num = num * 100
        # replaces count with percentage
        FlairDict[flair] = num
    i = 0
    for flair in FlairList:
        # Adds Percentage to flairs name
        flair += ' (' + str(round(FlairDict[flair], 2)) + '%)'
        FlairList[i] = flair
        i += 1
    return FlairDict, FlairList, total


def FlairsDisplay(organizedflairs, exploding=None):
    # Creates list of objects used in chart
    labels = organizedflairs[1]
    sizes = []
    explode = []
    colors = []
    # Gets colours for the chart (all different)
    for i in range(len(labels)):
        try:
            color = ColorList[i]
        except IndexError:
            i -= (len(labels) + 1)
            color = ColorList[i]
        colors.append(color)
    # Gets the sizes of each flair and adds them to to "sizes"
    for flair in organizedflairs[0]:
        x = organizedflairs[0][flair]
        sizes.append(x)
    # Sets the biggest slice to explode (be shown separated from everything else
    if exploding is None:
        for size in sizes:
            # if the size is equal to the greatest in the list
            if size == max(sizes):
                explode.append(0.1)
            else:
                explode.append(0.0)
    # Sets a particular flair to explode
    elif exploding is not None:
        # Sets No flair to explode
        if (exploding == 'None') or (exploding == 'none'):
            for _ in labels:
                explode.append(0.0)
        # if the flair isn't being shown it raises an Exception
        elif exploding not in labels:
            raise Exception("exploding not valid item")
        # else it sets that flair to explode
        else:
            for label in labels:
                if label == exploding:
                    explode.append(0.1)
                else:
                    explode.append(0.0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=0, colors=colors)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Sets title showing information
    plt.title("Percentage of each flairs used in r/{} (out of {} posts in hot)".format(subreddit.display_name,
                                                                                       organizedflairs[2]))
    plt.show()


def main():
    # Subreddit being used
    init("teenagers")
    flairs = getflairs(100)
    organizedflairs = flairOrganize(flairs)
    FlairsDisplay(organizedflairs=organizedflairs, exploding='None')


if __name__ == '__main__':
    main()
