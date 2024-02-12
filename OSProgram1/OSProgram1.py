"""
OS Program 1
Noah Pelc
10FEB24



Built-in timing functions for each supported language will be posted on the Program 1 Canvas assignment page.

This program does not need to be multiprocess or multithreaded.

You may use your language's standard linked list class(es), if any, to implement any required linked lists in your program. See specific advice in the section for each language.

You will submit your assignment using GitHub Classroom. See the Program 1 assignment page for more information.



"""

from operator import index
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
    def __init__(self):
        pass

    def __init__(self, version, parent, index):
        self.version=version
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

                """
                For the purposes of performance evaluation, the PCBs are simplified as follows:

                All PCBs are implemented as an array of size n.
                Each process is referred to by the PCB index, 0 through (n - 1).
                Each PCB is a structure consisting of only two fields:
                parent: a PCB index corresponding to the process's creator
                children: a pointer to a linked list, where each list element contains the PCB index of one child process

                The necessary functions are simplified as follows:

                create(p) represents the create function executed by process PCB[p]. The function creates a new child process PCB[q] of process PCB[p] by performing the following tasks:
                allocate a free PCB[q]
                record the parent's index, p, in PCB[q]
                initialize the list of children of PCB[q] as empty
                create a new link containing the child's index q and appends the link to the linked list of PCB[p]


                destroy(p) represents the destroy function executed by process PCB[p]. The function recursively destroys all descendant processes (child, grandchild, etc.) of process PCB[p] by performing the following tasks:
                for each element q on the linked list of children of PCB[p]:
                destroy(q) /* recursively destroy all descendants */
                free PCB[q]
                deallocate the element q from the linked list
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

            case _:
                print("Error in PCB version assignment")
    def create(p):





"""
    Write a main method or function that provides the following workflow.
        Ask the user to enter commands of the form "create N", "destroy N", or "end", where N is an integer between 0 and 15.
        While the user has not typed "end", continue accepting commands. Add each command to a list of actions to take while you run the simulation.
            Hint: the commands could be stored as a list of (string, int) pairs, or you might think of another way to store them.
        When the user types "end" (or optionally any word that is not "create" or "destroy"), stop accepting commands and complete the following steps.
        Create an object of the Version 1 class and an object of the Version 2 class.
        Run the command sequence once with the Version 1 object, calling its showProcessInfo method after each command to show the changes in the tree after each command.
        Repeat step 5, but with Version 2.
        Store the current system time in a variable, then run the command sequence 200 times with Version 1. After this, store the new current system time in a second variable. Subtract the start time from the end time to get the Version 1 running time, then display the Version 1 running time.
            Note: Don't call showProcessInfo while running this loop. This will make the output shorter and more readable.
        Repeat step 7, but with Version 2.
"""

print("Welcome to the process hierarchy program.")
command = input("please enter command (create N; destroy N; end): ")
#BREAK COMMAND INTO WORD AND NUMBER TUPLE


PCBs=[16]