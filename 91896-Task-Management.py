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


# def int_validation(input, bounds=None):



def search_dict(input):
    """This function takes in a nested dictionary and iterates through
    to search for a specific target case within the dictionary. 
    This function returns either the found result in a formatted 
    printable string or None."""

    msg = "Please enter the desired ID"
    target_id = easygui.enterbox(msg)

    # Checking if the desired id is in in the dictionary and outputting 
    # the details of that id if it is found.
    for id, details in input.items():
        if id == target_id:
            output = format_dict_single(details)
            return output
    
    return None


def add_task(task_dictionary, team_members_dictionary):
    """This function takes in the Task Dictionary and 
    Team Members Dictionary and inserts a new task. This task 
    will only be inserted if all compulsory fields are filled, 
    looping enterbox request until fulfilled or cancelled."""

    task_fields = [
        "Title", 
        "Description", 
        "Assignee (optional)", 
        "Priority", 
        "Status"
    ]
    int_bounds = {
        "Priority": [1, 3]
    }


    new_task = []
    task_values = []
    # new_task = easygui.multenterbox(
    #     "Please Enter Task Details",
    #     "New Task",
    #     task_fields
    # )
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
                    if index != 2:
                        error = "All Necessary fields are \
                            required to create task"
                        break
                    else:
                        assignee = False
                
                else:
                    if (task_fields[index] in int_bounds):

                        try:
                            int_test = int(task_values[index])
                        except TypeError:
                            error = f"{task_fields[index]} \
                                must be an Integer."
                            break

                        bounds = int_bounds[task_fields[index]]
                        if not (
                            min(bounds) <= int_test <= max(bounds)
                            ):
                            error = f"{task_fields[index].strip()} \
                                must be within \
                                {min(bounds)} to {max(bounds)}"
                            break

                    elif index == 2:
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
                # Format key value pairs for task here!!!
                task_dictionary[new_id] = new_task
                return task_dictionary, team_members_dictionary
                

def update_task(task_dictionary, team_members_dictionary):
    """This function takes in the Task Dictionary and 
    Team Members Dictionary, asking the user for a task detail to
    edit and validating the requested change for the given detail."""

msg1, msg2 = add_task(task_dictionary, team_members_dictionary)

print(format_dict_all(msg1))
print(f"\n\n{format_dict_all(msg2)}")
