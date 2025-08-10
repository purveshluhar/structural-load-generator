import json
from typing import Callable
from dotenv import load_dotenv
import os
from helper_func.socket_handler import (setup_socket_client,
                                        send_message_str, send_message_json,
                                        recv_message_json)

# Global Variable to keep track if automatic module selection is on/off
auto_step = False
# Global Variable to keep track of the last page visited
page_history_stack: list[Callable] = [exit]
# Global Variable to set input_data
input_data = {}
# Global variable to store code_data
code_data = {}
# Global variable to store summary data
summary_data = {}

def process_json(f_path, mode='r'):
    """
    Function to process JSON file
    :param f_path: string, json file path
    :param mode:
    :return: dictionary
    """

    # Load from code data from JSON file
    with open(f_path, mode) as fd:
        data = json.load(fd)

    return data


def clear_JSON_data(data):
    """
    To clear existing data in a dictionary
    :param data: dict
    :return:
    """

    for key, value in data.items():
        if type(value) is dict:
            clear_JSON_data(value)
        else:
            data[key] = ""

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


def create_view(arr, option:dict, is_summary=False):
    """
    Function creates the CLI view
    :param arr: string of headers
    :param option: string of menu items
    :param is_summary:
    :return: none
    """

    print(
        "-----------------------------------------------------------------------------------")
    print(f"{arr[0]}")
    print(
        "-----------------------------------------------------------------------------------")

    print(arr[1])

    if not is_summary:
        for key, value in option.items():
            print(f"\t{key}. {value}")
    else:
        for key, value in option.items():
            print(f"\t{key}: {value}")

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
                if page_history_stack[-1] == exit:
                    # Store the input_data before exiting
                    write_json("input_data.json", input_data)
                    write_json("summary_data.json", summary_data)

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
    elif input_typ != str:
        try:
            if type(float(choice)) == input_typ:
                return float(choice)
        except ValueError:
            return get_inp(min_num, max_num, is_main, True, is_range, display, input_typ)
    else:
        return choice

    return ""


def confirm_selection(selection, call_function, next_function=(),
                      exception=False):
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
    elif exception:
        return 0
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
        5: "Snow Module         [ Generate Snow Loads ]",
        6: "Summary of Inputs   [ Prints the summary of inputs ]"
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
        case '6': summary_inputs()
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
        4: "Input Building Geometry"
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
        case _:
            select_building_code()


def select_building_code():
    """
    Function to select building code
    :return:
    """

    global code_data
    global input_data
    global summary_data

    option_str = create_dict(code_data)

    create_view(
        [
            "SELECT BUILDING CODE",
            "Choose the applicable code for your project :"
        ], option_str
    )

    print("*        - Go back to Code Settings\n")

    choice = get_inp(1, len(option_str))
    building_code = option_str[int(choice)]
    input_data["Code Setting"]["Building Code"] = building_code
    summary_data["Code Setting"]["Building Code"] = building_code
    summary_data["Code Setting"]["Standard Version"] = code_data[
        building_code]["Standard Version"]

    confirm_selection(option_str[int(choice)], select_building_code,
                      select_occupancy_group)


def select_occupancy_group():
    """
    Function to select occupancy group
    :return:
    """

    global code_data
    global summary_data
    global input_data

    building_code = summary_data["Code Setting"]["Building Code"]
    option_str = create_dict(code_data[building_code]["OccupancyGroups"])

    create_view(
        [
            "SELECT OCCUPANCY GROUP",
            "Choose the occupancy group for your project :"
        ], option_str
    )

    print("*        - Go back to Code Settings\n")

    choice = get_inp(1, len(option_str))
    occupancy_group = option_str[int(choice)]
    risk_category = code_data[building_code]["OccupancyGroups"][option_str[
        int(choice)]]

    input_data["Code Setting"]["Occupancy Group"] = occupancy_group
    input_data["Code Setting"]["Risk Category"] = risk_category
    summary_data["Code Setting"]["Occupancy Group"] = occupancy_group
    summary_data["Code Setting"]["Risk Category"] = risk_category

    # Add Importance Factor as per risk category
    arr = ["Wind", "Seismic", "Snow"]
    for item in arr:
        summary_data[f"{item} Module"]["Importance Factor"] = code_data[
            building_code]["RiskCategories"][risk_category][item]

    summary_data["Code Setting"]["Risk Level"] = code_data[building_code][
        "RiskCategories"][risk_category]["Level"]
    summary_data["Wind Module"]["MRI"] = code_data[building_code][
        "RiskCategories"][risk_category]["MRI"]

    confirm_selection(occupancy_group, select_occupancy_group,
                      input_building_geometry)


def manual_select_risk_category():
    """
    Function to manually select risk category
    :return:
    """

    global summary_data
    global code_data
    global input_data

    building_code = summary_data["Code Setting"]["Building Code"]
    option_str = create_dict(code_data[building_code]["RiskCategories"])

    if summary_data["Code Setting"]["Occupancy Group"] == "":
        create_view(
            [
                "SELECT RISK CATEGORIES",
                "Choose the risk category for your project :"
            ], option_str
        )
    else:
        risk_category = summary_data["Code Setting"]["Risk Category"]
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
    risk_category = option_str[int(choice)]
    input_data["Code Setting"]["Risk Category"] = risk_category
    summary_data["Code Setting"]["Risk Category"] = risk_category

    # Add Importance Factor as per risk category to summary
    arr = ["Wind", "Seismic", "Snow"]
    for item in arr:
        summary_data[f"{item} Module"]["Importance Factor"] = code_data[
            building_code]["RiskCategories"][risk_category][item]

    summary_data["Code Setting"]["Risk Level"] = code_data[building_code][
        "RiskCategories"][risk_category]["Level"]
    summary_data["Wind Module"]["MRI"] = code_data[building_code][
        "RiskCategories"][risk_category]["MRI"]

    confirm_selection(risk_category, manual_select_risk_category,
                      input_building_geometry)


def input_building_geometry():
    """
    Function to define building geometry
    :return:
    """

    global summary_data
    global input_data

    option_str = {
        1: "Roof Angle (deg)",
        2: "Building Length (ft)",
        3: "Least Width (ft)",
        4: "Mean Roof Height (ft)",
        5: "Project Name"
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
        if value == "Project Name":
            choice = get_inp(display=f"{key}. {value}: > ", input_typ=str,
                             is_range=False)
        else:
            choice = get_inp(display=f"{key}. {value}: > ", input_typ=float,
                         is_range=False)
        input_data["Code Setting"][value] = choice
        summary_data["Code Setting"][value] = choice

    message = ""
    for index, (key, value) in enumerate(option_str.items()):
        message += f"{value}: {summary_data["Code Setting"][value]}"
        if index+1 != len(option_str):
            message += "\n"

    confirm_selection(message, input_building_geometry, select_location)


def summary_inputs():
    """
    Function summarizes all the inputs of the structure
    :return:
    """

    global input_data

    print_data = {}
    index = 0
    for key, value in input_data.items():
        for ckey, cvalue in value.items():
            index += 1
            print_data[f"{index}. {ckey}"] = cvalue

    create_view(
        [
            "SUMMARY OF INPUTS",
            "The loads will be generated as per below summarized inputs for the structure:"
        ], print_data, is_summary=True
    )

    print("Please select an option: ")
    print(f"1-{index}: Edit that input")
    print("*       - Go back to Main Menu")
    print("Proceed to Wind, Seismic, or Snow Module once inputs are "
          "confirmed.\n")

    choice = get_inp(1, 7)

    match choice:
        case '1':
            select_building_code()
        case '2':
            select_occupancy_group()
        case '3':
            manual_select_risk_category()
        case '4' | '5' | '6' | '7':
            input_building_geometry()
        case '8' | '9' | '10':
            select_location()
        case _:
            main_menu()

def write_json(filepath, data):
    """

    :param filepath:
    :param data:
    :return:
    """

    with open(filepath, 'w', encoding="utf-8") as fd:
        json.dump(data, fd, indent=4)


def select_location():
    """
    Function to view select location module
    :return:
    """

    global input_data
    global summary_data

    option_str = {
        1: "221 NE 122nd Avenue, Portland, OR 97230",
        2: "Seattle, WA",
    }

    create_view(
        [
            "INPUT BUILDING LOCATION",
            "You will be asked to provide the building address in any of the "
            "following format: "
        ], option_str
    )

    print("*        - Go back to Main Menu\n")

    message = "Type building address or '*' to go back: > "
    choice = get_inp(is_range=False, display=message, input_typ=str)
    input_data["Select Location"]["Location"] = choice
    summary_data["Select Location"]["Location"] = choice

    confirm_selection(choice, select_location, exception=True)
    get_lat_long()


def get_lat_long():
    """
    Calls geo-locator api to get longitude and latitude
    :return:
    """

    global input_data
    global summary_data

    # Load the PORT from .env
    load_dotenv()
    port = os.getenv("GEOLOCATOR_PORT")

    # Set up the socket
    socket = setup_socket_client(port)

    # Send location to geo-locator
    send_message_str(socket, input_data["Select Location"]["Location"])

    # Receive lat and long
    message = recv_message_json(socket)

    summary_data["Select Location"]["Latitude"] = message["lat"]
    summary_data["Select Location"]["Longitude"] = message["lon"]

    global auto_step
    if auto_step:
        return wind_module()
    else:
        return page_history_stack.pop()()


def wind_module():
    """
    Function to view wind module
    :return:
    """

    global input_data

    option_str = create_dict(input_data["Wind Module"])

    create_view(
        [
            "WIND MODULE",
            "You will be asked to provide the following: "
        ], option_str
    )

    print("start    - To begin input")
    print("*        - Go back to Code Settings\n")

    message = "Type 'start' to begin or '*' to go back: > "
    get_inp(is_range=False, display=message, input_typ=str)

    get_wind_inputs()
    get_wind_loads()


def get_wind_inputs():
    """

    :return:
    """

    global input_data
    global summary_data

    option_str = create_dict(input_data["Wind Module"])
    building_code = summary_data["Code Setting"]["Building Code"]

    for key, value in option_str.items():
        print(f"\nSelect the {value}: ")
        if value == "Exposure Category":
            sub_menu = create_dict(code_data[building_code]["Wind"][value])
            for index, (ckey, cvalue) in enumerate(sub_menu.items()):
                print(f"{index + 1}. {cvalue}")

            choice = get_inp(1, len(sub_menu))
            exposure_cat = sub_menu[int(choice)]
            input_data["Wind Module"][value] = exposure_cat
            summary_data["Wind Module"][value] = exposure_cat
            summary_data["Wind Module"]["zg (ft)"] = code_data[building_code][
                "Wind"][value][exposure_cat]['zg (ft)']
            summary_data["Wind Module"]["alpha"] = code_data[building_code][
                "Wind"][value][exposure_cat]['alpha']

        else:
            choice = get_inp(display=f"{key}. {value}: > ", input_typ=float,
                             is_range=False)
            input_data["Wind Module"][value] = choice
            summary_data["Wind Module"][value] = choice

    message = ""
    for index, (key, value) in enumerate(option_str.items()):
        p_val = input_data['Wind Module'][value]
        message += f"{value}: {p_val}"
        if index + 1 != len(option_str):
            message += "\n"

    confirm_selection(message, wind_module, exception=True)
    return


def get_wind_loads():
    """

    :return:
    """

    global summary_data
    global input_data

    # Load the PORT from .env
    load_dotenv()
    port = os.getenv("WIND_PORT")

    # Set up the socket
    socket = setup_socket_client(port)

    req_data = {
        "lat": summary_data["Select Location"]["Latitude"],
        "lon": summary_data["Select Location"]["Longitude"],
        "standardsVersion": summary_data["Code Setting"]["Standard Version"],
        "riskLevel": summary_data["Code Setting"]["Risk Level"],
        "MRI": str(summary_data["Wind Module"]["MRI"]),
        "z": summary_data["Code Setting"]["Mean Roof Height (ft)"],
        "zg": summary_data["Wind Module"]["zg (ft)"],
        "alpha": summary_data["Wind Module"]["alpha"],
        "Kzt": summary_data["Wind Module"]["Kzt"],
        "Ke": summary_data["Wind Module"]["Ke"],
        "Kd": summary_data["Wind Module"]["Kd"],
        "Building Code": summary_data["Code Setting"]["Building Code"]
    }

    write_json("summary_data.json", summary_data)
    write_json("input_data.json", input_data)

    # Send location to geo-locator
    send_message_json(socket, req_data)

    # Receive seismic load and spectrum value
    message = recv_message_json(socket)

    for key, item in message.items():
        if "Error" in key:
            break
        summary_data["Wind Module"][key] = item

    global auto_step
    if auto_step:
        return seismic_module()
    else:
        return page_history_stack.pop()()


def seismic_module():
    """
    Function to view seismic module
    :return:
    """

    global input_data

    option_str = create_dict(input_data["Seismic Module"])

    create_view(
        [
            "SEISMIC MODULE",
            "You will be asked to provide the following: "
        ], option_str
    )

    print("start    - To begin input")
    print("*        - Go back to Code Settings\n")

    message = "Type 'start' to begin or '*' to go back: > "
    get_inp(is_range=False, display=message, input_typ=str)

    get_seismic_inputs()
    get_seismic_load()

def get_seismic_inputs():
    """
    Gets site class and seismic force resisting system from the user
    :return:
    """

    global input_data
    global summary_data

    option_str = create_dict(input_data["Seismic Module"])
    building_code = summary_data["Code Setting"]["Building Code"]

    for key, value in option_str.items():
        print(f"\nSelect the {value}: ")
        if value == "Seismic Resisting System":
            srs_dict = {}
            index = 0
            for ckey, cvalue in code_data[building_code]["Seismic"][
                value].items():
                for item in cvalue:
                    index += 1
                    srs_dict[index] = {
                        "Name": f"{ckey}-{item['name']}",
                        "R": item["R"],
                        "Omega": item["Omega"],
                        "Cd": item["Cd"]
                    }
                    print(f"{index}. {ckey}-{item['name']}")

            choice = get_inp(1, index)
            input_data["Seismic Module"][value] = srs_dict[int(choice)]['Name']
            summary_data["Seismic Module"][value] = srs_dict[int(choice)]
        elif "Weight" in value:
            choice = get_inp(display=f"{key}. {value}: > ", input_typ=float,
                             is_range=False)
            input_data["Seismic Module"][value] = choice
            summary_data["Seismic Module"][value] = choice
        else:
            sub_menu = create_dict(code_data[building_code]["Seismic"][value])
            for index, (ckey, cvalue) in enumerate(sub_menu.items()):
                print(f"{index+1}. {cvalue}")

            choice = get_inp(1, len(sub_menu))
            site_class = code_data[building_code]["Seismic"]["Site Class"][
                sub_menu[int(choice)]]
            input_data["Seismic Module"][value] = site_class
            summary_data["Seismic Module"][value] = site_class

    message = ""
    for index, (key, value) in enumerate(option_str.items()):
        p_val = input_data['Seismic Module'][value]
        message += f"{value}: {p_val}"
        if index+1 != len(option_str):
            message += "\n"

    confirm_selection(message, seismic_module, exception=True)
    return


def get_seismic_load():
    """
    Calls seismic microservice to get seismic loads
    :return:
    """

    global summary_data
    global input_data

    # Load the PORT from .env
    load_dotenv()
    port = os.getenv("SEISMIC_PORT")

    # Set up the socket
    socket = setup_socket_client(port)

    req_data = {
        "latitude": summary_data["Select Location"]["Latitude"],
        "longitude": summary_data["Select Location"]["Longitude"],
        "riskCategory": summary_data["Code Setting"]["Risk Category"],
        "siteClass": summary_data["Seismic Module"]["Site Class"],
        "title": summary_data["Code Setting"]["Project Name"],
        "R": summary_data["Seismic Module"]["Seismic Resisting System"]["R"],
        "I": summary_data["Seismic Module"]["Importance Factor"],
        "W": summary_data["Seismic Module"]["Weight (kips)"],
        "Building Code": summary_data["Code Setting"]["Building Code"]
    }

    # Send location to geo-locator
    send_message_json(socket, req_data)

    # Receive seismic load and spectrum value
    message = recv_message_json(socket)

    for key, item in message.items():
        if "Error" in key:
            break
        summary_data["Seismic Module"][key] = item

    global auto_step
    if auto_step:
        return snow_module()
    else:
        return page_history_stack.pop()()


def snow_module():
    """
    Function to view snow module
    :return:
    """

    global input_data

    option_str = create_dict(input_data["Snow Module"])

    create_view(
        [
            "SNOW MODULE",
            "You will be asked to provide the following: "
        ], option_str
    )

    print("start    - To begin input")
    print("*        - Go back to Code Settings\n")

    message = "Type 'start' to begin or '*' to go back: > "
    get_inp(is_range=False, display=message, input_typ=str)

    get_snow_inputs()
    get_snow_loads()

def get_snow_inputs():
    """

    :return:
    """

    global input_data
    global summary_data

    option_str = create_dict(input_data["Snow Module"])
    building_code = summary_data["Code Setting"]["Building Code"]

    for key, value in option_str.items():
        print(f"\nSelect the {value}: ")
        choice = get_inp(display=f"{key}. {value}: > ", input_typ=float,
                         is_range=False)
        input_data["Snow Module"][value] = choice
        summary_data["Snow Module"][value] = choice

    message = ""
    for index, (key, value) in enumerate(option_str.items()):
        p_val = input_data['Snow Module'][value]
        message += f"{value}: {p_val}"
        if index + 1 != len(option_str):
            message += "\n"

    confirm_selection(message, snow_module, exception=True)
    return

def get_snow_loads():
    """

    :return:
    """

    global summary_data
    global input_data

    # Load the PORT from .env
    load_dotenv()
    port = os.getenv("SNOW_PORT")

    # Set up the socket
    socket = setup_socket_client(port)

    req_data = {
        "lat": summary_data["Select Location"]["Latitude"],
        "lon": summary_data["Select Location"]["Longitude"],
        "standardsVersion": summary_data["Code Setting"]["Standard Version"],
        "riskLevel": summary_data["Code Setting"]["Risk Level"],
        "Ce": summary_data["Snow Module"]["Ce"],
        "Ct": summary_data["Snow Module"]["Ct"],
        "I": summary_data["Snow Module"]["Importance Factor"],
        "Building Code": summary_data["Code Setting"]["Building Code"]
    }

    # Send location to snow-service
    send_message_json(socket, req_data)

    # Receive snow load and spectrum value
    message = recv_message_json(socket)

    for key, item in message.items():
        if "Error" in key:
            break
        summary_data["Snow Module"][key] = item

    global auto_step
    if auto_step:
        return summary_inputs()
    else:
        return page_history_stack.pop()()


def main():
    """
    Python CLI main function
    :return: None
    """

    f_path = "code_data.json"
    global code_data
    code_data = process_json(f_path)

    f_path = "input_data.json"
    global input_data
    input_data = process_json(f_path)

    #clear_JSON_data(input_data)

    f_path = "summary_data.json"
    global summary_data
    summary_data = process_json(f_path)

    #clear_JSON_data(summary_data)

    main_menu()

if __name__ == '__main__':
    main()
