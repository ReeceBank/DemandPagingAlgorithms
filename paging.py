#by Reece van der Bank
# writen in python 3.6.4



# FIFO, LRU, and OPT paging algorithms in python.
#----- IMPORTS ------------------------------------------------------------------------------------------
import sys
import random

#----- MAIN (just for the sequence and calls each function) ---------------------------------------------
def main():
    #~~~<three different ways to load in a sequence>~~~
    pages = stringToArray(85625354235326256856234213754315) #for using a already made sequence, any number greater than 0 works
    pages = [5,9,4,2,4,2,6,9,7,0,7,6,3,9,6,1,6,9,6,1,9,9,8,2,1,5,7,3,5,0] #can also simply set the pages as a already made array
    pages = randArray(32) #creates a random sequence of size 16. change for greater sizes
    #just comment out/remove the ones not wanting to be used
    #~~~</three different ways to load in a sequence>~~~
    
    size = int(sys.argv[1])
    print ("FIFO", FIFO(size,pages), "page faults.")
    print ("LRU", LRU(size,pages), "page faults.")
    print ("OPT", OPT(size,pages), "page faults.")

#----- FIFO START ---------------------------------------------------------------------------------------
def FIFO(size,pages):
    pagefaults = 0
    fifoList = [] #page frame
    fifoAge = [] # tracks the current age of the pages in the frame. this is the same as order of them going in as the fist page will always be the oldest, second will be second oldest etc.
    
    for i in pages:    
       
        if i in fifoList: #fifo doesnt care if a page is already in frame, but lru does
            continue
        else:
            pagefaults+=1 #page was not in the frame so a fault occured
            if (len(fifoList)<size): #sees if theres empty space in the frame, if there is then it just adds the page and tracks its order/age
                fifoList.append(i)
                fifoAge = [x+1 for x in fifoAge]
                fifoAge.append(0)
            else:
                fifoList.pop(fifoAge.index(max(fifoAge))) #if the frame is full then it finds and removes the oldest page from both the frame and age tracking list
                fifoAge.pop(fifoAge.index(max(fifoAge)))
                fifoList.append(i)
                fifoAge = [x+1 for x in fifoAge] #ages all the other pages up by one
                fifoAge.append(0)                #newest added page is given an age of zero
    
    return pagefaults 
#----- LRU START ---------------------------------------------------------------------------------------
# lru is almost idential to fifo except when a page is fround thats already in the frame is just resets that pages age and ages all the other pages up by one
def LRU(size,pages):
    pagefaults = 0

    lruList = [] #page frame
    lruAge = [] #tracks the least recently used
    
    for i in pages:  

        if i in lruList:
            lruAge = [x+1 for x in lruAge] # increase the age of each page by 1 
            lruAge[lruList.index(i)] = 0 #when a page has been found and is a hit then it resets the counter for that page since lru wants to remove the least recently used page, and this one was just used
        else:
            pagefaults+=1
            if (len(lruList)<size): #the page frame has space for more pages so it just adds that page
                lruList.append(i)
                lruAge = [x+1 for x in lruAge] #ages every other page up by one
                lruAge.append(0) #and then sets the newest pages age to zero
            else:
                lruList.pop(lruAge.index(max(lruAge))) #if the frame is full then it finds and removes the least recently used page from both the frame and age tracking list
                lruAge.pop(lruAge.index(max(lruAge)))
                lruList.append(i)
                lruAge = [x+1 for x in lruAge] #ages all the other pages up by one
                lruAge.append(0)               #newest added page is given an age of zero
                
    return pagefaults

#----- OPT START -----------------------------------------------------------------------------------------   
def OPT(size,pages):
    pagefaults = 0
    
    optList = [] #page frame
    popList = pages[:] #makes a copy of the full sequence to remove them step by step to help keep track of which value is furthest away from being used. used as a basic list queue
    
    for i in pages:    
        if i in optList:
            popList.remove(i) 
            continue
        else:
            pagefaults+=1
            if (len(optList)<size): # the frame still has space so it just slots the next one in and go along the popList 'queue'
                optList.append(i)
                popList.remove(i)
            else:
                choppingblockList = []  #chopping block is dynamic and will only be used if every number in current frame appears later on. theyre added as the program finds which ones are still in the sequence and their distance from the start.
                popList.remove(i)
                for x in optList:
                    if(x not in popList): #poplist is constaly reduced so as to not find pages already loaded in
                        optList.remove(x)
                        optList.append(i)
                        break #found a page in the frame that doesnt appear again, making it the easiest choice to remove
                    else:
                        choppingblockList.append(popList.index(x))
                        
                if (len(choppingblockList)==len(optList)):

                    optList.pop(choppingblockList.index(max(choppingblockList))) #will only be reached if every value in the frame appears again later in the sequence, then will find which one is furthest away and replaces it
                    optList.append(i)
                    
    return pagefaults  

#----- Random number sequence generator -------------------------------------------------------------
# Used to make random strings of given length for running the algorithms
def randArray(length):
    randList = []
    for x in range(length):
        randList.append(random.randint(0,9)) 
    return randList

#convert a string to array
def stringToArray(string):
    randarray = [int(i) for i in str(string)] #to convert a given string of numbers like 123194231 into a array of [1,2,3,1,9,4.. etc for the algorithms. just a simply QoL function
    return randarray


#----- name=main ------------------------------------------------------------------------------------   
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python paging.py [number of pages]")
    elif (sys.argv[1]=='0'): #failsafing
        print("Frame size cannot be smaller than 1")
    else:
        main()
