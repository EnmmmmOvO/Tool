import datetime
import sys

def generate_schedule(days, start_date):
    start_of_week = start_date - datetime.timedelta(days=start_date.weekday())

    schedule = []
    
    t = 1
    for week in range(1, 11):  # We need 11 weeks to skip the 6th one
        if week == 6:  # Skip the 6th week
            continue

        week_schedule = f"## Week{week:02d}\n"

        num = 0
        for day in days:
            day_date = start_of_week + datetime.timedelta(days=(week - 1) * 7 + day)
            formatted_date = day_date.strftime("%Y-%m-%d")
            if num == 0:
                week_schedule += f"- Recording [{t:02d} ({formatted_date})]()  \n"
                num = 1
            else:
                week_schedule += f"&emsp;&emsp;&emsp;&emsp;&emsp;[{t:02d} ({formatted_date})]()  \n"
            t += 1

        week_schedule += "- Slide [](./slide)  \n"
        week_schedule += "&emsp;&emsp;&ensp;[](./slide)  \n"

        schedule.append(week_schedule)

    return "\n".join(schedule)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python readme.py <Course Name> <Course Number> <Start Date (yyyymmdd)> <Day of the week (1-7)> <Day of the week (1-7)>")
        sys.exit(1)

    try:
        start_date = datetime.datetime.strptime(sys.argv[3], "%Y%m%d").date()
    except ValueError:
        print("Invalid date format. Please use yyyymmdd format.")
        sys.exit(1)

    days_of_week = []
    for i in range(4, len(sys.argv)):
        days_of_week.append(int(sys.argv[i]) - 1)

    with open('README.md', 'w') as f:
        f.write(f"# {sys.argv[1]} {sys.argv[2]}\n\n" + generate_schedule(days_of_week, start_date))