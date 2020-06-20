Command:
    - ADD: add an entry to the database
        + You are required to enter all the information about the participant
        + ID: A generated incrementing 0 padded 8 digit number and it should be unique
        + Name: The contestant's name (must include both first and last name)
        + Email address: The contestants email address. 
        + School District: What school district is the contestant from (see more in must be a school district in the schoolDistricts.md in Schools_And_Competitions folder)
        + Competitions: What event the contestant is competing in (see more in Competitions.md in Schools_And_Competitions folder)
        + Birthday: Date of the contestant’s birth. Format mm/dd/yyyy. Example: 08/28/2004
        + Score: The score the contestant received (assume it is a percent value)
    - HELP: show instructions
    - CANCEL: cancel the current command
    - SHOWF: display the whole database sorted by first name
    - SHOW: display the whole database sorted by last name
    - SEARCH: 
        + ID: show you the specific contestant with the ID
        + School districts, competitions, fist name and last name: show you contestants with relevant information
    - EXIT: exit the program
        + If a file is opened, the file will be updated automatically
        + If there's no file opened, you can choose to update a particular file by entering the name of the file
        + Or you can choose to create a new file by entering a new unique name
        + If you don't want to save, enter Cancel command
        NOTE: all files will be saved into the Saved Database folder
    - OPEN: open a saved database
        + Enter the name of the file (it must exist in the Saved Database folder)
        NOTE: User can only open 1 file per run-time
    - DEL: delete a particular entry by ID
    - TOP: shows the top 3 contestant of a particular event
        + Enter a valid event and there must be at least one contestant in the event
        
