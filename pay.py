import token
import traceback
import unittest
import requests
import datetime
import time
import json


class test_case(unittest.TestCase):
    '''登录、验签、下单、支付、查询'''

    clientSign = None
    payid = None
    token = None
    user_id = None
    # 登录名
    loginname = '16100161002'
   # 登录密码
    pwd = 'nps0111C88AE04CEC1BA554D03D5B5970333A83585826C2A985DE5520D9E934389EFB84B52D344FB21AA8EA38A4940C8332692B8D4DA' \
          '2393549212EAFDC0F11CA5C9CC86FABB859E4E585CF57B02E7A928C9252403938EEC8D70A7781018F0C90E55FE475BB3881C1734697BFB' \
          'A39F4A92E6727833B72F5B50ED0F4A7522E0F0F9E65nps01'
    # 支付密码
    payPwd = "osCcV0C0putKl8ZnMwoXiIiJnUOyp2Y4UbmfqJk8ft558RE0iaQOjORp7XiLKU2Af0vZedRrr/Os37RaklM+NirARzkzY7/oA/fxbIdv6" \
             "mtSf3uwoRgn5cddgNPMiwJ6cukvH4jBbsrWmG5gkJbxdpGdfmGxGOf0BbB/+k4ESB43i1l7a3zML44NWalx55a9"
    # authcode
    Uepay_Auth = {'Uepay-Auth' : 'b1786828-c84a-4b70-b8f3-af77309f543b'}
    # 十位时间戳
    time2 = int(round(time.time()))
    # print(time1)
    # 十三位时间戳
    time1 = int(round(time.time() * 1000))
    # print(t)
    # 生成不重复订单号
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[
                                                                                -8:]
    # print(order_no)
    def test_scan_01(self):
        '''登录'''
        url = 'http://192.168.0.232:13030/app'
        data = {
            "appVersion": 205,
            "requestType": "50041",
            "arguments": {
                "areaCode": "0086",
                "loginName": test_case.loginname,
                "osType": "android",
                "pwd": test_case.pwd,
                "clientSign": 'b1786828-c84a-4b70-b8f3-af77309f543b'
            },
            "appSource": "android"
        }
        r4 = requests.post(url = url , headers = test_case.Uepay_Auth , json = data)
        print(r4.text)
        dic_info2 = json.loads(r4.text)
        # print(dic_info2)
        self.assertEqual(dic_info2['fault'],False,msg=dic_info2['message'])
        print(dic_info2['message'])
        test_case.token = dic_info2['result']['token']
        test_case.user_id = dic_info2['result']['id']
        # print(test_case.token)
        s = r4.status_code
        assert s==200



    def test_scan_02(self):
        '''验签'''
        url = 'http://192.168.0.22:8113/test/sign.do'
        data = {
            "appSource": "2",
            "appVersion": "1.4",
            "arguments": {
                "amt": "10",
                "notifyUrl": "http://www.uepay.com",
                "cny": "MOP",
                "detail": " { \"goods_detail\": [ { \"goods_name\":\"iPhone6s 16G\", \"quantity\":1, \"price\":555 } ], \"consignee\":\"收貨人\" , \"consignee_address\":\"收貨地址\" } ",
                "orderNo": test_case.order_no,
                "time": test_case.time2,
                "terminal": "WEB",
                "spbillCreateIp": "192.168.200.177",
                "nonceStr": test_case.time1,
                "body": "测试商品"
            },
            "clientSign": "",
            "merchantNo": "000030053310001",
            "requestType": "UNIFIEDORDER",
            "tradeType": "UEPAY_JSAPI"
        }
        r = requests.post(url=url, params={"park": "3315C66DF6265C47BC1BCE401E9C08C9"}, json=data)
        print(r.text)  # 解析返回结果并打印出来
        # print(r1.json())       #josn格式打印出来，适用于返回是json内
        # 把生成的验签拿出来
        dic_info = json.loads(r.text)
        test_case.clientSign = dic_info['clientSign']
        s = r.status_code
        assert s == 200



    def test_scan_03(self):
        # print(test_case.token)
        url1 = 'https://fat.uepay.mo/wallet/unifiedorder'
        data = {
            "appSource": "2",
            "appVersion": "1.4",
            "arguments": {
                "amt": "10",
                "notifyUrl": "http://www.uepay.com",
                "cny": "MOP",
                "detail": " { \"goods_detail\": [ { \"goods_name\":\"iPhone6s 16G\", \"quantity\":1, \"price\":555 } ], \"consignee\":\"收貨人\" , \"consignee_address\":\"收貨地址\" } ",
                "orderNo": test_case.order_no,
                "time": test_case.time2,
                "terminal": "WEB",
                "spbillCreateIp": "192.168.200.177",
                "nonceStr": test_case.time1,
                "body": "测试商品"
            },
            "clientSign": test_case.clientSign,
            "merchantNo": "000030053310001",
            "requestType": "UNIFIEDORDER",
            "tradeType": "UEPAY_JSAPI"
        }
        r1 = requests.post(url=url1, json=data)
        # print(r1.text)
        dic_info1 = json.loads(r1.text)
        # print(dic_info1)
        test_case.payid = dic_info1['results']['prepayid']
        # print(test_case.payid)
        s = r1.status_code
        assert s==200
        self.assertEqual(dic_info1['result'],'true')
        print(dic_info1['results'])



    def test_scan_04(self):
        url2 = 'http://192.168.0.232:13030/app'
        data2 = {
            "appSource": "ios",
            "appVersion": "2.5.0",
            "arguments":
                {
                    "amount": "1.00",
                    "clientSign": test_case.clientSign,
                    "enable": "amxfj",
                    "payPwd": test_case.payPwd,
                    "payType": "0",
                    "prepayid": test_case.payid,
                    "token": test_case.token,
                    "userId": test_case.user_id
                },
            "requestType": "60003"
        }

        r2 = requests.post(url=url2, headers=test_case.Uepay_Auth, json=data2)
        # print(r2.text)
        dic_info = json.loads(r2.text)
        self.assertEqual(dic_info['fault'],False)
        print(dic_info['message'])
        s = r2.status_code
        assert s==200


    def test_scan_05(self):
        url3 = 'http://192.168.0.232:13030/app'
        data = {
            "appVersion": 206,
            "requestType": "1307",
            "arguments": {
                "pageNo": "1",
                "loginName": test_case.loginname,
                "userId": test_case.user_id,
                "clientSign": test_case.clientSign,
                "token": test_case.token
            },
            "appSource": "android"
        }
        r3 = requests.post(url=url3, headers=test_case.Uepay_Auth , json=data)
        # print(r3.text)
        dic_info = json.loads(r3.text)
        s = r3.status_code
        assert s==200
        self.assertEqual(dic_info['fault'],False,msg=dic_info['fault'])
        print(dic_info['result'][3])


if __name__ == '__main__':
    unittest.main()
