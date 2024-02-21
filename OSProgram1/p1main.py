"""
OS Program 1
Noah Pelc
10FEB24



Built-in timing functions for each supported language will be posted on the Program 1 Canvas assignment page.

This program does not need to be multiprocess or multithreaded.

You may use your language's standard linked list class(es), if any, to implement any required linked lists in your program. See specific advice in the section for each language.

You will submit your assignment using GitHub Classroom. See the Program 1 assignment page for more information.



"""

import time

"""
    Implement Version 1 and Version 2 of the process creation hierarchy, described in the Description section (below), as separate classes or objects. Both versions must provide the following functions or methods.
        create(int parentPid)
            Allocates and initializes a free PCB object from the array of PCB objects
            For version 1, inserts the newly allocated PCB object into parentPid's list of children
            For version 2, connects the newly allocated PCB object to parentPid and, if it has siblings, its sibling process(es)
            If parentPid is not in the process hierarchy, do nothing; your code may return an error code or message in this case, but it should not halt
        destroy(int targetPid)
            Recursively destroys all descendants of targetPid and marks their PCBs as "free" in the PCB list (i.e., deallocates them)
            For version 1, removes targetPid from its parent's list of children
            For version 2, adjusts connections within the hierarchy graph as needed to re-connect the graph
            If targetPid is not in the process hierarchy, do nothing; your code may return an error code or message in this case, but it should not halt
        showProcessInfo()
            Recursively traverse the process creation hierarchy graph, printing information about each process as you go.
            The output must follow the format in this example.

            Process 0: parent is -1 and children are 1 2
            Process 1: parent is 0 and children are 3
            Process 2: parent is 0 and has no children
            Process 3: parent is 1 and has no children

                For Process 1 in this example, your output may say child is 3 instead of children are 3.
                For Processes 2 and 3 in this example, your output may say child is empty or children are empty instead of has no children.
            Output may be returned to the calling function or sent directly to standard output using println, cout, printf, or similar: your choice.
"""
class PCB:

    def __init__(self, version=0, parent=-1, index=0):
        self.version=version
        self.used = False
        match version:
            case 1:
                """
                Version 1 of the process creation hierarchy uses linked lists to keep track of child processes. In Version 1, each process's control block (PCB) contains at least these two fields:

                a pointer to its parent process and
                a linked list of pointers to 0 or more child processes.

                You might also need to add a "process ID" or "pid" field.
                """
                self.parent=parent
                self.children=[]
                self.pid = index
                self.used = True

                """
                For the purposes of performance evaluation, the PCBs are simplified as follows:

                All PCBs are implemented as an array of size n.
                Each process is referred to by the PCB index, 0 through (n - 1).
                Each PCB is a structure consisting of only two fields:
                parent: a PCB index corresponding to the process's creator
                children: a pointer to a linked list, where each list element contains the PCB index of one child process
                """
                


            case 2:
                """
                Version 2 of the same process creation hierarchy uses no linked lists. Instead, each PCB contains the 4 integer fields parent, first_child, younger_sibling, and older_sibling, as described in the subsection "Avoiding linked lists". Here is the relevant text from our zyBook, section 2.3.
        Linked lists require dynamic memory management, which is costly. The Linux OS has pioneered an approach that eliminates this overhead.

        Instead of a separate linked list anchored in the parent's PCB, the links are distributed over the child PCBs such that each points to the immediate younger sibling and immediate older sibling. The original 2 fields, parent and children, in the PCB of a process p are replaced by 4 new fields:

            parent: points to p's single parent as before
            first_child: points to p's first child
            younger_sibling: points to the sibling of p created immediately following p
            older_sibling: points to the sibling of p created immediately prior to p
                """
                self.parent=parent
                self.first_child=None
                self.younger_sibling=None
                self.older_sibling=None
                self.pid = index
                self.used = True


    """
    destroy(p) represents the destroy function executed by process PCB[p]. The function recursively destroys all descendant processes (child, grandchild, etc.) of process PCB[p] by performing the following tasks:
    for each element q on the linked list of children of PCB[p]:
    destroy(q) /* recursively destroy all descendants */
    free PCB[q]
    deallocate the element q from the linked list
    """
    def destroy1(self, pid, PCB1):
        PCB1[pid].used = False
        templist = [] #used to avoid skipping children during recursion
        for x in PCB1[pid].children:
            templist.append(x)
        for x in templist:
            PCB1[int(x)].destroy1(int(x), PCB1)
        if PCB1[pid].parent >= 0:
            PCB1[PCB1[pid].parent].children.remove(pid)
            

    def destroy2(self, pid, PCB2):
        PCB2[pid].used = False
        if PCB2[pid].parent >= 0:
            if PCB2[PCB2[pid].parent].first_child == pid:
                PCB2[PCB2[pid].parent].first_child = PCB2[pid].younger_sibling
            else: 
                PCB2[PCB2[pid].older_sibling].younger_sibling = PCB2[pid].younger_sibling
        x = PCB2[pid].first_child
        while x != None:
            PCB.destroy2(self, x, PCB2)
            x = PCB2[x].younger_sibling

    """
    create(p) represents the create function executed by process PCB[p]. The function creates a new child process PCB[q] of process PCB[p] by performing the following tasks:
    allocate a free PCB[q]
    record the parent's index, p, in PCB[q]
    initialize the list of children of PCB[q] as empty
    create a new link containing the child's index q and appends the link to the linked list of PCB[p]
    """
    def create1(self, parent, PCB1):
        for i in range(0,16,1):
            if PCB1[i].used == False:
                PCB1[i] = PCB(1, parent, i)
                PCB1[parent].children.append(i)
                break
                
    
    def create2(self, parent, PCB2):
        for i in range(0,16,1):
            if PCB2[i].used == False:
                PCB2[i] = PCB(2, parent, i)
                if PCB2[parent].first_child == None:
                    PCB2[parent].first_child = i
                    break
                else:
                    x = PCB2[parent].first_child
                    while PCB2[x].younger_sibling != None:
                        x = PCB2[x].younger_sibling
                    PCB2[x].younger_sibling = i
                    PCB2[i].older_sibling = x
                    break
                

    """
            showProcessInfo()
            Recursively traverse the process creation hierarchy graph, printing information about each process as you go.
            The output must follow the format in this example.

            Process 0: parent is -1 and children are 1 2
            Process 1: parent is 0 and children are 3
            Process 2: parent is 0 and has no children
            Process 3: parent is 1 and has no children

                For Process 1 in this example, your output may say child is 3 instead of children are 3.
                For Processes 2 and 3 in this example, your output may say child is empty or children are empty instead of has no children.
            Output may be returned to the calling function or sent directly to standard output using println, cout, printf, or similar: your choice.
    """
    def showProcessInfo(self, PCB2):
        if self.used == False:
            return
        childs = ""
        match self.version:
            case 1:
                for x in self.children:
                    childs += str(x) + " "
                    
            case 2:
                childs = ""
                x = self.first_child
                while x != None:
                    childs += str(x) + " "
                    x = PCB2[x].younger_sibling
            case 0:
                return
                    
        if len(childs) > 0:
            print(f"Process {self.pid}: parent is {self.parent} and children are {childs}")
        else:
            print(f"Process {self.pid}: parent is {self.parent} and has no children")
            




"""
    Write a main method or function that provides the following workflow.
        While the user has not typed "end", continue accepting commands. Add each command to a list of actions to take while you run the simulation.
            Hint: the commands could be stored as a list of (string, int) pairs, or you might think of another way to store them.
        When the user types "end" (or optionally any word that is not "create" or "destroy"), stop accepting commands and complete the following steps.

"""

print("Welcome to the process hierarchy program.")
command = ("skip", "0") #This is filler and is going to be skipped at execution
commandList=[]
while(command[0] != "end"):
    #Ask the user to enter commands of the form "create N", "destroy N", or "end", where N is an integer between 0 and 15.
    commandList.append((command[0], command[1]))
    command = input("please enter command to add (create N; destroy N; end): ").split()


#Create an object of the Version 1 class and an object of the Version 2 class.

PCB1=[PCB()] * 16
PCB1[0] = PCB(1, -1, 0)
PCB2=[PCB()] * 16
PCB2[0] = PCB(2, -1, 0)


#Run the command sequence once with the Version 1 object, calling its showProcessInfo method after each command to show the changes in the tree after each command.  Repeat step 5, but with Version 2.
for x in commandList:
    numba = int(x[1])
    match x[0]:
        case "create":
            if PCB1[numba].used == True:
                PCB1[numba].create1(numba, PCB1)
                PCB2[numba].create2(numba, PCB2)

        case "destroy":
            if PCB1[numba].used == True:
                PCB1[numba].destroy1(numba, PCB1)
                PCB2[numba].destroy2(numba, PCB2)

        case _:
            pass

for x in PCB1:
    x.showProcessInfo(PCB1)
print()
for x in PCB2:
    x.showProcessInfo(PCB2)

#Store the current system time in a variable, then run the command sequence 200 times with Version 1. After this, store the new current system time in a second variable. Subtract the start time from the end time to get the Version 1 running time, then display the Version 1 running time.
#Note: Don't call showProcessInfo while running this loop. This will make the output shorter and more readable.
#Repeat step 7, but with Version 2.



startTime1 = time.time_ns()
for j in range(0,200,1):
    PCB1=[PCB()] * 16
    PCB1[0] = PCB(1, -1, 0)
    for x in commandList:
        numba = int(x[1])
        match x[0]:
            case "create":
                if PCB1[numba].used == True:
                    PCB1[numba].create1(numba, PCB1)

            case "destroy":
                if PCB1[numba].used == True:
                    PCB1[numba].destroy1(numba, PCB1)

            case _:
                pass
endTime1 = time.time_ns()


startTime2 = time.time_ns()
for j in range(0,200,1):
    PCB2=[PCB()] * 16
    PCB2[0] = PCB(2, -1, 0)
    for x in commandList:
        numba = int(x[1])
        match x[0]:
            case "create":
                if PCB1[numba].used == True:
                    PCB2[numba].create2(numba, PCB2)

            case "destroy":
                if PCB1[numba].used == True:
                    PCB2[numba].destroy2(numba, PCB2)

            case _:
                pass
endTime2 = time.time_ns()

runtime1 = endTime1 - startTime1
runtime2 = endTime2 - startTime2


print("Run time for version 1: " + str(runtime1) + "\nRuntime for version2: " + str(runtime2))

print("end of program")