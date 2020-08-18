import pymongo
import datetime
import serial
import time

client = pymongo.MongoClient(
    "mongodb://localhost:27017/test?retryWrites=true&w=majority")
db = client.flowers.measurements


def arduino_read():
    ser = serial.Serial(
        port='COM6',
        baudrate=9600,
    )
    message = ser.readline()
    soil_data = []
    atmosphere_data = []
    try:
        for i in range(0, len(message) // 21):
            atmosphere_data.append({"id": i, "tp": float(message[0 + (21 * i):7 + (21 * i)]),
                                    "hm": float(message[7 + (21 * i):14 + (21 * i)])})
            soil_data.append({"id": i, "mo": float(message[14 + (21 * i):21 + (21 * i)])})
        print(soil_data, atmosphere_data)
    except Exception as e:
        print(e)

    return soil_data, atmosphere_data


def make_list(soil_data, atmosphere_data):
    print("OK")
    return {
        "soil": soil_data,
        "atmosphere": atmosphere_data,
        "timestamp": datetime.datetime.now().timestamp()
    }


if __name__ == "__main__":
    while True:
        try:
            db.insert_one(make_list(*arduino_read()))
        except Exception as e:
            print(e)
        time.sleep(600)
