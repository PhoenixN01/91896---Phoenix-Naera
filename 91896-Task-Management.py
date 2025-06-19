import easygui

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


def output_dict_all(input):
    """This function takes in a nested dictionary and outputs each key / value
    into a string. This function uses basic handling of formatting information to present the information"""

    # Defines an empty list that will contain the output message lines
    msg_lines = []

    # Iterates through each Id and their dictionaries
    for id, details in input.items():
        msg_lines.append(f"\n{id}")
        for detail_id, detail in details.items():
            if isinstance(detail, list):
                new_detail = ", ".join(detail)
                msg_lines.append(f"  {detail_id}: {new_detail}")
            else:
                msg_lines.append(f"  {detail_id}: {detail}")
    msg = "\n".join(msg_lines)

    return msg


