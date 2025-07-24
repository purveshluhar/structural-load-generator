import json

# Global Variable to keep track if automatic module selection is on/off
auto_step = False


def process_json(f_path):
    """
    Function to process JSON file
    :param f_path: string, json file path
    :return: dictionary
    """

    # Load from code data from JSON file
    with open(f_path, 'r') as fd:
        data = json.load(fd)


def get_inp(min_num, max_num, invalid=False):
    """
    Function checks if the input entered is in range and return True or False
    :param min_num
    :param max_num
    :param invalid: boolean
    :return: boolean
    """

    if not invalid:
        choice = input(f"Enter the number of your choice ({min_num}-{max_num}, "
                            f"'next' or '*' to exit) : ")
    else:
        choice = input(f"Invalid Input. Please enter the number of your "
                       f"choice ({min_num}-{max_num}, next' or '*' to exit) : ")


    if choice == "*":
        exit(0)
    elif choice == "next":
        # Declare global variable
        global auto_step
        auto_step = True
        return "next"

    try:
        if min_num <= int(choice) <= max_num:
            return choice
    # If user entered string
    except ValueError:
        return get_inp(min_num, max_num, True)

    return get_inp(min_num, max_num, True)


def main_menu():
    """
    Function to view the main-menu
    :return:
    """

    print(
        "-----------------------------------------------------------------------------------")
    print(
        "                              STRUCTURAL LOAD GENERATOR                            ")
    print(
        "-----------------------------------------------------------------------------------")

    print("Please select a module to continue :")
    print(
        "\t1. Code Setting        [ Set building code, occupancy, risk, geometry ]")
    print(
        "\t2. Select Location     [ Enter the site location of the building ]")
    print(
        "\t3. Wind Module         [ Generate Wind Loads ]")
    print(
        "\t4. Seismic Module      [ Generate Seismic Loads ]")
    print(
        "\t5. Snow Module         [ Generate Snow Loads ]")
    print(
        "-----------------------------------------------------------------------------------")
    print("next     - Automatically step through all module")
    print("*        - Exit the program\n")

    choice = get_inp(1, 5)

    match choice:
        case 1: code_setting()
        case 2: select_location()
        case 3: wind_module()
        case 4: seismic_module()
        case 5: snow_module()
        case _: code_setting()


def code_setting():
    """
    Function to view code-setting module
    :return:
    """

    print(
        "-----------------------------------------------------------------------------------")
    print(
        "                                CODE SETTINGS MODULE                               ")
    print(
        "-----------------------------------------------------------------------------------")

    print("Choose an option :")
    print(
        "\t1. Select Building Code")
    print(
        "\t2. Select Occupancy Group")
    print(
        "\t3. Manually Set Risk Category")
    print(
        "\t4. Input Building Geometry")
    print(
        "-----------------------------------------------------------------------------------")
    print("*        - Go back to Main Menu\n")

    if not auto_step:
        choice = get_inp(1, 4)
    else:
        choice = "next"

    match choice:
        case 1:
            select_building_code()
        case 2:
            select_occupancy_group()
        case 3:
            manual_select_risk_category()
        case 4:
            input_building_geometry()
        case _:
            select_building_code()


def select_building_code():
    """
    Function to select building code
    :return:
    """

    pass


def select_occupancy_group():
    """
    Function to select occupancy group
    :return:
    """

    pass


def manual_select_risk_category():
    """
    Function to manually select risk category
    :return:
    """

    pass


def input_building_geometry():
    """
    Function to define building geometry
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
    code_data = process_json(f_path)

    main_menu()

if __name__ == '__main__':
    main()
