**07/06/2020**
Steps to implement "Cancel" command:
    - when "Add" is called, create a participant object an insert to a list that stores all 
    the objects
    - When the "Cancel" is called, check with the state of the program; delete the latest object
    int the list 
    - NOTE: I'm no sure that after deleting the object, the program would stop asking for input
    or not