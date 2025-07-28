import json
from typing import Callable

# Global Variable to keep track if automatic module selection is on/off
auto_step = False
# Global Variable to keep track of the last page visited
page_history_stack: list[Callable] = [exit]
# Global Variable to set inputs
input_data = {
    "Building Code": "International Building Code 2021",
    "Occupancy Group": "",
    "Risk Category": "",
    "Roof Angle (deg)": "",
    "Building Length (ft)": "",
    "Least Width (ft)": "",
    "Mean Roof Height (ft)": ""
}
# Global variable to store code_data
code_data = {}

def process_json(f_path):
    """
    Function to process JSON file
    :param f_path: string, json file path
    :return: dictionary
    """

    # Load from code data from JSON file
    with open(f_path, 'r') as fd:
        data = json.load(fd)

    return data


def create_dict(data:dict):
    """

    :param data:
    :return:
    """

    export = {}
    for index, (key, value) in enumerate(data.items()):
        export[index+1] = key

    return export


def create_view(arr, option:dict):
    """
    Function creates the CLI view
    :param arr: string of headers
    :param option: string of menu items
    :return: none
    """

    print(
        "-----------------------------------------------------------------------------------")
    print(f"{arr[0]}")
    print(
        "-----------------------------------------------------------------------------------")

    print(arr[1])

    for key, value in option.items():
        print(f"\t{key}. {value}")

    print(
        "-----------------------------------------------------------------------------------")


def get_inp(min_num=0, max_num=0, is_main=False, invalid=False,
            is_range=True, display="", input_typ:type=int):
    """
    Function checks if the input entered is in range and return True or False
    :param min_num
    :param max_num
    :param invalid: boolean
    :param is_main: boolean
    :param is_range: boolean
    :param input_typ
    :param display
    :return: boolean
    """

    if is_range:
        if not invalid:
            if is_main:
                choice = input(f"Enter the number of your choice ({min_num}-"
                               f" {max_num}, 'next' or '*' to exit) : > ")
            else:
                choice = input(
                    f"Enter the number of your choice ({min_num}-{max_num}, "
                    f"'*' to go back) : > ")
        else:
            if is_main:
                choice = input(f"Invalid Input. Please enter the number of your "
                               f"choice ({min_num}-{max_num}, next' or '*' to exit) "
                               f": > ")
            else:
                choice = input(f"Invalid Input. Please enter the number of your "
                               f"choice ({min_num}-{max_num}, '*' to go back) "
                               f": > ")
    else:
        if not invalid:
            choice = input(display)
        else:
            print("Invalid Input. Try again")
            choice = input(display)

    global page_history_stack
    if type(choice) == str:
        if "*" in choice:
            call_func = ()
            for i in range(choice.count("*")):
                call_func = page_history_stack.pop()

            return call_func()
        elif choice == "next":
            # Declare global variable
            global auto_step
            auto_step = True
            return "next"
        elif choice == "start":
            return ""

    if is_range:
        try:
            if min_num <= int(choice) <= max_num:
                return choice
        # If user entered string
        except ValueError:
            return get_inp(min_num, max_num, is_main, True)
    else:
        try:
            if type(float(choice)) == input_typ:
                return float(choice)
        except ValueError:
            return get_inp(min_num, max_num, is_main, True, is_range, display, input_typ)

    return ""


def confirm_selection(selection, call_function, next_function):
    """
    Function to view the confirmation selection of the input made
    :return: integer
    """

    print(f"\nYou selected:\n{selection}\n")
    print("Would you like to:")
    print("\t 1. Confirm and Proceed")
    print("\t 2. Edit this input")

    choice = get_inp(1, 2)

    if int(choice) == 2:
        return call_function()

    global auto_step
    if auto_step:
        return next_function()
    else:
        return page_history_stack.pop()()


def main_menu():
    """
    Function to view the main-menu
    :return:
    """

    option_str = {
        1: "Code Setting        [ Set building code, occupancy, risk, "
            "geometry ]",
        2: "Select Location     [ Enter the site location of the building ]",
        3: "Wind Module         [ Generate Wind Loads ]",
        4: "Seismic Module      [ Generate Seismic Loads ]",
        5: "Snow Module         [ Generate Snow Loads ]"
    }

    create_view(
        [
            "STRUCTURAL LOAD GENERATOR",
            "Please select a module to continue :"
        ], option_str
    )

    print("next     - Automatically step through all module")
    print("*        - Exit the program\n")

    choice = get_inp(1, len(option_str), True)

    # Add main menu to page visited
    global page_history_stack
    page_history_stack.append(main_menu)

    match choice:
        case '1': code_setting()
        case '2': select_location()
        case '3': wind_module()
        case '4': seismic_module()
        case '5': snow_module()
        case _: code_setting()


def code_setting():
    """
    Function to view code-setting module
    :return:
    """

    option_str = {
        1: "Select Building Code",
        2: "Select Occupancy Group",
        3: "Manually Set Risk Category",
        4: "Input Building Geometry",
        5: "Summary of Inputs"
    }

    create_view(
        [
            "CODE SETTINGS MODULE",
            "Choose an option: "
        ], option_str
    )

    print("*        - Go back to Main Menu\n")

    if not auto_step:
        choice = get_inp(1, len(option_str))
    else:
        choice = "next"

    # Add main menu to page visited
    global page_history_stack
    page_history_stack.append(code_setting)

    match choice:
        case '1':
            select_building_code()
        case '2':
            select_occupancy_group()
        case '3':
            manual_select_risk_category()
        case '4':
            input_building_geometry()
        case '5':
            summary_inputs()
        case _:
            select_building_code()


def select_building_code():
    """
    Function to select building code
    :return:
    """

    option_str = {
        1: "International Building Code 2021",
        2: "International Building Code 2018",
        3: "ASCE 7-16",
        4: "Unified Facilities Criteria"
    }

    create_view(
        [
            "SELECT BUILDING CODE",
            "Choose the applicable code for your project :"
        ], option_str
    )

    print("*        - Go back to Code Settings\n")

    choice = get_inp(1, len(option_str))
    global input_data
    input_data["Building Code"] = option_str[int(choice)]

    confirm_selection(option_str[int(choice)], select_building_code,
                      select_occupancy_group)


def select_occupancy_group():
    """
    Function to select occupancy group
    :return:
    """

    global input_data
    global code_data

    option_str = create_dict(code_data[input_data["Building Code"]][
        "OccupancyGroups"])

    create_view(
        [
            "SELECT OCCUPANCY GROUP",
            "Choose the occupancy group for your project :"
        ], option_str
    )

    print("*        - Go back to Code Settings\n")

    choice = get_inp(1, len(option_str))
    input_data["Occupancy Group"] = option_str[int(choice)]

    confirm_selection(option_str[int(choice)], select_occupancy_group,
                      input_building_geometry)


def manual_select_risk_category():
    """
    Function to manually select risk category
    :return:
    """

    global input_data
    global code_data

    option_str = create_dict(code_data[input_data["Building Code"]][
                                 "RiskCategories"])

    if input_data["Occupancy Group"] == "":
        create_view(
            [
                "SELECT RISK CATEGORIES",
                "Choose the risk category for your project :"
            ], option_str
        )
    else:
        risk_category = code_data[input_data["Building Code"]][
                                 "OccupancyGroups"][input_data["Occupancy Group"]]
        create_view(
            [
                "SELECT RISK CATEGORIES",
                f"Risk Category Selected from Occupancy Group: "
                f"{risk_category}\n"
                "Choose the risk category to overwrite above:"
            ], option_str
        )

    print("*        - Go back to Code Settings\n")

    choice = get_inp(1, len(option_str))
    input_data["Risk Category"] = option_str[int(choice)]

    confirm_selection(option_str[int(choice)], manual_select_risk_category,
                      input_building_geometry)


def input_building_geometry():
    """
    Function to define building geometry
    :return:
    """

    global input_data
    option_str = {
        1: "Roof Angle (deg)",
        2: "Building Length (ft)",
        3: "Least Width (ft)",
        4: "Mean Roof Height (ft)"
    }

    create_view(
        [
            "INPUT BUILDING GEOMETRY",
            "You will be asked to provide the following: "
        ], option_str
    )

    print("start    - To begin input")
    print("*        - Go back to Code Settings\n")

    message = "Type 'start' to begin or '*' to go back: > "
    get_inp(is_range=False, display=message, input_typ=str)
    for key, value in option_str.items():
        choice = get_inp(display=f"{key}. {value}: > ", input_typ=float,
                         is_range=False)
        input_data[value] = choice

    message = ""
    for key, value in option_str.items():
        message += f"{value}: {input_data[value]}"
        if value != "Mean Roof Height (ft)":
            message += "\n"

    confirm_selection(message, input_building_geometry, summary_inputs)


def summary_inputs():
    """

    :return:
    """

    pass


def select_location():
    """
    Function to view select location module
    :return:
    """

    pass


def wind_module():
    """
    Function to view wind module
    :return:
    """

    pass


def seismic_module():
    """
    Function to view seismic module
    :return:
    """

    pass


def snow_module():
    """
    Function to view snow module
    :return:
    """

    pass


def main():
    """
    Python CLI main function
    :return: None
    """

    f_path = "code_data.json"
    global code_data
    code_data = process_json(f_path)

    main_menu()

if __name__ == '__main__':
    main()
