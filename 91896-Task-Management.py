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
        "Assignee": "None",
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

TASK_FIELDS = [
    "Title",
    "Description",
    "Assignee",
    "Priority",
    "Status"
]
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


def int_validation(input, bounds, field):
    """This Function takes in an input to be tested and a value for
    the boundaries of the integer. This function will either return 
    True for a successful validation or an error message corresponding
    with the type of error it encountered, along with the field it is 
    reffering to."""

    # Checks if the input is an integer and returns an error otherwise
    try:
        int_test = int(input)
    except:
        error = f"{input} must be a valid integer"
        return error

    # Checking if any bounds are present, returning True if 
    if bounds == None:
        return True
    elif (min(bounds) <= int_test <= max(bounds)):
        return True
    else:
        error = f"{int_test} is an invalid value for {field}.\n\n"
        error += f"{field} must be within "
        error += f"{min(bounds)} to {max(bounds)}"
        return error


def search_dict(input):
    """This function takes in a nested dictionary and iterates through
    to search for a specific target case within the dictionary. 
    This function returns either the found id or None."""

    # Asks user to select an option to search for
    msg = "Please choose from the options below:"
    choices = []
    for id, details in input.items():
        key_list = list(details.keys())
        choices.append(f"{id}: {details[key_list[0]]}")

    result = easygui.choicebox(msg, "Search", choices)

    # Returns user to menu if they cancelled or exited the window
    if result == None:
        return None
    
    else:
        result_id = list(input.keys())[choices.index(result)]
        return result_id

def task_value_validation(
        task_field, task_value, 
        team_members_dictionary, 
        int_bounds, status_options):
    """This function handles the various validations required by
    Add Task and Edit Task. This function ensures that each field is 
    created and/or changed to an approved value, returning a 
    corresponding error if not. This function will also return a bool
    representing the presence of an assignee for the details."""

    error = ""
    assignee = False

    # Checks for a missing value being received
    if task_value.strip() == "":
        if task_field != "Assignee":
            error = f"{task_field} is required to continue"
        else:
            task_value = "None"

    # Checking if the value requires integer validation as well as 
    # boundary validation if needed
    # (A boundary value of none from int_bounds won't check boundaries)
    elif task_field in int_bounds:
        check_int = int_validation(
            task_value, int_bounds[task_field], task_field
            )
        if not check_int == True:
            error = check_int

    # Checking if an assignee value is a valid id or "None"
    elif task_field == "Assignee":
        member_id = task_value
        if not (
            member_id in \
            team_members_dictionary.keys()
            or member_id.lower() == "none"
            ):
            member_id_list = team_members_dictionary.keys()
            error = f"{member_id} is not a valid ID for Assignee\n\n"
            error += f"Assignee ID's: {', '.join(member_id_list)}"
        elif member_id.lower() == "none":
            task_value = "None"
        else:
            assignee = True

    # Checking if a status value is within the valid options
    elif task_field == "Status":
        if not task_value in status_options:
            options_msg = ", ".join(status_options)
            error = "Status must be one of the following options: \n\n"
            error += f"{options_msg}"
    
    return error, assignee, task_value

def add_task(
        task_dictionary, team_members_dictionary,
        task_fields, status_options, int_bounds):
    """This function takes in the Task Dictionary and 
    Team Members Dictionary and inserts a new task. This task 
    will only be inserted if all compulsory fields are filled, 
    looping the multenterbox request until fulfilled or cancelled."""

    task_values = []

    # Looping multenterbox request until the task is fulfilled
    while True:
        new_task = cast(list[str] | None, easygui.multenterbox(
            "Please Enter Task Details", 
            "New Task", 
            task_fields,
            task_values
            ))
        
        # Returning user to menu if the window was cancelled or exited
        if new_task == None:
            return task_dictionary, team_members_dictionary
        
        else:
            task_values = list(new_task)

            # Looping through each field in the multenterbox result
            for index in range(0, len(task_values)):
                
                # Validating each task field in the result
                error, assignee, task_values[index] = \
                    task_value_validation(
                        task_fields[index], task_values[index], 
                        team_members_dictionary, int_bounds, 
                        status_options
                        )
                
                # Exiting at the first sign of an error
                if error:
                    break
            
            # Restarting the request if an error occured, 
            # procedurally adding the task if it is fulfilled properly
            if error:
                easygui.msgbox(error, "Error")
                continue
            else:
                id_list = list(task_dictionary.keys())
                new_id = "T"
                new_id += str(int(id_list[-1][1:]) + 1)

                if assignee:
                    team_members_dictionary[
                        list(team_members_dictionary.keys())[index]
                        ]["Tasks Assigned"].append(new_id)
                
                task_dict = dict(zip(task_fields, task_values))
                task_dictionary[new_id] = task_dict
                msg = "Task Added Successfully\n\n"
                msg += format_dict_single(task_dict)
                easygui.msgbox(msg, "Task Confirmation")
                return task_dictionary, team_members_dictionary
                

def edit_task(
        task_dictionary, team_members_dictionary, 
        status_options, int_bounds):
    """This function takes in the Task Dictionary and 
    Team Members Dictionary, asking the user for a task detail to
    edit and validating the requested change for the given detail."""

    task_id = search_dict(task_dictionary)
    member_id_list = team_members_dictionary.keys()
    
    # Returning the user if the search function was cancelled or exited
    if task_id == None:
        return task_dictionary, team_members_dictionary
    
    else:

        # Looping the task detail editing, similar to add_task()
        while True:

            # Formatting the task display, field choices and buttonbox 
            # for the task editing
            task_details = dict(task_dictionary[task_id])
            details = "Current Details: \n\n"
            details += f"{format_dict_single(task_details)}"
            choices = list(task_details.keys())
            choices.append("Exit")
            selection = easygui.buttonbox(
                details, "Select field to edit", choices)
            
            if selection in [None, "Exit"]:
                return task_dictionary, team_members_dictionary
            
            else:
                current_detail = task_dictionary[task_id][selection]
                error = ""

                msg = f"What would you like to change {selection} to?"
                if selection in ["Assignee", "Status"]:
                    if selection == "Assignee":
                        options = member_id_list
                    elif selection == "Status":
                        options = status_options
                    msg += f"\n\nOptions: "
                    msg += ", ".join(options)

                new_detail = easygui.enterbox(
                    msg,
                    f"Edit {selection}",
                    current_detail)
                
                # Returns user back to task view if cancelled or exited
                if new_detail == None:
                    continue
                
                # Validates users modification to the task
                else:
                    error, assignee, new_detail = task_value_validation(
                        selection, new_detail, 
                        team_members_dictionary,
                        int_bounds, status_options
                    )
                
                if error:
                    easygui.msgbox(error, "Error")
                    continue
                
                # Updates dictionaries and loops back to menu with new 
                # task details, saved and ready to exit
                else:
                    if selection == "Assignee":
                        if not new_detail == current_detail:
                            team_members_dictionary[current_detail]\
                                ["Tasks Assigned"].remove(task_id)
                            if assignee:

                                team_members_dictionary[new_detail]\
                                    ["Tasks Assigned"].append(task_id)
                                team_members_dictionary[new_detail]\
                                    ["Tasks Assigned"].sort()
                        
                    task_dictionary[task_id][selection] = new_detail
                    completed_msg = "Change Added Successfully\n\n"
                    completed_msg += f"Old Detail: {current_detail}\n"
                    completed_msg += f"New Detail: {new_detail}"

def generate_report(task_dictionary, status_options):
    """Generate a report containing the number of tasks in each status.
    """

    report_dict = {status: int(0) for status in status_options}

    # Iterates through each task to count status quantities
    for task in task_dictionary.values():
        report_dict[task["Status"]] += 1
    
    # Formats report sections based on the collated amounts of each 
    # status
    msg_lines = [
        f"  {key}: {value}" for key, value in report_dict.items()
        ]
    msg = "\n---Task Report---\n"
    msg += "\n".join(msg_lines)

    # Outputs final version of the report to the user
    easygui.msgbox(msg, "Task Report")
    return

def main(
        task_dictionary, 
        team_members_dictionary, 
        task_fields,
        status_options,
        int_bounds):

    # Declares the list of functions available in the menu screen    
    menu_options = [
        "Search for a Task",
        "Search for a Team Member",
        "Add Task",
        "Edit Task",
        "View All Tasks",
        "View Members",
        "Generate Report",
        "Quit Menu"
    ]

    # Loops the menu screen until user specifically exits or quits the 
    # menu
    while True:
        msg = "Welcome\n\nPlease select an action to continue"
        action = easygui.buttonbox(msg, "Main Menu", menu_options)

        if action in [None, "Quit Menu"]:
            return task_dictionary, team_members_dictionary
        
        else:
            
            # Check if the selection involved the search function
            if action in [menu_options[0], menu_options[1]]:
                input_list = [task_dictionary, team_members_dictionary]
                
                # Searches the corresponding dict to the users selection
                id = search_dict(
                    input_list[menu_options.index(str(action))]
                    )

                if id == None:
                    continue
                
                # Outputs the results
                else:
                    result = format_dict_single(
                        input_list[menu_options.index(str(action))][id]
                        )
                    easygui.msgbox(
                        f"Search Complete\n\n{result}", 
                        "Search Result"
                        )

            # Checks if the task specific functions are required
            elif action in [menu_options[2], menu_options[3]]:
                task_actions = [
                    lambda: add_task(
                        task_dictionary, team_members_dictionary,
                        task_fields, status_options, int_bounds
                    ),
                    lambda: edit_task(
                        task_dictionary, team_members_dictionary,
                        status_options, int_bounds
                    )
                ]

                # Dynamically selects task function based on the index 
                # from menu_options, starting after the search indexes
                task_dictionary, team_members_dictionary = \
                    task_actions[(menu_options.index(str(action)))-2]()
            
            # Checks if an entire dict is needed to be outputted
            elif action in [menu_options[4], menu_options[5]]:
                dict_list = [task_dictionary, team_members_dictionary]
                title_list = [
                    "Task Dictionary", "Team Members Dictionary"]
                
                # Dynamically choose and format Dict title and data
                title = title_list[menu_options.index(str(action))-4]
                msg = f"{title}\n\n"
                msg += format_dict_all(
                    dict_list[menu_options.index(str(action))-4])
                
                easygui.msgbox(msg, title)

            # Checks if the report is selected
            elif action == "Generate Report":
                generate_report(task_dictionary, status_options)

# Run the main menu with the required dicts and constants for all 
# functions included in the menu
task_dictionary, team_members_dictionary = \
    main(
    task_dictionary, team_members_dictionary, 
    TASK_FIELDS, STATUS_OPTIONS, INT_BOUNDS
    )