from pandas_ods_reader import read_ods
import numpy as np
import datetime as dt
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

path = "zaman çizelgesi.ods"

lessons_number = 6
sheet_name = "Raw Data"

lessons = []

def main():
    df = read_ods(path, sheet_name)

    for i in range(lessons_number):
        col_name = "Ders{}".format(i)
        col = df[col_name]
        col_len = len(col)

        for j in range(col_len):
            if df[col_name][j] != None:
                sort_by_lessons(df[col_name][j], i, j, df)

    print(lessons)
    plot()

def sort_by_lessons(lesson_name, i, j, df):
    try:
        start = "Başlangıç{}".format(i)
        stop = "Bitiş{}".format(i)
        start_time = datetime.strptime(convert_to_time(df[start][j]), "%H:%M")
        stop_time = datetime.strptime(convert_to_time(df[stop][j]), "%H:%M")

        duration = stop_time - start_time

        for a in lessons:
            if lesson_name == a[0]:
                a[1] = a[1]+duration
                return

        lessons.append([lesson_name, duration])
    except:
        print("False format")

def convert_to_time(time):
    time = time.replace("PT", "").replace("H", ":").replace("M00S","")
    return time

def plot():
    global lessons

    x = []
    y = []

    for l in lessons:
        x.append(l[0])
        y.append(l[1])

    zero = dt.datetime(2018,1,1)
    time = [zero+t for t in y]

    zero = mdates.date2num(zero)
    print(zero)
    time = [t-zero for t in mdates.date2num(time)]
    print(time)

    f = plt.figure()
    ax = f.add_subplot(1,1,1)

    ax.bar(x, time)
    ax.yaxis_date()
    ax.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    # add 10% margin on top (since ax.margins seems to not work here)
    ylim = ax.get_ylim()
    ax.set_ylim(None, ylim[1]+0.1*np.diff(ylim))
    #
    # plt.bar(x,y)

    plt.show()
main()
