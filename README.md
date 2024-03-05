# Passhammer

A Python application to assist in finding available appointments for passport and ID services at Norwegian police stations.

## Features

* **Graphical Interface (GUI)** 
* **Branch Selection:** Allows the user to choose relevant police branches from a list. 
* **Service Selection:** Provides a dropdown to pick the desired passport or ID service.
* **Date Range:**  Input fields for flexible start and end dates.
* **Monitoring:** Continuously checks the availability of appointments within the defined date range at the specified interval.
* **Alerts:** Notifies the user with a popup message if available timeslots are found, offering to open the booking URL.

## Installation

**Prerequisites**

* Python 3 ([https://www.python.org/downloads/](https://www.python.org/downloads/))
* tkinter (usually included in standard Python installations)
* requests library: `pip install requests`

**Instructions**

1. Download or clone the project.
2. Navigate to the project directory.
3. Run the script: `python passhammer.py` (assuming your main script is named 'passhammer.py')

## Usage

1. **Select Branches:** Choose the desired police branches from the list. You can chose multiple branches by using CTRL.
2. **Select Service:** Pick the appropriate passport or ID service from the dropdown menu.
3. **Enter Date Range:** Provide the start and end dates within which to search for appointments.
4. **Set Check Interval:**  Input how often (in minutes) the script should check for availability.
5. **Click 'Submit':** Start the monitoring process.

## License

This project is licensed under MIT
