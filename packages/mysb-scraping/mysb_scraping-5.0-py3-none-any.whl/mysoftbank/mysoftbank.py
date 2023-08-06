import re
import ast
import requests
from bs4 import BeautifulSoup


class API:

    def __init__(self, telnum=None, password=None, line_access_token=None):
        self.telnum = telnum
        self.password = password
        self.line_access_token = line_access_token
        self.data = {}

    def _login(self):
        session = requests.Session()
        r = session.get("https://my.softbank.jp/msb/d/webLink/doSend/MRERE0000")		
        soup = BeautifulSoup(r.text, "lxml")
        ticket = soup.find("input", type="hidden").get("value")
        payload = {
            "telnum": self.telnum,
            "password": self.password,
            "ticket": ticket
        }
        session.post("https://id.my.softbank.jp/sbid_auth/type1/2.0/login.php", data=payload)
        return session

    def _move_data_management(self):
        session = self._login()
        r = session.get("https://my.softbank.jp/msb/d/webLink/doSend/MRERE0000")
        soup = BeautifulSoup(r.text, "lxml")
        auth_token = soup.find_all("input")
        payload = {
            "mfiv": auth_token[0].get("value"),
            "mfsb": auth_token[1].get("value"),
        }
        return session.post("https://re11.my.softbank.jp/resfe/top/", data=payload)

    def get_data(self):
        req_data = self._move_data_management()
        pie_chart = re.findall('chartType": {2}"pie",(.+),}]};', req_data.text)[0]
        pie_chart_to_dic = "{" + pie_chart + "}"
        data_dic = ast.literal_eval(pie_chart_to_dic)

        used_data = "0" if data_dic["usedGigaData"] == "" else data_dic["usedGigaData"]
        remain_data = "0" if data_dic["remainData"] == "" else data_dic["remainData"]
        step_remain_data = "0" if data_dic["stepRemainData"] == "" else data_dic["stepRemainData"]
        additional_data = "0" if data_dic["currentAdditionalData"] == "" else data_dic["currentAdditionalData"]
        additional_used_data = "0" if data_dic["currentAdditionalUsedData"] == "" else data_dic["currentAdditionalUsedData"]
        given_data = "0" if data_dic["currentGivenData"] == "" else data_dic["currentGivenData"]
        given_used_data = "0" if data_dic["currentGivenUsedData"] == "" else data_dic["currentGivenUsedData"]

        result_dic = {
            "used_data": float(used_data),
            "remain_data": float(remain_data),
            "step_remain_data": float(step_remain_data),
            "additional_data": float(additional_data),
            "additional_used_data": float(additional_used_data),
            "given_data": float(given_data),
            "given_used_data": float(given_used_data),
        }

        self.data = result_dic

        return result_dic

    def send_message(self):

        if not self.data:
            self.data = self.get_data()

        remain = round(self.data["remain_data"], 2)
        total = round(remain + self.data["used_data"], 2)
        rate = round(remain / total * 100, 2)

        text = "\n{}GB / {}GB ({}%)".format(remain, total, rate)
        line_notify_token = self.line_access_token
        line_notify_api = "https://notify-api.line.me/api/notify"
        payload = {"message": text}
        headers = {"Authorization": "Bearer " + line_notify_token}
        line_notify = requests.post(line_notify_api, data=payload, headers=headers)
        return line_notify.status_code
