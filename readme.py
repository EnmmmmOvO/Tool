import datetime
import sys


def generate_schedule(days):
    current_date = datetime.datetime.now()

    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())

    schedule = []

    for week in range(1, 11):  # We need 11 weeks to skip the 6th one
        if week == 6:  # Skip the 6th week
            continue

        week_schedule = f"## Week{week:02d}\n"

        num = 0
        for day in days:
            day_date = start_of_week + datetime.timedelta(days=(week - 1) * 7 + day)
            formatted_date = day_date.strftime("%Y-%m-%d")
            if num == 0:
                week_schedule += f"- Recording [{day:02d} ({formatted_date})]()  \n"
                num = 1
            else:
                week_schedule += f"&emsp;&emsp;&emsp;&emsp;&emsp;[02 ({formatted_date})]()  \n"

        week_schedule += "- Slide [](./slide)  \n"
        week_schedule += "&emsp;&emsp;&ensp;[](./slide)  \n"

        schedule.append(week_schedule)

    return "\n".join(schedule)


if __name__ == '__main__':
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: python readme.py <Course Name> <Course Number> <Day of the week (1-7)> <Day of the week (1-7)>")
        sys.exit(1)

    days_of_week = [int(sys.argv[3]) - 1]

    if len(sys.argv) == 5:
        days_of_week.append(int(sys.argv[4]) - 1)

    with open('README.md', 'w') as f:
        f.write(f"# {sys.argv[1]} {sys.argv[2]}\n\n" + generate_schedule(days_of_week))
