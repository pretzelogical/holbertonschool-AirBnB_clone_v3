#!/usr/bin/python3
import inspect
import io
import sys
import cmd
import shutil
import os

"""
 Backup console file
"""
if os.path.exists("tmp_console_main.py"):
    shutil.copy("tmp_console_main.py", "console.py")
shutil.copy("console.py", "tmp_console_main.py")


"""
 Updating console to remove "__main__"
"""
with open("tmp_console_main.py", "r") as file_i:
    console_lines = file_i.readlines()
    with open("console.py", "w") as file_o:
        in_main = False
        for line in console_lines:
            if "__main__" in line:
                in_main = True
            elif in_main:
                if "cmdloop" not in line:
                    file_o.write(line.lstrip("    ")) 
            else:
                file_o.write(line)

import console


"""
 Create console
"""
console_obj = "HBNBCommand"
for name, obj in inspect.getmembers(console):
    if inspect.isclass(obj) and issubclass(obj, cmd.Cmd):
        console_obj = obj

my_console = console_obj(stdout=io.StringIO(), stdin=io.StringIO())
my_console.use_rawinput = False


"""
 Exec command
"""
def exec_command(my_console, the_command, last_lines = 1):
    my_console.stdout = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = my_console.stdout
    my_console.onecmd(the_command)
    sys.stdout = real_stdout
    lines = my_console.stdout.getvalue().split("\n")
    return "\n".join(lines[(-1*(last_lines+1)):-1])


"""
 Tests
"""
# States
state_id_0 = exec_command(my_console, "create State name=\"California\"")
if state_id_0 is None or state_id_0 == "":
    print("FAIL: Can't create State")

# Cities
city_id_0_0 = exec_command(my_console, "create City state_id=\"{}\" name=\"Fremont\"".format(state_id_0))
if city_id_0_0 is None or city_id_0_0 == "":
    print("FAIL: Can't create City")

# Users
user_id_0 = exec_command(my_console, "create User email=\"a@a.com\" password=\"pwd\" first_name=\"fn\" last_name=\"ln\"")
if user_id_0 is None or user_id_0 == "":
    print("FAIL: Can't create User")
user_id_1 = exec_command(my_console, "create User email=\"b@b.com\" password=\"pwd\" first_name=\"fn\" last_name=\"ln\"")
if user_id_1 is None or user_id_1 == "":
    print("FAIL: Can't create User")
user_id_2 = exec_command(my_console, "create User email=\"c@c.com\" password=\"pwd\" first_name=\"fn\" last_name=\"ln\"")
if user_id_2 is None or user_id_2 == "":
    print("FAIL: Can't create User")
user_id_3 = exec_command(my_console, "create User email=\"d@d.com\" password=\"pwd\" first_name=\"fn\" last_name=\"ln\"")
if user_id_3 is None or user_id_3 == "":
    print("FAIL: Can't create User")

# Places
place_id_0 = exec_command(my_console, "create Place city_id=\"{}\" user_id=\"{}\" name=\"House0\" description=\"des\" number_rooms=4 number_bathrooms=3 max_guest=6 price_by_night=100 latitude=1.3 longitude=2.3".format(city_id_0_0, user_id_0))
if place_id_0 is None or place_id_0 == "":
    print("FAIL: Can't create Place")
place_id_1 = exec_command(my_console, "create Place city_id=\"{}\" user_id=\"{}\" name=\"House1\" description=\"des\" number_rooms=1 number_bathrooms=1 max_guest=2 price_by_night=90 latitude=1.3 longitude=2.3".format(city_id_0_0, user_id_1))
if place_id_1 is None or place_id_1 == "":
    print("FAIL: Can't create Place")

# Reviews
review_id_0 = exec_command(my_console, "create Review place_id=\"{}\" user_id=\"{}\" text=\"review0\"".format(place_id_0, user_id_1))
if review_id_0 is None or review_id_0 == "":
    print("FAIL: Can't create Review")
review_id_1 = exec_command(my_console, "create Review place_id=\"{}\" user_id=\"{}\" text=\"review1\"".format(place_id_0, user_id_2))
if review_id_1 is None or review_id_1 == "":
    print("FAIL: Can't create Review")
review_id_2 = exec_command(my_console, "create Review place_id=\"{}\" user_id=\"{}\" text=\"review2\"".format(place_id_0, user_id_3))
if review_id_2 is None or review_id_2 == "":
    print("FAIL: Can't create Review")
review_id_3 = exec_command(my_console, "create Review place_id=\"{}\" user_id=\"{}\" text=\"review3\"".format(place_id_0, user_id_2))
if review_id_3 is None or review_id_3 == "":
    print("FAIL: Can't create Review")
    


print("OK", end="")

shutil.copy("tmp_console_main.py", "console.py")
