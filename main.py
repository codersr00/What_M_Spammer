import json


try:
    from pywhatkit import sendwhatmsg
    import pandas as pd
    from pandas.io.pytables import Selection
except Exception as e:
    print(e)


def send_what_msg(
    coutryCode: str,
    phNumber: str,
    msg: str,
    time_hour: int,
    time_min: int,
    wait_time: int = 20,
):
    sendwhatmsg(
        phone_no=coutryCode + phNumber,
        message=msg,
        time_hour=time_hour,
        time_min=time_min,
        wait_time=wait_time,
    )


class xl_reader:
    def __init__(self, file: str) -> None:
        try:
            self.xl = pd.read_excel(file)
        except Exception as e:
            print(e)
            print(file)
            exit(1)
        self.slNo = []
        self.phNumber = []
        self.setValues()

    def setValues(self):
        self.df = pd.DataFrame(self.xl)
        for i in range(0, len(self.df.index)):
            self.slNo.append(self.df.iloc[i]["Sl No."])
            self.phNumber.append(self.df.iloc[i]["Ph Number"])

    def getSlNo(self):
        return self.slNo

    def getPhNum(self):
        return self.phNumber


if __name__ == "__main__":
    with open("config.json") as f:
        CONFIG = json.load(f)
    xlR = xl_reader(CONFIG["path"])
    phNum = xlR.getPhNum()
    j = 0
    for i in phNum:
        send_what_msg(
            coutryCode=CONFIG["country_code"],
            phNumber=str(i),
            msg=(CONFIG["msg"]),
            time_hour=int(CONFIG["time_hour"]),
            time_min=int(CONFIG["time_min"]) + j
        )
        j = j + 1
