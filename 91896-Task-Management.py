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


def output_dict(input):
    """This function takes in a dictionary and outputs each key / value
    into a window, formating nested dictionaries and lists into 
    printable strings."""

    # Defines an empty list that will contain the output message lines
    msg_lines = []
    for id, details in input:
        msg_lines.append(f"\n{id}")
        for detail, value in details:
            if isinstance(value, list):
                new_value = ", ".join(value)
                msg_lines.append(f"\t{detail}: {new_value}")
            else:
                str(value)
                msg_lines.append(f"\t{detail}: {value}")
        