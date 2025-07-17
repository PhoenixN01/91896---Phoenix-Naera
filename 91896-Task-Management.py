import easygui
from typing import cast

task_dictionary = {
    "T1": {
        "Title": "Design Homepage",
        "Description": "Create a mockup of the homepage",
        "Assignee": "JSM",
        "Priority": 3,
        "Status": "In Progress"
    },
    "T2": {
        "Title": "Implement Login Page",
        "Description": "Create the Login Page for the website",
        "Assignee": "JSM",
        "Priority": 3,
        "Status": "Blocked"
    },
    "T3": {
        "Title": "Fix Navigation Menu",
        "Description": "Fix the navigation menu to be more user-friendly",
        "Assignee": "",
        "Priority": 1,
        "Status": "Not Started"
    },
    "T4": {
        "Title": "Add Payment Process",
        "Description": "Implement payment processing for the website",
        "Assignee": "JLO",
        "Priority": 2,
        "Status": "In Progress"
    },
    "T5": {
        "Title": "Create an About Us page",
        "Description": "Create a page with information about the company",
        "Assignee": "BDI",
        "Priority": 1,
        "Status": "Blocked"
    }
}


team_members_dictionary = {
    "JSM": {
        "Name": "John Smith",
        "Email": "John@techvision.com",
        "Tasks Assigned": ["T1", "T2"]
    },
    "JLO": {
        "Name": "Jane Love",
        "Email": "Jane@techvision.com",
        "Tasks Assigned": ["T4"]
    },
    "BDI": {
        "Name": "Bob Dillon",
        "Email": "bob@techvision.com",
        "Tasks Assigned": ["T5"]    
    }
}


STATUS_OPTIONS = [
    "Not Started",
    "In Progress",
    "Blocked",
    "Completed"
]
INT_BOUNDS = {
    "Priority": [1, 3]
}



def format_dict_all(input):
    """This function takes in a nested dictionary and outputs each 
    key / value into a string. This function uses basic handling of 
    formatting information when returning an output. This function can 
    handle 1 layer of nested dictionaries."""

    # Defines an empty list that will contain the output message lines.
    msg_lines = []

    # Iterates through each Id and their dictionaries to format each 
    # nested dictionary, joining each item to the final message.
    for id, details in input.items():
        msg_lines.append(f"\n{id}")
        for detail_id, detail in details.items():
            if isinstance(detail, list):
                new_detail = ", ".join(detail)
                detail = new_detail
            msg_lines.append(f"  {detail_id}: {detail}")
    msg = "\n".join(msg_lines)

    return msg


def format_dict_single(input):
    """This function takes in a dictionary that does not contain nested
    dictionaries and formats the contents into a printable string as an 
    output."""

    # Defines an empty list that will contain the output message lines.
    msg_lines = []

    # Iterates through the single dictionary to convert the contents
    # into a message with basic formatting.
    for id, detail in input.items():
        if isinstance(detail, list):
            new_detail = ", ".join(detail)
            detail = new_detail
        msg_lines.append(f"{id}: {detail}")

    msg = "\n".join(msg_lines)
    return msg


def int_validation(input, bounds=list):
    """This Function takes in an input to be tested and a value for
    the boundaries of the integer. This function will either return 
    True for a successful validation or an error message corresponding
    with the type of error it encountered."""

    # Checks if the input is an integer and returns an error otherwise
    try:
        int_test = int(input)
    except TypeError:
        error = f"{input} must be a valid integer"
        return error

    # Checking if any bounds are present, returning True if 
    if bounds == None:
        return True
    elif (min(bounds) <= int_test <= max(bounds)):
        return True
    else:
        error = f"{int_test} must be within \
            {min(bounds)} to {max(bounds)}"
        return error


def search_dict(input):
    """This function takes in a nested dictionary and iterates through
    to search for a specific target case within the dictionary. 
    This function returns either the found id or None."""

    msg = "Please enter the desired ID"
    target_id = easygui.enterbox(msg)

    # Checking if the desired id is in in the dictionary and outputting 
    # the id if it is found.
    for id in input.keys():
        if id == target_id:
            return id
    
    return None


def add_task(
        task_dictionary, 
        team_members_dictionary, 
        status_options,
        int_bounds):
    """This function takes in the Task Dictionary and 
    Team Members Dictionary and inserts a new task. This task 
    will only be inserted if all compulsory fields are filled, 
    looping enterbox request until fulfilled or cancelled."""

    task_fields = dict(task_dictionary["T1"].keys())
    task_values = []

    while True:
        new_task = cast(list[str] | None, easygui.multenterbox(
            "Please Enter Task Details", 
            "New Task", 
            task_fields,
            task_values
            ))
        
        if new_task == None:
            return task_dictionary, team_members_dictionary
        
        else:
            task_values = list(new_task)
            error = ""

            for index in range(0, len(task_values)):

                if task_values[index].strip() == "":
                    if task_fields[index] != "Assignee":
                        error = "All Necessary fields are \
                            required to create task"
                        break
                    else:
                        assignee = False
                        task_values[index] == "None"

                elif task_fields[index] in int_bounds:

                    check_int = int_validation(
                        task_values[index],
                        int_bounds[task_fields[index]])
                    
                    if not check_int == True:
                        error = check_int
                        break

                elif task_fields[index] == "Assignee":
                    member_id = task_values[index]
                    if not (
                        member_id in \
                        team_members_dictionary.keys()
                        ):
                        error = f"{task_values[index]} \
                            is not a valid ID for \
                            {task_fields[index][:8]}"
                    else:
                        assignee = True
                
                elif task_fields[index] == "Status":
                    if not task_values[index] in status_options:
                        options_msg = ", ".join(status_options)
                        error = f"Status must be one of the \
                            following options: {options_msg}"
                else:
                    continue

            if error:
                easygui.msgbox(error, "Error")
                continue
            else:
                id_list = list(task_dictionary.keys())
                new_id = "T"
                new_id += str(int(id_list[-1][1:]) + 1)

                if assignee:
                    team_members_dictionary[task_values[index]]
                    ["Tasks Assigned"].append(new_id)
                
                task_dict = dict(zip(task_fields, task_values))
                task_dictionary[new_id] = task_dict
                return task_dictionary, team_members_dictionary
                

def update_task(
        task_dictionary, 
        team_members_dictionary, 
        status_options,
        int_bounds):
    """This function takes in the Task Dictionary and 
    Team Members Dictionary, asking the user for a task detail to
    edit and validating the requested change for the given detail."""

    task_id = search_dict(task_dictionary)
    
    if task_id == None:
        return
    
    else:
        task_details = dict(task_dictionary[task_id])
        details = format_dict_single(task_details)
        choices = task_details.keys()
        selection = easygui.buttonbox(
            details, 
            "Select field to edit",
            choices,
            cancel_choice="Exit")
        
        if selection in [None, "Exit"]:
            return task_dictionary, team_members_dictionary
        
        else:
            current_detail = task_dictionary[task_id][selection]
            msg = f"What would you like to change {selection} to?"
            new_detail = easygui.enterbox(
                msg,
                "Edit Field",
                current_detail)
            
            if new_detail == None:
                return task_dictionary, team_members_dictionary
            
            else:
                if new_detail.strip() == "":
                    if selection != "Assignee":
                        error = "All Necessary fields are \
                            required to create task"
                    else:
                        assignee = False
                        new_detail == "None"
                
                elif selection in int_bounds:
                    check_int = int_validation(
                        new_detail,
                        int_bounds[selection])

                    if not check_int == True:
                        error = check_int
                elif selection == "Assignee":
                    member_id = current_detail

# msg1, msg2 = add_task(task_dictionary, team_members_dictionary)


# print(format_dict_all(msg1))
# print(f"\n\n{format_dict_all(msg2)}")

# easygui.msgbox(format_dict_all(task_dictionary))