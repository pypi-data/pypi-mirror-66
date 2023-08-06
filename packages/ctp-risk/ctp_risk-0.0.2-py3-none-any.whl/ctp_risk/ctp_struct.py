#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '2018/12/10'


from ctypes import *
from .ctp_enum import *

class  CShfeFtdcDisseminationField(Structure):
    """信息分发"""
    _fields_ = [
        ("SequenceSeries", c_short),
        ("SequenceNo", c_int32),
    ]

    def getSequenceSeries(self):
        '''序列系列号'''
        return self.SequenceSeries

    def getSequenceNo(self):
        '''序列号'''
        return self.SequenceNo

    @property
    def __str__(self):
        return f"'SequenceSeries'={self.getSequenceSeries()}, 'SequenceNo'={self.getSequenceNo()}"

    @property
    def __dict__(self):
        return {'SequenceSeries': self.getSequenceSeries(), 'SequenceNo': self.getSequenceNo()}


class  CShfeFtdcReqUserLoginField(Structure):
    """用户登录请求"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("Password", c_char*41),
        ("UserProductInfo", c_char*11),
        ("InterfaceProductInfo", c_char*11),
        ("ProtocolInfo", c_char*11),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    def getUserProductInfo(self):
        '''用户端产品信息'''
        return str(self.UserProductInfo, 'GBK')

    def getInterfaceProductInfo(self):
        '''接口端产品信息'''
        return str(self.InterfaceProductInfo, 'GBK')

    def getProtocolInfo(self):
        '''协议信息'''
        return str(self.ProtocolInfo, 'GBK')

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'Password'={self.getPassword()}, 'UserProductInfo'={self.getUserProductInfo()}, 'InterfaceProductInfo'={self.getInterfaceProductInfo()}, 'ProtocolInfo'={self.getProtocolInfo()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'Password': self.getPassword(), 'UserProductInfo': self.getUserProductInfo(), 'InterfaceProductInfo': self.getInterfaceProductInfo(), 'ProtocolInfo': self.getProtocolInfo()}


class  CShfeFtdcRspUserLoginField(Structure):
    """用户登录应答"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("LoginTime", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("SystemName", c_char*41),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("MaxOrderRef", c_char*13),
        ("SHFETime", c_char*9),
        ("DCETime", c_char*9),
        ("CZCETime", c_char*9),
        ("FFEXTime", c_char*9),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getLoginTime(self):
        '''登录成功时间'''
        return str(self.LoginTime, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getSystemName(self):
        '''交易系统名称'''
        return str(self.SystemName, 'GBK')

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getMaxOrderRef(self):
        '''最大报单引用'''
        return str(self.MaxOrderRef, 'GBK')

    def getSHFETime(self):
        '''上期所时间'''
        return str(self.SHFETime, 'GBK')

    def getDCETime(self):
        '''大商所时间'''
        return str(self.DCETime, 'GBK')

    def getCZCETime(self):
        '''郑商所时间'''
        return str(self.CZCETime, 'GBK')

    def getFFEXTime(self):
        '''中金所时间'''
        return str(self.FFEXTime, 'GBK')

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'LoginTime'={self.getLoginTime()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'SystemName'={self.getSystemName()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'MaxOrderRef'={self.getMaxOrderRef()}, 'SHFETime'={self.getSHFETime()}, 'DCETime'={self.getDCETime()}, 'CZCETime'={self.getCZCETime()}, 'FFEXTime'={self.getFFEXTime()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'LoginTime': self.getLoginTime(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'SystemName': self.getSystemName(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'MaxOrderRef': self.getMaxOrderRef(), 'SHFETime': self.getSHFETime(), 'DCETime': self.getDCETime(), 'CZCETime': self.getCZCETime(), 'FFEXTime': self.getFFEXTime()}


class  CShfeFtdcUserLogoutField(Structure):
    """用户登出请求"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID()}


class  CShfeFtdcForceUserLogoutField(Structure):
    """强制交易员退出"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID()}


class  CShfeFtdcTransferHeaderField(Structure):
    """银期转帐报文头"""
    _fields_ = [
        ("Version", c_char*4),
        ("TradeCode", c_char*7),
        ("TradeDate", c_char*9),
        ("TradeTime", c_char*9),
        ("TradeSerial", c_char*9),
        ("FutureID", c_char*11),
        ("BankID", c_char*4),
        ("BankBrchID", c_char*5),
        ("OperNo", c_char*17),
        ("DeviceID", c_char*3),
        ("RecordNum", c_char*7),
        ("SessionID", c_int32),
        ("RequestID", c_int32),
    ]

    def getVersion(self):
        '''版本号，常量，1.0'''
        return str(self.Version, 'GBK')

    def getTradeCode(self):
        '''交易代码，必填'''
        return str(self.TradeCode, 'GBK')

    def getTradeDate(self):
        '''交易日期，必填，格式：yyyymmdd'''
        return str(self.TradeDate, 'GBK')

    def getTradeTime(self):
        '''交易时间，必填，格式：hhmmss'''
        return str(self.TradeTime, 'GBK')

    def getTradeSerial(self):
        '''发起方流水号，N/A'''
        return str(self.TradeSerial, 'GBK')

    def getFutureID(self):
        '''期货公司代码，必填'''
        return str(self.FutureID, 'GBK')

    def getBankID(self):
        '''银行代码，根据查询银行得到，必填'''
        return str(self.BankID, 'GBK')

    def getBankBrchID(self):
        '''银行分中心代码，根据查询银行得到，必填'''
        return str(self.BankBrchID, 'GBK')

    def getOperNo(self):
        '''操作员，N/A'''
        return str(self.OperNo, 'GBK')

    def getDeviceID(self):
        '''交易设备类型，N/A'''
        return str(self.DeviceID, 'GBK')

    def getRecordNum(self):
        '''记录数，N/A'''
        return str(self.RecordNum, 'GBK')

    def getSessionID(self):
        '''会话编号，N/A'''
        return self.SessionID

    def getRequestID(self):
        '''请求编号，N/A'''
        return self.RequestID

    @property
    def __str__(self):
        return f"'Version'={self.getVersion()}, 'TradeCode'={self.getTradeCode()}, 'TradeDate'={self.getTradeDate()}, 'TradeTime'={self.getTradeTime()}, 'TradeSerial'={self.getTradeSerial()}, 'FutureID'={self.getFutureID()}, 'BankID'={self.getBankID()}, 'BankBrchID'={self.getBankBrchID()}, 'OperNo'={self.getOperNo()}, 'DeviceID'={self.getDeviceID()}, 'RecordNum'={self.getRecordNum()}, 'SessionID'={self.getSessionID()}, 'RequestID'={self.getRequestID()}"

    @property
    def __dict__(self):
        return {'Version': self.getVersion(), 'TradeCode': self.getTradeCode(), 'TradeDate': self.getTradeDate(), 'TradeTime': self.getTradeTime(), 'TradeSerial': self.getTradeSerial(), 'FutureID': self.getFutureID(), 'BankID': self.getBankID(), 'BankBrchID': self.getBankBrchID(), 'OperNo': self.getOperNo(), 'DeviceID': self.getDeviceID(), 'RecordNum': self.getRecordNum(), 'SessionID': self.getSessionID(), 'RequestID': self.getRequestID()}


class  CShfeFtdcTransferBankToFutureReqField(Structure):
    """银行资金转期货请求，TradeCode=202001"""
    _fields_ = [
        ("FutureAccount", c_char*13),
        ("FuturePwdFlag", c_char),
        ("FutureAccPwd", c_char*17),
        ("TradeAmt", c_double),
        ("CustFee", c_double),
        ("CurrencyCode", c_char*4),
    ]

    def getFutureAccount(self):
        '''期货资金账户'''
        return str(self.FutureAccount, 'GBK')

    def getFuturePwdFlag(self):
        '''密码标志'''
        return TShfeFtdcFuturePwdFlagType(ord(self.FuturePwdFlag))

    def getFutureAccPwd(self):
        '''密码'''
        return str(self.FutureAccPwd, 'GBK')

    def getTradeAmt(self):
        '''转账金额'''
        return self.TradeAmt

    def getCustFee(self):
        '''客户手续费'''
        return self.CustFee

    def getCurrencyCode(self):
        '''币种：RMB-人民币 USD-美圆 HKD-港元'''
        return str(self.CurrencyCode, 'GBK')

    @property
    def __str__(self):
        return f"'FutureAccount'={self.getFutureAccount()}, 'FuturePwdFlag'={self.getFuturePwdFlag()}, 'FutureAccPwd'={self.getFutureAccPwd()}, 'TradeAmt'={self.getTradeAmt()}, 'CustFee'={self.getCustFee()}, 'CurrencyCode'={self.getCurrencyCode()}"

    @property
    def __dict__(self):
        return {'FutureAccount': self.getFutureAccount(), 'FuturePwdFlag': self.getFuturePwdFlag(), 'FutureAccPwd': self.getFutureAccPwd(), 'TradeAmt': self.getTradeAmt(), 'CustFee': self.getCustFee(), 'CurrencyCode': self.getCurrencyCode()}


class  CShfeFtdcTransferBankToFutureRspField(Structure):
    """银行资金转期货请求响应"""
    _fields_ = [
        ("RetCode", c_char*5),
        ("RetInfo", c_char*129),
        ("FutureAccount", c_char*13),
        ("TradeAmt", c_double),
        ("CustFee", c_double),
        ("CurrencyCode", c_char*4),
    ]

    def getRetCode(self):
        '''响应代码'''
        return str(self.RetCode, 'GBK')

    def getRetInfo(self):
        '''响应信息'''
        return str(self.RetInfo, 'GBK')

    def getFutureAccount(self):
        '''资金账户'''
        return str(self.FutureAccount, 'GBK')

    def getTradeAmt(self):
        '''转帐金额'''
        return self.TradeAmt

    def getCustFee(self):
        '''应收客户手续费'''
        return self.CustFee

    def getCurrencyCode(self):
        '''币种'''
        return str(self.CurrencyCode, 'GBK')

    @property
    def __str__(self):
        return f"'RetCode'={self.getRetCode()}, 'RetInfo'={self.getRetInfo()}, 'FutureAccount'={self.getFutureAccount()}, 'TradeAmt'={self.getTradeAmt()}, 'CustFee'={self.getCustFee()}, 'CurrencyCode'={self.getCurrencyCode()}"

    @property
    def __dict__(self):
        return {'RetCode': self.getRetCode(), 'RetInfo': self.getRetInfo(), 'FutureAccount': self.getFutureAccount(), 'TradeAmt': self.getTradeAmt(), 'CustFee': self.getCustFee(), 'CurrencyCode': self.getCurrencyCode()}


class  CShfeFtdcTransferFutureToBankReqField(Structure):
    """期货资金转银行请求，TradeCode=202002"""
    _fields_ = [
        ("FutureAccount", c_char*13),
        ("FuturePwdFlag", c_char),
        ("FutureAccPwd", c_char*17),
        ("TradeAmt", c_double),
        ("CustFee", c_double),
        ("CurrencyCode", c_char*4),
    ]

    def getFutureAccount(self):
        '''期货资金账户'''
        return str(self.FutureAccount, 'GBK')

    def getFuturePwdFlag(self):
        '''密码标志'''
        return TShfeFtdcFuturePwdFlagType(ord(self.FuturePwdFlag))

    def getFutureAccPwd(self):
        '''密码'''
        return str(self.FutureAccPwd, 'GBK')

    def getTradeAmt(self):
        '''转账金额'''
        return self.TradeAmt

    def getCustFee(self):
        '''客户手续费'''
        return self.CustFee

    def getCurrencyCode(self):
        '''币种：RMB-人民币 USD-美圆 HKD-港元'''
        return str(self.CurrencyCode, 'GBK')

    @property
    def __str__(self):
        return f"'FutureAccount'={self.getFutureAccount()}, 'FuturePwdFlag'={self.getFuturePwdFlag()}, 'FutureAccPwd'={self.getFutureAccPwd()}, 'TradeAmt'={self.getTradeAmt()}, 'CustFee'={self.getCustFee()}, 'CurrencyCode'={self.getCurrencyCode()}"

    @property
    def __dict__(self):
        return {'FutureAccount': self.getFutureAccount(), 'FuturePwdFlag': self.getFuturePwdFlag(), 'FutureAccPwd': self.getFutureAccPwd(), 'TradeAmt': self.getTradeAmt(), 'CustFee': self.getCustFee(), 'CurrencyCode': self.getCurrencyCode()}


class  CShfeFtdcTransferFutureToBankRspField(Structure):
    """期货资金转银行请求响应"""
    _fields_ = [
        ("RetCode", c_char*5),
        ("RetInfo", c_char*129),
        ("FutureAccount", c_char*13),
        ("TradeAmt", c_double),
        ("CustFee", c_double),
        ("CurrencyCode", c_char*4),
    ]

    def getRetCode(self):
        '''响应代码'''
        return str(self.RetCode, 'GBK')

    def getRetInfo(self):
        '''响应信息'''
        return str(self.RetInfo, 'GBK')

    def getFutureAccount(self):
        '''资金账户'''
        return str(self.FutureAccount, 'GBK')

    def getTradeAmt(self):
        '''转帐金额'''
        return self.TradeAmt

    def getCustFee(self):
        '''应收客户手续费'''
        return self.CustFee

    def getCurrencyCode(self):
        '''币种'''
        return str(self.CurrencyCode, 'GBK')

    @property
    def __str__(self):
        return f"'RetCode'={self.getRetCode()}, 'RetInfo'={self.getRetInfo()}, 'FutureAccount'={self.getFutureAccount()}, 'TradeAmt'={self.getTradeAmt()}, 'CustFee'={self.getCustFee()}, 'CurrencyCode'={self.getCurrencyCode()}"

    @property
    def __dict__(self):
        return {'RetCode': self.getRetCode(), 'RetInfo': self.getRetInfo(), 'FutureAccount': self.getFutureAccount(), 'TradeAmt': self.getTradeAmt(), 'CustFee': self.getCustFee(), 'CurrencyCode': self.getCurrencyCode()}


class  CShfeFtdcTransferQryBankReqField(Structure):
    """查询银行资金请求，TradeCode=204002"""
    _fields_ = [
        ("FutureAccount", c_char*13),
        ("FuturePwdFlag", c_char),
        ("FutureAccPwd", c_char*17),
        ("CurrencyCode", c_char*4),
    ]

    def getFutureAccount(self):
        '''期货资金账户'''
        return str(self.FutureAccount, 'GBK')

    def getFuturePwdFlag(self):
        '''密码标志'''
        return TShfeFtdcFuturePwdFlagType(ord(self.FuturePwdFlag))

    def getFutureAccPwd(self):
        '''密码'''
        return str(self.FutureAccPwd, 'GBK')

    def getCurrencyCode(self):
        '''币种：RMB-人民币 USD-美圆 HKD-港元'''
        return str(self.CurrencyCode, 'GBK')

    @property
    def __str__(self):
        return f"'FutureAccount'={self.getFutureAccount()}, 'FuturePwdFlag'={self.getFuturePwdFlag()}, 'FutureAccPwd'={self.getFutureAccPwd()}, 'CurrencyCode'={self.getCurrencyCode()}"

    @property
    def __dict__(self):
        return {'FutureAccount': self.getFutureAccount(), 'FuturePwdFlag': self.getFuturePwdFlag(), 'FutureAccPwd': self.getFutureAccPwd(), 'CurrencyCode': self.getCurrencyCode()}


class  CShfeFtdcTransferQryBankRspField(Structure):
    """查询银行资金请求响应"""
    _fields_ = [
        ("RetCode", c_char*5),
        ("RetInfo", c_char*129),
        ("FutureAccount", c_char*13),
        ("TradeAmt", c_double),
        ("UseAmt", c_double),
        ("FetchAmt", c_double),
        ("CurrencyCode", c_char*4),
    ]

    def getRetCode(self):
        '''响应代码'''
        return str(self.RetCode, 'GBK')

    def getRetInfo(self):
        '''响应信息'''
        return str(self.RetInfo, 'GBK')

    def getFutureAccount(self):
        '''资金账户'''
        return str(self.FutureAccount, 'GBK')

    def getTradeAmt(self):
        '''银行余额'''
        return self.TradeAmt

    def getUseAmt(self):
        '''银行可用余额'''
        return self.UseAmt

    def getFetchAmt(self):
        '''银行可取余额'''
        return self.FetchAmt

    def getCurrencyCode(self):
        '''币种'''
        return str(self.CurrencyCode, 'GBK')

    @property
    def __str__(self):
        return f"'RetCode'={self.getRetCode()}, 'RetInfo'={self.getRetInfo()}, 'FutureAccount'={self.getFutureAccount()}, 'TradeAmt'={self.getTradeAmt()}, 'UseAmt'={self.getUseAmt()}, 'FetchAmt'={self.getFetchAmt()}, 'CurrencyCode'={self.getCurrencyCode()}"

    @property
    def __dict__(self):
        return {'RetCode': self.getRetCode(), 'RetInfo': self.getRetInfo(), 'FutureAccount': self.getFutureAccount(), 'TradeAmt': self.getTradeAmt(), 'UseAmt': self.getUseAmt(), 'FetchAmt': self.getFetchAmt(), 'CurrencyCode': self.getCurrencyCode()}


class  CShfeFtdcTransferQryDetailReqField(Structure):
    """查询银行交易明细请求，TradeCode=204999"""
    _fields_ = [
        ("FutureAccount", c_char*13),
    ]

    def getFutureAccount(self):
        '''期货资金账户'''
        return str(self.FutureAccount, 'GBK')

    @property
    def __str__(self):
        return f"'FutureAccount'={self.getFutureAccount()}"

    @property
    def __dict__(self):
        return {'FutureAccount': self.getFutureAccount()}


class  CShfeFtdcTransferQryDetailRspField(Structure):
    """查询银行交易明细请求响应"""
    _fields_ = [
        ("TradeDate", c_char*9),
        ("TradeTime", c_char*9),
        ("TradeCode", c_char*7),
        ("FutureSerial", c_int32),
        ("FutureID", c_char*11),
        ("FutureAccount", c_char*22),
        ("BankSerial", c_int32),
        ("BankID", c_char*4),
        ("BankBrchID", c_char*5),
        ("BankAccount", c_char*41),
        ("CertCode", c_char*21),
        ("CurrencyCode", c_char*4),
        ("TxAmount", c_double),
        ("Flag", c_char),
    ]

    def getTradeDate(self):
        '''交易日期'''
        return str(self.TradeDate, 'GBK')

    def getTradeTime(self):
        '''交易时间'''
        return str(self.TradeTime, 'GBK')

    def getTradeCode(self):
        '''交易代码'''
        return str(self.TradeCode, 'GBK')

    def getFutureSerial(self):
        '''期货流水号'''
        return self.FutureSerial

    def getFutureID(self):
        '''期货公司代码'''
        return str(self.FutureID, 'GBK')

    def getFutureAccount(self):
        '''资金帐号'''
        return str(self.FutureAccount, 'GBK')

    def getBankSerial(self):
        '''银行流水号'''
        return self.BankSerial

    def getBankID(self):
        '''银行代码'''
        return str(self.BankID, 'GBK')

    def getBankBrchID(self):
        '''银行分中心代码'''
        return str(self.BankBrchID, 'GBK')

    def getBankAccount(self):
        '''银行账号'''
        return str(self.BankAccount, 'GBK')

    def getCertCode(self):
        '''证件号码'''
        return str(self.CertCode, 'GBK')

    def getCurrencyCode(self):
        '''货币代码'''
        return str(self.CurrencyCode, 'GBK')

    def getTxAmount(self):
        '''发生金额'''
        return self.TxAmount

    def getFlag(self):
        '''有效标志'''
        return TShfeFtdcTransferValidFlagType(ord(self.Flag))

    @property
    def __str__(self):
        return f"'TradeDate'={self.getTradeDate()}, 'TradeTime'={self.getTradeTime()}, 'TradeCode'={self.getTradeCode()}, 'FutureSerial'={self.getFutureSerial()}, 'FutureID'={self.getFutureID()}, 'FutureAccount'={self.getFutureAccount()}, 'BankSerial'={self.getBankSerial()}, 'BankID'={self.getBankID()}, 'BankBrchID'={self.getBankBrchID()}, 'BankAccount'={self.getBankAccount()}, 'CertCode'={self.getCertCode()}, 'CurrencyCode'={self.getCurrencyCode()}, 'TxAmount'={self.getTxAmount()}, 'Flag'={self.getFlag()}"

    @property
    def __dict__(self):
        return {'TradeDate': self.getTradeDate(), 'TradeTime': self.getTradeTime(), 'TradeCode': self.getTradeCode(), 'FutureSerial': self.getFutureSerial(), 'FutureID': self.getFutureID(), 'FutureAccount': self.getFutureAccount(), 'BankSerial': self.getBankSerial(), 'BankID': self.getBankID(), 'BankBrchID': self.getBankBrchID(), 'BankAccount': self.getBankAccount(), 'CertCode': self.getCertCode(), 'CurrencyCode': self.getCurrencyCode(), 'TxAmount': self.getTxAmount(), 'Flag': self.getFlag()}


class  CShfeFtdcRspInfoField(Structure):
    """响应信息"""
    _fields_ = [
        ("ErrorID", c_int32),
        ("ErrorMsg", c_char*81),
    ]

    def getErrorID(self):
        '''错误代码'''
        return self.ErrorID

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    @property
    def __str__(self):
        return f"'ErrorID'={self.getErrorID()}, 'ErrorMsg'={self.getErrorMsg()}"

    @property
    def __dict__(self):
        return {'ErrorID': self.getErrorID(), 'ErrorMsg': self.getErrorMsg()}


class  CShfeFtdcExchangeField(Structure):
    """交易所"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("ExchangeName", c_char*61),
        ("ExchangeProperty", c_char),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getExchangeName(self):
        '''交易所名称'''
        return str(self.ExchangeName, 'GBK')

    def getExchangeProperty(self):
        '''交易所属性'''
        return TShfeFtdcExchangePropertyType(ord(self.ExchangeProperty))

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'ExchangeName'={self.getExchangeName()}, 'ExchangeProperty'={self.getExchangeProperty()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'ExchangeName': self.getExchangeName(), 'ExchangeProperty': self.getExchangeProperty()}


class  CShfeFtdcProductField(Structure):
    """产品"""
    _fields_ = [
        ("ProductID", c_char*31),
        ("ProductName", c_char*21),
        ("ExchangeID", c_char*9),
        ("ProductClass", c_char),
        ("VolumeMultiple", c_int32),
        ("PriceTick", c_double),
        ("MaxMarketOrderVolume", c_int32),
        ("MinMarketOrderVolume", c_int32),
        ("MaxLimitOrderVolume", c_int32),
        ("MinLimitOrderVolume", c_int32),
        ("PositionType", c_char),
        ("PositionDateType", c_char),
        ("CloseDealType", c_char),
        ("TradeCurrencyID", c_char*4),
        ("MortgageFundUseRange", c_char),
        ("ExchangeProductID", c_char*31),
        ("UnderlyingMultiple", c_double),
    ]

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getProductName(self):
        '''产品名称'''
        return str(self.ProductName, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getProductClass(self):
        '''产品类型'''
        return TShfeFtdcProductClassType(ord(self.ProductClass))

    def getVolumeMultiple(self):
        '''合约数量乘数'''
        return self.VolumeMultiple

    def getPriceTick(self):
        '''最小变动价位'''
        return self.PriceTick

    def getMaxMarketOrderVolume(self):
        '''市价单最大下单量'''
        return self.MaxMarketOrderVolume

    def getMinMarketOrderVolume(self):
        '''市价单最小下单量'''
        return self.MinMarketOrderVolume

    def getMaxLimitOrderVolume(self):
        '''限价单最大下单量'''
        return self.MaxLimitOrderVolume

    def getMinLimitOrderVolume(self):
        '''限价单最小下单量'''
        return self.MinLimitOrderVolume

    def getPositionType(self):
        '''持仓类型'''
        return TShfeFtdcPositionTypeType(ord(self.PositionType))

    def getPositionDateType(self):
        '''持仓日期类型'''
        return TShfeFtdcPositionDateTypeType(ord(self.PositionDateType))

    def getCloseDealType(self):
        '''平仓处理类型'''
        return TShfeFtdcCloseDealTypeType(ord(self.CloseDealType))

    def getTradeCurrencyID(self):
        '''交易币种类型'''
        return str(self.TradeCurrencyID, 'GBK')

    def getMortgageFundUseRange(self):
        '''质押资金可用范围'''
        return TShfeFtdcMortgageFundUseRangeType(ord(self.MortgageFundUseRange))

    def getExchangeProductID(self):
        '''交易所产品代码'''
        return str(self.ExchangeProductID, 'GBK')

    def getUnderlyingMultiple(self):
        '''合约基础商品乘数'''
        return self.UnderlyingMultiple

    @property
    def __str__(self):
        return f"'ProductID'={self.getProductID()}, 'ProductName'={self.getProductName()}, 'ExchangeID'={self.getExchangeID()}, 'ProductClass'={self.getProductClass()}, 'VolumeMultiple'={self.getVolumeMultiple()}, 'PriceTick'={self.getPriceTick()}, 'MaxMarketOrderVolume'={self.getMaxMarketOrderVolume()}, 'MinMarketOrderVolume'={self.getMinMarketOrderVolume()}, 'MaxLimitOrderVolume'={self.getMaxLimitOrderVolume()}, 'MinLimitOrderVolume'={self.getMinLimitOrderVolume()}, 'PositionType'={self.getPositionType()}, 'PositionDateType'={self.getPositionDateType()}, 'CloseDealType'={self.getCloseDealType()}, 'TradeCurrencyID'={self.getTradeCurrencyID()}, 'MortgageFundUseRange'={self.getMortgageFundUseRange()}, 'ExchangeProductID'={self.getExchangeProductID()}, 'UnderlyingMultiple'={self.getUnderlyingMultiple()}"

    @property
    def __dict__(self):
        return {'ProductID': self.getProductID(), 'ProductName': self.getProductName(), 'ExchangeID': self.getExchangeID(), 'ProductClass': self.getProductClass(), 'VolumeMultiple': self.getVolumeMultiple(), 'PriceTick': self.getPriceTick(), 'MaxMarketOrderVolume': self.getMaxMarketOrderVolume(), 'MinMarketOrderVolume': self.getMinMarketOrderVolume(), 'MaxLimitOrderVolume': self.getMaxLimitOrderVolume(), 'MinLimitOrderVolume': self.getMinLimitOrderVolume(), 'PositionType': self.getPositionType(), 'PositionDateType': self.getPositionDateType(), 'CloseDealType': self.getCloseDealType(), 'TradeCurrencyID': self.getTradeCurrencyID(), 'MortgageFundUseRange': self.getMortgageFundUseRange(), 'ExchangeProductID': self.getExchangeProductID(), 'UnderlyingMultiple': self.getUnderlyingMultiple()}


class  CShfeFtdcInstrumentField(Structure):
    """合约"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("InstrumentName", c_char*21),
        ("ExchangeInstID", c_char*31),
        ("ProductID", c_char*31),
        ("ProductClass", c_char),
        ("DeliveryYear", c_int32),
        ("DeliveryMonth", c_int32),
        ("MaxMarketOrderVolume", c_int32),
        ("MinMarketOrderVolume", c_int32),
        ("MaxLimitOrderVolume", c_int32),
        ("MinLimitOrderVolume", c_int32),
        ("VolumeMultiple", c_int32),
        ("PriceTick", c_double),
        ("CreateDate", c_char*9),
        ("OpenDate", c_char*9),
        ("ExpireDate", c_char*9),
        ("StartDelivDate", c_char*9),
        ("EndDelivDate", c_char*9),
        ("InstLifePhase", c_char),
        ("IsTrading", c_int32),
        ("PositionType", c_char),
        ("PositionDateType", c_char),
        ("LongMarginRatio", c_double),
        ("ShortMarginRatio", c_double),
        ("MaxMarginSideAlgorithm", c_char),
        ("UnderlyingInstrID", c_char*31),
        ("StrikePrice", c_double),
        ("OptionsType", c_char),
        ("UnderlyingMultiple", c_double),
        ("CombinationType", c_char),
        ("ProductGroupID", c_char*31),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getInstrumentName(self):
        '''合约名称'''
        return str(self.InstrumentName, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getProductClass(self):
        '''产品类型'''
        return TShfeFtdcProductClassType(ord(self.ProductClass))

    def getDeliveryYear(self):
        '''交割年份'''
        return self.DeliveryYear

    def getDeliveryMonth(self):
        '''交割月'''
        return self.DeliveryMonth

    def getMaxMarketOrderVolume(self):
        '''市价单最大下单量'''
        return self.MaxMarketOrderVolume

    def getMinMarketOrderVolume(self):
        '''市价单最小下单量'''
        return self.MinMarketOrderVolume

    def getMaxLimitOrderVolume(self):
        '''限价单最大下单量'''
        return self.MaxLimitOrderVolume

    def getMinLimitOrderVolume(self):
        '''限价单最小下单量'''
        return self.MinLimitOrderVolume

    def getVolumeMultiple(self):
        '''合约数量乘数'''
        return self.VolumeMultiple

    def getPriceTick(self):
        '''最小变动价位'''
        return self.PriceTick

    def getCreateDate(self):
        '''创建日'''
        return str(self.CreateDate, 'GBK')

    def getOpenDate(self):
        '''上市日'''
        return str(self.OpenDate, 'GBK')

    def getExpireDate(self):
        '''到期日'''
        return str(self.ExpireDate, 'GBK')

    def getStartDelivDate(self):
        '''开始交割日'''
        return str(self.StartDelivDate, 'GBK')

    def getEndDelivDate(self):
        '''结束交割日'''
        return str(self.EndDelivDate, 'GBK')

    def getInstLifePhase(self):
        '''合约生命周期状态'''
        return TShfeFtdcInstLifePhaseType(ord(self.InstLifePhase))

    def getIsTrading(self):
        '''当前是否交易'''
        return self.IsTrading

    def getPositionType(self):
        '''持仓类型'''
        return TShfeFtdcPositionTypeType(ord(self.PositionType))

    def getPositionDateType(self):
        '''持仓日期类型'''
        return TShfeFtdcPositionDateTypeType(ord(self.PositionDateType))

    def getLongMarginRatio(self):
        '''多头保证金率'''
        return self.LongMarginRatio

    def getShortMarginRatio(self):
        '''空头保证金率'''
        return self.ShortMarginRatio

    def getMaxMarginSideAlgorithm(self):
        '''是否使用大额单边保证金算法'''
        return TShfeFtdcMaxMarginSideAlgorithmType(ord(self.MaxMarginSideAlgorithm))

    def getUnderlyingInstrID(self):
        '''基础商品代码'''
        return str(self.UnderlyingInstrID, 'GBK')

    def getStrikePrice(self):
        '''执行价'''
        return self.StrikePrice

    def getOptionsType(self):
        '''期权类型'''
        return TShfeFtdcOptionsTypeType(ord(self.OptionsType))

    def getUnderlyingMultiple(self):
        '''合约基础商品乘数'''
        return self.UnderlyingMultiple

    def getCombinationType(self):
        '''组合类型'''
        return TShfeFtdcCombinationTypeType(ord(self.CombinationType))

    def getProductGroupID(self):
        '''产品组代码'''
        return str(self.ProductGroupID, 'GBK')

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'InstrumentName'={self.getInstrumentName()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'ProductID'={self.getProductID()}, 'ProductClass'={self.getProductClass()}, 'DeliveryYear'={self.getDeliveryYear()}, 'DeliveryMonth'={self.getDeliveryMonth()}, 'MaxMarketOrderVolume'={self.getMaxMarketOrderVolume()}, 'MinMarketOrderVolume'={self.getMinMarketOrderVolume()}, 'MaxLimitOrderVolume'={self.getMaxLimitOrderVolume()}, 'MinLimitOrderVolume'={self.getMinLimitOrderVolume()}, 'VolumeMultiple'={self.getVolumeMultiple()}, 'PriceTick'={self.getPriceTick()}, 'CreateDate'={self.getCreateDate()}, 'OpenDate'={self.getOpenDate()}, 'ExpireDate'={self.getExpireDate()}, 'StartDelivDate'={self.getStartDelivDate()}, 'EndDelivDate'={self.getEndDelivDate()}, 'InstLifePhase'={self.getInstLifePhase()}, 'IsTrading'={self.getIsTrading()}, 'PositionType'={self.getPositionType()}, 'PositionDateType'={self.getPositionDateType()}, 'LongMarginRatio'={self.getLongMarginRatio()}, 'ShortMarginRatio'={self.getShortMarginRatio()}, 'MaxMarginSideAlgorithm'={self.getMaxMarginSideAlgorithm()}, 'UnderlyingInstrID'={self.getUnderlyingInstrID()}, 'StrikePrice'={self.getStrikePrice()}, 'OptionsType'={self.getOptionsType()}, 'UnderlyingMultiple'={self.getUnderlyingMultiple()}, 'CombinationType'={self.getCombinationType()}, 'ProductGroupID'={self.getProductGroupID()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID(), 'InstrumentName': self.getInstrumentName(), 'ExchangeInstID': self.getExchangeInstID(), 'ProductID': self.getProductID(), 'ProductClass': self.getProductClass(), 'DeliveryYear': self.getDeliveryYear(), 'DeliveryMonth': self.getDeliveryMonth(), 'MaxMarketOrderVolume': self.getMaxMarketOrderVolume(), 'MinMarketOrderVolume': self.getMinMarketOrderVolume(), 'MaxLimitOrderVolume': self.getMaxLimitOrderVolume(), 'MinLimitOrderVolume': self.getMinLimitOrderVolume(), 'VolumeMultiple': self.getVolumeMultiple(), 'PriceTick': self.getPriceTick(), 'CreateDate': self.getCreateDate(), 'OpenDate': self.getOpenDate(), 'ExpireDate': self.getExpireDate(), 'StartDelivDate': self.getStartDelivDate(), 'EndDelivDate': self.getEndDelivDate(), 'InstLifePhase': self.getInstLifePhase(), 'IsTrading': self.getIsTrading(), 'PositionType': self.getPositionType(), 'PositionDateType': self.getPositionDateType(), 'LongMarginRatio': self.getLongMarginRatio(), 'ShortMarginRatio': self.getShortMarginRatio(), 'MaxMarginSideAlgorithm': self.getMaxMarginSideAlgorithm(), 'UnderlyingInstrID': self.getUnderlyingInstrID(), 'StrikePrice': self.getStrikePrice(), 'OptionsType': self.getOptionsType(), 'UnderlyingMultiple': self.getUnderlyingMultiple(), 'CombinationType': self.getCombinationType(), 'ProductGroupID': self.getProductGroupID()}


class  CShfeFtdcBrokerField(Structure):
    """经纪公司"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("BrokerAbbr", c_char*9),
        ("BrokerName", c_char*81),
        ("IsActive", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getBrokerAbbr(self):
        '''经纪公司简称'''
        return str(self.BrokerAbbr, 'GBK')

    def getBrokerName(self):
        '''经纪公司名称'''
        return str(self.BrokerName, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'BrokerAbbr'={self.getBrokerAbbr()}, 'BrokerName'={self.getBrokerName()}, 'IsActive'={self.getIsActive()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'BrokerAbbr': self.getBrokerAbbr(), 'BrokerName': self.getBrokerName(), 'IsActive': self.getIsActive()}


class  CShfeFtdcTraderField(Structure):
    """交易所交易员"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("TraderID", c_char*21),
        ("ParticipantID", c_char*11),
        ("Password", c_char*41),
        ("InstallCount", c_int32),
        ("BrokerID", c_char*11),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    def getInstallCount(self):
        '''安装数量'''
        return self.InstallCount

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'TraderID'={self.getTraderID()}, 'ParticipantID'={self.getParticipantID()}, 'Password'={self.getPassword()}, 'InstallCount'={self.getInstallCount()}, 'BrokerID'={self.getBrokerID()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'TraderID': self.getTraderID(), 'ParticipantID': self.getParticipantID(), 'Password': self.getPassword(), 'InstallCount': self.getInstallCount(), 'BrokerID': self.getBrokerID()}


class  CShfeFtdcInvestorField(Structure):
    """投资者"""
    _fields_ = [
        ("InvestorID", c_char*13),
        ("BrokerID", c_char*11),
        ("InvestorGroupID", c_char*13),
        ("InvestorName", c_char*81),
        ("IdentifiedCardType", c_char),
        ("IdentifiedCardNo", c_char*51),
        ("IsActive", c_int32),
        ("Telephone", c_char*41),
        ("Address", c_char*101),
        ("OpenDate", c_char*9),
        ("Mobile", c_char*41),
        ("CommModelID", c_char*13),
        ("MarginModelID", c_char*13),
    ]

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorGroupID(self):
        '''投资者分组代码'''
        return str(self.InvestorGroupID, 'GBK')

    def getInvestorName(self):
        '''投资者名称'''
        return str(self.InvestorName, 'GBK')

    def getIdentifiedCardType(self):
        '''证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.IdentifiedCardType))

    def getIdentifiedCardNo(self):
        '''证件号码'''
        return str(self.IdentifiedCardNo, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    def getTelephone(self):
        '''联系电话'''
        return str(self.Telephone, 'GBK')

    def getAddress(self):
        '''通讯地址'''
        return str(self.Address, 'GBK')

    def getOpenDate(self):
        '''开户日期'''
        return str(self.OpenDate, 'GBK')

    def getMobile(self):
        '''手机'''
        return str(self.Mobile, 'GBK')

    def getCommModelID(self):
        '''手续费率模板代码'''
        return str(self.CommModelID, 'GBK')

    def getMarginModelID(self):
        '''保证金率模板代码'''
        return str(self.MarginModelID, 'GBK')

    @property
    def __str__(self):
        return f"'InvestorID'={self.getInvestorID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorGroupID'={self.getInvestorGroupID()}, 'InvestorName'={self.getInvestorName()}, 'IdentifiedCardType'={self.getIdentifiedCardType()}, 'IdentifiedCardNo'={self.getIdentifiedCardNo()}, 'IsActive'={self.getIsActive()}, 'Telephone'={self.getTelephone()}, 'Address'={self.getAddress()}, 'OpenDate'={self.getOpenDate()}, 'Mobile'={self.getMobile()}, 'CommModelID'={self.getCommModelID()}, 'MarginModelID'={self.getMarginModelID()}"

    @property
    def __dict__(self):
        return {'InvestorID': self.getInvestorID(), 'BrokerID': self.getBrokerID(), 'InvestorGroupID': self.getInvestorGroupID(), 'InvestorName': self.getInvestorName(), 'IdentifiedCardType': self.getIdentifiedCardType(), 'IdentifiedCardNo': self.getIdentifiedCardNo(), 'IsActive': self.getIsActive(), 'Telephone': self.getTelephone(), 'Address': self.getAddress(), 'OpenDate': self.getOpenDate(), 'Mobile': self.getMobile(), 'CommModelID': self.getCommModelID(), 'MarginModelID': self.getMarginModelID()}


class  CShfeFtdcTradingCodeField(Structure):
    """交易编码"""
    _fields_ = [
        ("InvestorID", c_char*13),
        ("BrokerID", c_char*11),
        ("ExchangeID", c_char*9),
        ("ClientID", c_char*11),
        ("IsActive", c_int32),
        ("ClientIDType", c_char),
    ]

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    def getClientIDType(self):
        '''交易编码类型'''
        return TShfeFtdcClientIDTypeType(ord(self.ClientIDType))

    @property
    def __str__(self):
        return f"'InvestorID'={self.getInvestorID()}, 'BrokerID'={self.getBrokerID()}, 'ExchangeID'={self.getExchangeID()}, 'ClientID'={self.getClientID()}, 'IsActive'={self.getIsActive()}, 'ClientIDType'={self.getClientIDType()}"

    @property
    def __dict__(self):
        return {'InvestorID': self.getInvestorID(), 'BrokerID': self.getBrokerID(), 'ExchangeID': self.getExchangeID(), 'ClientID': self.getClientID(), 'IsActive': self.getIsActive(), 'ClientIDType': self.getClientIDType()}


class  CShfeFtdcPartBrokerField(Structure):
    """会员编码和经纪公司编码对照表"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("IsActive", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'IsActive'={self.getIsActive()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'IsActive': self.getIsActive()}


class  CShfeFtdcSuperUserField(Structure):
    """管理用户"""
    _fields_ = [
        ("UserID", c_char*16),
        ("UserName", c_char*81),
        ("Password", c_char*41),
        ("IsActive", c_int32),
    ]

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getUserName(self):
        '''用户名称'''
        return str(self.UserName, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    @property
    def __str__(self):
        return f"'UserID'={self.getUserID()}, 'UserName'={self.getUserName()}, 'Password'={self.getPassword()}, 'IsActive'={self.getIsActive()}"

    @property
    def __dict__(self):
        return {'UserID': self.getUserID(), 'UserName': self.getUserName(), 'Password': self.getPassword(), 'IsActive': self.getIsActive()}


class  CShfeFtdcSuperUserFunctionField(Structure):
    """管理用户功能权限"""
    _fields_ = [
        ("UserID", c_char*16),
        ("FunctionCode", c_char),
    ]

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getFunctionCode(self):
        '''功能代码'''
        return TShfeFtdcFunctionCodeType(ord(self.FunctionCode))

    @property
    def __str__(self):
        return f"'UserID'={self.getUserID()}, 'FunctionCode'={self.getFunctionCode()}"

    @property
    def __dict__(self):
        return {'UserID': self.getUserID(), 'FunctionCode': self.getFunctionCode()}


class  CShfeFtdcInvestorGroupField(Structure):
    """投资者组"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorGroupID", c_char*13),
        ("InvestorGroupName", c_char*41),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorGroupID(self):
        '''投资者分组代码'''
        return str(self.InvestorGroupID, 'GBK')

    def getInvestorGroupName(self):
        '''投资者分组名称'''
        return str(self.InvestorGroupName, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorGroupID'={self.getInvestorGroupID()}, 'InvestorGroupName'={self.getInvestorGroupName()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorGroupID': self.getInvestorGroupID(), 'InvestorGroupName': self.getInvestorGroupName()}


class  CShfeFtdcTradingAccountField(Structure):
    """资金账户"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("AccountID", c_char*13),
        ("PreMortgage", c_double),
        ("PreCredit", c_double),
        ("PreDeposit", c_double),
        ("PreBalance", c_double),
        ("PreMargin", c_double),
        ("InterestBase", c_double),
        ("Interest", c_double),
        ("Deposit", c_double),
        ("Withdraw", c_double),
        ("FrozenMargin", c_double),
        ("FrozenCash", c_double),
        ("FrozenCommission", c_double),
        ("CurrMargin", c_double),
        ("CashIn", c_double),
        ("Commission", c_double),
        ("CloseProfit", c_double),
        ("PositionProfit", c_double),
        ("Balance", c_double),
        ("Available", c_double),
        ("WithdrawQuota", c_double),
        ("Reserve", c_double),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("Credit", c_double),
        ("Mortgage", c_double),
        ("ExchangeMargin", c_double),
        ("DeliveryMargin", c_double),
        ("ExchangeDeliveryMargin", c_double),
        ("ReserveBalance", c_double),
        ("CurrencyID", c_char*4),
        ("PreFundMortgageIn", c_double),
        ("PreFundMortgageOut", c_double),
        ("FundMortgageIn", c_double),
        ("FundMortgageOut", c_double),
        ("FundMortgageAvailable", c_double),
        ("MortgageableFund", c_double),
        ("SpecProductMargin", c_double),
        ("SpecProductFrozenMargin", c_double),
        ("SpecProductCommission", c_double),
        ("SpecProductFrozenCommission", c_double),
        ("SpecProductPositionProfit", c_double),
        ("SpecProductCloseProfit", c_double),
        ("SpecProductPositionProfitByAlg", c_double),
        ("SpecProductExchangeMargin", c_double),
        ("FrozenSwap", c_double),
        ("RemainSwap", c_double),
        ("OptionCloseProfit", c_double),
        ("OptionValue", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getPreMortgage(self):
        '''上次质押金额'''
        return self.PreMortgage

    def getPreCredit(self):
        '''上次信用额度'''
        return self.PreCredit

    def getPreDeposit(self):
        '''上次存款额'''
        return self.PreDeposit

    def getPreBalance(self):
        '''上次结算准备金'''
        return self.PreBalance

    def getPreMargin(self):
        '''上次占用的保证金'''
        return self.PreMargin

    def getInterestBase(self):
        '''利息基数'''
        return self.InterestBase

    def getInterest(self):
        '''利息收入'''
        return self.Interest

    def getDeposit(self):
        '''入金金额'''
        return self.Deposit

    def getWithdraw(self):
        '''出金金额'''
        return self.Withdraw

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCurrMargin(self):
        '''当前保证金总额'''
        return self.CurrMargin

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getBalance(self):
        '''期货结算准备金'''
        return self.Balance

    def getAvailable(self):
        '''可用资金'''
        return self.Available

    def getWithdrawQuota(self):
        '''可取资金'''
        return self.WithdrawQuota

    def getReserve(self):
        '''基本准备金'''
        return self.Reserve

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getCredit(self):
        '''信用额度'''
        return self.Credit

    def getMortgage(self):
        '''质押金额'''
        return self.Mortgage

    def getExchangeMargin(self):
        '''交易所保证金'''
        return self.ExchangeMargin

    def getDeliveryMargin(self):
        '''投资者交割保证金'''
        return self.DeliveryMargin

    def getExchangeDeliveryMargin(self):
        '''交易所交割保证金'''
        return self.ExchangeDeliveryMargin

    def getReserveBalance(self):
        '''保底期货结算准备金'''
        return self.ReserveBalance

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getPreFundMortgageIn(self):
        '''上次货币质入金额'''
        return self.PreFundMortgageIn

    def getPreFundMortgageOut(self):
        '''上次货币质出金额'''
        return self.PreFundMortgageOut

    def getFundMortgageIn(self):
        '''货币质入金额'''
        return self.FundMortgageIn

    def getFundMortgageOut(self):
        '''货币质出金额'''
        return self.FundMortgageOut

    def getFundMortgageAvailable(self):
        '''货币质押余额'''
        return self.FundMortgageAvailable

    def getMortgageableFund(self):
        '''可质押货币金额'''
        return self.MortgageableFund

    def getSpecProductMargin(self):
        '''特殊产品占用保证金'''
        return self.SpecProductMargin

    def getSpecProductFrozenMargin(self):
        '''特殊产品冻结保证金'''
        return self.SpecProductFrozenMargin

    def getSpecProductCommission(self):
        '''特殊产品手续费'''
        return self.SpecProductCommission

    def getSpecProductFrozenCommission(self):
        '''特殊产品冻结手续费'''
        return self.SpecProductFrozenCommission

    def getSpecProductPositionProfit(self):
        '''特殊产品持仓盈亏'''
        return self.SpecProductPositionProfit

    def getSpecProductCloseProfit(self):
        '''特殊产品平仓盈亏'''
        return self.SpecProductCloseProfit

    def getSpecProductPositionProfitByAlg(self):
        '''根据持仓盈亏算法计算的特殊产品持仓盈亏'''
        return self.SpecProductPositionProfitByAlg

    def getSpecProductExchangeMargin(self):
        '''特殊产品交易所保证金'''
        return self.SpecProductExchangeMargin

    def getFrozenSwap(self):
        '''延时换汇冻结金额'''
        return self.FrozenSwap

    def getRemainSwap(self):
        '''剩余换汇额度'''
        return self.RemainSwap

    def getOptionCloseProfit(self):
        '''期权平仓盈亏'''
        return self.OptionCloseProfit

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'AccountID'={self.getAccountID()}, 'PreMortgage'={self.getPreMortgage()}, 'PreCredit'={self.getPreCredit()}, 'PreDeposit'={self.getPreDeposit()}, 'PreBalance'={self.getPreBalance()}, 'PreMargin'={self.getPreMargin()}, 'InterestBase'={self.getInterestBase()}, 'Interest'={self.getInterest()}, 'Deposit'={self.getDeposit()}, 'Withdraw'={self.getWithdraw()}, 'FrozenMargin'={self.getFrozenMargin()}, 'FrozenCash'={self.getFrozenCash()}, 'FrozenCommission'={self.getFrozenCommission()}, 'CurrMargin'={self.getCurrMargin()}, 'CashIn'={self.getCashIn()}, 'Commission'={self.getCommission()}, 'CloseProfit'={self.getCloseProfit()}, 'PositionProfit'={self.getPositionProfit()}, 'Balance'={self.getBalance()}, 'Available'={self.getAvailable()}, 'WithdrawQuota'={self.getWithdrawQuota()}, 'Reserve'={self.getReserve()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'Credit'={self.getCredit()}, 'Mortgage'={self.getMortgage()}, 'ExchangeMargin'={self.getExchangeMargin()}, 'DeliveryMargin'={self.getDeliveryMargin()}, 'ExchangeDeliveryMargin'={self.getExchangeDeliveryMargin()}, 'ReserveBalance'={self.getReserveBalance()}, 'CurrencyID'={self.getCurrencyID()}, 'PreFundMortgageIn'={self.getPreFundMortgageIn()}, 'PreFundMortgageOut'={self.getPreFundMortgageOut()}, 'FundMortgageIn'={self.getFundMortgageIn()}, 'FundMortgageOut'={self.getFundMortgageOut()}, 'FundMortgageAvailable'={self.getFundMortgageAvailable()}, 'MortgageableFund'={self.getMortgageableFund()}, 'SpecProductMargin'={self.getSpecProductMargin()}, 'SpecProductFrozenMargin'={self.getSpecProductFrozenMargin()}, 'SpecProductCommission'={self.getSpecProductCommission()}, 'SpecProductFrozenCommission'={self.getSpecProductFrozenCommission()}, 'SpecProductPositionProfit'={self.getSpecProductPositionProfit()}, 'SpecProductCloseProfit'={self.getSpecProductCloseProfit()}, 'SpecProductPositionProfitByAlg'={self.getSpecProductPositionProfitByAlg()}, 'SpecProductExchangeMargin'={self.getSpecProductExchangeMargin()}, 'FrozenSwap'={self.getFrozenSwap()}, 'RemainSwap'={self.getRemainSwap()}, 'OptionCloseProfit'={self.getOptionCloseProfit()}, 'OptionValue'={self.getOptionValue()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'AccountID': self.getAccountID(), 'PreMortgage': self.getPreMortgage(), 'PreCredit': self.getPreCredit(), 'PreDeposit': self.getPreDeposit(), 'PreBalance': self.getPreBalance(), 'PreMargin': self.getPreMargin(), 'InterestBase': self.getInterestBase(), 'Interest': self.getInterest(), 'Deposit': self.getDeposit(), 'Withdraw': self.getWithdraw(), 'FrozenMargin': self.getFrozenMargin(), 'FrozenCash': self.getFrozenCash(), 'FrozenCommission': self.getFrozenCommission(), 'CurrMargin': self.getCurrMargin(), 'CashIn': self.getCashIn(), 'Commission': self.getCommission(), 'CloseProfit': self.getCloseProfit(), 'PositionProfit': self.getPositionProfit(), 'Balance': self.getBalance(), 'Available': self.getAvailable(), 'WithdrawQuota': self.getWithdrawQuota(), 'Reserve': self.getReserve(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'Credit': self.getCredit(), 'Mortgage': self.getMortgage(), 'ExchangeMargin': self.getExchangeMargin(), 'DeliveryMargin': self.getDeliveryMargin(), 'ExchangeDeliveryMargin': self.getExchangeDeliveryMargin(), 'ReserveBalance': self.getReserveBalance(), 'CurrencyID': self.getCurrencyID(), 'PreFundMortgageIn': self.getPreFundMortgageIn(), 'PreFundMortgageOut': self.getPreFundMortgageOut(), 'FundMortgageIn': self.getFundMortgageIn(), 'FundMortgageOut': self.getFundMortgageOut(), 'FundMortgageAvailable': self.getFundMortgageAvailable(), 'MortgageableFund': self.getMortgageableFund(), 'SpecProductMargin': self.getSpecProductMargin(), 'SpecProductFrozenMargin': self.getSpecProductFrozenMargin(), 'SpecProductCommission': self.getSpecProductCommission(), 'SpecProductFrozenCommission': self.getSpecProductFrozenCommission(), 'SpecProductPositionProfit': self.getSpecProductPositionProfit(), 'SpecProductCloseProfit': self.getSpecProductCloseProfit(), 'SpecProductPositionProfitByAlg': self.getSpecProductPositionProfitByAlg(), 'SpecProductExchangeMargin': self.getSpecProductExchangeMargin(), 'FrozenSwap': self.getFrozenSwap(), 'RemainSwap': self.getRemainSwap(), 'OptionCloseProfit': self.getOptionCloseProfit(), 'OptionValue': self.getOptionValue()}


class  CShfeFtdcInvestorPositionField(Structure):
    """投资者持仓"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("PosiDirection", c_char),
        ("HedgeFlag", c_char),
        ("PositionDate", c_char),
        ("YdPosition", c_int32),
        ("Position", c_int32),
        ("LongFrozen", c_int32),
        ("ShortFrozen", c_int32),
        ("LongFrozenAmount", c_double),
        ("ShortFrozenAmount", c_double),
        ("OpenVolume", c_int32),
        ("CloseVolume", c_int32),
        ("OpenAmount", c_double),
        ("CloseAmount", c_double),
        ("PositionCost", c_double),
        ("PreMargin", c_double),
        ("UseMargin", c_double),
        ("FrozenMargin", c_double),
        ("FrozenCash", c_double),
        ("FrozenCommission", c_double),
        ("CashIn", c_double),
        ("Commission", c_double),
        ("CloseProfit", c_double),
        ("PositionProfit", c_double),
        ("PreSettlementPrice", c_double),
        ("SettlementPrice", c_double),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("OpenCost", c_double),
        ("ExchangeMargin", c_double),
        ("CombPosition", c_int32),
        ("CombLongFrozen", c_int32),
        ("CombShortFrozen", c_int32),
        ("CloseProfitByDate", c_double),
        ("CloseProfitByTrade", c_double),
        ("TodayPosition", c_int32),
        ("MarginRateByMoney", c_double),
        ("MarginRateByVolume", c_double),
        ("StrikeFrozen", c_int32),
        ("StrikeFrozenAmount", c_double),
        ("AbandonFrozen", c_int32),
        ("ExchangeID", c_char*9),
        ("YdStrikeFrozen", c_int32),
        ("InvestUnitID", c_char*17),
        ("OptionValue", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPosiDirection(self):
        '''持仓多空方向'''
        return TShfeFtdcPosiDirectionType(ord(self.PosiDirection))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPositionDate(self):
        '''持仓日期'''
        return TShfeFtdcPositionDateType(ord(self.PositionDate))

    def getYdPosition(self):
        '''上日持仓'''
        return self.YdPosition

    def getPosition(self):
        '''今日持仓'''
        return self.Position

    def getLongFrozen(self):
        '''多头冻结'''
        return self.LongFrozen

    def getShortFrozen(self):
        '''空头冻结'''
        return self.ShortFrozen

    def getLongFrozenAmount(self):
        '''开仓冻结金额'''
        return self.LongFrozenAmount

    def getShortFrozenAmount(self):
        '''开仓冻结金额'''
        return self.ShortFrozenAmount

    def getOpenVolume(self):
        '''开仓量'''
        return self.OpenVolume

    def getCloseVolume(self):
        '''平仓量'''
        return self.CloseVolume

    def getOpenAmount(self):
        '''开仓金额'''
        return self.OpenAmount

    def getCloseAmount(self):
        '''平仓金额'''
        return self.CloseAmount

    def getPositionCost(self):
        '''持仓成本'''
        return self.PositionCost

    def getPreMargin(self):
        '''上次占用的保证金'''
        return self.PreMargin

    def getUseMargin(self):
        '''占用的保证金'''
        return self.UseMargin

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getPreSettlementPrice(self):
        '''上次结算价'''
        return self.PreSettlementPrice

    def getSettlementPrice(self):
        '''本次结算价'''
        return self.SettlementPrice

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getOpenCost(self):
        '''开仓成本'''
        return self.OpenCost

    def getExchangeMargin(self):
        '''交易所保证金'''
        return self.ExchangeMargin

    def getCombPosition(self):
        '''组合成交形成的持仓'''
        return self.CombPosition

    def getCombLongFrozen(self):
        '''组合多头冻结'''
        return self.CombLongFrozen

    def getCombShortFrozen(self):
        '''组合空头冻结'''
        return self.CombShortFrozen

    def getCloseProfitByDate(self):
        '''逐日盯市平仓盈亏'''
        return self.CloseProfitByDate

    def getCloseProfitByTrade(self):
        '''逐笔对冲平仓盈亏'''
        return self.CloseProfitByTrade

    def getTodayPosition(self):
        '''今日持仓'''
        return self.TodayPosition

    def getMarginRateByMoney(self):
        '''保证金率'''
        return self.MarginRateByMoney

    def getMarginRateByVolume(self):
        '''保证金率(按手数)'''
        return self.MarginRateByVolume

    def getStrikeFrozen(self):
        '''执行冻结'''
        return self.StrikeFrozen

    def getStrikeFrozenAmount(self):
        '''执行冻结金额'''
        return self.StrikeFrozenAmount

    def getAbandonFrozen(self):
        '''放弃执行冻结'''
        return self.AbandonFrozen

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getYdStrikeFrozen(self):
        '''执行冻结的昨仓'''
        return self.YdStrikeFrozen

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'PosiDirection'={self.getPosiDirection()}, 'HedgeFlag'={self.getHedgeFlag()}, 'PositionDate'={self.getPositionDate()}, 'YdPosition'={self.getYdPosition()}, 'Position'={self.getPosition()}, 'LongFrozen'={self.getLongFrozen()}, 'ShortFrozen'={self.getShortFrozen()}, 'LongFrozenAmount'={self.getLongFrozenAmount()}, 'ShortFrozenAmount'={self.getShortFrozenAmount()}, 'OpenVolume'={self.getOpenVolume()}, 'CloseVolume'={self.getCloseVolume()}, 'OpenAmount'={self.getOpenAmount()}, 'CloseAmount'={self.getCloseAmount()}, 'PositionCost'={self.getPositionCost()}, 'PreMargin'={self.getPreMargin()}, 'UseMargin'={self.getUseMargin()}, 'FrozenMargin'={self.getFrozenMargin()}, 'FrozenCash'={self.getFrozenCash()}, 'FrozenCommission'={self.getFrozenCommission()}, 'CashIn'={self.getCashIn()}, 'Commission'={self.getCommission()}, 'CloseProfit'={self.getCloseProfit()}, 'PositionProfit'={self.getPositionProfit()}, 'PreSettlementPrice'={self.getPreSettlementPrice()}, 'SettlementPrice'={self.getSettlementPrice()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'OpenCost'={self.getOpenCost()}, 'ExchangeMargin'={self.getExchangeMargin()}, 'CombPosition'={self.getCombPosition()}, 'CombLongFrozen'={self.getCombLongFrozen()}, 'CombShortFrozen'={self.getCombShortFrozen()}, 'CloseProfitByDate'={self.getCloseProfitByDate()}, 'CloseProfitByTrade'={self.getCloseProfitByTrade()}, 'TodayPosition'={self.getTodayPosition()}, 'MarginRateByMoney'={self.getMarginRateByMoney()}, 'MarginRateByVolume'={self.getMarginRateByVolume()}, 'StrikeFrozen'={self.getStrikeFrozen()}, 'StrikeFrozenAmount'={self.getStrikeFrozenAmount()}, 'AbandonFrozen'={self.getAbandonFrozen()}, 'ExchangeID'={self.getExchangeID()}, 'YdStrikeFrozen'={self.getYdStrikeFrozen()}, 'InvestUnitID'={self.getInvestUnitID()}, 'OptionValue'={self.getOptionValue()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'PosiDirection': self.getPosiDirection(), 'HedgeFlag': self.getHedgeFlag(), 'PositionDate': self.getPositionDate(), 'YdPosition': self.getYdPosition(), 'Position': self.getPosition(), 'LongFrozen': self.getLongFrozen(), 'ShortFrozen': self.getShortFrozen(), 'LongFrozenAmount': self.getLongFrozenAmount(), 'ShortFrozenAmount': self.getShortFrozenAmount(), 'OpenVolume': self.getOpenVolume(), 'CloseVolume': self.getCloseVolume(), 'OpenAmount': self.getOpenAmount(), 'CloseAmount': self.getCloseAmount(), 'PositionCost': self.getPositionCost(), 'PreMargin': self.getPreMargin(), 'UseMargin': self.getUseMargin(), 'FrozenMargin': self.getFrozenMargin(), 'FrozenCash': self.getFrozenCash(), 'FrozenCommission': self.getFrozenCommission(), 'CashIn': self.getCashIn(), 'Commission': self.getCommission(), 'CloseProfit': self.getCloseProfit(), 'PositionProfit': self.getPositionProfit(), 'PreSettlementPrice': self.getPreSettlementPrice(), 'SettlementPrice': self.getSettlementPrice(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'OpenCost': self.getOpenCost(), 'ExchangeMargin': self.getExchangeMargin(), 'CombPosition': self.getCombPosition(), 'CombLongFrozen': self.getCombLongFrozen(), 'CombShortFrozen': self.getCombShortFrozen(), 'CloseProfitByDate': self.getCloseProfitByDate(), 'CloseProfitByTrade': self.getCloseProfitByTrade(), 'TodayPosition': self.getTodayPosition(), 'MarginRateByMoney': self.getMarginRateByMoney(), 'MarginRateByVolume': self.getMarginRateByVolume(), 'StrikeFrozen': self.getStrikeFrozen(), 'StrikeFrozenAmount': self.getStrikeFrozenAmount(), 'AbandonFrozen': self.getAbandonFrozen(), 'ExchangeID': self.getExchangeID(), 'YdStrikeFrozen': self.getYdStrikeFrozen(), 'InvestUnitID': self.getInvestUnitID(), 'OptionValue': self.getOptionValue()}


class  CShfeFtdcInstrumentMarginRateField(Structure):
    """合约保证金率"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("IsRelative", c_int32),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getIsRelative(self):
        '''是否相对交易所收取'''
        return self.IsRelative

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'IsRelative'={self.getIsRelative()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'IsRelative': self.getIsRelative()}


class  CShfeFtdcInstrumentCommissionRateField(Structure):
    """合约手续费率"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("OpenRatioByMoney", c_double),
        ("OpenRatioByVolume", c_double),
        ("CloseRatioByMoney", c_double),
        ("CloseRatioByVolume", c_double),
        ("CloseTodayRatioByMoney", c_double),
        ("CloseTodayRatioByVolume", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getOpenRatioByMoney(self):
        '''开仓手续费率'''
        return self.OpenRatioByMoney

    def getOpenRatioByVolume(self):
        '''开仓手续费'''
        return self.OpenRatioByVolume

    def getCloseRatioByMoney(self):
        '''平仓手续费率'''
        return self.CloseRatioByMoney

    def getCloseRatioByVolume(self):
        '''平仓手续费'''
        return self.CloseRatioByVolume

    def getCloseTodayRatioByMoney(self):
        '''平今手续费率'''
        return self.CloseTodayRatioByMoney

    def getCloseTodayRatioByVolume(self):
        '''平今手续费'''
        return self.CloseTodayRatioByVolume

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'OpenRatioByMoney'={self.getOpenRatioByMoney()}, 'OpenRatioByVolume'={self.getOpenRatioByVolume()}, 'CloseRatioByMoney'={self.getCloseRatioByMoney()}, 'CloseRatioByVolume'={self.getCloseRatioByVolume()}, 'CloseTodayRatioByMoney'={self.getCloseTodayRatioByMoney()}, 'CloseTodayRatioByVolume'={self.getCloseTodayRatioByVolume()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'OpenRatioByMoney': self.getOpenRatioByMoney(), 'OpenRatioByVolume': self.getOpenRatioByVolume(), 'CloseRatioByMoney': self.getCloseRatioByMoney(), 'CloseRatioByVolume': self.getCloseRatioByVolume(), 'CloseTodayRatioByMoney': self.getCloseTodayRatioByMoney(), 'CloseTodayRatioByVolume': self.getCloseTodayRatioByVolume()}


class  CShfeFtdcDepthMarketDataField(Structure):
    """深度行情"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("ExchangeInstID", c_char*31),
        ("LastPrice", c_double),
        ("PreSettlementPrice", c_double),
        ("PreClosePrice", c_double),
        ("PreOpenInterest", c_double),
        ("OpenPrice", c_double),
        ("HighestPrice", c_double),
        ("LowestPrice", c_double),
        ("Volume", c_int32),
        ("Turnover", c_double),
        ("OpenInterest", c_double),
        ("ClosePrice", c_double),
        ("SettlementPrice", c_double),
        ("UpperLimitPrice", c_double),
        ("LowerLimitPrice", c_double),
        ("PreDelta", c_double),
        ("CurrDelta", c_double),
        ("UpdateTime", c_char*9),
        ("UpdateMillisec", c_int32),
        ("BidPrice1", c_double),
        ("BidVolume1", c_int32),
        ("AskPrice1", c_double),
        ("AskVolume1", c_int32),
        ("BidPrice2", c_double),
        ("BidVolume2", c_int32),
        ("AskPrice2", c_double),
        ("AskVolume2", c_int32),
        ("BidPrice3", c_double),
        ("BidVolume3", c_int32),
        ("AskPrice3", c_double),
        ("AskVolume3", c_int32),
        ("BidPrice4", c_double),
        ("BidVolume4", c_int32),
        ("AskPrice4", c_double),
        ("AskVolume4", c_int32),
        ("BidPrice5", c_double),
        ("BidVolume5", c_int32),
        ("AskPrice5", c_double),
        ("AskVolume5", c_int32),
        ("AveragePrice", c_double),
        ("ActionDay", c_char*9),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getLastPrice(self):
        '''最新价'''
        return self.LastPrice

    def getPreSettlementPrice(self):
        '''上次结算价'''
        return self.PreSettlementPrice

    def getPreClosePrice(self):
        '''昨收盘'''
        return self.PreClosePrice

    def getPreOpenInterest(self):
        '''昨持仓量'''
        return self.PreOpenInterest

    def getOpenPrice(self):
        '''今开盘'''
        return self.OpenPrice

    def getHighestPrice(self):
        '''最高价'''
        return self.HighestPrice

    def getLowestPrice(self):
        '''最低价'''
        return self.LowestPrice

    def getVolume(self):
        '''数量'''
        return self.Volume

    def getTurnover(self):
        '''成交金额'''
        return self.Turnover

    def getOpenInterest(self):
        '''持仓量'''
        return self.OpenInterest

    def getClosePrice(self):
        '''今收盘'''
        return self.ClosePrice

    def getSettlementPrice(self):
        '''本次结算价'''
        return self.SettlementPrice

    def getUpperLimitPrice(self):
        '''涨停板价'''
        return self.UpperLimitPrice

    def getLowerLimitPrice(self):
        '''跌停板价'''
        return self.LowerLimitPrice

    def getPreDelta(self):
        '''昨虚实度'''
        return self.PreDelta

    def getCurrDelta(self):
        '''今虚实度'''
        return self.CurrDelta

    def getUpdateTime(self):
        '''最后修改时间'''
        return str(self.UpdateTime, 'GBK')

    def getUpdateMillisec(self):
        '''最后修改毫秒'''
        return self.UpdateMillisec

    def getBidPrice1(self):
        '''申买价一'''
        return self.BidPrice1

    def getBidVolume1(self):
        '''申买量一'''
        return self.BidVolume1

    def getAskPrice1(self):
        '''申卖价一'''
        return self.AskPrice1

    def getAskVolume1(self):
        '''申卖量一'''
        return self.AskVolume1

    def getBidPrice2(self):
        '''申买价二'''
        return self.BidPrice2

    def getBidVolume2(self):
        '''申买量二'''
        return self.BidVolume2

    def getAskPrice2(self):
        '''申卖价二'''
        return self.AskPrice2

    def getAskVolume2(self):
        '''申卖量二'''
        return self.AskVolume2

    def getBidPrice3(self):
        '''申买价三'''
        return self.BidPrice3

    def getBidVolume3(self):
        '''申买量三'''
        return self.BidVolume3

    def getAskPrice3(self):
        '''申卖价三'''
        return self.AskPrice3

    def getAskVolume3(self):
        '''申卖量三'''
        return self.AskVolume3

    def getBidPrice4(self):
        '''申买价四'''
        return self.BidPrice4

    def getBidVolume4(self):
        '''申买量四'''
        return self.BidVolume4

    def getAskPrice4(self):
        '''申卖价四'''
        return self.AskPrice4

    def getAskVolume4(self):
        '''申卖量四'''
        return self.AskVolume4

    def getBidPrice5(self):
        '''申买价五'''
        return self.BidPrice5

    def getBidVolume5(self):
        '''申买量五'''
        return self.BidVolume5

    def getAskPrice5(self):
        '''申卖价五'''
        return self.AskPrice5

    def getAskVolume5(self):
        '''申卖量五'''
        return self.AskVolume5

    def getAveragePrice(self):
        '''当日均价'''
        return self.AveragePrice

    def getActionDay(self):
        '''业务日期'''
        return str(self.ActionDay, 'GBK')

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'LastPrice'={self.getLastPrice()}, 'PreSettlementPrice'={self.getPreSettlementPrice()}, 'PreClosePrice'={self.getPreClosePrice()}, 'PreOpenInterest'={self.getPreOpenInterest()}, 'OpenPrice'={self.getOpenPrice()}, 'HighestPrice'={self.getHighestPrice()}, 'LowestPrice'={self.getLowestPrice()}, 'Volume'={self.getVolume()}, 'Turnover'={self.getTurnover()}, 'OpenInterest'={self.getOpenInterest()}, 'ClosePrice'={self.getClosePrice()}, 'SettlementPrice'={self.getSettlementPrice()}, 'UpperLimitPrice'={self.getUpperLimitPrice()}, 'LowerLimitPrice'={self.getLowerLimitPrice()}, 'PreDelta'={self.getPreDelta()}, 'CurrDelta'={self.getCurrDelta()}, 'UpdateTime'={self.getUpdateTime()}, 'UpdateMillisec'={self.getUpdateMillisec()}, 'BidPrice1'={self.getBidPrice1()}, 'BidVolume1'={self.getBidVolume1()}, 'AskPrice1'={self.getAskPrice1()}, 'AskVolume1'={self.getAskVolume1()}, 'BidPrice2'={self.getBidPrice2()}, 'BidVolume2'={self.getBidVolume2()}, 'AskPrice2'={self.getAskPrice2()}, 'AskVolume2'={self.getAskVolume2()}, 'BidPrice3'={self.getBidPrice3()}, 'BidVolume3'={self.getBidVolume3()}, 'AskPrice3'={self.getAskPrice3()}, 'AskVolume3'={self.getAskVolume3()}, 'BidPrice4'={self.getBidPrice4()}, 'BidVolume4'={self.getBidVolume4()}, 'AskPrice4'={self.getAskPrice4()}, 'AskVolume4'={self.getAskVolume4()}, 'BidPrice5'={self.getBidPrice5()}, 'BidVolume5'={self.getBidVolume5()}, 'AskPrice5'={self.getAskPrice5()}, 'AskVolume5'={self.getAskVolume5()}, 'AveragePrice'={self.getAveragePrice()}, 'ActionDay'={self.getActionDay()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID(), 'ExchangeInstID': self.getExchangeInstID(), 'LastPrice': self.getLastPrice(), 'PreSettlementPrice': self.getPreSettlementPrice(), 'PreClosePrice': self.getPreClosePrice(), 'PreOpenInterest': self.getPreOpenInterest(), 'OpenPrice': self.getOpenPrice(), 'HighestPrice': self.getHighestPrice(), 'LowestPrice': self.getLowestPrice(), 'Volume': self.getVolume(), 'Turnover': self.getTurnover(), 'OpenInterest': self.getOpenInterest(), 'ClosePrice': self.getClosePrice(), 'SettlementPrice': self.getSettlementPrice(), 'UpperLimitPrice': self.getUpperLimitPrice(), 'LowerLimitPrice': self.getLowerLimitPrice(), 'PreDelta': self.getPreDelta(), 'CurrDelta': self.getCurrDelta(), 'UpdateTime': self.getUpdateTime(), 'UpdateMillisec': self.getUpdateMillisec(), 'BidPrice1': self.getBidPrice1(), 'BidVolume1': self.getBidVolume1(), 'AskPrice1': self.getAskPrice1(), 'AskVolume1': self.getAskVolume1(), 'BidPrice2': self.getBidPrice2(), 'BidVolume2': self.getBidVolume2(), 'AskPrice2': self.getAskPrice2(), 'AskVolume2': self.getAskVolume2(), 'BidPrice3': self.getBidPrice3(), 'BidVolume3': self.getBidVolume3(), 'AskPrice3': self.getAskPrice3(), 'AskVolume3': self.getAskVolume3(), 'BidPrice4': self.getBidPrice4(), 'BidVolume4': self.getBidVolume4(), 'AskPrice4': self.getAskPrice4(), 'AskVolume4': self.getAskVolume4(), 'BidPrice5': self.getBidPrice5(), 'BidVolume5': self.getBidVolume5(), 'AskPrice5': self.getAskPrice5(), 'AskVolume5': self.getAskVolume5(), 'AveragePrice': self.getAveragePrice(), 'ActionDay': self.getActionDay()}


class  CShfeFtdcInstrumentTradingRightField(Structure):
    """投资者合约交易权限"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("TradingRight", c_char),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getTradingRight(self):
        '''交易权限'''
        return TShfeFtdcTradingRightType(ord(self.TradingRight))

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'TradingRight'={self.getTradingRight()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'TradingRight': self.getTradingRight()}


class  CShfeFtdcBrokerUserField(Structure):
    """经纪公司用户"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("UserName", c_char*81),
        ("UserType", c_char),
        ("IsActive", c_int32),
        ("IsUsingOTP", c_int32),
        ("IsAuthForce", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getUserName(self):
        '''用户名称'''
        return str(self.UserName, 'GBK')

    def getUserType(self):
        '''用户类型'''
        return TShfeFtdcUserTypeType(ord(self.UserType))

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    def getIsUsingOTP(self):
        '''是否使用令牌'''
        return self.IsUsingOTP

    def getIsAuthForce(self):
        '''是否强制终端认证'''
        return self.IsAuthForce

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'UserName'={self.getUserName()}, 'UserType'={self.getUserType()}, 'IsActive'={self.getIsActive()}, 'IsUsingOTP'={self.getIsUsingOTP()}, 'IsAuthForce'={self.getIsAuthForce()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'UserName': self.getUserName(), 'UserType': self.getUserType(), 'IsActive': self.getIsActive(), 'IsUsingOTP': self.getIsUsingOTP(), 'IsAuthForce': self.getIsAuthForce()}


class  CShfeFtdcBrokerUserPasswordField(Structure):
    """经纪公司用户口令"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("Password", c_char*41),
        ("LastUpdateTime", c_char*17),
        ("LastLoginTime", c_char*17),
        ("ExpireDate", c_char*9),
        ("WeakExpireDate", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    def getLastUpdateTime(self):
        '''上次修改时间'''
        return str(self.LastUpdateTime, 'GBK')

    def getLastLoginTime(self):
        '''上次登陆时间'''
        return str(self.LastLoginTime, 'GBK')

    def getExpireDate(self):
        '''密码过期时间'''
        return str(self.ExpireDate, 'GBK')

    def getWeakExpireDate(self):
        '''弱密码过期时间'''
        return str(self.WeakExpireDate, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'Password'={self.getPassword()}, 'LastUpdateTime'={self.getLastUpdateTime()}, 'LastLoginTime'={self.getLastLoginTime()}, 'ExpireDate'={self.getExpireDate()}, 'WeakExpireDate'={self.getWeakExpireDate()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'Password': self.getPassword(), 'LastUpdateTime': self.getLastUpdateTime(), 'LastLoginTime': self.getLastLoginTime(), 'ExpireDate': self.getExpireDate(), 'WeakExpireDate': self.getWeakExpireDate()}


class  CShfeFtdcBrokerUserFunctionField(Structure):
    """经纪公司用户功能权限"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("BrokerFunctionCode", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getBrokerFunctionCode(self):
        '''经纪公司功能代码'''
        return TShfeFtdcBrokerFunctionCodeType(ord(self.BrokerFunctionCode))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'BrokerFunctionCode'={self.getBrokerFunctionCode()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'BrokerFunctionCode': self.getBrokerFunctionCode()}


class  CShfeFtdcTraderOfferField(Structure):
    """交易所交易员报盘机"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("TraderID", c_char*21),
        ("ParticipantID", c_char*11),
        ("Password", c_char*41),
        ("InstallID", c_int32),
        ("OrderLocalID", c_char*13),
        ("TraderConnectStatus", c_char),
        ("ConnectRequestDate", c_char*9),
        ("ConnectRequestTime", c_char*9),
        ("LastReportDate", c_char*9),
        ("LastReportTime", c_char*9),
        ("ConnectDate", c_char*9),
        ("ConnectTime", c_char*9),
        ("StartDate", c_char*9),
        ("StartTime", c_char*9),
        ("TradingDay", c_char*9),
        ("BrokerID", c_char*11),
        ("MaxTradeID", c_char*21),
        ("MaxOrderMessageReference", c_char*7),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getTraderConnectStatus(self):
        '''交易所交易员连接状态'''
        return TShfeFtdcTraderConnectStatusType(ord(self.TraderConnectStatus))

    def getConnectRequestDate(self):
        '''发出连接请求的日期'''
        return str(self.ConnectRequestDate, 'GBK')

    def getConnectRequestTime(self):
        '''发出连接请求的时间'''
        return str(self.ConnectRequestTime, 'GBK')

    def getLastReportDate(self):
        '''上次报告日期'''
        return str(self.LastReportDate, 'GBK')

    def getLastReportTime(self):
        '''上次报告时间'''
        return str(self.LastReportTime, 'GBK')

    def getConnectDate(self):
        '''完成连接日期'''
        return str(self.ConnectDate, 'GBK')

    def getConnectTime(self):
        '''完成连接时间'''
        return str(self.ConnectTime, 'GBK')

    def getStartDate(self):
        '''启动日期'''
        return str(self.StartDate, 'GBK')

    def getStartTime(self):
        '''启动时间'''
        return str(self.StartTime, 'GBK')

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getMaxTradeID(self):
        '''本席位最大成交编号'''
        return str(self.MaxTradeID, 'GBK')

    def getMaxOrderMessageReference(self):
        '''本席位最大报单备拷'''
        return str(self.MaxOrderMessageReference, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'TraderID'={self.getTraderID()}, 'ParticipantID'={self.getParticipantID()}, 'Password'={self.getPassword()}, 'InstallID'={self.getInstallID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'TraderConnectStatus'={self.getTraderConnectStatus()}, 'ConnectRequestDate'={self.getConnectRequestDate()}, 'ConnectRequestTime'={self.getConnectRequestTime()}, 'LastReportDate'={self.getLastReportDate()}, 'LastReportTime'={self.getLastReportTime()}, 'ConnectDate'={self.getConnectDate()}, 'ConnectTime'={self.getConnectTime()}, 'StartDate'={self.getStartDate()}, 'StartTime'={self.getStartTime()}, 'TradingDay'={self.getTradingDay()}, 'BrokerID'={self.getBrokerID()}, 'MaxTradeID'={self.getMaxTradeID()}, 'MaxOrderMessageReference'={self.getMaxOrderMessageReference()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'TraderID': self.getTraderID(), 'ParticipantID': self.getParticipantID(), 'Password': self.getPassword(), 'InstallID': self.getInstallID(), 'OrderLocalID': self.getOrderLocalID(), 'TraderConnectStatus': self.getTraderConnectStatus(), 'ConnectRequestDate': self.getConnectRequestDate(), 'ConnectRequestTime': self.getConnectRequestTime(), 'LastReportDate': self.getLastReportDate(), 'LastReportTime': self.getLastReportTime(), 'ConnectDate': self.getConnectDate(), 'ConnectTime': self.getConnectTime(), 'StartDate': self.getStartDate(), 'StartTime': self.getStartTime(), 'TradingDay': self.getTradingDay(), 'BrokerID': self.getBrokerID(), 'MaxTradeID': self.getMaxTradeID(), 'MaxOrderMessageReference': self.getMaxOrderMessageReference()}


class  CShfeFtdcSettlementInfoField(Structure):
    """投资者结算结果"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("SequenceNo", c_int32),
        ("Content", c_char*501),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getContent(self):
        '''消息正文'''
        return str(self.Content, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'SequenceNo'={self.getSequenceNo()}, 'Content'={self.getContent()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'SequenceNo': self.getSequenceNo(), 'Content': self.getContent(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcInstrumentMarginRateAdjustField(Structure):
    """合约保证金率调整"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("IsRelative", c_int32),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getIsRelative(self):
        '''是否相对交易所收取'''
        return self.IsRelative

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'IsRelative'={self.getIsRelative()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'IsRelative': self.getIsRelative()}


class  CShfeFtdcExchangeMarginRateField(Structure):
    """交易所保证金率"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InstrumentID", c_char*31),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InstrumentID'={self.getInstrumentID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InstrumentID': self.getInstrumentID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume()}


class  CShfeFtdcExchangeMarginRateAdjustField(Structure):
    """交易所保证金率调整"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InstrumentID", c_char*31),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("ExchLongMarginRatioByMoney", c_double),
        ("ExchLongMarginRatioByVolume", c_double),
        ("ExchShortMarginRatioByMoney", c_double),
        ("ExchShortMarginRatioByVolume", c_double),
        ("NoLongMarginRatioByMoney", c_double),
        ("NoLongMarginRatioByVolume", c_double),
        ("NoShortMarginRatioByMoney", c_double),
        ("NoShortMarginRatioByVolume", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''跟随交易所投资者多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''跟随交易所投资者多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''跟随交易所投资者空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''跟随交易所投资者空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getExchLongMarginRatioByMoney(self):
        '''交易所多头保证金率'''
        return self.ExchLongMarginRatioByMoney

    def getExchLongMarginRatioByVolume(self):
        '''交易所多头保证金费'''
        return self.ExchLongMarginRatioByVolume

    def getExchShortMarginRatioByMoney(self):
        '''交易所空头保证金率'''
        return self.ExchShortMarginRatioByMoney

    def getExchShortMarginRatioByVolume(self):
        '''交易所空头保证金费'''
        return self.ExchShortMarginRatioByVolume

    def getNoLongMarginRatioByMoney(self):
        '''不跟随交易所投资者多头保证金率'''
        return self.NoLongMarginRatioByMoney

    def getNoLongMarginRatioByVolume(self):
        '''不跟随交易所投资者多头保证金费'''
        return self.NoLongMarginRatioByVolume

    def getNoShortMarginRatioByMoney(self):
        '''不跟随交易所投资者空头保证金率'''
        return self.NoShortMarginRatioByMoney

    def getNoShortMarginRatioByVolume(self):
        '''不跟随交易所投资者空头保证金费'''
        return self.NoShortMarginRatioByVolume

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InstrumentID'={self.getInstrumentID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'ExchLongMarginRatioByMoney'={self.getExchLongMarginRatioByMoney()}, 'ExchLongMarginRatioByVolume'={self.getExchLongMarginRatioByVolume()}, 'ExchShortMarginRatioByMoney'={self.getExchShortMarginRatioByMoney()}, 'ExchShortMarginRatioByVolume'={self.getExchShortMarginRatioByVolume()}, 'NoLongMarginRatioByMoney'={self.getNoLongMarginRatioByMoney()}, 'NoLongMarginRatioByVolume'={self.getNoLongMarginRatioByVolume()}, 'NoShortMarginRatioByMoney'={self.getNoShortMarginRatioByMoney()}, 'NoShortMarginRatioByVolume'={self.getNoShortMarginRatioByVolume()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InstrumentID': self.getInstrumentID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'ExchLongMarginRatioByMoney': self.getExchLongMarginRatioByMoney(), 'ExchLongMarginRatioByVolume': self.getExchLongMarginRatioByVolume(), 'ExchShortMarginRatioByMoney': self.getExchShortMarginRatioByMoney(), 'ExchShortMarginRatioByVolume': self.getExchShortMarginRatioByVolume(), 'NoLongMarginRatioByMoney': self.getNoLongMarginRatioByMoney(), 'NoLongMarginRatioByVolume': self.getNoLongMarginRatioByVolume(), 'NoShortMarginRatioByMoney': self.getNoShortMarginRatioByMoney(), 'NoShortMarginRatioByVolume': self.getNoShortMarginRatioByVolume()}


class  CShfeFtdcSettlementRefField(Structure):
    """结算引用"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID()}


class  CShfeFtdcCurrentTimeField(Structure):
    """当前时间"""
    _fields_ = [
        ("CurrDate", c_char*9),
        ("CurrTime", c_char*9),
        ("CurrMillisec", c_int32),
        ("ActionDay", c_char*9),
    ]

    def getCurrDate(self):
        '''当前日期'''
        return str(self.CurrDate, 'GBK')

    def getCurrTime(self):
        '''当前时间'''
        return str(self.CurrTime, 'GBK')

    def getCurrMillisec(self):
        '''当前时间（毫秒）'''
        return self.CurrMillisec

    def getActionDay(self):
        '''业务日期'''
        return str(self.ActionDay, 'GBK')

    @property
    def __str__(self):
        return f"'CurrDate'={self.getCurrDate()}, 'CurrTime'={self.getCurrTime()}, 'CurrMillisec'={self.getCurrMillisec()}, 'ActionDay'={self.getActionDay()}"

    @property
    def __dict__(self):
        return {'CurrDate': self.getCurrDate(), 'CurrTime': self.getCurrTime(), 'CurrMillisec': self.getCurrMillisec(), 'ActionDay': self.getActionDay()}


class  CShfeFtdcCommPhaseField(Structure):
    """通讯阶段"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("CommPhaseNo", c_short),
        ("SystemID", c_char*21),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getCommPhaseNo(self):
        '''通讯时段编号'''
        return self.CommPhaseNo

    def getSystemID(self):
        '''系统编号'''
        return str(self.SystemID, 'GBK')

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'CommPhaseNo'={self.getCommPhaseNo()}, 'SystemID'={self.getSystemID()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'CommPhaseNo': self.getCommPhaseNo(), 'SystemID': self.getSystemID()}


class  CShfeFtdcLoginInfoField(Structure):
    """登录信息"""
    _fields_ = [
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("LoginDate", c_char*9),
        ("LoginTime", c_char*9),
        ("IPAddress", c_char*16),
        ("UserProductInfo", c_char*11),
        ("InterfaceProductInfo", c_char*11),
        ("ProtocolInfo", c_char*11),
        ("SystemName", c_char*41),
        ("PasswordDeprecated", c_char*41),
        ("MaxOrderRef", c_char*13),
        ("SHFETime", c_char*9),
        ("DCETime", c_char*9),
        ("CZCETime", c_char*9),
        ("FFEXTime", c_char*9),
        ("MacAddress", c_char*21),
        ("OneTimePassword", c_char*41),
        ("INETime", c_char*9),
        ("IsQryControl", c_int32),
        ("LoginRemark", c_char*36),
        ("Password", c_char*41),
    ]

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getLoginDate(self):
        '''登录日期'''
        return str(self.LoginDate, 'GBK')

    def getLoginTime(self):
        '''登录时间'''
        return str(self.LoginTime, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getUserProductInfo(self):
        '''用户端产品信息'''
        return str(self.UserProductInfo, 'GBK')

    def getInterfaceProductInfo(self):
        '''接口端产品信息'''
        return str(self.InterfaceProductInfo, 'GBK')

    def getProtocolInfo(self):
        '''协议信息'''
        return str(self.ProtocolInfo, 'GBK')

    def getSystemName(self):
        '''系统名称'''
        return str(self.SystemName, 'GBK')

    def getPasswordDeprecated(self):
        '''密码,已弃用'''
        return str(self.PasswordDeprecated, 'GBK')

    def getMaxOrderRef(self):
        '''最大报单引用'''
        return str(self.MaxOrderRef, 'GBK')

    def getSHFETime(self):
        '''上期所时间'''
        return str(self.SHFETime, 'GBK')

    def getDCETime(self):
        '''大商所时间'''
        return str(self.DCETime, 'GBK')

    def getCZCETime(self):
        '''郑商所时间'''
        return str(self.CZCETime, 'GBK')

    def getFFEXTime(self):
        '''中金所时间'''
        return str(self.FFEXTime, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    def getOneTimePassword(self):
        '''动态密码'''
        return str(self.OneTimePassword, 'GBK')

    def getINETime(self):
        '''能源中心时间'''
        return str(self.INETime, 'GBK')

    def getIsQryControl(self):
        '''查询时是否需要流控'''
        return self.IsQryControl

    def getLoginRemark(self):
        '''登录备注'''
        return str(self.LoginRemark, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    @property
    def __str__(self):
        return f"'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'LoginDate'={self.getLoginDate()}, 'LoginTime'={self.getLoginTime()}, 'IPAddress'={self.getIPAddress()}, 'UserProductInfo'={self.getUserProductInfo()}, 'InterfaceProductInfo'={self.getInterfaceProductInfo()}, 'ProtocolInfo'={self.getProtocolInfo()}, 'SystemName'={self.getSystemName()}, 'PasswordDeprecated'={self.getPasswordDeprecated()}, 'MaxOrderRef'={self.getMaxOrderRef()}, 'SHFETime'={self.getSHFETime()}, 'DCETime'={self.getDCETime()}, 'CZCETime'={self.getCZCETime()}, 'FFEXTime'={self.getFFEXTime()}, 'MacAddress'={self.getMacAddress()}, 'OneTimePassword'={self.getOneTimePassword()}, 'INETime'={self.getINETime()}, 'IsQryControl'={self.getIsQryControl()}, 'LoginRemark'={self.getLoginRemark()}, 'Password'={self.getPassword()}"

    @property
    def __dict__(self):
        return {'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'LoginDate': self.getLoginDate(), 'LoginTime': self.getLoginTime(), 'IPAddress': self.getIPAddress(), 'UserProductInfo': self.getUserProductInfo(), 'InterfaceProductInfo': self.getInterfaceProductInfo(), 'ProtocolInfo': self.getProtocolInfo(), 'SystemName': self.getSystemName(), 'PasswordDeprecated': self.getPasswordDeprecated(), 'MaxOrderRef': self.getMaxOrderRef(), 'SHFETime': self.getSHFETime(), 'DCETime': self.getDCETime(), 'CZCETime': self.getCZCETime(), 'FFEXTime': self.getFFEXTime(), 'MacAddress': self.getMacAddress(), 'OneTimePassword': self.getOneTimePassword(), 'INETime': self.getINETime(), 'IsQryControl': self.getIsQryControl(), 'LoginRemark': self.getLoginRemark(), 'Password': self.getPassword()}


class  CShfeFtdcLogoutAllField(Structure):
    """登录信息"""
    _fields_ = [
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("SystemName", c_char*41),
    ]

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getSystemName(self):
        '''系统名称'''
        return str(self.SystemName, 'GBK')

    @property
    def __str__(self):
        return f"'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'SystemName'={self.getSystemName()}"

    @property
    def __dict__(self):
        return {'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'SystemName': self.getSystemName()}


class  CShfeFtdcFrontStatusField(Structure):
    """前置状态"""
    _fields_ = [
        ("FrontID", c_int32),
        ("LastReportDate", c_char*9),
        ("LastReportTime", c_char*9),
        ("IsActive", c_int32),
    ]

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getLastReportDate(self):
        '''上次报告日期'''
        return str(self.LastReportDate, 'GBK')

    def getLastReportTime(self):
        '''上次报告时间'''
        return str(self.LastReportTime, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    @property
    def __str__(self):
        return f"'FrontID'={self.getFrontID()}, 'LastReportDate'={self.getLastReportDate()}, 'LastReportTime'={self.getLastReportTime()}, 'IsActive'={self.getIsActive()}"

    @property
    def __dict__(self):
        return {'FrontID': self.getFrontID(), 'LastReportDate': self.getLastReportDate(), 'LastReportTime': self.getLastReportTime(), 'IsActive': self.getIsActive()}


class  CShfeFtdcUserPasswordUpdateField(Structure):
    """用户口令变更"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("OldPassword", c_char*41),
        ("NewPassword", c_char*41),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOldPassword(self):
        '''原来的口令'''
        return str(self.OldPassword, 'GBK')

    def getNewPassword(self):
        '''新的口令'''
        return str(self.NewPassword, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'OldPassword'={self.getOldPassword()}, 'NewPassword'={self.getNewPassword()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'OldPassword': self.getOldPassword(), 'NewPassword': self.getNewPassword()}


class  CShfeFtdcInputOrderField(Structure):
    """输入报单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("UserForceClose", c_int32),
        ("IsSwapOrder", c_int32),
        ("ExchangeID", c_char*9),
        ("InvestUnitID", c_char*17),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("ClientID", c_char*11),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getUserForceClose(self):
        '''用户强评标志'''
        return self.UserForceClose

    def getIsSwapOrder(self):
        '''互换单标志'''
        return self.IsSwapOrder

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getClientID(self):
        '''交易编码'''
        return str(self.ClientID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'UserForceClose'={self.getUserForceClose()}, 'IsSwapOrder'={self.getIsSwapOrder()}, 'ExchangeID'={self.getExchangeID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'ClientID'={self.getClientID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'UserForceClose': self.getUserForceClose(), 'IsSwapOrder': self.getIsSwapOrder(), 'ExchangeID': self.getExchangeID(), 'InvestUnitID': self.getInvestUnitID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'ClientID': self.getClientID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcOrderField(Structure):
    """报单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("OrderLocalID", c_char*13),
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("ExchangeInstID", c_char*31),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderSubmitStatus", c_char),
        ("NotifySequence", c_int32),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("OrderSysID", c_char*21),
        ("OrderSource", c_char),
        ("OrderStatus", c_char),
        ("OrderType", c_char),
        ("VolumeTraded", c_int32),
        ("VolumeTotal", c_int32),
        ("InsertDate", c_char*9),
        ("InsertTime", c_char*9),
        ("ActiveTime", c_char*9),
        ("SuspendTime", c_char*9),
        ("UpdateTime", c_char*9),
        ("CancelTime", c_char*9),
        ("ActiveTraderID", c_char*21),
        ("ClearingPartID", c_char*11),
        ("SequenceNo", c_int32),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("UserProductInfo", c_char*11),
        ("StatusMsg", c_char*81),
        ("UserForceClose", c_int32),
        ("ActiveUserID", c_char*16),
        ("BrokerOrderSeq", c_int32),
        ("RelativeOrderSysID", c_char*21),
        ("ZCETotalTradedVolume", c_int32),
        ("IsSwapOrder", c_int32),
        ("BranchID", c_char*9),
        ("InvestUnitID", c_char*17),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderSubmitStatus(self):
        '''报单提交状态'''
        return TShfeFtdcOrderSubmitStatusType(ord(self.OrderSubmitStatus))

    def getNotifySequence(self):
        '''报单提示序号'''
        return self.NotifySequence

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getOrderSource(self):
        '''报单来源'''
        return TShfeFtdcOrderSourceType(ord(self.OrderSource))

    def getOrderStatus(self):
        '''报单状态'''
        return TShfeFtdcOrderStatusType(ord(self.OrderStatus))

    def getOrderType(self):
        '''报单类型'''
        return TShfeFtdcOrderTypeType(ord(self.OrderType))

    def getVolumeTraded(self):
        '''今成交数量'''
        return self.VolumeTraded

    def getVolumeTotal(self):
        '''剩余数量'''
        return self.VolumeTotal

    def getInsertDate(self):
        '''报单日期'''
        return str(self.InsertDate, 'GBK')

    def getInsertTime(self):
        '''委托时间'''
        return str(self.InsertTime, 'GBK')

    def getActiveTime(self):
        '''激活时间'''
        return str(self.ActiveTime, 'GBK')

    def getSuspendTime(self):
        '''挂起时间'''
        return str(self.SuspendTime, 'GBK')

    def getUpdateTime(self):
        '''最后修改时间'''
        return str(self.UpdateTime, 'GBK')

    def getCancelTime(self):
        '''撤销时间'''
        return str(self.CancelTime, 'GBK')

    def getActiveTraderID(self):
        '''最后修改交易所交易员代码'''
        return str(self.ActiveTraderID, 'GBK')

    def getClearingPartID(self):
        '''结算会员编号'''
        return str(self.ClearingPartID, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getUserProductInfo(self):
        '''用户端产品信息'''
        return str(self.UserProductInfo, 'GBK')

    def getStatusMsg(self):
        '''状态信息'''
        return str(self.StatusMsg, 'GBK')

    def getUserForceClose(self):
        '''用户强评标志'''
        return self.UserForceClose

    def getActiveUserID(self):
        '''操作用户代码'''
        return str(self.ActiveUserID, 'GBK')

    def getBrokerOrderSeq(self):
        '''经纪公司报单编号'''
        return self.BrokerOrderSeq

    def getRelativeOrderSysID(self):
        '''相关报单'''
        return str(self.RelativeOrderSysID, 'GBK')

    def getZCETotalTradedVolume(self):
        '''郑商所成交数量'''
        return self.ZCETotalTradedVolume

    def getIsSwapOrder(self):
        '''互换单标志'''
        return self.IsSwapOrder

    def getBranchID(self):
        '''营业部编号'''
        return str(self.BranchID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderSubmitStatus'={self.getOrderSubmitStatus()}, 'NotifySequence'={self.getNotifySequence()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'OrderSysID'={self.getOrderSysID()}, 'OrderSource'={self.getOrderSource()}, 'OrderStatus'={self.getOrderStatus()}, 'OrderType'={self.getOrderType()}, 'VolumeTraded'={self.getVolumeTraded()}, 'VolumeTotal'={self.getVolumeTotal()}, 'InsertDate'={self.getInsertDate()}, 'InsertTime'={self.getInsertTime()}, 'ActiveTime'={self.getActiveTime()}, 'SuspendTime'={self.getSuspendTime()}, 'UpdateTime'={self.getUpdateTime()}, 'CancelTime'={self.getCancelTime()}, 'ActiveTraderID'={self.getActiveTraderID()}, 'ClearingPartID'={self.getClearingPartID()}, 'SequenceNo'={self.getSequenceNo()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'UserProductInfo'={self.getUserProductInfo()}, 'StatusMsg'={self.getStatusMsg()}, 'UserForceClose'={self.getUserForceClose()}, 'ActiveUserID'={self.getActiveUserID()}, 'BrokerOrderSeq'={self.getBrokerOrderSeq()}, 'RelativeOrderSysID'={self.getRelativeOrderSysID()}, 'ZCETotalTradedVolume'={self.getZCETotalTradedVolume()}, 'IsSwapOrder'={self.getIsSwapOrder()}, 'BranchID'={self.getBranchID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'OrderLocalID': self.getOrderLocalID(), 'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'ExchangeInstID': self.getExchangeInstID(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderSubmitStatus': self.getOrderSubmitStatus(), 'NotifySequence': self.getNotifySequence(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'OrderSysID': self.getOrderSysID(), 'OrderSource': self.getOrderSource(), 'OrderStatus': self.getOrderStatus(), 'OrderType': self.getOrderType(), 'VolumeTraded': self.getVolumeTraded(), 'VolumeTotal': self.getVolumeTotal(), 'InsertDate': self.getInsertDate(), 'InsertTime': self.getInsertTime(), 'ActiveTime': self.getActiveTime(), 'SuspendTime': self.getSuspendTime(), 'UpdateTime': self.getUpdateTime(), 'CancelTime': self.getCancelTime(), 'ActiveTraderID': self.getActiveTraderID(), 'ClearingPartID': self.getClearingPartID(), 'SequenceNo': self.getSequenceNo(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'UserProductInfo': self.getUserProductInfo(), 'StatusMsg': self.getStatusMsg(), 'UserForceClose': self.getUserForceClose(), 'ActiveUserID': self.getActiveUserID(), 'BrokerOrderSeq': self.getBrokerOrderSeq(), 'RelativeOrderSysID': self.getRelativeOrderSysID(), 'ZCETotalTradedVolume': self.getZCETotalTradedVolume(), 'IsSwapOrder': self.getIsSwapOrder(), 'BranchID': self.getBranchID(), 'InvestUnitID': self.getInvestUnitID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcExchangeOrderField(Structure):
    """交易所报单"""
    _fields_ = [
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("OrderLocalID", c_char*13),
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("ExchangeInstID", c_char*31),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderSubmitStatus", c_char),
        ("NotifySequence", c_int32),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("OrderSysID", c_char*21),
        ("OrderSource", c_char),
        ("OrderStatus", c_char),
        ("OrderType", c_char),
        ("VolumeTraded", c_int32),
        ("VolumeTotal", c_int32),
        ("InsertDate", c_char*9),
        ("InsertTime", c_char*9),
        ("ActiveTime", c_char*9),
        ("SuspendTime", c_char*9),
        ("UpdateTime", c_char*9),
        ("CancelTime", c_char*9),
        ("ActiveTraderID", c_char*21),
        ("ClearingPartID", c_char*11),
        ("SequenceNo", c_int32),
        ("BranchID", c_char*9),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderSubmitStatus(self):
        '''报单提交状态'''
        return TShfeFtdcOrderSubmitStatusType(ord(self.OrderSubmitStatus))

    def getNotifySequence(self):
        '''报单提示序号'''
        return self.NotifySequence

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getOrderSource(self):
        '''报单来源'''
        return TShfeFtdcOrderSourceType(ord(self.OrderSource))

    def getOrderStatus(self):
        '''报单状态'''
        return TShfeFtdcOrderStatusType(ord(self.OrderStatus))

    def getOrderType(self):
        '''报单类型'''
        return TShfeFtdcOrderTypeType(ord(self.OrderType))

    def getVolumeTraded(self):
        '''今成交数量'''
        return self.VolumeTraded

    def getVolumeTotal(self):
        '''剩余数量'''
        return self.VolumeTotal

    def getInsertDate(self):
        '''报单日期'''
        return str(self.InsertDate, 'GBK')

    def getInsertTime(self):
        '''委托时间'''
        return str(self.InsertTime, 'GBK')

    def getActiveTime(self):
        '''激活时间'''
        return str(self.ActiveTime, 'GBK')

    def getSuspendTime(self):
        '''挂起时间'''
        return str(self.SuspendTime, 'GBK')

    def getUpdateTime(self):
        '''最后修改时间'''
        return str(self.UpdateTime, 'GBK')

    def getCancelTime(self):
        '''撤销时间'''
        return str(self.CancelTime, 'GBK')

    def getActiveTraderID(self):
        '''最后修改交易所交易员代码'''
        return str(self.ActiveTraderID, 'GBK')

    def getClearingPartID(self):
        '''结算会员编号'''
        return str(self.ClearingPartID, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getBranchID(self):
        '''营业部编号'''
        return str(self.BranchID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderSubmitStatus'={self.getOrderSubmitStatus()}, 'NotifySequence'={self.getNotifySequence()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'OrderSysID'={self.getOrderSysID()}, 'OrderSource'={self.getOrderSource()}, 'OrderStatus'={self.getOrderStatus()}, 'OrderType'={self.getOrderType()}, 'VolumeTraded'={self.getVolumeTraded()}, 'VolumeTotal'={self.getVolumeTotal()}, 'InsertDate'={self.getInsertDate()}, 'InsertTime'={self.getInsertTime()}, 'ActiveTime'={self.getActiveTime()}, 'SuspendTime'={self.getSuspendTime()}, 'UpdateTime'={self.getUpdateTime()}, 'CancelTime'={self.getCancelTime()}, 'ActiveTraderID'={self.getActiveTraderID()}, 'ClearingPartID'={self.getClearingPartID()}, 'SequenceNo'={self.getSequenceNo()}, 'BranchID'={self.getBranchID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'OrderLocalID': self.getOrderLocalID(), 'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'ExchangeInstID': self.getExchangeInstID(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderSubmitStatus': self.getOrderSubmitStatus(), 'NotifySequence': self.getNotifySequence(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'OrderSysID': self.getOrderSysID(), 'OrderSource': self.getOrderSource(), 'OrderStatus': self.getOrderStatus(), 'OrderType': self.getOrderType(), 'VolumeTraded': self.getVolumeTraded(), 'VolumeTotal': self.getVolumeTotal(), 'InsertDate': self.getInsertDate(), 'InsertTime': self.getInsertTime(), 'ActiveTime': self.getActiveTime(), 'SuspendTime': self.getSuspendTime(), 'UpdateTime': self.getUpdateTime(), 'CancelTime': self.getCancelTime(), 'ActiveTraderID': self.getActiveTraderID(), 'ClearingPartID': self.getClearingPartID(), 'SequenceNo': self.getSequenceNo(), 'BranchID': self.getBranchID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcExchangeOrderInsertErrorField(Structure):
    """交易所报单插入失败"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderLocalID", c_char*13),
        ("ErrorID", c_int32),
        ("ErrorMsg", c_char*81),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getErrorID(self):
        '''错误代码'''
        return self.ErrorID

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ErrorID'={self.getErrorID()}, 'ErrorMsg'={self.getErrorMsg()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderLocalID': self.getOrderLocalID(), 'ErrorID': self.getErrorID(), 'ErrorMsg': self.getErrorMsg()}


class  CShfeFtdcInputOrderActionField(Structure):
    """输入报单操作"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("OrderActionRef", c_int32),
        ("OrderRef", c_char*13),
        ("RequestID", c_int32),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("ExchangeID", c_char*9),
        ("OrderSysID", c_char*21),
        ("ActionFlag", c_char),
        ("LimitPrice", c_double),
        ("VolumeChange", c_int32),
        ("UserID", c_char*16),
        ("InstrumentID", c_char*31),
        ("InvestUnitID", c_char*17),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getOrderActionRef(self):
        '''报单操作引用'''
        return self.OrderActionRef

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getActionFlag(self):
        '''操作标志'''
        return TShfeFtdcActionFlagType(ord(self.ActionFlag))

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeChange(self):
        '''数量变化'''
        return self.VolumeChange

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'OrderActionRef'={self.getOrderActionRef()}, 'OrderRef'={self.getOrderRef()}, 'RequestID'={self.getRequestID()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'ExchangeID'={self.getExchangeID()}, 'OrderSysID'={self.getOrderSysID()}, 'ActionFlag'={self.getActionFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeChange'={self.getVolumeChange()}, 'UserID'={self.getUserID()}, 'InstrumentID'={self.getInstrumentID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'OrderActionRef': self.getOrderActionRef(), 'OrderRef': self.getOrderRef(), 'RequestID': self.getRequestID(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'ExchangeID': self.getExchangeID(), 'OrderSysID': self.getOrderSysID(), 'ActionFlag': self.getActionFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeChange': self.getVolumeChange(), 'UserID': self.getUserID(), 'InstrumentID': self.getInstrumentID(), 'InvestUnitID': self.getInvestUnitID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcOrderActionField(Structure):
    """报单操作"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("OrderActionRef", c_int32),
        ("OrderRef", c_char*13),
        ("RequestID", c_int32),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("ExchangeID", c_char*9),
        ("OrderSysID", c_char*21),
        ("ActionFlag", c_char),
        ("LimitPrice", c_double),
        ("VolumeChange", c_int32),
        ("ActionDate", c_char*9),
        ("ActionTime", c_char*9),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderLocalID", c_char*13),
        ("ActionLocalID", c_char*13),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("BusinessUnit", c_char*21),
        ("OrderActionStatus", c_char),
        ("UserID", c_char*16),
        ("StatusMsg", c_char*81),
        ("InstrumentID", c_char*31),
        ("BranchID", c_char*9),
        ("InvestUnitID", c_char*17),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getOrderActionRef(self):
        '''报单操作引用'''
        return self.OrderActionRef

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getActionFlag(self):
        '''操作标志'''
        return TShfeFtdcActionFlagType(ord(self.ActionFlag))

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeChange(self):
        '''数量变化'''
        return self.VolumeChange

    def getActionDate(self):
        '''操作日期'''
        return str(self.ActionDate, 'GBK')

    def getActionTime(self):
        '''操作时间'''
        return str(self.ActionTime, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getActionLocalID(self):
        '''操作本地编号'''
        return str(self.ActionLocalID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getOrderActionStatus(self):
        '''报单操作状态'''
        return TShfeFtdcOrderActionStatusType(ord(self.OrderActionStatus))

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getStatusMsg(self):
        '''状态信息'''
        return str(self.StatusMsg, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBranchID(self):
        '''营业部编号'''
        return str(self.BranchID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'OrderActionRef'={self.getOrderActionRef()}, 'OrderRef'={self.getOrderRef()}, 'RequestID'={self.getRequestID()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'ExchangeID'={self.getExchangeID()}, 'OrderSysID'={self.getOrderSysID()}, 'ActionFlag'={self.getActionFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeChange'={self.getVolumeChange()}, 'ActionDate'={self.getActionDate()}, 'ActionTime'={self.getActionTime()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ActionLocalID'={self.getActionLocalID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'BusinessUnit'={self.getBusinessUnit()}, 'OrderActionStatus'={self.getOrderActionStatus()}, 'UserID'={self.getUserID()}, 'StatusMsg'={self.getStatusMsg()}, 'InstrumentID'={self.getInstrumentID()}, 'BranchID'={self.getBranchID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'OrderActionRef': self.getOrderActionRef(), 'OrderRef': self.getOrderRef(), 'RequestID': self.getRequestID(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'ExchangeID': self.getExchangeID(), 'OrderSysID': self.getOrderSysID(), 'ActionFlag': self.getActionFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeChange': self.getVolumeChange(), 'ActionDate': self.getActionDate(), 'ActionTime': self.getActionTime(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderLocalID': self.getOrderLocalID(), 'ActionLocalID': self.getActionLocalID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'BusinessUnit': self.getBusinessUnit(), 'OrderActionStatus': self.getOrderActionStatus(), 'UserID': self.getUserID(), 'StatusMsg': self.getStatusMsg(), 'InstrumentID': self.getInstrumentID(), 'BranchID': self.getBranchID(), 'InvestUnitID': self.getInvestUnitID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcExchangeOrderActionField(Structure):
    """交易所报单操作"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("OrderSysID", c_char*21),
        ("ActionFlag", c_char),
        ("LimitPrice", c_double),
        ("VolumeChange", c_int32),
        ("ActionDate", c_char*9),
        ("ActionTime", c_char*9),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderLocalID", c_char*13),
        ("ActionLocalID", c_char*13),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("BusinessUnit", c_char*21),
        ("OrderActionStatus", c_char),
        ("UserID", c_char*16),
        ("BranchID", c_char*9),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getActionFlag(self):
        '''操作标志'''
        return TShfeFtdcActionFlagType(ord(self.ActionFlag))

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeChange(self):
        '''数量变化'''
        return self.VolumeChange

    def getActionDate(self):
        '''操作日期'''
        return str(self.ActionDate, 'GBK')

    def getActionTime(self):
        '''操作时间'''
        return str(self.ActionTime, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getActionLocalID(self):
        '''操作本地编号'''
        return str(self.ActionLocalID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getOrderActionStatus(self):
        '''报单操作状态'''
        return TShfeFtdcOrderActionStatusType(ord(self.OrderActionStatus))

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getBranchID(self):
        '''营业部编号'''
        return str(self.BranchID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'OrderSysID'={self.getOrderSysID()}, 'ActionFlag'={self.getActionFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeChange'={self.getVolumeChange()}, 'ActionDate'={self.getActionDate()}, 'ActionTime'={self.getActionTime()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ActionLocalID'={self.getActionLocalID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'BusinessUnit'={self.getBusinessUnit()}, 'OrderActionStatus'={self.getOrderActionStatus()}, 'UserID'={self.getUserID()}, 'BranchID'={self.getBranchID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'OrderSysID': self.getOrderSysID(), 'ActionFlag': self.getActionFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeChange': self.getVolumeChange(), 'ActionDate': self.getActionDate(), 'ActionTime': self.getActionTime(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderLocalID': self.getOrderLocalID(), 'ActionLocalID': self.getActionLocalID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'BusinessUnit': self.getBusinessUnit(), 'OrderActionStatus': self.getOrderActionStatus(), 'UserID': self.getUserID(), 'BranchID': self.getBranchID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcExchangeOrderActionErrorField(Structure):
    """交易所报单操作失败"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("OrderSysID", c_char*21),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderLocalID", c_char*13),
        ("ActionLocalID", c_char*13),
        ("ErrorID", c_int32),
        ("ErrorMsg", c_char*81),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getActionLocalID(self):
        '''操作本地编号'''
        return str(self.ActionLocalID, 'GBK')

    def getErrorID(self):
        '''错误代码'''
        return self.ErrorID

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'OrderSysID'={self.getOrderSysID()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ActionLocalID'={self.getActionLocalID()}, 'ErrorID'={self.getErrorID()}, 'ErrorMsg'={self.getErrorMsg()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'OrderSysID': self.getOrderSysID(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderLocalID': self.getOrderLocalID(), 'ActionLocalID': self.getActionLocalID(), 'ErrorID': self.getErrorID(), 'ErrorMsg': self.getErrorMsg()}


class  CShfeFtdcExchangeTradeField(Structure):
    """交易所成交"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("TradeID", c_char*21),
        ("Direction", c_char),
        ("OrderSysID", c_char*21),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("TradingRole", c_char),
        ("ExchangeInstID", c_char*31),
        ("OffsetFlag", c_char),
        ("HedgeFlag", c_char),
        ("Price", c_double),
        ("Volume", c_int32),
        ("TradeDate", c_char*9),
        ("TradeTime", c_char*9),
        ("TradeType", c_char),
        ("PriceSource", c_char),
        ("TraderID", c_char*21),
        ("OrderLocalID", c_char*13),
        ("ClearingPartID", c_char*11),
        ("BusinessUnit", c_char*21),
        ("SequenceNo", c_int32),
        ("TradeSource", c_char),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTradeID(self):
        '''成交编号'''
        return str(self.TradeID, 'GBK')

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getTradingRole(self):
        '''交易角色'''
        return TShfeFtdcTradingRoleType(ord(self.TradingRole))

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getOffsetFlag(self):
        '''开平标志'''
        return TShfeFtdcOffsetFlagType(ord(self.OffsetFlag))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPrice(self):
        '''价格'''
        return self.Price

    def getVolume(self):
        '''数量'''
        return self.Volume

    def getTradeDate(self):
        '''成交时期'''
        return str(self.TradeDate, 'GBK')

    def getTradeTime(self):
        '''成交时间'''
        return str(self.TradeTime, 'GBK')

    def getTradeType(self):
        '''成交类型'''
        return TShfeFtdcTradeTypeType(ord(self.TradeType))

    def getPriceSource(self):
        '''成交价来源'''
        return TShfeFtdcPriceSourceType(ord(self.PriceSource))

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getClearingPartID(self):
        '''结算会员编号'''
        return str(self.ClearingPartID, 'GBK')

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getTradeSource(self):
        '''成交来源'''
        return TShfeFtdcTradeSourceType(ord(self.TradeSource))

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'TradeID'={self.getTradeID()}, 'Direction'={self.getDirection()}, 'OrderSysID'={self.getOrderSysID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'TradingRole'={self.getTradingRole()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'OffsetFlag'={self.getOffsetFlag()}, 'HedgeFlag'={self.getHedgeFlag()}, 'Price'={self.getPrice()}, 'Volume'={self.getVolume()}, 'TradeDate'={self.getTradeDate()}, 'TradeTime'={self.getTradeTime()}, 'TradeType'={self.getTradeType()}, 'PriceSource'={self.getPriceSource()}, 'TraderID'={self.getTraderID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ClearingPartID'={self.getClearingPartID()}, 'BusinessUnit'={self.getBusinessUnit()}, 'SequenceNo'={self.getSequenceNo()}, 'TradeSource'={self.getTradeSource()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'TradeID': self.getTradeID(), 'Direction': self.getDirection(), 'OrderSysID': self.getOrderSysID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'TradingRole': self.getTradingRole(), 'ExchangeInstID': self.getExchangeInstID(), 'OffsetFlag': self.getOffsetFlag(), 'HedgeFlag': self.getHedgeFlag(), 'Price': self.getPrice(), 'Volume': self.getVolume(), 'TradeDate': self.getTradeDate(), 'TradeTime': self.getTradeTime(), 'TradeType': self.getTradeType(), 'PriceSource': self.getPriceSource(), 'TraderID': self.getTraderID(), 'OrderLocalID': self.getOrderLocalID(), 'ClearingPartID': self.getClearingPartID(), 'BusinessUnit': self.getBusinessUnit(), 'SequenceNo': self.getSequenceNo(), 'TradeSource': self.getTradeSource()}


class  CShfeFtdcTradeField(Structure):
    """成交"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("ExchangeID", c_char*9),
        ("TradeID", c_char*21),
        ("Direction", c_char),
        ("OrderSysID", c_char*21),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("TradingRole", c_char),
        ("ExchangeInstID", c_char*31),
        ("OffsetFlag", c_char),
        ("HedgeFlag", c_char),
        ("Price", c_double),
        ("Volume", c_int32),
        ("TradeDate", c_char*9),
        ("TradeTime", c_char*9),
        ("TradeType", c_char),
        ("PriceSource", c_char),
        ("TraderID", c_char*21),
        ("OrderLocalID", c_char*13),
        ("ClearingPartID", c_char*11),
        ("BusinessUnit", c_char*21),
        ("SequenceNo", c_int32),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("BrokerOrderSeq", c_int32),
        ("TradeSource", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTradeID(self):
        '''成交编号'''
        return str(self.TradeID, 'GBK')

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getTradingRole(self):
        '''交易角色'''
        return TShfeFtdcTradingRoleType(ord(self.TradingRole))

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getOffsetFlag(self):
        '''开平标志'''
        return TShfeFtdcOffsetFlagType(ord(self.OffsetFlag))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPrice(self):
        '''价格'''
        return self.Price

    def getVolume(self):
        '''数量'''
        return self.Volume

    def getTradeDate(self):
        '''成交时期'''
        return str(self.TradeDate, 'GBK')

    def getTradeTime(self):
        '''成交时间'''
        return str(self.TradeTime, 'GBK')

    def getTradeType(self):
        '''成交类型'''
        return TShfeFtdcTradeTypeType(ord(self.TradeType))

    def getPriceSource(self):
        '''成交价来源'''
        return TShfeFtdcPriceSourceType(ord(self.PriceSource))

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getClearingPartID(self):
        '''结算会员编号'''
        return str(self.ClearingPartID, 'GBK')

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getBrokerOrderSeq(self):
        '''经纪公司报单编号'''
        return self.BrokerOrderSeq

    def getTradeSource(self):
        '''成交来源'''
        return TShfeFtdcTradeSourceType(ord(self.TradeSource))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'ExchangeID'={self.getExchangeID()}, 'TradeID'={self.getTradeID()}, 'Direction'={self.getDirection()}, 'OrderSysID'={self.getOrderSysID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'TradingRole'={self.getTradingRole()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'OffsetFlag'={self.getOffsetFlag()}, 'HedgeFlag'={self.getHedgeFlag()}, 'Price'={self.getPrice()}, 'Volume'={self.getVolume()}, 'TradeDate'={self.getTradeDate()}, 'TradeTime'={self.getTradeTime()}, 'TradeType'={self.getTradeType()}, 'PriceSource'={self.getPriceSource()}, 'TraderID'={self.getTraderID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ClearingPartID'={self.getClearingPartID()}, 'BusinessUnit'={self.getBusinessUnit()}, 'SequenceNo'={self.getSequenceNo()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'BrokerOrderSeq'={self.getBrokerOrderSeq()}, 'TradeSource'={self.getTradeSource()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'ExchangeID': self.getExchangeID(), 'TradeID': self.getTradeID(), 'Direction': self.getDirection(), 'OrderSysID': self.getOrderSysID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'TradingRole': self.getTradingRole(), 'ExchangeInstID': self.getExchangeInstID(), 'OffsetFlag': self.getOffsetFlag(), 'HedgeFlag': self.getHedgeFlag(), 'Price': self.getPrice(), 'Volume': self.getVolume(), 'TradeDate': self.getTradeDate(), 'TradeTime': self.getTradeTime(), 'TradeType': self.getTradeType(), 'PriceSource': self.getPriceSource(), 'TraderID': self.getTraderID(), 'OrderLocalID': self.getOrderLocalID(), 'ClearingPartID': self.getClearingPartID(), 'BusinessUnit': self.getBusinessUnit(), 'SequenceNo': self.getSequenceNo(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'BrokerOrderSeq': self.getBrokerOrderSeq(), 'TradeSource': self.getTradeSource()}


class  CShfeFtdcUserSessionField(Structure):
    """用户会话"""
    _fields_ = [
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("LoginDate", c_char*9),
        ("LoginTime", c_char*9),
        ("IPAddress", c_char*16),
        ("UserProductInfo", c_char*11),
        ("InterfaceProductInfo", c_char*11),
        ("ProtocolInfo", c_char*11),
        ("MacAddress", c_char*21),
        ("LoginRemark", c_char*36),
    ]

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getLoginDate(self):
        '''登录日期'''
        return str(self.LoginDate, 'GBK')

    def getLoginTime(self):
        '''登录时间'''
        return str(self.LoginTime, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getUserProductInfo(self):
        '''用户端产品信息'''
        return str(self.UserProductInfo, 'GBK')

    def getInterfaceProductInfo(self):
        '''接口端产品信息'''
        return str(self.InterfaceProductInfo, 'GBK')

    def getProtocolInfo(self):
        '''协议信息'''
        return str(self.ProtocolInfo, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    def getLoginRemark(self):
        '''登录备注'''
        return str(self.LoginRemark, 'GBK')

    @property
    def __str__(self):
        return f"'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'LoginDate'={self.getLoginDate()}, 'LoginTime'={self.getLoginTime()}, 'IPAddress'={self.getIPAddress()}, 'UserProductInfo'={self.getUserProductInfo()}, 'InterfaceProductInfo'={self.getInterfaceProductInfo()}, 'ProtocolInfo'={self.getProtocolInfo()}, 'MacAddress'={self.getMacAddress()}, 'LoginRemark'={self.getLoginRemark()}"

    @property
    def __dict__(self):
        return {'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'LoginDate': self.getLoginDate(), 'LoginTime': self.getLoginTime(), 'IPAddress': self.getIPAddress(), 'UserProductInfo': self.getUserProductInfo(), 'InterfaceProductInfo': self.getInterfaceProductInfo(), 'ProtocolInfo': self.getProtocolInfo(), 'MacAddress': self.getMacAddress(), 'LoginRemark': self.getLoginRemark()}


class  CShfeFtdcQueryMaxOrderVolumeField(Structure):
    """查询最大报单数量"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("Direction", c_char),
        ("OffsetFlag", c_char),
        ("HedgeFlag", c_char),
        ("MaxVolume", c_int32),
        ("ExchangeID", c_char*9),
        ("InvestUnitID", c_char*17),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getOffsetFlag(self):
        '''开平标志'''
        return TShfeFtdcOffsetFlagType(ord(self.OffsetFlag))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getMaxVolume(self):
        '''最大允许报单数量'''
        return self.MaxVolume

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'Direction'={self.getDirection()}, 'OffsetFlag'={self.getOffsetFlag()}, 'HedgeFlag'={self.getHedgeFlag()}, 'MaxVolume'={self.getMaxVolume()}, 'ExchangeID'={self.getExchangeID()}, 'InvestUnitID'={self.getInvestUnitID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'Direction': self.getDirection(), 'OffsetFlag': self.getOffsetFlag(), 'HedgeFlag': self.getHedgeFlag(), 'MaxVolume': self.getMaxVolume(), 'ExchangeID': self.getExchangeID(), 'InvestUnitID': self.getInvestUnitID()}


class  CShfeFtdcSettlementInfoConfirmField(Structure):
    """投资者结算结果确认信息"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("ConfirmDate", c_char*9),
        ("ConfirmTime", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getConfirmDate(self):
        '''确认日期'''
        return str(self.ConfirmDate, 'GBK')

    def getConfirmTime(self):
        '''确认时间'''
        return str(self.ConfirmTime, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'ConfirmDate'={self.getConfirmDate()}, 'ConfirmTime'={self.getConfirmTime()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'ConfirmDate': self.getConfirmDate(), 'ConfirmTime': self.getConfirmTime()}


class  CShfeFtdcSyncDepositField(Structure):
    """出入金同步"""
    _fields_ = [
        ("DepositSeqNo", c_char*15),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("Deposit", c_double),
        ("IsForce", c_int32),
        ("CurrencyID", c_char*4),
    ]

    def getDepositSeqNo(self):
        '''出入金流水号'''
        return str(self.DepositSeqNo, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getDeposit(self):
        '''入金金额'''
        return self.Deposit

    def getIsForce(self):
        '''是否强制进行'''
        return self.IsForce

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'DepositSeqNo'={self.getDepositSeqNo()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'Deposit'={self.getDeposit()}, 'IsForce'={self.getIsForce()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'DepositSeqNo': self.getDepositSeqNo(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'Deposit': self.getDeposit(), 'IsForce': self.getIsForce(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcBrokerSyncField(Structure):
    """经纪公司同步"""
    _fields_ = [
        ("BrokerID", c_char*11),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID()}


class  CShfeFtdcSyncingInvestorField(Structure):
    """正在同步中的投资者"""
    _fields_ = [
        ("InvestorID", c_char*13),
        ("BrokerID", c_char*11),
        ("InvestorGroupID", c_char*13),
        ("InvestorName", c_char*81),
        ("IdentifiedCardType", c_char),
        ("IdentifiedCardNo", c_char*51),
        ("IsActive", c_int32),
        ("Telephone", c_char*41),
        ("Address", c_char*101),
        ("OpenDate", c_char*9),
        ("Mobile", c_char*41),
        ("CommModelID", c_char*13),
        ("MarginModelID", c_char*13),
    ]

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorGroupID(self):
        '''投资者分组代码'''
        return str(self.InvestorGroupID, 'GBK')

    def getInvestorName(self):
        '''投资者名称'''
        return str(self.InvestorName, 'GBK')

    def getIdentifiedCardType(self):
        '''证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.IdentifiedCardType))

    def getIdentifiedCardNo(self):
        '''证件号码'''
        return str(self.IdentifiedCardNo, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    def getTelephone(self):
        '''联系电话'''
        return str(self.Telephone, 'GBK')

    def getAddress(self):
        '''通讯地址'''
        return str(self.Address, 'GBK')

    def getOpenDate(self):
        '''开户日期'''
        return str(self.OpenDate, 'GBK')

    def getMobile(self):
        '''手机'''
        return str(self.Mobile, 'GBK')

    def getCommModelID(self):
        '''手续费率模板代码'''
        return str(self.CommModelID, 'GBK')

    def getMarginModelID(self):
        '''保证金率模板代码'''
        return str(self.MarginModelID, 'GBK')

    @property
    def __str__(self):
        return f"'InvestorID'={self.getInvestorID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorGroupID'={self.getInvestorGroupID()}, 'InvestorName'={self.getInvestorName()}, 'IdentifiedCardType'={self.getIdentifiedCardType()}, 'IdentifiedCardNo'={self.getIdentifiedCardNo()}, 'IsActive'={self.getIsActive()}, 'Telephone'={self.getTelephone()}, 'Address'={self.getAddress()}, 'OpenDate'={self.getOpenDate()}, 'Mobile'={self.getMobile()}, 'CommModelID'={self.getCommModelID()}, 'MarginModelID'={self.getMarginModelID()}"

    @property
    def __dict__(self):
        return {'InvestorID': self.getInvestorID(), 'BrokerID': self.getBrokerID(), 'InvestorGroupID': self.getInvestorGroupID(), 'InvestorName': self.getInvestorName(), 'IdentifiedCardType': self.getIdentifiedCardType(), 'IdentifiedCardNo': self.getIdentifiedCardNo(), 'IsActive': self.getIsActive(), 'Telephone': self.getTelephone(), 'Address': self.getAddress(), 'OpenDate': self.getOpenDate(), 'Mobile': self.getMobile(), 'CommModelID': self.getCommModelID(), 'MarginModelID': self.getMarginModelID()}


class  CShfeFtdcSyncingTradingCodeField(Structure):
    """正在同步中的交易代码"""
    _fields_ = [
        ("InvestorID", c_char*13),
        ("BrokerID", c_char*11),
        ("ExchangeID", c_char*9),
        ("ClientID", c_char*11),
        ("IsActive", c_int32),
        ("ClientIDType", c_char),
    ]

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    def getClientIDType(self):
        '''交易编码类型'''
        return TShfeFtdcClientIDTypeType(ord(self.ClientIDType))

    @property
    def __str__(self):
        return f"'InvestorID'={self.getInvestorID()}, 'BrokerID'={self.getBrokerID()}, 'ExchangeID'={self.getExchangeID()}, 'ClientID'={self.getClientID()}, 'IsActive'={self.getIsActive()}, 'ClientIDType'={self.getClientIDType()}"

    @property
    def __dict__(self):
        return {'InvestorID': self.getInvestorID(), 'BrokerID': self.getBrokerID(), 'ExchangeID': self.getExchangeID(), 'ClientID': self.getClientID(), 'IsActive': self.getIsActive(), 'ClientIDType': self.getClientIDType()}


class  CShfeFtdcSyncingInvestorGroupField(Structure):
    """正在同步中的投资者分组"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorGroupID", c_char*13),
        ("InvestorGroupName", c_char*41),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorGroupID(self):
        '''投资者分组代码'''
        return str(self.InvestorGroupID, 'GBK')

    def getInvestorGroupName(self):
        '''投资者分组名称'''
        return str(self.InvestorGroupName, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorGroupID'={self.getInvestorGroupID()}, 'InvestorGroupName'={self.getInvestorGroupName()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorGroupID': self.getInvestorGroupID(), 'InvestorGroupName': self.getInvestorGroupName()}


class  CShfeFtdcSyncingTradingAccountField(Structure):
    """正在同步中的交易账号"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("AccountID", c_char*13),
        ("PreMortgage", c_double),
        ("PreCredit", c_double),
        ("PreDeposit", c_double),
        ("PreBalance", c_double),
        ("PreMargin", c_double),
        ("InterestBase", c_double),
        ("Interest", c_double),
        ("Deposit", c_double),
        ("Withdraw", c_double),
        ("FrozenMargin", c_double),
        ("FrozenCash", c_double),
        ("FrozenCommission", c_double),
        ("CurrMargin", c_double),
        ("CashIn", c_double),
        ("Commission", c_double),
        ("CloseProfit", c_double),
        ("PositionProfit", c_double),
        ("Balance", c_double),
        ("Available", c_double),
        ("WithdrawQuota", c_double),
        ("Reserve", c_double),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("Credit", c_double),
        ("Mortgage", c_double),
        ("ExchangeMargin", c_double),
        ("DeliveryMargin", c_double),
        ("ExchangeDeliveryMargin", c_double),
        ("ReserveBalance", c_double),
        ("CurrencyID", c_char*4),
        ("PreFundMortgageIn", c_double),
        ("PreFundMortgageOut", c_double),
        ("FundMortgageIn", c_double),
        ("FundMortgageOut", c_double),
        ("FundMortgageAvailable", c_double),
        ("MortgageableFund", c_double),
        ("SpecProductMargin", c_double),
        ("SpecProductFrozenMargin", c_double),
        ("SpecProductCommission", c_double),
        ("SpecProductFrozenCommission", c_double),
        ("SpecProductPositionProfit", c_double),
        ("SpecProductCloseProfit", c_double),
        ("SpecProductPositionProfitByAlg", c_double),
        ("SpecProductExchangeMargin", c_double),
        ("FrozenSwap", c_double),
        ("RemainSwap", c_double),
        ("OptionCloseProfit", c_double),
        ("OptionValue", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getPreMortgage(self):
        '''上次质押金额'''
        return self.PreMortgage

    def getPreCredit(self):
        '''上次信用额度'''
        return self.PreCredit

    def getPreDeposit(self):
        '''上次存款额'''
        return self.PreDeposit

    def getPreBalance(self):
        '''上次结算准备金'''
        return self.PreBalance

    def getPreMargin(self):
        '''上次占用的保证金'''
        return self.PreMargin

    def getInterestBase(self):
        '''利息基数'''
        return self.InterestBase

    def getInterest(self):
        '''利息收入'''
        return self.Interest

    def getDeposit(self):
        '''入金金额'''
        return self.Deposit

    def getWithdraw(self):
        '''出金金额'''
        return self.Withdraw

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCurrMargin(self):
        '''当前保证金总额'''
        return self.CurrMargin

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getBalance(self):
        '''期货结算准备金'''
        return self.Balance

    def getAvailable(self):
        '''可用资金'''
        return self.Available

    def getWithdrawQuota(self):
        '''可取资金'''
        return self.WithdrawQuota

    def getReserve(self):
        '''基本准备金'''
        return self.Reserve

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getCredit(self):
        '''信用额度'''
        return self.Credit

    def getMortgage(self):
        '''质押金额'''
        return self.Mortgage

    def getExchangeMargin(self):
        '''交易所保证金'''
        return self.ExchangeMargin

    def getDeliveryMargin(self):
        '''投资者交割保证金'''
        return self.DeliveryMargin

    def getExchangeDeliveryMargin(self):
        '''交易所交割保证金'''
        return self.ExchangeDeliveryMargin

    def getReserveBalance(self):
        '''保底期货结算准备金'''
        return self.ReserveBalance

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getPreFundMortgageIn(self):
        '''上次货币质入金额'''
        return self.PreFundMortgageIn

    def getPreFundMortgageOut(self):
        '''上次货币质出金额'''
        return self.PreFundMortgageOut

    def getFundMortgageIn(self):
        '''货币质入金额'''
        return self.FundMortgageIn

    def getFundMortgageOut(self):
        '''货币质出金额'''
        return self.FundMortgageOut

    def getFundMortgageAvailable(self):
        '''货币质押余额'''
        return self.FundMortgageAvailable

    def getMortgageableFund(self):
        '''可质押货币金额'''
        return self.MortgageableFund

    def getSpecProductMargin(self):
        '''特殊产品占用保证金'''
        return self.SpecProductMargin

    def getSpecProductFrozenMargin(self):
        '''特殊产品冻结保证金'''
        return self.SpecProductFrozenMargin

    def getSpecProductCommission(self):
        '''特殊产品手续费'''
        return self.SpecProductCommission

    def getSpecProductFrozenCommission(self):
        '''特殊产品冻结手续费'''
        return self.SpecProductFrozenCommission

    def getSpecProductPositionProfit(self):
        '''特殊产品持仓盈亏'''
        return self.SpecProductPositionProfit

    def getSpecProductCloseProfit(self):
        '''特殊产品平仓盈亏'''
        return self.SpecProductCloseProfit

    def getSpecProductPositionProfitByAlg(self):
        '''根据持仓盈亏算法计算的特殊产品持仓盈亏'''
        return self.SpecProductPositionProfitByAlg

    def getSpecProductExchangeMargin(self):
        '''特殊产品交易所保证金'''
        return self.SpecProductExchangeMargin

    def getFrozenSwap(self):
        '''延时换汇冻结金额'''
        return self.FrozenSwap

    def getRemainSwap(self):
        '''剩余换汇额度'''
        return self.RemainSwap

    def getOptionCloseProfit(self):
        '''期权平仓盈亏'''
        return self.OptionCloseProfit

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'AccountID'={self.getAccountID()}, 'PreMortgage'={self.getPreMortgage()}, 'PreCredit'={self.getPreCredit()}, 'PreDeposit'={self.getPreDeposit()}, 'PreBalance'={self.getPreBalance()}, 'PreMargin'={self.getPreMargin()}, 'InterestBase'={self.getInterestBase()}, 'Interest'={self.getInterest()}, 'Deposit'={self.getDeposit()}, 'Withdraw'={self.getWithdraw()}, 'FrozenMargin'={self.getFrozenMargin()}, 'FrozenCash'={self.getFrozenCash()}, 'FrozenCommission'={self.getFrozenCommission()}, 'CurrMargin'={self.getCurrMargin()}, 'CashIn'={self.getCashIn()}, 'Commission'={self.getCommission()}, 'CloseProfit'={self.getCloseProfit()}, 'PositionProfit'={self.getPositionProfit()}, 'Balance'={self.getBalance()}, 'Available'={self.getAvailable()}, 'WithdrawQuota'={self.getWithdrawQuota()}, 'Reserve'={self.getReserve()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'Credit'={self.getCredit()}, 'Mortgage'={self.getMortgage()}, 'ExchangeMargin'={self.getExchangeMargin()}, 'DeliveryMargin'={self.getDeliveryMargin()}, 'ExchangeDeliveryMargin'={self.getExchangeDeliveryMargin()}, 'ReserveBalance'={self.getReserveBalance()}, 'CurrencyID'={self.getCurrencyID()}, 'PreFundMortgageIn'={self.getPreFundMortgageIn()}, 'PreFundMortgageOut'={self.getPreFundMortgageOut()}, 'FundMortgageIn'={self.getFundMortgageIn()}, 'FundMortgageOut'={self.getFundMortgageOut()}, 'FundMortgageAvailable'={self.getFundMortgageAvailable()}, 'MortgageableFund'={self.getMortgageableFund()}, 'SpecProductMargin'={self.getSpecProductMargin()}, 'SpecProductFrozenMargin'={self.getSpecProductFrozenMargin()}, 'SpecProductCommission'={self.getSpecProductCommission()}, 'SpecProductFrozenCommission'={self.getSpecProductFrozenCommission()}, 'SpecProductPositionProfit'={self.getSpecProductPositionProfit()}, 'SpecProductCloseProfit'={self.getSpecProductCloseProfit()}, 'SpecProductPositionProfitByAlg'={self.getSpecProductPositionProfitByAlg()}, 'SpecProductExchangeMargin'={self.getSpecProductExchangeMargin()}, 'FrozenSwap'={self.getFrozenSwap()}, 'RemainSwap'={self.getRemainSwap()}, 'OptionCloseProfit'={self.getOptionCloseProfit()}, 'OptionValue'={self.getOptionValue()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'AccountID': self.getAccountID(), 'PreMortgage': self.getPreMortgage(), 'PreCredit': self.getPreCredit(), 'PreDeposit': self.getPreDeposit(), 'PreBalance': self.getPreBalance(), 'PreMargin': self.getPreMargin(), 'InterestBase': self.getInterestBase(), 'Interest': self.getInterest(), 'Deposit': self.getDeposit(), 'Withdraw': self.getWithdraw(), 'FrozenMargin': self.getFrozenMargin(), 'FrozenCash': self.getFrozenCash(), 'FrozenCommission': self.getFrozenCommission(), 'CurrMargin': self.getCurrMargin(), 'CashIn': self.getCashIn(), 'Commission': self.getCommission(), 'CloseProfit': self.getCloseProfit(), 'PositionProfit': self.getPositionProfit(), 'Balance': self.getBalance(), 'Available': self.getAvailable(), 'WithdrawQuota': self.getWithdrawQuota(), 'Reserve': self.getReserve(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'Credit': self.getCredit(), 'Mortgage': self.getMortgage(), 'ExchangeMargin': self.getExchangeMargin(), 'DeliveryMargin': self.getDeliveryMargin(), 'ExchangeDeliveryMargin': self.getExchangeDeliveryMargin(), 'ReserveBalance': self.getReserveBalance(), 'CurrencyID': self.getCurrencyID(), 'PreFundMortgageIn': self.getPreFundMortgageIn(), 'PreFundMortgageOut': self.getPreFundMortgageOut(), 'FundMortgageIn': self.getFundMortgageIn(), 'FundMortgageOut': self.getFundMortgageOut(), 'FundMortgageAvailable': self.getFundMortgageAvailable(), 'MortgageableFund': self.getMortgageableFund(), 'SpecProductMargin': self.getSpecProductMargin(), 'SpecProductFrozenMargin': self.getSpecProductFrozenMargin(), 'SpecProductCommission': self.getSpecProductCommission(), 'SpecProductFrozenCommission': self.getSpecProductFrozenCommission(), 'SpecProductPositionProfit': self.getSpecProductPositionProfit(), 'SpecProductCloseProfit': self.getSpecProductCloseProfit(), 'SpecProductPositionProfitByAlg': self.getSpecProductPositionProfitByAlg(), 'SpecProductExchangeMargin': self.getSpecProductExchangeMargin(), 'FrozenSwap': self.getFrozenSwap(), 'RemainSwap': self.getRemainSwap(), 'OptionCloseProfit': self.getOptionCloseProfit(), 'OptionValue': self.getOptionValue()}


class  CShfeFtdcSyncingInvestorPositionField(Structure):
    """正在同步中的投资者持仓"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("PosiDirection", c_char),
        ("HedgeFlag", c_char),
        ("PositionDate", c_char),
        ("YdPosition", c_int32),
        ("Position", c_int32),
        ("LongFrozen", c_int32),
        ("ShortFrozen", c_int32),
        ("LongFrozenAmount", c_double),
        ("ShortFrozenAmount", c_double),
        ("OpenVolume", c_int32),
        ("CloseVolume", c_int32),
        ("OpenAmount", c_double),
        ("CloseAmount", c_double),
        ("PositionCost", c_double),
        ("PreMargin", c_double),
        ("UseMargin", c_double),
        ("FrozenMargin", c_double),
        ("FrozenCash", c_double),
        ("FrozenCommission", c_double),
        ("CashIn", c_double),
        ("Commission", c_double),
        ("CloseProfit", c_double),
        ("PositionProfit", c_double),
        ("PreSettlementPrice", c_double),
        ("SettlementPrice", c_double),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("OpenCost", c_double),
        ("ExchangeMargin", c_double),
        ("CombPosition", c_int32),
        ("CombLongFrozen", c_int32),
        ("CombShortFrozen", c_int32),
        ("CloseProfitByDate", c_double),
        ("CloseProfitByTrade", c_double),
        ("TodayPosition", c_int32),
        ("MarginRateByMoney", c_double),
        ("MarginRateByVolume", c_double),
        ("StrikeFrozen", c_int32),
        ("StrikeFrozenAmount", c_double),
        ("AbandonFrozen", c_int32),
        ("ExchangeID", c_char*9),
        ("YdStrikeFrozen", c_int32),
        ("InvestUnitID", c_char*17),
        ("OptionValue", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPosiDirection(self):
        '''持仓多空方向'''
        return TShfeFtdcPosiDirectionType(ord(self.PosiDirection))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPositionDate(self):
        '''持仓日期'''
        return TShfeFtdcPositionDateType(ord(self.PositionDate))

    def getYdPosition(self):
        '''上日持仓'''
        return self.YdPosition

    def getPosition(self):
        '''今日持仓'''
        return self.Position

    def getLongFrozen(self):
        '''多头冻结'''
        return self.LongFrozen

    def getShortFrozen(self):
        '''空头冻结'''
        return self.ShortFrozen

    def getLongFrozenAmount(self):
        '''开仓冻结金额'''
        return self.LongFrozenAmount

    def getShortFrozenAmount(self):
        '''开仓冻结金额'''
        return self.ShortFrozenAmount

    def getOpenVolume(self):
        '''开仓量'''
        return self.OpenVolume

    def getCloseVolume(self):
        '''平仓量'''
        return self.CloseVolume

    def getOpenAmount(self):
        '''开仓金额'''
        return self.OpenAmount

    def getCloseAmount(self):
        '''平仓金额'''
        return self.CloseAmount

    def getPositionCost(self):
        '''持仓成本'''
        return self.PositionCost

    def getPreMargin(self):
        '''上次占用的保证金'''
        return self.PreMargin

    def getUseMargin(self):
        '''占用的保证金'''
        return self.UseMargin

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getPreSettlementPrice(self):
        '''上次结算价'''
        return self.PreSettlementPrice

    def getSettlementPrice(self):
        '''本次结算价'''
        return self.SettlementPrice

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getOpenCost(self):
        '''开仓成本'''
        return self.OpenCost

    def getExchangeMargin(self):
        '''交易所保证金'''
        return self.ExchangeMargin

    def getCombPosition(self):
        '''组合成交形成的持仓'''
        return self.CombPosition

    def getCombLongFrozen(self):
        '''组合多头冻结'''
        return self.CombLongFrozen

    def getCombShortFrozen(self):
        '''组合空头冻结'''
        return self.CombShortFrozen

    def getCloseProfitByDate(self):
        '''逐日盯市平仓盈亏'''
        return self.CloseProfitByDate

    def getCloseProfitByTrade(self):
        '''逐笔对冲平仓盈亏'''
        return self.CloseProfitByTrade

    def getTodayPosition(self):
        '''今日持仓'''
        return self.TodayPosition

    def getMarginRateByMoney(self):
        '''保证金率'''
        return self.MarginRateByMoney

    def getMarginRateByVolume(self):
        '''保证金率(按手数)'''
        return self.MarginRateByVolume

    def getStrikeFrozen(self):
        '''执行冻结'''
        return self.StrikeFrozen

    def getStrikeFrozenAmount(self):
        '''执行冻结金额'''
        return self.StrikeFrozenAmount

    def getAbandonFrozen(self):
        '''放弃执行冻结'''
        return self.AbandonFrozen

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getYdStrikeFrozen(self):
        '''执行冻结的昨仓'''
        return self.YdStrikeFrozen

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'PosiDirection'={self.getPosiDirection()}, 'HedgeFlag'={self.getHedgeFlag()}, 'PositionDate'={self.getPositionDate()}, 'YdPosition'={self.getYdPosition()}, 'Position'={self.getPosition()}, 'LongFrozen'={self.getLongFrozen()}, 'ShortFrozen'={self.getShortFrozen()}, 'LongFrozenAmount'={self.getLongFrozenAmount()}, 'ShortFrozenAmount'={self.getShortFrozenAmount()}, 'OpenVolume'={self.getOpenVolume()}, 'CloseVolume'={self.getCloseVolume()}, 'OpenAmount'={self.getOpenAmount()}, 'CloseAmount'={self.getCloseAmount()}, 'PositionCost'={self.getPositionCost()}, 'PreMargin'={self.getPreMargin()}, 'UseMargin'={self.getUseMargin()}, 'FrozenMargin'={self.getFrozenMargin()}, 'FrozenCash'={self.getFrozenCash()}, 'FrozenCommission'={self.getFrozenCommission()}, 'CashIn'={self.getCashIn()}, 'Commission'={self.getCommission()}, 'CloseProfit'={self.getCloseProfit()}, 'PositionProfit'={self.getPositionProfit()}, 'PreSettlementPrice'={self.getPreSettlementPrice()}, 'SettlementPrice'={self.getSettlementPrice()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'OpenCost'={self.getOpenCost()}, 'ExchangeMargin'={self.getExchangeMargin()}, 'CombPosition'={self.getCombPosition()}, 'CombLongFrozen'={self.getCombLongFrozen()}, 'CombShortFrozen'={self.getCombShortFrozen()}, 'CloseProfitByDate'={self.getCloseProfitByDate()}, 'CloseProfitByTrade'={self.getCloseProfitByTrade()}, 'TodayPosition'={self.getTodayPosition()}, 'MarginRateByMoney'={self.getMarginRateByMoney()}, 'MarginRateByVolume'={self.getMarginRateByVolume()}, 'StrikeFrozen'={self.getStrikeFrozen()}, 'StrikeFrozenAmount'={self.getStrikeFrozenAmount()}, 'AbandonFrozen'={self.getAbandonFrozen()}, 'ExchangeID'={self.getExchangeID()}, 'YdStrikeFrozen'={self.getYdStrikeFrozen()}, 'InvestUnitID'={self.getInvestUnitID()}, 'OptionValue'={self.getOptionValue()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'PosiDirection': self.getPosiDirection(), 'HedgeFlag': self.getHedgeFlag(), 'PositionDate': self.getPositionDate(), 'YdPosition': self.getYdPosition(), 'Position': self.getPosition(), 'LongFrozen': self.getLongFrozen(), 'ShortFrozen': self.getShortFrozen(), 'LongFrozenAmount': self.getLongFrozenAmount(), 'ShortFrozenAmount': self.getShortFrozenAmount(), 'OpenVolume': self.getOpenVolume(), 'CloseVolume': self.getCloseVolume(), 'OpenAmount': self.getOpenAmount(), 'CloseAmount': self.getCloseAmount(), 'PositionCost': self.getPositionCost(), 'PreMargin': self.getPreMargin(), 'UseMargin': self.getUseMargin(), 'FrozenMargin': self.getFrozenMargin(), 'FrozenCash': self.getFrozenCash(), 'FrozenCommission': self.getFrozenCommission(), 'CashIn': self.getCashIn(), 'Commission': self.getCommission(), 'CloseProfit': self.getCloseProfit(), 'PositionProfit': self.getPositionProfit(), 'PreSettlementPrice': self.getPreSettlementPrice(), 'SettlementPrice': self.getSettlementPrice(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'OpenCost': self.getOpenCost(), 'ExchangeMargin': self.getExchangeMargin(), 'CombPosition': self.getCombPosition(), 'CombLongFrozen': self.getCombLongFrozen(), 'CombShortFrozen': self.getCombShortFrozen(), 'CloseProfitByDate': self.getCloseProfitByDate(), 'CloseProfitByTrade': self.getCloseProfitByTrade(), 'TodayPosition': self.getTodayPosition(), 'MarginRateByMoney': self.getMarginRateByMoney(), 'MarginRateByVolume': self.getMarginRateByVolume(), 'StrikeFrozen': self.getStrikeFrozen(), 'StrikeFrozenAmount': self.getStrikeFrozenAmount(), 'AbandonFrozen': self.getAbandonFrozen(), 'ExchangeID': self.getExchangeID(), 'YdStrikeFrozen': self.getYdStrikeFrozen(), 'InvestUnitID': self.getInvestUnitID(), 'OptionValue': self.getOptionValue()}


class  CShfeFtdcSyncingInstrumentMarginRateField(Structure):
    """正在同步中的合约保证金率"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("IsRelative", c_int32),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getIsRelative(self):
        '''是否相对交易所收取'''
        return self.IsRelative

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'IsRelative'={self.getIsRelative()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'IsRelative': self.getIsRelative()}


class  CShfeFtdcSyncingInstrumentCommissionRateField(Structure):
    """正在同步中的合约手续费率"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("OpenRatioByMoney", c_double),
        ("OpenRatioByVolume", c_double),
        ("CloseRatioByMoney", c_double),
        ("CloseRatioByVolume", c_double),
        ("CloseTodayRatioByMoney", c_double),
        ("CloseTodayRatioByVolume", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getOpenRatioByMoney(self):
        '''开仓手续费率'''
        return self.OpenRatioByMoney

    def getOpenRatioByVolume(self):
        '''开仓手续费'''
        return self.OpenRatioByVolume

    def getCloseRatioByMoney(self):
        '''平仓手续费率'''
        return self.CloseRatioByMoney

    def getCloseRatioByVolume(self):
        '''平仓手续费'''
        return self.CloseRatioByVolume

    def getCloseTodayRatioByMoney(self):
        '''平今手续费率'''
        return self.CloseTodayRatioByMoney

    def getCloseTodayRatioByVolume(self):
        '''平今手续费'''
        return self.CloseTodayRatioByVolume

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'OpenRatioByMoney'={self.getOpenRatioByMoney()}, 'OpenRatioByVolume'={self.getOpenRatioByVolume()}, 'CloseRatioByMoney'={self.getCloseRatioByMoney()}, 'CloseRatioByVolume'={self.getCloseRatioByVolume()}, 'CloseTodayRatioByMoney'={self.getCloseTodayRatioByMoney()}, 'CloseTodayRatioByVolume'={self.getCloseTodayRatioByVolume()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'OpenRatioByMoney': self.getOpenRatioByMoney(), 'OpenRatioByVolume': self.getOpenRatioByVolume(), 'CloseRatioByMoney': self.getCloseRatioByMoney(), 'CloseRatioByVolume': self.getCloseRatioByVolume(), 'CloseTodayRatioByMoney': self.getCloseTodayRatioByMoney(), 'CloseTodayRatioByVolume': self.getCloseTodayRatioByVolume()}


class  CShfeFtdcSyncingInstrumentTradingRightField(Structure):
    """正在同步中的合约交易权限"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("TradingRight", c_char),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getTradingRight(self):
        '''交易权限'''
        return TShfeFtdcTradingRightType(ord(self.TradingRight))

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'TradingRight'={self.getTradingRight()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'TradingRight': self.getTradingRight()}


class  CShfeFtdcQryOrderField(Structure):
    """查询报单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("OrderSysID", c_char*21),
        ("InsertTimeStart", c_char*9),
        ("InsertTimeEnd", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getInsertTimeStart(self):
        '''开始时间'''
        return str(self.InsertTimeStart, 'GBK')

    def getInsertTimeEnd(self):
        '''结束时间'''
        return str(self.InsertTimeEnd, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'OrderSysID'={self.getOrderSysID()}, 'InsertTimeStart'={self.getInsertTimeStart()}, 'InsertTimeEnd'={self.getInsertTimeEnd()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID(), 'OrderSysID': self.getOrderSysID(), 'InsertTimeStart': self.getInsertTimeStart(), 'InsertTimeEnd': self.getInsertTimeEnd()}


class  CShfeFtdcQryTradeField(Structure):
    """查询成交"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("TradeID", c_char*21),
        ("TradeTimeStart", c_char*9),
        ("TradeTimeEnd", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTradeID(self):
        '''成交编号'''
        return str(self.TradeID, 'GBK')

    def getTradeTimeStart(self):
        '''开始时间'''
        return str(self.TradeTimeStart, 'GBK')

    def getTradeTimeEnd(self):
        '''结束时间'''
        return str(self.TradeTimeEnd, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'TradeID'={self.getTradeID()}, 'TradeTimeStart'={self.getTradeTimeStart()}, 'TradeTimeEnd'={self.getTradeTimeEnd()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID(), 'TradeID': self.getTradeID(), 'TradeTimeStart': self.getTradeTimeStart(), 'TradeTimeEnd': self.getTradeTimeEnd()}


class  CShfeFtdcQryInvestorPositionField(Structure):
    """查询投资者持仓"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcQryTradingAccountField(Structure):
    """查询资金账户"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("CurrencyID", c_char*4),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcQryInvestorField(Structure):
    """查询投资者"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcQryTradingCodeField(Structure):
    """查询交易编码"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("ExchangeID", c_char*9),
        ("ClientID", c_char*11),
        ("ClientIDType", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getClientIDType(self):
        '''交易编码类型'''
        return TShfeFtdcClientIDTypeType(ord(self.ClientIDType))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'ExchangeID'={self.getExchangeID()}, 'ClientID'={self.getClientID()}, 'ClientIDType'={self.getClientIDType()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'ExchangeID': self.getExchangeID(), 'ClientID': self.getClientID(), 'ClientIDType': self.getClientIDType()}


class  CShfeFtdcQryInvestorGroupField(Structure):
    """查询交易编码"""
    _fields_ = [
        ("BrokerID", c_char*11),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID()}


class  CShfeFtdcQryInstrumentMarginRateField(Structure):
    """查询交易编码"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("HedgeFlag", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'HedgeFlag'={self.getHedgeFlag()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'HedgeFlag': self.getHedgeFlag()}


class  CShfeFtdcQryInstrumentCommissionRateField(Structure):
    """查询手续费率"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcQryInstrumentTradingRightField(Structure):
    """查询交易编码"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcQryBrokerField(Structure):
    """查询经纪公司"""
    _fields_ = [
        ("BrokerID", c_char*11),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID()}


class  CShfeFtdcQryTraderField(Structure):
    """查询交易员"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("TraderID", c_char*21),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'TraderID'={self.getTraderID()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'TraderID': self.getTraderID()}


class  CShfeFtdcQrySuperUserFunctionField(Structure):
    """查询管理用户功能权限"""
    _fields_ = [
        ("UserID", c_char*16),
    ]

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    @property
    def __str__(self):
        return f"'UserID'={self.getUserID()}"

    @property
    def __dict__(self):
        return {'UserID': self.getUserID()}


class  CShfeFtdcQryUserSessionField(Structure):
    """查询用户会话"""
    _fields_ = [
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
    ]

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    @property
    def __str__(self):
        return f"'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}"

    @property
    def __dict__(self):
        return {'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID()}


class  CShfeFtdcQryPartBrokerField(Structure):
    """查询经纪公司会员代码"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("BrokerID", c_char*11),
        ("ParticipantID", c_char*11),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'BrokerID'={self.getBrokerID()}, 'ParticipantID'={self.getParticipantID()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'BrokerID': self.getBrokerID(), 'ParticipantID': self.getParticipantID()}


class  CShfeFtdcQryFrontStatusField(Structure):
    """查询前置状态"""
    _fields_ = [
        ("FrontID", c_int32),
    ]

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    @property
    def __str__(self):
        return f"'FrontID'={self.getFrontID()}"

    @property
    def __dict__(self):
        return {'FrontID': self.getFrontID()}


class  CShfeFtdcQryExchangeOrderField(Structure):
    """查询交易所报单"""
    _fields_ = [
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("ExchangeInstID", c_char*31),
        ("ExchangeID", c_char*9),
        ("TraderID", c_char*21),
    ]

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    @property
    def __str__(self):
        return f"'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'ExchangeID'={self.getExchangeID()}, 'TraderID'={self.getTraderID()}"

    @property
    def __dict__(self):
        return {'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'ExchangeInstID': self.getExchangeInstID(), 'ExchangeID': self.getExchangeID(), 'TraderID': self.getTraderID()}


class  CShfeFtdcQryOrderActionField(Structure):
    """查询报单操作"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("ExchangeID", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'ExchangeID'={self.getExchangeID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'ExchangeID': self.getExchangeID()}


class  CShfeFtdcQryExchangeOrderActionField(Structure):
    """查询交易所报单操作"""
    _fields_ = [
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("ExchangeID", c_char*9),
        ("TraderID", c_char*21),
    ]

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    @property
    def __str__(self):
        return f"'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'ExchangeID'={self.getExchangeID()}, 'TraderID'={self.getTraderID()}"

    @property
    def __dict__(self):
        return {'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'ExchangeID': self.getExchangeID(), 'TraderID': self.getTraderID()}


class  CShfeFtdcQrySuperUserField(Structure):
    """查询管理用户"""
    _fields_ = [
        ("UserID", c_char*16),
    ]

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    @property
    def __str__(self):
        return f"'UserID'={self.getUserID()}"

    @property
    def __dict__(self):
        return {'UserID': self.getUserID()}


class  CShfeFtdcQryExchangeField(Structure):
    """查询交易所"""
    _fields_ = [
        ("ExchangeID", c_char*9),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID()}


class  CShfeFtdcQryProductField(Structure):
    """查询产品"""
    _fields_ = [
        ("ProductID", c_char*31),
        ("ProductClass", c_char),
    ]

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getProductClass(self):
        '''产品类型'''
        return TShfeFtdcProductClassType(ord(self.ProductClass))

    @property
    def __str__(self):
        return f"'ProductID'={self.getProductID()}, 'ProductClass'={self.getProductClass()}"

    @property
    def __dict__(self):
        return {'ProductID': self.getProductID(), 'ProductClass': self.getProductClass()}


class  CShfeFtdcQryInstrumentField(Structure):
    """查询合约"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("ExchangeInstID", c_char*31),
        ("ProductID", c_char*31),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'ProductID'={self.getProductID()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID(), 'ExchangeInstID': self.getExchangeInstID(), 'ProductID': self.getProductID()}


class  CShfeFtdcQryDepthMarketDataField(Structure):
    """查询行情"""
    _fields_ = [
        ("InstrumentID", c_char*31),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcQryBrokerUserField(Structure):
    """查询经纪公司用户"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID()}


class  CShfeFtdcQryBrokerUserFunctionField(Structure):
    """查询经纪公司用户权限"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID()}


class  CShfeFtdcQryTraderOfferField(Structure):
    """查询交易员报盘机"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("TraderID", c_char*21),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'TraderID'={self.getTraderID()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'TraderID': self.getTraderID()}


class  CShfeFtdcQrySyncDepositField(Structure):
    """查询出入金流水"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("DepositSeqNo", c_char*15),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getDepositSeqNo(self):
        '''出入金流水号'''
        return str(self.DepositSeqNo, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'DepositSeqNo'={self.getDepositSeqNo()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'DepositSeqNo': self.getDepositSeqNo()}


class  CShfeFtdcQrySettlementInfoField(Structure):
    """查询投资者结算结果"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("TradingDay", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'TradingDay'={self.getTradingDay()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'TradingDay': self.getTradingDay()}


class  CShfeFtdcQryHisOrderField(Structure):
    """查询报单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("OrderSysID", c_char*21),
        ("InsertTimeStart", c_char*9),
        ("InsertTimeEnd", c_char*9),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getInsertTimeStart(self):
        '''开始时间'''
        return str(self.InsertTimeStart, 'GBK')

    def getInsertTimeEnd(self):
        '''结束时间'''
        return str(self.InsertTimeEnd, 'GBK')

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'OrderSysID'={self.getOrderSysID()}, 'InsertTimeStart'={self.getInsertTimeStart()}, 'InsertTimeEnd'={self.getInsertTimeEnd()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID(), 'OrderSysID': self.getOrderSysID(), 'InsertTimeStart': self.getInsertTimeStart(), 'InsertTimeEnd': self.getInsertTimeEnd(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID()}


class  CShfeFtdcInvestorDepartmentFlatField(Structure):
    """组织架构投资者对应关系扁平表"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("DepartmentID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getDepartmentID(self):
        '''组织架构代码'''
        return str(self.DepartmentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'DepartmentID'={self.getDepartmentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'DepartmentID': self.getDepartmentID()}


class  CShfeFtdcDepartmentUserField(Structure):
    """操作员组织架构关系"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorRange", c_char),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcDepartmentRangeType(ord(self.InvestorRange))

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorRange'={self.getInvestorRange()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorRange': self.getInvestorRange(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcDepartmentField(Structure):
    """组织架构"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("DepartmentID", c_char*13),
        ("DepartmentName", c_char*81),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getDepartmentID(self):
        '''组织架构代码'''
        return str(self.DepartmentID, 'GBK')

    def getDepartmentName(self):
        '''组织架构名称'''
        return str(self.DepartmentName, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'DepartmentID'={self.getDepartmentID()}, 'DepartmentName'={self.getDepartmentName()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'DepartmentID': self.getDepartmentID(), 'DepartmentName': self.getDepartmentName()}


class  CShfeFtdcQueryBrokerDepositField(Structure):
    """查询经纪公司资金"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("ExchangeID", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'ExchangeID'={self.getExchangeID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'ExchangeID': self.getExchangeID()}


class  CShfeFtdcBrokerDepositField(Structure):
    """经纪公司资金"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("BrokerID", c_char*11),
        ("ParticipantID", c_char*11),
        ("ExchangeID", c_char*9),
        ("PreBalance", c_double),
        ("CurrMargin", c_double),
        ("CloseProfit", c_double),
        ("Balance", c_double),
        ("Deposit", c_double),
        ("Withdraw", c_double),
        ("Available", c_double),
        ("Reserve", c_double),
        ("FrozenMargin", c_double),
    ]

    def getTradingDay(self):
        '''交易日期'''
        return str(self.TradingDay, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getPreBalance(self):
        '''上次结算准备金'''
        return self.PreBalance

    def getCurrMargin(self):
        '''当前保证金总额'''
        return self.CurrMargin

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getBalance(self):
        '''期货结算准备金'''
        return self.Balance

    def getDeposit(self):
        '''入金金额'''
        return self.Deposit

    def getWithdraw(self):
        '''出金金额'''
        return self.Withdraw

    def getAvailable(self):
        '''可提资金'''
        return self.Available

    def getReserve(self):
        '''基本准备金'''
        return self.Reserve

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'BrokerID'={self.getBrokerID()}, 'ParticipantID'={self.getParticipantID()}, 'ExchangeID'={self.getExchangeID()}, 'PreBalance'={self.getPreBalance()}, 'CurrMargin'={self.getCurrMargin()}, 'CloseProfit'={self.getCloseProfit()}, 'Balance'={self.getBalance()}, 'Deposit'={self.getDeposit()}, 'Withdraw'={self.getWithdraw()}, 'Available'={self.getAvailable()}, 'Reserve'={self.getReserve()}, 'FrozenMargin'={self.getFrozenMargin()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'BrokerID': self.getBrokerID(), 'ParticipantID': self.getParticipantID(), 'ExchangeID': self.getExchangeID(), 'PreBalance': self.getPreBalance(), 'CurrMargin': self.getCurrMargin(), 'CloseProfit': self.getCloseProfit(), 'Balance': self.getBalance(), 'Deposit': self.getDeposit(), 'Withdraw': self.getWithdraw(), 'Available': self.getAvailable(), 'Reserve': self.getReserve(), 'FrozenMargin': self.getFrozenMargin()}


class  CShfeFtdcMarketDataField(Structure):
    """市场行情"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("ExchangeInstID", c_char*31),
        ("LastPrice", c_double),
        ("PreSettlementPrice", c_double),
        ("PreClosePrice", c_double),
        ("PreOpenInterest", c_double),
        ("OpenPrice", c_double),
        ("HighestPrice", c_double),
        ("LowestPrice", c_double),
        ("Volume", c_int32),
        ("Turnover", c_double),
        ("OpenInterest", c_double),
        ("ClosePrice", c_double),
        ("SettlementPrice", c_double),
        ("UpperLimitPrice", c_double),
        ("LowerLimitPrice", c_double),
        ("PreDelta", c_double),
        ("CurrDelta", c_double),
        ("UpdateTime", c_char*9),
        ("UpdateMillisec", c_int32),
        ("ActionDay", c_char*9),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getLastPrice(self):
        '''最新价'''
        return self.LastPrice

    def getPreSettlementPrice(self):
        '''上次结算价'''
        return self.PreSettlementPrice

    def getPreClosePrice(self):
        '''昨收盘'''
        return self.PreClosePrice

    def getPreOpenInterest(self):
        '''昨持仓量'''
        return self.PreOpenInterest

    def getOpenPrice(self):
        '''今开盘'''
        return self.OpenPrice

    def getHighestPrice(self):
        '''最高价'''
        return self.HighestPrice

    def getLowestPrice(self):
        '''最低价'''
        return self.LowestPrice

    def getVolume(self):
        '''数量'''
        return self.Volume

    def getTurnover(self):
        '''成交金额'''
        return self.Turnover

    def getOpenInterest(self):
        '''持仓量'''
        return self.OpenInterest

    def getClosePrice(self):
        '''今收盘'''
        return self.ClosePrice

    def getSettlementPrice(self):
        '''本次结算价'''
        return self.SettlementPrice

    def getUpperLimitPrice(self):
        '''涨停板价'''
        return self.UpperLimitPrice

    def getLowerLimitPrice(self):
        '''跌停板价'''
        return self.LowerLimitPrice

    def getPreDelta(self):
        '''昨虚实度'''
        return self.PreDelta

    def getCurrDelta(self):
        '''今虚实度'''
        return self.CurrDelta

    def getUpdateTime(self):
        '''最后修改时间'''
        return str(self.UpdateTime, 'GBK')

    def getUpdateMillisec(self):
        '''最后修改毫秒'''
        return self.UpdateMillisec

    def getActionDay(self):
        '''业务日期'''
        return str(self.ActionDay, 'GBK')

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'LastPrice'={self.getLastPrice()}, 'PreSettlementPrice'={self.getPreSettlementPrice()}, 'PreClosePrice'={self.getPreClosePrice()}, 'PreOpenInterest'={self.getPreOpenInterest()}, 'OpenPrice'={self.getOpenPrice()}, 'HighestPrice'={self.getHighestPrice()}, 'LowestPrice'={self.getLowestPrice()}, 'Volume'={self.getVolume()}, 'Turnover'={self.getTurnover()}, 'OpenInterest'={self.getOpenInterest()}, 'ClosePrice'={self.getClosePrice()}, 'SettlementPrice'={self.getSettlementPrice()}, 'UpperLimitPrice'={self.getUpperLimitPrice()}, 'LowerLimitPrice'={self.getLowerLimitPrice()}, 'PreDelta'={self.getPreDelta()}, 'CurrDelta'={self.getCurrDelta()}, 'UpdateTime'={self.getUpdateTime()}, 'UpdateMillisec'={self.getUpdateMillisec()}, 'ActionDay'={self.getActionDay()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID(), 'ExchangeInstID': self.getExchangeInstID(), 'LastPrice': self.getLastPrice(), 'PreSettlementPrice': self.getPreSettlementPrice(), 'PreClosePrice': self.getPreClosePrice(), 'PreOpenInterest': self.getPreOpenInterest(), 'OpenPrice': self.getOpenPrice(), 'HighestPrice': self.getHighestPrice(), 'LowestPrice': self.getLowestPrice(), 'Volume': self.getVolume(), 'Turnover': self.getTurnover(), 'OpenInterest': self.getOpenInterest(), 'ClosePrice': self.getClosePrice(), 'SettlementPrice': self.getSettlementPrice(), 'UpperLimitPrice': self.getUpperLimitPrice(), 'LowerLimitPrice': self.getLowerLimitPrice(), 'PreDelta': self.getPreDelta(), 'CurrDelta': self.getCurrDelta(), 'UpdateTime': self.getUpdateTime(), 'UpdateMillisec': self.getUpdateMillisec(), 'ActionDay': self.getActionDay()}


class  CShfeFtdcMarketDataBaseField(Structure):
    """行情基础属性"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("PreSettlementPrice", c_double),
        ("PreClosePrice", c_double),
        ("PreOpenInterest", c_double),
        ("PreDelta", c_double),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getPreSettlementPrice(self):
        '''上次结算价'''
        return self.PreSettlementPrice

    def getPreClosePrice(self):
        '''昨收盘'''
        return self.PreClosePrice

    def getPreOpenInterest(self):
        '''昨持仓量'''
        return self.PreOpenInterest

    def getPreDelta(self):
        '''昨虚实度'''
        return self.PreDelta

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'PreSettlementPrice'={self.getPreSettlementPrice()}, 'PreClosePrice'={self.getPreClosePrice()}, 'PreOpenInterest'={self.getPreOpenInterest()}, 'PreDelta'={self.getPreDelta()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'PreSettlementPrice': self.getPreSettlementPrice(), 'PreClosePrice': self.getPreClosePrice(), 'PreOpenInterest': self.getPreOpenInterest(), 'PreDelta': self.getPreDelta()}


class  CShfeFtdcMarketDataStaticField(Structure):
    """行情静态属性"""
    _fields_ = [
        ("OpenPrice", c_double),
        ("HighestPrice", c_double),
        ("LowestPrice", c_double),
        ("ClosePrice", c_double),
        ("UpperLimitPrice", c_double),
        ("LowerLimitPrice", c_double),
        ("SettlementPrice", c_double),
        ("CurrDelta", c_double),
    ]

    def getOpenPrice(self):
        '''今开盘'''
        return self.OpenPrice

    def getHighestPrice(self):
        '''最高价'''
        return self.HighestPrice

    def getLowestPrice(self):
        '''最低价'''
        return self.LowestPrice

    def getClosePrice(self):
        '''今收盘'''
        return self.ClosePrice

    def getUpperLimitPrice(self):
        '''涨停板价'''
        return self.UpperLimitPrice

    def getLowerLimitPrice(self):
        '''跌停板价'''
        return self.LowerLimitPrice

    def getSettlementPrice(self):
        '''本次结算价'''
        return self.SettlementPrice

    def getCurrDelta(self):
        '''今虚实度'''
        return self.CurrDelta

    @property
    def __str__(self):
        return f"'OpenPrice'={self.getOpenPrice()}, 'HighestPrice'={self.getHighestPrice()}, 'LowestPrice'={self.getLowestPrice()}, 'ClosePrice'={self.getClosePrice()}, 'UpperLimitPrice'={self.getUpperLimitPrice()}, 'LowerLimitPrice'={self.getLowerLimitPrice()}, 'SettlementPrice'={self.getSettlementPrice()}, 'CurrDelta'={self.getCurrDelta()}"

    @property
    def __dict__(self):
        return {'OpenPrice': self.getOpenPrice(), 'HighestPrice': self.getHighestPrice(), 'LowestPrice': self.getLowestPrice(), 'ClosePrice': self.getClosePrice(), 'UpperLimitPrice': self.getUpperLimitPrice(), 'LowerLimitPrice': self.getLowerLimitPrice(), 'SettlementPrice': self.getSettlementPrice(), 'CurrDelta': self.getCurrDelta()}


class  CShfeFtdcMarketDataLastMatchField(Structure):
    """行情最新成交属性"""
    _fields_ = [
        ("LastPrice", c_double),
        ("Volume", c_int32),
        ("Turnover", c_double),
        ("OpenInterest", c_double),
    ]

    def getLastPrice(self):
        '''最新价'''
        return self.LastPrice

    def getVolume(self):
        '''数量'''
        return self.Volume

    def getTurnover(self):
        '''成交金额'''
        return self.Turnover

    def getOpenInterest(self):
        '''持仓量'''
        return self.OpenInterest

    @property
    def __str__(self):
        return f"'LastPrice'={self.getLastPrice()}, 'Volume'={self.getVolume()}, 'Turnover'={self.getTurnover()}, 'OpenInterest'={self.getOpenInterest()}"

    @property
    def __dict__(self):
        return {'LastPrice': self.getLastPrice(), 'Volume': self.getVolume(), 'Turnover': self.getTurnover(), 'OpenInterest': self.getOpenInterest()}


class  CShfeFtdcMarketDataBestPriceField(Structure):
    """行情最优价属性"""
    _fields_ = [
        ("BidPrice1", c_double),
        ("BidVolume1", c_int32),
        ("AskPrice1", c_double),
        ("AskVolume1", c_int32),
    ]

    def getBidPrice1(self):
        '''申买价一'''
        return self.BidPrice1

    def getBidVolume1(self):
        '''申买量一'''
        return self.BidVolume1

    def getAskPrice1(self):
        '''申卖价一'''
        return self.AskPrice1

    def getAskVolume1(self):
        '''申卖量一'''
        return self.AskVolume1

    @property
    def __str__(self):
        return f"'BidPrice1'={self.getBidPrice1()}, 'BidVolume1'={self.getBidVolume1()}, 'AskPrice1'={self.getAskPrice1()}, 'AskVolume1'={self.getAskVolume1()}"

    @property
    def __dict__(self):
        return {'BidPrice1': self.getBidPrice1(), 'BidVolume1': self.getBidVolume1(), 'AskPrice1': self.getAskPrice1(), 'AskVolume1': self.getAskVolume1()}


class  CShfeFtdcMarketDataBid23Field(Structure):
    """行情申买二、三属性"""
    _fields_ = [
        ("BidPrice2", c_double),
        ("BidVolume2", c_int32),
        ("BidPrice3", c_double),
        ("BidVolume3", c_int32),
    ]

    def getBidPrice2(self):
        '''申买价二'''
        return self.BidPrice2

    def getBidVolume2(self):
        '''申买量二'''
        return self.BidVolume2

    def getBidPrice3(self):
        '''申买价三'''
        return self.BidPrice3

    def getBidVolume3(self):
        '''申买量三'''
        return self.BidVolume3

    @property
    def __str__(self):
        return f"'BidPrice2'={self.getBidPrice2()}, 'BidVolume2'={self.getBidVolume2()}, 'BidPrice3'={self.getBidPrice3()}, 'BidVolume3'={self.getBidVolume3()}"

    @property
    def __dict__(self):
        return {'BidPrice2': self.getBidPrice2(), 'BidVolume2': self.getBidVolume2(), 'BidPrice3': self.getBidPrice3(), 'BidVolume3': self.getBidVolume3()}


class  CShfeFtdcMarketDataAsk23Field(Structure):
    """行情申卖二、三属性"""
    _fields_ = [
        ("AskPrice2", c_double),
        ("AskVolume2", c_int32),
        ("AskPrice3", c_double),
        ("AskVolume3", c_int32),
    ]

    def getAskPrice2(self):
        '''申卖价二'''
        return self.AskPrice2

    def getAskVolume2(self):
        '''申卖量二'''
        return self.AskVolume2

    def getAskPrice3(self):
        '''申卖价三'''
        return self.AskPrice3

    def getAskVolume3(self):
        '''申卖量三'''
        return self.AskVolume3

    @property
    def __str__(self):
        return f"'AskPrice2'={self.getAskPrice2()}, 'AskVolume2'={self.getAskVolume2()}, 'AskPrice3'={self.getAskPrice3()}, 'AskVolume3'={self.getAskVolume3()}"

    @property
    def __dict__(self):
        return {'AskPrice2': self.getAskPrice2(), 'AskVolume2': self.getAskVolume2(), 'AskPrice3': self.getAskPrice3(), 'AskVolume3': self.getAskVolume3()}


class  CShfeFtdcMarketDataBid45Field(Structure):
    """行情申买四、五属性"""
    _fields_ = [
        ("BidPrice4", c_double),
        ("BidVolume4", c_int32),
        ("BidPrice5", c_double),
        ("BidVolume5", c_int32),
    ]

    def getBidPrice4(self):
        '''申买价四'''
        return self.BidPrice4

    def getBidVolume4(self):
        '''申买量四'''
        return self.BidVolume4

    def getBidPrice5(self):
        '''申买价五'''
        return self.BidPrice5

    def getBidVolume5(self):
        '''申买量五'''
        return self.BidVolume5

    @property
    def __str__(self):
        return f"'BidPrice4'={self.getBidPrice4()}, 'BidVolume4'={self.getBidVolume4()}, 'BidPrice5'={self.getBidPrice5()}, 'BidVolume5'={self.getBidVolume5()}"

    @property
    def __dict__(self):
        return {'BidPrice4': self.getBidPrice4(), 'BidVolume4': self.getBidVolume4(), 'BidPrice5': self.getBidPrice5(), 'BidVolume5': self.getBidVolume5()}


class  CShfeFtdcMarketDataAsk45Field(Structure):
    """行情申卖四、五属性"""
    _fields_ = [
        ("AskPrice4", c_double),
        ("AskVolume4", c_int32),
        ("AskPrice5", c_double),
        ("AskVolume5", c_int32),
    ]

    def getAskPrice4(self):
        '''申卖价四'''
        return self.AskPrice4

    def getAskVolume4(self):
        '''申卖量四'''
        return self.AskVolume4

    def getAskPrice5(self):
        '''申卖价五'''
        return self.AskPrice5

    def getAskVolume5(self):
        '''申卖量五'''
        return self.AskVolume5

    @property
    def __str__(self):
        return f"'AskPrice4'={self.getAskPrice4()}, 'AskVolume4'={self.getAskVolume4()}, 'AskPrice5'={self.getAskPrice5()}, 'AskVolume5'={self.getAskVolume5()}"

    @property
    def __dict__(self):
        return {'AskPrice4': self.getAskPrice4(), 'AskVolume4': self.getAskVolume4(), 'AskPrice5': self.getAskPrice5(), 'AskVolume5': self.getAskVolume5()}


class  CShfeFtdcMarketDataUpdateTimeField(Structure):
    """行情更新时间属性"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("UpdateTime", c_char*9),
        ("UpdateMillisec", c_int32),
        ("ActionDay", c_char*9),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getUpdateTime(self):
        '''最后修改时间'''
        return str(self.UpdateTime, 'GBK')

    def getUpdateMillisec(self):
        '''最后修改毫秒'''
        return self.UpdateMillisec

    def getActionDay(self):
        '''业务日期'''
        return str(self.ActionDay, 'GBK')

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'UpdateTime'={self.getUpdateTime()}, 'UpdateMillisec'={self.getUpdateMillisec()}, 'ActionDay'={self.getActionDay()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'UpdateTime': self.getUpdateTime(), 'UpdateMillisec': self.getUpdateMillisec(), 'ActionDay': self.getActionDay()}


class  CShfeFtdcSpecificInstrumentField(Structure):
    """指定的合约"""
    _fields_ = [
        ("InstrumentID", c_char*31),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcInstrumentStatusField(Structure):
    """合约状态"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("ExchangeInstID", c_char*31),
        ("SettlementGroupID", c_char*9),
        ("InstrumentID", c_char*31),
        ("InstrumentStatus", c_char),
        ("TradingSegmentSN", c_int32),
        ("EnterTime", c_char*9),
        ("EnterReason", c_char),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getSettlementGroupID(self):
        '''结算组代码'''
        return str(self.SettlementGroupID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInstrumentStatus(self):
        '''合约交易状态'''
        return TShfeFtdcInstrumentStatusType(ord(self.InstrumentStatus))

    def getTradingSegmentSN(self):
        '''交易阶段编号'''
        return self.TradingSegmentSN

    def getEnterTime(self):
        '''进入本状态时间'''
        return str(self.EnterTime, 'GBK')

    def getEnterReason(self):
        '''进入本状态原因'''
        return TShfeFtdcInstStatusEnterReasonType(ord(self.EnterReason))

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'SettlementGroupID'={self.getSettlementGroupID()}, 'InstrumentID'={self.getInstrumentID()}, 'InstrumentStatus'={self.getInstrumentStatus()}, 'TradingSegmentSN'={self.getTradingSegmentSN()}, 'EnterTime'={self.getEnterTime()}, 'EnterReason'={self.getEnterReason()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'ExchangeInstID': self.getExchangeInstID(), 'SettlementGroupID': self.getSettlementGroupID(), 'InstrumentID': self.getInstrumentID(), 'InstrumentStatus': self.getInstrumentStatus(), 'TradingSegmentSN': self.getTradingSegmentSN(), 'EnterTime': self.getEnterTime(), 'EnterReason': self.getEnterReason()}


class  CShfeFtdcQryInstrumentStatusField(Structure):
    """查询合约状态"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("ExchangeInstID", c_char*31),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'ExchangeInstID'={self.getExchangeInstID()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'ExchangeInstID': self.getExchangeInstID()}


class  CShfeFtdcInvestorAccountField(Structure):
    """投资者账户"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcPositionProfitAlgorithmField(Structure):
    """浮动盈亏算法"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("AccountID", c_char*13),
        ("Algorithm", c_char),
        ("Memo", c_char*161),
        ("CurrencyID", c_char*4),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getAlgorithm(self):
        '''盈亏算法'''
        return TShfeFtdcAlgorithmType(ord(self.Algorithm))

    def getMemo(self):
        '''备注'''
        return str(self.Memo, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'AccountID'={self.getAccountID()}, 'Algorithm'={self.getAlgorithm()}, 'Memo'={self.getMemo()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'AccountID': self.getAccountID(), 'Algorithm': self.getAlgorithm(), 'Memo': self.getMemo(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcDiscountField(Structure):
    """会员资金折扣"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorRange", c_char),
        ("InvestorID", c_char*13),
        ("Discount", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getDiscount(self):
        '''资金折扣比例'''
        return self.Discount

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorRange'={self.getInvestorRange()}, 'InvestorID'={self.getInvestorID()}, 'Discount'={self.getDiscount()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorRange': self.getInvestorRange(), 'InvestorID': self.getInvestorID(), 'Discount': self.getDiscount()}


class  CShfeFtdcQryTransferBankField(Structure):
    """查询转帐银行"""
    _fields_ = [
        ("BankID", c_char*4),
        ("BankBrchID", c_char*5),
    ]

    def getBankID(self):
        '''银行代码'''
        return str(self.BankID, 'GBK')

    def getBankBrchID(self):
        '''银行分中心代码'''
        return str(self.BankBrchID, 'GBK')

    @property
    def __str__(self):
        return f"'BankID'={self.getBankID()}, 'BankBrchID'={self.getBankBrchID()}"

    @property
    def __dict__(self):
        return {'BankID': self.getBankID(), 'BankBrchID': self.getBankBrchID()}


class  CShfeFtdcTransferBankField(Structure):
    """转帐银行"""
    _fields_ = [
        ("BankID", c_char*4),
        ("BankBrchID", c_char*5),
        ("BankName", c_char*101),
        ("IsActive", c_int32),
    ]

    def getBankID(self):
        '''银行代码'''
        return str(self.BankID, 'GBK')

    def getBankBrchID(self):
        '''银行分中心代码'''
        return str(self.BankBrchID, 'GBK')

    def getBankName(self):
        '''银行名称'''
        return str(self.BankName, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    @property
    def __str__(self):
        return f"'BankID'={self.getBankID()}, 'BankBrchID'={self.getBankBrchID()}, 'BankName'={self.getBankName()}, 'IsActive'={self.getIsActive()}"

    @property
    def __dict__(self):
        return {'BankID': self.getBankID(), 'BankBrchID': self.getBankBrchID(), 'BankName': self.getBankName(), 'IsActive': self.getIsActive()}


class  CShfeFtdcQryInvestorPositionDetailField(Structure):
    """查询投资者持仓明细"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcInvestorPositionDetailField(Structure):
    """投资者持仓明细"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("HedgeFlag", c_char),
        ("Direction", c_char),
        ("OpenDate", c_char*9),
        ("TradeID", c_char*21),
        ("Volume", c_int32),
        ("OpenPrice", c_double),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("TradeType", c_char),
        ("CombInstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("CloseProfitByDate", c_double),
        ("CloseProfitByTrade", c_double),
        ("PositionProfitByDate", c_double),
        ("PositionProfitByTrade", c_double),
        ("Margin", c_double),
        ("ExchMargin", c_double),
        ("MarginRateByMoney", c_double),
        ("MarginRateByVolume", c_double),
        ("LastSettlementPrice", c_double),
        ("SettlementPrice", c_double),
        ("CloseVolume", c_int32),
        ("CloseAmount", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getDirection(self):
        '''买卖'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getOpenDate(self):
        '''开仓日期'''
        return str(self.OpenDate, 'GBK')

    def getTradeID(self):
        '''成交编号'''
        return str(self.TradeID, 'GBK')

    def getVolume(self):
        '''数量'''
        return self.Volume

    def getOpenPrice(self):
        '''开仓价'''
        return self.OpenPrice

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getTradeType(self):
        '''成交类型'''
        return TShfeFtdcTradeTypeType(ord(self.TradeType))

    def getCombInstrumentID(self):
        '''组合合约代码'''
        return str(self.CombInstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getCloseProfitByDate(self):
        '''逐日盯市平仓盈亏'''
        return self.CloseProfitByDate

    def getCloseProfitByTrade(self):
        '''逐笔对冲平仓盈亏'''
        return self.CloseProfitByTrade

    def getPositionProfitByDate(self):
        '''逐日盯市持仓盈亏'''
        return self.PositionProfitByDate

    def getPositionProfitByTrade(self):
        '''逐笔对冲持仓盈亏'''
        return self.PositionProfitByTrade

    def getMargin(self):
        '''投资者保证金'''
        return self.Margin

    def getExchMargin(self):
        '''交易所保证金'''
        return self.ExchMargin

    def getMarginRateByMoney(self):
        '''保证金率'''
        return self.MarginRateByMoney

    def getMarginRateByVolume(self):
        '''保证金率(按手数)'''
        return self.MarginRateByVolume

    def getLastSettlementPrice(self):
        '''昨结算价'''
        return self.LastSettlementPrice

    def getSettlementPrice(self):
        '''结算价'''
        return self.SettlementPrice

    def getCloseVolume(self):
        '''平仓量'''
        return self.CloseVolume

    def getCloseAmount(self):
        '''平仓金额'''
        return self.CloseAmount

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'Direction'={self.getDirection()}, 'OpenDate'={self.getOpenDate()}, 'TradeID'={self.getTradeID()}, 'Volume'={self.getVolume()}, 'OpenPrice'={self.getOpenPrice()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'TradeType'={self.getTradeType()}, 'CombInstrumentID'={self.getCombInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'CloseProfitByDate'={self.getCloseProfitByDate()}, 'CloseProfitByTrade'={self.getCloseProfitByTrade()}, 'PositionProfitByDate'={self.getPositionProfitByDate()}, 'PositionProfitByTrade'={self.getPositionProfitByTrade()}, 'Margin'={self.getMargin()}, 'ExchMargin'={self.getExchMargin()}, 'MarginRateByMoney'={self.getMarginRateByMoney()}, 'MarginRateByVolume'={self.getMarginRateByVolume()}, 'LastSettlementPrice'={self.getLastSettlementPrice()}, 'SettlementPrice'={self.getSettlementPrice()}, 'CloseVolume'={self.getCloseVolume()}, 'CloseAmount'={self.getCloseAmount()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'HedgeFlag': self.getHedgeFlag(), 'Direction': self.getDirection(), 'OpenDate': self.getOpenDate(), 'TradeID': self.getTradeID(), 'Volume': self.getVolume(), 'OpenPrice': self.getOpenPrice(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'TradeType': self.getTradeType(), 'CombInstrumentID': self.getCombInstrumentID(), 'ExchangeID': self.getExchangeID(), 'CloseProfitByDate': self.getCloseProfitByDate(), 'CloseProfitByTrade': self.getCloseProfitByTrade(), 'PositionProfitByDate': self.getPositionProfitByDate(), 'PositionProfitByTrade': self.getPositionProfitByTrade(), 'Margin': self.getMargin(), 'ExchMargin': self.getExchMargin(), 'MarginRateByMoney': self.getMarginRateByMoney(), 'MarginRateByVolume': self.getMarginRateByVolume(), 'LastSettlementPrice': self.getLastSettlementPrice(), 'SettlementPrice': self.getSettlementPrice(), 'CloseVolume': self.getCloseVolume(), 'CloseAmount': self.getCloseAmount()}


class  CShfeFtdcTradingAccountPasswordField(Structure):
    """资金账户口令域"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("AccountID", c_char*13),
        ("Password", c_char*41),
        ("CurrencyID", c_char*4),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'AccountID'={self.getAccountID()}, 'Password'={self.getPassword()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'AccountID': self.getAccountID(), 'Password': self.getPassword(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcMDTraderOfferField(Structure):
    """交易所行情报盘机"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("TraderID", c_char*21),
        ("ParticipantID", c_char*11),
        ("Password", c_char*41),
        ("InstallID", c_int32),
        ("OrderLocalID", c_char*13),
        ("TraderConnectStatus", c_char),
        ("ConnectRequestDate", c_char*9),
        ("ConnectRequestTime", c_char*9),
        ("LastReportDate", c_char*9),
        ("LastReportTime", c_char*9),
        ("ConnectDate", c_char*9),
        ("ConnectTime", c_char*9),
        ("StartDate", c_char*9),
        ("StartTime", c_char*9),
        ("TradingDay", c_char*9),
        ("BrokerID", c_char*11),
        ("MaxTradeID", c_char*21),
        ("MaxOrderMessageReference", c_char*7),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getTraderConnectStatus(self):
        '''交易所交易员连接状态'''
        return TShfeFtdcTraderConnectStatusType(ord(self.TraderConnectStatus))

    def getConnectRequestDate(self):
        '''发出连接请求的日期'''
        return str(self.ConnectRequestDate, 'GBK')

    def getConnectRequestTime(self):
        '''发出连接请求的时间'''
        return str(self.ConnectRequestTime, 'GBK')

    def getLastReportDate(self):
        '''上次报告日期'''
        return str(self.LastReportDate, 'GBK')

    def getLastReportTime(self):
        '''上次报告时间'''
        return str(self.LastReportTime, 'GBK')

    def getConnectDate(self):
        '''完成连接日期'''
        return str(self.ConnectDate, 'GBK')

    def getConnectTime(self):
        '''完成连接时间'''
        return str(self.ConnectTime, 'GBK')

    def getStartDate(self):
        '''启动日期'''
        return str(self.StartDate, 'GBK')

    def getStartTime(self):
        '''启动时间'''
        return str(self.StartTime, 'GBK')

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getMaxTradeID(self):
        '''本席位最大成交编号'''
        return str(self.MaxTradeID, 'GBK')

    def getMaxOrderMessageReference(self):
        '''本席位最大报单备拷'''
        return str(self.MaxOrderMessageReference, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'TraderID'={self.getTraderID()}, 'ParticipantID'={self.getParticipantID()}, 'Password'={self.getPassword()}, 'InstallID'={self.getInstallID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'TraderConnectStatus'={self.getTraderConnectStatus()}, 'ConnectRequestDate'={self.getConnectRequestDate()}, 'ConnectRequestTime'={self.getConnectRequestTime()}, 'LastReportDate'={self.getLastReportDate()}, 'LastReportTime'={self.getLastReportTime()}, 'ConnectDate'={self.getConnectDate()}, 'ConnectTime'={self.getConnectTime()}, 'StartDate'={self.getStartDate()}, 'StartTime'={self.getStartTime()}, 'TradingDay'={self.getTradingDay()}, 'BrokerID'={self.getBrokerID()}, 'MaxTradeID'={self.getMaxTradeID()}, 'MaxOrderMessageReference'={self.getMaxOrderMessageReference()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'TraderID': self.getTraderID(), 'ParticipantID': self.getParticipantID(), 'Password': self.getPassword(), 'InstallID': self.getInstallID(), 'OrderLocalID': self.getOrderLocalID(), 'TraderConnectStatus': self.getTraderConnectStatus(), 'ConnectRequestDate': self.getConnectRequestDate(), 'ConnectRequestTime': self.getConnectRequestTime(), 'LastReportDate': self.getLastReportDate(), 'LastReportTime': self.getLastReportTime(), 'ConnectDate': self.getConnectDate(), 'ConnectTime': self.getConnectTime(), 'StartDate': self.getStartDate(), 'StartTime': self.getStartTime(), 'TradingDay': self.getTradingDay(), 'BrokerID': self.getBrokerID(), 'MaxTradeID': self.getMaxTradeID(), 'MaxOrderMessageReference': self.getMaxOrderMessageReference()}


class  CShfeFtdcQryMDTraderOfferField(Structure):
    """查询行情报盘机"""
    _fields_ = [
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("TraderID", c_char*21),
    ]

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    @property
    def __str__(self):
        return f"'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'TraderID'={self.getTraderID()}"

    @property
    def __dict__(self):
        return {'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'TraderID': self.getTraderID()}


class  CShfeFtdcQryNoticeField(Structure):
    """查询客户通知"""
    _fields_ = [
        ("BrokerID", c_char*11),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID()}


class  CShfeFtdcNoticeField(Structure):
    """客户通知"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("Content", c_char*501),
        ("SequenceLabel", c_char*2),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getContent(self):
        '''消息正文'''
        return str(self.Content, 'GBK')

    def getSequenceLabel(self):
        '''经纪公司通知内容序列号'''
        return str(self.SequenceLabel, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'Content'={self.getContent()}, 'SequenceLabel'={self.getSequenceLabel()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'Content': self.getContent(), 'SequenceLabel': self.getSequenceLabel()}


class  CShfeFtdcUserRightField(Structure):
    """用户权限"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("UserRightType", c_char),
        ("IsForbidden", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getUserRightType(self):
        '''客户权限类型'''
        return TShfeFtdcUserRightTypeType(ord(self.UserRightType))

    def getIsForbidden(self):
        '''是否禁止'''
        return self.IsForbidden

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'UserRightType'={self.getUserRightType()}, 'IsForbidden'={self.getIsForbidden()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'UserRightType': self.getUserRightType(), 'IsForbidden': self.getIsForbidden()}


class  CShfeFtdcQrySettlementInfoConfirmField(Structure):
    """查询结算信息确认域"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcLoadSettlementInfoField(Structure):
    """装载结算信息"""
    _fields_ = [
        ("BrokerID", c_char*11),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID()}


class  CShfeFtdcBrokerWithdrawAlgorithmField(Structure):
    """经纪公司可提资金算法表"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("WithdrawAlgorithm", c_char),
        ("UsingRatio", c_double),
        ("IncludeCloseProfit", c_char),
        ("AllWithoutTrade", c_char),
        ("AvailIncludeCloseProfit", c_char),
        ("IsBrokerUserEvent", c_int32),
        ("CurrencyID", c_char*4),
        ("FundMortgageRatio", c_double),
        ("BalanceAlgorithm", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getWithdrawAlgorithm(self):
        '''可提资金算法'''
        return TShfeFtdcAlgorithmType(ord(self.WithdrawAlgorithm))

    def getUsingRatio(self):
        '''资金使用率'''
        return self.UsingRatio

    def getIncludeCloseProfit(self):
        '''可提是否包含平仓盈利'''
        return TShfeFtdcIncludeCloseProfitType(ord(self.IncludeCloseProfit))

    def getAllWithoutTrade(self):
        '''本日无仓且无成交客户是否受可提比例限制'''
        return TShfeFtdcAllWithoutTradeType(ord(self.AllWithoutTrade))

    def getAvailIncludeCloseProfit(self):
        '''可用是否包含平仓盈利'''
        return TShfeFtdcIncludeCloseProfitType(ord(self.AvailIncludeCloseProfit))

    def getIsBrokerUserEvent(self):
        '''是否启用用户事件'''
        return self.IsBrokerUserEvent

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getFundMortgageRatio(self):
        '''货币质押比率'''
        return self.FundMortgageRatio

    def getBalanceAlgorithm(self):
        '''权益算法'''
        return TShfeFtdcBalanceAlgorithmType(ord(self.BalanceAlgorithm))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'WithdrawAlgorithm'={self.getWithdrawAlgorithm()}, 'UsingRatio'={self.getUsingRatio()}, 'IncludeCloseProfit'={self.getIncludeCloseProfit()}, 'AllWithoutTrade'={self.getAllWithoutTrade()}, 'AvailIncludeCloseProfit'={self.getAvailIncludeCloseProfit()}, 'IsBrokerUserEvent'={self.getIsBrokerUserEvent()}, 'CurrencyID'={self.getCurrencyID()}, 'FundMortgageRatio'={self.getFundMortgageRatio()}, 'BalanceAlgorithm'={self.getBalanceAlgorithm()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'WithdrawAlgorithm': self.getWithdrawAlgorithm(), 'UsingRatio': self.getUsingRatio(), 'IncludeCloseProfit': self.getIncludeCloseProfit(), 'AllWithoutTrade': self.getAllWithoutTrade(), 'AvailIncludeCloseProfit': self.getAvailIncludeCloseProfit(), 'IsBrokerUserEvent': self.getIsBrokerUserEvent(), 'CurrencyID': self.getCurrencyID(), 'FundMortgageRatio': self.getFundMortgageRatio(), 'BalanceAlgorithm': self.getBalanceAlgorithm()}


class  CShfeFtdcTradingAccountPasswordUpdateV1Field(Structure):
    """资金账户口令变更域"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("OldPassword", c_char*41),
        ("NewPassword", c_char*41),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getOldPassword(self):
        '''原来的口令'''
        return str(self.OldPassword, 'GBK')

    def getNewPassword(self):
        '''新的口令'''
        return str(self.NewPassword, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'OldPassword'={self.getOldPassword()}, 'NewPassword'={self.getNewPassword()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'OldPassword': self.getOldPassword(), 'NewPassword': self.getNewPassword()}


class  CShfeFtdcTradingAccountPasswordUpdateField(Structure):
    """资金账户口令变更域"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("AccountID", c_char*13),
        ("OldPassword", c_char*41),
        ("NewPassword", c_char*41),
        ("CurrencyID", c_char*4),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getOldPassword(self):
        '''原来的口令'''
        return str(self.OldPassword, 'GBK')

    def getNewPassword(self):
        '''新的口令'''
        return str(self.NewPassword, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'AccountID'={self.getAccountID()}, 'OldPassword'={self.getOldPassword()}, 'NewPassword'={self.getNewPassword()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'AccountID': self.getAccountID(), 'OldPassword': self.getOldPassword(), 'NewPassword': self.getNewPassword(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcQryCombinationLegField(Structure):
    """查询组合合约分腿"""
    _fields_ = [
        ("CombInstrumentID", c_char*31),
        ("LegID", c_int32),
        ("LegInstrumentID", c_char*31),
    ]

    def getCombInstrumentID(self):
        '''组合合约代码'''
        return str(self.CombInstrumentID, 'GBK')

    def getLegID(self):
        '''单腿编号'''
        return self.LegID

    def getLegInstrumentID(self):
        '''单腿合约代码'''
        return str(self.LegInstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'CombInstrumentID'={self.getCombInstrumentID()}, 'LegID'={self.getLegID()}, 'LegInstrumentID'={self.getLegInstrumentID()}"

    @property
    def __dict__(self):
        return {'CombInstrumentID': self.getCombInstrumentID(), 'LegID': self.getLegID(), 'LegInstrumentID': self.getLegInstrumentID()}


class  CShfeFtdcQrySyncStatusField(Structure):
    """查询组合合约分腿"""
    _fields_ = [
        ("TradingDay", c_char*9),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay()}


class  CShfeFtdcCombinationLegField(Structure):
    """组合交易合约的单腿"""
    _fields_ = [
        ("CombInstrumentID", c_char*31),
        ("LegID", c_int32),
        ("LegInstrumentID", c_char*31),
        ("Direction", c_char),
        ("LegMultiple", c_int32),
        ("ImplyLevel", c_int32),
    ]

    def getCombInstrumentID(self):
        '''组合合约代码'''
        return str(self.CombInstrumentID, 'GBK')

    def getLegID(self):
        '''单腿编号'''
        return self.LegID

    def getLegInstrumentID(self):
        '''单腿合约代码'''
        return str(self.LegInstrumentID, 'GBK')

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getLegMultiple(self):
        '''单腿乘数'''
        return self.LegMultiple

    def getImplyLevel(self):
        '''派生层数'''
        return self.ImplyLevel

    @property
    def __str__(self):
        return f"'CombInstrumentID'={self.getCombInstrumentID()}, 'LegID'={self.getLegID()}, 'LegInstrumentID'={self.getLegInstrumentID()}, 'Direction'={self.getDirection()}, 'LegMultiple'={self.getLegMultiple()}, 'ImplyLevel'={self.getImplyLevel()}"

    @property
    def __dict__(self):
        return {'CombInstrumentID': self.getCombInstrumentID(), 'LegID': self.getLegID(), 'LegInstrumentID': self.getLegInstrumentID(), 'Direction': self.getDirection(), 'LegMultiple': self.getLegMultiple(), 'ImplyLevel': self.getImplyLevel()}


class  CShfeFtdcSyncStatusField(Structure):
    """数据同步状态"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("DataSyncStatus", c_char),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getDataSyncStatus(self):
        '''数据同步状态'''
        return TShfeFtdcDataSyncStatusType(ord(self.DataSyncStatus))

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'DataSyncStatus'={self.getDataSyncStatus()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'DataSyncStatus': self.getDataSyncStatus()}


class  CShfeFtdcQryLinkManField(Structure):
    """查询联系人"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcLinkManField(Structure):
    """联系人"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("PersonType", c_char),
        ("IdentifiedCardType", c_char),
        ("IdentifiedCardNo", c_char*51),
        ("PersonName", c_char*81),
        ("Telephone", c_char*41),
        ("Address", c_char*101),
        ("ZipCode", c_char*7),
        ("Priority", c_int32),
        ("UOAZipCode", c_char*11),
        ("PersonFullName", c_char*101),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPersonType(self):
        '''联系人类型'''
        return TShfeFtdcPersonTypeType(ord(self.PersonType))

    def getIdentifiedCardType(self):
        '''证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.IdentifiedCardType))

    def getIdentifiedCardNo(self):
        '''证件号码'''
        return str(self.IdentifiedCardNo, 'GBK')

    def getPersonName(self):
        '''名称'''
        return str(self.PersonName, 'GBK')

    def getTelephone(self):
        '''联系电话'''
        return str(self.Telephone, 'GBK')

    def getAddress(self):
        '''通讯地址'''
        return str(self.Address, 'GBK')

    def getZipCode(self):
        '''邮政编码'''
        return str(self.ZipCode, 'GBK')

    def getPriority(self):
        '''优先级'''
        return self.Priority

    def getUOAZipCode(self):
        '''开户邮政编码'''
        return str(self.UOAZipCode, 'GBK')

    def getPersonFullName(self):
        '''全称'''
        return str(self.PersonFullName, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'PersonType'={self.getPersonType()}, 'IdentifiedCardType'={self.getIdentifiedCardType()}, 'IdentifiedCardNo'={self.getIdentifiedCardNo()}, 'PersonName'={self.getPersonName()}, 'Telephone'={self.getTelephone()}, 'Address'={self.getAddress()}, 'ZipCode'={self.getZipCode()}, 'Priority'={self.getPriority()}, 'UOAZipCode'={self.getUOAZipCode()}, 'PersonFullName'={self.getPersonFullName()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'PersonType': self.getPersonType(), 'IdentifiedCardType': self.getIdentifiedCardType(), 'IdentifiedCardNo': self.getIdentifiedCardNo(), 'PersonName': self.getPersonName(), 'Telephone': self.getTelephone(), 'Address': self.getAddress(), 'ZipCode': self.getZipCode(), 'Priority': self.getPriority(), 'UOAZipCode': self.getUOAZipCode(), 'PersonFullName': self.getPersonFullName()}


class  CShfeFtdcQryBrokerUserEventField(Structure):
    """查询经纪公司用户事件"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("UserEventType", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getUserEventType(self):
        '''用户事件类型'''
        return TShfeFtdcUserEventTypeType(ord(self.UserEventType))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'UserEventType'={self.getUserEventType()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'UserEventType': self.getUserEventType()}


class  CShfeFtdcBrokerUserEventField(Structure):
    """查询经纪公司用户事件"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("UserEventType", c_char),
        ("EventSequenceNo", c_int32),
        ("EventDate", c_char*9),
        ("EventTime", c_char*9),
        ("UserEventInfo", c_char*1025),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getUserEventType(self):
        '''用户事件类型'''
        return TShfeFtdcUserEventTypeType(ord(self.UserEventType))

    def getEventSequenceNo(self):
        '''用户事件序号'''
        return self.EventSequenceNo

    def getEventDate(self):
        '''事件发生日期'''
        return str(self.EventDate, 'GBK')

    def getEventTime(self):
        '''事件发生时间'''
        return str(self.EventTime, 'GBK')

    def getUserEventInfo(self):
        '''用户事件信息'''
        return str(self.UserEventInfo, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'UserEventType'={self.getUserEventType()}, 'EventSequenceNo'={self.getEventSequenceNo()}, 'EventDate'={self.getEventDate()}, 'EventTime'={self.getEventTime()}, 'UserEventInfo'={self.getUserEventInfo()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'UserEventType': self.getUserEventType(), 'EventSequenceNo': self.getEventSequenceNo(), 'EventDate': self.getEventDate(), 'EventTime': self.getEventTime(), 'UserEventInfo': self.getUserEventInfo(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcQryContractBankField(Structure):
    """查询签约银行请求"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("BankID", c_char*4),
        ("BankBrchID", c_char*5),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getBankID(self):
        '''银行代码'''
        return str(self.BankID, 'GBK')

    def getBankBrchID(self):
        '''银行分中心代码'''
        return str(self.BankBrchID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'BankID'={self.getBankID()}, 'BankBrchID'={self.getBankBrchID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'BankID': self.getBankID(), 'BankBrchID': self.getBankBrchID()}


class  CShfeFtdcContractBankField(Structure):
    """查询签约银行响应"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("BankID", c_char*4),
        ("BankBrchID", c_char*5),
        ("BankName", c_char*101),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getBankID(self):
        '''银行代码'''
        return str(self.BankID, 'GBK')

    def getBankBrchID(self):
        '''银行分中心代码'''
        return str(self.BankBrchID, 'GBK')

    def getBankName(self):
        '''银行名称'''
        return str(self.BankName, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'BankID'={self.getBankID()}, 'BankBrchID'={self.getBankBrchID()}, 'BankName'={self.getBankName()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'BankID': self.getBankID(), 'BankBrchID': self.getBankBrchID(), 'BankName': self.getBankName()}


class  CShfeFtdcInvestorPositionCombineDetailField(Structure):
    """投资者组合持仓明细"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("OpenDate", c_char*9),
        ("ExchangeID", c_char*9),
        ("SettlementID", c_int32),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("ComTradeID", c_char*21),
        ("TradeID", c_char*21),
        ("InstrumentID", c_char*31),
        ("HedgeFlag", c_char),
        ("Direction", c_char),
        ("TotalAmt", c_int32),
        ("Margin", c_double),
        ("ExchMargin", c_double),
        ("MarginRateByMoney", c_double),
        ("MarginRateByVolume", c_double),
        ("LegID", c_int32),
        ("LegMultiple", c_int32),
        ("CombInstrumentID", c_char*31),
        ("TradeGroupID", c_int32),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getOpenDate(self):
        '''开仓日期'''
        return str(self.OpenDate, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getComTradeID(self):
        '''组合编号'''
        return str(self.ComTradeID, 'GBK')

    def getTradeID(self):
        '''撮合编号'''
        return str(self.TradeID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getDirection(self):
        '''买卖'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getTotalAmt(self):
        '''持仓量'''
        return self.TotalAmt

    def getMargin(self):
        '''投资者保证金'''
        return self.Margin

    def getExchMargin(self):
        '''交易所保证金'''
        return self.ExchMargin

    def getMarginRateByMoney(self):
        '''保证金率'''
        return self.MarginRateByMoney

    def getMarginRateByVolume(self):
        '''保证金率(按手数)'''
        return self.MarginRateByVolume

    def getLegID(self):
        '''单腿编号'''
        return self.LegID

    def getLegMultiple(self):
        '''单腿乘数'''
        return self.LegMultiple

    def getCombInstrumentID(self):
        '''组合持仓合约编码'''
        return str(self.CombInstrumentID, 'GBK')

    def getTradeGroupID(self):
        '''成交组号'''
        return self.TradeGroupID

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'OpenDate'={self.getOpenDate()}, 'ExchangeID'={self.getExchangeID()}, 'SettlementID'={self.getSettlementID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'ComTradeID'={self.getComTradeID()}, 'TradeID'={self.getTradeID()}, 'InstrumentID'={self.getInstrumentID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'Direction'={self.getDirection()}, 'TotalAmt'={self.getTotalAmt()}, 'Margin'={self.getMargin()}, 'ExchMargin'={self.getExchMargin()}, 'MarginRateByMoney'={self.getMarginRateByMoney()}, 'MarginRateByVolume'={self.getMarginRateByVolume()}, 'LegID'={self.getLegID()}, 'LegMultiple'={self.getLegMultiple()}, 'CombInstrumentID'={self.getCombInstrumentID()}, 'TradeGroupID'={self.getTradeGroupID()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'OpenDate': self.getOpenDate(), 'ExchangeID': self.getExchangeID(), 'SettlementID': self.getSettlementID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'ComTradeID': self.getComTradeID(), 'TradeID': self.getTradeID(), 'InstrumentID': self.getInstrumentID(), 'HedgeFlag': self.getHedgeFlag(), 'Direction': self.getDirection(), 'TotalAmt': self.getTotalAmt(), 'Margin': self.getMargin(), 'ExchMargin': self.getExchMargin(), 'MarginRateByMoney': self.getMarginRateByMoney(), 'MarginRateByVolume': self.getMarginRateByVolume(), 'LegID': self.getLegID(), 'LegMultiple': self.getLegMultiple(), 'CombInstrumentID': self.getCombInstrumentID(), 'TradeGroupID': self.getTradeGroupID()}


class  CShfeFtdcParkedOrderField(Structure):
    """预埋单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("UserForceClose", c_int32),
        ("ExchangeID", c_char*9),
        ("ParkedOrderID", c_char*13),
        ("UserType", c_char),
        ("Status", c_char),
        ("ErrorID", c_int32),
        ("ErrorMsg", c_char*81),
        ("IsSwapOrder", c_int32),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("ClientID", c_char*11),
        ("InvestUnitID", c_char*17),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getUserForceClose(self):
        '''用户强评标志'''
        return self.UserForceClose

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParkedOrderID(self):
        '''预埋报单编号'''
        return str(self.ParkedOrderID, 'GBK')

    def getUserType(self):
        '''用户类型'''
        return TShfeFtdcUserTypeType(ord(self.UserType))

    def getStatus(self):
        '''预埋单状态'''
        return TShfeFtdcParkedOrderStatusType(ord(self.Status))

    def getErrorID(self):
        '''错误代码'''
        return self.ErrorID

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    def getIsSwapOrder(self):
        '''互换单标志'''
        return self.IsSwapOrder

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getClientID(self):
        '''交易编码'''
        return str(self.ClientID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'UserForceClose'={self.getUserForceClose()}, 'ExchangeID'={self.getExchangeID()}, 'ParkedOrderID'={self.getParkedOrderID()}, 'UserType'={self.getUserType()}, 'Status'={self.getStatus()}, 'ErrorID'={self.getErrorID()}, 'ErrorMsg'={self.getErrorMsg()}, 'IsSwapOrder'={self.getIsSwapOrder()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'ClientID'={self.getClientID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'UserForceClose': self.getUserForceClose(), 'ExchangeID': self.getExchangeID(), 'ParkedOrderID': self.getParkedOrderID(), 'UserType': self.getUserType(), 'Status': self.getStatus(), 'ErrorID': self.getErrorID(), 'ErrorMsg': self.getErrorMsg(), 'IsSwapOrder': self.getIsSwapOrder(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'ClientID': self.getClientID(), 'InvestUnitID': self.getInvestUnitID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcParkedOrderActionField(Structure):
    """输入预埋单操作"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("OrderActionRef", c_int32),
        ("OrderRef", c_char*13),
        ("RequestID", c_int32),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("ExchangeID", c_char*9),
        ("OrderSysID", c_char*21),
        ("ActionFlag", c_char),
        ("LimitPrice", c_double),
        ("VolumeChange", c_int32),
        ("UserID", c_char*16),
        ("InstrumentID", c_char*31),
        ("ParkedOrderActionID", c_char*13),
        ("UserType", c_char),
        ("Status", c_char),
        ("ErrorID", c_int32),
        ("ErrorMsg", c_char*81),
        ("InvestUnitID", c_char*17),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getOrderActionRef(self):
        '''报单操作引用'''
        return self.OrderActionRef

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getActionFlag(self):
        '''操作标志'''
        return TShfeFtdcActionFlagType(ord(self.ActionFlag))

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeChange(self):
        '''数量变化'''
        return self.VolumeChange

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getParkedOrderActionID(self):
        '''预埋撤单单编号'''
        return str(self.ParkedOrderActionID, 'GBK')

    def getUserType(self):
        '''用户类型'''
        return TShfeFtdcUserTypeType(ord(self.UserType))

    def getStatus(self):
        '''预埋撤单状态'''
        return TShfeFtdcParkedOrderStatusType(ord(self.Status))

    def getErrorID(self):
        '''错误代码'''
        return self.ErrorID

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'OrderActionRef'={self.getOrderActionRef()}, 'OrderRef'={self.getOrderRef()}, 'RequestID'={self.getRequestID()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'ExchangeID'={self.getExchangeID()}, 'OrderSysID'={self.getOrderSysID()}, 'ActionFlag'={self.getActionFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeChange'={self.getVolumeChange()}, 'UserID'={self.getUserID()}, 'InstrumentID'={self.getInstrumentID()}, 'ParkedOrderActionID'={self.getParkedOrderActionID()}, 'UserType'={self.getUserType()}, 'Status'={self.getStatus()}, 'ErrorID'={self.getErrorID()}, 'ErrorMsg'={self.getErrorMsg()}, 'InvestUnitID'={self.getInvestUnitID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'OrderActionRef': self.getOrderActionRef(), 'OrderRef': self.getOrderRef(), 'RequestID': self.getRequestID(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'ExchangeID': self.getExchangeID(), 'OrderSysID': self.getOrderSysID(), 'ActionFlag': self.getActionFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeChange': self.getVolumeChange(), 'UserID': self.getUserID(), 'InstrumentID': self.getInstrumentID(), 'ParkedOrderActionID': self.getParkedOrderActionID(), 'UserType': self.getUserType(), 'Status': self.getStatus(), 'ErrorID': self.getErrorID(), 'ErrorMsg': self.getErrorMsg(), 'InvestUnitID': self.getInvestUnitID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcQryParkedOrderField(Structure):
    """查询预埋单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID()}


class  CShfeFtdcQryParkedOrderActionField(Structure):
    """查询预埋撤单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID()}


class  CShfeFtdcRemoveParkedOrderField(Structure):
    """删除预埋单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("ParkedOrderID", c_char*13),
        ("InvestUnitID", c_char*17),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getParkedOrderID(self):
        '''预埋报单编号'''
        return str(self.ParkedOrderID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'ParkedOrderID'={self.getParkedOrderID()}, 'InvestUnitID'={self.getInvestUnitID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'ParkedOrderID': self.getParkedOrderID(), 'InvestUnitID': self.getInvestUnitID()}


class  CShfeFtdcRemoveParkedOrderActionField(Structure):
    """删除预埋撤单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("ParkedOrderActionID", c_char*13),
        ("InvestUnitID", c_char*17),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getParkedOrderActionID(self):
        '''预埋撤单编号'''
        return str(self.ParkedOrderActionID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'ParkedOrderActionID'={self.getParkedOrderActionID()}, 'InvestUnitID'={self.getInvestUnitID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'ParkedOrderActionID': self.getParkedOrderActionID(), 'InvestUnitID': self.getInvestUnitID()}


class  CShfeFtdcInvestorWithdrawAlgorithmField(Structure):
    """经纪公司可提资金算法表"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorRange", c_char),
        ("InvestorID", c_char*13),
        ("UsingRatio", c_double),
        ("CurrencyID", c_char*4),
        ("FundMortgageRatio", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getUsingRatio(self):
        '''可提资金比例'''
        return self.UsingRatio

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getFundMortgageRatio(self):
        '''货币质押比率'''
        return self.FundMortgageRatio

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorRange'={self.getInvestorRange()}, 'InvestorID'={self.getInvestorID()}, 'UsingRatio'={self.getUsingRatio()}, 'CurrencyID'={self.getCurrencyID()}, 'FundMortgageRatio'={self.getFundMortgageRatio()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorRange': self.getInvestorRange(), 'InvestorID': self.getInvestorID(), 'UsingRatio': self.getUsingRatio(), 'CurrencyID': self.getCurrencyID(), 'FundMortgageRatio': self.getFundMortgageRatio()}


class  CShfeFtdcQryInvestorPositionCombineDetailField(Structure):
    """查询组合持仓明细"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("CombInstrumentID", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getCombInstrumentID(self):
        '''组合持仓合约编码'''
        return str(self.CombInstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'CombInstrumentID'={self.getCombInstrumentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'CombInstrumentID': self.getCombInstrumentID()}


class  CShfeFtdcMarketDataAveragePriceField(Structure):
    """成交均价"""
    _fields_ = [
        ("AveragePrice", c_double),
    ]

    def getAveragePrice(self):
        '''当日均价'''
        return self.AveragePrice

    @property
    def __str__(self):
        return f"'AveragePrice'={self.getAveragePrice()}"

    @property
    def __dict__(self):
        return {'AveragePrice': self.getAveragePrice()}


class  CShfeFtdcVerifyInvestorPasswordField(Structure):
    """校验投资者密码"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("Password", c_char*41),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'Password'={self.getPassword()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'Password': self.getPassword()}


class  CShfeFtdcUserIPField(Structure):
    """用户IP"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("IPAddress", c_char*16),
        ("IPMask", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getIPMask(self):
        '''IP地址掩码'''
        return str(self.IPMask, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'IPAddress'={self.getIPAddress()}, 'IPMask'={self.getIPMask()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'IPAddress': self.getIPAddress(), 'IPMask': self.getIPMask(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcTradingNoticeInfoField(Structure):
    """用户事件通知信息"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("SendTime", c_char*9),
        ("FieldContent", c_char*501),
        ("SequenceSeries", c_short),
        ("SequenceNo", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getSendTime(self):
        '''发送时间'''
        return str(self.SendTime, 'GBK')

    def getFieldContent(self):
        '''消息正文'''
        return str(self.FieldContent, 'GBK')

    def getSequenceSeries(self):
        '''序列系列号'''
        return self.SequenceSeries

    def getSequenceNo(self):
        '''序列号'''
        return self.SequenceNo

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'SendTime'={self.getSendTime()}, 'FieldContent'={self.getFieldContent()}, 'SequenceSeries'={self.getSequenceSeries()}, 'SequenceNo'={self.getSequenceNo()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'SendTime': self.getSendTime(), 'FieldContent': self.getFieldContent(), 'SequenceSeries': self.getSequenceSeries(), 'SequenceNo': self.getSequenceNo()}


class  CShfeFtdcTradingNoticeField(Structure):
    """用户事件通知"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorRange", c_char),
        ("InvestorID", c_char*13),
        ("SequenceSeries", c_short),
        ("UserID", c_char*16),
        ("SendTime", c_char*9),
        ("SequenceNo", c_int32),
        ("FieldContent", c_char*501),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getSequenceSeries(self):
        '''序列系列号'''
        return self.SequenceSeries

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getSendTime(self):
        '''发送时间'''
        return str(self.SendTime, 'GBK')

    def getSequenceNo(self):
        '''序列号'''
        return self.SequenceNo

    def getFieldContent(self):
        '''消息正文'''
        return str(self.FieldContent, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorRange'={self.getInvestorRange()}, 'InvestorID'={self.getInvestorID()}, 'SequenceSeries'={self.getSequenceSeries()}, 'UserID'={self.getUserID()}, 'SendTime'={self.getSendTime()}, 'SequenceNo'={self.getSequenceNo()}, 'FieldContent'={self.getFieldContent()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorRange': self.getInvestorRange(), 'InvestorID': self.getInvestorID(), 'SequenceSeries': self.getSequenceSeries(), 'UserID': self.getUserID(), 'SendTime': self.getSendTime(), 'SequenceNo': self.getSequenceNo(), 'FieldContent': self.getFieldContent()}


class  CShfeFtdcQryTradingNoticeField(Structure):
    """查询交易事件通知"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcQryErrOrderField(Structure):
    """查询错误报单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcErrOrderField(Structure):
    """错误报单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("UserForceClose", c_int32),
        ("ErrorID", c_int32),
        ("ErrorMsg", c_char*81),
        ("IsSwapOrder", c_int32),
        ("ExchangeID", c_char*9),
        ("InvestUnitID", c_char*17),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("ClientID", c_char*11),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getUserForceClose(self):
        '''用户强评标志'''
        return self.UserForceClose

    def getErrorID(self):
        '''错误代码'''
        return self.ErrorID

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    def getIsSwapOrder(self):
        '''互换单标志'''
        return self.IsSwapOrder

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getClientID(self):
        '''交易编码'''
        return str(self.ClientID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'UserForceClose'={self.getUserForceClose()}, 'ErrorID'={self.getErrorID()}, 'ErrorMsg'={self.getErrorMsg()}, 'IsSwapOrder'={self.getIsSwapOrder()}, 'ExchangeID'={self.getExchangeID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'ClientID'={self.getClientID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'UserForceClose': self.getUserForceClose(), 'ErrorID': self.getErrorID(), 'ErrorMsg': self.getErrorMsg(), 'IsSwapOrder': self.getIsSwapOrder(), 'ExchangeID': self.getExchangeID(), 'InvestUnitID': self.getInvestUnitID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'ClientID': self.getClientID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcQryErrOrderActionField(Structure):
    """查询错误报单操作"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcErrOrderActionField(Structure):
    """错误报单操作"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("OrderActionRef", c_int32),
        ("OrderRef", c_char*13),
        ("RequestID", c_int32),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("ExchangeID", c_char*9),
        ("OrderSysID", c_char*21),
        ("ActionFlag", c_char),
        ("LimitPrice", c_double),
        ("VolumeChange", c_int32),
        ("ActionDate", c_char*9),
        ("ActionTime", c_char*9),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderLocalID", c_char*13),
        ("ActionLocalID", c_char*13),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("BusinessUnit", c_char*21),
        ("OrderActionStatus", c_char),
        ("UserID", c_char*16),
        ("StatusMsg", c_char*81),
        ("InstrumentID", c_char*31),
        ("BranchID", c_char*9),
        ("InvestUnitID", c_char*17),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
        ("ErrorID", c_int32),
        ("ErrorMsg", c_char*81),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getOrderActionRef(self):
        '''报单操作引用'''
        return self.OrderActionRef

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getActionFlag(self):
        '''操作标志'''
        return TShfeFtdcActionFlagType(ord(self.ActionFlag))

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeChange(self):
        '''数量变化'''
        return self.VolumeChange

    def getActionDate(self):
        '''操作日期'''
        return str(self.ActionDate, 'GBK')

    def getActionTime(self):
        '''操作时间'''
        return str(self.ActionTime, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getActionLocalID(self):
        '''操作本地编号'''
        return str(self.ActionLocalID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getOrderActionStatus(self):
        '''报单操作状态'''
        return TShfeFtdcOrderActionStatusType(ord(self.OrderActionStatus))

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getStatusMsg(self):
        '''状态信息'''
        return str(self.StatusMsg, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBranchID(self):
        '''营业部编号'''
        return str(self.BranchID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    def getErrorID(self):
        '''错误代码'''
        return self.ErrorID

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'OrderActionRef'={self.getOrderActionRef()}, 'OrderRef'={self.getOrderRef()}, 'RequestID'={self.getRequestID()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'ExchangeID'={self.getExchangeID()}, 'OrderSysID'={self.getOrderSysID()}, 'ActionFlag'={self.getActionFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeChange'={self.getVolumeChange()}, 'ActionDate'={self.getActionDate()}, 'ActionTime'={self.getActionTime()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ActionLocalID'={self.getActionLocalID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'BusinessUnit'={self.getBusinessUnit()}, 'OrderActionStatus'={self.getOrderActionStatus()}, 'UserID'={self.getUserID()}, 'StatusMsg'={self.getStatusMsg()}, 'InstrumentID'={self.getInstrumentID()}, 'BranchID'={self.getBranchID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}, 'ErrorID'={self.getErrorID()}, 'ErrorMsg'={self.getErrorMsg()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'OrderActionRef': self.getOrderActionRef(), 'OrderRef': self.getOrderRef(), 'RequestID': self.getRequestID(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'ExchangeID': self.getExchangeID(), 'OrderSysID': self.getOrderSysID(), 'ActionFlag': self.getActionFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeChange': self.getVolumeChange(), 'ActionDate': self.getActionDate(), 'ActionTime': self.getActionTime(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderLocalID': self.getOrderLocalID(), 'ActionLocalID': self.getActionLocalID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'BusinessUnit': self.getBusinessUnit(), 'OrderActionStatus': self.getOrderActionStatus(), 'UserID': self.getUserID(), 'StatusMsg': self.getStatusMsg(), 'InstrumentID': self.getInstrumentID(), 'BranchID': self.getBranchID(), 'InvestUnitID': self.getInvestUnitID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress(), 'ErrorID': self.getErrorID(), 'ErrorMsg': self.getErrorMsg()}


class  CShfeFtdcInvestorSumInfoField(Structure):
    """投资者信息摘要"""
    _fields_ = [
        ("Count", c_int32),
        ("md5_1", c_char),
        ("md5_2", c_char),
        ("md5_3", c_char),
        ("md5_4", c_char),
        ("md5_5", c_char),
        ("md5_6", c_char),
        ("md5_7", c_char),
        ("md5_8", c_char),
        ("md5_9", c_char),
        ("md5_10", c_char),
        ("md5_11", c_char),
        ("md5_12", c_char),
        ("md5_13", c_char),
        ("md5_14", c_char),
        ("md5_15", c_char),
        ("md5_16", c_char),
    ]

    def getCount(self):
        '''投资者人数'''
        return self.Count

    def getmd5_1(self):
        '''MD5校验码1'''
        return TShfeFtdcMD5Type(ord(self.md5_1))

    def getmd5_2(self):
        '''MD5校验码2'''
        return TShfeFtdcMD5Type(ord(self.md5_2))

    def getmd5_3(self):
        '''MD5校验码3'''
        return TShfeFtdcMD5Type(ord(self.md5_3))

    def getmd5_4(self):
        '''MD5校验码4'''
        return TShfeFtdcMD5Type(ord(self.md5_4))

    def getmd5_5(self):
        '''MD5校验码5'''
        return TShfeFtdcMD5Type(ord(self.md5_5))

    def getmd5_6(self):
        '''MD5校验码6'''
        return TShfeFtdcMD5Type(ord(self.md5_6))

    def getmd5_7(self):
        '''MD5校验码7'''
        return TShfeFtdcMD5Type(ord(self.md5_7))

    def getmd5_8(self):
        '''MD5校验码8'''
        return TShfeFtdcMD5Type(ord(self.md5_8))

    def getmd5_9(self):
        '''MD5校验码9'''
        return TShfeFtdcMD5Type(ord(self.md5_9))

    def getmd5_10(self):
        '''MD5校验码10'''
        return TShfeFtdcMD5Type(ord(self.md5_10))

    def getmd5_11(self):
        '''MD5校验码11'''
        return TShfeFtdcMD5Type(ord(self.md5_11))

    def getmd5_12(self):
        '''MD5校验码12'''
        return TShfeFtdcMD5Type(ord(self.md5_12))

    def getmd5_13(self):
        '''MD5校验码13'''
        return TShfeFtdcMD5Type(ord(self.md5_13))

    def getmd5_14(self):
        '''MD5校验码14'''
        return TShfeFtdcMD5Type(ord(self.md5_14))

    def getmd5_15(self):
        '''MD5校验码15'''
        return TShfeFtdcMD5Type(ord(self.md5_15))

    def getmd5_16(self):
        '''MD5校验码16'''
        return TShfeFtdcMD5Type(ord(self.md5_16))

    @property
    def __str__(self):
        return f"'Count'={self.getCount()}, 'md5_1'={self.getmd5_1()}, 'md5_2'={self.getmd5_2()}, 'md5_3'={self.getmd5_3()}, 'md5_4'={self.getmd5_4()}, 'md5_5'={self.getmd5_5()}, 'md5_6'={self.getmd5_6()}, 'md5_7'={self.getmd5_7()}, 'md5_8'={self.getmd5_8()}, 'md5_9'={self.getmd5_9()}, 'md5_10'={self.getmd5_10()}, 'md5_11'={self.getmd5_11()}, 'md5_12'={self.getmd5_12()}, 'md5_13'={self.getmd5_13()}, 'md5_14'={self.getmd5_14()}, 'md5_15'={self.getmd5_15()}, 'md5_16'={self.getmd5_16()}"

    @property
    def __dict__(self):
        return {'Count': self.getCount(), 'md5_1': self.getmd5_1(), 'md5_2': self.getmd5_2(), 'md5_3': self.getmd5_3(), 'md5_4': self.getmd5_4(), 'md5_5': self.getmd5_5(), 'md5_6': self.getmd5_6(), 'md5_7': self.getmd5_7(), 'md5_8': self.getmd5_8(), 'md5_9': self.getmd5_9(), 'md5_10': self.getmd5_10(), 'md5_11': self.getmd5_11(), 'md5_12': self.getmd5_12(), 'md5_13': self.getmd5_13(), 'md5_14': self.getmd5_14(), 'md5_15': self.getmd5_15(), 'md5_16': self.getmd5_16()}


class  CShfeFtdcSettlementSessionField(Structure):
    """结算会话"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID()}


class  CShfeFtdcReqRiskUserLoginField(Structure):
    """用户登录请求"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("Password", c_char*41),
        ("Version", c_int32),
        ("LocalSessionID", c_int32),
        ("MacAddress", c_char*21),
        ("ClientIPAddress", c_char*16),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getPassword(self):
        '''密码'''
        return str(self.Password, 'GBK')

    def getVersion(self):
        '''客户端版本,20091230版Version=1,之前版本Version=0'''
        return self.Version

    def getLocalSessionID(self):
        '''本地前置中客户端连接的SessionID'''
        return self.LocalSessionID

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    def getClientIPAddress(self):
        '''终端IP地址'''
        return str(self.ClientIPAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'Password'={self.getPassword()}, 'Version'={self.getVersion()}, 'LocalSessionID'={self.getLocalSessionID()}, 'MacAddress'={self.getMacAddress()}, 'ClientIPAddress'={self.getClientIPAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'Password': self.getPassword(), 'Version': self.getVersion(), 'LocalSessionID': self.getLocalSessionID(), 'MacAddress': self.getMacAddress(), 'ClientIPAddress': self.getClientIPAddress()}


class  CShfeFtdcRspRiskUserLoginField(Structure):
    """用户登录应答"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("Version", c_int32),
        ("FrontType", c_char),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getVersion(self):
        '''客户端版本,20091230版Version=1,之前版本Version=0'''
        return self.Version

    def getFrontType(self):
        '''前置类型'''
        return TShfeFtdcFrontTypeType(ord(self.FrontType))

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'Version'={self.getVersion()}, 'FrontType'={self.getFrontType()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'Version': self.getVersion(), 'FrontType': self.getFrontType()}


class  CShfeFtdcInvestorRangeSumInfoField(Structure):
    """特定范围投资者信息摘要请求"""
    _fields_ = [
        ("startindex", c_int32),
        ("endindex", c_int32),
        ("BrokerID", c_char*11),
    ]

    def getstartindex(self):
        '''投资者起始下标'''
        return self.startindex

    def getendindex(self):
        '''投资者结束下标'''
        return self.endindex

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    @property
    def __str__(self):
        return f"'startindex'={self.getstartindex()}, 'endindex'={self.getendindex()}, 'BrokerID'={self.getBrokerID()}"

    @property
    def __dict__(self):
        return {'startindex': self.getstartindex(), 'endindex': self.getendindex(), 'BrokerID': self.getBrokerID()}


class  CShfeFtdcReqInvestorAccountField(Structure):
    """投资者资金查询请求"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("TradingDayStart", c_char*9),
        ("TradingDayEnd", c_char*9),
        ("InvestorIDStart", c_char*13),
        ("InvestorIDEnd", c_char*13),
        ("SortType", c_char),
        ("ResultCount", c_int32),
        ("ResultRatio", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getTradingDayStart(self):
        '''起始交易日期'''
        return str(self.TradingDayStart, 'GBK')

    def getTradingDayEnd(self):
        '''结束交易日期'''
        return str(self.TradingDayEnd, 'GBK')

    def getInvestorIDStart(self):
        '''起始投资者代码'''
        return str(self.InvestorIDStart, 'GBK')

    def getInvestorIDEnd(self):
        '''结束投资者代码'''
        return str(self.InvestorIDEnd, 'GBK')

    def getSortType(self):
        '''资金排序方法'''
        return TShfeFtdcAccountSortTypeType(ord(self.SortType))

    def getResultCount(self):
        '''按排名数返回结果'''
        return self.ResultCount

    def getResultRatio(self):
        '''按比例返回结果'''
        return self.ResultRatio

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'TradingDayStart'={self.getTradingDayStart()}, 'TradingDayEnd'={self.getTradingDayEnd()}, 'InvestorIDStart'={self.getInvestorIDStart()}, 'InvestorIDEnd'={self.getInvestorIDEnd()}, 'SortType'={self.getSortType()}, 'ResultCount'={self.getResultCount()}, 'ResultRatio'={self.getResultRatio()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'TradingDayStart': self.getTradingDayStart(), 'TradingDayEnd': self.getTradingDayEnd(), 'InvestorIDStart': self.getInvestorIDStart(), 'InvestorIDEnd': self.getInvestorIDEnd(), 'SortType': self.getSortType(), 'ResultCount': self.getResultCount(), 'ResultRatio': self.getResultRatio()}


class  CShfeFtdcInvestorRiskAccountField(Structure):
    """投资者资金查询响应"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("AccountID", c_char*13),
        ("PreMortgage", c_double),
        ("PreCredit", c_double),
        ("PreDeposit", c_double),
        ("PreBalance", c_double),
        ("PreMargin", c_double),
        ("Withdraw", c_double),
        ("CurrMargin", c_double),
        ("Commission", c_double),
        ("CloseProfit", c_double),
        ("PositionProfit", c_double),
        ("Balance", c_double),
        ("Available", c_double),
        ("Mortgage", c_double),
        ("ExchangeMargin", c_double),
        ("Reserve", c_double),
        ("WithdrawQuota", c_double),
        ("Credit", c_double),
        ("PreExchMargin", c_double),
        ("ForceCloseStat", c_int32),
        ("DeliveryMargin", c_double),
        ("ExchangeDeliveryMargin", c_double),
        ("FrozenMargin", c_double),
        ("FrozenCommission", c_double),
        ("CurrencyID", c_char*4),
        ("PreSpecProductMargin", c_double),
        ("PreSpecProductExchangeMargin", c_double),
        ("PreMarginOnMortgage", c_double),
        ("PreExchMarginOnMortgage", c_double),
        ("PreFundMortgageIn", c_double),
        ("PreFundMortgageOut", c_double),
        ("Deposit", c_double),
        ("TradingPositionProfit", c_double),
        ("FundMortgageIn", c_double),
        ("FundMortgageOut", c_double),
        ("FundMortgageAvailable", c_double),
        ("MortgageableFund", c_double),
        ("SpecProductExchangeMargin", c_double),
        ("SpecProductFrozenMargin", c_double),
        ("SpecProductMargin", c_double),
        ("SpecProductCommission", c_double),
        ("SpecProductFrozenCommission", c_double),
        ("SpecProductPositionProfit", c_double),
        ("SpecProductCloseProfit", c_double),
        ("SpecProductPositionProfitByAlg", c_double),
        ("FrozenMarginOnMortgage", c_double),
        ("MarginOnMortgage", c_double),
        ("ExchMarginOnMortgage", c_double),
        ("FrozenCommissionOnMortgage", c_double),
        ("PositionProfitOnMortgage", c_double),
        ("CommissionOnMortgage", c_double),
        ("CloseProfitOnMortgage", c_double),
        ("OptionCloseProfit", c_double),
        ("OptionValue", c_double),
        ("FrozenCash", c_double),
        ("CashIn", c_double),
        ("MaintCurrMargin", c_double),
        ("MaintExchangeMargin", c_double),
        ("FixedMargin", c_double),
        ("ExchFixedMargin", c_double),
        ("FrozenSwap", c_double),
        ("RemainSwap", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getPreMortgage(self):
        '''上次质押金额'''
        return self.PreMortgage

    def getPreCredit(self):
        '''上次信用额度'''
        return self.PreCredit

    def getPreDeposit(self):
        '''上次存款额'''
        return self.PreDeposit

    def getPreBalance(self):
        '''上次总权益'''
        return self.PreBalance

    def getPreMargin(self):
        '''上次占用的保证金'''
        return self.PreMargin

    def getWithdraw(self):
        '''出金金额'''
        return self.Withdraw

    def getCurrMargin(self):
        '''当前保证金总额'''
        return self.CurrMargin

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getBalance(self):
        '''总权益'''
        return self.Balance

    def getAvailable(self):
        '''可用资金'''
        return self.Available

    def getMortgage(self):
        '''质押金额'''
        return self.Mortgage

    def getExchangeMargin(self):
        '''交易所保证金'''
        return self.ExchangeMargin

    def getReserve(self):
        '''基本准备金'''
        return self.Reserve

    def getWithdrawQuota(self):
        '''可取资金'''
        return self.WithdrawQuota

    def getCredit(self):
        '''信用额度'''
        return self.Credit

    def getPreExchMargin(self):
        '''上次交易所保证金'''
        return self.PreExchMargin

    def getForceCloseStat(self):
        '''历史强平次数'''
        return self.ForceCloseStat

    def getDeliveryMargin(self):
        '''投资者交割保证金'''
        return self.DeliveryMargin

    def getExchangeDeliveryMargin(self):
        '''交易所交割保证金'''
        return self.ExchangeDeliveryMargin

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getPreSpecProductMargin(self):
        '''上次特殊产品占用交易所保证金'''
        return self.PreSpecProductMargin

    def getPreSpecProductExchangeMargin(self):
        '''上次特殊产品占用保证金'''
        return self.PreSpecProductExchangeMargin

    def getPreMarginOnMortgage(self):
        '''上一交易日算在质押上的保证金'''
        return self.PreMarginOnMortgage

    def getPreExchMarginOnMortgage(self):
        '''上一交易日算在质押上的交易所保证金'''
        return self.PreExchMarginOnMortgage

    def getPreFundMortgageIn(self):
        '''上次货币质入金额'''
        return self.PreFundMortgageIn

    def getPreFundMortgageOut(self):
        '''上次货币质入金额'''
        return self.PreFundMortgageOut

    def getDeposit(self):
        '''入金金额'''
        return self.Deposit

    def getTradingPositionProfit(self):
        '''交易持仓盈亏'''
        return self.TradingPositionProfit

    def getFundMortgageIn(self):
        '''货币质入金额'''
        return self.FundMortgageIn

    def getFundMortgageOut(self):
        '''货币质出金额'''
        return self.FundMortgageOut

    def getFundMortgageAvailable(self):
        '''货币质押余额'''
        return self.FundMortgageAvailable

    def getMortgageableFund(self):
        '''可质押货币金额'''
        return self.MortgageableFund

    def getSpecProductExchangeMargin(self):
        '''特殊品种交易所占用保证金'''
        return self.SpecProductExchangeMargin

    def getSpecProductFrozenMargin(self):
        '''特殊产品冻结保证金'''
        return self.SpecProductFrozenMargin

    def getSpecProductMargin(self):
        '''特殊产品占用保证金'''
        return self.SpecProductMargin

    def getSpecProductCommission(self):
        '''特殊产品手续费'''
        return self.SpecProductCommission

    def getSpecProductFrozenCommission(self):
        '''特殊产品冻结手续费'''
        return self.SpecProductFrozenCommission

    def getSpecProductPositionProfit(self):
        '''特殊产品持仓盈亏'''
        return self.SpecProductPositionProfit

    def getSpecProductCloseProfit(self):
        '''特殊产品平仓盈亏'''
        return self.SpecProductCloseProfit

    def getSpecProductPositionProfitByAlg(self):
        '''根据持仓盈亏算法计算的特殊产品持仓盈亏'''
        return self.SpecProductPositionProfitByAlg

    def getFrozenMarginOnMortgage(self):
        '''算在质押上的保证金冻结'''
        return self.FrozenMarginOnMortgage

    def getMarginOnMortgage(self):
        '''算在质押上的保证金'''
        return self.MarginOnMortgage

    def getExchMarginOnMortgage(self):
        '''算在质押上的交易所保证金'''
        return self.ExchMarginOnMortgage

    def getFrozenCommissionOnMortgage(self):
        '''算在质押上的冻结手续费'''
        return self.FrozenCommissionOnMortgage

    def getPositionProfitOnMortgage(self):
        '''算在质押上的持仓盈亏'''
        return self.PositionProfitOnMortgage

    def getCommissionOnMortgage(self):
        '''算在质押上的手续费'''
        return self.CommissionOnMortgage

    def getCloseProfitOnMortgage(self):
        '''算在质押上的平仓盈亏'''
        return self.CloseProfitOnMortgage

    def getOptionCloseProfit(self):
        '''期权平仓盈亏'''
        return self.OptionCloseProfit

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getMaintCurrMargin(self):
        '''维持保证金总额'''
        return self.MaintCurrMargin

    def getMaintExchangeMargin(self):
        '''交易所维持保证金'''
        return self.MaintExchangeMargin

    def getFixedMargin(self):
        '''昨结算价计算的期权保证金'''
        return self.FixedMargin

    def getExchFixedMargin(self):
        '''交易所昨结算价计算的期权保证金'''
        return self.ExchFixedMargin

    def getFrozenSwap(self):
        '''延时换汇冻结金额'''
        return self.FrozenSwap

    def getRemainSwap(self):
        '''剩余换汇额度'''
        return self.RemainSwap

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'AccountID'={self.getAccountID()}, 'PreMortgage'={self.getPreMortgage()}, 'PreCredit'={self.getPreCredit()}, 'PreDeposit'={self.getPreDeposit()}, 'PreBalance'={self.getPreBalance()}, 'PreMargin'={self.getPreMargin()}, 'Withdraw'={self.getWithdraw()}, 'CurrMargin'={self.getCurrMargin()}, 'Commission'={self.getCommission()}, 'CloseProfit'={self.getCloseProfit()}, 'PositionProfit'={self.getPositionProfit()}, 'Balance'={self.getBalance()}, 'Available'={self.getAvailable()}, 'Mortgage'={self.getMortgage()}, 'ExchangeMargin'={self.getExchangeMargin()}, 'Reserve'={self.getReserve()}, 'WithdrawQuota'={self.getWithdrawQuota()}, 'Credit'={self.getCredit()}, 'PreExchMargin'={self.getPreExchMargin()}, 'ForceCloseStat'={self.getForceCloseStat()}, 'DeliveryMargin'={self.getDeliveryMargin()}, 'ExchangeDeliveryMargin'={self.getExchangeDeliveryMargin()}, 'FrozenMargin'={self.getFrozenMargin()}, 'FrozenCommission'={self.getFrozenCommission()}, 'CurrencyID'={self.getCurrencyID()}, 'PreSpecProductMargin'={self.getPreSpecProductMargin()}, 'PreSpecProductExchangeMargin'={self.getPreSpecProductExchangeMargin()}, 'PreMarginOnMortgage'={self.getPreMarginOnMortgage()}, 'PreExchMarginOnMortgage'={self.getPreExchMarginOnMortgage()}, 'PreFundMortgageIn'={self.getPreFundMortgageIn()}, 'PreFundMortgageOut'={self.getPreFundMortgageOut()}, 'Deposit'={self.getDeposit()}, 'TradingPositionProfit'={self.getTradingPositionProfit()}, 'FundMortgageIn'={self.getFundMortgageIn()}, 'FundMortgageOut'={self.getFundMortgageOut()}, 'FundMortgageAvailable'={self.getFundMortgageAvailable()}, 'MortgageableFund'={self.getMortgageableFund()}, 'SpecProductExchangeMargin'={self.getSpecProductExchangeMargin()}, 'SpecProductFrozenMargin'={self.getSpecProductFrozenMargin()}, 'SpecProductMargin'={self.getSpecProductMargin()}, 'SpecProductCommission'={self.getSpecProductCommission()}, 'SpecProductFrozenCommission'={self.getSpecProductFrozenCommission()}, 'SpecProductPositionProfit'={self.getSpecProductPositionProfit()}, 'SpecProductCloseProfit'={self.getSpecProductCloseProfit()}, 'SpecProductPositionProfitByAlg'={self.getSpecProductPositionProfitByAlg()}, 'FrozenMarginOnMortgage'={self.getFrozenMarginOnMortgage()}, 'MarginOnMortgage'={self.getMarginOnMortgage()}, 'ExchMarginOnMortgage'={self.getExchMarginOnMortgage()}, 'FrozenCommissionOnMortgage'={self.getFrozenCommissionOnMortgage()}, 'PositionProfitOnMortgage'={self.getPositionProfitOnMortgage()}, 'CommissionOnMortgage'={self.getCommissionOnMortgage()}, 'CloseProfitOnMortgage'={self.getCloseProfitOnMortgage()}, 'OptionCloseProfit'={self.getOptionCloseProfit()}, 'OptionValue'={self.getOptionValue()}, 'FrozenCash'={self.getFrozenCash()}, 'CashIn'={self.getCashIn()}, 'MaintCurrMargin'={self.getMaintCurrMargin()}, 'MaintExchangeMargin'={self.getMaintExchangeMargin()}, 'FixedMargin'={self.getFixedMargin()}, 'ExchFixedMargin'={self.getExchFixedMargin()}, 'FrozenSwap'={self.getFrozenSwap()}, 'RemainSwap'={self.getRemainSwap()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'AccountID': self.getAccountID(), 'PreMortgage': self.getPreMortgage(), 'PreCredit': self.getPreCredit(), 'PreDeposit': self.getPreDeposit(), 'PreBalance': self.getPreBalance(), 'PreMargin': self.getPreMargin(), 'Withdraw': self.getWithdraw(), 'CurrMargin': self.getCurrMargin(), 'Commission': self.getCommission(), 'CloseProfit': self.getCloseProfit(), 'PositionProfit': self.getPositionProfit(), 'Balance': self.getBalance(), 'Available': self.getAvailable(), 'Mortgage': self.getMortgage(), 'ExchangeMargin': self.getExchangeMargin(), 'Reserve': self.getReserve(), 'WithdrawQuota': self.getWithdrawQuota(), 'Credit': self.getCredit(), 'PreExchMargin': self.getPreExchMargin(), 'ForceCloseStat': self.getForceCloseStat(), 'DeliveryMargin': self.getDeliveryMargin(), 'ExchangeDeliveryMargin': self.getExchangeDeliveryMargin(), 'FrozenMargin': self.getFrozenMargin(), 'FrozenCommission': self.getFrozenCommission(), 'CurrencyID': self.getCurrencyID(), 'PreSpecProductMargin': self.getPreSpecProductMargin(), 'PreSpecProductExchangeMargin': self.getPreSpecProductExchangeMargin(), 'PreMarginOnMortgage': self.getPreMarginOnMortgage(), 'PreExchMarginOnMortgage': self.getPreExchMarginOnMortgage(), 'PreFundMortgageIn': self.getPreFundMortgageIn(), 'PreFundMortgageOut': self.getPreFundMortgageOut(), 'Deposit': self.getDeposit(), 'TradingPositionProfit': self.getTradingPositionProfit(), 'FundMortgageIn': self.getFundMortgageIn(), 'FundMortgageOut': self.getFundMortgageOut(), 'FundMortgageAvailable': self.getFundMortgageAvailable(), 'MortgageableFund': self.getMortgageableFund(), 'SpecProductExchangeMargin': self.getSpecProductExchangeMargin(), 'SpecProductFrozenMargin': self.getSpecProductFrozenMargin(), 'SpecProductMargin': self.getSpecProductMargin(), 'SpecProductCommission': self.getSpecProductCommission(), 'SpecProductFrozenCommission': self.getSpecProductFrozenCommission(), 'SpecProductPositionProfit': self.getSpecProductPositionProfit(), 'SpecProductCloseProfit': self.getSpecProductCloseProfit(), 'SpecProductPositionProfitByAlg': self.getSpecProductPositionProfitByAlg(), 'FrozenMarginOnMortgage': self.getFrozenMarginOnMortgage(), 'MarginOnMortgage': self.getMarginOnMortgage(), 'ExchMarginOnMortgage': self.getExchMarginOnMortgage(), 'FrozenCommissionOnMortgage': self.getFrozenCommissionOnMortgage(), 'PositionProfitOnMortgage': self.getPositionProfitOnMortgage(), 'CommissionOnMortgage': self.getCommissionOnMortgage(), 'CloseProfitOnMortgage': self.getCloseProfitOnMortgage(), 'OptionCloseProfit': self.getOptionCloseProfit(), 'OptionValue': self.getOptionValue(), 'FrozenCash': self.getFrozenCash(), 'CashIn': self.getCashIn(), 'MaintCurrMargin': self.getMaintCurrMargin(), 'MaintExchangeMargin': self.getMaintExchangeMargin(), 'FixedMargin': self.getFixedMargin(), 'ExchFixedMargin': self.getExchFixedMargin(), 'FrozenSwap': self.getFrozenSwap(), 'RemainSwap': self.getRemainSwap()}


class  CShfeFtdcReqInvestorPositionField(Structure):
    """投资者持仓查询请求"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("TradingDayStart", c_char*9),
        ("TradingDayEnd", c_char*9),
        ("InvestorIDStart", c_char*13),
        ("InvestorIDEnd", c_char*13),
        ("InstIDStart", c_char*31),
        ("InstIDEnd", c_char*31),
        ("ProductIDStart", c_char*31),
        ("ProductIDEnd", c_char*31),
        ("SortType", c_char),
        ("ResultCount", c_int32),
        ("ResultRatio", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getTradingDayStart(self):
        '''起始交易日期'''
        return str(self.TradingDayStart, 'GBK')

    def getTradingDayEnd(self):
        '''结束交易日期'''
        return str(self.TradingDayEnd, 'GBK')

    def getInvestorIDStart(self):
        '''起始投资者代码'''
        return str(self.InvestorIDStart, 'GBK')

    def getInvestorIDEnd(self):
        '''结束投资者代码'''
        return str(self.InvestorIDEnd, 'GBK')

    def getInstIDStart(self):
        '''起始合约代码'''
        return str(self.InstIDStart, 'GBK')

    def getInstIDEnd(self):
        '''结束合约代码'''
        return str(self.InstIDEnd, 'GBK')

    def getProductIDStart(self):
        '''起始产品代码'''
        return str(self.ProductIDStart, 'GBK')

    def getProductIDEnd(self):
        '''结束产品代码'''
        return str(self.ProductIDEnd, 'GBK')

    def getSortType(self):
        '''持仓排序方法'''
        return TShfeFtdcPositionSortTypeType(ord(self.SortType))

    def getResultCount(self):
        '''按排名数返回结果'''
        return self.ResultCount

    def getResultRatio(self):
        '''按比例返回结果'''
        return self.ResultRatio

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'TradingDayStart'={self.getTradingDayStart()}, 'TradingDayEnd'={self.getTradingDayEnd()}, 'InvestorIDStart'={self.getInvestorIDStart()}, 'InvestorIDEnd'={self.getInvestorIDEnd()}, 'InstIDStart'={self.getInstIDStart()}, 'InstIDEnd'={self.getInstIDEnd()}, 'ProductIDStart'={self.getProductIDStart()}, 'ProductIDEnd'={self.getProductIDEnd()}, 'SortType'={self.getSortType()}, 'ResultCount'={self.getResultCount()}, 'ResultRatio'={self.getResultRatio()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'TradingDayStart': self.getTradingDayStart(), 'TradingDayEnd': self.getTradingDayEnd(), 'InvestorIDStart': self.getInvestorIDStart(), 'InvestorIDEnd': self.getInvestorIDEnd(), 'InstIDStart': self.getInstIDStart(), 'InstIDEnd': self.getInstIDEnd(), 'ProductIDStart': self.getProductIDStart(), 'ProductIDEnd': self.getProductIDEnd(), 'SortType': self.getSortType(), 'ResultCount': self.getResultCount(), 'ResultRatio': self.getResultRatio()}


class  CShfeFtdcRspInvestorPositionField(Structure):
    """投资者持仓查询响应"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("PosiDirection", c_char),
        ("HedgeFlag", c_char),
        ("PositionDate", c_char),
        ("YdPosition", c_int32),
        ("Position", c_int32),
        ("LongFrozen", c_int32),
        ("ShortFrozen", c_int32),
        ("LongFrozenAmount", c_double),
        ("ShortFrozenAmount", c_double),
        ("OpenVolume", c_int32),
        ("CloseVolume", c_int32),
        ("OpenAmount", c_double),
        ("CloseAmount", c_double),
        ("PositionCost", c_double),
        ("PreMargin", c_double),
        ("UseMargin", c_double),
        ("FrozenMargin", c_double),
        ("FrozenCash", c_double),
        ("FrozenCommission", c_double),
        ("CashIn", c_double),
        ("Commission", c_double),
        ("CloseProfit", c_double),
        ("PositionProfit", c_double),
        ("PreSettlementPrice", c_double),
        ("SettlementPrice", c_double),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("OpenCost", c_double),
        ("ExchangeMargin", c_double),
        ("CombPosition", c_int32),
        ("CombLongFrozen", c_int32),
        ("CombShortFrozen", c_int32),
        ("CloseProfitByDate", c_double),
        ("CloseProfitByTrade", c_double),
        ("TodayPosition", c_int32),
        ("MarginRateByMoney", c_double),
        ("MarginRateByVolume", c_double),
        ("StrikeFrozen", c_int32),
        ("StrikeFrozenAmount", c_double),
        ("AbandonFrozen", c_int32),
        ("OptionValue", c_double),
        ("MaintUseMargin", c_double),
        ("MaintExchangeMargin", c_double),
        ("IndexSettlementPrice", c_double),
        ("FixedMargin", c_double),
        ("ExchangeID", c_char*9),
        ("YdStrikeFrozen", c_int32),
        ("InvestUnitID", c_char*17),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPosiDirection(self):
        '''持仓多空方向'''
        return TShfeFtdcPosiDirectionType(ord(self.PosiDirection))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPositionDate(self):
        '''持仓日期'''
        return TShfeFtdcPositionDateType(ord(self.PositionDate))

    def getYdPosition(self):
        '''上日持仓'''
        return self.YdPosition

    def getPosition(self):
        '''今日持仓'''
        return self.Position

    def getLongFrozen(self):
        '''多头冻结'''
        return self.LongFrozen

    def getShortFrozen(self):
        '''空头冻结'''
        return self.ShortFrozen

    def getLongFrozenAmount(self):
        '''开仓冻结金额'''
        return self.LongFrozenAmount

    def getShortFrozenAmount(self):
        '''开仓冻结金额'''
        return self.ShortFrozenAmount

    def getOpenVolume(self):
        '''开仓量'''
        return self.OpenVolume

    def getCloseVolume(self):
        '''平仓量'''
        return self.CloseVolume

    def getOpenAmount(self):
        '''开仓金额'''
        return self.OpenAmount

    def getCloseAmount(self):
        '''平仓金额'''
        return self.CloseAmount

    def getPositionCost(self):
        '''持仓成本'''
        return self.PositionCost

    def getPreMargin(self):
        '''上次占用的保证金'''
        return self.PreMargin

    def getUseMargin(self):
        '''占用的保证金'''
        return self.UseMargin

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getPreSettlementPrice(self):
        '''上次结算价'''
        return self.PreSettlementPrice

    def getSettlementPrice(self):
        '''本次结算价'''
        return self.SettlementPrice

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getOpenCost(self):
        '''开仓成本'''
        return self.OpenCost

    def getExchangeMargin(self):
        '''交易所保证金'''
        return self.ExchangeMargin

    def getCombPosition(self):
        '''组合成交形成的持仓'''
        return self.CombPosition

    def getCombLongFrozen(self):
        '''组合多头冻结'''
        return self.CombLongFrozen

    def getCombShortFrozen(self):
        '''组合空头冻结'''
        return self.CombShortFrozen

    def getCloseProfitByDate(self):
        '''逐日盯市平仓盈亏'''
        return self.CloseProfitByDate

    def getCloseProfitByTrade(self):
        '''逐笔对冲平仓盈亏'''
        return self.CloseProfitByTrade

    def getTodayPosition(self):
        '''今日持仓'''
        return self.TodayPosition

    def getMarginRateByMoney(self):
        '''保证金率'''
        return self.MarginRateByMoney

    def getMarginRateByVolume(self):
        '''保证金率(按手数)'''
        return self.MarginRateByVolume

    def getStrikeFrozen(self):
        '''执行冻结'''
        return self.StrikeFrozen

    def getStrikeFrozenAmount(self):
        '''执行冻结金额'''
        return self.StrikeFrozenAmount

    def getAbandonFrozen(self):
        '''放弃执行冻结'''
        return self.AbandonFrozen

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    def getMaintUseMargin(self):
        '''占用的维持保证金'''
        return self.MaintUseMargin

    def getMaintExchangeMargin(self):
        '''交易所维持保证金'''
        return self.MaintExchangeMargin

    def getIndexSettlementPrice(self):
        '''期权标的合约的本次结算价'''
        return self.IndexSettlementPrice

    def getFixedMargin(self):
        '''昨结算价计算的期权保证金'''
        return self.FixedMargin

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getYdStrikeFrozen(self):
        '''执行冻结的昨仓'''
        return self.YdStrikeFrozen

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'PosiDirection'={self.getPosiDirection()}, 'HedgeFlag'={self.getHedgeFlag()}, 'PositionDate'={self.getPositionDate()}, 'YdPosition'={self.getYdPosition()}, 'Position'={self.getPosition()}, 'LongFrozen'={self.getLongFrozen()}, 'ShortFrozen'={self.getShortFrozen()}, 'LongFrozenAmount'={self.getLongFrozenAmount()}, 'ShortFrozenAmount'={self.getShortFrozenAmount()}, 'OpenVolume'={self.getOpenVolume()}, 'CloseVolume'={self.getCloseVolume()}, 'OpenAmount'={self.getOpenAmount()}, 'CloseAmount'={self.getCloseAmount()}, 'PositionCost'={self.getPositionCost()}, 'PreMargin'={self.getPreMargin()}, 'UseMargin'={self.getUseMargin()}, 'FrozenMargin'={self.getFrozenMargin()}, 'FrozenCash'={self.getFrozenCash()}, 'FrozenCommission'={self.getFrozenCommission()}, 'CashIn'={self.getCashIn()}, 'Commission'={self.getCommission()}, 'CloseProfit'={self.getCloseProfit()}, 'PositionProfit'={self.getPositionProfit()}, 'PreSettlementPrice'={self.getPreSettlementPrice()}, 'SettlementPrice'={self.getSettlementPrice()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'OpenCost'={self.getOpenCost()}, 'ExchangeMargin'={self.getExchangeMargin()}, 'CombPosition'={self.getCombPosition()}, 'CombLongFrozen'={self.getCombLongFrozen()}, 'CombShortFrozen'={self.getCombShortFrozen()}, 'CloseProfitByDate'={self.getCloseProfitByDate()}, 'CloseProfitByTrade'={self.getCloseProfitByTrade()}, 'TodayPosition'={self.getTodayPosition()}, 'MarginRateByMoney'={self.getMarginRateByMoney()}, 'MarginRateByVolume'={self.getMarginRateByVolume()}, 'StrikeFrozen'={self.getStrikeFrozen()}, 'StrikeFrozenAmount'={self.getStrikeFrozenAmount()}, 'AbandonFrozen'={self.getAbandonFrozen()}, 'OptionValue'={self.getOptionValue()}, 'MaintUseMargin'={self.getMaintUseMargin()}, 'MaintExchangeMargin'={self.getMaintExchangeMargin()}, 'IndexSettlementPrice'={self.getIndexSettlementPrice()}, 'FixedMargin'={self.getFixedMargin()}, 'ExchangeID'={self.getExchangeID()}, 'YdStrikeFrozen'={self.getYdStrikeFrozen()}, 'InvestUnitID'={self.getInvestUnitID()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'PosiDirection': self.getPosiDirection(), 'HedgeFlag': self.getHedgeFlag(), 'PositionDate': self.getPositionDate(), 'YdPosition': self.getYdPosition(), 'Position': self.getPosition(), 'LongFrozen': self.getLongFrozen(), 'ShortFrozen': self.getShortFrozen(), 'LongFrozenAmount': self.getLongFrozenAmount(), 'ShortFrozenAmount': self.getShortFrozenAmount(), 'OpenVolume': self.getOpenVolume(), 'CloseVolume': self.getCloseVolume(), 'OpenAmount': self.getOpenAmount(), 'CloseAmount': self.getCloseAmount(), 'PositionCost': self.getPositionCost(), 'PreMargin': self.getPreMargin(), 'UseMargin': self.getUseMargin(), 'FrozenMargin': self.getFrozenMargin(), 'FrozenCash': self.getFrozenCash(), 'FrozenCommission': self.getFrozenCommission(), 'CashIn': self.getCashIn(), 'Commission': self.getCommission(), 'CloseProfit': self.getCloseProfit(), 'PositionProfit': self.getPositionProfit(), 'PreSettlementPrice': self.getPreSettlementPrice(), 'SettlementPrice': self.getSettlementPrice(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'OpenCost': self.getOpenCost(), 'ExchangeMargin': self.getExchangeMargin(), 'CombPosition': self.getCombPosition(), 'CombLongFrozen': self.getCombLongFrozen(), 'CombShortFrozen': self.getCombShortFrozen(), 'CloseProfitByDate': self.getCloseProfitByDate(), 'CloseProfitByTrade': self.getCloseProfitByTrade(), 'TodayPosition': self.getTodayPosition(), 'MarginRateByMoney': self.getMarginRateByMoney(), 'MarginRateByVolume': self.getMarginRateByVolume(), 'StrikeFrozen': self.getStrikeFrozen(), 'StrikeFrozenAmount': self.getStrikeFrozenAmount(), 'AbandonFrozen': self.getAbandonFrozen(), 'OptionValue': self.getOptionValue(), 'MaintUseMargin': self.getMaintUseMargin(), 'MaintExchangeMargin': self.getMaintExchangeMargin(), 'IndexSettlementPrice': self.getIndexSettlementPrice(), 'FixedMargin': self.getFixedMargin(), 'ExchangeID': self.getExchangeID(), 'YdStrikeFrozen': self.getYdStrikeFrozen(), 'InvestUnitID': self.getInvestUnitID()}


class  CShfeFtdcReqInvestorTradeField(Structure):
    """投资者交易查询请求"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("TradingDayStart", c_char*9),
        ("TradingDayEnd", c_char*9),
        ("InvestorIDStart", c_char*13),
        ("InvestorIDEnd", c_char*13),
        ("InstIDStart", c_char*31),
        ("InstIDEnd", c_char*31),
        ("ProductIDStart", c_char*31),
        ("ProductIDEnd", c_char*31),
        ("SortType", c_char),
        ("ResultCount", c_int32),
        ("ResultRatio", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getTradingDayStart(self):
        '''起始交易日期'''
        return str(self.TradingDayStart, 'GBK')

    def getTradingDayEnd(self):
        '''结束交易日期'''
        return str(self.TradingDayEnd, 'GBK')

    def getInvestorIDStart(self):
        '''起始投资者代码'''
        return str(self.InvestorIDStart, 'GBK')

    def getInvestorIDEnd(self):
        '''结束投资者代码'''
        return str(self.InvestorIDEnd, 'GBK')

    def getInstIDStart(self):
        '''起始合约代码'''
        return str(self.InstIDStart, 'GBK')

    def getInstIDEnd(self):
        '''结束合约代码'''
        return str(self.InstIDEnd, 'GBK')

    def getProductIDStart(self):
        '''起始产品代码'''
        return str(self.ProductIDStart, 'GBK')

    def getProductIDEnd(self):
        '''结束产品代码'''
        return str(self.ProductIDEnd, 'GBK')

    def getSortType(self):
        '''交易排序方法'''
        return TShfeFtdcTradeSortTypeType(ord(self.SortType))

    def getResultCount(self):
        '''按排名数返回结果'''
        return self.ResultCount

    def getResultRatio(self):
        '''按比例返回结果'''
        return self.ResultRatio

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'TradingDayStart'={self.getTradingDayStart()}, 'TradingDayEnd'={self.getTradingDayEnd()}, 'InvestorIDStart'={self.getInvestorIDStart()}, 'InvestorIDEnd'={self.getInvestorIDEnd()}, 'InstIDStart'={self.getInstIDStart()}, 'InstIDEnd'={self.getInstIDEnd()}, 'ProductIDStart'={self.getProductIDStart()}, 'ProductIDEnd'={self.getProductIDEnd()}, 'SortType'={self.getSortType()}, 'ResultCount'={self.getResultCount()}, 'ResultRatio'={self.getResultRatio()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'TradingDayStart': self.getTradingDayStart(), 'TradingDayEnd': self.getTradingDayEnd(), 'InvestorIDStart': self.getInvestorIDStart(), 'InvestorIDEnd': self.getInvestorIDEnd(), 'InstIDStart': self.getInstIDStart(), 'InstIDEnd': self.getInstIDEnd(), 'ProductIDStart': self.getProductIDStart(), 'ProductIDEnd': self.getProductIDEnd(), 'SortType': self.getSortType(), 'ResultCount': self.getResultCount(), 'ResultRatio': self.getResultRatio()}


class  CShfeFtdcRspInvestorTradeField(Structure):
    """投资者交易查询响应"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("ExchangeID", c_char*9),
        ("TradeID", c_char*21),
        ("Direction", c_char),
        ("OrderSysID", c_char*21),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("TradingRole", c_char),
        ("ExchangeInstID", c_char*31),
        ("OffsetFlag", c_char),
        ("HedgeFlag", c_char),
        ("Price", c_double),
        ("Volume", c_int32),
        ("TradeDate", c_char*9),
        ("TradeTime", c_char*9),
        ("TradeType", c_char),
        ("PriceSource", c_char),
        ("TraderID", c_char*21),
        ("OrderLocalID", c_char*13),
        ("ClearingPartID", c_char*11),
        ("BusinessUnit", c_char*21),
        ("SequenceNo", c_int32),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("BrokerOrderSeq", c_int32),
        ("TradeSource", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTradeID(self):
        '''成交编号'''
        return str(self.TradeID, 'GBK')

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getTradingRole(self):
        '''交易角色'''
        return TShfeFtdcTradingRoleType(ord(self.TradingRole))

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getOffsetFlag(self):
        '''开平标志'''
        return TShfeFtdcOffsetFlagType(ord(self.OffsetFlag))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPrice(self):
        '''价格'''
        return self.Price

    def getVolume(self):
        '''数量'''
        return self.Volume

    def getTradeDate(self):
        '''成交时期'''
        return str(self.TradeDate, 'GBK')

    def getTradeTime(self):
        '''成交时间'''
        return str(self.TradeTime, 'GBK')

    def getTradeType(self):
        '''成交类型'''
        return TShfeFtdcTradeTypeType(ord(self.TradeType))

    def getPriceSource(self):
        '''成交价来源'''
        return TShfeFtdcPriceSourceType(ord(self.PriceSource))

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getClearingPartID(self):
        '''结算会员编号'''
        return str(self.ClearingPartID, 'GBK')

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getBrokerOrderSeq(self):
        '''经纪公司报单编号'''
        return self.BrokerOrderSeq

    def getTradeSource(self):
        '''成交来源'''
        return TShfeFtdcTradeSourceType(ord(self.TradeSource))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'ExchangeID'={self.getExchangeID()}, 'TradeID'={self.getTradeID()}, 'Direction'={self.getDirection()}, 'OrderSysID'={self.getOrderSysID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'TradingRole'={self.getTradingRole()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'OffsetFlag'={self.getOffsetFlag()}, 'HedgeFlag'={self.getHedgeFlag()}, 'Price'={self.getPrice()}, 'Volume'={self.getVolume()}, 'TradeDate'={self.getTradeDate()}, 'TradeTime'={self.getTradeTime()}, 'TradeType'={self.getTradeType()}, 'PriceSource'={self.getPriceSource()}, 'TraderID'={self.getTraderID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ClearingPartID'={self.getClearingPartID()}, 'BusinessUnit'={self.getBusinessUnit()}, 'SequenceNo'={self.getSequenceNo()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'BrokerOrderSeq'={self.getBrokerOrderSeq()}, 'TradeSource'={self.getTradeSource()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'ExchangeID': self.getExchangeID(), 'TradeID': self.getTradeID(), 'Direction': self.getDirection(), 'OrderSysID': self.getOrderSysID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'TradingRole': self.getTradingRole(), 'ExchangeInstID': self.getExchangeInstID(), 'OffsetFlag': self.getOffsetFlag(), 'HedgeFlag': self.getHedgeFlag(), 'Price': self.getPrice(), 'Volume': self.getVolume(), 'TradeDate': self.getTradeDate(), 'TradeTime': self.getTradeTime(), 'TradeType': self.getTradeType(), 'PriceSource': self.getPriceSource(), 'TraderID': self.getTraderID(), 'OrderLocalID': self.getOrderLocalID(), 'ClearingPartID': self.getClearingPartID(), 'BusinessUnit': self.getBusinessUnit(), 'SequenceNo': self.getSequenceNo(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'BrokerOrderSeq': self.getBrokerOrderSeq(), 'TradeSource': self.getTradeSource()}


class  CShfeFtdcReqInvestorOrderField(Structure):
    """投资者报单查询请求"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("TradingDay", c_char*9),
        ("InvestorIDStart", c_char*13),
        ("InvestorIDEnd", c_char*13),
        ("InstIDStart", c_char*31),
        ("InstIDEnd", c_char*31),
        ("ProductIDStart", c_char*31),
        ("ProductIDEnd", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getTradingDay(self):
        '''交易日期'''
        return str(self.TradingDay, 'GBK')

    def getInvestorIDStart(self):
        '''起始投资者代码'''
        return str(self.InvestorIDStart, 'GBK')

    def getInvestorIDEnd(self):
        '''结束投资者代码'''
        return str(self.InvestorIDEnd, 'GBK')

    def getInstIDStart(self):
        '''起始合约代码'''
        return str(self.InstIDStart, 'GBK')

    def getInstIDEnd(self):
        '''结束合约代码'''
        return str(self.InstIDEnd, 'GBK')

    def getProductIDStart(self):
        '''起始产品代码'''
        return str(self.ProductIDStart, 'GBK')

    def getProductIDEnd(self):
        '''结束产品代码'''
        return str(self.ProductIDEnd, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'TradingDay'={self.getTradingDay()}, 'InvestorIDStart'={self.getInvestorIDStart()}, 'InvestorIDEnd'={self.getInvestorIDEnd()}, 'InstIDStart'={self.getInstIDStart()}, 'InstIDEnd'={self.getInstIDEnd()}, 'ProductIDStart'={self.getProductIDStart()}, 'ProductIDEnd'={self.getProductIDEnd()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'TradingDay': self.getTradingDay(), 'InvestorIDStart': self.getInvestorIDStart(), 'InvestorIDEnd': self.getInvestorIDEnd(), 'InstIDStart': self.getInstIDStart(), 'InstIDEnd': self.getInstIDEnd(), 'ProductIDStart': self.getProductIDStart(), 'ProductIDEnd': self.getProductIDEnd()}


class  CShfeFtdcRspInvestorOrderField(Structure):
    """投资者报单查询响应"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("OrderLocalID", c_char*13),
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("ExchangeInstID", c_char*31),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderSubmitStatus", c_char),
        ("NotifySequence", c_int32),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("OrderSysID", c_char*21),
        ("OrderSource", c_char),
        ("OrderStatus", c_char),
        ("OrderType", c_char),
        ("VolumeTraded", c_int32),
        ("VolumeTotal", c_int32),
        ("InsertDate", c_char*9),
        ("InsertTime", c_char*9),
        ("ActiveTime", c_char*9),
        ("SuspendTime", c_char*9),
        ("UpdateTime", c_char*9),
        ("CancelTime", c_char*9),
        ("ActiveTraderID", c_char*21),
        ("ClearingPartID", c_char*11),
        ("SequenceNo", c_int32),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("UserProductInfo", c_char*11),
        ("StatusMsg", c_char*81),
        ("UserForceClose", c_int32),
        ("ActiveUserID", c_char*16),
        ("BrokerOrderSeq", c_int32),
        ("RelativeOrderSysID", c_char*21),
        ("ZCETotalTradedVolume", c_int32),
        ("IsSwapOrder", c_int32),
        ("BranchID", c_char*9),
        ("InvestUnitID", c_char*17),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderSubmitStatus(self):
        '''报单提交状态'''
        return TShfeFtdcOrderSubmitStatusType(ord(self.OrderSubmitStatus))

    def getNotifySequence(self):
        '''报单提示序号'''
        return self.NotifySequence

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getOrderSource(self):
        '''报单来源'''
        return TShfeFtdcOrderSourceType(ord(self.OrderSource))

    def getOrderStatus(self):
        '''报单状态'''
        return TShfeFtdcOrderStatusType(ord(self.OrderStatus))

    def getOrderType(self):
        '''报单类型'''
        return TShfeFtdcOrderTypeType(ord(self.OrderType))

    def getVolumeTraded(self):
        '''今成交数量'''
        return self.VolumeTraded

    def getVolumeTotal(self):
        '''剩余数量'''
        return self.VolumeTotal

    def getInsertDate(self):
        '''报单日期'''
        return str(self.InsertDate, 'GBK')

    def getInsertTime(self):
        '''委托时间'''
        return str(self.InsertTime, 'GBK')

    def getActiveTime(self):
        '''激活时间'''
        return str(self.ActiveTime, 'GBK')

    def getSuspendTime(self):
        '''挂起时间'''
        return str(self.SuspendTime, 'GBK')

    def getUpdateTime(self):
        '''最后修改时间'''
        return str(self.UpdateTime, 'GBK')

    def getCancelTime(self):
        '''撤销时间'''
        return str(self.CancelTime, 'GBK')

    def getActiveTraderID(self):
        '''最后修改交易所交易员代码'''
        return str(self.ActiveTraderID, 'GBK')

    def getClearingPartID(self):
        '''结算会员编号'''
        return str(self.ClearingPartID, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getUserProductInfo(self):
        '''用户端产品信息'''
        return str(self.UserProductInfo, 'GBK')

    def getStatusMsg(self):
        '''状态信息'''
        return str(self.StatusMsg, 'GBK')

    def getUserForceClose(self):
        '''用户强评标志'''
        return self.UserForceClose

    def getActiveUserID(self):
        '''操作用户代码'''
        return str(self.ActiveUserID, 'GBK')

    def getBrokerOrderSeq(self):
        '''经纪公司报单编号'''
        return self.BrokerOrderSeq

    def getRelativeOrderSysID(self):
        '''相关报单'''
        return str(self.RelativeOrderSysID, 'GBK')

    def getZCETotalTradedVolume(self):
        '''郑商所成交数量'''
        return self.ZCETotalTradedVolume

    def getIsSwapOrder(self):
        '''互换单标志'''
        return self.IsSwapOrder

    def getBranchID(self):
        '''营业部编号'''
        return str(self.BranchID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderSubmitStatus'={self.getOrderSubmitStatus()}, 'NotifySequence'={self.getNotifySequence()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'OrderSysID'={self.getOrderSysID()}, 'OrderSource'={self.getOrderSource()}, 'OrderStatus'={self.getOrderStatus()}, 'OrderType'={self.getOrderType()}, 'VolumeTraded'={self.getVolumeTraded()}, 'VolumeTotal'={self.getVolumeTotal()}, 'InsertDate'={self.getInsertDate()}, 'InsertTime'={self.getInsertTime()}, 'ActiveTime'={self.getActiveTime()}, 'SuspendTime'={self.getSuspendTime()}, 'UpdateTime'={self.getUpdateTime()}, 'CancelTime'={self.getCancelTime()}, 'ActiveTraderID'={self.getActiveTraderID()}, 'ClearingPartID'={self.getClearingPartID()}, 'SequenceNo'={self.getSequenceNo()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'UserProductInfo'={self.getUserProductInfo()}, 'StatusMsg'={self.getStatusMsg()}, 'UserForceClose'={self.getUserForceClose()}, 'ActiveUserID'={self.getActiveUserID()}, 'BrokerOrderSeq'={self.getBrokerOrderSeq()}, 'RelativeOrderSysID'={self.getRelativeOrderSysID()}, 'ZCETotalTradedVolume'={self.getZCETotalTradedVolume()}, 'IsSwapOrder'={self.getIsSwapOrder()}, 'BranchID'={self.getBranchID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'OrderLocalID': self.getOrderLocalID(), 'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'ExchangeInstID': self.getExchangeInstID(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderSubmitStatus': self.getOrderSubmitStatus(), 'NotifySequence': self.getNotifySequence(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'OrderSysID': self.getOrderSysID(), 'OrderSource': self.getOrderSource(), 'OrderStatus': self.getOrderStatus(), 'OrderType': self.getOrderType(), 'VolumeTraded': self.getVolumeTraded(), 'VolumeTotal': self.getVolumeTotal(), 'InsertDate': self.getInsertDate(), 'InsertTime': self.getInsertTime(), 'ActiveTime': self.getActiveTime(), 'SuspendTime': self.getSuspendTime(), 'UpdateTime': self.getUpdateTime(), 'CancelTime': self.getCancelTime(), 'ActiveTraderID': self.getActiveTraderID(), 'ClearingPartID': self.getClearingPartID(), 'SequenceNo': self.getSequenceNo(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'UserProductInfo': self.getUserProductInfo(), 'StatusMsg': self.getStatusMsg(), 'UserForceClose': self.getUserForceClose(), 'ActiveUserID': self.getActiveUserID(), 'BrokerOrderSeq': self.getBrokerOrderSeq(), 'RelativeOrderSysID': self.getRelativeOrderSysID(), 'ZCETotalTradedVolume': self.getZCETotalTradedVolume(), 'IsSwapOrder': self.getIsSwapOrder(), 'BranchID': self.getBranchID(), 'InvestUnitID': self.getInvestUnitID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcInvestorPositionStaticField(Structure):
    """投资者持仓统计查询响应"""
    _fields_ = [
        ("ProductID", c_char*31),
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("YdPosition", c_int32),
        ("Position", c_int32),
        ("LongPosition", c_int32),
        ("ShortPosition", c_int32),
        ("NetPosition", c_int32),
        ("SpecuLongPosi", c_int32),
        ("SpecuShortPosi", c_int32),
        ("HedgeLongPosi", c_int32),
        ("HedgeShortPosi", c_int32),
        ("TodayPosition", c_int32),
        ("PositionCost", c_double),
    ]

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getInstrumentID(self):
        '''合约编号'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getYdPosition(self):
        '''昨持仓'''
        return self.YdPosition

    def getPosition(self):
        '''总持仓'''
        return self.Position

    def getLongPosition(self):
        '''多头持仓'''
        return self.LongPosition

    def getShortPosition(self):
        '''空头持仓'''
        return self.ShortPosition

    def getNetPosition(self):
        '''净持仓'''
        return self.NetPosition

    def getSpecuLongPosi(self):
        '''投机多头持仓'''
        return self.SpecuLongPosi

    def getSpecuShortPosi(self):
        '''投机空头持仓'''
        return self.SpecuShortPosi

    def getHedgeLongPosi(self):
        '''保值多头持仓'''
        return self.HedgeLongPosi

    def getHedgeShortPosi(self):
        '''保值空头持仓'''
        return self.HedgeShortPosi

    def getTodayPosition(self):
        '''今仓'''
        return self.TodayPosition

    def getPositionCost(self):
        '''总持仓成本'''
        return self.PositionCost

    @property
    def __str__(self):
        return f"'ProductID'={self.getProductID()}, 'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'YdPosition'={self.getYdPosition()}, 'Position'={self.getPosition()}, 'LongPosition'={self.getLongPosition()}, 'ShortPosition'={self.getShortPosition()}, 'NetPosition'={self.getNetPosition()}, 'SpecuLongPosi'={self.getSpecuLongPosi()}, 'SpecuShortPosi'={self.getSpecuShortPosi()}, 'HedgeLongPosi'={self.getHedgeLongPosi()}, 'HedgeShortPosi'={self.getHedgeShortPosi()}, 'TodayPosition'={self.getTodayPosition()}, 'PositionCost'={self.getPositionCost()}"

    @property
    def __dict__(self):
        return {'ProductID': self.getProductID(), 'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'YdPosition': self.getYdPosition(), 'Position': self.getPosition(), 'LongPosition': self.getLongPosition(), 'ShortPosition': self.getShortPosition(), 'NetPosition': self.getNetPosition(), 'SpecuLongPosi': self.getSpecuLongPosi(), 'SpecuShortPosi': self.getSpecuShortPosi(), 'HedgeLongPosi': self.getHedgeLongPosi(), 'HedgeShortPosi': self.getHedgeShortPosi(), 'TodayPosition': self.getTodayPosition(), 'PositionCost': self.getPositionCost()}


class  CShfeFtdcInvestorTradeStaticField(Structure):
    """投资者成交统计查询响应"""
    _fields_ = [
        ("ProductID", c_char*31),
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("TotalVol", c_int32),
        ("TotalAmt", c_double),
        ("BuyVol", c_int32),
        ("BuyAmt", c_double),
        ("SellVol", c_int32),
        ("SellAmt", c_double),
        ("NetVol", c_int32),
        ("NetAmt", c_double),
    ]

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getInstrumentID(self):
        '''合约编号'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getTotalVol(self):
        '''总成交量'''
        return self.TotalVol

    def getTotalAmt(self):
        '''总成交额'''
        return self.TotalAmt

    def getBuyVol(self):
        '''买成交量'''
        return self.BuyVol

    def getBuyAmt(self):
        '''买成交额'''
        return self.BuyAmt

    def getSellVol(self):
        '''卖成交量'''
        return self.SellVol

    def getSellAmt(self):
        '''卖成交额'''
        return self.SellAmt

    def getNetVol(self):
        '''净买入成交量'''
        return self.NetVol

    def getNetAmt(self):
        '''净买入成交额'''
        return self.NetAmt

    @property
    def __str__(self):
        return f"'ProductID'={self.getProductID()}, 'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'TotalVol'={self.getTotalVol()}, 'TotalAmt'={self.getTotalAmt()}, 'BuyVol'={self.getBuyVol()}, 'BuyAmt'={self.getBuyAmt()}, 'SellVol'={self.getSellVol()}, 'SellAmt'={self.getSellAmt()}, 'NetVol'={self.getNetVol()}, 'NetAmt'={self.getNetAmt()}"

    @property
    def __dict__(self):
        return {'ProductID': self.getProductID(), 'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'TotalVol': self.getTotalVol(), 'TotalAmt': self.getTotalAmt(), 'BuyVol': self.getBuyVol(), 'BuyAmt': self.getBuyAmt(), 'SellVol': self.getSellVol(), 'SellAmt': self.getSellAmt(), 'NetVol': self.getNetVol(), 'NetAmt': self.getNetAmt()}


class  CShfeFtdcSubMarketDataField(Structure):
    """订阅实时行情"""
    _fields_ = [
        ("InstrumentID", c_char*31),
    ]

    def getInstrumentID(self):
        '''合约编号'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcQryInstPositionRateField(Structure):
    """合约持仓比例查询"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InstIDStart", c_char*31),
        ("InstIDEnd", c_char*31),
        ("hbtotal_little", c_double),
        ("hbtotal_medium", c_double),
        ("hstotal_little", c_double),
        ("hstotal_medium", c_double),
        ("htotal_little", c_double),
        ("htotal_medium", c_double),
        ("sbtotal_little", c_double),
        ("sbtotal_medium", c_double),
        ("sstotal_little", c_double),
        ("sstotal_medium", c_double),
        ("stotal_little", c_double),
        ("stotal_medium", c_double),
        ("buytotal_little", c_double),
        ("buytotal_medium", c_double),
        ("selltotal_little", c_double),
        ("selltotal_medium", c_double),
        ("total_little", c_double),
        ("total_medium", c_double),
        ("ValueMode", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInstIDStart(self):
        '''起始合约代码'''
        return str(self.InstIDStart, 'GBK')

    def getInstIDEnd(self):
        '''结束合约代码'''
        return str(self.InstIDEnd, 'GBK')

    def gethbtotal_little(self):
        '''散户保值买入持仓量定义'''
        return self.hbtotal_little

    def gethbtotal_medium(self):
        '''中户保值买入持仓量定义'''
        return self.hbtotal_medium

    def gethstotal_little(self):
        '''散户保值卖出持仓量定义'''
        return self.hstotal_little

    def gethstotal_medium(self):
        '''中户保值卖出持仓量定义'''
        return self.hstotal_medium

    def gethtotal_little(self):
        '''散户保值持仓量定义'''
        return self.htotal_little

    def gethtotal_medium(self):
        '''中户保值持仓量定义'''
        return self.htotal_medium

    def getsbtotal_little(self):
        '''散户投机买入持仓量定义'''
        return self.sbtotal_little

    def getsbtotal_medium(self):
        '''中户投机买入持仓量定义'''
        return self.sbtotal_medium

    def getsstotal_little(self):
        '''散户投机卖出持仓量定义'''
        return self.sstotal_little

    def getsstotal_medium(self):
        '''中户投机卖出持仓量定义'''
        return self.sstotal_medium

    def getstotal_little(self):
        '''散户投机持仓量定义'''
        return self.stotal_little

    def getstotal_medium(self):
        '''中户投机持仓量定义'''
        return self.stotal_medium

    def getbuytotal_little(self):
        '''散户买入持仓量定义'''
        return self.buytotal_little

    def getbuytotal_medium(self):
        '''中户买入持仓量定义'''
        return self.buytotal_medium

    def getselltotal_little(self):
        '''散户卖出持仓量定义'''
        return self.selltotal_little

    def getselltotal_medium(self):
        '''中户卖出持仓量定义'''
        return self.selltotal_medium

    def gettotal_little(self):
        '''散户总持仓量定义'''
        return self.total_little

    def gettotal_medium(self):
        '''中户总持仓量定义'''
        return self.total_medium

    def getValueMode(self):
        '''取值方式'''
        return TShfeFtdcValueModeType(ord(self.ValueMode))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InstIDStart'={self.getInstIDStart()}, 'InstIDEnd'={self.getInstIDEnd()}, 'hbtotal_little'={self.gethbtotal_little()}, 'hbtotal_medium'={self.gethbtotal_medium()}, 'hstotal_little'={self.gethstotal_little()}, 'hstotal_medium'={self.gethstotal_medium()}, 'htotal_little'={self.gethtotal_little()}, 'htotal_medium'={self.gethtotal_medium()}, 'sbtotal_little'={self.getsbtotal_little()}, 'sbtotal_medium'={self.getsbtotal_medium()}, 'sstotal_little'={self.getsstotal_little()}, 'sstotal_medium'={self.getsstotal_medium()}, 'stotal_little'={self.getstotal_little()}, 'stotal_medium'={self.getstotal_medium()}, 'buytotal_little'={self.getbuytotal_little()}, 'buytotal_medium'={self.getbuytotal_medium()}, 'selltotal_little'={self.getselltotal_little()}, 'selltotal_medium'={self.getselltotal_medium()}, 'total_little'={self.gettotal_little()}, 'total_medium'={self.gettotal_medium()}, 'ValueMode'={self.getValueMode()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InstIDStart': self.getInstIDStart(), 'InstIDEnd': self.getInstIDEnd(), 'hbtotal_little': self.gethbtotal_little(), 'hbtotal_medium': self.gethbtotal_medium(), 'hstotal_little': self.gethstotal_little(), 'hstotal_medium': self.gethstotal_medium(), 'htotal_little': self.gethtotal_little(), 'htotal_medium': self.gethtotal_medium(), 'sbtotal_little': self.getsbtotal_little(), 'sbtotal_medium': self.getsbtotal_medium(), 'sstotal_little': self.getsstotal_little(), 'sstotal_medium': self.getsstotal_medium(), 'stotal_little': self.getstotal_little(), 'stotal_medium': self.getstotal_medium(), 'buytotal_little': self.getbuytotal_little(), 'buytotal_medium': self.getbuytotal_medium(), 'selltotal_little': self.getselltotal_little(), 'selltotal_medium': self.getselltotal_medium(), 'total_little': self.gettotal_little(), 'total_medium': self.gettotal_medium(), 'ValueMode': self.getValueMode()}


class  CShfeFtdcRspInstPositionRateField(Structure):
    """合约持仓比例应答"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InstrumentID", c_char*31),
        ("hbtotal_amt_little", c_int32),
        ("hbtotal_amt_medium", c_int32),
        ("hbtotal_amt_large", c_int32),
        ("hstotal_amt_little", c_int32),
        ("hstotal_amt_medium", c_int32),
        ("hstotal_amt_large", c_int32),
        ("htotal_amt_little", c_int32),
        ("htotal_amt_medium", c_int32),
        ("htotal_amt_large", c_int32),
        ("sbtotal_amt_little", c_int32),
        ("sbtotal_amt_medium", c_int32),
        ("sbtotal_amt_large", c_int32),
        ("sstotal_amt_little", c_int32),
        ("sstotal_amt_medium", c_int32),
        ("sstotal_amt_large", c_int32),
        ("stotal_amt_little", c_int32),
        ("stotal_amt_medium", c_int32),
        ("stotal_amt_large", c_int32),
        ("buytotal_amt_little", c_int32),
        ("buytotal_amt_medium", c_int32),
        ("buytotal_amt_large", c_int32),
        ("selltotal_amt_little", c_int32),
        ("selltotal_amt_medium", c_int32),
        ("selltotal_amt_large", c_int32),
        ("total_amt_little", c_int32),
        ("total_amt_medium", c_int32),
        ("total_amt_large", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def gethbtotal_amt_little(self):
        '''散户保值买入持仓量'''
        return self.hbtotal_amt_little

    def gethbtotal_amt_medium(self):
        '''中户保值买入持仓量'''
        return self.hbtotal_amt_medium

    def gethbtotal_amt_large(self):
        '''大户保值买入持仓量'''
        return self.hbtotal_amt_large

    def gethstotal_amt_little(self):
        '''散户保值卖出持仓量'''
        return self.hstotal_amt_little

    def gethstotal_amt_medium(self):
        '''中户保值卖出持仓量'''
        return self.hstotal_amt_medium

    def gethstotal_amt_large(self):
        '''大户保值卖出持仓量'''
        return self.hstotal_amt_large

    def gethtotal_amt_little(self):
        '''散户保值持仓量'''
        return self.htotal_amt_little

    def gethtotal_amt_medium(self):
        '''中户保值持仓量'''
        return self.htotal_amt_medium

    def gethtotal_amt_large(self):
        '''大户保值持仓量'''
        return self.htotal_amt_large

    def getsbtotal_amt_little(self):
        '''散户投机买入持仓量'''
        return self.sbtotal_amt_little

    def getsbtotal_amt_medium(self):
        '''中户投机买入持仓量'''
        return self.sbtotal_amt_medium

    def getsbtotal_amt_large(self):
        '''大户投机买入持仓量'''
        return self.sbtotal_amt_large

    def getsstotal_amt_little(self):
        '''散户投机卖出持仓量'''
        return self.sstotal_amt_little

    def getsstotal_amt_medium(self):
        '''中户投机卖出持仓量'''
        return self.sstotal_amt_medium

    def getsstotal_amt_large(self):
        '''大户投机卖出持仓量'''
        return self.sstotal_amt_large

    def getstotal_amt_little(self):
        '''散户投机持仓量'''
        return self.stotal_amt_little

    def getstotal_amt_medium(self):
        '''中户投机持仓量'''
        return self.stotal_amt_medium

    def getstotal_amt_large(self):
        '''大户投机持仓量'''
        return self.stotal_amt_large

    def getbuytotal_amt_little(self):
        '''散户买入持仓量'''
        return self.buytotal_amt_little

    def getbuytotal_amt_medium(self):
        '''中户买入持仓量'''
        return self.buytotal_amt_medium

    def getbuytotal_amt_large(self):
        '''大户买入持仓量'''
        return self.buytotal_amt_large

    def getselltotal_amt_little(self):
        '''散户卖出持仓量'''
        return self.selltotal_amt_little

    def getselltotal_amt_medium(self):
        '''中户卖出持仓量'''
        return self.selltotal_amt_medium

    def getselltotal_amt_large(self):
        '''大户卖出持仓量'''
        return self.selltotal_amt_large

    def gettotal_amt_little(self):
        '''散户总持仓量'''
        return self.total_amt_little

    def gettotal_amt_medium(self):
        '''中户总持仓量'''
        return self.total_amt_medium

    def gettotal_amt_large(self):
        '''大户总持仓量'''
        return self.total_amt_large

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InstrumentID'={self.getInstrumentID()}, 'hbtotal_amt_little'={self.gethbtotal_amt_little()}, 'hbtotal_amt_medium'={self.gethbtotal_amt_medium()}, 'hbtotal_amt_large'={self.gethbtotal_amt_large()}, 'hstotal_amt_little'={self.gethstotal_amt_little()}, 'hstotal_amt_medium'={self.gethstotal_amt_medium()}, 'hstotal_amt_large'={self.gethstotal_amt_large()}, 'htotal_amt_little'={self.gethtotal_amt_little()}, 'htotal_amt_medium'={self.gethtotal_amt_medium()}, 'htotal_amt_large'={self.gethtotal_amt_large()}, 'sbtotal_amt_little'={self.getsbtotal_amt_little()}, 'sbtotal_amt_medium'={self.getsbtotal_amt_medium()}, 'sbtotal_amt_large'={self.getsbtotal_amt_large()}, 'sstotal_amt_little'={self.getsstotal_amt_little()}, 'sstotal_amt_medium'={self.getsstotal_amt_medium()}, 'sstotal_amt_large'={self.getsstotal_amt_large()}, 'stotal_amt_little'={self.getstotal_amt_little()}, 'stotal_amt_medium'={self.getstotal_amt_medium()}, 'stotal_amt_large'={self.getstotal_amt_large()}, 'buytotal_amt_little'={self.getbuytotal_amt_little()}, 'buytotal_amt_medium'={self.getbuytotal_amt_medium()}, 'buytotal_amt_large'={self.getbuytotal_amt_large()}, 'selltotal_amt_little'={self.getselltotal_amt_little()}, 'selltotal_amt_medium'={self.getselltotal_amt_medium()}, 'selltotal_amt_large'={self.getselltotal_amt_large()}, 'total_amt_little'={self.gettotal_amt_little()}, 'total_amt_medium'={self.gettotal_amt_medium()}, 'total_amt_large'={self.gettotal_amt_large()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InstrumentID': self.getInstrumentID(), 'hbtotal_amt_little': self.gethbtotal_amt_little(), 'hbtotal_amt_medium': self.gethbtotal_amt_medium(), 'hbtotal_amt_large': self.gethbtotal_amt_large(), 'hstotal_amt_little': self.gethstotal_amt_little(), 'hstotal_amt_medium': self.gethstotal_amt_medium(), 'hstotal_amt_large': self.gethstotal_amt_large(), 'htotal_amt_little': self.gethtotal_amt_little(), 'htotal_amt_medium': self.gethtotal_amt_medium(), 'htotal_amt_large': self.gethtotal_amt_large(), 'sbtotal_amt_little': self.getsbtotal_amt_little(), 'sbtotal_amt_medium': self.getsbtotal_amt_medium(), 'sbtotal_amt_large': self.getsbtotal_amt_large(), 'sstotal_amt_little': self.getsstotal_amt_little(), 'sstotal_amt_medium': self.getsstotal_amt_medium(), 'sstotal_amt_large': self.getsstotal_amt_large(), 'stotal_amt_little': self.getstotal_amt_little(), 'stotal_amt_medium': self.getstotal_amt_medium(), 'stotal_amt_large': self.getstotal_amt_large(), 'buytotal_amt_little': self.getbuytotal_amt_little(), 'buytotal_amt_medium': self.getbuytotal_amt_medium(), 'buytotal_amt_large': self.getbuytotal_amt_large(), 'selltotal_amt_little': self.getselltotal_amt_little(), 'selltotal_amt_medium': self.getselltotal_amt_medium(), 'selltotal_amt_large': self.getselltotal_amt_large(), 'total_amt_little': self.gettotal_amt_little(), 'total_amt_medium': self.gettotal_amt_medium(), 'total_amt_large': self.gettotal_amt_large()}


class  CShfeFtdcQryProductPositionRateField(Structure):
    """产品持仓比例查询"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("ProductID", c_char*31),
        ("hbtotal_little", c_double),
        ("hbtotal_medium", c_double),
        ("hstotal_little", c_double),
        ("hstotal_medium", c_double),
        ("htotal_little", c_double),
        ("htotal_medium", c_double),
        ("sbtotal_little", c_double),
        ("sbtotal_medium", c_double),
        ("sstotal_little", c_double),
        ("sstotal_medium", c_double),
        ("stotal_little", c_double),
        ("stotal_medium", c_double),
        ("buytotal_little", c_double),
        ("buytotal_medium", c_double),
        ("selltotal_little", c_double),
        ("selltotal_medium", c_double),
        ("total_little", c_double),
        ("total_medium", c_double),
        ("ValueMode", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def gethbtotal_little(self):
        '''散户保值买入持仓量定义'''
        return self.hbtotal_little

    def gethbtotal_medium(self):
        '''中户保值买入持仓量定义'''
        return self.hbtotal_medium

    def gethstotal_little(self):
        '''散户保值卖出持仓量定义'''
        return self.hstotal_little

    def gethstotal_medium(self):
        '''中户保值卖出持仓量定义'''
        return self.hstotal_medium

    def gethtotal_little(self):
        '''散户保值持仓量定义'''
        return self.htotal_little

    def gethtotal_medium(self):
        '''中户保值持仓量定义'''
        return self.htotal_medium

    def getsbtotal_little(self):
        '''散户投机买入持仓量定义'''
        return self.sbtotal_little

    def getsbtotal_medium(self):
        '''中户投机买入持仓量定义'''
        return self.sbtotal_medium

    def getsstotal_little(self):
        '''散户投机卖出持仓量定义'''
        return self.sstotal_little

    def getsstotal_medium(self):
        '''中户投机卖出持仓量定义'''
        return self.sstotal_medium

    def getstotal_little(self):
        '''散户投机持仓量定义'''
        return self.stotal_little

    def getstotal_medium(self):
        '''中户投机持仓量定义'''
        return self.stotal_medium

    def getbuytotal_little(self):
        '''散户买入持仓量定义'''
        return self.buytotal_little

    def getbuytotal_medium(self):
        '''中户买入持仓量定义'''
        return self.buytotal_medium

    def getselltotal_little(self):
        '''散户卖出持仓量定义'''
        return self.selltotal_little

    def getselltotal_medium(self):
        '''中户卖出持仓量定义'''
        return self.selltotal_medium

    def gettotal_little(self):
        '''散户总持仓量定义'''
        return self.total_little

    def gettotal_medium(self):
        '''中户总持仓量定义'''
        return self.total_medium

    def getValueMode(self):
        '''取值方式'''
        return TShfeFtdcValueModeType(ord(self.ValueMode))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'ProductID'={self.getProductID()}, 'hbtotal_little'={self.gethbtotal_little()}, 'hbtotal_medium'={self.gethbtotal_medium()}, 'hstotal_little'={self.gethstotal_little()}, 'hstotal_medium'={self.gethstotal_medium()}, 'htotal_little'={self.gethtotal_little()}, 'htotal_medium'={self.gethtotal_medium()}, 'sbtotal_little'={self.getsbtotal_little()}, 'sbtotal_medium'={self.getsbtotal_medium()}, 'sstotal_little'={self.getsstotal_little()}, 'sstotal_medium'={self.getsstotal_medium()}, 'stotal_little'={self.getstotal_little()}, 'stotal_medium'={self.getstotal_medium()}, 'buytotal_little'={self.getbuytotal_little()}, 'buytotal_medium'={self.getbuytotal_medium()}, 'selltotal_little'={self.getselltotal_little()}, 'selltotal_medium'={self.getselltotal_medium()}, 'total_little'={self.gettotal_little()}, 'total_medium'={self.gettotal_medium()}, 'ValueMode'={self.getValueMode()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'ProductID': self.getProductID(), 'hbtotal_little': self.gethbtotal_little(), 'hbtotal_medium': self.gethbtotal_medium(), 'hstotal_little': self.gethstotal_little(), 'hstotal_medium': self.gethstotal_medium(), 'htotal_little': self.gethtotal_little(), 'htotal_medium': self.gethtotal_medium(), 'sbtotal_little': self.getsbtotal_little(), 'sbtotal_medium': self.getsbtotal_medium(), 'sstotal_little': self.getsstotal_little(), 'sstotal_medium': self.getsstotal_medium(), 'stotal_little': self.getstotal_little(), 'stotal_medium': self.getstotal_medium(), 'buytotal_little': self.getbuytotal_little(), 'buytotal_medium': self.getbuytotal_medium(), 'selltotal_little': self.getselltotal_little(), 'selltotal_medium': self.getselltotal_medium(), 'total_little': self.gettotal_little(), 'total_medium': self.gettotal_medium(), 'ValueMode': self.getValueMode()}


class  CShfeFtdcRspProductPositionRateField(Structure):
    """产品持仓比例"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("ProductID", c_char*31),
        ("hbtotal_amt_little", c_int32),
        ("hbtotal_amt_medium", c_int32),
        ("hbtotal_amt_large", c_int32),
        ("hstotal_amt_little", c_int32),
        ("hstotal_amt_medium", c_int32),
        ("hstotal_amt_large", c_int32),
        ("htotal_amt_little", c_int32),
        ("htotal_amt_medium", c_int32),
        ("htotal_amt_large", c_int32),
        ("sbtotal_amt_little", c_int32),
        ("sbtotal_amt_medium", c_int32),
        ("sbtotal_amt_large", c_int32),
        ("sstotal_amt_little", c_int32),
        ("sstotal_amt_medium", c_int32),
        ("sstotal_amt_large", c_int32),
        ("stotal_amt_little", c_int32),
        ("stotal_amt_medium", c_int32),
        ("stotal_amt_large", c_int32),
        ("buytotal_amt_little", c_int32),
        ("buytotal_amt_medium", c_int32),
        ("buytotal_amt_large", c_int32),
        ("selltotal_amt_little", c_int32),
        ("selltotal_amt_medium", c_int32),
        ("selltotal_amt_large", c_int32),
        ("total_amt_little", c_int32),
        ("total_amt_medium", c_int32),
        ("total_amt_large", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def gethbtotal_amt_little(self):
        '''散户保值买入持仓量'''
        return self.hbtotal_amt_little

    def gethbtotal_amt_medium(self):
        '''中户保值买入持仓量'''
        return self.hbtotal_amt_medium

    def gethbtotal_amt_large(self):
        '''大户保值买入持仓量'''
        return self.hbtotal_amt_large

    def gethstotal_amt_little(self):
        '''散户保值卖出持仓量'''
        return self.hstotal_amt_little

    def gethstotal_amt_medium(self):
        '''中户保值卖出持仓量'''
        return self.hstotal_amt_medium

    def gethstotal_amt_large(self):
        '''大户保值卖出持仓量'''
        return self.hstotal_amt_large

    def gethtotal_amt_little(self):
        '''散户保值持仓量'''
        return self.htotal_amt_little

    def gethtotal_amt_medium(self):
        '''中户保值持仓量'''
        return self.htotal_amt_medium

    def gethtotal_amt_large(self):
        '''大户保值持仓量'''
        return self.htotal_amt_large

    def getsbtotal_amt_little(self):
        '''散户投机买入持仓量'''
        return self.sbtotal_amt_little

    def getsbtotal_amt_medium(self):
        '''中户投机买入持仓量'''
        return self.sbtotal_amt_medium

    def getsbtotal_amt_large(self):
        '''大户投机买入持仓量'''
        return self.sbtotal_amt_large

    def getsstotal_amt_little(self):
        '''散户投机卖出持仓量'''
        return self.sstotal_amt_little

    def getsstotal_amt_medium(self):
        '''中户投机卖出持仓量'''
        return self.sstotal_amt_medium

    def getsstotal_amt_large(self):
        '''大户投机卖出持仓量'''
        return self.sstotal_amt_large

    def getstotal_amt_little(self):
        '''散户投机持仓量'''
        return self.stotal_amt_little

    def getstotal_amt_medium(self):
        '''中户投机持仓量'''
        return self.stotal_amt_medium

    def getstotal_amt_large(self):
        '''大户投机持仓量'''
        return self.stotal_amt_large

    def getbuytotal_amt_little(self):
        '''散户买入持仓量'''
        return self.buytotal_amt_little

    def getbuytotal_amt_medium(self):
        '''中户买入持仓量'''
        return self.buytotal_amt_medium

    def getbuytotal_amt_large(self):
        '''大户买入持仓量'''
        return self.buytotal_amt_large

    def getselltotal_amt_little(self):
        '''散户卖出持仓量'''
        return self.selltotal_amt_little

    def getselltotal_amt_medium(self):
        '''中户卖出持仓量'''
        return self.selltotal_amt_medium

    def getselltotal_amt_large(self):
        '''大户卖出持仓量'''
        return self.selltotal_amt_large

    def gettotal_amt_little(self):
        '''散户总持仓量'''
        return self.total_amt_little

    def gettotal_amt_medium(self):
        '''中户总持仓量'''
        return self.total_amt_medium

    def gettotal_amt_large(self):
        '''大户总持仓量'''
        return self.total_amt_large

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'ProductID'={self.getProductID()}, 'hbtotal_amt_little'={self.gethbtotal_amt_little()}, 'hbtotal_amt_medium'={self.gethbtotal_amt_medium()}, 'hbtotal_amt_large'={self.gethbtotal_amt_large()}, 'hstotal_amt_little'={self.gethstotal_amt_little()}, 'hstotal_amt_medium'={self.gethstotal_amt_medium()}, 'hstotal_amt_large'={self.gethstotal_amt_large()}, 'htotal_amt_little'={self.gethtotal_amt_little()}, 'htotal_amt_medium'={self.gethtotal_amt_medium()}, 'htotal_amt_large'={self.gethtotal_amt_large()}, 'sbtotal_amt_little'={self.getsbtotal_amt_little()}, 'sbtotal_amt_medium'={self.getsbtotal_amt_medium()}, 'sbtotal_amt_large'={self.getsbtotal_amt_large()}, 'sstotal_amt_little'={self.getsstotal_amt_little()}, 'sstotal_amt_medium'={self.getsstotal_amt_medium()}, 'sstotal_amt_large'={self.getsstotal_amt_large()}, 'stotal_amt_little'={self.getstotal_amt_little()}, 'stotal_amt_medium'={self.getstotal_amt_medium()}, 'stotal_amt_large'={self.getstotal_amt_large()}, 'buytotal_amt_little'={self.getbuytotal_amt_little()}, 'buytotal_amt_medium'={self.getbuytotal_amt_medium()}, 'buytotal_amt_large'={self.getbuytotal_amt_large()}, 'selltotal_amt_little'={self.getselltotal_amt_little()}, 'selltotal_amt_medium'={self.getselltotal_amt_medium()}, 'selltotal_amt_large'={self.getselltotal_amt_large()}, 'total_amt_little'={self.gettotal_amt_little()}, 'total_amt_medium'={self.gettotal_amt_medium()}, 'total_amt_large'={self.gettotal_amt_large()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'ProductID': self.getProductID(), 'hbtotal_amt_little': self.gethbtotal_amt_little(), 'hbtotal_amt_medium': self.gethbtotal_amt_medium(), 'hbtotal_amt_large': self.gethbtotal_amt_large(), 'hstotal_amt_little': self.gethstotal_amt_little(), 'hstotal_amt_medium': self.gethstotal_amt_medium(), 'hstotal_amt_large': self.gethstotal_amt_large(), 'htotal_amt_little': self.gethtotal_amt_little(), 'htotal_amt_medium': self.gethtotal_amt_medium(), 'htotal_amt_large': self.gethtotal_amt_large(), 'sbtotal_amt_little': self.getsbtotal_amt_little(), 'sbtotal_amt_medium': self.getsbtotal_amt_medium(), 'sbtotal_amt_large': self.getsbtotal_amt_large(), 'sstotal_amt_little': self.getsstotal_amt_little(), 'sstotal_amt_medium': self.getsstotal_amt_medium(), 'sstotal_amt_large': self.getsstotal_amt_large(), 'stotal_amt_little': self.getstotal_amt_little(), 'stotal_amt_medium': self.getstotal_amt_medium(), 'stotal_amt_large': self.getstotal_amt_large(), 'buytotal_amt_little': self.getbuytotal_amt_little(), 'buytotal_amt_medium': self.getbuytotal_amt_medium(), 'buytotal_amt_large': self.getbuytotal_amt_large(), 'selltotal_amt_little': self.getselltotal_amt_little(), 'selltotal_amt_medium': self.getselltotal_amt_medium(), 'selltotal_amt_large': self.getselltotal_amt_large(), 'total_amt_little': self.gettotal_amt_little(), 'total_amt_medium': self.gettotal_amt_medium(), 'total_amt_large': self.gettotal_amt_large()}


class  CShfeFtdcIsWriteOnceField(Structure):
    """历史模拟法压力测试只返回一次结果"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("IsWriteOnce", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getIsWriteOnce(self):
        '''是否只返回一次结果'''
        return self.IsWriteOnce

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'IsWriteOnce'={self.getIsWriteOnce()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'IsWriteOnce': self.getIsWriteOnce()}


class  CShfeFtdcSTSettlePriceField(Structure):
    """压力测试结算价格(或浮动)"""
    _fields_ = [
        ("Day", c_int32),
        ("InstrumentID", c_char*31),
        ("PriceType", c_char),
        ("Price", c_double),
    ]

    def getDay(self):
        '''第几天'''
        return self.Day

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getPriceType(self):
        '''结算价格类型(Day=1时有效)'''
        return TShfeFtdcSTPriceTypeType(ord(self.PriceType))

    def getPrice(self):
        '''结算价格(或浮动)'''
        return self.Price

    @property
    def __str__(self):
        return f"'Day'={self.getDay()}, 'InstrumentID'={self.getInstrumentID()}, 'PriceType'={self.getPriceType()}, 'Price'={self.getPrice()}"

    @property
    def __dict__(self):
        return {'Day': self.getDay(), 'InstrumentID': self.getInstrumentID(), 'PriceType': self.getPriceType(), 'Price': self.getPrice()}


class  CShfeFtdcSTInstrumentMarginRateField(Structure):
    """压力测试投资者保证金率"""
    _fields_ = [
        ("Day", c_int32),
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("IsRelative", c_int32),
    ]

    def getDay(self):
        '''第几天'''
        return self.Day

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getIsRelative(self):
        '''是否相对交易所收取'''
        return self.IsRelative

    @property
    def __str__(self):
        return f"'Day'={self.getDay()}, 'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'IsRelative'={self.getIsRelative()}"

    @property
    def __dict__(self):
        return {'Day': self.getDay(), 'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'IsRelative': self.getIsRelative()}


class  CShfeFtdcSTInstrumentMarginRateAdjustField(Structure):
    """压力测试投资者保证金率调整"""
    _fields_ = [
        ("Day", c_int32),
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("IsRelative", c_int32),
    ]

    def getDay(self):
        '''第几天'''
        return self.Day

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getIsRelative(self):
        '''是否相对交易所收取'''
        return self.IsRelative

    @property
    def __str__(self):
        return f"'Day'={self.getDay()}, 'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'IsRelative'={self.getIsRelative()}"

    @property
    def __dict__(self):
        return {'Day': self.getDay(), 'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'IsRelative': self.getIsRelative()}


class  CShfeFtdcSTExchangeMarginRateField(Structure):
    """压力测试交易所保证金率"""
    _fields_ = [
        ("Day", c_int32),
        ("BrokerID", c_char*11),
        ("InstrumentID", c_char*31),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
    ]

    def getDay(self):
        '''第几天'''
        return self.Day

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    @property
    def __str__(self):
        return f"'Day'={self.getDay()}, 'BrokerID'={self.getBrokerID()}, 'InstrumentID'={self.getInstrumentID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}"

    @property
    def __dict__(self):
        return {'Day': self.getDay(), 'BrokerID': self.getBrokerID(), 'InstrumentID': self.getInstrumentID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume()}


class  CShfeFtdcSTExchangeMarginRateAdjustField(Structure):
    """压力测试交易所保证金率调整"""
    _fields_ = [
        ("Day", c_int32),
        ("BrokerID", c_char*11),
        ("InstrumentID", c_char*31),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("ExchLongMarginRatioByMoney", c_double),
        ("ExchLongMarginRatioByVolume", c_double),
        ("ExchShortMarginRatioByMoney", c_double),
        ("ExchShortMarginRatioByVolume", c_double),
        ("NoLongMarginRatioByMoney", c_double),
        ("NoLongMarginRatioByVolume", c_double),
        ("NoShortMarginRatioByMoney", c_double),
        ("NoShortMarginRatioByVolume", c_double),
    ]

    def getDay(self):
        '''第几天'''
        return self.Day

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''跟随交易所投资者多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''跟随交易所投资者多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''跟随交易所投资者空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''跟随交易所投资者空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getExchLongMarginRatioByMoney(self):
        '''交易所多头保证金率'''
        return self.ExchLongMarginRatioByMoney

    def getExchLongMarginRatioByVolume(self):
        '''交易所多头保证金费'''
        return self.ExchLongMarginRatioByVolume

    def getExchShortMarginRatioByMoney(self):
        '''交易所空头保证金率'''
        return self.ExchShortMarginRatioByMoney

    def getExchShortMarginRatioByVolume(self):
        '''交易所空头保证金费'''
        return self.ExchShortMarginRatioByVolume

    def getNoLongMarginRatioByMoney(self):
        '''不跟随交易所投资者多头保证金率'''
        return self.NoLongMarginRatioByMoney

    def getNoLongMarginRatioByVolume(self):
        '''不跟随交易所投资者多头保证金费'''
        return self.NoLongMarginRatioByVolume

    def getNoShortMarginRatioByMoney(self):
        '''不跟随交易所投资者空头保证金率'''
        return self.NoShortMarginRatioByMoney

    def getNoShortMarginRatioByVolume(self):
        '''不跟随交易所投资者空头保证金费'''
        return self.NoShortMarginRatioByVolume

    @property
    def __str__(self):
        return f"'Day'={self.getDay()}, 'BrokerID'={self.getBrokerID()}, 'InstrumentID'={self.getInstrumentID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'ExchLongMarginRatioByMoney'={self.getExchLongMarginRatioByMoney()}, 'ExchLongMarginRatioByVolume'={self.getExchLongMarginRatioByVolume()}, 'ExchShortMarginRatioByMoney'={self.getExchShortMarginRatioByMoney()}, 'ExchShortMarginRatioByVolume'={self.getExchShortMarginRatioByVolume()}, 'NoLongMarginRatioByMoney'={self.getNoLongMarginRatioByMoney()}, 'NoLongMarginRatioByVolume'={self.getNoLongMarginRatioByVolume()}, 'NoShortMarginRatioByMoney'={self.getNoShortMarginRatioByMoney()}, 'NoShortMarginRatioByVolume'={self.getNoShortMarginRatioByVolume()}"

    @property
    def __dict__(self):
        return {'Day': self.getDay(), 'BrokerID': self.getBrokerID(), 'InstrumentID': self.getInstrumentID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'ExchLongMarginRatioByMoney': self.getExchLongMarginRatioByMoney(), 'ExchLongMarginRatioByVolume': self.getExchLongMarginRatioByVolume(), 'ExchShortMarginRatioByMoney': self.getExchShortMarginRatioByMoney(), 'ExchShortMarginRatioByVolume': self.getExchShortMarginRatioByVolume(), 'NoLongMarginRatioByMoney': self.getNoLongMarginRatioByMoney(), 'NoLongMarginRatioByVolume': self.getNoLongMarginRatioByVolume(), 'NoShortMarginRatioByMoney': self.getNoShortMarginRatioByMoney(), 'NoShortMarginRatioByVolume': self.getNoShortMarginRatioByVolume()}


class  CShfeFtdcInvestorLinkManField(Structure):
    """投资者与联系人信息"""
    _fields_ = [
        ("InvestorID", c_char*13),
        ("BrokerID", c_char*11),
        ("InvestorGroupID", c_char*13),
        ("InvestorName", c_char*81),
        ("IdentifiedCardType", c_char),
        ("IdentifiedCardNo", c_char*51),
        ("IsActive", c_int32),
        ("Telephone", c_char*41),
        ("Address", c_char*101),
        ("OrderManIdentifiedCardType", c_char),
        ("OrderManIdentifiedCardNo", c_char*51),
        ("OrderManPersonName", c_char*81),
        ("OrderManTelephone", c_char*41),
        ("OrderManAddress", c_char*101),
        ("OrderManZipCode", c_char*7),
        ("FundManIdentifiedCardType", c_char),
        ("FundManIdentifiedCardNo", c_char*51),
        ("FundManPersonName", c_char*81),
        ("FundManTelephone", c_char*41),
        ("FundManAddress", c_char*101),
        ("FundManZipCode", c_char*7),
        ("OpenManIdentifiedCardType", c_char),
        ("OpenManIdentifiedCardNo", c_char*51),
        ("OpenManPersonName", c_char*81),
        ("OpenManTelephone", c_char*41),
        ("OpenManAddress", c_char*101),
        ("OpenManZipCode", c_char*7),
        ("SettlementManIdentifiedCardType", c_char),
        ("SettlementManIdentifiedCardNo", c_char*51),
        ("SettlementManPersonName", c_char*81),
        ("SettlementManTelephone", c_char*41),
        ("SettlementManAddress", c_char*101),
        ("SettlementManZipCode", c_char*7),
        ("OpenDate", c_char*9),
        ("Mobile", c_char*41),
        ("EMail", c_char*101),
        ("InvestorType", c_char),
        ("PhoneCountryCode", c_char*11),
        ("PhoneAreaCode", c_char*11),
        ("OpenPhoneCountryCode", c_char*11),
        ("OpenPhoneAreaCode", c_char*11),
        ("OrderPhoneCountryCode", c_char*11),
        ("OrderPhoneAreaCode", c_char*11),
        ("FundPhoneCountryCode", c_char*11),
        ("FundPhoneAreaCode", c_char*11),
        ("SettlePhoneCountryCode", c_char*11),
        ("SettlePhoneAreaCode", c_char*11),
        ("CompanyManIdentifiedCardType", c_char),
        ("CompanyManIdentifiedCardNo", c_char*51),
        ("CompanyManPersonName", c_char*81),
        ("CompanyManTelephone", c_char*41),
        ("CompanyManAddress", c_char*101),
        ("CompanyManZipCode", c_char*7),
        ("CorporationManIdentifiedCardType", c_char),
        ("CorporationManIdentifiedCardNo", c_char*51),
        ("CorporationManPersonName", c_char*81),
        ("CorporationManTelephone", c_char*41),
        ("CorporationManAddress", c_char*101),
        ("CorporationManZipCode", c_char*7),
        ("LinkManIdentifiedCardType", c_char),
        ("LinkManIdentifiedCardNo", c_char*51),
        ("LinkManPersonName", c_char*81),
        ("LinkManTelephone", c_char*41),
        ("LinkManAddress", c_char*101),
        ("LinkManZipCode", c_char*7),
        ("LedgerIdentifiedCardType", c_char),
        ("LedgerIdentifiedCardNo", c_char*51),
        ("LedgerPersonName", c_char*81),
        ("LedgerTelephone", c_char*41),
        ("LedgerAddress", c_char*101),
        ("LedgerZipCode", c_char*7),
        ("TrusteeIdentifiedCardType", c_char),
        ("TrusteeIdentifiedCardNo", c_char*51),
        ("TrusteePersonName", c_char*81),
        ("TrusteeTelephone", c_char*41),
        ("TrusteeAddress", c_char*101),
        ("TrusteeZipCode", c_char*7),
        ("TrusteeCorporationManIdentifiedCardType", c_char),
        ("TrusteeCorporationManIdentifiedCardNo", c_char*51),
        ("TrusteeCorporationManPersonName", c_char*81),
        ("TrusteeCorporationManTelephone", c_char*41),
        ("TrusteeCorporationManAddress", c_char*101),
        ("TrusteeCorporationManZipCode", c_char*7),
        ("TrusteeOpenManIdentifiedCardType", c_char),
        ("TrusteeOpenManIdentifiedCardNo", c_char*51),
        ("TrusteeOpenManPersonName", c_char*81),
        ("TrusteeOpenManTelephone", c_char*41),
        ("TrusteeOpenManAddress", c_char*101),
        ("TrusteeOpenManZipCode", c_char*7),
        ("TrusteeContactManIdentifiedCardType", c_char),
        ("TrusteeContactManIdentifiedCardNo", c_char*51),
        ("TrusteeContactManPersonName", c_char*81),
        ("TrusteeContactManTelephone", c_char*41),
        ("TrusteeContactManAddress", c_char*101),
        ("TrusteeContactManZipCode", c_char*7),
    ]

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorGroupID(self):
        '''投资者分组代码'''
        return str(self.InvestorGroupID, 'GBK')

    def getInvestorName(self):
        '''投资者名称'''
        return str(self.InvestorName, 'GBK')

    def getIdentifiedCardType(self):
        '''证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.IdentifiedCardType))

    def getIdentifiedCardNo(self):
        '''证件号码'''
        return str(self.IdentifiedCardNo, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    def getTelephone(self):
        '''联系电话'''
        return str(self.Telephone, 'GBK')

    def getAddress(self):
        '''通讯地址'''
        return str(self.Address, 'GBK')

    def getOrderManIdentifiedCardType(self):
        '''指定下单人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.OrderManIdentifiedCardType))

    def getOrderManIdentifiedCardNo(self):
        '''指定下单人证件号码'''
        return str(self.OrderManIdentifiedCardNo, 'GBK')

    def getOrderManPersonName(self):
        '''指定下单人名称'''
        return str(self.OrderManPersonName, 'GBK')

    def getOrderManTelephone(self):
        '''指定下单人联系电话'''
        return str(self.OrderManTelephone, 'GBK')

    def getOrderManAddress(self):
        '''指定下单人通讯地址'''
        return str(self.OrderManAddress, 'GBK')

    def getOrderManZipCode(self):
        '''指定下单人邮政编码'''
        return str(self.OrderManZipCode, 'GBK')

    def getFundManIdentifiedCardType(self):
        '''资金调拨人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.FundManIdentifiedCardType))

    def getFundManIdentifiedCardNo(self):
        '''资金调拨人证件号码'''
        return str(self.FundManIdentifiedCardNo, 'GBK')

    def getFundManPersonName(self):
        '''资金调拨人名称'''
        return str(self.FundManPersonName, 'GBK')

    def getFundManTelephone(self):
        '''资金调拨人联系电话'''
        return str(self.FundManTelephone, 'GBK')

    def getFundManAddress(self):
        '''资金调拨人通讯地址'''
        return str(self.FundManAddress, 'GBK')

    def getFundManZipCode(self):
        '''资金调拨人邮政编码'''
        return str(self.FundManZipCode, 'GBK')

    def getOpenManIdentifiedCardType(self):
        '''开户授权人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.OpenManIdentifiedCardType))

    def getOpenManIdentifiedCardNo(self):
        '''开户授权人证件号码'''
        return str(self.OpenManIdentifiedCardNo, 'GBK')

    def getOpenManPersonName(self):
        '''开户授权人名称'''
        return str(self.OpenManPersonName, 'GBK')

    def getOpenManTelephone(self):
        '''开户授权人联系电话'''
        return str(self.OpenManTelephone, 'GBK')

    def getOpenManAddress(self):
        '''开户授权人通讯地址'''
        return str(self.OpenManAddress, 'GBK')

    def getOpenManZipCode(self):
        '''开户授权人邮政编码'''
        return str(self.OpenManZipCode, 'GBK')

    def getSettlementManIdentifiedCardType(self):
        '''结算单确认人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.SettlementManIdentifiedCardType))

    def getSettlementManIdentifiedCardNo(self):
        '''结算单确认人证件号码'''
        return str(self.SettlementManIdentifiedCardNo, 'GBK')

    def getSettlementManPersonName(self):
        '''结算单确认人名称'''
        return str(self.SettlementManPersonName, 'GBK')

    def getSettlementManTelephone(self):
        '''结算单确认人联系电话'''
        return str(self.SettlementManTelephone, 'GBK')

    def getSettlementManAddress(self):
        '''结算单确认人通讯地址'''
        return str(self.SettlementManAddress, 'GBK')

    def getSettlementManZipCode(self):
        '''结算单确认人邮政编码'''
        return str(self.SettlementManZipCode, 'GBK')

    def getOpenDate(self):
        '''开户日期'''
        return str(self.OpenDate, 'GBK')

    def getMobile(self):
        '''手机'''
        return str(self.Mobile, 'GBK')

    def getEMail(self):
        '''电子邮件'''
        return str(self.EMail, 'GBK')

    def getInvestorType(self):
        '''投资者类型'''
        return TShfeFtdcInvestorTypeType(ord(self.InvestorType))

    def getPhoneCountryCode(self):
        '''国家代码'''
        return str(self.PhoneCountryCode, 'GBK')

    def getPhoneAreaCode(self):
        '''区号'''
        return str(self.PhoneAreaCode, 'GBK')

    def getOpenPhoneCountryCode(self):
        '''开户授权人国家代码'''
        return str(self.OpenPhoneCountryCode, 'GBK')

    def getOpenPhoneAreaCode(self):
        '''开户授权人区号'''
        return str(self.OpenPhoneAreaCode, 'GBK')

    def getOrderPhoneCountryCode(self):
        '''指定下单人国家代码'''
        return str(self.OrderPhoneCountryCode, 'GBK')

    def getOrderPhoneAreaCode(self):
        '''指定下单人区号'''
        return str(self.OrderPhoneAreaCode, 'GBK')

    def getFundPhoneCountryCode(self):
        '''资金调拨人国家代码'''
        return str(self.FundPhoneCountryCode, 'GBK')

    def getFundPhoneAreaCode(self):
        '''资金调拨人区号'''
        return str(self.FundPhoneAreaCode, 'GBK')

    def getSettlePhoneCountryCode(self):
        '''结算单确认人国家代码'''
        return str(self.SettlePhoneCountryCode, 'GBK')

    def getSettlePhoneAreaCode(self):
        '''结算单确认人区号'''
        return str(self.SettlePhoneAreaCode, 'GBK')

    def getCompanyManIdentifiedCardType(self):
        '''法人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.CompanyManIdentifiedCardType))

    def getCompanyManIdentifiedCardNo(self):
        '''法人证件号码'''
        return str(self.CompanyManIdentifiedCardNo, 'GBK')

    def getCompanyManPersonName(self):
        '''法人名称'''
        return str(self.CompanyManPersonName, 'GBK')

    def getCompanyManTelephone(self):
        '''法人联系电话'''
        return str(self.CompanyManTelephone, 'GBK')

    def getCompanyManAddress(self):
        '''法人通讯地址'''
        return str(self.CompanyManAddress, 'GBK')

    def getCompanyManZipCode(self):
        '''法人邮政编码'''
        return str(self.CompanyManZipCode, 'GBK')

    def getCorporationManIdentifiedCardType(self):
        '''法人代表证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.CorporationManIdentifiedCardType))

    def getCorporationManIdentifiedCardNo(self):
        '''法人代表证件号码'''
        return str(self.CorporationManIdentifiedCardNo, 'GBK')

    def getCorporationManPersonName(self):
        '''法人代表名称'''
        return str(self.CorporationManPersonName, 'GBK')

    def getCorporationManTelephone(self):
        '''法人代表联系电话'''
        return str(self.CorporationManTelephone, 'GBK')

    def getCorporationManAddress(self):
        '''法人代表通讯地址'''
        return str(self.CorporationManAddress, 'GBK')

    def getCorporationManZipCode(self):
        '''法人代表邮政编码'''
        return str(self.CorporationManZipCode, 'GBK')

    def getLinkManIdentifiedCardType(self):
        '''联系人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.LinkManIdentifiedCardType))

    def getLinkManIdentifiedCardNo(self):
        '''联系人证件号码'''
        return str(self.LinkManIdentifiedCardNo, 'GBK')

    def getLinkManPersonName(self):
        '''联系人名称'''
        return str(self.LinkManPersonName, 'GBK')

    def getLinkManTelephone(self):
        '''联系人联系电话'''
        return str(self.LinkManTelephone, 'GBK')

    def getLinkManAddress(self):
        '''联系人通讯地址'''
        return str(self.LinkManAddress, 'GBK')

    def getLinkManZipCode(self):
        '''联系人邮政编码'''
        return str(self.LinkManZipCode, 'GBK')

    def getLedgerIdentifiedCardType(self):
        '''分户管理资产负责人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.LedgerIdentifiedCardType))

    def getLedgerIdentifiedCardNo(self):
        '''分户管理资产负责人证件号码'''
        return str(self.LedgerIdentifiedCardNo, 'GBK')

    def getLedgerPersonName(self):
        '''分户管理资产负责人名称'''
        return str(self.LedgerPersonName, 'GBK')

    def getLedgerTelephone(self):
        '''分户管理资产负责人联系电话'''
        return str(self.LedgerTelephone, 'GBK')

    def getLedgerAddress(self):
        '''分户管理资产负责人通讯地址'''
        return str(self.LedgerAddress, 'GBK')

    def getLedgerZipCode(self):
        '''分户管理资产负责人邮政编码'''
        return str(self.LedgerZipCode, 'GBK')

    def getTrusteeIdentifiedCardType(self):
        '''托管人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.TrusteeIdentifiedCardType))

    def getTrusteeIdentifiedCardNo(self):
        '''托管人证件号码'''
        return str(self.TrusteeIdentifiedCardNo, 'GBK')

    def getTrusteePersonName(self):
        '''托管人名称'''
        return str(self.TrusteePersonName, 'GBK')

    def getTrusteeTelephone(self):
        '''托管人联系电话'''
        return str(self.TrusteeTelephone, 'GBK')

    def getTrusteeAddress(self):
        '''托管人通讯地址'''
        return str(self.TrusteeAddress, 'GBK')

    def getTrusteeZipCode(self):
        '''托管人邮政编码'''
        return str(self.TrusteeZipCode, 'GBK')

    def getTrusteeCorporationManIdentifiedCardType(self):
        '''托管机构法人代表证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.TrusteeCorporationManIdentifiedCardType))

    def getTrusteeCorporationManIdentifiedCardNo(self):
        '''托管机构法人代表证件号码'''
        return str(self.TrusteeCorporationManIdentifiedCardNo, 'GBK')

    def getTrusteeCorporationManPersonName(self):
        '''托管机构法人代表名称'''
        return str(self.TrusteeCorporationManPersonName, 'GBK')

    def getTrusteeCorporationManTelephone(self):
        '''托管机构法人代表联系电话'''
        return str(self.TrusteeCorporationManTelephone, 'GBK')

    def getTrusteeCorporationManAddress(self):
        '''托管机构法人代表通讯地址'''
        return str(self.TrusteeCorporationManAddress, 'GBK')

    def getTrusteeCorporationManZipCode(self):
        '''托管机构法人代表邮政编码'''
        return str(self.TrusteeCorporationManZipCode, 'GBK')

    def getTrusteeOpenManIdentifiedCardType(self):
        '''托管机构开户授权人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.TrusteeOpenManIdentifiedCardType))

    def getTrusteeOpenManIdentifiedCardNo(self):
        '''托管机构开户授权人证件号码'''
        return str(self.TrusteeOpenManIdentifiedCardNo, 'GBK')

    def getTrusteeOpenManPersonName(self):
        '''托管机构开户授权人名称'''
        return str(self.TrusteeOpenManPersonName, 'GBK')

    def getTrusteeOpenManTelephone(self):
        '''托管机构开户授权人联系电话'''
        return str(self.TrusteeOpenManTelephone, 'GBK')

    def getTrusteeOpenManAddress(self):
        '''托管机构开户授权人通讯地址'''
        return str(self.TrusteeOpenManAddress, 'GBK')

    def getTrusteeOpenManZipCode(self):
        '''托管机构开户授权人邮政编码'''
        return str(self.TrusteeOpenManZipCode, 'GBK')

    def getTrusteeContactManIdentifiedCardType(self):
        '''托管机构联系人证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.TrusteeContactManIdentifiedCardType))

    def getTrusteeContactManIdentifiedCardNo(self):
        '''托管机构联系人证件号码'''
        return str(self.TrusteeContactManIdentifiedCardNo, 'GBK')

    def getTrusteeContactManPersonName(self):
        '''托管机构联系人名称'''
        return str(self.TrusteeContactManPersonName, 'GBK')

    def getTrusteeContactManTelephone(self):
        '''托管机构联系人联系电话'''
        return str(self.TrusteeContactManTelephone, 'GBK')

    def getTrusteeContactManAddress(self):
        '''托管机构联系人通讯地址'''
        return str(self.TrusteeContactManAddress, 'GBK')

    def getTrusteeContactManZipCode(self):
        '''托管机构联系人邮政编码'''
        return str(self.TrusteeContactManZipCode, 'GBK')

    @property
    def __str__(self):
        return f"'InvestorID'={self.getInvestorID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorGroupID'={self.getInvestorGroupID()}, 'InvestorName'={self.getInvestorName()}, 'IdentifiedCardType'={self.getIdentifiedCardType()}, 'IdentifiedCardNo'={self.getIdentifiedCardNo()}, 'IsActive'={self.getIsActive()}, 'Telephone'={self.getTelephone()}, 'Address'={self.getAddress()}, 'OrderManIdentifiedCardType'={self.getOrderManIdentifiedCardType()}, 'OrderManIdentifiedCardNo'={self.getOrderManIdentifiedCardNo()}, 'OrderManPersonName'={self.getOrderManPersonName()}, 'OrderManTelephone'={self.getOrderManTelephone()}, 'OrderManAddress'={self.getOrderManAddress()}, 'OrderManZipCode'={self.getOrderManZipCode()}, 'FundManIdentifiedCardType'={self.getFundManIdentifiedCardType()}, 'FundManIdentifiedCardNo'={self.getFundManIdentifiedCardNo()}, 'FundManPersonName'={self.getFundManPersonName()}, 'FundManTelephone'={self.getFundManTelephone()}, 'FundManAddress'={self.getFundManAddress()}, 'FundManZipCode'={self.getFundManZipCode()}, 'OpenManIdentifiedCardType'={self.getOpenManIdentifiedCardType()}, 'OpenManIdentifiedCardNo'={self.getOpenManIdentifiedCardNo()}, 'OpenManPersonName'={self.getOpenManPersonName()}, 'OpenManTelephone'={self.getOpenManTelephone()}, 'OpenManAddress'={self.getOpenManAddress()}, 'OpenManZipCode'={self.getOpenManZipCode()}, 'SettlementManIdentifiedCardType'={self.getSettlementManIdentifiedCardType()}, 'SettlementManIdentifiedCardNo'={self.getSettlementManIdentifiedCardNo()}, 'SettlementManPersonName'={self.getSettlementManPersonName()}, 'SettlementManTelephone'={self.getSettlementManTelephone()}, 'SettlementManAddress'={self.getSettlementManAddress()}, 'SettlementManZipCode'={self.getSettlementManZipCode()}, 'OpenDate'={self.getOpenDate()}, 'Mobile'={self.getMobile()}, 'EMail'={self.getEMail()}, 'InvestorType'={self.getInvestorType()}, 'PhoneCountryCode'={self.getPhoneCountryCode()}, 'PhoneAreaCode'={self.getPhoneAreaCode()}, 'OpenPhoneCountryCode'={self.getOpenPhoneCountryCode()}, 'OpenPhoneAreaCode'={self.getOpenPhoneAreaCode()}, 'OrderPhoneCountryCode'={self.getOrderPhoneCountryCode()}, 'OrderPhoneAreaCode'={self.getOrderPhoneAreaCode()}, 'FundPhoneCountryCode'={self.getFundPhoneCountryCode()}, 'FundPhoneAreaCode'={self.getFundPhoneAreaCode()}, 'SettlePhoneCountryCode'={self.getSettlePhoneCountryCode()}, 'SettlePhoneAreaCode'={self.getSettlePhoneAreaCode()}, 'CompanyManIdentifiedCardType'={self.getCompanyManIdentifiedCardType()}, 'CompanyManIdentifiedCardNo'={self.getCompanyManIdentifiedCardNo()}, 'CompanyManPersonName'={self.getCompanyManPersonName()}, 'CompanyManTelephone'={self.getCompanyManTelephone()}, 'CompanyManAddress'={self.getCompanyManAddress()}, 'CompanyManZipCode'={self.getCompanyManZipCode()}, 'CorporationManIdentifiedCardType'={self.getCorporationManIdentifiedCardType()}, 'CorporationManIdentifiedCardNo'={self.getCorporationManIdentifiedCardNo()}, 'CorporationManPersonName'={self.getCorporationManPersonName()}, 'CorporationManTelephone'={self.getCorporationManTelephone()}, 'CorporationManAddress'={self.getCorporationManAddress()}, 'CorporationManZipCode'={self.getCorporationManZipCode()}, 'LinkManIdentifiedCardType'={self.getLinkManIdentifiedCardType()}, 'LinkManIdentifiedCardNo'={self.getLinkManIdentifiedCardNo()}, 'LinkManPersonName'={self.getLinkManPersonName()}, 'LinkManTelephone'={self.getLinkManTelephone()}, 'LinkManAddress'={self.getLinkManAddress()}, 'LinkManZipCode'={self.getLinkManZipCode()}, 'LedgerIdentifiedCardType'={self.getLedgerIdentifiedCardType()}, 'LedgerIdentifiedCardNo'={self.getLedgerIdentifiedCardNo()}, 'LedgerPersonName'={self.getLedgerPersonName()}, 'LedgerTelephone'={self.getLedgerTelephone()}, 'LedgerAddress'={self.getLedgerAddress()}, 'LedgerZipCode'={self.getLedgerZipCode()}, 'TrusteeIdentifiedCardType'={self.getTrusteeIdentifiedCardType()}, 'TrusteeIdentifiedCardNo'={self.getTrusteeIdentifiedCardNo()}, 'TrusteePersonName'={self.getTrusteePersonName()}, 'TrusteeTelephone'={self.getTrusteeTelephone()}, 'TrusteeAddress'={self.getTrusteeAddress()}, 'TrusteeZipCode'={self.getTrusteeZipCode()}, 'TrusteeCorporationManIdentifiedCardType'={self.getTrusteeCorporationManIdentifiedCardType()}, 'TrusteeCorporationManIdentifiedCardNo'={self.getTrusteeCorporationManIdentifiedCardNo()}, 'TrusteeCorporationManPersonName'={self.getTrusteeCorporationManPersonName()}, 'TrusteeCorporationManTelephone'={self.getTrusteeCorporationManTelephone()}, 'TrusteeCorporationManAddress'={self.getTrusteeCorporationManAddress()}, 'TrusteeCorporationManZipCode'={self.getTrusteeCorporationManZipCode()}, 'TrusteeOpenManIdentifiedCardType'={self.getTrusteeOpenManIdentifiedCardType()}, 'TrusteeOpenManIdentifiedCardNo'={self.getTrusteeOpenManIdentifiedCardNo()}, 'TrusteeOpenManPersonName'={self.getTrusteeOpenManPersonName()}, 'TrusteeOpenManTelephone'={self.getTrusteeOpenManTelephone()}, 'TrusteeOpenManAddress'={self.getTrusteeOpenManAddress()}, 'TrusteeOpenManZipCode'={self.getTrusteeOpenManZipCode()}, 'TrusteeContactManIdentifiedCardType'={self.getTrusteeContactManIdentifiedCardType()}, 'TrusteeContactManIdentifiedCardNo'={self.getTrusteeContactManIdentifiedCardNo()}, 'TrusteeContactManPersonName'={self.getTrusteeContactManPersonName()}, 'TrusteeContactManTelephone'={self.getTrusteeContactManTelephone()}, 'TrusteeContactManAddress'={self.getTrusteeContactManAddress()}, 'TrusteeContactManZipCode'={self.getTrusteeContactManZipCode()}"

    @property
    def __dict__(self):
        return {'InvestorID': self.getInvestorID(), 'BrokerID': self.getBrokerID(), 'InvestorGroupID': self.getInvestorGroupID(), 'InvestorName': self.getInvestorName(), 'IdentifiedCardType': self.getIdentifiedCardType(), 'IdentifiedCardNo': self.getIdentifiedCardNo(), 'IsActive': self.getIsActive(), 'Telephone': self.getTelephone(), 'Address': self.getAddress(), 'OrderManIdentifiedCardType': self.getOrderManIdentifiedCardType(), 'OrderManIdentifiedCardNo': self.getOrderManIdentifiedCardNo(), 'OrderManPersonName': self.getOrderManPersonName(), 'OrderManTelephone': self.getOrderManTelephone(), 'OrderManAddress': self.getOrderManAddress(), 'OrderManZipCode': self.getOrderManZipCode(), 'FundManIdentifiedCardType': self.getFundManIdentifiedCardType(), 'FundManIdentifiedCardNo': self.getFundManIdentifiedCardNo(), 'FundManPersonName': self.getFundManPersonName(), 'FundManTelephone': self.getFundManTelephone(), 'FundManAddress': self.getFundManAddress(), 'FundManZipCode': self.getFundManZipCode(), 'OpenManIdentifiedCardType': self.getOpenManIdentifiedCardType(), 'OpenManIdentifiedCardNo': self.getOpenManIdentifiedCardNo(), 'OpenManPersonName': self.getOpenManPersonName(), 'OpenManTelephone': self.getOpenManTelephone(), 'OpenManAddress': self.getOpenManAddress(), 'OpenManZipCode': self.getOpenManZipCode(), 'SettlementManIdentifiedCardType': self.getSettlementManIdentifiedCardType(), 'SettlementManIdentifiedCardNo': self.getSettlementManIdentifiedCardNo(), 'SettlementManPersonName': self.getSettlementManPersonName(), 'SettlementManTelephone': self.getSettlementManTelephone(), 'SettlementManAddress': self.getSettlementManAddress(), 'SettlementManZipCode': self.getSettlementManZipCode(), 'OpenDate': self.getOpenDate(), 'Mobile': self.getMobile(), 'EMail': self.getEMail(), 'InvestorType': self.getInvestorType(), 'PhoneCountryCode': self.getPhoneCountryCode(), 'PhoneAreaCode': self.getPhoneAreaCode(), 'OpenPhoneCountryCode': self.getOpenPhoneCountryCode(), 'OpenPhoneAreaCode': self.getOpenPhoneAreaCode(), 'OrderPhoneCountryCode': self.getOrderPhoneCountryCode(), 'OrderPhoneAreaCode': self.getOrderPhoneAreaCode(), 'FundPhoneCountryCode': self.getFundPhoneCountryCode(), 'FundPhoneAreaCode': self.getFundPhoneAreaCode(), 'SettlePhoneCountryCode': self.getSettlePhoneCountryCode(), 'SettlePhoneAreaCode': self.getSettlePhoneAreaCode(), 'CompanyManIdentifiedCardType': self.getCompanyManIdentifiedCardType(), 'CompanyManIdentifiedCardNo': self.getCompanyManIdentifiedCardNo(), 'CompanyManPersonName': self.getCompanyManPersonName(), 'CompanyManTelephone': self.getCompanyManTelephone(), 'CompanyManAddress': self.getCompanyManAddress(), 'CompanyManZipCode': self.getCompanyManZipCode(), 'CorporationManIdentifiedCardType': self.getCorporationManIdentifiedCardType(), 'CorporationManIdentifiedCardNo': self.getCorporationManIdentifiedCardNo(), 'CorporationManPersonName': self.getCorporationManPersonName(), 'CorporationManTelephone': self.getCorporationManTelephone(), 'CorporationManAddress': self.getCorporationManAddress(), 'CorporationManZipCode': self.getCorporationManZipCode(), 'LinkManIdentifiedCardType': self.getLinkManIdentifiedCardType(), 'LinkManIdentifiedCardNo': self.getLinkManIdentifiedCardNo(), 'LinkManPersonName': self.getLinkManPersonName(), 'LinkManTelephone': self.getLinkManTelephone(), 'LinkManAddress': self.getLinkManAddress(), 'LinkManZipCode': self.getLinkManZipCode(), 'LedgerIdentifiedCardType': self.getLedgerIdentifiedCardType(), 'LedgerIdentifiedCardNo': self.getLedgerIdentifiedCardNo(), 'LedgerPersonName': self.getLedgerPersonName(), 'LedgerTelephone': self.getLedgerTelephone(), 'LedgerAddress': self.getLedgerAddress(), 'LedgerZipCode': self.getLedgerZipCode(), 'TrusteeIdentifiedCardType': self.getTrusteeIdentifiedCardType(), 'TrusteeIdentifiedCardNo': self.getTrusteeIdentifiedCardNo(), 'TrusteePersonName': self.getTrusteePersonName(), 'TrusteeTelephone': self.getTrusteeTelephone(), 'TrusteeAddress': self.getTrusteeAddress(), 'TrusteeZipCode': self.getTrusteeZipCode(), 'TrusteeCorporationManIdentifiedCardType': self.getTrusteeCorporationManIdentifiedCardType(), 'TrusteeCorporationManIdentifiedCardNo': self.getTrusteeCorporationManIdentifiedCardNo(), 'TrusteeCorporationManPersonName': self.getTrusteeCorporationManPersonName(), 'TrusteeCorporationManTelephone': self.getTrusteeCorporationManTelephone(), 'TrusteeCorporationManAddress': self.getTrusteeCorporationManAddress(), 'TrusteeCorporationManZipCode': self.getTrusteeCorporationManZipCode(), 'TrusteeOpenManIdentifiedCardType': self.getTrusteeOpenManIdentifiedCardType(), 'TrusteeOpenManIdentifiedCardNo': self.getTrusteeOpenManIdentifiedCardNo(), 'TrusteeOpenManPersonName': self.getTrusteeOpenManPersonName(), 'TrusteeOpenManTelephone': self.getTrusteeOpenManTelephone(), 'TrusteeOpenManAddress': self.getTrusteeOpenManAddress(), 'TrusteeOpenManZipCode': self.getTrusteeOpenManZipCode(), 'TrusteeContactManIdentifiedCardType': self.getTrusteeContactManIdentifiedCardType(), 'TrusteeContactManIdentifiedCardNo': self.getTrusteeContactManIdentifiedCardNo(), 'TrusteeContactManPersonName': self.getTrusteeContactManPersonName(), 'TrusteeContactManTelephone': self.getTrusteeContactManTelephone(), 'TrusteeContactManAddress': self.getTrusteeContactManAddress(), 'TrusteeContactManZipCode': self.getTrusteeContactManZipCode()}


class  CShfeFtdcSubInvestorTradeField(Structure):
    """订阅投资者成交"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcSubInvestorPositionField(Structure):
    """订阅投资者持仓"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcNotifySequenceField(Structure):
    """序列号"""
    _fields_ = [
        ("SequenceNo", c_int32),
    ]

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    @property
    def __str__(self):
        return f"'SequenceNo'={self.getSequenceNo()}"

    @property
    def __dict__(self):
        return {'SequenceNo': self.getSequenceNo()}


class  CShfeFtdcSequencialTradeField(Structure):
    """有序的成交"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("ExchangeID", c_char*9),
        ("TradeID", c_char*21),
        ("Direction", c_char),
        ("OrderSysID", c_char*21),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("TradingRole", c_char),
        ("ExchangeInstID", c_char*31),
        ("OffsetFlag", c_char),
        ("HedgeFlag", c_char),
        ("Price", c_double),
        ("Volume", c_int32),
        ("TradeDate", c_char*9),
        ("TradeTime", c_char*9),
        ("TradeType", c_char),
        ("PriceSource", c_char),
        ("TraderID", c_char*21),
        ("OrderLocalID", c_char*13),
        ("ClearingPartID", c_char*11),
        ("BusinessUnit", c_char*21),
        ("SequenceNo", c_int32),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("BrokerOrderSeq", c_int32),
        ("TradeSource", c_char),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getTradeID(self):
        '''成交编号'''
        return str(self.TradeID, 'GBK')

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getTradingRole(self):
        '''交易角色'''
        return TShfeFtdcTradingRoleType(ord(self.TradingRole))

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getOffsetFlag(self):
        '''开平标志'''
        return TShfeFtdcOffsetFlagType(ord(self.OffsetFlag))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPrice(self):
        '''价格'''
        return self.Price

    def getVolume(self):
        '''数量'''
        return self.Volume

    def getTradeDate(self):
        '''成交时期'''
        return str(self.TradeDate, 'GBK')

    def getTradeTime(self):
        '''成交时间'''
        return str(self.TradeTime, 'GBK')

    def getTradeType(self):
        '''成交类型'''
        return TShfeFtdcTradeTypeType(ord(self.TradeType))

    def getPriceSource(self):
        '''成交价来源'''
        return TShfeFtdcPriceSourceType(ord(self.PriceSource))

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getClearingPartID(self):
        '''结算会员编号'''
        return str(self.ClearingPartID, 'GBK')

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getBrokerOrderSeq(self):
        '''经纪公司报单编号'''
        return self.BrokerOrderSeq

    def getTradeSource(self):
        '''成交来源'''
        return TShfeFtdcTradeSourceType(ord(self.TradeSource))

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'ExchangeID'={self.getExchangeID()}, 'TradeID'={self.getTradeID()}, 'Direction'={self.getDirection()}, 'OrderSysID'={self.getOrderSysID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'TradingRole'={self.getTradingRole()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'OffsetFlag'={self.getOffsetFlag()}, 'HedgeFlag'={self.getHedgeFlag()}, 'Price'={self.getPrice()}, 'Volume'={self.getVolume()}, 'TradeDate'={self.getTradeDate()}, 'TradeTime'={self.getTradeTime()}, 'TradeType'={self.getTradeType()}, 'PriceSource'={self.getPriceSource()}, 'TraderID'={self.getTraderID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ClearingPartID'={self.getClearingPartID()}, 'BusinessUnit'={self.getBusinessUnit()}, 'SequenceNo'={self.getSequenceNo()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'BrokerOrderSeq'={self.getBrokerOrderSeq()}, 'TradeSource'={self.getTradeSource()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'ExchangeID': self.getExchangeID(), 'TradeID': self.getTradeID(), 'Direction': self.getDirection(), 'OrderSysID': self.getOrderSysID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'TradingRole': self.getTradingRole(), 'ExchangeInstID': self.getExchangeInstID(), 'OffsetFlag': self.getOffsetFlag(), 'HedgeFlag': self.getHedgeFlag(), 'Price': self.getPrice(), 'Volume': self.getVolume(), 'TradeDate': self.getTradeDate(), 'TradeTime': self.getTradeTime(), 'TradeType': self.getTradeType(), 'PriceSource': self.getPriceSource(), 'TraderID': self.getTraderID(), 'OrderLocalID': self.getOrderLocalID(), 'ClearingPartID': self.getClearingPartID(), 'BusinessUnit': self.getBusinessUnit(), 'SequenceNo': self.getSequenceNo(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'BrokerOrderSeq': self.getBrokerOrderSeq(), 'TradeSource': self.getTradeSource()}


class  CShfeFtdcSequencialOrderField(Structure):
    """有序的报单"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("OrderLocalID", c_char*13),
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("ExchangeInstID", c_char*31),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderSubmitStatus", c_char),
        ("NotifySequence", c_int32),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("OrderSysID", c_char*21),
        ("OrderSource", c_char),
        ("OrderStatus", c_char),
        ("OrderType", c_char),
        ("VolumeTraded", c_int32),
        ("VolumeTotal", c_int32),
        ("InsertDate", c_char*9),
        ("InsertTime", c_char*9),
        ("ActiveTime", c_char*9),
        ("SuspendTime", c_char*9),
        ("UpdateTime", c_char*9),
        ("CancelTime", c_char*9),
        ("ActiveTraderID", c_char*21),
        ("ClearingPartID", c_char*11),
        ("SequenceNo", c_int32),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("UserProductInfo", c_char*11),
        ("StatusMsg", c_char*81),
        ("UserForceClose", c_int32),
        ("ActiveUserID", c_char*16),
        ("BrokerOrderSeq", c_int32),
        ("RelativeOrderSysID", c_char*21),
        ("ZCETotalTradedVolume", c_int32),
        ("IsSwapOrder", c_int32),
        ("BranchID", c_char*9),
        ("InvestUnitID", c_char*17),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getOrderLocalID(self):
        '''本地报单编号'''
        return str(self.OrderLocalID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderSubmitStatus(self):
        '''报单提交状态'''
        return TShfeFtdcOrderSubmitStatusType(ord(self.OrderSubmitStatus))

    def getNotifySequence(self):
        '''报单提示序号'''
        return self.NotifySequence

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getOrderSysID(self):
        '''报单编号'''
        return str(self.OrderSysID, 'GBK')

    def getOrderSource(self):
        '''报单来源'''
        return TShfeFtdcOrderSourceType(ord(self.OrderSource))

    def getOrderStatus(self):
        '''报单状态'''
        return TShfeFtdcOrderStatusType(ord(self.OrderStatus))

    def getOrderType(self):
        '''报单类型'''
        return TShfeFtdcOrderTypeType(ord(self.OrderType))

    def getVolumeTraded(self):
        '''今成交数量'''
        return self.VolumeTraded

    def getVolumeTotal(self):
        '''剩余数量'''
        return self.VolumeTotal

    def getInsertDate(self):
        '''报单日期'''
        return str(self.InsertDate, 'GBK')

    def getInsertTime(self):
        '''委托时间'''
        return str(self.InsertTime, 'GBK')

    def getActiveTime(self):
        '''激活时间'''
        return str(self.ActiveTime, 'GBK')

    def getSuspendTime(self):
        '''挂起时间'''
        return str(self.SuspendTime, 'GBK')

    def getUpdateTime(self):
        '''最后修改时间'''
        return str(self.UpdateTime, 'GBK')

    def getCancelTime(self):
        '''撤销时间'''
        return str(self.CancelTime, 'GBK')

    def getActiveTraderID(self):
        '''最后修改交易所交易员代码'''
        return str(self.ActiveTraderID, 'GBK')

    def getClearingPartID(self):
        '''结算会员编号'''
        return str(self.ClearingPartID, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getUserProductInfo(self):
        '''用户端产品信息'''
        return str(self.UserProductInfo, 'GBK')

    def getStatusMsg(self):
        '''状态信息'''
        return str(self.StatusMsg, 'GBK')

    def getUserForceClose(self):
        '''用户强评标志'''
        return self.UserForceClose

    def getActiveUserID(self):
        '''操作用户代码'''
        return str(self.ActiveUserID, 'GBK')

    def getBrokerOrderSeq(self):
        '''经纪公司报单编号'''
        return self.BrokerOrderSeq

    def getRelativeOrderSysID(self):
        '''相关报单'''
        return str(self.RelativeOrderSysID, 'GBK')

    def getZCETotalTradedVolume(self):
        '''郑商所成交数量'''
        return self.ZCETotalTradedVolume

    def getIsSwapOrder(self):
        '''互换单标志'''
        return self.IsSwapOrder

    def getBranchID(self):
        '''营业部编号'''
        return str(self.BranchID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'OrderLocalID'={self.getOrderLocalID()}, 'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderSubmitStatus'={self.getOrderSubmitStatus()}, 'NotifySequence'={self.getNotifySequence()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'OrderSysID'={self.getOrderSysID()}, 'OrderSource'={self.getOrderSource()}, 'OrderStatus'={self.getOrderStatus()}, 'OrderType'={self.getOrderType()}, 'VolumeTraded'={self.getVolumeTraded()}, 'VolumeTotal'={self.getVolumeTotal()}, 'InsertDate'={self.getInsertDate()}, 'InsertTime'={self.getInsertTime()}, 'ActiveTime'={self.getActiveTime()}, 'SuspendTime'={self.getSuspendTime()}, 'UpdateTime'={self.getUpdateTime()}, 'CancelTime'={self.getCancelTime()}, 'ActiveTraderID'={self.getActiveTraderID()}, 'ClearingPartID'={self.getClearingPartID()}, 'SequenceNo'={self.getSequenceNo()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'UserProductInfo'={self.getUserProductInfo()}, 'StatusMsg'={self.getStatusMsg()}, 'UserForceClose'={self.getUserForceClose()}, 'ActiveUserID'={self.getActiveUserID()}, 'BrokerOrderSeq'={self.getBrokerOrderSeq()}, 'RelativeOrderSysID'={self.getRelativeOrderSysID()}, 'ZCETotalTradedVolume'={self.getZCETotalTradedVolume()}, 'IsSwapOrder'={self.getIsSwapOrder()}, 'BranchID'={self.getBranchID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'OrderLocalID': self.getOrderLocalID(), 'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'ExchangeInstID': self.getExchangeInstID(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderSubmitStatus': self.getOrderSubmitStatus(), 'NotifySequence': self.getNotifySequence(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'OrderSysID': self.getOrderSysID(), 'OrderSource': self.getOrderSource(), 'OrderStatus': self.getOrderStatus(), 'OrderType': self.getOrderType(), 'VolumeTraded': self.getVolumeTraded(), 'VolumeTotal': self.getVolumeTotal(), 'InsertDate': self.getInsertDate(), 'InsertTime': self.getInsertTime(), 'ActiveTime': self.getActiveTime(), 'SuspendTime': self.getSuspendTime(), 'UpdateTime': self.getUpdateTime(), 'CancelTime': self.getCancelTime(), 'ActiveTraderID': self.getActiveTraderID(), 'ClearingPartID': self.getClearingPartID(), 'SequenceNo': self.getSequenceNo(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'UserProductInfo': self.getUserProductInfo(), 'StatusMsg': self.getStatusMsg(), 'UserForceClose': self.getUserForceClose(), 'ActiveUserID': self.getActiveUserID(), 'BrokerOrderSeq': self.getBrokerOrderSeq(), 'RelativeOrderSysID': self.getRelativeOrderSysID(), 'ZCETotalTradedVolume': self.getZCETotalTradedVolume(), 'IsSwapOrder': self.getIsSwapOrder(), 'BranchID': self.getBranchID(), 'InvestUnitID': self.getInvestUnitID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcSequencialBrokerUserEventField(Structure):
    """有序的经纪公司用户事件"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("UserEventType", c_char),
        ("EventSequenceNo", c_int32),
        ("EventDate", c_char*9),
        ("EventTime", c_char*9),
        ("UserEventInfo", c_char*1025),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getUserEventType(self):
        '''用户事件类型'''
        return TShfeFtdcUserEventTypeType(ord(self.UserEventType))

    def getEventSequenceNo(self):
        '''用户事件序号'''
        return self.EventSequenceNo

    def getEventDate(self):
        '''事件发生日期'''
        return str(self.EventDate, 'GBK')

    def getEventTime(self):
        '''事件发生时间'''
        return str(self.EventTime, 'GBK')

    def getUserEventInfo(self):
        '''用户事件信息'''
        return str(self.UserEventInfo, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'UserEventType'={self.getUserEventType()}, 'EventSequenceNo'={self.getEventSequenceNo()}, 'EventDate'={self.getEventDate()}, 'EventTime'={self.getEventTime()}, 'UserEventInfo'={self.getUserEventInfo()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'UserEventType': self.getUserEventType(), 'EventSequenceNo': self.getEventSequenceNo(), 'EventDate': self.getEventDate(), 'EventTime': self.getEventTime(), 'UserEventInfo': self.getUserEventInfo(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcSequencialPositionField(Structure):
    """有序的持仓"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("PosiDirection", c_char),
        ("HedgeFlag", c_char),
        ("PositionDate", c_char),
        ("YdPosition", c_int32),
        ("Position", c_int32),
        ("LongFrozen", c_int32),
        ("ShortFrozen", c_int32),
        ("LongFrozenAmount", c_double),
        ("ShortFrozenAmount", c_double),
        ("OpenVolume", c_int32),
        ("CloseVolume", c_int32),
        ("OpenAmount", c_double),
        ("CloseAmount", c_double),
        ("PositionCost", c_double),
        ("PreMargin", c_double),
        ("UseMargin", c_double),
        ("FrozenMargin", c_double),
        ("FrozenCash", c_double),
        ("FrozenCommission", c_double),
        ("CashIn", c_double),
        ("Commission", c_double),
        ("CloseProfit", c_double),
        ("PositionProfit", c_double),
        ("PreSettlementPrice", c_double),
        ("SettlementPrice", c_double),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("OpenCost", c_double),
        ("ExchangeMargin", c_double),
        ("CombPosition", c_int32),
        ("CombLongFrozen", c_int32),
        ("CombShortFrozen", c_int32),
        ("CloseProfitByDate", c_double),
        ("CloseProfitByTrade", c_double),
        ("TodayPosition", c_int32),
        ("MarginRateByMoney", c_double),
        ("MarginRateByVolume", c_double),
        ("StrikeFrozen", c_int32),
        ("StrikeFrozenAmount", c_double),
        ("AbandonFrozen", c_int32),
        ("OptionValue", c_double),
        ("MaintUseMargin", c_double),
        ("MaintExchangeMargin", c_double),
        ("IndexSettlementPrice", c_double),
        ("FixedMargin", c_double),
        ("ExchangeID", c_char*9),
        ("YdStrikeFrozen", c_int32),
        ("InvestUnitID", c_char*17),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPosiDirection(self):
        '''持仓多空方向'''
        return TShfeFtdcPosiDirectionType(ord(self.PosiDirection))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPositionDate(self):
        '''持仓日期'''
        return TShfeFtdcPositionDateType(ord(self.PositionDate))

    def getYdPosition(self):
        '''上日持仓'''
        return self.YdPosition

    def getPosition(self):
        '''今日持仓'''
        return self.Position

    def getLongFrozen(self):
        '''多头冻结'''
        return self.LongFrozen

    def getShortFrozen(self):
        '''空头冻结'''
        return self.ShortFrozen

    def getLongFrozenAmount(self):
        '''开仓冻结金额'''
        return self.LongFrozenAmount

    def getShortFrozenAmount(self):
        '''开仓冻结金额'''
        return self.ShortFrozenAmount

    def getOpenVolume(self):
        '''开仓量'''
        return self.OpenVolume

    def getCloseVolume(self):
        '''平仓量'''
        return self.CloseVolume

    def getOpenAmount(self):
        '''开仓金额'''
        return self.OpenAmount

    def getCloseAmount(self):
        '''平仓金额'''
        return self.CloseAmount

    def getPositionCost(self):
        '''持仓成本'''
        return self.PositionCost

    def getPreMargin(self):
        '''上次占用的保证金'''
        return self.PreMargin

    def getUseMargin(self):
        '''占用的保证金'''
        return self.UseMargin

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getPreSettlementPrice(self):
        '''上次结算价'''
        return self.PreSettlementPrice

    def getSettlementPrice(self):
        '''本次结算价'''
        return self.SettlementPrice

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getOpenCost(self):
        '''开仓成本'''
        return self.OpenCost

    def getExchangeMargin(self):
        '''交易所保证金'''
        return self.ExchangeMargin

    def getCombPosition(self):
        '''组合成交形成的持仓'''
        return self.CombPosition

    def getCombLongFrozen(self):
        '''组合多头冻结'''
        return self.CombLongFrozen

    def getCombShortFrozen(self):
        '''组合空头冻结'''
        return self.CombShortFrozen

    def getCloseProfitByDate(self):
        '''逐日盯市平仓盈亏'''
        return self.CloseProfitByDate

    def getCloseProfitByTrade(self):
        '''逐笔对冲平仓盈亏'''
        return self.CloseProfitByTrade

    def getTodayPosition(self):
        '''今日持仓'''
        return self.TodayPosition

    def getMarginRateByMoney(self):
        '''保证金率'''
        return self.MarginRateByMoney

    def getMarginRateByVolume(self):
        '''保证金率(按手数)'''
        return self.MarginRateByVolume

    def getStrikeFrozen(self):
        '''执行冻结'''
        return self.StrikeFrozen

    def getStrikeFrozenAmount(self):
        '''执行冻结金额'''
        return self.StrikeFrozenAmount

    def getAbandonFrozen(self):
        '''放弃执行冻结'''
        return self.AbandonFrozen

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    def getMaintUseMargin(self):
        '''占用的维持保证金'''
        return self.MaintUseMargin

    def getMaintExchangeMargin(self):
        '''交易所维持保证金'''
        return self.MaintExchangeMargin

    def getIndexSettlementPrice(self):
        '''期权标的合约的本次结算价'''
        return self.IndexSettlementPrice

    def getFixedMargin(self):
        '''昨结算价计算的期权保证金'''
        return self.FixedMargin

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getYdStrikeFrozen(self):
        '''执行冻结的昨仓'''
        return self.YdStrikeFrozen

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'PosiDirection'={self.getPosiDirection()}, 'HedgeFlag'={self.getHedgeFlag()}, 'PositionDate'={self.getPositionDate()}, 'YdPosition'={self.getYdPosition()}, 'Position'={self.getPosition()}, 'LongFrozen'={self.getLongFrozen()}, 'ShortFrozen'={self.getShortFrozen()}, 'LongFrozenAmount'={self.getLongFrozenAmount()}, 'ShortFrozenAmount'={self.getShortFrozenAmount()}, 'OpenVolume'={self.getOpenVolume()}, 'CloseVolume'={self.getCloseVolume()}, 'OpenAmount'={self.getOpenAmount()}, 'CloseAmount'={self.getCloseAmount()}, 'PositionCost'={self.getPositionCost()}, 'PreMargin'={self.getPreMargin()}, 'UseMargin'={self.getUseMargin()}, 'FrozenMargin'={self.getFrozenMargin()}, 'FrozenCash'={self.getFrozenCash()}, 'FrozenCommission'={self.getFrozenCommission()}, 'CashIn'={self.getCashIn()}, 'Commission'={self.getCommission()}, 'CloseProfit'={self.getCloseProfit()}, 'PositionProfit'={self.getPositionProfit()}, 'PreSettlementPrice'={self.getPreSettlementPrice()}, 'SettlementPrice'={self.getSettlementPrice()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'OpenCost'={self.getOpenCost()}, 'ExchangeMargin'={self.getExchangeMargin()}, 'CombPosition'={self.getCombPosition()}, 'CombLongFrozen'={self.getCombLongFrozen()}, 'CombShortFrozen'={self.getCombShortFrozen()}, 'CloseProfitByDate'={self.getCloseProfitByDate()}, 'CloseProfitByTrade'={self.getCloseProfitByTrade()}, 'TodayPosition'={self.getTodayPosition()}, 'MarginRateByMoney'={self.getMarginRateByMoney()}, 'MarginRateByVolume'={self.getMarginRateByVolume()}, 'StrikeFrozen'={self.getStrikeFrozen()}, 'StrikeFrozenAmount'={self.getStrikeFrozenAmount()}, 'AbandonFrozen'={self.getAbandonFrozen()}, 'OptionValue'={self.getOptionValue()}, 'MaintUseMargin'={self.getMaintUseMargin()}, 'MaintExchangeMargin'={self.getMaintExchangeMargin()}, 'IndexSettlementPrice'={self.getIndexSettlementPrice()}, 'FixedMargin'={self.getFixedMargin()}, 'ExchangeID'={self.getExchangeID()}, 'YdStrikeFrozen'={self.getYdStrikeFrozen()}, 'InvestUnitID'={self.getInvestUnitID()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'PosiDirection': self.getPosiDirection(), 'HedgeFlag': self.getHedgeFlag(), 'PositionDate': self.getPositionDate(), 'YdPosition': self.getYdPosition(), 'Position': self.getPosition(), 'LongFrozen': self.getLongFrozen(), 'ShortFrozen': self.getShortFrozen(), 'LongFrozenAmount': self.getLongFrozenAmount(), 'ShortFrozenAmount': self.getShortFrozenAmount(), 'OpenVolume': self.getOpenVolume(), 'CloseVolume': self.getCloseVolume(), 'OpenAmount': self.getOpenAmount(), 'CloseAmount': self.getCloseAmount(), 'PositionCost': self.getPositionCost(), 'PreMargin': self.getPreMargin(), 'UseMargin': self.getUseMargin(), 'FrozenMargin': self.getFrozenMargin(), 'FrozenCash': self.getFrozenCash(), 'FrozenCommission': self.getFrozenCommission(), 'CashIn': self.getCashIn(), 'Commission': self.getCommission(), 'CloseProfit': self.getCloseProfit(), 'PositionProfit': self.getPositionProfit(), 'PreSettlementPrice': self.getPreSettlementPrice(), 'SettlementPrice': self.getSettlementPrice(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'OpenCost': self.getOpenCost(), 'ExchangeMargin': self.getExchangeMargin(), 'CombPosition': self.getCombPosition(), 'CombLongFrozen': self.getCombLongFrozen(), 'CombShortFrozen': self.getCombShortFrozen(), 'CloseProfitByDate': self.getCloseProfitByDate(), 'CloseProfitByTrade': self.getCloseProfitByTrade(), 'TodayPosition': self.getTodayPosition(), 'MarginRateByMoney': self.getMarginRateByMoney(), 'MarginRateByVolume': self.getMarginRateByVolume(), 'StrikeFrozen': self.getStrikeFrozen(), 'StrikeFrozenAmount': self.getStrikeFrozenAmount(), 'AbandonFrozen': self.getAbandonFrozen(), 'OptionValue': self.getOptionValue(), 'MaintUseMargin': self.getMaintUseMargin(), 'MaintExchangeMargin': self.getMaintExchangeMargin(), 'IndexSettlementPrice': self.getIndexSettlementPrice(), 'FixedMargin': self.getFixedMargin(), 'ExchangeID': self.getExchangeID(), 'YdStrikeFrozen': self.getYdStrikeFrozen(), 'InvestUnitID': self.getInvestUnitID()}


class  CShfeFtdcQryRiskNotifyPatternField(Structure):
    """查询客户风险通知模版"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("Reserve", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getReserve(self):
        '''保留字段'''
        return str(self.Reserve, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'Reserve'={self.getReserve()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'Reserve': self.getReserve()}


class  CShfeFtdcRiskNotifyPatternField(Structure):
    """客户风险通知模版"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("NotifyClass", c_char),
        ("IsActive", c_int32),
        ("IsAutoSystem", c_int32),
        ("IsAutoSMS", c_int32),
        ("IsAutoEmail", c_int32),
        ("SystemPattern", c_char*257),
        ("SMSPattern", c_char*257),
        ("EmailPattern", c_char*257),
        ("Reserve", c_char*101),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码，请求修改模版时有效'''
        return str(self.UserID, 'GBK')

    def getNotifyClass(self):
        '''通知类型'''
        return TShfeFtdcNotifyClassType(ord(self.NotifyClass))

    def getIsActive(self):
        '''是否启用'''
        return self.IsActive

    def getIsAutoSystem(self):
        '''是否自动系统通知'''
        return self.IsAutoSystem

    def getIsAutoSMS(self):
        '''是否自动短信通知'''
        return self.IsAutoSMS

    def getIsAutoEmail(self):
        '''是否自动邮件通知'''
        return self.IsAutoEmail

    def getSystemPattern(self):
        '''系统通知模版内容'''
        return str(self.SystemPattern, 'GBK')

    def getSMSPattern(self):
        '''短信通知模版内容'''
        return str(self.SMSPattern, 'GBK')

    def getEmailPattern(self):
        '''邮件通知模版内容'''
        return str(self.EmailPattern, 'GBK')

    def getReserve(self):
        '''预留参数(暂时只用作warnlevel)'''
        return str(self.Reserve, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'NotifyClass'={self.getNotifyClass()}, 'IsActive'={self.getIsActive()}, 'IsAutoSystem'={self.getIsAutoSystem()}, 'IsAutoSMS'={self.getIsAutoSMS()}, 'IsAutoEmail'={self.getIsAutoEmail()}, 'SystemPattern'={self.getSystemPattern()}, 'SMSPattern'={self.getSMSPattern()}, 'EmailPattern'={self.getEmailPattern()}, 'Reserve'={self.getReserve()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'NotifyClass': self.getNotifyClass(), 'IsActive': self.getIsActive(), 'IsAutoSystem': self.getIsAutoSystem(), 'IsAutoSMS': self.getIsAutoSMS(), 'IsAutoEmail': self.getIsAutoEmail(), 'SystemPattern': self.getSystemPattern(), 'SMSPattern': self.getSMSPattern(), 'EmailPattern': self.getEmailPattern(), 'Reserve': self.getReserve()}


class  CShfeFtdcQryRiskNotifyTokenField(Structure):
    """查询客户风险通知模版中自动替换字段"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID()}


class  CShfeFtdcRiskNotifyTokenField(Structure):
    """客户风险通知模版中自动替换字段"""
    _fields_ = [
        ("Token", c_char*61),
        ("Description", c_char*81),
    ]

    def getToken(self):
        '''自动替换字段'''
        return str(self.Token, 'GBK')

    def getDescription(self):
        '''自动替换字段的描述'''
        return str(self.Description, 'GBK')

    @property
    def __str__(self):
        return f"'Token'={self.getToken()}, 'Description'={self.getDescription()}"

    @property
    def __dict__(self):
        return {'Token': self.getToken(), 'Description': self.getDescription()}


class  CShfeFtdcRiskNotifyCommandField(Structure):
    """请求发送客户风险通知的命令"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("NotifyClass", c_char),
        ("InvestorID", c_char*13),
        ("IsAutoSystem", c_int32),
        ("IsAutoSMS", c_int32),
        ("IsAutoEmail", c_int32),
        ("Reserve", c_char*31),
        ("Pattern", c_char*257),
        ("IsNormal", c_int32),
        ("IsWarn", c_int32),
        ("CurrencyID", c_char*4),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getNotifyClass(self):
        '''通知类型'''
        return TShfeFtdcNotifyClassType(ord(self.NotifyClass))

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getIsAutoSystem(self):
        '''是否发送系统通知'''
        return self.IsAutoSystem

    def getIsAutoSMS(self):
        '''是否发送短信通知'''
        return self.IsAutoSMS

    def getIsAutoEmail(self):
        '''是否发送邮件通知'''
        return self.IsAutoEmail

    def getReserve(self):
        '''保留字段'''
        return str(self.Reserve, 'GBK')

    def getPattern(self):
        '''通知模版内容'''
        return str(self.Pattern, 'GBK')

    def getIsNormal(self):
        '''是否允许发送正常通知'''
        return self.IsNormal

    def getIsWarn(self):
        '''是否允许发送警示通知'''
        return self.IsWarn

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'NotifyClass'={self.getNotifyClass()}, 'InvestorID'={self.getInvestorID()}, 'IsAutoSystem'={self.getIsAutoSystem()}, 'IsAutoSMS'={self.getIsAutoSMS()}, 'IsAutoEmail'={self.getIsAutoEmail()}, 'Reserve'={self.getReserve()}, 'Pattern'={self.getPattern()}, 'IsNormal'={self.getIsNormal()}, 'IsWarn'={self.getIsWarn()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'NotifyClass': self.getNotifyClass(), 'InvestorID': self.getInvestorID(), 'IsAutoSystem': self.getIsAutoSystem(), 'IsAutoSMS': self.getIsAutoSMS(), 'IsAutoEmail': self.getIsAutoEmail(), 'Reserve': self.getReserve(), 'Pattern': self.getPattern(), 'IsNormal': self.getIsNormal(), 'IsWarn': self.getIsWarn(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcForceCloseStandardField(Structure):
    """强平标准"""
    _fields_ = [
        ("ForceCloseLevel", c_char),
        ("ForceCloseRelease", c_char),
        ("FCNonLimitFirst", c_int32),
        ("FCPosiProfitLossFirst", c_int32),
        ("FCCustomAmount", c_double),
        ("FCCustomRiskLevel", c_double),
    ]

    def getForceCloseLevel(self):
        '''强平标准'''
        return TShfeFtdcForceCloseLevelType(ord(self.ForceCloseLevel))

    def getForceCloseRelease(self):
        '''强平资金释放标准'''
        return TShfeFtdcForceCloseReleaseType(ord(self.ForceCloseRelease))

    def getFCNonLimitFirst(self):
        '''非停板方向持仓优先'''
        return self.FCNonLimitFirst

    def getFCPosiProfitLossFirst(self):
        '''亏损大的持仓优先'''
        return self.FCPosiProfitLossFirst

    def getFCCustomAmount(self):
        '''强平自定义金额'''
        return self.FCCustomAmount

    def getFCCustomRiskLevel(self):
        '''强平自定义平止风险度M/B'''
        return self.FCCustomRiskLevel

    @property
    def __str__(self):
        return f"'ForceCloseLevel'={self.getForceCloseLevel()}, 'ForceCloseRelease'={self.getForceCloseRelease()}, 'FCNonLimitFirst'={self.getFCNonLimitFirst()}, 'FCPosiProfitLossFirst'={self.getFCPosiProfitLossFirst()}, 'FCCustomAmount'={self.getFCCustomAmount()}, 'FCCustomRiskLevel'={self.getFCCustomRiskLevel()}"

    @property
    def __dict__(self):
        return {'ForceCloseLevel': self.getForceCloseLevel(), 'ForceCloseRelease': self.getForceCloseRelease(), 'FCNonLimitFirst': self.getFCNonLimitFirst(), 'FCPosiProfitLossFirst': self.getFCPosiProfitLossFirst(), 'FCCustomAmount': self.getFCCustomAmount(), 'FCCustomRiskLevel': self.getFCCustomRiskLevel()}


class  CShfeFtdcForceClosePositionRuleField(Structure):
    """强平持仓规则"""
    _fields_ = [
        ("ProductInstrumentID", c_char*31),
        ("FCPosiDirection", c_char),
        ("FCHedgeFlag", c_char),
        ("FCCombPosiFlag", c_char),
        ("FCHistoryPosiOrder", c_char),
        ("FCPrice", c_char),
        ("PriceTick", c_int32),
        ("FCRulePriority", c_char*21),
    ]

    def getProductInstrumentID(self):
        '''产品或合约代码'''
        return str(self.ProductInstrumentID, 'GBK')

    def getFCPosiDirection(self):
        '''强平持仓方向'''
        return TShfeFtdcForceClosePosiDirectionType(ord(self.FCPosiDirection))

    def getFCHedgeFlag(self):
        '''强平投机套保标志'''
        return TShfeFtdcForceCloseHedgeFlagType(ord(self.FCHedgeFlag))

    def getFCCombPosiFlag(self):
        '''强平组合持仓标志'''
        return TShfeFtdcForceCloseCombPosiFlagType(ord(self.FCCombPosiFlag))

    def getFCHistoryPosiOrder(self):
        '''强平历史持仓顺序'''
        return TShfeFtdcForceCloseHistoryPosiOrderType(ord(self.FCHistoryPosiOrder))

    def getFCPrice(self):
        '''强平价格类型'''
        return TShfeFtdcForceClosePriceTypeType(ord(self.FCPrice))

    def getPriceTick(self):
        '''限价调整点数'''
        return self.PriceTick

    def getFCRulePriority(self):
        '''批量强平计算规则优先级'''
        return str(self.FCRulePriority, 'GBK')

    @property
    def __str__(self):
        return f"'ProductInstrumentID'={self.getProductInstrumentID()}, 'FCPosiDirection'={self.getFCPosiDirection()}, 'FCHedgeFlag'={self.getFCHedgeFlag()}, 'FCCombPosiFlag'={self.getFCCombPosiFlag()}, 'FCHistoryPosiOrder'={self.getFCHistoryPosiOrder()}, 'FCPrice'={self.getFCPrice()}, 'PriceTick'={self.getPriceTick()}, 'FCRulePriority'={self.getFCRulePriority()}"

    @property
    def __dict__(self):
        return {'ProductInstrumentID': self.getProductInstrumentID(), 'FCPosiDirection': self.getFCPosiDirection(), 'FCHedgeFlag': self.getFCHedgeFlag(), 'FCCombPosiFlag': self.getFCCombPosiFlag(), 'FCHistoryPosiOrder': self.getFCHistoryPosiOrder(), 'FCPrice': self.getFCPrice(), 'PriceTick': self.getPriceTick(), 'FCRulePriority': self.getFCRulePriority()}


class  CShfeFtdcForceCloseListField(Structure):
    """强平名单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcForceClosePositionField(Structure):
    """投资者强平持仓"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("PosiDirection", c_char),
        ("HedgeFlag", c_char),
        ("PositionDate", c_char),
        ("Position", c_int32),
        ("FCPosition", c_int32),
        ("FCPriceType", c_char),
        ("PriceTick", c_int32),
        ("FCPrice", c_double),
        ("ReleaseMargin", c_double),
        ("CloseProfit", c_double),
        ("ExchReleaseMargin", c_double),
        ("PosiProfit", c_double),
        ("CashIn", c_double),
        ("OptionValue", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPosiDirection(self):
        '''持仓多空方向'''
        return TShfeFtdcPosiDirectionType(ord(self.PosiDirection))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPositionDate(self):
        '''持仓日期'''
        return TShfeFtdcPositionDateType(ord(self.PositionDate))

    def getPosition(self):
        '''当前持仓数量'''
        return self.Position

    def getFCPosition(self):
        '''需强平持仓数量'''
        return self.FCPosition

    def getFCPriceType(self):
        '''强平价格类型'''
        return TShfeFtdcForceClosePriceTypeType(ord(self.FCPriceType))

    def getPriceTick(self):
        '''限价调整点数'''
        return self.PriceTick

    def getFCPrice(self):
        '''强平价格'''
        return self.FCPrice

    def getReleaseMargin(self):
        '''平仓释放的保证金'''
        return self.ReleaseMargin

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getExchReleaseMargin(self):
        '''平仓释放的交易所保证金'''
        return self.ExchReleaseMargin

    def getPosiProfit(self):
        '''持仓盈亏'''
        return self.PosiProfit

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'PosiDirection'={self.getPosiDirection()}, 'HedgeFlag'={self.getHedgeFlag()}, 'PositionDate'={self.getPositionDate()}, 'Position'={self.getPosition()}, 'FCPosition'={self.getFCPosition()}, 'FCPriceType'={self.getFCPriceType()}, 'PriceTick'={self.getPriceTick()}, 'FCPrice'={self.getFCPrice()}, 'ReleaseMargin'={self.getReleaseMargin()}, 'CloseProfit'={self.getCloseProfit()}, 'ExchReleaseMargin'={self.getExchReleaseMargin()}, 'PosiProfit'={self.getPosiProfit()}, 'CashIn'={self.getCashIn()}, 'OptionValue'={self.getOptionValue()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'PosiDirection': self.getPosiDirection(), 'HedgeFlag': self.getHedgeFlag(), 'PositionDate': self.getPositionDate(), 'Position': self.getPosition(), 'FCPosition': self.getFCPosition(), 'FCPriceType': self.getFCPriceType(), 'PriceTick': self.getPriceTick(), 'FCPrice': self.getFCPrice(), 'ReleaseMargin': self.getReleaseMargin(), 'CloseProfit': self.getCloseProfit(), 'ExchReleaseMargin': self.getExchReleaseMargin(), 'PosiProfit': self.getPosiProfit(), 'CashIn': self.getCashIn(), 'OptionValue': self.getOptionValue()}


class  CShfeFtdcRspForceClosePositionField(Structure):
    """强平应答"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("PosiDirection", c_char),
        ("HedgeFlag", c_char),
        ("PositionDate", c_char),
        ("Position", c_int32),
        ("FCPosition", c_int32),
        ("FCPriceType", c_char),
        ("PriceTick", c_int32),
        ("FCPrice", c_double),
        ("ReleaseMargin", c_double),
        ("CloseProfit", c_double),
        ("FCID", c_char*24),
        ("Time", c_char*9),
        ("CurrMillisec", c_int32),
        ("ExchReleaseMargin", c_double),
        ("PosiProfit", c_double),
        ("CashIn", c_double),
        ("OptionValue", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPosiDirection(self):
        '''持仓多空方向'''
        return TShfeFtdcPosiDirectionType(ord(self.PosiDirection))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPositionDate(self):
        '''持仓日期'''
        return TShfeFtdcPositionDateType(ord(self.PositionDate))

    def getPosition(self):
        '''当前持仓数量'''
        return self.Position

    def getFCPosition(self):
        '''需强平持仓数量'''
        return self.FCPosition

    def getFCPriceType(self):
        '''强平价格类型'''
        return TShfeFtdcForceClosePriceTypeType(ord(self.FCPriceType))

    def getPriceTick(self):
        '''限价调整点数'''
        return self.PriceTick

    def getFCPrice(self):
        '''强平价格'''
        return self.FCPrice

    def getReleaseMargin(self):
        '''平仓释放的保证金'''
        return self.ReleaseMargin

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getFCID(self):
        '''强平场景编号'''
        return str(self.FCID, 'GBK')

    def getTime(self):
        '''辅助强平单的生成时间'''
        return str(self.Time, 'GBK')

    def getCurrMillisec(self):
        '''当前时间（毫秒）'''
        return self.CurrMillisec

    def getExchReleaseMargin(self):
        '''平仓释放的交易所保证金'''
        return self.ExchReleaseMargin

    def getPosiProfit(self):
        '''持仓盈亏'''
        return self.PosiProfit

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'PosiDirection'={self.getPosiDirection()}, 'HedgeFlag'={self.getHedgeFlag()}, 'PositionDate'={self.getPositionDate()}, 'Position'={self.getPosition()}, 'FCPosition'={self.getFCPosition()}, 'FCPriceType'={self.getFCPriceType()}, 'PriceTick'={self.getPriceTick()}, 'FCPrice'={self.getFCPrice()}, 'ReleaseMargin'={self.getReleaseMargin()}, 'CloseProfit'={self.getCloseProfit()}, 'FCID'={self.getFCID()}, 'Time'={self.getTime()}, 'CurrMillisec'={self.getCurrMillisec()}, 'ExchReleaseMargin'={self.getExchReleaseMargin()}, 'PosiProfit'={self.getPosiProfit()}, 'CashIn'={self.getCashIn()}, 'OptionValue'={self.getOptionValue()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'PosiDirection': self.getPosiDirection(), 'HedgeFlag': self.getHedgeFlag(), 'PositionDate': self.getPositionDate(), 'Position': self.getPosition(), 'FCPosition': self.getFCPosition(), 'FCPriceType': self.getFCPriceType(), 'PriceTick': self.getPriceTick(), 'FCPrice': self.getFCPrice(), 'ReleaseMargin': self.getReleaseMargin(), 'CloseProfit': self.getCloseProfit(), 'FCID': self.getFCID(), 'Time': self.getTime(), 'CurrMillisec': self.getCurrMillisec(), 'ExchReleaseMargin': self.getExchReleaseMargin(), 'PosiProfit': self.getPosiProfit(), 'CashIn': self.getCashIn(), 'OptionValue': self.getOptionValue()}


class  CShfeFtdcRiskForceCloseOrderField(Structure):
    """风控强平报单输入"""
    _fields_ = [
        ("FCType", c_char),
        ("Time1", c_char*9),
        ("Millisec1", c_int32),
        ("Time2", c_char*9),
        ("Millisec2", c_int32),
        ("FCSceneId", c_char*24),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("UserForceClose", c_int32),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("IsSwapOrder", c_int32),
        ("ExchangeID", c_char*9),
        ("InvestUnitID", c_char*17),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("ClientID", c_char*11),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getFCType(self):
        '''风控强平类型'''
        return TShfeFtdcForceCloseTypeType(ord(self.FCType))

    def getTime1(self):
        '''辅助强平单的生成时间'''
        return str(self.Time1, 'GBK')

    def getMillisec1(self):
        '''辅助强平单的生成时间（毫秒）'''
        return self.Millisec1

    def getTime2(self):
        '''强平单的提交时间'''
        return str(self.Time2, 'GBK')

    def getMillisec2(self):
        '''强平单的提交时间（毫秒）'''
        return self.Millisec2

    def getFCSceneId(self):
        '''强平场景编号'''
        return str(self.FCSceneId, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getUserForceClose(self):
        '''用户强评标志'''
        return self.UserForceClose

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getIsSwapOrder(self):
        '''互换单标志'''
        return self.IsSwapOrder

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getClientID(self):
        '''交易编码'''
        return str(self.ClientID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'FCType'={self.getFCType()}, 'Time1'={self.getTime1()}, 'Millisec1'={self.getMillisec1()}, 'Time2'={self.getTime2()}, 'Millisec2'={self.getMillisec2()}, 'FCSceneId'={self.getFCSceneId()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'UserForceClose'={self.getUserForceClose()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'IsSwapOrder'={self.getIsSwapOrder()}, 'ExchangeID'={self.getExchangeID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'ClientID'={self.getClientID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'FCType': self.getFCType(), 'Time1': self.getTime1(), 'Millisec1': self.getMillisec1(), 'Time2': self.getTime2(), 'Millisec2': self.getMillisec2(), 'FCSceneId': self.getFCSceneId(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'UserForceClose': self.getUserForceClose(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'IsSwapOrder': self.getIsSwapOrder(), 'ExchangeID': self.getExchangeID(), 'InvestUnitID': self.getInvestUnitID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'ClientID': self.getClientID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcFrontStatusReportField(Structure):
    """前置状态报告"""
    _fields_ = [
        ("Seconds", c_int32),
    ]

    def getSeconds(self):
        '''前置time(NULL)'''
        return self.Seconds

    @property
    def __str__(self):
        return f"'Seconds'={self.getSeconds()}"

    @property
    def __dict__(self):
        return {'Seconds': self.getSeconds()}


class  CShfeFtdcIndexNPPParamField(Structure):
    """净持仓保证金指标参数"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("ProductIDs", c_char*101),
        ("WarnLevel", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getProductIDs(self):
        '''产品代码'''
        return str(self.ProductIDs, 'GBK')

    def getWarnLevel(self):
        '''报警值'''
        return self.WarnLevel

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'ProductIDs'={self.getProductIDs()}, 'WarnLevel'={self.getWarnLevel()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'ProductIDs': self.getProductIDs(), 'WarnLevel': self.getWarnLevel()}


class  CShfeFtdcIndexNPPField(Structure):
    """净持仓保证金指标值"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("ProductIDs", c_char*101),
        ("Value", c_double),
        ("LongMargin", c_double),
        ("ShortMargin", c_double),
        ("Balance", c_double),
        ("WarnLevel", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getProductIDs(self):
        '''产品代码'''
        return str(self.ProductIDs, 'GBK')

    def getValue(self):
        '''指标值'''
        return self.Value

    def getLongMargin(self):
        '''多头保证金'''
        return self.LongMargin

    def getShortMargin(self):
        '''空头保证金'''
        return self.ShortMargin

    def getBalance(self):
        '''总权益'''
        return self.Balance

    def getWarnLevel(self):
        '''报警值'''
        return self.WarnLevel

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'ProductIDs'={self.getProductIDs()}, 'Value'={self.getValue()}, 'LongMargin'={self.getLongMargin()}, 'ShortMargin'={self.getShortMargin()}, 'Balance'={self.getBalance()}, 'WarnLevel'={self.getWarnLevel()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'ProductIDs': self.getProductIDs(), 'Value': self.getValue(), 'LongMargin': self.getLongMargin(), 'ShortMargin': self.getShortMargin(), 'Balance': self.getBalance(), 'WarnLevel': self.getWarnLevel()}


class  CShfeFtdcNormalRiskQueryField(Structure):
    """一般查询请求"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID()}


class  CShfeFtdcQrySafePriceRangeField(Structure):
    """查询安全价格波动范围请求"""
    _fields_ = [
        ("PriceVaryAlgo", c_char),
        ("RiskLevel", c_char),
        ("MaxLimitDay", c_int32),
    ]

    def getPriceVaryAlgo(self):
        '''合约价格波动方法'''
        return TShfeFtdcPriceVaryAlgoType(ord(self.PriceVaryAlgo))

    def getRiskLevel(self):
        '''风险类型'''
        return TShfeFtdcNotifyClassType(ord(self.RiskLevel))

    def getMaxLimitDay(self):
        '''按合约顺序波动时的最大允许停板个数'''
        return self.MaxLimitDay

    @property
    def __str__(self):
        return f"'PriceVaryAlgo'={self.getPriceVaryAlgo()}, 'RiskLevel'={self.getRiskLevel()}, 'MaxLimitDay'={self.getMaxLimitDay()}"

    @property
    def __dict__(self):
        return {'PriceVaryAlgo': self.getPriceVaryAlgo(), 'RiskLevel': self.getRiskLevel(), 'MaxLimitDay': self.getMaxLimitDay()}


class  CShfeFtdcPriceVaryParamField(Structure):
    """价格波动参数"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("Direction", c_char),
        ("Pecent", c_double),
        ("BasePriceType", c_char),
        ("BasePrice", c_double),
    ]

    def getInstrumentID(self):
        '''合约编号'''
        return str(self.InstrumentID, 'GBK')

    def getDirection(self):
        '''价格波动方向'''
        return TShfeFtdcPriceVaryDirType(ord(self.Direction))

    def getPecent(self):
        '''价格波动幅度(>=0有效)'''
        return self.Pecent

    def getBasePriceType(self):
        '''价格波动的基准价类型'''
        return TShfeFtdcPriceTypeType(ord(self.BasePriceType))

    def getBasePrice(self):
        '''自定义基准价'''
        return self.BasePrice

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'Direction'={self.getDirection()}, 'Pecent'={self.getPecent()}, 'BasePriceType'={self.getBasePriceType()}, 'BasePrice'={self.getBasePrice()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'Direction': self.getDirection(), 'Pecent': self.getPecent(), 'BasePriceType': self.getBasePriceType(), 'BasePrice': self.getBasePrice()}


class  CShfeFtdcSafePriceRangeField(Structure):
    """查询安全价格波动范围应答"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("BasePrice", c_double),
        ("LimitPrice", c_double),
        ("VaryPecent", c_double),
        ("LimitDayCnt", c_int32),
        ("VaryTickCnt", c_int32),
        ("LimitTickCnt", c_int32),
        ("HasLimit", c_int32),
        ("PecentPerLimit", c_double),
        ("InLimitVaryPct", c_double),
        ("OutLimitVaryPct", c_double),
        ("LongVol", c_int32),
        ("ShortVol", c_int32),
        ("Direction", c_char),
        ("BadDir", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBasePrice(self):
        '''基准价格'''
        return self.BasePrice

    def getLimitPrice(self):
        '''波动价格'''
        return self.LimitPrice

    def getVaryPecent(self):
        '''总波动幅度'''
        return self.VaryPecent

    def getLimitDayCnt(self):
        '''停板个数'''
        return self.LimitDayCnt

    def getVaryTickCnt(self):
        '''总波动点数'''
        return self.VaryTickCnt

    def getLimitTickCnt(self):
        '''停板点数'''
        return self.LimitTickCnt

    def getHasLimit(self):
        '''是否有波动限制'''
        return self.HasLimit

    def getPecentPerLimit(self):
        '''涨跌停'''
        return self.PecentPerLimit

    def getInLimitVaryPct(self):
        '''停板波动'''
        return self.InLimitVaryPct

    def getOutLimitVaryPct(self):
        '''停板外波动'''
        return self.OutLimitVaryPct

    def getLongVol(self):
        '''总买持'''
        return self.LongVol

    def getShortVol(self):
        '''总卖持'''
        return self.ShortVol

    def getDirection(self):
        '''波动方向'''
        return TShfeFtdcPriceVaryDirType(ord(self.Direction))

    def getBadDir(self):
        '''不利方向'''
        return TShfeFtdcPriceVaryDirType(ord(self.BadDir))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'BasePrice'={self.getBasePrice()}, 'LimitPrice'={self.getLimitPrice()}, 'VaryPecent'={self.getVaryPecent()}, 'LimitDayCnt'={self.getLimitDayCnt()}, 'VaryTickCnt'={self.getVaryTickCnt()}, 'LimitTickCnt'={self.getLimitTickCnt()}, 'HasLimit'={self.getHasLimit()}, 'PecentPerLimit'={self.getPecentPerLimit()}, 'InLimitVaryPct'={self.getInLimitVaryPct()}, 'OutLimitVaryPct'={self.getOutLimitVaryPct()}, 'LongVol'={self.getLongVol()}, 'ShortVol'={self.getShortVol()}, 'Direction'={self.getDirection()}, 'BadDir'={self.getBadDir()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'BasePrice': self.getBasePrice(), 'LimitPrice': self.getLimitPrice(), 'VaryPecent': self.getVaryPecent(), 'LimitDayCnt': self.getLimitDayCnt(), 'VaryTickCnt': self.getVaryTickCnt(), 'LimitTickCnt': self.getLimitTickCnt(), 'HasLimit': self.getHasLimit(), 'PecentPerLimit': self.getPecentPerLimit(), 'InLimitVaryPct': self.getInLimitVaryPct(), 'OutLimitVaryPct': self.getOutLimitVaryPct(), 'LongVol': self.getLongVol(), 'ShortVol': self.getShortVol(), 'Direction': self.getDirection(), 'BadDir': self.getBadDir()}


class  CShfeFtdcQryPriceVaryEffectField(Structure):
    """查询价格波动对投资者风险的影响"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("RiskLevel", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getRiskLevel(self):
        '''风险类型'''
        return TShfeFtdcNotifyClassType(ord(self.RiskLevel))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'RiskLevel'={self.getRiskLevel()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'RiskLevel': self.getRiskLevel()}


class  CShfeFtdcBrokerInvestorField(Structure):
    """经纪公司投资者"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}


class  CShfeFtdcTradeParamField(Structure):
    """交易系统参数"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("TradeParamID", c_char),
        ("TradeParamValue", c_char*256),
        ("Memo", c_char*161),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getTradeParamID(self):
        '''参数代码'''
        return TShfeFtdcTradeParamIDType(ord(self.TradeParamID))

    def getTradeParamValue(self):
        '''参数代码值'''
        return str(self.TradeParamValue, 'GBK')

    def getMemo(self):
        '''备注'''
        return str(self.Memo, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'TradeParamID'={self.getTradeParamID()}, 'TradeParamValue'={self.getTradeParamValue()}, 'Memo'={self.getMemo()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'TradeParamID': self.getTradeParamID(), 'TradeParamValue': self.getTradeParamValue(), 'Memo': self.getMemo()}


class  CShfeFtdcRiskParkedOrderField(Structure):
    """风控预埋单"""
    _fields_ = [
        ("ParkedOrderID", c_char*13),
        ("LocalID", c_char*13),
        ("UserType", c_char),
        ("Status", c_char),
        ("StatusMsg", c_char*81),
        ("TriggerType", c_char),
        ("TradeSegment", c_int32),
        ("ExchangeID", c_char*9),
        ("FCType", c_char),
        ("Time1", c_char*9),
        ("Millisec1", c_int32),
        ("Time2", c_char*9),
        ("Millisec2", c_int32),
        ("FCSceneId", c_char*24),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("UserForceClose", c_int32),
        ("OrderSubmitStatus", c_char),
        ("OrderStatus", c_char),
        ("OrderStatusMsg", c_char*81),
        ("ErrorID", c_int32),
        ("ErrorMsg", c_char*81),
        ("ParkedTime", c_char*9),
        ("OriginalParkedVol", c_int32),
        ("MaxCloseVol1", c_int32),
        ("MaxCloseVol2", c_int32),
        ("Call1", c_double),
        ("Call2", c_double),
        ("MoneyIO1", c_double),
        ("MoneyIO2", c_double),
        ("DeleteReason", c_char*31),
        ("ForceCloseRelease", c_char),
        ("IsSwapOrder", c_int32),
        ("InvestUnitID", c_char*17),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("ClientID", c_char*11),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getParkedOrderID(self):
        '''预埋报单编号'''
        return str(self.ParkedOrderID, 'GBK')

    def getLocalID(self):
        '''预埋单本地编号'''
        return str(self.LocalID, 'GBK')

    def getUserType(self):
        '''风控用户类型'''
        return TShfeFtdcRiskUserTypeType(ord(self.UserType))

    def getStatus(self):
        '''预埋单状态'''
        return TShfeFtdcRiskParkedOrderStatusType(ord(self.Status))

    def getStatusMsg(self):
        '''预埋单状态信息'''
        return str(self.StatusMsg, 'GBK')

    def getTriggerType(self):
        '''触发类型'''
        return TShfeFtdcOrderTriggerTypeType(ord(self.TriggerType))

    def getTradeSegment(self):
        '''交易阶段'''
        return self.TradeSegment

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getFCType(self):
        '''风控强平类型'''
        return TShfeFtdcForceCloseTypeType(ord(self.FCType))

    def getTime1(self):
        '''辅助强平单的生成时间'''
        return str(self.Time1, 'GBK')

    def getMillisec1(self):
        '''辅助强平单的生成时间（毫秒）'''
        return self.Millisec1

    def getTime2(self):
        '''强平单的提交时间'''
        return str(self.Time2, 'GBK')

    def getMillisec2(self):
        '''强平单的提交时间（毫秒）'''
        return self.Millisec2

    def getFCSceneId(self):
        '''强平场景编号'''
        return str(self.FCSceneId, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getUserForceClose(self):
        '''用户强评标志'''
        return self.UserForceClose

    def getOrderSubmitStatus(self):
        '''报单提交状态'''
        return TShfeFtdcOrderSubmitStatusType(ord(self.OrderSubmitStatus))

    def getOrderStatus(self):
        '''报单状态'''
        return TShfeFtdcOrderStatusType(ord(self.OrderStatus))

    def getOrderStatusMsg(self):
        '''报单状态信息'''
        return str(self.OrderStatusMsg, 'GBK')

    def getErrorID(self):
        '''错误代码'''
        return self.ErrorID

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    def getParkedTime(self):
        '''预埋时间'''
        return str(self.ParkedTime, 'GBK')

    def getOriginalParkedVol(self):
        '''预埋量'''
        return self.OriginalParkedVol

    def getMaxCloseVol1(self):
        '''预埋时可平量'''
        return self.MaxCloseVol1

    def getMaxCloseVol2(self):
        '''触发时可平量'''
        return self.MaxCloseVol2

    def getCall1(self):
        '''预埋时追保'''
        return self.Call1

    def getCall2(self):
        '''触发时追保'''
        return self.Call2

    def getMoneyIO1(self):
        '''预埋时出入金'''
        return self.MoneyIO1

    def getMoneyIO2(self):
        '''触发时出入金'''
        return self.MoneyIO2

    def getDeleteReason(self):
        '''删除原因'''
        return str(self.DeleteReason, 'GBK')

    def getForceCloseRelease(self):
        '''强平资金释放标准'''
        return TShfeFtdcForceCloseReleaseType(ord(self.ForceCloseRelease))

    def getIsSwapOrder(self):
        '''互换单标志'''
        return self.IsSwapOrder

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getClientID(self):
        '''交易编码'''
        return str(self.ClientID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'ParkedOrderID'={self.getParkedOrderID()}, 'LocalID'={self.getLocalID()}, 'UserType'={self.getUserType()}, 'Status'={self.getStatus()}, 'StatusMsg'={self.getStatusMsg()}, 'TriggerType'={self.getTriggerType()}, 'TradeSegment'={self.getTradeSegment()}, 'ExchangeID'={self.getExchangeID()}, 'FCType'={self.getFCType()}, 'Time1'={self.getTime1()}, 'Millisec1'={self.getMillisec1()}, 'Time2'={self.getTime2()}, 'Millisec2'={self.getMillisec2()}, 'FCSceneId'={self.getFCSceneId()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'UserForceClose'={self.getUserForceClose()}, 'OrderSubmitStatus'={self.getOrderSubmitStatus()}, 'OrderStatus'={self.getOrderStatus()}, 'OrderStatusMsg'={self.getOrderStatusMsg()}, 'ErrorID'={self.getErrorID()}, 'ErrorMsg'={self.getErrorMsg()}, 'ParkedTime'={self.getParkedTime()}, 'OriginalParkedVol'={self.getOriginalParkedVol()}, 'MaxCloseVol1'={self.getMaxCloseVol1()}, 'MaxCloseVol2'={self.getMaxCloseVol2()}, 'Call1'={self.getCall1()}, 'Call2'={self.getCall2()}, 'MoneyIO1'={self.getMoneyIO1()}, 'MoneyIO2'={self.getMoneyIO2()}, 'DeleteReason'={self.getDeleteReason()}, 'ForceCloseRelease'={self.getForceCloseRelease()}, 'IsSwapOrder'={self.getIsSwapOrder()}, 'InvestUnitID'={self.getInvestUnitID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'ClientID'={self.getClientID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'ParkedOrderID': self.getParkedOrderID(), 'LocalID': self.getLocalID(), 'UserType': self.getUserType(), 'Status': self.getStatus(), 'StatusMsg': self.getStatusMsg(), 'TriggerType': self.getTriggerType(), 'TradeSegment': self.getTradeSegment(), 'ExchangeID': self.getExchangeID(), 'FCType': self.getFCType(), 'Time1': self.getTime1(), 'Millisec1': self.getMillisec1(), 'Time2': self.getTime2(), 'Millisec2': self.getMillisec2(), 'FCSceneId': self.getFCSceneId(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'UserForceClose': self.getUserForceClose(), 'OrderSubmitStatus': self.getOrderSubmitStatus(), 'OrderStatus': self.getOrderStatus(), 'OrderStatusMsg': self.getOrderStatusMsg(), 'ErrorID': self.getErrorID(), 'ErrorMsg': self.getErrorMsg(), 'ParkedTime': self.getParkedTime(), 'OriginalParkedVol': self.getOriginalParkedVol(), 'MaxCloseVol1': self.getMaxCloseVol1(), 'MaxCloseVol2': self.getMaxCloseVol2(), 'Call1': self.getCall1(), 'Call2': self.getCall2(), 'MoneyIO1': self.getMoneyIO1(), 'MoneyIO2': self.getMoneyIO2(), 'DeleteReason': self.getDeleteReason(), 'ForceCloseRelease': self.getForceCloseRelease(), 'IsSwapOrder': self.getIsSwapOrder(), 'InvestUnitID': self.getInvestUnitID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'ClientID': self.getClientID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcRemoveRiskParkedOrderField(Structure):
    """删除风控预埋单"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorID", c_char*13),
        ("ParkedOrderID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getParkedOrderID(self):
        '''预埋报单编号'''
        return str(self.ParkedOrderID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorID'={self.getInvestorID()}, 'ParkedOrderID'={self.getParkedOrderID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorID': self.getInvestorID(), 'ParkedOrderID': self.getParkedOrderID()}


class  CShfeFtdcSeqRiskParkedOrderField(Structure):
    """有序的风控预埋单"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("ParkedOrderID", c_char*13),
        ("LocalID", c_char*13),
        ("UserType", c_char),
        ("Status", c_char),
        ("StatusMsg", c_char*81),
        ("TriggerType", c_char),
        ("TradeSegment", c_int32),
        ("ExchangeID", c_char*9),
        ("FCType", c_char),
        ("Time1", c_char*9),
        ("Millisec1", c_int32),
        ("Time2", c_char*9),
        ("Millisec2", c_int32),
        ("FCSceneId", c_char*24),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("OrderRef", c_char*13),
        ("UserID", c_char*16),
        ("OrderPriceType", c_char),
        ("Direction", c_char),
        ("CombOffsetFlag", c_char*5),
        ("CombHedgeFlag", c_char*5),
        ("LimitPrice", c_double),
        ("VolumeTotalOriginal", c_int32),
        ("TimeCondition", c_char),
        ("GTDDate", c_char*9),
        ("VolumeCondition", c_char),
        ("MinVolume", c_int32),
        ("ContingentCondition", c_char),
        ("StopPrice", c_double),
        ("ForceCloseReason", c_char),
        ("IsAutoSuspend", c_int32),
        ("BusinessUnit", c_char*21),
        ("RequestID", c_int32),
        ("UserForceClose", c_int32),
        ("OrderSubmitStatus", c_char),
        ("OrderStatus", c_char),
        ("OrderStatusMsg", c_char*81),
        ("ErrorID", c_int32),
        ("ErrorMsg", c_char*81),
        ("ParkedTime", c_char*9),
        ("OriginalParkedVol", c_int32),
        ("MaxCloseVol1", c_int32),
        ("MaxCloseVol2", c_int32),
        ("Call1", c_double),
        ("Call2", c_double),
        ("MoneyIO1", c_double),
        ("MoneyIO2", c_double),
        ("DeleteReason", c_char*31),
        ("ForceCloseRelease", c_char),
        ("IsSwapOrder", c_int32),
        ("InvestUnitID", c_char*17),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("ClientID", c_char*11),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getParkedOrderID(self):
        '''预埋报单编号'''
        return str(self.ParkedOrderID, 'GBK')

    def getLocalID(self):
        '''预埋单本地编号'''
        return str(self.LocalID, 'GBK')

    def getUserType(self):
        '''风控用户类型'''
        return TShfeFtdcRiskUserTypeType(ord(self.UserType))

    def getStatus(self):
        '''预埋单状态'''
        return TShfeFtdcRiskParkedOrderStatusType(ord(self.Status))

    def getStatusMsg(self):
        '''预埋单状态信息'''
        return str(self.StatusMsg, 'GBK')

    def getTriggerType(self):
        '''触发类型'''
        return TShfeFtdcOrderTriggerTypeType(ord(self.TriggerType))

    def getTradeSegment(self):
        '''交易阶段'''
        return self.TradeSegment

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getFCType(self):
        '''风控强平类型'''
        return TShfeFtdcForceCloseTypeType(ord(self.FCType))

    def getTime1(self):
        '''辅助强平单的生成时间'''
        return str(self.Time1, 'GBK')

    def getMillisec1(self):
        '''辅助强平单的生成时间（毫秒）'''
        return self.Millisec1

    def getTime2(self):
        '''强平单的提交时间'''
        return str(self.Time2, 'GBK')

    def getMillisec2(self):
        '''强平单的提交时间（毫秒）'''
        return self.Millisec2

    def getFCSceneId(self):
        '''强平场景编号'''
        return str(self.FCSceneId, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getOrderRef(self):
        '''报单引用'''
        return str(self.OrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getOrderPriceType(self):
        '''报单价格条件'''
        return TShfeFtdcOrderPriceTypeType(ord(self.OrderPriceType))

    def getDirection(self):
        '''买卖方向'''
        return TShfeFtdcDirectionType(ord(self.Direction))

    def getCombOffsetFlag(self):
        '''组合开平标志'''
        return str(self.CombOffsetFlag, 'GBK')

    def getCombHedgeFlag(self):
        '''组合投机套保标志'''
        return str(self.CombHedgeFlag, 'GBK')

    def getLimitPrice(self):
        '''价格'''
        return self.LimitPrice

    def getVolumeTotalOriginal(self):
        '''数量'''
        return self.VolumeTotalOriginal

    def getTimeCondition(self):
        '''有效期类型'''
        return TShfeFtdcTimeConditionType(ord(self.TimeCondition))

    def getGTDDate(self):
        '''GTD日期'''
        return str(self.GTDDate, 'GBK')

    def getVolumeCondition(self):
        '''成交量类型'''
        return TShfeFtdcVolumeConditionType(ord(self.VolumeCondition))

    def getMinVolume(self):
        '''最小成交量'''
        return self.MinVolume

    def getContingentCondition(self):
        '''触发条件'''
        return TShfeFtdcContingentConditionType(ord(self.ContingentCondition))

    def getStopPrice(self):
        '''止损价'''
        return self.StopPrice

    def getForceCloseReason(self):
        '''强平原因'''
        return TShfeFtdcForceCloseReasonType(ord(self.ForceCloseReason))

    def getIsAutoSuspend(self):
        '''自动挂起标志'''
        return self.IsAutoSuspend

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getUserForceClose(self):
        '''用户强评标志'''
        return self.UserForceClose

    def getOrderSubmitStatus(self):
        '''报单提交状态'''
        return TShfeFtdcOrderSubmitStatusType(ord(self.OrderSubmitStatus))

    def getOrderStatus(self):
        '''报单状态'''
        return TShfeFtdcOrderStatusType(ord(self.OrderStatus))

    def getOrderStatusMsg(self):
        '''报单状态信息'''
        return str(self.OrderStatusMsg, 'GBK')

    def getErrorID(self):
        '''错误代码'''
        return self.ErrorID

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    def getParkedTime(self):
        '''预埋时间'''
        return str(self.ParkedTime, 'GBK')

    def getOriginalParkedVol(self):
        '''预埋量'''
        return self.OriginalParkedVol

    def getMaxCloseVol1(self):
        '''预埋时可平量'''
        return self.MaxCloseVol1

    def getMaxCloseVol2(self):
        '''触发时可平量'''
        return self.MaxCloseVol2

    def getCall1(self):
        '''预埋时追保'''
        return self.Call1

    def getCall2(self):
        '''触发时追保'''
        return self.Call2

    def getMoneyIO1(self):
        '''预埋时出入金'''
        return self.MoneyIO1

    def getMoneyIO2(self):
        '''触发时出入金'''
        return self.MoneyIO2

    def getDeleteReason(self):
        '''删除原因'''
        return str(self.DeleteReason, 'GBK')

    def getForceCloseRelease(self):
        '''强平资金释放标准'''
        return TShfeFtdcForceCloseReleaseType(ord(self.ForceCloseRelease))

    def getIsSwapOrder(self):
        '''互换单标志'''
        return self.IsSwapOrder

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getClientID(self):
        '''交易编码'''
        return str(self.ClientID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'ParkedOrderID'={self.getParkedOrderID()}, 'LocalID'={self.getLocalID()}, 'UserType'={self.getUserType()}, 'Status'={self.getStatus()}, 'StatusMsg'={self.getStatusMsg()}, 'TriggerType'={self.getTriggerType()}, 'TradeSegment'={self.getTradeSegment()}, 'ExchangeID'={self.getExchangeID()}, 'FCType'={self.getFCType()}, 'Time1'={self.getTime1()}, 'Millisec1'={self.getMillisec1()}, 'Time2'={self.getTime2()}, 'Millisec2'={self.getMillisec2()}, 'FCSceneId'={self.getFCSceneId()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'OrderRef'={self.getOrderRef()}, 'UserID'={self.getUserID()}, 'OrderPriceType'={self.getOrderPriceType()}, 'Direction'={self.getDirection()}, 'CombOffsetFlag'={self.getCombOffsetFlag()}, 'CombHedgeFlag'={self.getCombHedgeFlag()}, 'LimitPrice'={self.getLimitPrice()}, 'VolumeTotalOriginal'={self.getVolumeTotalOriginal()}, 'TimeCondition'={self.getTimeCondition()}, 'GTDDate'={self.getGTDDate()}, 'VolumeCondition'={self.getVolumeCondition()}, 'MinVolume'={self.getMinVolume()}, 'ContingentCondition'={self.getContingentCondition()}, 'StopPrice'={self.getStopPrice()}, 'ForceCloseReason'={self.getForceCloseReason()}, 'IsAutoSuspend'={self.getIsAutoSuspend()}, 'BusinessUnit'={self.getBusinessUnit()}, 'RequestID'={self.getRequestID()}, 'UserForceClose'={self.getUserForceClose()}, 'OrderSubmitStatus'={self.getOrderSubmitStatus()}, 'OrderStatus'={self.getOrderStatus()}, 'OrderStatusMsg'={self.getOrderStatusMsg()}, 'ErrorID'={self.getErrorID()}, 'ErrorMsg'={self.getErrorMsg()}, 'ParkedTime'={self.getParkedTime()}, 'OriginalParkedVol'={self.getOriginalParkedVol()}, 'MaxCloseVol1'={self.getMaxCloseVol1()}, 'MaxCloseVol2'={self.getMaxCloseVol2()}, 'Call1'={self.getCall1()}, 'Call2'={self.getCall2()}, 'MoneyIO1'={self.getMoneyIO1()}, 'MoneyIO2'={self.getMoneyIO2()}, 'DeleteReason'={self.getDeleteReason()}, 'ForceCloseRelease'={self.getForceCloseRelease()}, 'IsSwapOrder'={self.getIsSwapOrder()}, 'InvestUnitID'={self.getInvestUnitID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'ClientID'={self.getClientID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'ParkedOrderID': self.getParkedOrderID(), 'LocalID': self.getLocalID(), 'UserType': self.getUserType(), 'Status': self.getStatus(), 'StatusMsg': self.getStatusMsg(), 'TriggerType': self.getTriggerType(), 'TradeSegment': self.getTradeSegment(), 'ExchangeID': self.getExchangeID(), 'FCType': self.getFCType(), 'Time1': self.getTime1(), 'Millisec1': self.getMillisec1(), 'Time2': self.getTime2(), 'Millisec2': self.getMillisec2(), 'FCSceneId': self.getFCSceneId(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'OrderRef': self.getOrderRef(), 'UserID': self.getUserID(), 'OrderPriceType': self.getOrderPriceType(), 'Direction': self.getDirection(), 'CombOffsetFlag': self.getCombOffsetFlag(), 'CombHedgeFlag': self.getCombHedgeFlag(), 'LimitPrice': self.getLimitPrice(), 'VolumeTotalOriginal': self.getVolumeTotalOriginal(), 'TimeCondition': self.getTimeCondition(), 'GTDDate': self.getGTDDate(), 'VolumeCondition': self.getVolumeCondition(), 'MinVolume': self.getMinVolume(), 'ContingentCondition': self.getContingentCondition(), 'StopPrice': self.getStopPrice(), 'ForceCloseReason': self.getForceCloseReason(), 'IsAutoSuspend': self.getIsAutoSuspend(), 'BusinessUnit': self.getBusinessUnit(), 'RequestID': self.getRequestID(), 'UserForceClose': self.getUserForceClose(), 'OrderSubmitStatus': self.getOrderSubmitStatus(), 'OrderStatus': self.getOrderStatus(), 'OrderStatusMsg': self.getOrderStatusMsg(), 'ErrorID': self.getErrorID(), 'ErrorMsg': self.getErrorMsg(), 'ParkedTime': self.getParkedTime(), 'OriginalParkedVol': self.getOriginalParkedVol(), 'MaxCloseVol1': self.getMaxCloseVol1(), 'MaxCloseVol2': self.getMaxCloseVol2(), 'Call1': self.getCall1(), 'Call2': self.getCall2(), 'MoneyIO1': self.getMoneyIO1(), 'MoneyIO2': self.getMoneyIO2(), 'DeleteReason': self.getDeleteReason(), 'ForceCloseRelease': self.getForceCloseRelease(), 'IsSwapOrder': self.getIsSwapOrder(), 'InvestUnitID': self.getInvestUnitID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'ClientID': self.getClientID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcRiskInvestorInfoField(Structure):
    """风控中投资者消息"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("Mobile", c_char*41),
        ("EMail", c_char*101),
        ("IsEMail", c_int32),
        ("IsSMS", c_int32),
        ("InvestorType", c_char),
        ("PhoneCountryCode", c_char*11),
        ("PhoneAreaCode", c_char*11),
        ("OpenPhoneCountryCode", c_char*11),
        ("OpenPhoneAreaCode", c_char*11),
        ("OrderPhoneCountryCode", c_char*11),
        ("OrderPhoneAreaCode", c_char*11),
        ("FundPhoneCountryCode", c_char*11),
        ("FundPhoneAreaCode", c_char*11),
        ("SettlePhoneCountryCode", c_char*11),
        ("SettlePhoneAreaCode", c_char*11),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getMobile(self):
        '''手机'''
        return str(self.Mobile, 'GBK')

    def getEMail(self):
        '''电子邮件'''
        return str(self.EMail, 'GBK')

    def getIsEMail(self):
        '''是否允许发送邮件'''
        return self.IsEMail

    def getIsSMS(self):
        '''是否允许发送邮件'''
        return self.IsSMS

    def getInvestorType(self):
        '''投资者类型'''
        return TShfeFtdcInvestorTypeType(ord(self.InvestorType))

    def getPhoneCountryCode(self):
        '''国家代码'''
        return str(self.PhoneCountryCode, 'GBK')

    def getPhoneAreaCode(self):
        '''区号'''
        return str(self.PhoneAreaCode, 'GBK')

    def getOpenPhoneCountryCode(self):
        '''开户授权人国家代码'''
        return str(self.OpenPhoneCountryCode, 'GBK')

    def getOpenPhoneAreaCode(self):
        '''开户授权人区号'''
        return str(self.OpenPhoneAreaCode, 'GBK')

    def getOrderPhoneCountryCode(self):
        '''指定下单人国家代码'''
        return str(self.OrderPhoneCountryCode, 'GBK')

    def getOrderPhoneAreaCode(self):
        '''指定下单人区号'''
        return str(self.OrderPhoneAreaCode, 'GBK')

    def getFundPhoneCountryCode(self):
        '''资金调拨人国家代码'''
        return str(self.FundPhoneCountryCode, 'GBK')

    def getFundPhoneAreaCode(self):
        '''资金调拨人区号'''
        return str(self.FundPhoneAreaCode, 'GBK')

    def getSettlePhoneCountryCode(self):
        '''结算单确认人国家代码'''
        return str(self.SettlePhoneCountryCode, 'GBK')

    def getSettlePhoneAreaCode(self):
        '''结算单确认人区号'''
        return str(self.SettlePhoneAreaCode, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'Mobile'={self.getMobile()}, 'EMail'={self.getEMail()}, 'IsEMail'={self.getIsEMail()}, 'IsSMS'={self.getIsSMS()}, 'InvestorType'={self.getInvestorType()}, 'PhoneCountryCode'={self.getPhoneCountryCode()}, 'PhoneAreaCode'={self.getPhoneAreaCode()}, 'OpenPhoneCountryCode'={self.getOpenPhoneCountryCode()}, 'OpenPhoneAreaCode'={self.getOpenPhoneAreaCode()}, 'OrderPhoneCountryCode'={self.getOrderPhoneCountryCode()}, 'OrderPhoneAreaCode'={self.getOrderPhoneAreaCode()}, 'FundPhoneCountryCode'={self.getFundPhoneCountryCode()}, 'FundPhoneAreaCode'={self.getFundPhoneAreaCode()}, 'SettlePhoneCountryCode'={self.getSettlePhoneCountryCode()}, 'SettlePhoneAreaCode'={self.getSettlePhoneAreaCode()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'Mobile': self.getMobile(), 'EMail': self.getEMail(), 'IsEMail': self.getIsEMail(), 'IsSMS': self.getIsSMS(), 'InvestorType': self.getInvestorType(), 'PhoneCountryCode': self.getPhoneCountryCode(), 'PhoneAreaCode': self.getPhoneAreaCode(), 'OpenPhoneCountryCode': self.getOpenPhoneCountryCode(), 'OpenPhoneAreaCode': self.getOpenPhoneAreaCode(), 'OrderPhoneCountryCode': self.getOrderPhoneCountryCode(), 'OrderPhoneAreaCode': self.getOrderPhoneAreaCode(), 'FundPhoneCountryCode': self.getFundPhoneCountryCode(), 'FundPhoneAreaCode': self.getFundPhoneAreaCode(), 'SettlePhoneCountryCode': self.getSettlePhoneCountryCode(), 'SettlePhoneAreaCode': self.getSettlePhoneAreaCode()}


class  CShfeFtdcRiskNotifyAField(Structure):
    """客户风险通知版本A"""
    _fields_ = [
        ("SequenceNo", c_int32),
        ("EventDate", c_char*9),
        ("EventTime", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorID", c_char*13),
        ("NotifyClass", c_char),
        ("NotifyMethod", c_char),
        ("NotifyStatus", c_char),
        ("Message", c_char*257),
        ("Reserve", c_char*31),
        ("CurrencyID", c_char*4),
    ]

    def getSequenceNo(self):
        '''风险通知事件在当天的序号'''
        return self.SequenceNo

    def getEventDate(self):
        '''事件发生日期'''
        return str(self.EventDate, 'GBK')

    def getEventTime(self):
        '''事件发生时间'''
        return str(self.EventTime, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''请求发送该风险通知的用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getNotifyClass(self):
        '''通知类型'''
        return TShfeFtdcNotifyClassType(ord(self.NotifyClass))

    def getNotifyMethod(self):
        '''风险通知途径'''
        return TShfeFtdcRiskNotifyMethodType(ord(self.NotifyMethod))

    def getNotifyStatus(self):
        '''风险通知状态'''
        return TShfeFtdcRiskNotifyStatusType(ord(self.NotifyStatus))

    def getMessage(self):
        '''通知内容'''
        return str(self.Message, 'GBK')

    def getReserve(self):
        '''预留字段(人工通知-通知操作员，否则为错误原因)'''
        return str(self.Reserve, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'SequenceNo'={self.getSequenceNo()}, 'EventDate'={self.getEventDate()}, 'EventTime'={self.getEventTime()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorID'={self.getInvestorID()}, 'NotifyClass'={self.getNotifyClass()}, 'NotifyMethod'={self.getNotifyMethod()}, 'NotifyStatus'={self.getNotifyStatus()}, 'Message'={self.getMessage()}, 'Reserve'={self.getReserve()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'SequenceNo': self.getSequenceNo(), 'EventDate': self.getEventDate(), 'EventTime': self.getEventTime(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorID': self.getInvestorID(), 'NotifyClass': self.getNotifyClass(), 'NotifyMethod': self.getNotifyMethod(), 'NotifyStatus': self.getNotifyStatus(), 'Message': self.getMessage(), 'Reserve': self.getReserve(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcSeqRiskNotifyAField(Structure):
    """有序的客户风险通知版本A"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("SequenceNo", c_int32),
        ("EventDate", c_char*9),
        ("EventTime", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorID", c_char*13),
        ("NotifyClass", c_char),
        ("NotifyMethod", c_char),
        ("NotifyStatus", c_char),
        ("Message", c_char*257),
        ("Reserve", c_char*31),
        ("CurrencyID", c_char*4),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getSequenceNo(self):
        '''风险通知事件在当天的序号'''
        return self.SequenceNo

    def getEventDate(self):
        '''事件发生日期'''
        return str(self.EventDate, 'GBK')

    def getEventTime(self):
        '''事件发生时间'''
        return str(self.EventTime, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''请求发送该风险通知的用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getNotifyClass(self):
        '''通知类型'''
        return TShfeFtdcNotifyClassType(ord(self.NotifyClass))

    def getNotifyMethod(self):
        '''风险通知途径'''
        return TShfeFtdcRiskNotifyMethodType(ord(self.NotifyMethod))

    def getNotifyStatus(self):
        '''风险通知状态'''
        return TShfeFtdcRiskNotifyStatusType(ord(self.NotifyStatus))

    def getMessage(self):
        '''通知内容'''
        return str(self.Message, 'GBK')

    def getReserve(self):
        '''预留字段(人工通知-通知操作员，否则为错误原因)'''
        return str(self.Reserve, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'SequenceNo'={self.getSequenceNo()}, 'EventDate'={self.getEventDate()}, 'EventTime'={self.getEventTime()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorID'={self.getInvestorID()}, 'NotifyClass'={self.getNotifyClass()}, 'NotifyMethod'={self.getNotifyMethod()}, 'NotifyStatus'={self.getNotifyStatus()}, 'Message'={self.getMessage()}, 'Reserve'={self.getReserve()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'SequenceNo': self.getSequenceNo(), 'EventDate': self.getEventDate(), 'EventTime': self.getEventTime(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorID': self.getInvestorID(), 'NotifyClass': self.getNotifyClass(), 'NotifyMethod': self.getNotifyMethod(), 'NotifyStatus': self.getNotifyStatus(), 'Message': self.getMessage(), 'Reserve': self.getReserve(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcSeqDepositField(Structure):
    """有序的出入金"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("Type", c_char),
        ("Flag", c_char),
        ("Direction", c_char),
        ("TradingDay", c_char*9),
        ("SequenceNo", c_char*15),
        ("Time", c_char*9),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("Amount", c_double),
        ("CurrencyID", c_char*4),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getType(self):
        '''出入金类型'''
        return TShfeFtdcFundIOTypeType(ord(self.Type))

    def getFlag(self):
        '''有效标志-有效或冲正'''
        return TShfeFtdcAvailabilityFlagType(ord(self.Flag))

    def getDirection(self):
        '''出入金方向'''
        return TShfeFtdcFundDirectionType(ord(self.Direction))

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSequenceNo(self):
        '''流水号'''
        return str(self.SequenceNo, 'GBK')

    def getTime(self):
        '''时间'''
        return str(self.Time, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getAmount(self):
        '''出入金金额'''
        return self.Amount

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'Type'={self.getType()}, 'Flag'={self.getFlag()}, 'Direction'={self.getDirection()}, 'TradingDay'={self.getTradingDay()}, 'SequenceNo'={self.getSequenceNo()}, 'Time'={self.getTime()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'Amount'={self.getAmount()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'Type': self.getType(), 'Flag': self.getFlag(), 'Direction': self.getDirection(), 'TradingDay': self.getTradingDay(), 'SequenceNo': self.getSequenceNo(), 'Time': self.getTime(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'Amount': self.getAmount(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcSeqTradingCodeField(Structure):
    """有序的交易编码"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("InvestorID", c_char*13),
        ("BrokerID", c_char*11),
        ("ExchangeID", c_char*9),
        ("ClientID", c_char*11),
        ("IsActive", c_int32),
        ("Action", c_char),
        ("ClientIDType", c_char),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    def getAction(self):
        '''操作标志(修改或删除)'''
        return TShfeFtdcActionFlagType(ord(self.Action))

    def getClientIDType(self):
        '''交易编码类型'''
        return TShfeFtdcClientIDTypeType(ord(self.ClientIDType))

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'InvestorID'={self.getInvestorID()}, 'BrokerID'={self.getBrokerID()}, 'ExchangeID'={self.getExchangeID()}, 'ClientID'={self.getClientID()}, 'IsActive'={self.getIsActive()}, 'Action'={self.getAction()}, 'ClientIDType'={self.getClientIDType()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'InvestorID': self.getInvestorID(), 'BrokerID': self.getBrokerID(), 'ExchangeID': self.getExchangeID(), 'ClientID': self.getClientID(), 'IsActive': self.getIsActive(), 'Action': self.getAction(), 'ClientIDType': self.getClientIDType()}


class  CShfeFtdcRiskUserEventField(Structure):
    """风控用户操作事件"""
    _fields_ = [
        ("SequenceNo", c_int32),
        ("EventDate", c_char*9),
        ("EventTime", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("EventType", c_char),
        ("EventInfo", c_char*1025),
        ("TradingDay", c_char*9),
    ]

    def getSequenceNo(self):
        '''用户事件当天的序号'''
        return self.SequenceNo

    def getEventDate(self):
        '''事件发生日期'''
        return str(self.EventDate, 'GBK')

    def getEventTime(self):
        '''事件发生时间'''
        return str(self.EventTime, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getEventType(self):
        '''事件类型'''
        return TShfeFtdcRiskUserEventType(ord(self.EventType))

    def getEventInfo(self):
        '''事件信息'''
        return str(self.EventInfo, 'GBK')

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    @property
    def __str__(self):
        return f"'SequenceNo'={self.getSequenceNo()}, 'EventDate'={self.getEventDate()}, 'EventTime'={self.getEventTime()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'EventType'={self.getEventType()}, 'EventInfo'={self.getEventInfo()}, 'TradingDay'={self.getTradingDay()}"

    @property
    def __dict__(self):
        return {'SequenceNo': self.getSequenceNo(), 'EventDate': self.getEventDate(), 'EventTime': self.getEventTime(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'EventType': self.getEventType(), 'EventInfo': self.getEventInfo(), 'TradingDay': self.getTradingDay()}


class  CShfeFtdcRiskNtfSequenceField(Structure):
    """风控订阅序列号"""
    _fields_ = [
        ("SequenceNo", c_int32),
        ("DataType", c_char*21),
    ]

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getDataType(self):
        '''业务数据类型'''
        return str(self.DataType, 'GBK')

    @property
    def __str__(self):
        return f"'SequenceNo'={self.getSequenceNo()}, 'DataType'={self.getDataType()}"

    @property
    def __dict__(self):
        return {'SequenceNo': self.getSequenceNo(), 'DataType': self.getDataType()}


class  CShfeFtdcRiskNotifyPatternAField(Structure):
    """客户风险通知模版版本A"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("NotifyClass", c_char),
        ("NotifyMethod", c_char),
        ("IsActive", c_int32),
        ("Pattern", c_char*257),
        ("Reserve", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码，请求修改模版时有效'''
        return str(self.UserID, 'GBK')

    def getNotifyClass(self):
        '''通知类型'''
        return TShfeFtdcNotifyClassType(ord(self.NotifyClass))

    def getNotifyMethod(self):
        '''风险通知途径'''
        return TShfeFtdcRiskNotifyMethodType(ord(self.NotifyMethod))

    def getIsActive(self):
        '''是否启用'''
        return self.IsActive

    def getPattern(self):
        '''通知模版内容'''
        return str(self.Pattern, 'GBK')

    def getReserve(self):
        '''预留参数(暂时只用作warnlevel)'''
        return str(self.Reserve, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'NotifyClass'={self.getNotifyClass()}, 'NotifyMethod'={self.getNotifyMethod()}, 'IsActive'={self.getIsActive()}, 'Pattern'={self.getPattern()}, 'Reserve'={self.getReserve()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'NotifyClass': self.getNotifyClass(), 'NotifyMethod': self.getNotifyMethod(), 'IsActive': self.getIsActive(), 'Pattern': self.getPattern(), 'Reserve': self.getReserve()}


class  CShfeFtdcProductLimitsField(Structure):
    """品种停板涨跌幅"""
    _fields_ = [
        ("ProductID", c_char*31),
        ("Limit1", c_double),
        ("Limit2", c_double),
        ("Limit3", c_double),
        ("Limit4", c_double),
        ("MaxMarginRate1", c_double),
        ("Price", c_double),
    ]

    def getProductID(self):
        '''品种或合约代码'''
        return str(self.ProductID, 'GBK')

    def getLimit1(self):
        '''D1涨跌幅'''
        return self.Limit1

    def getLimit2(self):
        '''D2涨跌幅'''
        return self.Limit2

    def getLimit3(self):
        '''D3涨跌幅'''
        return self.Limit3

    def getLimit4(self):
        '''D4涨跌幅'''
        return self.Limit4

    def getMaxMarginRate1(self):
        '''最大保证金率'''
        return self.MaxMarginRate1

    def getPrice(self):
        '''结算价'''
        return self.Price

    @property
    def __str__(self):
        return f"'ProductID'={self.getProductID()}, 'Limit1'={self.getLimit1()}, 'Limit2'={self.getLimit2()}, 'Limit3'={self.getLimit3()}, 'Limit4'={self.getLimit4()}, 'MaxMarginRate1'={self.getMaxMarginRate1()}, 'Price'={self.getPrice()}"

    @property
    def __dict__(self):
        return {'ProductID': self.getProductID(), 'Limit1': self.getLimit1(), 'Limit2': self.getLimit2(), 'Limit3': self.getLimit3(), 'Limit4': self.getLimit4(), 'MaxMarginRate1': self.getMaxMarginRate1(), 'Price': self.getPrice()}


class  CShfeFtdcPredictRiskAccountField(Structure):
    """风险预算资金账户"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("Balance0", c_double),
        ("Lose1", c_double),
        ("Balance1", c_double),
        ("Lose2", c_double),
        ("Balance2", c_double),
        ("Lose3", c_double),
        ("Balance3", c_double),
        ("Lose4", c_double),
        ("Balance4", c_double),
        ("CurrencyID", c_char*4),
        ("FundMortgageIn", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBalance0(self):
        '''初始权益'''
        return self.Balance0

    def getLose1(self):
        '''D1亏损'''
        return self.Lose1

    def getBalance1(self):
        '''D1权益'''
        return self.Balance1

    def getLose2(self):
        '''D2亏损'''
        return self.Lose2

    def getBalance2(self):
        '''D2权益'''
        return self.Balance2

    def getLose3(self):
        '''D3亏损'''
        return self.Lose3

    def getBalance3(self):
        '''D3权益'''
        return self.Balance3

    def getLose4(self):
        '''D4亏损'''
        return self.Lose4

    def getBalance4(self):
        '''D4权益'''
        return self.Balance4

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getFundMortgageIn(self):
        '''货币质入金额'''
        return self.FundMortgageIn

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'Balance0'={self.getBalance0()}, 'Lose1'={self.getLose1()}, 'Balance1'={self.getBalance1()}, 'Lose2'={self.getLose2()}, 'Balance2'={self.getBalance2()}, 'Lose3'={self.getLose3()}, 'Balance3'={self.getBalance3()}, 'Lose4'={self.getLose4()}, 'Balance4'={self.getBalance4()}, 'CurrencyID'={self.getCurrencyID()}, 'FundMortgageIn'={self.getFundMortgageIn()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'Balance0': self.getBalance0(), 'Lose1': self.getLose1(), 'Balance1': self.getBalance1(), 'Lose2': self.getLose2(), 'Balance2': self.getBalance2(), 'Lose3': self.getLose3(), 'Balance3': self.getBalance3(), 'Lose4': self.getLose4(), 'Balance4': self.getBalance4(), 'CurrencyID': self.getCurrencyID(), 'FundMortgageIn': self.getFundMortgageIn()}


class  CShfeFtdcPredictRiskPositionField(Structure):
    """风险预算持仓"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("LongVol", c_int32),
        ("ShortVol", c_int32),
        ("NetVol", c_int32),
        ("Price0", c_double),
        ("Price1", c_double),
        ("Limit1", c_double),
        ("Limit2", c_double),
        ("Limit3", c_double),
        ("Limit4", c_double),
        ("Multiple", c_int32),
        ("Lose1", c_double),
        ("Lose2", c_double),
        ("Lose3", c_double),
        ("Lose4", c_double),
        ("LeftVol", c_int32),
        ("ShouldClose", c_int32),
        ("CanClose", c_int32),
        ("CurrMarginRate", c_double),
        ("MarginRate1", c_double),
        ("NetMargin1", c_double),
        ("Available1", c_double),
        ("Margin1PerVol", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getLongVol(self):
        '''多头持仓'''
        return self.LongVol

    def getShortVol(self):
        '''空头持仓'''
        return self.ShortVol

    def getNetVol(self):
        '''净持仓'''
        return self.NetVol

    def getPrice0(self):
        '''初始价格'''
        return self.Price0

    def getPrice1(self):
        '''D1结算价'''
        return self.Price1

    def getLimit1(self):
        '''D1涨跌幅'''
        return self.Limit1

    def getLimit2(self):
        '''D2涨跌幅'''
        return self.Limit2

    def getLimit3(self):
        '''D3涨跌幅'''
        return self.Limit3

    def getLimit4(self):
        '''D4涨跌幅'''
        return self.Limit4

    def getMultiple(self):
        '''合约乘数'''
        return self.Multiple

    def getLose1(self):
        '''D1亏损'''
        return self.Lose1

    def getLose2(self):
        '''D2亏损'''
        return self.Lose2

    def getLose3(self):
        '''D3亏损'''
        return self.Lose3

    def getLose4(self):
        '''D4亏损'''
        return self.Lose4

    def getLeftVol(self):
        '''可留手数'''
        return self.LeftVol

    def getShouldClose(self):
        '''D1应强平'''
        return self.ShouldClose

    def getCanClose(self):
        '''调整后可强平'''
        return self.CanClose

    def getCurrMarginRate(self):
        '''当前保证金率'''
        return self.CurrMarginRate

    def getMarginRate1(self):
        '''调整后保证金率'''
        return self.MarginRate1

    def getNetMargin1(self):
        '''净持仓保证金'''
        return self.NetMargin1

    def getAvailable1(self):
        '''D1可用'''
        return self.Available1

    def getMargin1PerVol(self):
        '''1手保证金'''
        return self.Margin1PerVol

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'LongVol'={self.getLongVol()}, 'ShortVol'={self.getShortVol()}, 'NetVol'={self.getNetVol()}, 'Price0'={self.getPrice0()}, 'Price1'={self.getPrice1()}, 'Limit1'={self.getLimit1()}, 'Limit2'={self.getLimit2()}, 'Limit3'={self.getLimit3()}, 'Limit4'={self.getLimit4()}, 'Multiple'={self.getMultiple()}, 'Lose1'={self.getLose1()}, 'Lose2'={self.getLose2()}, 'Lose3'={self.getLose3()}, 'Lose4'={self.getLose4()}, 'LeftVol'={self.getLeftVol()}, 'ShouldClose'={self.getShouldClose()}, 'CanClose'={self.getCanClose()}, 'CurrMarginRate'={self.getCurrMarginRate()}, 'MarginRate1'={self.getMarginRate1()}, 'NetMargin1'={self.getNetMargin1()}, 'Available1'={self.getAvailable1()}, 'Margin1PerVol'={self.getMargin1PerVol()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'LongVol': self.getLongVol(), 'ShortVol': self.getShortVol(), 'NetVol': self.getNetVol(), 'Price0': self.getPrice0(), 'Price1': self.getPrice1(), 'Limit1': self.getLimit1(), 'Limit2': self.getLimit2(), 'Limit3': self.getLimit3(), 'Limit4': self.getLimit4(), 'Multiple': self.getMultiple(), 'Lose1': self.getLose1(), 'Lose2': self.getLose2(), 'Lose3': self.getLose3(), 'Lose4': self.getLose4(), 'LeftVol': self.getLeftVol(), 'ShouldClose': self.getShouldClose(), 'CanClose': self.getCanClose(), 'CurrMarginRate': self.getCurrMarginRate(), 'MarginRate1': self.getMarginRate1(), 'NetMargin1': self.getNetMargin1(), 'Available1': self.getAvailable1(), 'Margin1PerVol': self.getMargin1PerVol()}


class  CShfeFtdcPredictRiskParamField(Structure):
    """风险预算参数"""
    _fields_ = [
        ("D1", c_int32),
        ("IsFilter", c_int32),
    ]

    def getD1(self):
        '''D1日期'''
        return self.D1

    def getIsFilter(self):
        '''是否过滤无效记录'''
        return self.IsFilter

    @property
    def __str__(self):
        return f"'D1'={self.getD1()}, 'IsFilter'={self.getIsFilter()}"

    @property
    def __dict__(self):
        return {'D1': self.getD1(), 'IsFilter': self.getIsFilter()}


class  CShfeFtdcRiskSyncInvestorField(Structure):
    """风控中同步投资者"""
    _fields_ = [
        ("Action", c_char),
        ("InvestorID", c_char*13),
        ("BrokerID", c_char*11),
        ("InvestorGroupID", c_char*13),
        ("InvestorName", c_char*81),
        ("IdentifiedCardType", c_char),
        ("IdentifiedCardNo", c_char*51),
        ("IsActive", c_int32),
        ("Telephone", c_char*41),
        ("Address", c_char*101),
        ("OpenDate", c_char*9),
        ("Mobile", c_char*41),
    ]

    def getAction(self):
        '''操作标志(修改或删除)'''
        return TShfeFtdcActionFlagType(ord(self.Action))

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorGroupID(self):
        '''投资者分组代码'''
        return str(self.InvestorGroupID, 'GBK')

    def getInvestorName(self):
        '''投资者名称'''
        return str(self.InvestorName, 'GBK')

    def getIdentifiedCardType(self):
        '''证件类型'''
        return TShfeFtdcIdCardTypeType(ord(self.IdentifiedCardType))

    def getIdentifiedCardNo(self):
        '''证件号码'''
        return str(self.IdentifiedCardNo, 'GBK')

    def getIsActive(self):
        '''是否活跃'''
        return self.IsActive

    def getTelephone(self):
        '''联系电话'''
        return str(self.Telephone, 'GBK')

    def getAddress(self):
        '''通讯地址'''
        return str(self.Address, 'GBK')

    def getOpenDate(self):
        '''开户日期'''
        return str(self.OpenDate, 'GBK')

    def getMobile(self):
        '''手机'''
        return str(self.Mobile, 'GBK')

    @property
    def __str__(self):
        return f"'Action'={self.getAction()}, 'InvestorID'={self.getInvestorID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorGroupID'={self.getInvestorGroupID()}, 'InvestorName'={self.getInvestorName()}, 'IdentifiedCardType'={self.getIdentifiedCardType()}, 'IdentifiedCardNo'={self.getIdentifiedCardNo()}, 'IsActive'={self.getIsActive()}, 'Telephone'={self.getTelephone()}, 'Address'={self.getAddress()}, 'OpenDate'={self.getOpenDate()}, 'Mobile'={self.getMobile()}"

    @property
    def __dict__(self):
        return {'Action': self.getAction(), 'InvestorID': self.getInvestorID(), 'BrokerID': self.getBrokerID(), 'InvestorGroupID': self.getInvestorGroupID(), 'InvestorName': self.getInvestorName(), 'IdentifiedCardType': self.getIdentifiedCardType(), 'IdentifiedCardNo': self.getIdentifiedCardNo(), 'IsActive': self.getIsActive(), 'Telephone': self.getTelephone(), 'Address': self.getAddress(), 'OpenDate': self.getOpenDate(), 'Mobile': self.getMobile()}


class  CShfeFtdcInstrumentPriceField(Structure):
    """合约价格"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("PriceType", c_char),
        ("Price", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getPriceType(self):
        '''价格类型'''
        return TShfeFtdcPriceTypeType(ord(self.PriceType))

    def getPrice(self):
        '''价格'''
        return self.Price

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'PriceType'={self.getPriceType()}, 'Price'={self.getPrice()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'PriceType': self.getPriceType(), 'Price': self.getPrice()}


class  CShfeFtdcInvestorHashField(Structure):
    """投资者与联系人信息的Hash值"""
    _fields_ = [
        ("MD5", c_char*17),
        ("InvestorIDBeg", c_char*13),
        ("InvestorIDEnd", c_char*13),
    ]

    def getMD5(self):
        '''请求中是业务类型，否则是数据MD5值'''
        return str(self.MD5, 'GBK')

    def getInvestorIDBeg(self):
        '''投资者代码(为空代表所有投资者代码)'''
        return str(self.InvestorIDBeg, 'GBK')

    def getInvestorIDEnd(self):
        '''投资者代码(为空代表所有投资者代码)'''
        return str(self.InvestorIDEnd, 'GBK')

    @property
    def __str__(self):
        return f"'MD5'={self.getMD5()}, 'InvestorIDBeg'={self.getInvestorIDBeg()}, 'InvestorIDEnd'={self.getInvestorIDEnd()}"

    @property
    def __dict__(self):
        return {'MD5': self.getMD5(), 'InvestorIDBeg': self.getInvestorIDBeg(), 'InvestorIDEnd': self.getInvestorIDEnd()}


class  CShfeFtdcInvestorIDRangeField(Structure):
    """投资者代码"""
    _fields_ = [
        ("InvestorIDBeg", c_char*13),
        ("InvestorIDEnd", c_char*13),
    ]

    def getInvestorIDBeg(self):
        '''投资者代码(为空代表所有投资者代码)'''
        return str(self.InvestorIDBeg, 'GBK')

    def getInvestorIDEnd(self):
        '''投资者代码(为空代表所有投资者代码)'''
        return str(self.InvestorIDEnd, 'GBK')

    @property
    def __str__(self):
        return f"'InvestorIDBeg'={self.getInvestorIDBeg()}, 'InvestorIDEnd'={self.getInvestorIDEnd()}"

    @property
    def __dict__(self):
        return {'InvestorIDBeg': self.getInvestorIDBeg(), 'InvestorIDEnd': self.getInvestorIDEnd()}


class  CShfeFtdcCommPhaseSequenceField(Structure):
    """带通讯时段编号的流序号"""
    _fields_ = [
        ("CommPhaseNo", c_short),
        ("SequenceSeries", c_short),
        ("SequenceNo", c_int32),
    ]

    def getCommPhaseNo(self):
        '''通讯时段编号'''
        return self.CommPhaseNo

    def getSequenceSeries(self):
        '''序列系列号'''
        return self.SequenceSeries

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    @property
    def __str__(self):
        return f"'CommPhaseNo'={self.getCommPhaseNo()}, 'SequenceSeries'={self.getSequenceSeries()}, 'SequenceNo'={self.getSequenceNo()}"

    @property
    def __dict__(self):
        return {'CommPhaseNo': self.getCommPhaseNo(), 'SequenceSeries': self.getSequenceSeries(), 'SequenceNo': self.getSequenceNo()}


class  CShfeFtdcRiskUserFunctionField(Structure):
    """风控用户权限"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("Function", c_char*25),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getFunction(self):
        '''权限名称'''
        return str(self.Function, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'Function'={self.getFunction()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'Function': self.getFunction()}


class  CShfeFtdcLinkStatusField(Structure):
    """连接状态"""
    _fields_ = [
        ("LinkStatus", c_char),
    ]

    def getLinkStatus(self):
        '''连接状态'''
        return TShfeFtdcLinkStatusType(ord(self.LinkStatus))

    @property
    def __str__(self):
        return f"'LinkStatus'={self.getLinkStatus()}"

    @property
    def __dict__(self):
        return {'LinkStatus': self.getLinkStatus()}


class  CShfeFtdcRiskSyncAccountField(Structure):
    """风控同步投资者资金账户"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("Withdraw", c_double),
        ("CurrMargin", c_double),
        ("Commission", c_double),
        ("CloseProfit", c_double),
        ("PositionProfit", c_double),
        ("Balance", c_double),
        ("Available", c_double),
        ("Mortgage", c_double),
        ("ExchangeMargin", c_double),
        ("WithdrawQuota", c_double),
        ("Credit", c_double),
        ("FrozenMargin", c_double),
        ("FrozenCommission", c_double),
        ("CurrencyID", c_char*4),
        ("Deposit", c_double),
        ("TradingPositionProfit", c_double),
        ("FundMortgageIn", c_double),
        ("FundMortgageOut", c_double),
        ("FundMortgageAvailable", c_double),
        ("MortgageableFund", c_double),
        ("SpecProductExchangeMargin", c_double),
        ("SpecProductFrozenMargin", c_double),
        ("SpecProductMargin", c_double),
        ("SpecProductCommission", c_double),
        ("SpecProductFrozenCommission", c_double),
        ("SpecProductPositionProfit", c_double),
        ("SpecProductCloseProfit", c_double),
        ("SpecProductPositionProfitByAlg", c_double),
        ("FrozenMarginOnMortgage", c_double),
        ("MarginOnMortgage", c_double),
        ("ExchMarginOnMortgage", c_double),
        ("FrozenCommissionOnMortgage", c_double),
        ("PositionProfitOnMortgage", c_double),
        ("CommissionOnMortgage", c_double),
        ("CloseProfitOnMortgage", c_double),
        ("OptionCloseProfit", c_double),
        ("OptionValue", c_double),
        ("FrozenCash", c_double),
        ("CashIn", c_double),
        ("MaintCurrMargin", c_double),
        ("MaintExchangeMargin", c_double),
        ("FixedMargin", c_double),
        ("ExchFixedMargin", c_double),
        ("FrozenSwap", c_double),
        ("RemainSwap", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getWithdraw(self):
        '''出金金额'''
        return self.Withdraw

    def getCurrMargin(self):
        '''当前保证金总额'''
        return self.CurrMargin

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getBalance(self):
        '''总权益'''
        return self.Balance

    def getAvailable(self):
        '''可用资金'''
        return self.Available

    def getMortgage(self):
        '''质押金额'''
        return self.Mortgage

    def getExchangeMargin(self):
        '''交易所保证金'''
        return self.ExchangeMargin

    def getWithdrawQuota(self):
        '''可取资金'''
        return self.WithdrawQuota

    def getCredit(self):
        '''信用额度'''
        return self.Credit

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getDeposit(self):
        '''入金金额'''
        return self.Deposit

    def getTradingPositionProfit(self):
        '''交易持仓盈亏'''
        return self.TradingPositionProfit

    def getFundMortgageIn(self):
        '''货币质入金额'''
        return self.FundMortgageIn

    def getFundMortgageOut(self):
        '''货币质出金额'''
        return self.FundMortgageOut

    def getFundMortgageAvailable(self):
        '''货币质押余额'''
        return self.FundMortgageAvailable

    def getMortgageableFund(self):
        '''可质押货币金额'''
        return self.MortgageableFund

    def getSpecProductExchangeMargin(self):
        '''特殊品种交易所占用保证金'''
        return self.SpecProductExchangeMargin

    def getSpecProductFrozenMargin(self):
        '''特殊产品冻结保证金'''
        return self.SpecProductFrozenMargin

    def getSpecProductMargin(self):
        '''特殊产品占用保证金'''
        return self.SpecProductMargin

    def getSpecProductCommission(self):
        '''特殊产品手续费'''
        return self.SpecProductCommission

    def getSpecProductFrozenCommission(self):
        '''特殊产品冻结手续费'''
        return self.SpecProductFrozenCommission

    def getSpecProductPositionProfit(self):
        '''特殊产品持仓盈亏'''
        return self.SpecProductPositionProfit

    def getSpecProductCloseProfit(self):
        '''特殊产品平仓盈亏'''
        return self.SpecProductCloseProfit

    def getSpecProductPositionProfitByAlg(self):
        '''根据持仓盈亏算法计算的特殊产品持仓盈亏'''
        return self.SpecProductPositionProfitByAlg

    def getFrozenMarginOnMortgage(self):
        '''算在质押上的保证金冻结'''
        return self.FrozenMarginOnMortgage

    def getMarginOnMortgage(self):
        '''算在质押上的保证金'''
        return self.MarginOnMortgage

    def getExchMarginOnMortgage(self):
        '''算在质押上的交易所保证金'''
        return self.ExchMarginOnMortgage

    def getFrozenCommissionOnMortgage(self):
        '''算在质押上的冻结手续费'''
        return self.FrozenCommissionOnMortgage

    def getPositionProfitOnMortgage(self):
        '''算在质押上的持仓盈亏'''
        return self.PositionProfitOnMortgage

    def getCommissionOnMortgage(self):
        '''算在质押上的手续费'''
        return self.CommissionOnMortgage

    def getCloseProfitOnMortgage(self):
        '''算在质押上的平仓盈亏'''
        return self.CloseProfitOnMortgage

    def getOptionCloseProfit(self):
        '''期权平仓盈亏'''
        return self.OptionCloseProfit

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getMaintCurrMargin(self):
        '''维持保证金总额'''
        return self.MaintCurrMargin

    def getMaintExchangeMargin(self):
        '''交易所维持保证金'''
        return self.MaintExchangeMargin

    def getFixedMargin(self):
        '''昨结算价计算的期权保证金'''
        return self.FixedMargin

    def getExchFixedMargin(self):
        '''昨结算价计算的交易所期权保证金'''
        return self.ExchFixedMargin

    def getFrozenSwap(self):
        '''延时换汇冻结金额'''
        return self.FrozenSwap

    def getRemainSwap(self):
        '''剩余换汇额度'''
        return self.RemainSwap

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'Withdraw'={self.getWithdraw()}, 'CurrMargin'={self.getCurrMargin()}, 'Commission'={self.getCommission()}, 'CloseProfit'={self.getCloseProfit()}, 'PositionProfit'={self.getPositionProfit()}, 'Balance'={self.getBalance()}, 'Available'={self.getAvailable()}, 'Mortgage'={self.getMortgage()}, 'ExchangeMargin'={self.getExchangeMargin()}, 'WithdrawQuota'={self.getWithdrawQuota()}, 'Credit'={self.getCredit()}, 'FrozenMargin'={self.getFrozenMargin()}, 'FrozenCommission'={self.getFrozenCommission()}, 'CurrencyID'={self.getCurrencyID()}, 'Deposit'={self.getDeposit()}, 'TradingPositionProfit'={self.getTradingPositionProfit()}, 'FundMortgageIn'={self.getFundMortgageIn()}, 'FundMortgageOut'={self.getFundMortgageOut()}, 'FundMortgageAvailable'={self.getFundMortgageAvailable()}, 'MortgageableFund'={self.getMortgageableFund()}, 'SpecProductExchangeMargin'={self.getSpecProductExchangeMargin()}, 'SpecProductFrozenMargin'={self.getSpecProductFrozenMargin()}, 'SpecProductMargin'={self.getSpecProductMargin()}, 'SpecProductCommission'={self.getSpecProductCommission()}, 'SpecProductFrozenCommission'={self.getSpecProductFrozenCommission()}, 'SpecProductPositionProfit'={self.getSpecProductPositionProfit()}, 'SpecProductCloseProfit'={self.getSpecProductCloseProfit()}, 'SpecProductPositionProfitByAlg'={self.getSpecProductPositionProfitByAlg()}, 'FrozenMarginOnMortgage'={self.getFrozenMarginOnMortgage()}, 'MarginOnMortgage'={self.getMarginOnMortgage()}, 'ExchMarginOnMortgage'={self.getExchMarginOnMortgage()}, 'FrozenCommissionOnMortgage'={self.getFrozenCommissionOnMortgage()}, 'PositionProfitOnMortgage'={self.getPositionProfitOnMortgage()}, 'CommissionOnMortgage'={self.getCommissionOnMortgage()}, 'CloseProfitOnMortgage'={self.getCloseProfitOnMortgage()}, 'OptionCloseProfit'={self.getOptionCloseProfit()}, 'OptionValue'={self.getOptionValue()}, 'FrozenCash'={self.getFrozenCash()}, 'CashIn'={self.getCashIn()}, 'MaintCurrMargin'={self.getMaintCurrMargin()}, 'MaintExchangeMargin'={self.getMaintExchangeMargin()}, 'FixedMargin'={self.getFixedMargin()}, 'ExchFixedMargin'={self.getExchFixedMargin()}, 'FrozenSwap'={self.getFrozenSwap()}, 'RemainSwap'={self.getRemainSwap()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'Withdraw': self.getWithdraw(), 'CurrMargin': self.getCurrMargin(), 'Commission': self.getCommission(), 'CloseProfit': self.getCloseProfit(), 'PositionProfit': self.getPositionProfit(), 'Balance': self.getBalance(), 'Available': self.getAvailable(), 'Mortgage': self.getMortgage(), 'ExchangeMargin': self.getExchangeMargin(), 'WithdrawQuota': self.getWithdrawQuota(), 'Credit': self.getCredit(), 'FrozenMargin': self.getFrozenMargin(), 'FrozenCommission': self.getFrozenCommission(), 'CurrencyID': self.getCurrencyID(), 'Deposit': self.getDeposit(), 'TradingPositionProfit': self.getTradingPositionProfit(), 'FundMortgageIn': self.getFundMortgageIn(), 'FundMortgageOut': self.getFundMortgageOut(), 'FundMortgageAvailable': self.getFundMortgageAvailable(), 'MortgageableFund': self.getMortgageableFund(), 'SpecProductExchangeMargin': self.getSpecProductExchangeMargin(), 'SpecProductFrozenMargin': self.getSpecProductFrozenMargin(), 'SpecProductMargin': self.getSpecProductMargin(), 'SpecProductCommission': self.getSpecProductCommission(), 'SpecProductFrozenCommission': self.getSpecProductFrozenCommission(), 'SpecProductPositionProfit': self.getSpecProductPositionProfit(), 'SpecProductCloseProfit': self.getSpecProductCloseProfit(), 'SpecProductPositionProfitByAlg': self.getSpecProductPositionProfitByAlg(), 'FrozenMarginOnMortgage': self.getFrozenMarginOnMortgage(), 'MarginOnMortgage': self.getMarginOnMortgage(), 'ExchMarginOnMortgage': self.getExchMarginOnMortgage(), 'FrozenCommissionOnMortgage': self.getFrozenCommissionOnMortgage(), 'PositionProfitOnMortgage': self.getPositionProfitOnMortgage(), 'CommissionOnMortgage': self.getCommissionOnMortgage(), 'CloseProfitOnMortgage': self.getCloseProfitOnMortgage(), 'OptionCloseProfit': self.getOptionCloseProfit(), 'OptionValue': self.getOptionValue(), 'FrozenCash': self.getFrozenCash(), 'CashIn': self.getCashIn(), 'MaintCurrMargin': self.getMaintCurrMargin(), 'MaintExchangeMargin': self.getMaintExchangeMargin(), 'FixedMargin': self.getFixedMargin(), 'ExchFixedMargin': self.getExchFixedMargin(), 'FrozenSwap': self.getFrozenSwap(), 'RemainSwap': self.getRemainSwap()}


class  CShfeFtdcSeqPreRiskAccountField(Structure):
    """风控资金账户昨日信息"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("AccountID", c_char*13),
        ("PreMortgage", c_double),
        ("PreCredit", c_double),
        ("PreDeposit", c_double),
        ("PreBalance", c_double),
        ("PreMargin", c_double),
        ("Reserve", c_double),
        ("PreExchMargin", c_double),
        ("ForceCloseStat", c_int32),
        ("DeliveryMargin", c_double),
        ("ExchangeDeliveryMargin", c_double),
        ("CurrencyID", c_char*4),
        ("PreSpecProductMargin", c_double),
        ("PreSpecProductExchangeMargin", c_double),
        ("PreMarginOnMortgage", c_double),
        ("PreExchMarginOnMortgage", c_double),
        ("PreFundMortgageIn", c_double),
        ("PreFundMortgageOut", c_double),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getPreMortgage(self):
        '''上次质押金额'''
        return self.PreMortgage

    def getPreCredit(self):
        '''上次信用额度'''
        return self.PreCredit

    def getPreDeposit(self):
        '''上次存款额'''
        return self.PreDeposit

    def getPreBalance(self):
        '''上次总权益'''
        return self.PreBalance

    def getPreMargin(self):
        '''上次占用的保证金'''
        return self.PreMargin

    def getReserve(self):
        '''基本准备金'''
        return self.Reserve

    def getPreExchMargin(self):
        '''上次交易所保证金'''
        return self.PreExchMargin

    def getForceCloseStat(self):
        '''历史强平次数'''
        return self.ForceCloseStat

    def getDeliveryMargin(self):
        '''投资者交割保证金'''
        return self.DeliveryMargin

    def getExchangeDeliveryMargin(self):
        '''交易所交割保证金'''
        return self.ExchangeDeliveryMargin

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getPreSpecProductMargin(self):
        '''上次特殊产品占用交易所保证金'''
        return self.PreSpecProductMargin

    def getPreSpecProductExchangeMargin(self):
        '''上次特殊产品占用保证金'''
        return self.PreSpecProductExchangeMargin

    def getPreMarginOnMortgage(self):
        '''上一交易日算在质押上的保证金'''
        return self.PreMarginOnMortgage

    def getPreExchMarginOnMortgage(self):
        '''上一交易日算在质押上的交易所保证金'''
        return self.PreExchMarginOnMortgage

    def getPreFundMortgageIn(self):
        '''上次货币质入金额'''
        return self.PreFundMortgageIn

    def getPreFundMortgageOut(self):
        '''上次货币质入金额'''
        return self.PreFundMortgageOut

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'AccountID'={self.getAccountID()}, 'PreMortgage'={self.getPreMortgage()}, 'PreCredit'={self.getPreCredit()}, 'PreDeposit'={self.getPreDeposit()}, 'PreBalance'={self.getPreBalance()}, 'PreMargin'={self.getPreMargin()}, 'Reserve'={self.getReserve()}, 'PreExchMargin'={self.getPreExchMargin()}, 'ForceCloseStat'={self.getForceCloseStat()}, 'DeliveryMargin'={self.getDeliveryMargin()}, 'ExchangeDeliveryMargin'={self.getExchangeDeliveryMargin()}, 'CurrencyID'={self.getCurrencyID()}, 'PreSpecProductMargin'={self.getPreSpecProductMargin()}, 'PreSpecProductExchangeMargin'={self.getPreSpecProductExchangeMargin()}, 'PreMarginOnMortgage'={self.getPreMarginOnMortgage()}, 'PreExchMarginOnMortgage'={self.getPreExchMarginOnMortgage()}, 'PreFundMortgageIn'={self.getPreFundMortgageIn()}, 'PreFundMortgageOut'={self.getPreFundMortgageOut()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'AccountID': self.getAccountID(), 'PreMortgage': self.getPreMortgage(), 'PreCredit': self.getPreCredit(), 'PreDeposit': self.getPreDeposit(), 'PreBalance': self.getPreBalance(), 'PreMargin': self.getPreMargin(), 'Reserve': self.getReserve(), 'PreExchMargin': self.getPreExchMargin(), 'ForceCloseStat': self.getForceCloseStat(), 'DeliveryMargin': self.getDeliveryMargin(), 'ExchangeDeliveryMargin': self.getExchangeDeliveryMargin(), 'CurrencyID': self.getCurrencyID(), 'PreSpecProductMargin': self.getPreSpecProductMargin(), 'PreSpecProductExchangeMargin': self.getPreSpecProductExchangeMargin(), 'PreMarginOnMortgage': self.getPreMarginOnMortgage(), 'PreExchMarginOnMortgage': self.getPreExchMarginOnMortgage(), 'PreFundMortgageIn': self.getPreFundMortgageIn(), 'PreFundMortgageOut': self.getPreFundMortgageOut()}


class  CShfeFtdcRspLocalFrontLoginField(Structure):
    """查询服务器登录应答"""
    _fields_ = [
        ("CommPhaseNo", c_short),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("FrontID", c_int32),
        ("FrontSessionID", c_int32),
    ]

    def getCommPhaseNo(self):
        '''通讯时段编号'''
        return self.CommPhaseNo

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getFrontSessionID(self):
        '''风控前置中连接的SessionID'''
        return self.FrontSessionID

    @property
    def __str__(self):
        return f"'CommPhaseNo'={self.getCommPhaseNo()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'FrontID'={self.getFrontID()}, 'FrontSessionID'={self.getFrontSessionID()}"

    @property
    def __dict__(self):
        return {'CommPhaseNo': self.getCommPhaseNo(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'FrontID': self.getFrontID(), 'FrontSessionID': self.getFrontSessionID()}


class  CShfeFtdcNoticeTokenField(Structure):
    """模板替换字段"""
    _fields_ = [
        ("Token", c_char*61),
        ("Description", c_char*81),
    ]

    def getToken(self):
        '''自动替换字段'''
        return str(self.Token, 'GBK')

    def getDescription(self):
        '''自动替换字段的描述'''
        return str(self.Description, 'GBK')

    @property
    def __str__(self):
        return f"'Token'={self.getToken()}, 'Description'={self.getDescription()}"

    @property
    def __dict__(self):
        return {'Token': self.getToken(), 'Description': self.getDescription()}


class  CShfeFtdcNoticePatternField(Structure):
    """通知模板"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("BizType", c_char*41),
        ("Method", c_char),
        ("BizName", c_char*41),
        ("UserID", c_char*16),
        ("IsActive", c_int32),
        ("Pattern", c_char*501),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getBizType(self):
        '''业务类型'''
        return str(self.BizType, 'GBK')

    def getMethod(self):
        '''通知途径'''
        return TShfeFtdcRiskNotifyMethodType(ord(self.Method))

    def getBizName(self):
        '''业务名称'''
        return str(self.BizName, 'GBK')

    def getUserID(self):
        '''最近修改模版的用户代码'''
        return str(self.UserID, 'GBK')

    def getIsActive(self):
        '''是否启用'''
        return self.IsActive

    def getPattern(self):
        '''通知模版内容'''
        return str(self.Pattern, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'BizType'={self.getBizType()}, 'Method'={self.getMethod()}, 'BizName'={self.getBizName()}, 'UserID'={self.getUserID()}, 'IsActive'={self.getIsActive()}, 'Pattern'={self.getPattern()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'BizType': self.getBizType(), 'Method': self.getMethod(), 'BizName': self.getBizName(), 'UserID': self.getUserID(), 'IsActive': self.getIsActive(), 'Pattern': self.getPattern()}


class  CShfeFtdcBizNoticeField(Structure):
    """业务通知"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("SequenceNo", c_int32),
        ("Method", c_char),
        ("EventTime", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorID", c_char*13),
        ("BizType", c_char*41),
        ("Status", c_char),
        ("Message", c_char*501),
        ("ErrorMsg", c_char*81),
    ]

    def getTradingDay(self):
        '''事件发生日期'''
        return str(self.TradingDay, 'GBK')

    def getSequenceNo(self):
        '''通知事件在当天的序号'''
        return self.SequenceNo

    def getMethod(self):
        '''风险通知途径'''
        return TShfeFtdcRiskNotifyMethodType(ord(self.Method))

    def getEventTime(self):
        '''事件发生时间'''
        return str(self.EventTime, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBizType(self):
        '''业务类型'''
        return str(self.BizType, 'GBK')

    def getStatus(self):
        '''通知状态'''
        return TShfeFtdcRiskNotifyStatusType(ord(self.Status))

    def getMessage(self):
        '''通知内容'''
        return str(self.Message, 'GBK')

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'SequenceNo'={self.getSequenceNo()}, 'Method'={self.getMethod()}, 'EventTime'={self.getEventTime()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorID'={self.getInvestorID()}, 'BizType'={self.getBizType()}, 'Status'={self.getStatus()}, 'Message'={self.getMessage()}, 'ErrorMsg'={self.getErrorMsg()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'SequenceNo': self.getSequenceNo(), 'Method': self.getMethod(), 'EventTime': self.getEventTime(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorID': self.getInvestorID(), 'BizType': self.getBizType(), 'Status': self.getStatus(), 'Message': self.getMessage(), 'ErrorMsg': self.getErrorMsg()}


class  CShfeFtdcRiskInvestorParamField(Structure):
    """投资者参数"""
    _fields_ = [
        ("ParamID", c_int32),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("ParamValue", c_char*41),
    ]

    def getParamID(self):
        '''参数代码'''
        return self.ParamID

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getParamValue(self):
        '''参数值'''
        return str(self.ParamValue, 'GBK')

    @property
    def __str__(self):
        return f"'ParamID'={self.getParamID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'ParamValue'={self.getParamValue()}"

    @property
    def __dict__(self):
        return {'ParamID': self.getParamID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'ParamValue': self.getParamValue()}


class  CShfeFtdcVaryMarketDataField(Structure):
    """变化行情"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("LastPrice", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getLastPrice(self):
        '''最新价'''
        return self.LastPrice

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'LastPrice'={self.getLastPrice()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'LastPrice': self.getLastPrice()}


class  CShfeFtdcPriceRangeField(Structure):
    """合约价格区间"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("Price1", c_double),
        ("Price2", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getPrice1(self):
        '''价格1'''
        return self.Price1

    def getPrice2(self):
        '''价格2'''
        return self.Price2

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'Price1'={self.getPrice1()}, 'Price2'={self.getPrice2()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'Price1': self.getPrice1(), 'Price2': self.getPrice2()}


class  CShfeFtdcSeqBizNoticeField(Structure):
    """有序的业务通知"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("TradingDay", c_char*9),
        ("SequenceNo", c_int32),
        ("Method", c_char),
        ("EventTime", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorID", c_char*13),
        ("BizType", c_char*41),
        ("Status", c_char),
        ("Message", c_char*501),
        ("ErrorMsg", c_char*81),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getTradingDay(self):
        '''事件发生日期'''
        return str(self.TradingDay, 'GBK')

    def getSequenceNo(self):
        '''通知事件在当天的序号'''
        return self.SequenceNo

    def getMethod(self):
        '''风险通知途径'''
        return TShfeFtdcRiskNotifyMethodType(ord(self.Method))

    def getEventTime(self):
        '''事件发生时间'''
        return str(self.EventTime, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBizType(self):
        '''业务类型'''
        return str(self.BizType, 'GBK')

    def getStatus(self):
        '''通知状态'''
        return TShfeFtdcRiskNotifyStatusType(ord(self.Status))

    def getMessage(self):
        '''通知内容'''
        return str(self.Message, 'GBK')

    def getErrorMsg(self):
        '''错误信息'''
        return str(self.ErrorMsg, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'TradingDay'={self.getTradingDay()}, 'SequenceNo'={self.getSequenceNo()}, 'Method'={self.getMethod()}, 'EventTime'={self.getEventTime()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorID'={self.getInvestorID()}, 'BizType'={self.getBizType()}, 'Status'={self.getStatus()}, 'Message'={self.getMessage()}, 'ErrorMsg'={self.getErrorMsg()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'TradingDay': self.getTradingDay(), 'SequenceNo': self.getSequenceNo(), 'Method': self.getMethod(), 'EventTime': self.getEventTime(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorID': self.getInvestorID(), 'BizType': self.getBizType(), 'Status': self.getStatus(), 'Message': self.getMessage(), 'ErrorMsg': self.getErrorMsg()}


class  CShfeFtdcRiskParamInfoField(Structure):
    """风控参数信息"""
    _fields_ = [
        ("ParamID", c_int32),
        ("Description", c_char*401),
    ]

    def getParamID(self):
        '''参数代码'''
        return self.ParamID

    def getDescription(self):
        '''参数说明'''
        return str(self.Description, 'GBK')

    @property
    def __str__(self):
        return f"'ParamID'={self.getParamID()}, 'Description'={self.getDescription()}"

    @property
    def __dict__(self):
        return {'ParamID': self.getParamID(), 'Description': self.getDescription()}


class  CShfeFtdcRiskLoginInfoField(Structure):
    """风控登录信息"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("LocalSessionID", c_int32),
        ("SessionID", c_int32),
        ("FrontID", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getLocalSessionID(self):
        '''本地前置会话编号'''
        return self.LocalSessionID

    def getSessionID(self):
        '''风控前置会话编号'''
        return self.SessionID

    def getFrontID(self):
        '''风控前置编号'''
        return self.FrontID

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'LocalSessionID'={self.getLocalSessionID()}, 'SessionID'={self.getSessionID()}, 'FrontID'={self.getFrontID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'LocalSessionID': self.getLocalSessionID(), 'SessionID': self.getSessionID(), 'FrontID': self.getFrontID()}


class  CShfeFtdcRiskPatternField(Structure):
    """风控通知模板"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("BizType", c_char*41),
        ("PatternID", c_int32),
        ("PatternName", c_char*41),
        ("Pattern", c_char*501),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getBizType(self):
        '''业务类型'''
        return str(self.BizType, 'GBK')

    def getPatternID(self):
        '''模板代码'''
        return self.PatternID

    def getPatternName(self):
        '''模板名称'''
        return str(self.PatternName, 'GBK')

    def getPattern(self):
        '''通知模版内容'''
        return str(self.Pattern, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'BizType'={self.getBizType()}, 'PatternID'={self.getPatternID()}, 'PatternName'={self.getPatternName()}, 'Pattern'={self.getPattern()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'BizType': self.getBizType(), 'PatternID': self.getPatternID(), 'PatternName': self.getPatternName(), 'Pattern': self.getPattern()}


class  CShfeFtdcInvestorPatternField(Structure):
    """投资者通知模板"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("BizType", c_char*41),
        ("Method", c_char),
        ("PatternID", c_int32),
        ("IsActive", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBizType(self):
        '''业务类型'''
        return str(self.BizType, 'GBK')

    def getMethod(self):
        '''通知途径'''
        return TShfeFtdcRiskNotifyMethodType(ord(self.Method))

    def getPatternID(self):
        '''模板代码'''
        return self.PatternID

    def getIsActive(self):
        '''是否启用'''
        return self.IsActive

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'BizType'={self.getBizType()}, 'Method'={self.getMethod()}, 'PatternID'={self.getPatternID()}, 'IsActive'={self.getIsActive()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'BizType': self.getBizType(), 'Method': self.getMethod(), 'PatternID': self.getPatternID(), 'IsActive': self.getIsActive()}


class  CShfeFtdcRiskNotifyBField(Structure):
    """客户风险通知版本B"""
    _fields_ = [
        ("SequenceNo", c_int32),
        ("EventDate", c_char*9),
        ("EventTime", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorID", c_char*13),
        ("NotifyClass", c_char),
        ("NotifyMethod", c_char),
        ("NotifyStatus", c_char),
        ("Message", c_char*501),
        ("Reserve", c_char*31),
        ("TradingDay", c_char*9),
        ("CurrencyID", c_char*4),
    ]

    def getSequenceNo(self):
        '''风险通知事件在当天的序号'''
        return self.SequenceNo

    def getEventDate(self):
        '''事件发生日期'''
        return str(self.EventDate, 'GBK')

    def getEventTime(self):
        '''事件发生时间'''
        return str(self.EventTime, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''请求发送该风险通知的用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getNotifyClass(self):
        '''通知类型'''
        return TShfeFtdcNotifyClassType(ord(self.NotifyClass))

    def getNotifyMethod(self):
        '''风险通知途径'''
        return TShfeFtdcRiskNotifyMethodType(ord(self.NotifyMethod))

    def getNotifyStatus(self):
        '''风险通知状态'''
        return TShfeFtdcRiskNotifyStatusType(ord(self.NotifyStatus))

    def getMessage(self):
        '''通知内容'''
        return str(self.Message, 'GBK')

    def getReserve(self):
        '''预留字段(人工通知-通知操作员，否则为错误原因)'''
        return str(self.Reserve, 'GBK')

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'SequenceNo'={self.getSequenceNo()}, 'EventDate'={self.getEventDate()}, 'EventTime'={self.getEventTime()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorID'={self.getInvestorID()}, 'NotifyClass'={self.getNotifyClass()}, 'NotifyMethod'={self.getNotifyMethod()}, 'NotifyStatus'={self.getNotifyStatus()}, 'Message'={self.getMessage()}, 'Reserve'={self.getReserve()}, 'TradingDay'={self.getTradingDay()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'SequenceNo': self.getSequenceNo(), 'EventDate': self.getEventDate(), 'EventTime': self.getEventTime(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorID': self.getInvestorID(), 'NotifyClass': self.getNotifyClass(), 'NotifyMethod': self.getNotifyMethod(), 'NotifyStatus': self.getNotifyStatus(), 'Message': self.getMessage(), 'Reserve': self.getReserve(), 'TradingDay': self.getTradingDay(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcSeqRiskNotifyBField(Structure):
    """有序的客户风险通知版本B"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("SequenceNo", c_int32),
        ("EventDate", c_char*9),
        ("EventTime", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorID", c_char*13),
        ("NotifyClass", c_char),
        ("NotifyMethod", c_char),
        ("NotifyStatus", c_char),
        ("Message", c_char*501),
        ("Reserve", c_char*31),
        ("TradingDay", c_char*9),
        ("CurrencyID", c_char*4),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getSequenceNo(self):
        '''风险通知事件在当天的序号'''
        return self.SequenceNo

    def getEventDate(self):
        '''事件发生日期'''
        return str(self.EventDate, 'GBK')

    def getEventTime(self):
        '''事件发生时间'''
        return str(self.EventTime, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''请求发送该风险通知的用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getNotifyClass(self):
        '''通知类型'''
        return TShfeFtdcNotifyClassType(ord(self.NotifyClass))

    def getNotifyMethod(self):
        '''风险通知途径'''
        return TShfeFtdcRiskNotifyMethodType(ord(self.NotifyMethod))

    def getNotifyStatus(self):
        '''风险通知状态'''
        return TShfeFtdcRiskNotifyStatusType(ord(self.NotifyStatus))

    def getMessage(self):
        '''通知内容'''
        return str(self.Message, 'GBK')

    def getReserve(self):
        '''预留字段(人工通知-通知操作员，否则为错误原因)'''
        return str(self.Reserve, 'GBK')

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'SequenceNo'={self.getSequenceNo()}, 'EventDate'={self.getEventDate()}, 'EventTime'={self.getEventTime()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorID'={self.getInvestorID()}, 'NotifyClass'={self.getNotifyClass()}, 'NotifyMethod'={self.getNotifyMethod()}, 'NotifyStatus'={self.getNotifyStatus()}, 'Message'={self.getMessage()}, 'Reserve'={self.getReserve()}, 'TradingDay'={self.getTradingDay()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'SequenceNo': self.getSequenceNo(), 'EventDate': self.getEventDate(), 'EventTime': self.getEventTime(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorID': self.getInvestorID(), 'NotifyClass': self.getNotifyClass(), 'NotifyMethod': self.getNotifyMethod(), 'NotifyStatus': self.getNotifyStatus(), 'Message': self.getMessage(), 'Reserve': self.getReserve(), 'TradingDay': self.getTradingDay(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcQryStatField(Structure):
    """查询持仓成交报排名的参数"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("ExchangeProductInstID", c_char*100),
        ("SortType", c_char),
        ("ResultCount", c_int32),
        ("ResultRatio", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getExchangeProductInstID(self):
        '''交易所品种合约代码组合(交易所代码使用前缀e:，格式如cu,e:SHFE,cu1105)'''
        return str(self.ExchangeProductInstID, 'GBK')

    def getSortType(self):
        '''排名类型'''
        return TShfeFtdcStatSortTypeType(ord(self.SortType))

    def getResultCount(self):
        '''按排名数返回结果'''
        return self.ResultCount

    def getResultRatio(self):
        '''按比例返回结果'''
        return self.ResultRatio

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'ExchangeProductInstID'={self.getExchangeProductInstID()}, 'SortType'={self.getSortType()}, 'ResultCount'={self.getResultCount()}, 'ResultRatio'={self.getResultRatio()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'ExchangeProductInstID': self.getExchangeProductInstID(), 'SortType': self.getSortType(), 'ResultCount': self.getResultCount(), 'ResultRatio': self.getResultRatio()}


class  CShfeFtdcPositionStatField(Structure):
    """持仓排名统计"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("ExchangeProductInstID", c_char*100),
        ("InvestorID", c_char*13),
        ("YdPosition", c_int32),
        ("Position", c_int32),
        ("LongPosition", c_int32),
        ("ShortPosition", c_int32),
        ("NetPosition", c_int32),
        ("SpecuLongPosi", c_int32),
        ("SpecuShortPosi", c_int32),
        ("HedgeLongPosi", c_int32),
        ("HedgeShortPosi", c_int32),
        ("TodayPosition", c_int32),
        ("PositionCost", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getExchangeProductInstID(self):
        '''交易所品种合约代码组合(交易所代码使用前缀e:，格式如cu,e:SHFE,cu1105)'''
        return str(self.ExchangeProductInstID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getYdPosition(self):
        '''昨持仓'''
        return self.YdPosition

    def getPosition(self):
        '''总持仓'''
        return self.Position

    def getLongPosition(self):
        '''多头持仓'''
        return self.LongPosition

    def getShortPosition(self):
        '''空头持仓'''
        return self.ShortPosition

    def getNetPosition(self):
        '''净持仓'''
        return self.NetPosition

    def getSpecuLongPosi(self):
        '''投机多头持仓'''
        return self.SpecuLongPosi

    def getSpecuShortPosi(self):
        '''投机空头持仓'''
        return self.SpecuShortPosi

    def getHedgeLongPosi(self):
        '''保值多头持仓'''
        return self.HedgeLongPosi

    def getHedgeShortPosi(self):
        '''保值空头持仓'''
        return self.HedgeShortPosi

    def getTodayPosition(self):
        '''今仓'''
        return self.TodayPosition

    def getPositionCost(self):
        '''总持仓成本'''
        return self.PositionCost

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'ExchangeProductInstID'={self.getExchangeProductInstID()}, 'InvestorID'={self.getInvestorID()}, 'YdPosition'={self.getYdPosition()}, 'Position'={self.getPosition()}, 'LongPosition'={self.getLongPosition()}, 'ShortPosition'={self.getShortPosition()}, 'NetPosition'={self.getNetPosition()}, 'SpecuLongPosi'={self.getSpecuLongPosi()}, 'SpecuShortPosi'={self.getSpecuShortPosi()}, 'HedgeLongPosi'={self.getHedgeLongPosi()}, 'HedgeShortPosi'={self.getHedgeShortPosi()}, 'TodayPosition'={self.getTodayPosition()}, 'PositionCost'={self.getPositionCost()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'ExchangeProductInstID': self.getExchangeProductInstID(), 'InvestorID': self.getInvestorID(), 'YdPosition': self.getYdPosition(), 'Position': self.getPosition(), 'LongPosition': self.getLongPosition(), 'ShortPosition': self.getShortPosition(), 'NetPosition': self.getNetPosition(), 'SpecuLongPosi': self.getSpecuLongPosi(), 'SpecuShortPosi': self.getSpecuShortPosi(), 'HedgeLongPosi': self.getHedgeLongPosi(), 'HedgeShortPosi': self.getHedgeShortPosi(), 'TodayPosition': self.getTodayPosition(), 'PositionCost': self.getPositionCost()}


class  CShfeFtdcTradeStatField(Structure):
    """成交排名统计"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("ExchangeProductInstID", c_char*100),
        ("InvestorID", c_char*13),
        ("TotalVol", c_int32),
        ("TotalAmt", c_double),
        ("BuyVol", c_int32),
        ("BuyAmt", c_double),
        ("SellVol", c_int32),
        ("SellAmt", c_double),
        ("NetVol", c_int32),
        ("NetAmt", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getExchangeProductInstID(self):
        '''交易所品种合约代码组合(交易所代码使用前缀e:，格式如cu,e:SHFE,cu1105)'''
        return str(self.ExchangeProductInstID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getTotalVol(self):
        '''总成交量'''
        return self.TotalVol

    def getTotalAmt(self):
        '''总成交额'''
        return self.TotalAmt

    def getBuyVol(self):
        '''买成交量'''
        return self.BuyVol

    def getBuyAmt(self):
        '''买成交额'''
        return self.BuyAmt

    def getSellVol(self):
        '''卖成交量'''
        return self.SellVol

    def getSellAmt(self):
        '''卖成交额'''
        return self.SellAmt

    def getNetVol(self):
        '''净买入成交量'''
        return self.NetVol

    def getNetAmt(self):
        '''净买入成交额'''
        return self.NetAmt

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'ExchangeProductInstID'={self.getExchangeProductInstID()}, 'InvestorID'={self.getInvestorID()}, 'TotalVol'={self.getTotalVol()}, 'TotalAmt'={self.getTotalAmt()}, 'BuyVol'={self.getBuyVol()}, 'BuyAmt'={self.getBuyAmt()}, 'SellVol'={self.getSellVol()}, 'SellAmt'={self.getSellAmt()}, 'NetVol'={self.getNetVol()}, 'NetAmt'={self.getNetAmt()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'ExchangeProductInstID': self.getExchangeProductInstID(), 'InvestorID': self.getInvestorID(), 'TotalVol': self.getTotalVol(), 'TotalAmt': self.getTotalAmt(), 'BuyVol': self.getBuyVol(), 'BuyAmt': self.getBuyAmt(), 'SellVol': self.getSellVol(), 'SellAmt': self.getSellAmt(), 'NetVol': self.getNetVol(), 'NetAmt': self.getNetAmt()}


class  CShfeFtdcOrderStatField(Structure):
    """报单排名统计"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("ExchangeProductInstID", c_char*100),
        ("InvestorID", c_char*13),
        ("TotalVol", c_int32),
        ("BuyVol", c_int32),
        ("SellVol", c_int32),
        ("NetVol", c_int32),
        ("TradeCount", c_int32),
        ("TotalCount", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getExchangeProductInstID(self):
        '''交易所品种合约代码组合(交易所代码使用前缀e:，格式如cu,e:SHFE,cu1105)'''
        return str(self.ExchangeProductInstID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getTotalVol(self):
        '''总报单量'''
        return self.TotalVol

    def getBuyVol(self):
        '''买报单量'''
        return self.BuyVol

    def getSellVol(self):
        '''卖报单量'''
        return self.SellVol

    def getNetVol(self):
        '''净买入报单量'''
        return self.NetVol

    def getTradeCount(self):
        '''有成交报单数'''
        return self.TradeCount

    def getTotalCount(self):
        '''总报单数'''
        return self.TotalCount

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'ExchangeProductInstID'={self.getExchangeProductInstID()}, 'InvestorID'={self.getInvestorID()}, 'TotalVol'={self.getTotalVol()}, 'BuyVol'={self.getBuyVol()}, 'SellVol'={self.getSellVol()}, 'NetVol'={self.getNetVol()}, 'TradeCount'={self.getTradeCount()}, 'TotalCount'={self.getTotalCount()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'ExchangeProductInstID': self.getExchangeProductInstID(), 'InvestorID': self.getInvestorID(), 'TotalVol': self.getTotalVol(), 'BuyVol': self.getBuyVol(), 'SellVol': self.getSellVol(), 'NetVol': self.getNetVol(), 'TradeCount': self.getTradeCount(), 'TotalCount': self.getTotalCount()}


class  CShfeFtdcDRSysIDField(Structure):
    """灾备子系统编号"""
    _fields_ = [
        ("DRSysID", c_int32),
    ]

    def getDRSysID(self):
        '''灾备子系统编号(每个子系统中心一个编号)'''
        return self.DRSysID

    @property
    def __str__(self):
        return f"'DRSysID'={self.getDRSysID()}"

    @property
    def __dict__(self):
        return {'DRSysID': self.getDRSysID()}


class  CShfeFtdcQryInvestorMarginRateField(Structure):
    """查询投资者保证金率"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("HedgeFlag", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'HedgeFlag'={self.getHedgeFlag()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'HedgeFlag': self.getHedgeFlag()}


class  CShfeFtdcInvestorMarginRateField(Structure):
    """投资者保证金率"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("MinMargin", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getMinMargin(self):
        '''单位（手）期权合约最小保证金'''
        return self.MinMargin

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'MinMargin'={self.getMinMargin()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'MinMargin': self.getMinMargin()}


class  CShfeFtdcSTPriceField(Structure):
    """压力测试结算价格"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorRange", c_char),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("PriceType", c_char),
        ("Price", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getInvestorID(self):
        '''投资者代码或模板代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getPriceType(self):
        '''价格类型'''
        return TShfeFtdcPriceTypeType(ord(self.PriceType))

    def getPrice(self):
        '''价格'''
        return self.Price

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorRange'={self.getInvestorRange()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'PriceType'={self.getPriceType()}, 'Price'={self.getPrice()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorRange': self.getInvestorRange(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'PriceType': self.getPriceType(), 'Price': self.getPrice()}


class  CShfeFtdcSTMarginRateField(Structure):
    """压力测试保证金率"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("MinMargin", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getMinMargin(self):
        '''单位（手）期权合约最小保证金'''
        return self.MinMargin

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'MinMargin'={self.getMinMargin()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'MinMargin': self.getMinMargin()}


class  CShfeFtdcSeqSmsCustomNotifyField(Structure):
    """短信自定义通知"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("SequenceNo", c_int32),
        ("Type", c_char),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorID", c_char*13),
        ("Mobile", c_char*41),
        ("Message", c_char*501),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getSequenceNo(self):
        '''通知事件在当天的序号'''
        return self.SequenceNo

    def getType(self):
        '''短信类型'''
        return TShfeFtdcSmsCustomTypeType(ord(self.Type))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getMobile(self):
        '''手机'''
        return str(self.Mobile, 'GBK')

    def getMessage(self):
        '''通知内容'''
        return str(self.Message, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'SequenceNo'={self.getSequenceNo()}, 'Type'={self.getType()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorID'={self.getInvestorID()}, 'Mobile'={self.getMobile()}, 'Message'={self.getMessage()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'SequenceNo': self.getSequenceNo(), 'Type': self.getType(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorID': self.getInvestorID(), 'Mobile': self.getMobile(), 'Message': self.getMessage()}


class  CShfeFtdcSetSmsStatusField(Structure):
    """请求设置短信通知状态"""
    _fields_ = [
        ("SequenceNo", c_int32),
        ("Type", c_char),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InvestorID", c_char*13),
        ("Status", c_char),
    ]

    def getSequenceNo(self):
        '''通知事件在当天的序号'''
        return self.SequenceNo

    def getType(self):
        '''短信类型'''
        return TShfeFtdcSmsCustomTypeType(ord(self.Type))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getStatus(self):
        '''通知状态'''
        return TShfeFtdcRiskNotifyStatusType(ord(self.Status))

    @property
    def __str__(self):
        return f"'SequenceNo'={self.getSequenceNo()}, 'Type'={self.getType()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InvestorID'={self.getInvestorID()}, 'Status'={self.getStatus()}"

    @property
    def __dict__(self):
        return {'SequenceNo': self.getSequenceNo(), 'Type': self.getType(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InvestorID': self.getInvestorID(), 'Status': self.getStatus()}


class  CShfeFtdcSTExchMarginRateField(Structure):
    """压力测试交易所保证金率"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("MinMargin", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getMinMargin(self):
        '''单位（手）期权合约最小保证金'''
        return self.MinMargin

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'MinMargin'={self.getMinMargin()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'MinMargin': self.getMinMargin()}


class  CShfeFtdcQryExchMarginRateField(Structure):
    """查询投资者交易所保证金率"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InstrumentID", c_char*31),
        ("HedgeFlag", c_char),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InstrumentID'={self.getInstrumentID()}, 'HedgeFlag'={self.getHedgeFlag()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InstrumentID': self.getInstrumentID(), 'HedgeFlag': self.getHedgeFlag()}


class  CShfeFtdcExchMarginRateField(Structure):
    """投资者交易所保证金率"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InstrumentID", c_char*31),
        ("HedgeFlag", c_char),
        ("LongMarginRatioByMoney", c_double),
        ("LongMarginRatioByVolume", c_double),
        ("ShortMarginRatioByMoney", c_double),
        ("ShortMarginRatioByVolume", c_double),
        ("MinMargin", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getLongMarginRatioByMoney(self):
        '''多头保证金率'''
        return self.LongMarginRatioByMoney

    def getLongMarginRatioByVolume(self):
        '''多头保证金费'''
        return self.LongMarginRatioByVolume

    def getShortMarginRatioByMoney(self):
        '''空头保证金率'''
        return self.ShortMarginRatioByMoney

    def getShortMarginRatioByVolume(self):
        '''空头保证金费'''
        return self.ShortMarginRatioByVolume

    def getMinMargin(self):
        '''单位（手）期权合约最小保证金'''
        return self.MinMargin

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InstrumentID'={self.getInstrumentID()}, 'HedgeFlag'={self.getHedgeFlag()}, 'LongMarginRatioByMoney'={self.getLongMarginRatioByMoney()}, 'LongMarginRatioByVolume'={self.getLongMarginRatioByVolume()}, 'ShortMarginRatioByMoney'={self.getShortMarginRatioByMoney()}, 'ShortMarginRatioByVolume'={self.getShortMarginRatioByVolume()}, 'MinMargin'={self.getMinMargin()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InstrumentID': self.getInstrumentID(), 'HedgeFlag': self.getHedgeFlag(), 'LongMarginRatioByMoney': self.getLongMarginRatioByMoney(), 'LongMarginRatioByVolume': self.getLongMarginRatioByVolume(), 'ShortMarginRatioByMoney': self.getShortMarginRatioByMoney(), 'ShortMarginRatioByVolume': self.getShortMarginRatioByVolume(), 'MinMargin': self.getMinMargin()}


class  CShfeFtdcSeqIPGroupMarginField(Structure):
    """投资者产品组保证金"""
    _fields_ = [
        ("UniqSequenceNo", c_int32),
        ("ProductGroupID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("FrozenMargin", c_double),
        ("LongFrozenMargin", c_double),
        ("ShortFrozenMargin", c_double),
        ("UseMargin", c_double),
        ("LongUseMargin", c_double),
        ("ShortUseMargin", c_double),
        ("ExchMargin", c_double),
        ("LongExchMargin", c_double),
        ("ShortExchMargin", c_double),
        ("CloseProfit", c_double),
        ("FrozenCommission", c_double),
        ("Commission", c_double),
        ("FrozenCash", c_double),
        ("CashIn", c_double),
        ("PositionProfit", c_double),
        ("OffsetAmount", c_double),
        ("LongOffsetAmount", c_double),
        ("ShortOffsetAmount", c_double),
        ("ExchOffsetAmount", c_double),
        ("LongExchOffsetAmount", c_double),
        ("ShortExchOffsetAmount", c_double),
        ("HedgeFlag", c_char),
        ("ExchangeID", c_char*9),
        ("InvestUnitID", c_char*17),
    ]

    def getUniqSequenceNo(self):
        '''流中唯一的序列号'''
        return self.UniqSequenceNo

    def getProductGroupID(self):
        '''品种/跨品种标示'''
        return str(self.ProductGroupID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getLongFrozenMargin(self):
        '''多头冻结的保证金'''
        return self.LongFrozenMargin

    def getShortFrozenMargin(self):
        '''空头冻结的保证金'''
        return self.ShortFrozenMargin

    def getUseMargin(self):
        '''占用的保证金'''
        return self.UseMargin

    def getLongUseMargin(self):
        '''多头保证金'''
        return self.LongUseMargin

    def getShortUseMargin(self):
        '''空头保证金'''
        return self.ShortUseMargin

    def getExchMargin(self):
        '''交易所保证金'''
        return self.ExchMargin

    def getLongExchMargin(self):
        '''交易所多头保证金'''
        return self.LongExchMargin

    def getShortExchMargin(self):
        '''交易所空头保证金'''
        return self.ShortExchMargin

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getOffsetAmount(self):
        '''折抵总金额'''
        return self.OffsetAmount

    def getLongOffsetAmount(self):
        '''多头折抵总金额'''
        return self.LongOffsetAmount

    def getShortOffsetAmount(self):
        '''空头折抵总金额'''
        return self.ShortOffsetAmount

    def getExchOffsetAmount(self):
        '''交易所折抵总金额'''
        return self.ExchOffsetAmount

    def getLongExchOffsetAmount(self):
        '''交易所多头折抵总金额'''
        return self.LongExchOffsetAmount

    def getShortExchOffsetAmount(self):
        '''交易所空头折抵总金额'''
        return self.ShortExchOffsetAmount

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    @property
    def __str__(self):
        return f"'UniqSequenceNo'={self.getUniqSequenceNo()}, 'ProductGroupID'={self.getProductGroupID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'FrozenMargin'={self.getFrozenMargin()}, 'LongFrozenMargin'={self.getLongFrozenMargin()}, 'ShortFrozenMargin'={self.getShortFrozenMargin()}, 'UseMargin'={self.getUseMargin()}, 'LongUseMargin'={self.getLongUseMargin()}, 'ShortUseMargin'={self.getShortUseMargin()}, 'ExchMargin'={self.getExchMargin()}, 'LongExchMargin'={self.getLongExchMargin()}, 'ShortExchMargin'={self.getShortExchMargin()}, 'CloseProfit'={self.getCloseProfit()}, 'FrozenCommission'={self.getFrozenCommission()}, 'Commission'={self.getCommission()}, 'FrozenCash'={self.getFrozenCash()}, 'CashIn'={self.getCashIn()}, 'PositionProfit'={self.getPositionProfit()}, 'OffsetAmount'={self.getOffsetAmount()}, 'LongOffsetAmount'={self.getLongOffsetAmount()}, 'ShortOffsetAmount'={self.getShortOffsetAmount()}, 'ExchOffsetAmount'={self.getExchOffsetAmount()}, 'LongExchOffsetAmount'={self.getLongExchOffsetAmount()}, 'ShortExchOffsetAmount'={self.getShortExchOffsetAmount()}, 'HedgeFlag'={self.getHedgeFlag()}, 'ExchangeID'={self.getExchangeID()}, 'InvestUnitID'={self.getInvestUnitID()}"

    @property
    def __dict__(self):
        return {'UniqSequenceNo': self.getUniqSequenceNo(), 'ProductGroupID': self.getProductGroupID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'FrozenMargin': self.getFrozenMargin(), 'LongFrozenMargin': self.getLongFrozenMargin(), 'ShortFrozenMargin': self.getShortFrozenMargin(), 'UseMargin': self.getUseMargin(), 'LongUseMargin': self.getLongUseMargin(), 'ShortUseMargin': self.getShortUseMargin(), 'ExchMargin': self.getExchMargin(), 'LongExchMargin': self.getLongExchMargin(), 'ShortExchMargin': self.getShortExchMargin(), 'CloseProfit': self.getCloseProfit(), 'FrozenCommission': self.getFrozenCommission(), 'Commission': self.getCommission(), 'FrozenCash': self.getFrozenCash(), 'CashIn': self.getCashIn(), 'PositionProfit': self.getPositionProfit(), 'OffsetAmount': self.getOffsetAmount(), 'LongOffsetAmount': self.getLongOffsetAmount(), 'ShortOffsetAmount': self.getShortOffsetAmount(), 'ExchOffsetAmount': self.getExchOffsetAmount(), 'LongExchOffsetAmount': self.getLongExchOffsetAmount(), 'ShortExchOffsetAmount': self.getShortExchOffsetAmount(), 'HedgeFlag': self.getHedgeFlag(), 'ExchangeID': self.getExchangeID(), 'InvestUnitID': self.getInvestUnitID()}


class  CShfeFtdcBrokerInvestorCurrencyField(Structure):
    """经纪公司投资者币种代码"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("CurrencyID", c_char*4),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'CurrencyID'={self.getCurrencyID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'CurrencyID': self.getCurrencyID()}


class  CShfeFtdcSecAgentInvestorField(Structure):
    """二代投资者"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("BrokerSecAgentID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者ID'''
        return str(self.InvestorID, 'GBK')

    def getBrokerSecAgentID(self):
        '''转委托中介机构资金帐号'''
        return str(self.BrokerSecAgentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'BrokerSecAgentID'={self.getBrokerSecAgentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'BrokerSecAgentID': self.getBrokerSecAgentID()}


class  CShfeFtdcSTStandardField(Structure):
    """压力测试标准"""
    _fields_ = [
        ("STDCECombMarginUsed", c_int32),
    ]

    def getSTDCECombMarginUsed(self):
        '''大商所盘后组合保证金优惠'''
        return self.STDCECombMarginUsed

    @property
    def __str__(self):
        return f"'STDCECombMarginUsed'={self.getSTDCECombMarginUsed()}"

    @property
    def __dict__(self):
        return {'STDCECombMarginUsed': self.getSTDCECombMarginUsed()}


class  CShfeFtdcSTDCECombMarginParamField(Structure):
    """压力测试大商所盘后组合保证金优惠参数"""
    _fields_ = [
        ("STDCECombType", c_char),
        ("SequenceNo", c_int32),
        ("ProductID", c_char*31),
        ("ProductID2", c_char*31),
    ]

    def getSTDCECombType(self):
        '''风控大商所组合类型'''
        return TShfeFtdcSTDCECombTypeType(ord(self.STDCECombType))

    def getSequenceNo(self):
        '''组合序号'''
        return self.SequenceNo

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getProductID2(self):
        '''产品代码'''
        return str(self.ProductID2, 'GBK')

    @property
    def __str__(self):
        return f"'STDCECombType'={self.getSTDCECombType()}, 'SequenceNo'={self.getSequenceNo()}, 'ProductID'={self.getProductID()}, 'ProductID2'={self.getProductID2()}"

    @property
    def __dict__(self):
        return {'STDCECombType': self.getSTDCECombType(), 'SequenceNo': self.getSequenceNo(), 'ProductID': self.getProductID(), 'ProductID2': self.getProductID2()}


class  CShfeFtdcSTDCESPInsGroupParamField(Structure):
    """压力测试大商所跨期组合合约分组参数"""
    _fields_ = [
        ("ProductID", c_char*31),
        ("InstrumentID", c_char*31),
        ("SequenceNo", c_int32),
    ]

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getSequenceNo(self):
        '''分组序号'''
        return self.SequenceNo

    @property
    def __str__(self):
        return f"'ProductID'={self.getProductID()}, 'InstrumentID'={self.getInstrumentID()}, 'SequenceNo'={self.getSequenceNo()}"

    @property
    def __dict__(self):
        return {'ProductID': self.getProductID(), 'InstrumentID': self.getInstrumentID(), 'SequenceNo': self.getSequenceNo()}


class  CShfeFtdcProductExchRateField(Structure):
    """产品报价汇率表"""
    _fields_ = [
        ("ProductID", c_char*31),
        ("QuoteCurrencyID", c_char*4),
        ("ExchangeRate", c_double),
    ]

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getQuoteCurrencyID(self):
        '''报价币种类型'''
        return str(self.QuoteCurrencyID, 'GBK')

    def getExchangeRate(self):
        '''汇率'''
        return self.ExchangeRate

    @property
    def __str__(self):
        return f"'ProductID'={self.getProductID()}, 'QuoteCurrencyID'={self.getQuoteCurrencyID()}, 'ExchangeRate'={self.getExchangeRate()}"

    @property
    def __dict__(self):
        return {'ProductID': self.getProductID(), 'QuoteCurrencyID': self.getQuoteCurrencyID(), 'ExchangeRate': self.getExchangeRate()}


class  CShfeFtdcRiskInvestorPositionField(Structure):
    """风控用于输出的投资者合约持仓"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("PosiDirection", c_char),
        ("HedgeFlag", c_char),
        ("PositionDate", c_char),
        ("YdPosition", c_int32),
        ("Position", c_int32),
        ("LongFrozen", c_int32),
        ("ShortFrozen", c_int32),
        ("LongFrozenAmount", c_double),
        ("ShortFrozenAmount", c_double),
        ("OpenVolume", c_int32),
        ("CloseVolume", c_int32),
        ("OpenAmount", c_double),
        ("CloseAmount", c_double),
        ("PositionCost", c_double),
        ("PreMargin", c_double),
        ("UseMargin", c_double),
        ("FrozenMargin", c_double),
        ("FrozenCash", c_double),
        ("FrozenCommission", c_double),
        ("CashIn", c_double),
        ("Commission", c_double),
        ("CloseProfit", c_double),
        ("PositionProfit", c_double),
        ("PreSettlementPrice", c_double),
        ("SettlementPrice", c_double),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("OpenCost", c_double),
        ("ExchangeMargin", c_double),
        ("CombPosition", c_int32),
        ("CombLongFrozen", c_int32),
        ("CombShortFrozen", c_int32),
        ("CloseProfitByDate", c_double),
        ("CloseProfitByTrade", c_double),
        ("TodayPosition", c_int32),
        ("MarginRateByMoney", c_double),
        ("MarginRateByVolume", c_double),
        ("StrikeFrozen", c_int32),
        ("StrikeFrozenAmount", c_double),
        ("AbandonFrozen", c_int32),
        ("OptionValue", c_double),
        ("MaintUseMargin", c_double),
        ("MaintExchangeMargin", c_double),
        ("IndexSettlementPrice", c_double),
        ("FixedMargin", c_double),
        ("ExchangeID", c_char*9),
        ("YdStrikeFrozen", c_int32),
        ("InvestUnitID", c_char*17),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPosiDirection(self):
        '''持仓多空方向'''
        return TShfeFtdcPosiDirectionType(ord(self.PosiDirection))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPositionDate(self):
        '''持仓日期'''
        return TShfeFtdcPositionDateType(ord(self.PositionDate))

    def getYdPosition(self):
        '''上日持仓'''
        return self.YdPosition

    def getPosition(self):
        '''今日持仓'''
        return self.Position

    def getLongFrozen(self):
        '''多头冻结'''
        return self.LongFrozen

    def getShortFrozen(self):
        '''空头冻结'''
        return self.ShortFrozen

    def getLongFrozenAmount(self):
        '''开仓冻结金额'''
        return self.LongFrozenAmount

    def getShortFrozenAmount(self):
        '''开仓冻结金额'''
        return self.ShortFrozenAmount

    def getOpenVolume(self):
        '''开仓量'''
        return self.OpenVolume

    def getCloseVolume(self):
        '''平仓量'''
        return self.CloseVolume

    def getOpenAmount(self):
        '''开仓金额'''
        return self.OpenAmount

    def getCloseAmount(self):
        '''平仓金额'''
        return self.CloseAmount

    def getPositionCost(self):
        '''持仓成本'''
        return self.PositionCost

    def getPreMargin(self):
        '''上次占用的保证金'''
        return self.PreMargin

    def getUseMargin(self):
        '''占用的保证金'''
        return self.UseMargin

    def getFrozenMargin(self):
        '''冻结的保证金'''
        return self.FrozenMargin

    def getFrozenCash(self):
        '''冻结的资金'''
        return self.FrozenCash

    def getFrozenCommission(self):
        '''冻结的手续费'''
        return self.FrozenCommission

    def getCashIn(self):
        '''资金差额'''
        return self.CashIn

    def getCommission(self):
        '''手续费'''
        return self.Commission

    def getCloseProfit(self):
        '''平仓盈亏'''
        return self.CloseProfit

    def getPositionProfit(self):
        '''持仓盈亏'''
        return self.PositionProfit

    def getPreSettlementPrice(self):
        '''上次结算价'''
        return self.PreSettlementPrice

    def getSettlementPrice(self):
        '''本次结算价'''
        return self.SettlementPrice

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getOpenCost(self):
        '''开仓成本'''
        return self.OpenCost

    def getExchangeMargin(self):
        '''交易所保证金'''
        return self.ExchangeMargin

    def getCombPosition(self):
        '''组合成交形成的持仓'''
        return self.CombPosition

    def getCombLongFrozen(self):
        '''组合多头冻结'''
        return self.CombLongFrozen

    def getCombShortFrozen(self):
        '''组合空头冻结'''
        return self.CombShortFrozen

    def getCloseProfitByDate(self):
        '''逐日盯市平仓盈亏'''
        return self.CloseProfitByDate

    def getCloseProfitByTrade(self):
        '''逐笔对冲平仓盈亏'''
        return self.CloseProfitByTrade

    def getTodayPosition(self):
        '''今日持仓'''
        return self.TodayPosition

    def getMarginRateByMoney(self):
        '''保证金率'''
        return self.MarginRateByMoney

    def getMarginRateByVolume(self):
        '''保证金率(按手数)'''
        return self.MarginRateByVolume

    def getStrikeFrozen(self):
        '''执行冻结'''
        return self.StrikeFrozen

    def getStrikeFrozenAmount(self):
        '''执行冻结金额'''
        return self.StrikeFrozenAmount

    def getAbandonFrozen(self):
        '''放弃执行冻结'''
        return self.AbandonFrozen

    def getOptionValue(self):
        '''期权市值'''
        return self.OptionValue

    def getMaintUseMargin(self):
        '''占用的维持保证金'''
        return self.MaintUseMargin

    def getMaintExchangeMargin(self):
        '''交易所维持保证金'''
        return self.MaintExchangeMargin

    def getIndexSettlementPrice(self):
        '''期权标的合约的本次结算价'''
        return self.IndexSettlementPrice

    def getFixedMargin(self):
        '''昨结算价计算的期权保证金'''
        return self.FixedMargin

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getYdStrikeFrozen(self):
        '''执行冻结的昨仓'''
        return self.YdStrikeFrozen

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'PosiDirection'={self.getPosiDirection()}, 'HedgeFlag'={self.getHedgeFlag()}, 'PositionDate'={self.getPositionDate()}, 'YdPosition'={self.getYdPosition()}, 'Position'={self.getPosition()}, 'LongFrozen'={self.getLongFrozen()}, 'ShortFrozen'={self.getShortFrozen()}, 'LongFrozenAmount'={self.getLongFrozenAmount()}, 'ShortFrozenAmount'={self.getShortFrozenAmount()}, 'OpenVolume'={self.getOpenVolume()}, 'CloseVolume'={self.getCloseVolume()}, 'OpenAmount'={self.getOpenAmount()}, 'CloseAmount'={self.getCloseAmount()}, 'PositionCost'={self.getPositionCost()}, 'PreMargin'={self.getPreMargin()}, 'UseMargin'={self.getUseMargin()}, 'FrozenMargin'={self.getFrozenMargin()}, 'FrozenCash'={self.getFrozenCash()}, 'FrozenCommission'={self.getFrozenCommission()}, 'CashIn'={self.getCashIn()}, 'Commission'={self.getCommission()}, 'CloseProfit'={self.getCloseProfit()}, 'PositionProfit'={self.getPositionProfit()}, 'PreSettlementPrice'={self.getPreSettlementPrice()}, 'SettlementPrice'={self.getSettlementPrice()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'OpenCost'={self.getOpenCost()}, 'ExchangeMargin'={self.getExchangeMargin()}, 'CombPosition'={self.getCombPosition()}, 'CombLongFrozen'={self.getCombLongFrozen()}, 'CombShortFrozen'={self.getCombShortFrozen()}, 'CloseProfitByDate'={self.getCloseProfitByDate()}, 'CloseProfitByTrade'={self.getCloseProfitByTrade()}, 'TodayPosition'={self.getTodayPosition()}, 'MarginRateByMoney'={self.getMarginRateByMoney()}, 'MarginRateByVolume'={self.getMarginRateByVolume()}, 'StrikeFrozen'={self.getStrikeFrozen()}, 'StrikeFrozenAmount'={self.getStrikeFrozenAmount()}, 'AbandonFrozen'={self.getAbandonFrozen()}, 'OptionValue'={self.getOptionValue()}, 'MaintUseMargin'={self.getMaintUseMargin()}, 'MaintExchangeMargin'={self.getMaintExchangeMargin()}, 'IndexSettlementPrice'={self.getIndexSettlementPrice()}, 'FixedMargin'={self.getFixedMargin()}, 'ExchangeID'={self.getExchangeID()}, 'YdStrikeFrozen'={self.getYdStrikeFrozen()}, 'InvestUnitID'={self.getInvestUnitID()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'PosiDirection': self.getPosiDirection(), 'HedgeFlag': self.getHedgeFlag(), 'PositionDate': self.getPositionDate(), 'YdPosition': self.getYdPosition(), 'Position': self.getPosition(), 'LongFrozen': self.getLongFrozen(), 'ShortFrozen': self.getShortFrozen(), 'LongFrozenAmount': self.getLongFrozenAmount(), 'ShortFrozenAmount': self.getShortFrozenAmount(), 'OpenVolume': self.getOpenVolume(), 'CloseVolume': self.getCloseVolume(), 'OpenAmount': self.getOpenAmount(), 'CloseAmount': self.getCloseAmount(), 'PositionCost': self.getPositionCost(), 'PreMargin': self.getPreMargin(), 'UseMargin': self.getUseMargin(), 'FrozenMargin': self.getFrozenMargin(), 'FrozenCash': self.getFrozenCash(), 'FrozenCommission': self.getFrozenCommission(), 'CashIn': self.getCashIn(), 'Commission': self.getCommission(), 'CloseProfit': self.getCloseProfit(), 'PositionProfit': self.getPositionProfit(), 'PreSettlementPrice': self.getPreSettlementPrice(), 'SettlementPrice': self.getSettlementPrice(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'OpenCost': self.getOpenCost(), 'ExchangeMargin': self.getExchangeMargin(), 'CombPosition': self.getCombPosition(), 'CombLongFrozen': self.getCombLongFrozen(), 'CombShortFrozen': self.getCombShortFrozen(), 'CloseProfitByDate': self.getCloseProfitByDate(), 'CloseProfitByTrade': self.getCloseProfitByTrade(), 'TodayPosition': self.getTodayPosition(), 'MarginRateByMoney': self.getMarginRateByMoney(), 'MarginRateByVolume': self.getMarginRateByVolume(), 'StrikeFrozen': self.getStrikeFrozen(), 'StrikeFrozenAmount': self.getStrikeFrozenAmount(), 'AbandonFrozen': self.getAbandonFrozen(), 'OptionValue': self.getOptionValue(), 'MaintUseMargin': self.getMaintUseMargin(), 'MaintExchangeMargin': self.getMaintExchangeMargin(), 'IndexSettlementPrice': self.getIndexSettlementPrice(), 'FixedMargin': self.getFixedMargin(), 'ExchangeID': self.getExchangeID(), 'YdStrikeFrozen': self.getYdStrikeFrozen(), 'InvestUnitID': self.getInvestUnitID()}


class  CShfeFtdcRiskQryExecOrderField(Structure):
    """风控执行宣告查询"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("ExecOrderSysID", c_char*21),
        ("InsertTimeStart", c_char*9),
        ("InsertTimeEnd", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getExecOrderSysID(self):
        '''执行宣告编号'''
        return str(self.ExecOrderSysID, 'GBK')

    def getInsertTimeStart(self):
        '''开始时间'''
        return str(self.InsertTimeStart, 'GBK')

    def getInsertTimeEnd(self):
        '''结束时间'''
        return str(self.InsertTimeEnd, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'ExecOrderSysID'={self.getExecOrderSysID()}, 'InsertTimeStart'={self.getInsertTimeStart()}, 'InsertTimeEnd'={self.getInsertTimeEnd()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID(), 'ExecOrderSysID': self.getExecOrderSysID(), 'InsertTimeStart': self.getInsertTimeStart(), 'InsertTimeEnd': self.getInsertTimeEnd()}


class  CShfeFtdcRiskExecOrderField(Structure):
    """风控执行宣告"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("ExecOrderRef", c_char*13),
        ("UserID", c_char*16),
        ("Volume", c_int32),
        ("RequestID", c_int32),
        ("BusinessUnit", c_char*21),
        ("OffsetFlag", c_char),
        ("HedgeFlag", c_char),
        ("ActionType", c_char),
        ("PosiDirection", c_char),
        ("ReservePositionFlag", c_char),
        ("CloseFlag", c_char),
        ("ExecOrderLocalID", c_char*13),
        ("ExchangeID", c_char*9),
        ("ParticipantID", c_char*11),
        ("ClientID", c_char*11),
        ("ExchangeInstID", c_char*31),
        ("TraderID", c_char*21),
        ("InstallID", c_int32),
        ("OrderSubmitStatus", c_char),
        ("NotifySequence", c_int32),
        ("TradingDay", c_char*9),
        ("SettlementID", c_int32),
        ("ExecOrderSysID", c_char*21),
        ("InsertDate", c_char*9),
        ("InsertTime", c_char*9),
        ("CancelTime", c_char*9),
        ("ExecResult", c_char),
        ("ClearingPartID", c_char*11),
        ("SequenceNo", c_int32),
        ("FrontID", c_int32),
        ("SessionID", c_int32),
        ("UserProductInfo", c_char*11),
        ("StatusMsg", c_char*81),
        ("ActiveUserID", c_char*16),
        ("BrokerExecOrderSeq", c_int32),
        ("BranchID", c_char*9),
        ("InvestUnitID", c_char*17),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExecOrderRef(self):
        '''执行宣告引用'''
        return str(self.ExecOrderRef, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getVolume(self):
        '''数量'''
        return self.Volume

    def getRequestID(self):
        '''请求编号'''
        return self.RequestID

    def getBusinessUnit(self):
        '''业务单元'''
        return str(self.BusinessUnit, 'GBK')

    def getOffsetFlag(self):
        '''开平标志'''
        return TShfeFtdcOffsetFlagType(ord(self.OffsetFlag))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getActionType(self):
        '''执行类型'''
        return TShfeFtdcActionTypeType(ord(self.ActionType))

    def getPosiDirection(self):
        '''保留头寸申请的持仓方向'''
        return TShfeFtdcPosiDirectionType(ord(self.PosiDirection))

    def getReservePositionFlag(self):
        '''期权行权后是否保留期货头寸的标记,该字段已废弃'''
        return TShfeFtdcExecOrderPositionFlagType(ord(self.ReservePositionFlag))

    def getCloseFlag(self):
        '''期权行权后生成的头寸是否自动平仓'''
        return TShfeFtdcExecOrderCloseFlagType(ord(self.CloseFlag))

    def getExecOrderLocalID(self):
        '''本地执行宣告编号'''
        return str(self.ExecOrderLocalID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getParticipantID(self):
        '''会员代码'''
        return str(self.ParticipantID, 'GBK')

    def getClientID(self):
        '''客户代码'''
        return str(self.ClientID, 'GBK')

    def getExchangeInstID(self):
        '''合约在交易所的代码'''
        return str(self.ExchangeInstID, 'GBK')

    def getTraderID(self):
        '''交易所交易员代码'''
        return str(self.TraderID, 'GBK')

    def getInstallID(self):
        '''安装编号'''
        return self.InstallID

    def getOrderSubmitStatus(self):
        '''执行宣告提交状态'''
        return TShfeFtdcOrderSubmitStatusType(ord(self.OrderSubmitStatus))

    def getNotifySequence(self):
        '''报单提示序号'''
        return self.NotifySequence

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getSettlementID(self):
        '''结算编号'''
        return self.SettlementID

    def getExecOrderSysID(self):
        '''执行宣告编号'''
        return str(self.ExecOrderSysID, 'GBK')

    def getInsertDate(self):
        '''报单日期'''
        return str(self.InsertDate, 'GBK')

    def getInsertTime(self):
        '''插入时间'''
        return str(self.InsertTime, 'GBK')

    def getCancelTime(self):
        '''撤销时间'''
        return str(self.CancelTime, 'GBK')

    def getExecResult(self):
        '''执行结果'''
        return TShfeFtdcExecResultType(ord(self.ExecResult))

    def getClearingPartID(self):
        '''结算会员编号'''
        return str(self.ClearingPartID, 'GBK')

    def getSequenceNo(self):
        '''序号'''
        return self.SequenceNo

    def getFrontID(self):
        '''前置编号'''
        return self.FrontID

    def getSessionID(self):
        '''会话编号'''
        return self.SessionID

    def getUserProductInfo(self):
        '''用户端产品信息'''
        return str(self.UserProductInfo, 'GBK')

    def getStatusMsg(self):
        '''状态信息'''
        return str(self.StatusMsg, 'GBK')

    def getActiveUserID(self):
        '''操作用户代码'''
        return str(self.ActiveUserID, 'GBK')

    def getBrokerExecOrderSeq(self):
        '''经纪公司报单编号'''
        return self.BrokerExecOrderSeq

    def getBranchID(self):
        '''营业部编号'''
        return str(self.BranchID, 'GBK')

    def getInvestUnitID(self):
        '''投资单元代码'''
        return str(self.InvestUnitID, 'GBK')

    def getAccountID(self):
        '''资金账号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'ExecOrderRef'={self.getExecOrderRef()}, 'UserID'={self.getUserID()}, 'Volume'={self.getVolume()}, 'RequestID'={self.getRequestID()}, 'BusinessUnit'={self.getBusinessUnit()}, 'OffsetFlag'={self.getOffsetFlag()}, 'HedgeFlag'={self.getHedgeFlag()}, 'ActionType'={self.getActionType()}, 'PosiDirection'={self.getPosiDirection()}, 'ReservePositionFlag'={self.getReservePositionFlag()}, 'CloseFlag'={self.getCloseFlag()}, 'ExecOrderLocalID'={self.getExecOrderLocalID()}, 'ExchangeID'={self.getExchangeID()}, 'ParticipantID'={self.getParticipantID()}, 'ClientID'={self.getClientID()}, 'ExchangeInstID'={self.getExchangeInstID()}, 'TraderID'={self.getTraderID()}, 'InstallID'={self.getInstallID()}, 'OrderSubmitStatus'={self.getOrderSubmitStatus()}, 'NotifySequence'={self.getNotifySequence()}, 'TradingDay'={self.getTradingDay()}, 'SettlementID'={self.getSettlementID()}, 'ExecOrderSysID'={self.getExecOrderSysID()}, 'InsertDate'={self.getInsertDate()}, 'InsertTime'={self.getInsertTime()}, 'CancelTime'={self.getCancelTime()}, 'ExecResult'={self.getExecResult()}, 'ClearingPartID'={self.getClearingPartID()}, 'SequenceNo'={self.getSequenceNo()}, 'FrontID'={self.getFrontID()}, 'SessionID'={self.getSessionID()}, 'UserProductInfo'={self.getUserProductInfo()}, 'StatusMsg'={self.getStatusMsg()}, 'ActiveUserID'={self.getActiveUserID()}, 'BrokerExecOrderSeq'={self.getBrokerExecOrderSeq()}, 'BranchID'={self.getBranchID()}, 'InvestUnitID'={self.getInvestUnitID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'ExecOrderRef': self.getExecOrderRef(), 'UserID': self.getUserID(), 'Volume': self.getVolume(), 'RequestID': self.getRequestID(), 'BusinessUnit': self.getBusinessUnit(), 'OffsetFlag': self.getOffsetFlag(), 'HedgeFlag': self.getHedgeFlag(), 'ActionType': self.getActionType(), 'PosiDirection': self.getPosiDirection(), 'ReservePositionFlag': self.getReservePositionFlag(), 'CloseFlag': self.getCloseFlag(), 'ExecOrderLocalID': self.getExecOrderLocalID(), 'ExchangeID': self.getExchangeID(), 'ParticipantID': self.getParticipantID(), 'ClientID': self.getClientID(), 'ExchangeInstID': self.getExchangeInstID(), 'TraderID': self.getTraderID(), 'InstallID': self.getInstallID(), 'OrderSubmitStatus': self.getOrderSubmitStatus(), 'NotifySequence': self.getNotifySequence(), 'TradingDay': self.getTradingDay(), 'SettlementID': self.getSettlementID(), 'ExecOrderSysID': self.getExecOrderSysID(), 'InsertDate': self.getInsertDate(), 'InsertTime': self.getInsertTime(), 'CancelTime': self.getCancelTime(), 'ExecResult': self.getExecResult(), 'ClearingPartID': self.getClearingPartID(), 'SequenceNo': self.getSequenceNo(), 'FrontID': self.getFrontID(), 'SessionID': self.getSessionID(), 'UserProductInfo': self.getUserProductInfo(), 'StatusMsg': self.getStatusMsg(), 'ActiveUserID': self.getActiveUserID(), 'BrokerExecOrderSeq': self.getBrokerExecOrderSeq(), 'BranchID': self.getBranchID(), 'InvestUnitID': self.getInvestUnitID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcOptionInstrCommRateField(Structure):
    """当前期权合约手续费的详细内容"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("OpenRatioByMoney", c_double),
        ("OpenRatioByVolume", c_double),
        ("CloseRatioByMoney", c_double),
        ("CloseRatioByVolume", c_double),
        ("CloseTodayRatioByMoney", c_double),
        ("CloseTodayRatioByVolume", c_double),
        ("StrikeRatioByMoney", c_double),
        ("StrikeRatioByVolume", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getOpenRatioByMoney(self):
        '''开仓手续费率'''
        return self.OpenRatioByMoney

    def getOpenRatioByVolume(self):
        '''开仓手续费'''
        return self.OpenRatioByVolume

    def getCloseRatioByMoney(self):
        '''平仓手续费率'''
        return self.CloseRatioByMoney

    def getCloseRatioByVolume(self):
        '''平仓手续费'''
        return self.CloseRatioByVolume

    def getCloseTodayRatioByMoney(self):
        '''平今手续费率'''
        return self.CloseTodayRatioByMoney

    def getCloseTodayRatioByVolume(self):
        '''平今手续费'''
        return self.CloseTodayRatioByVolume

    def getStrikeRatioByMoney(self):
        '''执行手续费率'''
        return self.StrikeRatioByMoney

    def getStrikeRatioByVolume(self):
        '''执行手续费'''
        return self.StrikeRatioByVolume

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'OpenRatioByMoney'={self.getOpenRatioByMoney()}, 'OpenRatioByVolume'={self.getOpenRatioByVolume()}, 'CloseRatioByMoney'={self.getCloseRatioByMoney()}, 'CloseRatioByVolume'={self.getCloseRatioByVolume()}, 'CloseTodayRatioByMoney'={self.getCloseTodayRatioByMoney()}, 'CloseTodayRatioByVolume'={self.getCloseTodayRatioByVolume()}, 'StrikeRatioByMoney'={self.getStrikeRatioByMoney()}, 'StrikeRatioByVolume'={self.getStrikeRatioByVolume()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'OpenRatioByMoney': self.getOpenRatioByMoney(), 'OpenRatioByVolume': self.getOpenRatioByVolume(), 'CloseRatioByMoney': self.getCloseRatioByMoney(), 'CloseRatioByVolume': self.getCloseRatioByVolume(), 'CloseTodayRatioByMoney': self.getCloseTodayRatioByMoney(), 'CloseTodayRatioByVolume': self.getCloseTodayRatioByVolume(), 'StrikeRatioByMoney': self.getStrikeRatioByMoney(), 'StrikeRatioByVolume': self.getStrikeRatioByVolume()}


class  CShfeFtdcQryOptionInstrCommRateField(Structure):
    """期权手续费率查询"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcMMOptionInstrCommRateField(Structure):
    """当前做市商期权合约手续费的详细内容"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("InvestorRange", c_char),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("OpenRatioByMoney", c_double),
        ("OpenRatioByVolume", c_double),
        ("CloseRatioByMoney", c_double),
        ("CloseRatioByVolume", c_double),
        ("CloseTodayRatioByMoney", c_double),
        ("CloseTodayRatioByVolume", c_double),
        ("StrikeRatioByMoney", c_double),
        ("StrikeRatioByVolume", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getOpenRatioByMoney(self):
        '''开仓手续费率'''
        return self.OpenRatioByMoney

    def getOpenRatioByVolume(self):
        '''开仓手续费'''
        return self.OpenRatioByVolume

    def getCloseRatioByMoney(self):
        '''平仓手续费率'''
        return self.CloseRatioByMoney

    def getCloseRatioByVolume(self):
        '''平仓手续费'''
        return self.CloseRatioByVolume

    def getCloseTodayRatioByMoney(self):
        '''平今手续费率'''
        return self.CloseTodayRatioByMoney

    def getCloseTodayRatioByVolume(self):
        '''平今手续费'''
        return self.CloseTodayRatioByVolume

    def getStrikeRatioByMoney(self):
        '''执行手续费率'''
        return self.StrikeRatioByMoney

    def getStrikeRatioByVolume(self):
        '''执行手续费'''
        return self.StrikeRatioByVolume

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'InvestorRange'={self.getInvestorRange()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'OpenRatioByMoney'={self.getOpenRatioByMoney()}, 'OpenRatioByVolume'={self.getOpenRatioByVolume()}, 'CloseRatioByMoney'={self.getCloseRatioByMoney()}, 'CloseRatioByVolume'={self.getCloseRatioByVolume()}, 'CloseTodayRatioByMoney'={self.getCloseTodayRatioByMoney()}, 'CloseTodayRatioByVolume'={self.getCloseTodayRatioByVolume()}, 'StrikeRatioByMoney'={self.getStrikeRatioByMoney()}, 'StrikeRatioByVolume'={self.getStrikeRatioByVolume()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'InvestorRange': self.getInvestorRange(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'OpenRatioByMoney': self.getOpenRatioByMoney(), 'OpenRatioByVolume': self.getOpenRatioByVolume(), 'CloseRatioByMoney': self.getCloseRatioByMoney(), 'CloseRatioByVolume': self.getCloseRatioByVolume(), 'CloseTodayRatioByMoney': self.getCloseTodayRatioByMoney(), 'CloseTodayRatioByVolume': self.getCloseTodayRatioByVolume(), 'StrikeRatioByMoney': self.getStrikeRatioByMoney(), 'StrikeRatioByVolume': self.getStrikeRatioByVolume()}


class  CShfeFtdcQryMMOptionInstrCommRateField(Structure):
    """做市商期权手续费率查询"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID()}


class  CShfeFtdcRiskQryLogUserLoginStatField(Structure):
    """风控查询交易用户登录统计信息"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("FailNumByUser", c_int32),
        ("AddressNumByUser", c_int32),
        ("UserNumByAddress", c_int32),
        ("TotalNumByAddress", c_int32),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getFailNumByUser(self):
        '''同一User的登录失败次数数阀值'''
        return self.FailNumByUser

    def getAddressNumByUser(self):
        '''同一User的不同登录地址数阀值'''
        return self.AddressNumByUser

    def getUserNumByAddress(self):
        '''同一IPMAC地址上的不同登录用户数阀值'''
        return self.UserNumByAddress

    def getTotalNumByAddress(self):
        '''同一IPMAC地址上的登录总次数阀值'''
        return self.TotalNumByAddress

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'FailNumByUser'={self.getFailNumByUser()}, 'AddressNumByUser'={self.getAddressNumByUser()}, 'UserNumByAddress'={self.getUserNumByAddress()}, 'TotalNumByAddress'={self.getTotalNumByAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'FailNumByUser': self.getFailNumByUser(), 'AddressNumByUser': self.getAddressNumByUser(), 'UserNumByAddress': self.getUserNumByAddress(), 'TotalNumByAddress': self.getTotalNumByAddress()}


class  CShfeFtdcRiskLogUserLoginStatField(Structure):
    """风控查询交易用户登录统计信息内容"""
    _fields_ = [
        ("StatType", c_char),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
        ("TotalNum", c_int32),
        ("SuccessNum", c_int32),
        ("FailNum", c_int32),
        ("UserNumByAddress", c_int32),
        ("AddressNumByUser", c_int32),
    ]

    def getStatType(self):
        '''交易用户登录统计类型'''
        return TShfeFtdcLoginStatTypeType(ord(self.StatType))

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    def getTotalNum(self):
        '''登录总次数'''
        return self.TotalNum

    def getSuccessNum(self):
        '''登录成功次数'''
        return self.SuccessNum

    def getFailNum(self):
        '''登录失败次数'''
        return self.FailNum

    def getUserNumByAddress(self):
        '''同一IPMAC地址上的不同登录用户数'''
        return self.UserNumByAddress

    def getAddressNumByUser(self):
        '''同一User的不同登录地址数'''
        return self.AddressNumByUser

    @property
    def __str__(self):
        return f"'StatType'={self.getStatType()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}, 'TotalNum'={self.getTotalNum()}, 'SuccessNum'={self.getSuccessNum()}, 'FailNum'={self.getFailNum()}, 'UserNumByAddress'={self.getUserNumByAddress()}, 'AddressNumByUser'={self.getAddressNumByUser()}"

    @property
    def __dict__(self):
        return {'StatType': self.getStatType(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress(), 'TotalNum': self.getTotalNum(), 'SuccessNum': self.getSuccessNum(), 'FailNum': self.getFailNum(), 'UserNumByAddress': self.getUserNumByAddress(), 'AddressNumByUser': self.getAddressNumByUser()}


class  CShfeFtdcRiskQryLogUserLoginInfoField(Structure):
    """风控查询交易用户登录信息"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress()}


class  CShfeFtdcRiskLogUserLoginInfoField(Structure):
    """风控查询交易用户登录信息内容"""
    _fields_ = [
        ("TradingDay", c_char*9),
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("IPAddress", c_char*16),
        ("MacAddress", c_char*21),
        ("TotalNum", c_int32),
        ("SuccessNum", c_int32),
        ("FailNum", c_int32),
    ]

    def getTradingDay(self):
        '''交易日'''
        return str(self.TradingDay, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getIPAddress(self):
        '''IP地址'''
        return str(self.IPAddress, 'GBK')

    def getMacAddress(self):
        '''Mac地址'''
        return str(self.MacAddress, 'GBK')

    def getTotalNum(self):
        '''登录总次数'''
        return self.TotalNum

    def getSuccessNum(self):
        '''登录成功次数'''
        return self.SuccessNum

    def getFailNum(self):
        '''登录失败次数'''
        return self.FailNum

    @property
    def __str__(self):
        return f"'TradingDay'={self.getTradingDay()}, 'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'IPAddress'={self.getIPAddress()}, 'MacAddress'={self.getMacAddress()}, 'TotalNum'={self.getTotalNum()}, 'SuccessNum'={self.getSuccessNum()}, 'FailNum'={self.getFailNum()}"

    @property
    def __dict__(self):
        return {'TradingDay': self.getTradingDay(), 'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'IPAddress': self.getIPAddress(), 'MacAddress': self.getMacAddress(), 'TotalNum': self.getTotalNum(), 'SuccessNum': self.getSuccessNum(), 'FailNum': self.getFailNum()}


class  CShfeFtdcRiskQryInstrumentGreeksField(Structure):
    """风控查询期权合约希腊值"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID()}


class  CShfeFtdcRiskInstrumentGreeksField(Structure):
    """风控期权合约希腊值"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("ExchangeID", c_char*9),
        ("Delta", c_double),
        ("Gamma", c_double),
        ("Vega", c_double),
        ("Theta", c_double),
        ("SettlementPrice", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getExchangeID(self):
        '''交易所代码'''
        return str(self.ExchangeID, 'GBK')

    def getDelta(self):
        '''期权价值关于期货价格变化的比率'''
        return self.Delta

    def getGamma(self):
        '''Delta关于期货价格变化的比率'''
        return self.Gamma

    def getVega(self):
        '''期权价值关于波动率变化的比率'''
        return self.Vega

    def getTheta(self):
        '''期权价值关于时间变化的比率'''
        return self.Theta

    def getSettlementPrice(self):
        '''当前最新结算价'''
        return self.SettlementPrice

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'ExchangeID'={self.getExchangeID()}, 'Delta'={self.getDelta()}, 'Gamma'={self.getGamma()}, 'Vega'={self.getVega()}, 'Theta'={self.getTheta()}, 'SettlementPrice'={self.getSettlementPrice()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'ExchangeID': self.getExchangeID(), 'Delta': self.getDelta(), 'Gamma': self.getGamma(), 'Vega': self.getVega(), 'Theta': self.getTheta(), 'SettlementPrice': self.getSettlementPrice()}


class  CShfeFtdcETPriceField(Structure):
    """行权试算结算价格"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorRange", c_char),
        ("InvestorID", c_char*13),
        ("InstrumentID", c_char*31),
        ("PriceType", c_char),
        ("Price", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorRange(self):
        '''投资者范围'''
        return TShfeFtdcInvestorRangeType(ord(self.InvestorRange))

    def getInvestorID(self):
        '''投资者代码或模板代码'''
        return str(self.InvestorID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getPriceType(self):
        '''价格类型'''
        return TShfeFtdcPriceTypeType(ord(self.PriceType))

    def getPrice(self):
        '''价格'''
        return self.Price

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorRange'={self.getInvestorRange()}, 'InvestorID'={self.getInvestorID()}, 'InstrumentID'={self.getInstrumentID()}, 'PriceType'={self.getPriceType()}, 'Price'={self.getPrice()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorRange': self.getInvestorRange(), 'InvestorID': self.getInvestorID(), 'InstrumentID': self.getInstrumentID(), 'PriceType': self.getPriceType(), 'Price': self.getPrice()}


class  CShfeFtdcETStrikePositionField(Structure):
    """行权试算持仓"""
    _fields_ = [
        ("InstrumentID", c_char*31),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("PosiDirection", c_char),
        ("HedgeFlag", c_char),
        ("PositionDate", c_char),
        ("Position", c_int32),
        ("EXEPosition", c_int32),
        ("EXEPriceType", c_char),
        ("EXEPrice", c_double),
    ]

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getPosiDirection(self):
        '''持仓多空方向'''
        return TShfeFtdcPosiDirectionType(ord(self.PosiDirection))

    def getHedgeFlag(self):
        '''投机套保标志'''
        return TShfeFtdcHedgeFlagType(ord(self.HedgeFlag))

    def getPositionDate(self):
        '''持仓日期'''
        return TShfeFtdcPositionDateType(ord(self.PositionDate))

    def getPosition(self):
        '''当前持仓数量'''
        return self.Position

    def getEXEPosition(self):
        '''需执行持仓数量'''
        return self.EXEPosition

    def getEXEPriceType(self):
        '''行权价格类型'''
        return TShfeFtdcPriceTypeType(ord(self.EXEPriceType))

    def getEXEPrice(self):
        '''行权试算价格'''
        return self.EXEPrice

    @property
    def __str__(self):
        return f"'InstrumentID'={self.getInstrumentID()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'PosiDirection'={self.getPosiDirection()}, 'HedgeFlag'={self.getHedgeFlag()}, 'PositionDate'={self.getPositionDate()}, 'Position'={self.getPosition()}, 'EXEPosition'={self.getEXEPosition()}, 'EXEPriceType'={self.getEXEPriceType()}, 'EXEPrice'={self.getEXEPrice()}"

    @property
    def __dict__(self):
        return {'InstrumentID': self.getInstrumentID(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'PosiDirection': self.getPosiDirection(), 'HedgeFlag': self.getHedgeFlag(), 'PositionDate': self.getPositionDate(), 'Position': self.getPosition(), 'EXEPosition': self.getEXEPosition(), 'EXEPriceType': self.getEXEPriceType(), 'EXEPrice': self.getEXEPrice()}


class  CShfeFtdcETDCECombMarginParamField(Structure):
    """行权试算大商所盘后组合保证金优惠参数"""
    _fields_ = [
        ("STDCECombType", c_char),
        ("SequenceNo", c_int32),
        ("ProductID", c_char*31),
        ("ProductID2", c_char*31),
    ]

    def getSTDCECombType(self):
        '''风控大商所组合类型'''
        return TShfeFtdcSTDCECombTypeType(ord(self.STDCECombType))

    def getSequenceNo(self):
        '''组合序号'''
        return self.SequenceNo

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getProductID2(self):
        '''产品代码'''
        return str(self.ProductID2, 'GBK')

    @property
    def __str__(self):
        return f"'STDCECombType'={self.getSTDCECombType()}, 'SequenceNo'={self.getSequenceNo()}, 'ProductID'={self.getProductID()}, 'ProductID2'={self.getProductID2()}"

    @property
    def __dict__(self):
        return {'STDCECombType': self.getSTDCECombType(), 'SequenceNo': self.getSequenceNo(), 'ProductID': self.getProductID(), 'ProductID2': self.getProductID2()}


class  CShfeFtdcETDCESPInsGroupParamField(Structure):
    """行权试算大商所跨期组合合约分组参数"""
    _fields_ = [
        ("ProductID", c_char*31),
        ("InstrumentID", c_char*31),
        ("SequenceNo", c_int32),
    ]

    def getProductID(self):
        '''产品代码'''
        return str(self.ProductID, 'GBK')

    def getInstrumentID(self):
        '''合约代码'''
        return str(self.InstrumentID, 'GBK')

    def getSequenceNo(self):
        '''分组序号'''
        return self.SequenceNo

    @property
    def __str__(self):
        return f"'ProductID'={self.getProductID()}, 'InstrumentID'={self.getInstrumentID()}, 'SequenceNo'={self.getSequenceNo()}"

    @property
    def __dict__(self):
        return {'ProductID': self.getProductID(), 'InstrumentID': self.getInstrumentID(), 'SequenceNo': self.getSequenceNo()}


class  CShfeFtdcInvestorTestResultField(Structure):
    """行权试算响应"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("AccountID", c_char*13),
        ("CurrencyID", c_char*4),
        ("Balance", c_double),
        ("Available", c_double),
        ("LongExeMargin", c_double),
        ("ShortExeMargin", c_double),
        ("ExeMoney", c_double),
        ("ExeProfit", c_double),
        ("ReleaseMoney", c_double),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getAccountID(self):
        '''投资者帐号'''
        return str(self.AccountID, 'GBK')

    def getCurrencyID(self):
        '''币种代码'''
        return str(self.CurrencyID, 'GBK')

    def getBalance(self):
        '''总权益'''
        return self.Balance

    def getAvailable(self):
        '''可用资金'''
        return self.Available

    def getLongExeMargin(self):
        '''买行权冻结保证金'''
        return self.LongExeMargin

    def getShortExeMargin(self):
        '''买行权冻结保证金'''
        return self.ShortExeMargin

    def getExeMoney(self):
        '''执行费用'''
        return self.ExeMoney

    def getExeProfit(self):
        '''执行盈亏总额'''
        return self.ExeProfit

    def getReleaseMoney(self):
        '''释放保证金'''
        return self.ReleaseMoney

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'AccountID'={self.getAccountID()}, 'CurrencyID'={self.getCurrencyID()}, 'Balance'={self.getBalance()}, 'Available'={self.getAvailable()}, 'LongExeMargin'={self.getLongExeMargin()}, 'ShortExeMargin'={self.getShortExeMargin()}, 'ExeMoney'={self.getExeMoney()}, 'ExeProfit'={self.getExeProfit()}, 'ReleaseMoney'={self.getReleaseMoney()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'AccountID': self.getAccountID(), 'CurrencyID': self.getCurrencyID(), 'Balance': self.getBalance(), 'Available': self.getAvailable(), 'LongExeMargin': self.getLongExeMargin(), 'ShortExeMargin': self.getShortExeMargin(), 'ExeMoney': self.getExeMoney(), 'ExeProfit': self.getExeProfit(), 'ReleaseMoney': self.getReleaseMoney()}


class  CShfeFtdcUserRightsAssignField(Structure):
    """当前交易中心"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("UserID", c_char*16),
        ("DRIdentityID", c_int32),
    ]

    def getBrokerID(self):
        '''应用单元代码'''
        return str(self.BrokerID, 'GBK')

    def getUserID(self):
        '''用户代码'''
        return str(self.UserID, 'GBK')

    def getDRIdentityID(self):
        '''交易中心代码'''
        return self.DRIdentityID

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'UserID'={self.getUserID()}, 'DRIdentityID'={self.getDRIdentityID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'UserID': self.getUserID(), 'DRIdentityID': self.getDRIdentityID()}


class  CShfeFtdcCurrDRIdentityField(Structure):
    """用户下单权限分配表"""
    _fields_ = [
        ("DRIdentityID", c_int32),
    ]

    def getDRIdentityID(self):
        '''交易中心代码'''
        return self.DRIdentityID

    @property
    def __str__(self):
        return f"'DRIdentityID'={self.getDRIdentityID()}"

    @property
    def __dict__(self):
        return {'DRIdentityID': self.getDRIdentityID()}


class  CShfeFtdcQrySyncDelaySwapField(Structure):
    """查询延时换汇"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("DelaySwapSeqNo", c_char*15),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getDelaySwapSeqNo(self):
        '''延时换汇流水号'''
        return str(self.DelaySwapSeqNo, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'DelaySwapSeqNo'={self.getDelaySwapSeqNo()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'DelaySwapSeqNo': self.getDelaySwapSeqNo()}


class  CShfeFtdcSyncDelaySwapField(Structure):
    """同步延时换汇"""
    _fields_ = [
        ("DelaySwapSeqNo", c_char*15),
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
        ("FromCurrencyID", c_char*4),
        ("FromAmount", c_double),
        ("FromFrozenSwap", c_double),
        ("FromRemainSwap", c_double),
        ("ToCurrencyID", c_char*4),
        ("ToAmount", c_double),
    ]

    def getDelaySwapSeqNo(self):
        '''换汇流水号'''
        return str(self.DelaySwapSeqNo, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getFromCurrencyID(self):
        '''源币种'''
        return str(self.FromCurrencyID, 'GBK')

    def getFromAmount(self):
        '''源金额'''
        return self.FromAmount

    def getFromFrozenSwap(self):
        '''源换汇冻结金额(可用冻结)'''
        return self.FromFrozenSwap

    def getFromRemainSwap(self):
        '''源剩余换汇额度(可提冻结)'''
        return self.FromRemainSwap

    def getToCurrencyID(self):
        '''目标币种'''
        return str(self.ToCurrencyID, 'GBK')

    def getToAmount(self):
        '''目标金额'''
        return self.ToAmount

    @property
    def __str__(self):
        return f"'DelaySwapSeqNo'={self.getDelaySwapSeqNo()}, 'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}, 'FromCurrencyID'={self.getFromCurrencyID()}, 'FromAmount'={self.getFromAmount()}, 'FromFrozenSwap'={self.getFromFrozenSwap()}, 'FromRemainSwap'={self.getFromRemainSwap()}, 'ToCurrencyID'={self.getToCurrencyID()}, 'ToAmount'={self.getToAmount()}"

    @property
    def __dict__(self):
        return {'DelaySwapSeqNo': self.getDelaySwapSeqNo(), 'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID(), 'FromCurrencyID': self.getFromCurrencyID(), 'FromAmount': self.getFromAmount(), 'FromFrozenSwap': self.getFromFrozenSwap(), 'FromRemainSwap': self.getFromRemainSwap(), 'ToCurrencyID': self.getToCurrencyID(), 'ToAmount': self.getToAmount()}


class  CShfeFtdcSecAgentCheckModeField(Structure):
    """二级代理商资金校验模式"""
    _fields_ = [
        ("InvestorID", c_char*13),
        ("BrokerID", c_char*11),
        ("CurrencyID", c_char*4),
        ("BrokerSecAgentID", c_char*13),
        ("CheckSelfAccount", c_int32),
    ]

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getCurrencyID(self):
        '''币种'''
        return str(self.CurrencyID, 'GBK')

    def getBrokerSecAgentID(self):
        '''境外中介机构资金帐号'''
        return str(self.BrokerSecAgentID, 'GBK')

    def getCheckSelfAccount(self):
        '''是否需要校验自己的资金账户'''
        return self.CheckSelfAccount

    @property
    def __str__(self):
        return f"'InvestorID'={self.getInvestorID()}, 'BrokerID'={self.getBrokerID()}, 'CurrencyID'={self.getCurrencyID()}, 'BrokerSecAgentID'={self.getBrokerSecAgentID()}, 'CheckSelfAccount'={self.getCheckSelfAccount()}"

    @property
    def __dict__(self):
        return {'InvestorID': self.getInvestorID(), 'BrokerID': self.getBrokerID(), 'CurrencyID': self.getCurrencyID(), 'BrokerSecAgentID': self.getBrokerSecAgentID(), 'CheckSelfAccount': self.getCheckSelfAccount()}


class  CShfeFtdcQrySecAgentCheckModeField(Structure):
    """查询二级代理商资金校验模式"""
    _fields_ = [
        ("BrokerID", c_char*11),
        ("InvestorID", c_char*13),
    ]

    def getBrokerID(self):
        '''经纪公司代码'''
        return str(self.BrokerID, 'GBK')

    def getInvestorID(self):
        '''投资者代码'''
        return str(self.InvestorID, 'GBK')

    @property
    def __str__(self):
        return f"'BrokerID'={self.getBrokerID()}, 'InvestorID'={self.getInvestorID()}"

    @property
    def __dict__(self):
        return {'BrokerID': self.getBrokerID(), 'InvestorID': self.getInvestorID()}

