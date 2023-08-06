# py_ctp

ctp risk api for python。支持windows(x86/x64) linux(x64).

#### 示例

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '201/9/13'
"""
import os
import platform
import signal
import sys
import threading
import time

from ctp_risk.ctp_struct import CShfeFtdcRspRiskUserLoginField, CShfeFtdcRspInfoField, CShfeFtdcSequencialTradeField, CShfeFtdcInstrumentField, CShfeFtdcExchangeField
from ctp_risk.ctp_trade import Trade


class Test:

    def __init__(self, addr, out_path, interval_seconds, user, pwd, broker='6000'):
        dllpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ctp_risk', f"lib{'64' if sys.maxsize > 2**32 else '32'}")
        # dllpath = os.path.dirname(os.path.abspath(__file__))  # 所有dll放在程序目录下
        # self.q = Quote(os.path.join(dllpath, 'ctp_quote.' + ('dll' if 'Windows' in platform.system() else 'so')))
        self.t = Trade(os.path.join(dllpath, 'riskapi.' + ('dll' if 'Windows' in platform.system() else 'so')))
        self.req = 0
        self.logined = False
        self.instruments: dict = {}
        self.exc_total: dict = {}
        '''保存交易所统计数据'''
        self.frontAddr = addr
        self.broker = broker
        self.investor = user
        self.pwd = pwd
        self.interval_seconds = int(interval_seconds)
        self.out_path = out_path
        signal.signal(signal.SIGINT, self.single_exit)  # ctrl c
        # signal.signal(signal.SIGTSTP, self.single_exit)  # ctrl z

    def single_exit(self, signal, frame):
        self.t.Release()
        time.sleep(1)
        sys.exit(0)

    def OnConnected(self):
        print('connected')
        threading.Thread(target=self.t.ReqRiskUserLogin, args=(self.broker, self.investor, self.pwd)).start()

    def OnDisconnected(self, reason):
        print(reason)
        self.logined = False

    def OnRspUserLogin(self, pRspRiskUserLogin: CShfeFtdcRspRiskUserLoginField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print(f'== login == {pRspInfo.__dict__}')

        if pRspInfo.getErrorID() == 0:
            self.logined = True
            t = threading.Thread(target=self.show)
            t.setDaemon(True)
            t.start()
            self.t.ReqSubscribeTrade()

    def OnInstrument(self, inst: CShfeFtdcInstrumentField):
        self.instruments[inst.getInstrumentID()] = inst

    def OnExchange(self, exc: CShfeFtdcExchangeField):
        self.exc_total[exc.getExchangeID()] = {'volume': 0, 'turnover': 0}

    def OnTrade(self, pSequencialTrade: CShfeFtdcSequencialTradeField):
        # print(f'== trade == {pSequencialTrade.__dict__}')
        inst: CShfeFtdcInstrumentField = self.instruments[pSequencialTrade.getInstrumentID()]
        self.exc_total[pSequencialTrade.getExchangeID()]['volume'] += pSequencialTrade.getVolume()
        self.exc_total[pSequencialTrade.getExchangeID()]['turnover'] += pSequencialTrade.getPrice() * pSequencialTrade.getVolume() * inst.getVolumeMultiple()

    def show(self):
        while self.logined:
            # print(self.exc_total)
            with open(os.path.join(self.out_path, 'total.txt'), 'w', encoding='utf-8') as f:
                line = ''
                for k, v in self.exc_total.items():
                    line += f"{k},{v['volume']},{v['turnover']}\n"
                f.write(line)
            time.sleep(self.interval_seconds)

    def Run(self):
        # CreateApi时会用到log目录,需要在程序目录下创建**而非dll下**
        self.t.CreateApi()
        spi = self.t.CreateSpi()
        self.t.RegisterSpi(spi)

        self.t.OnFrontConnected = self.OnConnected
        # self.t.OnFrontDisconnected = self.OnDisconnected
        # self.t.OnRspRiskUserLogin = self.OnRspUserLogin
        #
        # self.t.OnRtnSequencialTrade = self.OnTrade
        # '''成交信息'''
        #
        # # 以下为自动推送的响应
        # self.t.OnRtnInstrument = self.OnInstrument
        # self.t.OnRtnExchange = self.OnExchange
        # self.t.OnRtnProduct = lambda x: None
        # '''交易所'''
        # self.t.OnRtnTradingCode = lambda x: None
        # '''交易编码回报'''
        # self.t.OnRtnRiskSyncAccount = lambda x: None
        # '''帐户信息'''
        # self.t.OnRtnTimeSync = lambda x: None
        # '''服务器时间'''
        # self.t.OnRtnRiskDepthMarketData = lambda x: None
        # '''实时行情'''
        # self.t.OnRtnDepartment = lambda x: None
        # '''部门'''
        # self.t.OnRtnInvestorSumInfo = lambda x: None
        # '''投资者总数'''
        # self.t.OnRtnNoticeToken = lambda x: None
        # '''模板替换字段回报'''
        # self.t.OnRtnNoticePattern = lambda x: None
        # '''通知模板回报'''
        # self.t.OnRtnRiskParamInfo = lambda x: None
        # '''风控参数信息回报'''
        # self.t.OnRtnRiskInvestorParam = lambda x: None
        # '''投资者参数回报'''
        # self.t.OnRtnInvestorPattern = lambda x: None
        # '''投资者通知模板回报'''
        # self.t.OnRtnRiskNotifyToken = lambda x: None
        # '''风险通知模板自动替换字段回报'''
        # self.t.OnRtnClientSGDataSyncStart = lambda x: None
        # '''客户端结算组数据同步开始'''
        # self.t.OnRtnClientSGDataSyncEnd = lambda x: None
        # '''客户端结算组数据同步结束'''
        # self.t.OnRtnRiskPattern = lambda x: None
        # '''风控通知模板回报'''
        # self.t.OnRtnTradeParam = lambda x: None
        # '''交易系统参数'''
        # self.t.OnRtnProductExchangeRate = lambda x: None
        # '''产品报价汇率信息'''
        # self.t.OnRtnRiskUserFunction = lambda x: None  # print(x)
        # '''风控用户权限回报'''

        self.t.RegCB()

        self.t.RegisterFront(self.frontAddr)
        self.t.Init()
        # self.t.Join()
        time.sleep(5)


if __name__ == '__main__':
    # path = os.path.dirname(os.path.abspath(__file__))
    # shutil.copy(path + '/dll/ctp_trade.dll', path + '/py_ctp/lib/ctp_trade.dll')

    a = sys.argv[1] if len(sys.argv) > 1 else 'tcp://222.68.181.130:50001'
    o = sys.argv[2] if len(sys.argv) > 2 else './'
    s = sys.argv[3] if len(sys.argv) > 3 else 10
    user = 'your investorid'
    pwd = 'your password'
    t = Test(addr=a, out_path=o, interval_seconds=s, user=user, pwd=pwd)
    t.Run()
    print('presess ctrl+c to exit')
    while True:
        pass
```