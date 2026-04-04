# university-bus-tracker-ADBUs
This is a university bus tracker (named ADBUs) made using Django and simple frontend scripts.
ADBUs is a web application that is developed to track the movements and whereabout of an University bus (demo university is Assam Don Bosco University Azara Campus Guwahati India).

YOUTBUE: https://youtu.be/k9bs1fQGKko?si=EFGf43c42U9a_GEJ

# Setup Guide

Follow these steps to run the project locally on your machine.

# 1. Prerequisites

Make sure you have installed:

* Python (3.x)
* pip (comes with Python)
* Django (latest ver)
  


# 2. Download the Project
Either:

* Download ZIP from GitHub and extract it
  OR
* Clone using Git (if installed)

  

# 3. Navigate to Project Folder

Open terminal / command prompt:

"cd path/to/University-Bus-Tracker-ADBUs"

Make sure you are in the folder containing `manage.py`.



# 4. Create Virtual Environment (Recommended but optional)

"python -m venv venv"

Activate it:

# Windows:

"venv\Scripts\activate"

# Linux/Mac:

"source venv/bin/activate"



# 5. Install Dependencies


"pip install -r requirements.txt"



# 6. Setup Environment Variables

Create a `.env` file in the project root.

Example:

_____________________________________
SECRET_KEY=your_generated_secret_key
DEBUG=True
_____________________________________

To generate a secret key, run:

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"



# 7. Run the Development Server

"python manage.py runserver"



# 8. Run the Tick Server 

"python tracker/tick.py"
(open a 2nd terminal, with the same directory path)



# 9. Open in Browser

http://127.0.0.1:8000/



# Notes

* Do NOT upload or share your `.env` file
* If the project includes API keys, add your own where required



# Troubleshooting

* If a module is missing:

  "pip install <module_name>"

* Make sure virtual environment is activated
* Ensure you are in the correct directory (where `manage.py` exists)


# Done!

Your project should now be running locally 
