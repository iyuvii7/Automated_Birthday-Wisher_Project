import pandas as pd
import datetime as dt
import random
import smtplib

PLACE_HOLDER = "[NAME]"
MY_EMAIL = "iyuvii777@gmail.com"
PASSWORD = "kniq bobi vkez vjtb"


def read_birthday(file_path):
    # read csv file into dataframe
    birthdays = pd.read_csv(file_path)
    # Convert DataFrame to dictionary using list comprehension
    birthdays_dict = {(row["month"], row["day"]): list(
        birthdays[birthdays["month"] == row["month"]][birthdays["day"] == row["day"]].to_dict(orient="records")) for
        _, row
        in birthdays.iterrows()}
    return birthdays_dict


def send_birthday_email(person, letter):
    """send the birthday email to the person"""
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=person["email"],
                            msg=f"Subject:Happy Birthday.\n\n{letter}")


def check_and_sent_birthday_wishes(birthdays_dict):
    """Check if today is someone birthday and send wishes."""
    now = dt.datetime.now()
    today_month, today_day = now.month, now.weekday()
    # check if today month and today day matches the values in birthdays_dict dictionary
    if (today_month, today_day) in birthdays_dict:
        # if yes then templates variable contain the list of templates
        templates = ["letter_templates/letter_1.txt", "letter_templates/letter_2.txt", "letter_templates/letter_3.txt"]
        # open the randomly choose template file
        with open(random.choice(templates), mode="r") as file:
            random_letter = file.read()
            # for loop to get the name of person which have today birthday
            for each_dict in birthdays_dict[(today_month, today_day)]:
                # replace the [name] with the person name which have today birthday
                letter = random_letter.replace(PLACE_HOLDER, each_dict["name"])
                # call send_birthday_email function and pass the dictionary of person and wishing_letter
                send_birthday_email(each_dict, letter)


# birthday dict will store the return dictionary from read_birthday function
birthday_dict = read_birthday("birthdays.csv")
# check_and_sent_birthday_wishes function check which have today birthday and send wishes
check_and_sent_birthday_wishes(birthday_dict)