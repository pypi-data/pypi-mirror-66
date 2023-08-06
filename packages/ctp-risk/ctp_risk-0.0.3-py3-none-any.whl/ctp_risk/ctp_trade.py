#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HaiFeng
# @Email   : 24918700@qq.com
# @Time    : 2018/12/10


import os, sys, platform
import copy
from .ctp_struct import *


class Trade(object):

    def __init__(self):

        dllpath = os.path.dirname(os.path.abspath(__file__))
        absolute_dllfile_path = os.path.join(dllpath, f"lib{'64' if sys.maxsize > 2**32 else '32'}", 'riskapi.' + ('dll' if 'Windows' in platform.system() else 'so'))
        if not os.path.exists(absolute_dllfile_path):
            print('缺少DLL接口文件')
            return

        # make log dir for api log
        logdir = os.path.join(os.getcwd(), 'log')
        if not os.path.exists(logdir):
            os.mkdir(logdir)

        dlldir = os.path.split(absolute_dllfile_path)[0]
        # change work directory
        cur_path = os.getcwd()
        os.chdir(dlldir)

        self.h = CDLL(absolute_dllfile_path)

        self.h.CreateApi.argtypes = []
        self.h.CreateApi.restype = c_void_p

        self.h.CreateSpi.argtypes = []
        self.h.CreateSpi.restype = c_void_p

        self.api = None
        self.spi = None
        self.nRequestID = 0
        self.h.Release.argtypes = [c_void_p]
        self.h.Release.restype = c_void_p

        self.h.Init.argtypes = [c_void_p]
        self.h.Init.restype = c_void_p

        self.h.Join.argtypes = [c_void_p]
        self.h.Join.restype = c_void_p

        self.h.RegisterFront.argtypes = [c_void_p, c_void_p]
        self.h.RegisterFront.restype = c_void_p

        self.h.RegisterSpi.argtypes = [c_void_p, c_void_p]
        self.h.RegisterSpi.restype = c_void_p

        self.h.ReqRiskUserLogin.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqRiskUserLogin.restype = c_void_p

        self.h.ReqQryInvestorMarginRate.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqQryInvestorMarginRate.restype = c_void_p

        self.h.ReqQryOrderStat.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryOrderStat.restype = c_void_p

        self.h.ReqSubRiskMarketData.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqSubRiskMarketData.restype = c_void_p

        self.h.ReqUnSubRiskMarketData.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqUnSubRiskMarketData.restype = c_void_p

        self.h.ReqQryInstPositionRate.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqQryInstPositionRate.restype = c_void_p

        self.h.ReqQryProductPositionRate.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqQryProductPositionRate.restype = c_void_p

        self.h.ReqQryTradingCodeHash.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryTradingCodeHash.restype = c_void_p

        self.h.ReqQryTradingCode.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqQryTradingCode.restype = c_void_p

        self.h.ReqSubscribeTrade.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSubscribeTrade.restype = c_void_p

        self.h.ReqSubscribeOrder.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSubscribeOrder.restype = c_void_p

        self.h.ReqSubBrokerUserEvent.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSubBrokerUserEvent.restype = c_void_p

        self.h.ReqRiskOrderInsert.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqRiskOrderInsert.restype = c_void_p

        self.h.ReqRiskOrderAction.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqRiskOrderAction.restype = c_void_p

        self.h.ReqSubscribePosition.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSubscribePosition.restype = c_void_p

        self.h.ReqRiskNotifyCommand.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqRiskNotifyCommand.restype = c_void_p

        self.h.ReqBatchForceCloseCalc.argtypes = [
            c_void_p, c_void_p, c_void_p, c_int32, c_void_p, c_int32, c_int32]
        self.h.ReqBatchForceCloseCalc.restype = c_void_p

        self.h.ReqForceCloseCalc.argtypes = [
            c_void_p, c_void_p, c_void_p, c_int32, c_void_p, c_int32]
        self.h.ReqForceCloseCalc.restype = c_void_p

        self.h.ReqSetIndexNPPParam.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSetIndexNPPParam.restype = c_void_p

        self.h.ReqRemIndexNPPParam.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqRemIndexNPPParam.restype = c_void_p

        self.h.ReqQryLogin.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryLogin.restype = c_void_p

        self.h.ReqQryPriceVaryEffect.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryPriceVaryEffect.restype = c_void_p

        self.h.ReqQrySafePriceRange.argtypes = [
            c_void_p, c_void_p, c_void_p, c_int32, c_void_p, c_int32, c_int32]
        self.h.ReqQrySafePriceRange.restype = c_void_p

        self.h.ReqRiskParkedOrderInsert.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqRiskParkedOrderInsert.restype = c_void_p

        self.h.ReqRemoveRiskParkedOrder.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqRemoveRiskParkedOrder.restype = c_void_p

        self.h.ReqSubRiskParkedOrder.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSubRiskParkedOrder.restype = c_void_p

        self.h.ReqRiskUserPasswordUpd.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqRiskUserPasswordUpd.restype = c_void_p

        self.h.ReqSubSeqDeposit.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSubSeqDeposit.restype = c_void_p

        self.h.ReqAddRiskUserEvent.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqAddRiskUserEvent.restype = c_void_p

        self.h.ReqQryPredictRisk.argtypes = [
            c_void_p, c_void_p, c_void_p, c_int32, c_void_p, c_int32, c_int32]
        self.h.ReqQryPredictRisk.restype = c_void_p

        self.h.ReqQryInvestorLinkMan.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqQryInvestorLinkMan.restype = c_void_p

        self.h.ReqQryInvestorDepartment.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqQryInvestorDepartment.restype = c_void_p

        self.h.ReqSubPreRiskAccount.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSubPreRiskAccount.restype = c_void_p

        self.h.ReqModNoticePattern.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqModNoticePattern.restype = c_void_p

        self.h.ReqSubVaryMarketData.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqSubVaryMarketData.restype = c_void_p

        self.h.ReqUnSubVaryMarketData.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqUnSubVaryMarketData.restype = c_void_p

        self.h.ReqAddRiskNotifyA.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqAddRiskNotifyA.restype = c_void_p

        self.h.ReqAddBizNotice.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqAddBizNotice.restype = c_void_p

        self.h.ReqSubSeqData.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSubSeqData.restype = c_void_p

        self.h.ReqRiskQryBrokerDeposit.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqRiskQryBrokerDeposit.restype = c_void_p

        self.h.ReqModRiskInvestorParam.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqModRiskInvestorParam.restype = c_void_p

        self.h.ReqRemRiskInvestorParam.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqRemRiskInvestorParam.restype = c_void_p

        self.h.ReqForceRiskUserLogout.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqForceRiskUserLogout.restype = c_void_p

        self.h.ReqAddRiskPattern.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqAddRiskPattern.restype = c_void_p

        self.h.ReqModRiskPattern.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqModRiskPattern.restype = c_void_p

        self.h.ReqRemRiskPattern.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqRemRiskPattern.restype = c_void_p

        self.h.ReqAddInvestorPattern.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqAddInvestorPattern.restype = c_void_p

        self.h.ReqModInvestorPattern.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqModInvestorPattern.restype = c_void_p

        self.h.ReqRemInvestorPattern.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqRemInvestorPattern.restype = c_void_p

        self.h.ReqSubSeqRiskNotifyB.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSubSeqRiskNotifyB.restype = c_void_p

        self.h.ReqQryPositionStat.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryPositionStat.restype = c_void_p

        self.h.ReqQryTradeStat.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryTradeStat.restype = c_void_p

        self.h.ReqQryInvestorLinkManHash.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqQryInvestorLinkManHash.restype = c_void_p

        self.h.ReqQryInvestorDepartmentHash.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqQryInvestorDepartmentHash.restype = c_void_p

        self.h.ReqQryStressTest.argtypes = [c_void_p, c_void_p, c_int32, c_void_p, c_int32,
                                            c_void_p, c_int32, c_void_p, c_void_p, c_int32, c_void_p, c_int32, c_int32]
        self.h.ReqQryStressTest.restype = c_void_p

        self.h.ReqQryLowMarginInvestorHash.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqQryLowMarginInvestorHash.restype = c_void_p

        self.h.ReqQryLowMarginInvestor.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqQryLowMarginInvestor.restype = c_void_p

        self.h.ReqSetSmsStatus.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqSetSmsStatus.restype = c_void_p

        self.h.ReqQryExchMarginRate.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryExchMarginRate.restype = c_void_p

        self.h.ReqQryCommissionRate.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryCommissionRate.restype = c_void_p

        self.h.ReqQrySecAgentInvestorHash.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqQrySecAgentInvestorHash.restype = c_void_p

        self.h.ReqQrySecAgentInvestor.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqQrySecAgentInvestor.restype = c_void_p

        self.h.ReqQryOptionInstrCommRate.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqQryOptionInstrCommRate.restype = c_void_p

        self.h.ReqQryMMOptionInstrCommRate.argtypes = [
            c_void_p, c_void_p, c_int32]
        self.h.ReqQryMMOptionInstrCommRate.restype = c_void_p

        self.h.ReqQryExecOrder.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryExecOrder.restype = c_void_p

        self.h.ReqQryLogUserLoginStat.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryLogUserLoginStat.restype = c_void_p

        self.h.ReqQryLogUserLoginInfo.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryLogUserLoginInfo.restype = c_void_p

        self.h.ReqQryInstrumentGreeks.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryInstrumentGreeks.restype = c_void_p

        self.h.ReqQryExeciseTest.argtypes = [
            c_void_p, c_void_p, c_int32, c_void_p, c_int32, c_void_p, c_int32, c_void_p, c_int32, c_int32]
        self.h.ReqQryExeciseTest.restype = c_void_p

        self.h.ReqQryUserRightsAssign.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryUserRightsAssign.restype = c_void_p

        self.h.ReqQryCurrDRIdentity.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQryCurrDRIdentity.restype = c_void_p

        self.h.ReqQrySecAgentTradingAccount.argtypes = [
            c_void_p, c_void_p, c_int32, c_int32]
        self.h.ReqQrySecAgentTradingAccount.restype = c_void_p

        self.h.ReqQrySyncDelaySwap.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQrySyncDelaySwap.restype = c_void_p

        self.h.ReqQrySecAgentCheckMode.argtypes = [c_void_p, c_void_p, c_int32]
        self.h.ReqQrySecAgentCheckMode.restype = c_void_p
        os.chdir(cur_path)

    def CreateApi(self):
        self.api = self.h.CreateApi()
        return self.api

    def CreateSpi(self):
        self.spi = self.h.CreateSpi()
        return self.spi

    def Release(self):
        self.h.Release(self.api)

    def Init(self):
        self.h.Init(self.api)

    def Join(self):
        self.h.Join(self.api)

    def RegisterFront(self, pszFrontAddress: 'str'):
        self.h.RegisterFront(self.api, bytes(
            pszFrontAddress, encoding='ascii'))

    def RegisterSpi(self, pSpi):
        self.h.RegisterSpi(self.api, pSpi)

    def ReqRiskUserLogin(self, BrokerID: str = '', UserID: str = '', Password: str = '', Version: int = 1, LocalSessionID: int = 1, MacAddress: str = '', ClientIPAddress: str = ''):
        pReqRiskUserLogin = CShfeFtdcReqRiskUserLoginField()
        pReqRiskUserLogin.BrokerID = bytes(BrokerID, encoding='ascii')
        pReqRiskUserLogin.UserID = bytes(UserID, encoding='ascii')
        pReqRiskUserLogin.Password = bytes(Password, encoding='ascii')
        pReqRiskUserLogin.Version = Version
        pReqRiskUserLogin.LocalSessionID = LocalSessionID
        pReqRiskUserLogin.MacAddress = bytes(MacAddress, encoding='ascii')
        pReqRiskUserLogin.ClientIPAddress = bytes(
            ClientIPAddress, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRiskUserLogin(self.api, byref(
            pReqRiskUserLogin), self.nRequestID)

    def ReqQryInvestorMarginRate(self, BrokerID: str = '', InvestorID: str = '', InstrumentID: str = '', HedgeFlag: TShfeFtdcHedgeFlagType = list(TShfeFtdcHedgeFlagType)[0]):
        pQryInvestorMarginRate = CShfeFtdcQryInvestorMarginRateField()
        pQryInvestorMarginRate.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryInvestorMarginRate.InvestorID = bytes(InvestorID, encoding='ascii')
        pQryInvestorMarginRate.InstrumentID = bytes(
            InstrumentID, encoding='ascii')
        pQryInvestorMarginRate.HedgeFlag = HedgeFlag.value
        self.nRequestID += 1
        self.h.ReqQryInvestorMarginRate(self.api, byref(
            pQryInvestorMarginRate), self.nRequestID)

    def ReqQryOrderStat(self, BrokerID: str = '', ExchangeProductInstID: str = '', SortType: TShfeFtdcStatSortTypeType = list(TShfeFtdcStatSortTypeType)[0], ResultCount: int = 1, ResultRatio: float = .0):
        pQryStat = CShfeFtdcQryStatField()
        pQryStat.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryStat.ExchangeProductInstID = bytes(
            ExchangeProductInstID, encoding='ascii')
        pQryStat.SortType = SortType.value
        pQryStat.ResultCount = ResultCount
        pQryStat.ResultRatio = ResultRatio
        self.nRequestID += 1
        self.h.ReqQryOrderStat(self.api, byref(pQryStat), self.nRequestID)

    def ReqSubRiskMarketData(self, InstrumentID: str = '', SubMarketDataCnt: int = 1):
        pSubMarketData = CShfeFtdcSubMarketDataField()
        pSubMarketData.InstrumentID = bytes(InstrumentID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqSubRiskMarketData(self.api, byref(
            pSubMarketData), SubMarketDataCnt, self.nRequestID)

    def ReqUnSubRiskMarketData(self, InstrumentID: str = ''):
        pSubMarketData = CShfeFtdcSubMarketDataField()
        pSubMarketData.InstrumentID = bytes(InstrumentID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqUnSubRiskMarketData(
            self.api, byref(pSubMarketData), self.nRequestID)

    def ReqQryInstPositionRate(self, BrokerID: str = '', InstIDStart: str = '', InstIDEnd: str = '', hbtotal_little: float = .0, hbtotal_medium: float = .0, hstotal_little: float = .0, hstotal_medium: float = .0, htotal_little: float = .0, htotal_medium: float = .0, sbtotal_little: float = .0, sbtotal_medium: float = .0, sstotal_little: float = .0, sstotal_medium: float = .0, stotal_little: float = .0, stotal_medium: float = .0, buytotal_little: float = .0, buytotal_medium: float = .0, selltotal_little: float = .0, selltotal_medium: float = .0, total_little: float = .0, total_medium: float = .0, ValueMode: TShfeFtdcValueModeType = list(TShfeFtdcValueModeType)[0], QryInstPositionRateCnt: int = 1):
        pQryInstPositionRate = CShfeFtdcQryInstPositionRateField()
        pQryInstPositionRate.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryInstPositionRate.InstIDStart = bytes(InstIDStart, encoding='ascii')
        pQryInstPositionRate.InstIDEnd = bytes(InstIDEnd, encoding='ascii')
        pQryInstPositionRate.hbtotal_little = hbtotal_little
        pQryInstPositionRate.hbtotal_medium = hbtotal_medium
        pQryInstPositionRate.hstotal_little = hstotal_little
        pQryInstPositionRate.hstotal_medium = hstotal_medium
        pQryInstPositionRate.htotal_little = htotal_little
        pQryInstPositionRate.htotal_medium = htotal_medium
        pQryInstPositionRate.sbtotal_little = sbtotal_little
        pQryInstPositionRate.sbtotal_medium = sbtotal_medium
        pQryInstPositionRate.sstotal_little = sstotal_little
        pQryInstPositionRate.sstotal_medium = sstotal_medium
        pQryInstPositionRate.stotal_little = stotal_little
        pQryInstPositionRate.stotal_medium = stotal_medium
        pQryInstPositionRate.buytotal_little = buytotal_little
        pQryInstPositionRate.buytotal_medium = buytotal_medium
        pQryInstPositionRate.selltotal_little = selltotal_little
        pQryInstPositionRate.selltotal_medium = selltotal_medium
        pQryInstPositionRate.total_little = total_little
        pQryInstPositionRate.total_medium = total_medium
        pQryInstPositionRate.ValueMode = ValueMode.value
        self.nRequestID += 1
        self.h.ReqQryInstPositionRate(self.api, byref(
            pQryInstPositionRate), QryInstPositionRateCnt, self.nRequestID)

    def ReqQryProductPositionRate(self, BrokerID: str = '', ProductID: str = '', hbtotal_little: float = .0, hbtotal_medium: float = .0, hstotal_little: float = .0, hstotal_medium: float = .0, htotal_little: float = .0, htotal_medium: float = .0, sbtotal_little: float = .0, sbtotal_medium: float = .0, sstotal_little: float = .0, sstotal_medium: float = .0, stotal_little: float = .0, stotal_medium: float = .0, buytotal_little: float = .0, buytotal_medium: float = .0, selltotal_little: float = .0, selltotal_medium: float = .0, total_little: float = .0, total_medium: float = .0, ValueMode: TShfeFtdcValueModeType = list(TShfeFtdcValueModeType)[0]):
        pQryProductPositionRate = CShfeFtdcQryProductPositionRateField()
        pQryProductPositionRate.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryProductPositionRate.ProductID = bytes(ProductID, encoding='ascii')
        pQryProductPositionRate.hbtotal_little = hbtotal_little
        pQryProductPositionRate.hbtotal_medium = hbtotal_medium
        pQryProductPositionRate.hstotal_little = hstotal_little
        pQryProductPositionRate.hstotal_medium = hstotal_medium
        pQryProductPositionRate.htotal_little = htotal_little
        pQryProductPositionRate.htotal_medium = htotal_medium
        pQryProductPositionRate.sbtotal_little = sbtotal_little
        pQryProductPositionRate.sbtotal_medium = sbtotal_medium
        pQryProductPositionRate.sstotal_little = sstotal_little
        pQryProductPositionRate.sstotal_medium = sstotal_medium
        pQryProductPositionRate.stotal_little = stotal_little
        pQryProductPositionRate.stotal_medium = stotal_medium
        pQryProductPositionRate.buytotal_little = buytotal_little
        pQryProductPositionRate.buytotal_medium = buytotal_medium
        pQryProductPositionRate.selltotal_little = selltotal_little
        pQryProductPositionRate.selltotal_medium = selltotal_medium
        pQryProductPositionRate.total_little = total_little
        pQryProductPositionRate.total_medium = total_medium
        pQryProductPositionRate.ValueMode = ValueMode.value
        self.nRequestID += 1
        self.h.ReqQryProductPositionRate(self.api, byref(
            pQryProductPositionRate), self.nRequestID)

    def ReqQryTradingCodeHash(self, InvestorIDBeg: str = '', InvestorIDEnd: str = ''):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryTradingCodeHash(
            self.api, byref(pInvestorIDRange), self.nRequestID)

    def ReqQryTradingCode(self, InvestorIDBeg: str = '', InvestorIDEnd: str = '', InvestorIDRangeCnt: int = 1):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryTradingCode(self.api, byref(
            pInvestorIDRange), InvestorIDRangeCnt, self.nRequestID)

    def ReqSubscribeTrade(self, SequenceNo: int = 1):
        pNotifySequence = CShfeFtdcNotifySequenceField()
        pNotifySequence.SequenceNo = SequenceNo
        self.nRequestID += 1
        self.h.ReqSubscribeTrade(self.api, byref(
            pNotifySequence), self.nRequestID)

    def ReqSubscribeOrder(self, SequenceNo: int = 1):
        pNotifySequence = CShfeFtdcNotifySequenceField()
        pNotifySequence.SequenceNo = SequenceNo
        self.nRequestID += 1
        self.h.ReqSubscribeOrder(self.api, byref(
            pNotifySequence), self.nRequestID)

    def ReqSubBrokerUserEvent(self, SequenceNo: int = 1):
        pNotifySequence = CShfeFtdcNotifySequenceField()
        pNotifySequence.SequenceNo = SequenceNo
        self.nRequestID += 1
        self.h.ReqSubBrokerUserEvent(
            self.api, byref(pNotifySequence), self.nRequestID)

    def ReqRiskOrderInsert(self, FCType: TShfeFtdcForceCloseTypeType = list(TShfeFtdcForceCloseTypeType)[0], Time1: str = '', Millisec1: int = 1, Time2: str = '', Millisec2: int = 1, FCSceneId: str = '', BrokerID: str = '', InvestorID: str = '', InstrumentID: str = '', OrderRef: str = '', UserID: str = '', OrderPriceType: TShfeFtdcOrderPriceTypeType = list(TShfeFtdcOrderPriceTypeType)[0], Direction: TShfeFtdcDirectionType = list(TShfeFtdcDirectionType)[0], CombOffsetFlag: str = '', CombHedgeFlag: str = '', LimitPrice: float = .0, VolumeTotalOriginal: int = 1, TimeCondition: TShfeFtdcTimeConditionType = list(TShfeFtdcTimeConditionType)[0], GTDDate: str = '', VolumeCondition: TShfeFtdcVolumeConditionType = list(TShfeFtdcVolumeConditionType)[0], MinVolume: int = 1, ContingentCondition: TShfeFtdcContingentConditionType = list(TShfeFtdcContingentConditionType)[0], StopPrice: float = .0, ForceCloseReason: TShfeFtdcForceCloseReasonType = list(TShfeFtdcForceCloseReasonType)[0], IsAutoSuspend: int = 1, BusinessUnit: str = '', RequestID: int = 1, UserForceClose: int = 1, FrontID: int = 1, SessionID: int = 1, IsSwapOrder: int = 1, ExchangeID: str = '', InvestUnitID: str = '', AccountID: str = '', CurrencyID: str = '', ClientID: str = '', IPAddress: str = '', MacAddress: str = ''):
        pRiskForceCloseOrder = CShfeFtdcRiskForceCloseOrderField()
        pRiskForceCloseOrder.FCType = FCType.value
        pRiskForceCloseOrder.Time1 = bytes(Time1, encoding='ascii')
        pRiskForceCloseOrder.Millisec1 = Millisec1
        pRiskForceCloseOrder.Time2 = bytes(Time2, encoding='ascii')
        pRiskForceCloseOrder.Millisec2 = Millisec2
        pRiskForceCloseOrder.FCSceneId = bytes(FCSceneId, encoding='ascii')
        pRiskForceCloseOrder.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskForceCloseOrder.InvestorID = bytes(InvestorID, encoding='ascii')
        pRiskForceCloseOrder.InstrumentID = bytes(
            InstrumentID, encoding='ascii')
        pRiskForceCloseOrder.OrderRef = bytes(OrderRef, encoding='ascii')
        pRiskForceCloseOrder.UserID = bytes(UserID, encoding='ascii')
        pRiskForceCloseOrder.OrderPriceType = OrderPriceType.value
        pRiskForceCloseOrder.Direction = Direction.value
        pRiskForceCloseOrder.CombOffsetFlag = bytes(
            CombOffsetFlag, encoding='ascii')
        pRiskForceCloseOrder.CombHedgeFlag = bytes(
            CombHedgeFlag, encoding='ascii')
        pRiskForceCloseOrder.LimitPrice = LimitPrice
        pRiskForceCloseOrder.VolumeTotalOriginal = VolumeTotalOriginal
        pRiskForceCloseOrder.TimeCondition = TimeCondition.value
        pRiskForceCloseOrder.GTDDate = bytes(GTDDate, encoding='ascii')
        pRiskForceCloseOrder.VolumeCondition = VolumeCondition.value
        pRiskForceCloseOrder.MinVolume = MinVolume
        pRiskForceCloseOrder.ContingentCondition = ContingentCondition.value
        pRiskForceCloseOrder.StopPrice = StopPrice
        pRiskForceCloseOrder.ForceCloseReason = ForceCloseReason.value
        pRiskForceCloseOrder.IsAutoSuspend = IsAutoSuspend
        pRiskForceCloseOrder.BusinessUnit = bytes(
            BusinessUnit, encoding='ascii')
        pRiskForceCloseOrder.RequestID = RequestID
        pRiskForceCloseOrder.UserForceClose = UserForceClose
        pRiskForceCloseOrder.FrontID = FrontID
        pRiskForceCloseOrder.SessionID = SessionID
        pRiskForceCloseOrder.IsSwapOrder = IsSwapOrder
        pRiskForceCloseOrder.ExchangeID = bytes(ExchangeID, encoding='ascii')
        pRiskForceCloseOrder.InvestUnitID = bytes(
            InvestUnitID, encoding='ascii')
        pRiskForceCloseOrder.AccountID = bytes(AccountID, encoding='ascii')
        pRiskForceCloseOrder.CurrencyID = bytes(CurrencyID, encoding='ascii')
        pRiskForceCloseOrder.ClientID = bytes(ClientID, encoding='ascii')
        pRiskForceCloseOrder.IPAddress = bytes(IPAddress, encoding='ascii')
        pRiskForceCloseOrder.MacAddress = bytes(MacAddress, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRiskOrderInsert(self.api, byref(
            pRiskForceCloseOrder), self.nRequestID)

    def ReqRiskOrderAction(self, BrokerID: str = '', InvestorID: str = '', OrderActionRef: int = 1, OrderRef: str = '', RequestID: int = 1, FrontID: int = 1, SessionID: int = 1, ExchangeID: str = '', OrderSysID: str = '', ActionFlag: TShfeFtdcActionFlagType = list(TShfeFtdcActionFlagType)[0], LimitPrice: float = .0, VolumeChange: int = 1, UserID: str = '', InstrumentID: str = '', InvestUnitID: str = '', IPAddress: str = '', MacAddress: str = ''):
        pInputOrderAction = CShfeFtdcInputOrderActionField()
        pInputOrderAction.BrokerID = bytes(BrokerID, encoding='ascii')
        pInputOrderAction.InvestorID = bytes(InvestorID, encoding='ascii')
        pInputOrderAction.OrderActionRef = OrderActionRef
        pInputOrderAction.OrderRef = bytes(OrderRef, encoding='ascii')
        pInputOrderAction.RequestID = RequestID
        pInputOrderAction.FrontID = FrontID
        pInputOrderAction.SessionID = SessionID
        pInputOrderAction.ExchangeID = bytes(ExchangeID, encoding='ascii')
        pInputOrderAction.OrderSysID = bytes(OrderSysID, encoding='ascii')
        pInputOrderAction.ActionFlag = ActionFlag.value
        pInputOrderAction.LimitPrice = LimitPrice
        pInputOrderAction.VolumeChange = VolumeChange
        pInputOrderAction.UserID = bytes(UserID, encoding='ascii')
        pInputOrderAction.InstrumentID = bytes(InstrumentID, encoding='ascii')
        pInputOrderAction.InvestUnitID = bytes(InvestUnitID, encoding='ascii')
        pInputOrderAction.IPAddress = bytes(IPAddress, encoding='ascii')
        pInputOrderAction.MacAddress = bytes(MacAddress, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRiskOrderAction(self.api, byref(
            pInputOrderAction), self.nRequestID)

    def ReqSubscribePosition(self, SequenceNo: int = 1):
        pNotifySequence = CShfeFtdcNotifySequenceField()
        pNotifySequence.SequenceNo = SequenceNo
        self.nRequestID += 1
        self.h.ReqSubscribePosition(
            self.api, byref(pNotifySequence), self.nRequestID)

    def ReqRiskNotifyCommand(self, BrokerID: str = '', UserID: str = '', NotifyClass: TShfeFtdcNotifyClassType = list(TShfeFtdcNotifyClassType)[0], InvestorID: str = '', IsAutoSystem: int = 1, IsAutoSMS: int = 1, IsAutoEmail: int = 1, Reserve: str = '', Pattern: str = '', IsNormal: int = 1, IsWarn: int = 1, CurrencyID: str = ''):
        pRiskNotifyCommand = CShfeFtdcRiskNotifyCommandField()
        pRiskNotifyCommand.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskNotifyCommand.UserID = bytes(UserID, encoding='ascii')
        pRiskNotifyCommand.NotifyClass = NotifyClass.value
        pRiskNotifyCommand.InvestorID = bytes(InvestorID, encoding='ascii')
        pRiskNotifyCommand.IsAutoSystem = IsAutoSystem
        pRiskNotifyCommand.IsAutoSMS = IsAutoSMS
        pRiskNotifyCommand.IsAutoEmail = IsAutoEmail
        pRiskNotifyCommand.Reserve = bytes(Reserve, encoding='ascii')
        pRiskNotifyCommand.Pattern = bytes(Pattern, encoding='ascii')
        pRiskNotifyCommand.IsNormal = IsNormal
        pRiskNotifyCommand.IsWarn = IsWarn
        pRiskNotifyCommand.CurrencyID = bytes(CurrencyID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRiskNotifyCommand(self.api, byref(
            pRiskNotifyCommand), self.nRequestID)

    def ReqBatchForceCloseCalc(self, ForceCloseLevel: TShfeFtdcForceCloseLevelType = list(TShfeFtdcForceCloseLevelType)[0], ForceCloseRelease: TShfeFtdcForceCloseReleaseType = list(TShfeFtdcForceCloseReleaseType)[0], FCNonLimitFirst: int = 1, FCPosiProfitLossFirst: int = 1, FCCustomAmount: float = .0, FCCustomRiskLevel: float = .0, ProductInstrumentID: str = '', FCPosiDirection: TShfeFtdcForceClosePosiDirectionType = list(TShfeFtdcForceClosePosiDirectionType)[0], FCHedgeFlag: TShfeFtdcForceCloseHedgeFlagType = list(TShfeFtdcForceCloseHedgeFlagType)[0], FCCombPosiFlag: TShfeFtdcForceCloseCombPosiFlagType = list(TShfeFtdcForceCloseCombPosiFlagType)[0], FCHistoryPosiOrder: TShfeFtdcForceCloseHistoryPosiOrderType = list(TShfeFtdcForceCloseHistoryPosiOrderType)[0], FCPrice: TShfeFtdcForceClosePriceTypeType = list(TShfeFtdcForceClosePriceTypeType)[0], PriceTick: int = 1, FCRulePriority: str = '', ForceClosePositionRuleCnt: int = 1, BrokerID: str = '', InvestorID: str = '', ForceCloseListCnt: int = 1):
        pForceCloseStandard = CShfeFtdcForceCloseStandardField()
        pForceCloseStandard.ForceCloseLevel = ForceCloseLevel.value
        pForceCloseStandard.ForceCloseRelease = ForceCloseRelease.value
        pForceCloseStandard.FCNonLimitFirst = FCNonLimitFirst
        pForceCloseStandard.FCPosiProfitLossFirst = FCPosiProfitLossFirst
        pForceCloseStandard.FCCustomAmount = FCCustomAmount
        pForceCloseStandard.FCCustomRiskLevel = FCCustomRiskLevel
        pForceClosePositionRule = CShfeFtdcForceClosePositionRuleField()
        pForceClosePositionRule.ProductInstrumentID = bytes(
            ProductInstrumentID, encoding='ascii')
        pForceClosePositionRule.FCPosiDirection = FCPosiDirection.value
        pForceClosePositionRule.FCHedgeFlag = FCHedgeFlag.value
        pForceClosePositionRule.FCCombPosiFlag = FCCombPosiFlag.value
        pForceClosePositionRule.FCHistoryPosiOrder = FCHistoryPosiOrder.value
        pForceClosePositionRule.FCPrice = FCPrice.value
        pForceClosePositionRule.PriceTick = PriceTick
        pForceClosePositionRule.FCRulePriority = bytes(
            FCRulePriority, encoding='ascii')
        pForceCloseList = CShfeFtdcForceCloseListField()
        pForceCloseList.BrokerID = bytes(BrokerID, encoding='ascii')
        pForceCloseList.InvestorID = bytes(InvestorID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqBatchForceCloseCalc(self.api, byref(pForceCloseStandard), byref(
            pForceClosePositionRule), ForceClosePositionRuleCnt, byref(pForceCloseList), ForceCloseListCnt, self.nRequestID)

    def ReqForceCloseCalc(self, ForceCloseLevel: TShfeFtdcForceCloseLevelType = list(TShfeFtdcForceCloseLevelType)[0], ForceCloseRelease: TShfeFtdcForceCloseReleaseType = list(TShfeFtdcForceCloseReleaseType)[0], FCNonLimitFirst: int = 1, FCPosiProfitLossFirst: int = 1, FCCustomAmount: float = .0, FCCustomRiskLevel: float = .0, InstrumentID: str = '', BrokerID: str = '', InvestorID: str = '', PosiDirection: TShfeFtdcPosiDirectionType = list(TShfeFtdcPosiDirectionType)[0], HedgeFlag: TShfeFtdcHedgeFlagType = list(TShfeFtdcHedgeFlagType)[0], PositionDate: TShfeFtdcPositionDateType = list(TShfeFtdcPositionDateType)[0], Position: int = 1, FCPosition: int = 1, FCPriceType: TShfeFtdcForceClosePriceTypeType = list(TShfeFtdcForceClosePriceTypeType)[0], PriceTick: int = 1, FCPrice: float = .0, ReleaseMargin: float = .0, CloseProfit: float = .0, ExchReleaseMargin: float = .0, PosiProfit: float = .0, CashIn: float = .0, OptionValue: float = .0, ForceClosePositionCnt: int = 1):
        pForceCloseStandard = CShfeFtdcForceCloseStandardField()
        pForceCloseStandard.ForceCloseLevel = ForceCloseLevel.value
        pForceCloseStandard.ForceCloseRelease = ForceCloseRelease.value
        pForceCloseStandard.FCNonLimitFirst = FCNonLimitFirst
        pForceCloseStandard.FCPosiProfitLossFirst = FCPosiProfitLossFirst
        pForceCloseStandard.FCCustomAmount = FCCustomAmount
        pForceCloseStandard.FCCustomRiskLevel = FCCustomRiskLevel
        pForceClosePosition = CShfeFtdcForceClosePositionField()
        pForceClosePosition.InstrumentID = bytes(
            InstrumentID, encoding='ascii')
        pForceClosePosition.BrokerID = bytes(BrokerID, encoding='ascii')
        pForceClosePosition.InvestorID = bytes(InvestorID, encoding='ascii')
        pForceClosePosition.PosiDirection = PosiDirection.value
        pForceClosePosition.HedgeFlag = HedgeFlag.value
        pForceClosePosition.PositionDate = PositionDate.value
        pForceClosePosition.Position = Position
        pForceClosePosition.FCPosition = FCPosition
        pForceClosePosition.FCPriceType = FCPriceType.value
        pForceClosePosition.PriceTick = PriceTick
        pForceClosePosition.FCPrice = FCPrice
        pForceClosePosition.ReleaseMargin = ReleaseMargin
        pForceClosePosition.CloseProfit = CloseProfit
        pForceClosePosition.ExchReleaseMargin = ExchReleaseMargin
        pForceClosePosition.PosiProfit = PosiProfit
        pForceClosePosition.CashIn = CashIn
        pForceClosePosition.OptionValue = OptionValue
        pForceCloseList = CShfeFtdcForceCloseListField()
        self.nRequestID += 1
        self.h.ReqForceCloseCalc(self.api, byref(pForceCloseStandard), byref(
            pForceClosePosition), ForceClosePositionCnt, byref(pForceCloseList), self.nRequestID)

    def ReqSetIndexNPPParam(self, BrokerID: str = '', InvestorID: str = '', ProductIDs: str = '', WarnLevel: float = .0):
        pIndexNPPParam = CShfeFtdcIndexNPPParamField()
        pIndexNPPParam.BrokerID = bytes(BrokerID, encoding='ascii')
        pIndexNPPParam.InvestorID = bytes(InvestorID, encoding='ascii')
        pIndexNPPParam.ProductIDs = bytes(ProductIDs, encoding='ascii')
        pIndexNPPParam.WarnLevel = WarnLevel
        self.nRequestID += 1
        self.h.ReqSetIndexNPPParam(
            self.api, byref(pIndexNPPParam), self.nRequestID)

    def ReqRemIndexNPPParam(self, BrokerID: str = '', InvestorID: str = '', ProductIDs: str = '', WarnLevel: float = .0):
        pIndexNPPParam = CShfeFtdcIndexNPPParamField()
        pIndexNPPParam.BrokerID = bytes(BrokerID, encoding='ascii')
        pIndexNPPParam.InvestorID = bytes(InvestorID, encoding='ascii')
        pIndexNPPParam.ProductIDs = bytes(ProductIDs, encoding='ascii')
        pIndexNPPParam.WarnLevel = WarnLevel
        self.nRequestID += 1
        self.h.ReqRemIndexNPPParam(
            self.api, byref(pIndexNPPParam), self.nRequestID)

    def ReqQryLogin(self, BrokerID: str = '', UserID: str = ''):
        pNormalRiskQuery = CShfeFtdcNormalRiskQueryField()
        pNormalRiskQuery.BrokerID = bytes(BrokerID, encoding='ascii')
        pNormalRiskQuery.UserID = bytes(UserID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryLogin(self.api, byref(pNormalRiskQuery), self.nRequestID)

    def ReqQryPriceVaryEffect(self, BrokerID: str = '', InvestorID: str = '', RiskLevel: TShfeFtdcNotifyClassType = list(TShfeFtdcNotifyClassType)[0]):
        pQryPriceVaryEffect = CShfeFtdcQryPriceVaryEffectField()
        pQryPriceVaryEffect.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryPriceVaryEffect.InvestorID = bytes(InvestorID, encoding='ascii')
        pQryPriceVaryEffect.RiskLevel = RiskLevel.value
        self.nRequestID += 1
        self.h.ReqQryPriceVaryEffect(self.api, byref(
            pQryPriceVaryEffect), self.nRequestID)

    def ReqQrySafePriceRange(self, PriceVaryAlgo: TShfeFtdcPriceVaryAlgoType = list(TShfeFtdcPriceVaryAlgoType)[0], RiskLevel: TShfeFtdcNotifyClassType = list(TShfeFtdcNotifyClassType)[0], MaxLimitDay: int = 1, InstrumentID: str = '', Direction: TShfeFtdcPriceVaryDirType = list(TShfeFtdcPriceVaryDirType)[0], Pecent: float = .0, BasePriceType: TShfeFtdcPriceTypeType = list(TShfeFtdcPriceTypeType)[0], BasePrice: float = .0, PriceVaryParamCnt: int = 1, BrokerID: str = '', InvestorID: str = '', CurrencyID: str = '', BrokerInvestorCurrencyCnt: int = 1):
        pQrySafePriceRange = CShfeFtdcQrySafePriceRangeField()
        pQrySafePriceRange.PriceVaryAlgo = PriceVaryAlgo.value
        pQrySafePriceRange.RiskLevel = RiskLevel.value
        pQrySafePriceRange.MaxLimitDay = MaxLimitDay
        pPriceVaryParam = CShfeFtdcPriceVaryParamField()
        pPriceVaryParam.InstrumentID = bytes(InstrumentID, encoding='ascii')
        pPriceVaryParam.Direction = Direction.value
        pPriceVaryParam.Pecent = Pecent
        pPriceVaryParam.BasePriceType = BasePriceType.value
        pPriceVaryParam.BasePrice = BasePrice
        pBrokerInvestorCurrency = CShfeFtdcBrokerInvestorCurrencyField()
        pBrokerInvestorCurrency.BrokerID = bytes(BrokerID, encoding='ascii')
        pBrokerInvestorCurrency.InvestorID = bytes(
            InvestorID, encoding='ascii')
        pBrokerInvestorCurrency.CurrencyID = bytes(
            CurrencyID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQrySafePriceRange(self.api, byref(pQrySafePriceRange), byref(
            pPriceVaryParam), PriceVaryParamCnt, byref(pBrokerInvestorCurrency), BrokerInvestorCurrencyCnt, self.nRequestID)

    def ReqRiskParkedOrderInsert(self, ParkedOrderID: str = '', LocalID: str = '', UserType: TShfeFtdcRiskUserTypeType = list(TShfeFtdcRiskUserTypeType)[0], Status: TShfeFtdcRiskParkedOrderStatusType = list(TShfeFtdcRiskParkedOrderStatusType)[0], StatusMsg: str = '', TriggerType: TShfeFtdcOrderTriggerTypeType = list(TShfeFtdcOrderTriggerTypeType)[0], TradeSegment: int = 1, ExchangeID: str = '', FCType: TShfeFtdcForceCloseTypeType = list(TShfeFtdcForceCloseTypeType)[0], Time1: str = '', Millisec1: int = 1, Time2: str = '', Millisec2: int = 1, FCSceneId: str = '', BrokerID: str = '', InvestorID: str = '', InstrumentID: str = '', OrderRef: str = '', UserID: str = '', OrderPriceType: TShfeFtdcOrderPriceTypeType = list(TShfeFtdcOrderPriceTypeType)[0], Direction: TShfeFtdcDirectionType = list(TShfeFtdcDirectionType)[0], CombOffsetFlag: str = '', CombHedgeFlag: str = '', LimitPrice: float = .0, VolumeTotalOriginal: int = 1, TimeCondition: TShfeFtdcTimeConditionType = list(TShfeFtdcTimeConditionType)[0], GTDDate: str = '', VolumeCondition: TShfeFtdcVolumeConditionType = list(TShfeFtdcVolumeConditionType)[0], MinVolume: int = 1, ContingentCondition: TShfeFtdcContingentConditionType = list(TShfeFtdcContingentConditionType)[0], StopPrice: float = .0, ForceCloseReason: TShfeFtdcForceCloseReasonType = list(TShfeFtdcForceCloseReasonType)[0], IsAutoSuspend: int = 1, BusinessUnit: str = '', RequestID: int = 1, UserForceClose: int = 1, OrderSubmitStatus: TShfeFtdcOrderSubmitStatusType = list(TShfeFtdcOrderSubmitStatusType)[0], OrderStatus: TShfeFtdcOrderStatusType = list(TShfeFtdcOrderStatusType)[0], OrderStatusMsg: str = '', ErrorID: int = 1, ErrorMsg: str = '', ParkedTime: str = '', OriginalParkedVol: int = 1, MaxCloseVol1: int = 1, MaxCloseVol2: int = 1, Call1: float = .0, Call2: float = .0, MoneyIO1: float = .0, MoneyIO2: float = .0, DeleteReason: str = '', ForceCloseRelease: TShfeFtdcForceCloseReleaseType = list(TShfeFtdcForceCloseReleaseType)[0], IsSwapOrder: int = 1, InvestUnitID: str = '', AccountID: str = '', CurrencyID: str = '', ClientID: str = '', IPAddress: str = '', MacAddress: str = ''):
        pRiskParkedOrder = CShfeFtdcRiskParkedOrderField()
        pRiskParkedOrder.ParkedOrderID = bytes(ParkedOrderID, encoding='ascii')
        pRiskParkedOrder.LocalID = bytes(LocalID, encoding='ascii')
        pRiskParkedOrder.UserType = UserType.value
        pRiskParkedOrder.Status = Status.value
        pRiskParkedOrder.StatusMsg = bytes(StatusMsg, encoding='ascii')
        pRiskParkedOrder.TriggerType = TriggerType.value
        pRiskParkedOrder.TradeSegment = TradeSegment
        pRiskParkedOrder.ExchangeID = bytes(ExchangeID, encoding='ascii')
        pRiskParkedOrder.FCType = FCType.value
        pRiskParkedOrder.Time1 = bytes(Time1, encoding='ascii')
        pRiskParkedOrder.Millisec1 = Millisec1
        pRiskParkedOrder.Time2 = bytes(Time2, encoding='ascii')
        pRiskParkedOrder.Millisec2 = Millisec2
        pRiskParkedOrder.FCSceneId = bytes(FCSceneId, encoding='ascii')
        pRiskParkedOrder.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskParkedOrder.InvestorID = bytes(InvestorID, encoding='ascii')
        pRiskParkedOrder.InstrumentID = bytes(InstrumentID, encoding='ascii')
        pRiskParkedOrder.OrderRef = bytes(OrderRef, encoding='ascii')
        pRiskParkedOrder.UserID = bytes(UserID, encoding='ascii')
        pRiskParkedOrder.OrderPriceType = OrderPriceType.value
        pRiskParkedOrder.Direction = Direction.value
        pRiskParkedOrder.CombOffsetFlag = bytes(
            CombOffsetFlag, encoding='ascii')
        pRiskParkedOrder.CombHedgeFlag = bytes(CombHedgeFlag, encoding='ascii')
        pRiskParkedOrder.LimitPrice = LimitPrice
        pRiskParkedOrder.VolumeTotalOriginal = VolumeTotalOriginal
        pRiskParkedOrder.TimeCondition = TimeCondition.value
        pRiskParkedOrder.GTDDate = bytes(GTDDate, encoding='ascii')
        pRiskParkedOrder.VolumeCondition = VolumeCondition.value
        pRiskParkedOrder.MinVolume = MinVolume
        pRiskParkedOrder.ContingentCondition = ContingentCondition.value
        pRiskParkedOrder.StopPrice = StopPrice
        pRiskParkedOrder.ForceCloseReason = ForceCloseReason.value
        pRiskParkedOrder.IsAutoSuspend = IsAutoSuspend
        pRiskParkedOrder.BusinessUnit = bytes(BusinessUnit, encoding='ascii')
        pRiskParkedOrder.RequestID = RequestID
        pRiskParkedOrder.UserForceClose = UserForceClose
        pRiskParkedOrder.OrderSubmitStatus = OrderSubmitStatus.value
        pRiskParkedOrder.OrderStatus = OrderStatus.value
        pRiskParkedOrder.OrderStatusMsg = bytes(
            OrderStatusMsg, encoding='ascii')
        pRiskParkedOrder.ErrorID = ErrorID
        pRiskParkedOrder.ErrorMsg = bytes(ErrorMsg, encoding='ascii')
        pRiskParkedOrder.ParkedTime = bytes(ParkedTime, encoding='ascii')
        pRiskParkedOrder.OriginalParkedVol = OriginalParkedVol
        pRiskParkedOrder.MaxCloseVol1 = MaxCloseVol1
        pRiskParkedOrder.MaxCloseVol2 = MaxCloseVol2
        pRiskParkedOrder.Call1 = Call1
        pRiskParkedOrder.Call2 = Call2
        pRiskParkedOrder.MoneyIO1 = MoneyIO1
        pRiskParkedOrder.MoneyIO2 = MoneyIO2
        pRiskParkedOrder.DeleteReason = bytes(DeleteReason, encoding='ascii')
        pRiskParkedOrder.ForceCloseRelease = ForceCloseRelease.value
        pRiskParkedOrder.IsSwapOrder = IsSwapOrder
        pRiskParkedOrder.InvestUnitID = bytes(InvestUnitID, encoding='ascii')
        pRiskParkedOrder.AccountID = bytes(AccountID, encoding='ascii')
        pRiskParkedOrder.CurrencyID = bytes(CurrencyID, encoding='ascii')
        pRiskParkedOrder.ClientID = bytes(ClientID, encoding='ascii')
        pRiskParkedOrder.IPAddress = bytes(IPAddress, encoding='ascii')
        pRiskParkedOrder.MacAddress = bytes(MacAddress, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRiskParkedOrderInsert(
            self.api, byref(pRiskParkedOrder), self.nRequestID)

    def ReqRemoveRiskParkedOrder(self, BrokerID: str = '', UserID: str = '', InvestorID: str = '', ParkedOrderID: str = ''):
        pRemoveRiskParkedOrder = CShfeFtdcRemoveRiskParkedOrderField()
        pRemoveRiskParkedOrder.BrokerID = bytes(BrokerID, encoding='ascii')
        pRemoveRiskParkedOrder.UserID = bytes(UserID, encoding='ascii')
        pRemoveRiskParkedOrder.InvestorID = bytes(InvestorID, encoding='ascii')
        pRemoveRiskParkedOrder.ParkedOrderID = bytes(
            ParkedOrderID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRemoveRiskParkedOrder(self.api, byref(
            pRemoveRiskParkedOrder), self.nRequestID)

    def ReqSubRiskParkedOrder(self, SequenceNo: int = 1):
        pNotifySequence = CShfeFtdcNotifySequenceField()
        pNotifySequence.SequenceNo = SequenceNo
        self.nRequestID += 1
        self.h.ReqSubRiskParkedOrder(
            self.api, byref(pNotifySequence), self.nRequestID)

    def ReqRiskUserPasswordUpd(self, BrokerID: str = '', UserID: str = '', OldPassword: str = '', NewPassword: str = ''):
        pUserPasswordUpdate = CShfeFtdcUserPasswordUpdateField()
        pUserPasswordUpdate.BrokerID = bytes(BrokerID, encoding='ascii')
        pUserPasswordUpdate.UserID = bytes(UserID, encoding='ascii')
        pUserPasswordUpdate.OldPassword = bytes(OldPassword, encoding='ascii')
        pUserPasswordUpdate.NewPassword = bytes(NewPassword, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRiskUserPasswordUpd(self.api, byref(
            pUserPasswordUpdate), self.nRequestID)

    def ReqSubSeqDeposit(self, SequenceNo: int = 1, DataType: str = ''):
        pRiskNtfSequence = CShfeFtdcRiskNtfSequenceField()
        pRiskNtfSequence.SequenceNo = SequenceNo
        pRiskNtfSequence.DataType = bytes(DataType, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqSubSeqDeposit(self.api, byref(
            pRiskNtfSequence), self.nRequestID)

    def ReqAddRiskUserEvent(self, SequenceNo: int = 1, EventDate: str = '', EventTime: str = '', BrokerID: str = '', UserID: str = '', EventType: TShfeFtdcRiskUserEventType = list(TShfeFtdcRiskUserEventType)[0], EventInfo: str = '', TradingDay: str = ''):
        pRiskUserEvent = CShfeFtdcRiskUserEventField()
        pRiskUserEvent.SequenceNo = SequenceNo
        pRiskUserEvent.EventDate = bytes(EventDate, encoding='ascii')
        pRiskUserEvent.EventTime = bytes(EventTime, encoding='ascii')
        pRiskUserEvent.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskUserEvent.UserID = bytes(UserID, encoding='ascii')
        pRiskUserEvent.EventType = EventType.value
        pRiskUserEvent.EventInfo = bytes(EventInfo, encoding='ascii')
        pRiskUserEvent.TradingDay = bytes(TradingDay, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqAddRiskUserEvent(
            self.api, byref(pRiskUserEvent), self.nRequestID)

    def ReqQryPredictRisk(self, D1: int = 1, IsFilter: int = 1, BrokerID: str = '', InvestorID: str = '', BrokerInvestorCnt: int = 1, ProductID: str = '', Limit1: float = .0, Limit2: float = .0, Limit3: float = .0, Limit4: float = .0, MaxMarginRate1: float = .0, Price: float = .0, ProductLimitsCnt: int = 1):
        pPredictRiskParam = CShfeFtdcPredictRiskParamField()
        pPredictRiskParam.D1 = D1
        pPredictRiskParam.IsFilter = IsFilter
        pBrokerInvestor = CShfeFtdcBrokerInvestorField()
        pBrokerInvestor.BrokerID = bytes(BrokerID, encoding='ascii')
        pBrokerInvestor.InvestorID = bytes(InvestorID, encoding='ascii')
        pProductLimits = CShfeFtdcProductLimitsField()
        pProductLimits.ProductID = bytes(ProductID, encoding='ascii')
        pProductLimits.Limit1 = Limit1
        pProductLimits.Limit2 = Limit2
        pProductLimits.Limit3 = Limit3
        pProductLimits.Limit4 = Limit4
        pProductLimits.MaxMarginRate1 = MaxMarginRate1
        pProductLimits.Price = Price
        self.nRequestID += 1
        self.h.ReqQryPredictRisk(self.api, byref(pPredictRiskParam), byref(
            pBrokerInvestor), BrokerInvestorCnt, byref(pProductLimits), ProductLimitsCnt, self.nRequestID)

    def ReqQryInvestorLinkMan(self, InvestorIDBeg: str = '', InvestorIDEnd: str = '', InvestorIDRangeCnt: int = 1):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryInvestorLinkMan(self.api, byref(
            pInvestorIDRange), InvestorIDRangeCnt, self.nRequestID)

    def ReqQryInvestorDepartment(self, InvestorIDBeg: str = '', InvestorIDEnd: str = '', InvestorIDRangeCnt: int = 1):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryInvestorDepartment(self.api, byref(
            pInvestorIDRange), InvestorIDRangeCnt, self.nRequestID)

    def ReqSubPreRiskAccount(self, SequenceNo: int = 1, DataType: str = ''):
        pRiskNtfSequence = CShfeFtdcRiskNtfSequenceField()
        pRiskNtfSequence.SequenceNo = SequenceNo
        pRiskNtfSequence.DataType = bytes(DataType, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqSubPreRiskAccount(self.api, byref(
            pRiskNtfSequence), self.nRequestID)

    def ReqModNoticePattern(self, BrokerID: str = '', BizType: str = '', Method: TShfeFtdcRiskNotifyMethodType = list(TShfeFtdcRiskNotifyMethodType)[0], BizName: str = '', UserID: str = '', IsActive: int = 1, Pattern: str = ''):
        pNoticePattern = CShfeFtdcNoticePatternField()
        pNoticePattern.BrokerID = bytes(BrokerID, encoding='ascii')
        pNoticePattern.BizType = bytes(BizType, encoding='ascii')
        pNoticePattern.Method = Method.value
        pNoticePattern.BizName = bytes(BizName, encoding='ascii')
        pNoticePattern.UserID = bytes(UserID, encoding='ascii')
        pNoticePattern.IsActive = IsActive
        pNoticePattern.Pattern = bytes(Pattern, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqModNoticePattern(
            self.api, byref(pNoticePattern), self.nRequestID)

    def ReqSubVaryMarketData(self, InstrumentID: str = '', Price1: float = .0, Price2: float = .0, PriceRangeCnt: int = 1):
        pPriceRange = CShfeFtdcPriceRangeField()
        pPriceRange.InstrumentID = bytes(InstrumentID, encoding='ascii')
        pPriceRange.Price1 = Price1
        pPriceRange.Price2 = Price2
        self.nRequestID += 1
        self.h.ReqSubVaryMarketData(self.api, byref(
            pPriceRange), PriceRangeCnt, self.nRequestID)

    def ReqUnSubVaryMarketData(self, InstrumentID: str = '', SubMarketDataCnt: int = 1):
        pSubMarketData = CShfeFtdcSubMarketDataField()
        pSubMarketData.InstrumentID = bytes(InstrumentID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqUnSubVaryMarketData(self.api, byref(
            pSubMarketData), SubMarketDataCnt, self.nRequestID)

    def ReqAddRiskNotifyA(self, SequenceNo: int = 1, EventDate: str = '', EventTime: str = '', BrokerID: str = '', UserID: str = '', InvestorID: str = '', NotifyClass: TShfeFtdcNotifyClassType = list(TShfeFtdcNotifyClassType)[0], NotifyMethod: TShfeFtdcRiskNotifyMethodType = list(TShfeFtdcRiskNotifyMethodType)[0], NotifyStatus: TShfeFtdcRiskNotifyStatusType = list(TShfeFtdcRiskNotifyStatusType)[0], Message: str = '', Reserve: str = '', CurrencyID: str = ''):
        pRiskNotifyA = CShfeFtdcRiskNotifyAField()
        pRiskNotifyA.SequenceNo = SequenceNo
        pRiskNotifyA.EventDate = bytes(EventDate, encoding='ascii')
        pRiskNotifyA.EventTime = bytes(EventTime, encoding='ascii')
        pRiskNotifyA.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskNotifyA.UserID = bytes(UserID, encoding='ascii')
        pRiskNotifyA.InvestorID = bytes(InvestorID, encoding='ascii')
        pRiskNotifyA.NotifyClass = NotifyClass.value
        pRiskNotifyA.NotifyMethod = NotifyMethod.value
        pRiskNotifyA.NotifyStatus = NotifyStatus.value
        pRiskNotifyA.Message = bytes(Message, encoding='ascii')
        pRiskNotifyA.Reserve = bytes(Reserve, encoding='ascii')
        pRiskNotifyA.CurrencyID = bytes(CurrencyID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqAddRiskNotifyA(
            self.api, byref(pRiskNotifyA), self.nRequestID)

    def ReqAddBizNotice(self, TradingDay: str = '', SequenceNo: int = 1, Method: TShfeFtdcRiskNotifyMethodType = list(TShfeFtdcRiskNotifyMethodType)[0], EventTime: str = '', BrokerID: str = '', UserID: str = '', InvestorID: str = '', BizType: str = '', Status: TShfeFtdcRiskNotifyStatusType = list(TShfeFtdcRiskNotifyStatusType)[0], Message: str = '', ErrorMsg: str = ''):
        pBizNotice = CShfeFtdcBizNoticeField()
        pBizNotice.TradingDay = bytes(TradingDay, encoding='ascii')
        pBizNotice.SequenceNo = SequenceNo
        pBizNotice.Method = Method.value
        pBizNotice.EventTime = bytes(EventTime, encoding='ascii')
        pBizNotice.BrokerID = bytes(BrokerID, encoding='ascii')
        pBizNotice.UserID = bytes(UserID, encoding='ascii')
        pBizNotice.InvestorID = bytes(InvestorID, encoding='ascii')
        pBizNotice.BizType = bytes(BizType, encoding='ascii')
        pBizNotice.Status = Status.value
        pBizNotice.Message = bytes(Message, encoding='ascii')
        pBizNotice.ErrorMsg = bytes(ErrorMsg, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqAddBizNotice(self.api, byref(pBizNotice), self.nRequestID)

    def ReqSubSeqData(self, SequenceNo: int = 1, DataType: str = ''):
        pRiskNtfSequence = CShfeFtdcRiskNtfSequenceField()
        pRiskNtfSequence.SequenceNo = SequenceNo
        pRiskNtfSequence.DataType = bytes(DataType, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqSubSeqData(self.api, byref(
            pRiskNtfSequence), self.nRequestID)

    def ReqRiskQryBrokerDeposit(self, BrokerID: str = '', ExchangeID: str = ''):
        pQueryBrokerDeposit = CShfeFtdcQueryBrokerDepositField()
        pQueryBrokerDeposit.BrokerID = bytes(BrokerID, encoding='ascii')
        pQueryBrokerDeposit.ExchangeID = bytes(ExchangeID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRiskQryBrokerDeposit(self.api, byref(
            pQueryBrokerDeposit), self.nRequestID)

    def ReqModRiskInvestorParam(self, ParamID: int = 1, BrokerID: str = '', InvestorID: str = '', ParamValue: str = ''):
        pRiskInvestorParam = CShfeFtdcRiskInvestorParamField()
        pRiskInvestorParam.ParamID = ParamID
        pRiskInvestorParam.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskInvestorParam.InvestorID = bytes(InvestorID, encoding='ascii')
        pRiskInvestorParam.ParamValue = bytes(ParamValue, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqModRiskInvestorParam(
            self.api, byref(pRiskInvestorParam), self.nRequestID)

    def ReqRemRiskInvestorParam(self, ParamID: int = 1, BrokerID: str = '', InvestorID: str = '', ParamValue: str = ''):
        pRiskInvestorParam = CShfeFtdcRiskInvestorParamField()
        pRiskInvestorParam.ParamID = ParamID
        pRiskInvestorParam.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskInvestorParam.InvestorID = bytes(InvestorID, encoding='ascii')
        pRiskInvestorParam.ParamValue = bytes(ParamValue, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRemRiskInvestorParam(
            self.api, byref(pRiskInvestorParam), self.nRequestID)

    def ReqForceRiskUserLogout(self, BrokerID: str = '', UserID: str = '', LocalSessionID: int = 1, SessionID: int = 1, FrontID: int = 1):
        pRiskLoginInfo = CShfeFtdcRiskLoginInfoField()
        pRiskLoginInfo.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskLoginInfo.UserID = bytes(UserID, encoding='ascii')
        pRiskLoginInfo.LocalSessionID = LocalSessionID
        pRiskLoginInfo.SessionID = SessionID
        pRiskLoginInfo.FrontID = FrontID
        self.nRequestID += 1
        self.h.ReqForceRiskUserLogout(
            self.api, byref(pRiskLoginInfo), self.nRequestID)

    def ReqAddRiskPattern(self, BrokerID: str = '', BizType: str = '', PatternID: int = 1, PatternName: str = '', Pattern: str = ''):
        pRiskPattern = CShfeFtdcRiskPatternField()
        pRiskPattern.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskPattern.BizType = bytes(BizType, encoding='ascii')
        pRiskPattern.PatternID = PatternID
        pRiskPattern.PatternName = bytes(PatternName, encoding='ascii')
        pRiskPattern.Pattern = bytes(Pattern, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqAddRiskPattern(
            self.api, byref(pRiskPattern), self.nRequestID)

    def ReqModRiskPattern(self, BrokerID: str = '', BizType: str = '', PatternID: int = 1, PatternName: str = '', Pattern: str = ''):
        pRiskPattern = CShfeFtdcRiskPatternField()
        pRiskPattern.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskPattern.BizType = bytes(BizType, encoding='ascii')
        pRiskPattern.PatternID = PatternID
        pRiskPattern.PatternName = bytes(PatternName, encoding='ascii')
        pRiskPattern.Pattern = bytes(Pattern, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqModRiskPattern(
            self.api, byref(pRiskPattern), self.nRequestID)

    def ReqRemRiskPattern(self, BrokerID: str = '', BizType: str = '', PatternID: int = 1, PatternName: str = '', Pattern: str = ''):
        pRiskPattern = CShfeFtdcRiskPatternField()
        pRiskPattern.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskPattern.BizType = bytes(BizType, encoding='ascii')
        pRiskPattern.PatternID = PatternID
        pRiskPattern.PatternName = bytes(PatternName, encoding='ascii')
        pRiskPattern.Pattern = bytes(Pattern, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqRemRiskPattern(
            self.api, byref(pRiskPattern), self.nRequestID)

    def ReqAddInvestorPattern(self, BrokerID: str = '', InvestorID: str = '', BizType: str = '', Method: TShfeFtdcRiskNotifyMethodType = list(TShfeFtdcRiskNotifyMethodType)[0], PatternID: int = 1, IsActive: int = 1, InvestorPatternCnt: int = 1):
        pInvestorPattern = CShfeFtdcInvestorPatternField()
        pInvestorPattern.BrokerID = bytes(BrokerID, encoding='ascii')
        pInvestorPattern.InvestorID = bytes(InvestorID, encoding='ascii')
        pInvestorPattern.BizType = bytes(BizType, encoding='ascii')
        pInvestorPattern.Method = Method.value
        pInvestorPattern.PatternID = PatternID
        pInvestorPattern.IsActive = IsActive
        self.nRequestID += 1
        self.h.ReqAddInvestorPattern(self.api, byref(
            pInvestorPattern), InvestorPatternCnt, self.nRequestID)

    def ReqModInvestorPattern(self, BrokerID: str = '', InvestorID: str = '', BizType: str = '', Method: TShfeFtdcRiskNotifyMethodType = list(TShfeFtdcRiskNotifyMethodType)[0], PatternID: int = 1, IsActive: int = 1, InvestorPatternCnt: int = 1):
        pInvestorPattern = CShfeFtdcInvestorPatternField()
        pInvestorPattern.BrokerID = bytes(BrokerID, encoding='ascii')
        pInvestorPattern.InvestorID = bytes(InvestorID, encoding='ascii')
        pInvestorPattern.BizType = bytes(BizType, encoding='ascii')
        pInvestorPattern.Method = Method.value
        pInvestorPattern.PatternID = PatternID
        pInvestorPattern.IsActive = IsActive
        self.nRequestID += 1
        self.h.ReqModInvestorPattern(self.api, byref(
            pInvestorPattern), InvestorPatternCnt, self.nRequestID)

    def ReqRemInvestorPattern(self, BrokerID: str = '', InvestorID: str = '', BizType: str = '', Method: TShfeFtdcRiskNotifyMethodType = list(TShfeFtdcRiskNotifyMethodType)[0], PatternID: int = 1, IsActive: int = 1, InvestorPatternCnt: int = 1):
        pInvestorPattern = CShfeFtdcInvestorPatternField()
        pInvestorPattern.BrokerID = bytes(BrokerID, encoding='ascii')
        pInvestorPattern.InvestorID = bytes(InvestorID, encoding='ascii')
        pInvestorPattern.BizType = bytes(BizType, encoding='ascii')
        pInvestorPattern.Method = Method.value
        pInvestorPattern.PatternID = PatternID
        pInvestorPattern.IsActive = IsActive
        self.nRequestID += 1
        self.h.ReqRemInvestorPattern(self.api, byref(
            pInvestorPattern), InvestorPatternCnt, self.nRequestID)

    def ReqSubSeqRiskNotifyB(self, SequenceNo: int = 1, DataType: str = ''):
        pRiskNtfSequence = CShfeFtdcRiskNtfSequenceField()
        pRiskNtfSequence.SequenceNo = SequenceNo
        pRiskNtfSequence.DataType = bytes(DataType, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqSubSeqRiskNotifyB(self.api, byref(
            pRiskNtfSequence), self.nRequestID)

    def ReqQryPositionStat(self, BrokerID: str = '', ExchangeProductInstID: str = '', SortType: TShfeFtdcStatSortTypeType = list(TShfeFtdcStatSortTypeType)[0], ResultCount: int = 1, ResultRatio: float = .0):
        pQryStat = CShfeFtdcQryStatField()
        pQryStat.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryStat.ExchangeProductInstID = bytes(
            ExchangeProductInstID, encoding='ascii')
        pQryStat.SortType = SortType.value
        pQryStat.ResultCount = ResultCount
        pQryStat.ResultRatio = ResultRatio
        self.nRequestID += 1
        self.h.ReqQryPositionStat(self.api, byref(pQryStat), self.nRequestID)

    def ReqQryTradeStat(self, BrokerID: str = '', ExchangeProductInstID: str = '', SortType: TShfeFtdcStatSortTypeType = list(TShfeFtdcStatSortTypeType)[0], ResultCount: int = 1, ResultRatio: float = .0):
        pQryStat = CShfeFtdcQryStatField()
        pQryStat.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryStat.ExchangeProductInstID = bytes(
            ExchangeProductInstID, encoding='ascii')
        pQryStat.SortType = SortType.value
        pQryStat.ResultCount = ResultCount
        pQryStat.ResultRatio = ResultRatio
        self.nRequestID += 1
        self.h.ReqQryTradeStat(self.api, byref(pQryStat), self.nRequestID)

    def ReqQryInvestorLinkManHash(self, InvestorIDBeg: str = '', InvestorIDEnd: str = ''):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryInvestorLinkManHash(
            self.api, byref(pInvestorIDRange), self.nRequestID)

    def ReqQryInvestorDepartmentHash(self, InvestorIDBeg: str = '', InvestorIDEnd: str = ''):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryInvestorDepartmentHash(
            self.api, byref(pInvestorIDRange), self.nRequestID)

    def ReqQryStressTest(self, BrokerID: str = '', InvestorRange: TShfeFtdcInvestorRangeType = list(TShfeFtdcInvestorRangeType)[0], InvestorID: str = '', InstrumentID: str = '', PriceType: TShfeFtdcPriceTypeType = list(TShfeFtdcPriceTypeType)[0], Price: float = .0, STPriceCnt: int = 1, HedgeFlag: TShfeFtdcHedgeFlagType = list(TShfeFtdcHedgeFlagType)[0], LongMarginRatioByMoney: float = .0, LongMarginRatioByVolume: float = .0, ShortMarginRatioByMoney: float = .0, ShortMarginRatioByVolume: float = .0, MinMargin: float = .0, STMarginRateCnt: int = 1, STExchMarginRateCnt: int = 1, STDCECombMarginUsed: int = 1, STDCECombType: TShfeFtdcSTDCECombTypeType = list(TShfeFtdcSTDCECombTypeType)[0], SequenceNo: int = 1, ProductID: str = '', ProductID2: str = '', STDCECombMarginParamCnt: int = 1, STDCESPInsGroupParamCnt: int = 1):
        pSTPrice = CShfeFtdcSTPriceField()
        pSTPrice.BrokerID = bytes(BrokerID, encoding='ascii')
        pSTPrice.InvestorRange = InvestorRange.value
        pSTPrice.InvestorID = bytes(InvestorID, encoding='ascii')
        pSTPrice.InstrumentID = bytes(InstrumentID, encoding='ascii')
        pSTPrice.PriceType = PriceType.value
        pSTPrice.Price = Price
        pSTMarginRate = CShfeFtdcSTMarginRateField()
        pSTMarginRate.HedgeFlag = HedgeFlag.value
        pSTMarginRate.LongMarginRatioByMoney = LongMarginRatioByMoney
        pSTMarginRate.LongMarginRatioByVolume = LongMarginRatioByVolume
        pSTMarginRate.ShortMarginRatioByMoney = ShortMarginRatioByMoney
        pSTMarginRate.ShortMarginRatioByVolume = ShortMarginRatioByVolume
        pSTMarginRate.MinMargin = MinMargin
        pSTExchMarginRate = CShfeFtdcSTExchMarginRateField()
        pSTStandard = CShfeFtdcSTStandardField()
        pSTStandard.STDCECombMarginUsed = STDCECombMarginUsed
        pSTDCECombMarginParam = CShfeFtdcSTDCECombMarginParamField()
        pSTDCECombMarginParam.STDCECombType = STDCECombType.value
        pSTDCECombMarginParam.SequenceNo = SequenceNo
        pSTDCECombMarginParam.ProductID = bytes(ProductID, encoding='ascii')
        pSTDCECombMarginParam.ProductID2 = bytes(ProductID2, encoding='ascii')
        pSTDCESPInsGroupParam = CShfeFtdcSTDCESPInsGroupParamField()
        self.nRequestID += 1
        self.h.ReqQryStressTest(self.api, byref(pSTPrice), STPriceCnt, byref(pSTMarginRate), STMarginRateCnt, byref(pSTExchMarginRate), STExchMarginRateCnt, byref(
            pSTStandard), byref(pSTDCECombMarginParam), STDCECombMarginParamCnt, byref(pSTDCESPInsGroupParam), STDCESPInsGroupParamCnt, self.nRequestID)

    def ReqQryLowMarginInvestorHash(self, InvestorIDBeg: str = '', InvestorIDEnd: str = ''):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryLowMarginInvestorHash(
            self.api, byref(pInvestorIDRange), self.nRequestID)

    def ReqQryLowMarginInvestor(self, InvestorIDBeg: str = '', InvestorIDEnd: str = '', InvestorIDRangeCnt: int = 1):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryLowMarginInvestor(self.api, byref(
            pInvestorIDRange), InvestorIDRangeCnt, self.nRequestID)

    def ReqSetSmsStatus(self, SequenceNo: int = 1, Type: TShfeFtdcSmsCustomTypeType = list(TShfeFtdcSmsCustomTypeType)[0], BrokerID: str = '', UserID: str = '', InvestorID: str = '', Status: TShfeFtdcRiskNotifyStatusType = list(TShfeFtdcRiskNotifyStatusType)[0]):
        pSetSmsStatus = CShfeFtdcSetSmsStatusField()
        pSetSmsStatus.SequenceNo = SequenceNo
        pSetSmsStatus.Type = Type.value
        pSetSmsStatus.BrokerID = bytes(BrokerID, encoding='ascii')
        pSetSmsStatus.UserID = bytes(UserID, encoding='ascii')
        pSetSmsStatus.InvestorID = bytes(InvestorID, encoding='ascii')
        pSetSmsStatus.Status = Status.value
        self.nRequestID += 1
        self.h.ReqSetSmsStatus(self.api, byref(pSetSmsStatus), self.nRequestID)

    def ReqQryExchMarginRate(self, BrokerID: str = '', InstrumentID: str = '', HedgeFlag: TShfeFtdcHedgeFlagType = list(TShfeFtdcHedgeFlagType)[0]):
        pQryExchMarginRate = CShfeFtdcQryExchMarginRateField()
        pQryExchMarginRate.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryExchMarginRate.InstrumentID = bytes(InstrumentID, encoding='ascii')
        pQryExchMarginRate.HedgeFlag = HedgeFlag.value
        self.nRequestID += 1
        self.h.ReqQryExchMarginRate(self.api, byref(
            pQryExchMarginRate), self.nRequestID)

    def ReqQryCommissionRate(self, BrokerID: str = '', InvestorID: str = '', InstrumentID: str = ''):
        pQryInstrumentCommissionRate = CShfeFtdcQryInstrumentCommissionRateField()
        pQryInstrumentCommissionRate.BrokerID = bytes(
            BrokerID, encoding='ascii')
        pQryInstrumentCommissionRate.InvestorID = bytes(
            InvestorID, encoding='ascii')
        pQryInstrumentCommissionRate.InstrumentID = bytes(
            InstrumentID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryCommissionRate(self.api, byref(
            pQryInstrumentCommissionRate), self.nRequestID)

    def ReqQrySecAgentInvestorHash(self, InvestorIDBeg: str = '', InvestorIDEnd: str = ''):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQrySecAgentInvestorHash(
            self.api, byref(pInvestorIDRange), self.nRequestID)

    def ReqQrySecAgentInvestor(self, InvestorIDBeg: str = '', InvestorIDEnd: str = '', InvestorIDRangeCnt: int = 1):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQrySecAgentInvestor(self.api, byref(
            pInvestorIDRange), InvestorIDRangeCnt, self.nRequestID)

    def ReqQryOptionInstrCommRate(self, BrokerID: str = '', InvestorID: str = '', InstrumentID: str = ''):
        pQryOptionInstrCommRate = CShfeFtdcQryOptionInstrCommRateField()
        pQryOptionInstrCommRate.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryOptionInstrCommRate.InvestorID = bytes(
            InvestorID, encoding='ascii')
        pQryOptionInstrCommRate.InstrumentID = bytes(
            InstrumentID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryOptionInstrCommRate(self.api, byref(
            pQryOptionInstrCommRate), self.nRequestID)

    def ReqQryMMOptionInstrCommRate(self, BrokerID: str = '', InvestorID: str = '', InstrumentID: str = ''):
        pQryMMOptionInstrCommRate = CShfeFtdcQryMMOptionInstrCommRateField()
        pQryMMOptionInstrCommRate.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryMMOptionInstrCommRate.InvestorID = bytes(
            InvestorID, encoding='ascii')
        pQryMMOptionInstrCommRate.InstrumentID = bytes(
            InstrumentID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryMMOptionInstrCommRate(self.api, byref(
            pQryMMOptionInstrCommRate), self.nRequestID)

    def ReqQryExecOrder(self, BrokerID: str = '', InvestorID: str = '', InstrumentID: str = '', ExchangeID: str = '', ExecOrderSysID: str = '', InsertTimeStart: str = '', InsertTimeEnd: str = ''):
        pRiskQryExecOrder = CShfeFtdcRiskQryExecOrderField()
        pRiskQryExecOrder.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskQryExecOrder.InvestorID = bytes(InvestorID, encoding='ascii')
        pRiskQryExecOrder.InstrumentID = bytes(InstrumentID, encoding='ascii')
        pRiskQryExecOrder.ExchangeID = bytes(ExchangeID, encoding='ascii')
        pRiskQryExecOrder.ExecOrderSysID = bytes(
            ExecOrderSysID, encoding='ascii')
        pRiskQryExecOrder.InsertTimeStart = bytes(
            InsertTimeStart, encoding='ascii')
        pRiskQryExecOrder.InsertTimeEnd = bytes(
            InsertTimeEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryExecOrder(self.api, byref(
            pRiskQryExecOrder), self.nRequestID)

    def ReqQryLogUserLoginStat(self, BrokerID: str = '', FailNumByUser: int = 1, AddressNumByUser: int = 1, UserNumByAddress: int = 1, TotalNumByAddress: int = 1):
        pRiskQryLogUserLoginStat = CShfeFtdcRiskQryLogUserLoginStatField()
        pRiskQryLogUserLoginStat.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskQryLogUserLoginStat.FailNumByUser = FailNumByUser
        pRiskQryLogUserLoginStat.AddressNumByUser = AddressNumByUser
        pRiskQryLogUserLoginStat.UserNumByAddress = UserNumByAddress
        pRiskQryLogUserLoginStat.TotalNumByAddress = TotalNumByAddress
        self.nRequestID += 1
        self.h.ReqQryLogUserLoginStat(self.api, byref(
            pRiskQryLogUserLoginStat), self.nRequestID)

    def ReqQryLogUserLoginInfo(self, BrokerID: str = '', UserID: str = '', IPAddress: str = '', MacAddress: str = ''):
        pRiskQryLogUserLoginInfo = CShfeFtdcRiskQryLogUserLoginInfoField()
        pRiskQryLogUserLoginInfo.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskQryLogUserLoginInfo.UserID = bytes(UserID, encoding='ascii')
        pRiskQryLogUserLoginInfo.IPAddress = bytes(IPAddress, encoding='ascii')
        pRiskQryLogUserLoginInfo.MacAddress = bytes(
            MacAddress, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryLogUserLoginInfo(self.api, byref(
            pRiskQryLogUserLoginInfo), self.nRequestID)

    def ReqQryInstrumentGreeks(self, BrokerID: str = '', UserID: str = '', InstrumentID: str = '', ExchangeID: str = ''):
        pRiskQryInstrumentGreeks = CShfeFtdcRiskQryInstrumentGreeksField()
        pRiskQryInstrumentGreeks.BrokerID = bytes(BrokerID, encoding='ascii')
        pRiskQryInstrumentGreeks.UserID = bytes(UserID, encoding='ascii')
        pRiskQryInstrumentGreeks.InstrumentID = bytes(
            InstrumentID, encoding='ascii')
        pRiskQryInstrumentGreeks.ExchangeID = bytes(
            ExchangeID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryInstrumentGreeks(self.api, byref(
            pRiskQryInstrumentGreeks), self.nRequestID)

    def ReqQryExeciseTest(self, BrokerID: str = '', InvestorRange: TShfeFtdcInvestorRangeType = list(TShfeFtdcInvestorRangeType)[0], InvestorID: str = '', InstrumentID: str = '', PriceType: TShfeFtdcPriceTypeType = list(TShfeFtdcPriceTypeType)[0], Price: float = .0, ETPriceCnt: int = 1, PosiDirection: TShfeFtdcPosiDirectionType = list(TShfeFtdcPosiDirectionType)[0], HedgeFlag: TShfeFtdcHedgeFlagType = list(TShfeFtdcHedgeFlagType)[0], PositionDate: TShfeFtdcPositionDateType = list(TShfeFtdcPositionDateType)[0], Position: int = 1, EXEPosition: int = 1, EXEPriceType: TShfeFtdcPriceTypeType = list(TShfeFtdcPriceTypeType)[0], EXEPrice: float = .0, ETStrikePositionCnt: int = 1, STDCECombType: TShfeFtdcSTDCECombTypeType = list(TShfeFtdcSTDCECombTypeType)[0], SequenceNo: int = 1, ProductID: str = '', ProductID2: str = '', ETDCECombMarginParamCnt: int = 1, ETDCESPInsGroupParamCnt: int = 1):
        pETPrice = CShfeFtdcETPriceField()
        pETPrice.BrokerID = bytes(BrokerID, encoding='ascii')
        pETPrice.InvestorRange = InvestorRange.value
        pETPrice.InvestorID = bytes(InvestorID, encoding='ascii')
        pETPrice.InstrumentID = bytes(InstrumentID, encoding='ascii')
        pETPrice.PriceType = PriceType.value
        pETPrice.Price = Price
        pETStrikePosition = CShfeFtdcETStrikePositionField()
        pETStrikePosition.PosiDirection = PosiDirection.value
        pETStrikePosition.HedgeFlag = HedgeFlag.value
        pETStrikePosition.PositionDate = PositionDate.value
        pETStrikePosition.Position = Position
        pETStrikePosition.EXEPosition = EXEPosition
        pETStrikePosition.EXEPriceType = EXEPriceType.value
        pETStrikePosition.EXEPrice = EXEPrice
        pETDCECombMarginParam = CShfeFtdcETDCECombMarginParamField()
        pETDCECombMarginParam.STDCECombType = STDCECombType.value
        pETDCECombMarginParam.SequenceNo = SequenceNo
        pETDCECombMarginParam.ProductID = bytes(ProductID, encoding='ascii')
        pETDCECombMarginParam.ProductID2 = bytes(ProductID2, encoding='ascii')
        pETDCESPInsGroupParam = CShfeFtdcETDCESPInsGroupParamField()
        self.nRequestID += 1
        self.h.ReqQryExeciseTest(self.api, byref(pETPrice), ETPriceCnt, byref(pETStrikePosition), ETStrikePositionCnt, byref(
            pETDCECombMarginParam), ETDCECombMarginParamCnt, byref(pETDCESPInsGroupParam), ETDCESPInsGroupParamCnt, self.nRequestID)

    def ReqQryUserRightsAssign(self, InvestorIDBeg: str = '', InvestorIDEnd: str = ''):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryUserRightsAssign(
            self.api, byref(pInvestorIDRange), self.nRequestID)

    def ReqQryCurrDRIdentity(self, InvestorIDBeg: str = '', InvestorIDEnd: str = ''):
        pInvestorIDRange = CShfeFtdcInvestorIDRangeField()
        pInvestorIDRange.InvestorIDBeg = bytes(InvestorIDBeg, encoding='ascii')
        pInvestorIDRange.InvestorIDEnd = bytes(InvestorIDEnd, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQryCurrDRIdentity(self.api, byref(
            pInvestorIDRange), self.nRequestID)

    def ReqQrySecAgentTradingAccount(self, BrokerID: str = '', InvestorID: str = '', CurrencyID: str = '', QryTradingAccountCnt: int = 1):
        pQryTradingAccount = CShfeFtdcQryTradingAccountField()
        pQryTradingAccount.BrokerID = bytes(BrokerID, encoding='ascii')
        pQryTradingAccount.InvestorID = bytes(InvestorID, encoding='ascii')
        pQryTradingAccount.CurrencyID = bytes(CurrencyID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQrySecAgentTradingAccount(self.api, byref(
            pQryTradingAccount), QryTradingAccountCnt, self.nRequestID)

    def ReqQrySyncDelaySwap(self, BrokerID: str = '', DelaySwapSeqNo: str = ''):
        pQrySyncDelaySwap = CShfeFtdcQrySyncDelaySwapField()
        pQrySyncDelaySwap.BrokerID = bytes(BrokerID, encoding='ascii')
        pQrySyncDelaySwap.DelaySwapSeqNo = bytes(
            DelaySwapSeqNo, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQrySyncDelaySwap(self.api, byref(
            pQrySyncDelaySwap), self.nRequestID)

    def ReqQrySecAgentCheckMode(self, BrokerID: str = '', InvestorID: str = ''):
        pQrySecAgentCheckMode = CShfeFtdcQrySecAgentCheckModeField()
        pQrySecAgentCheckMode.BrokerID = bytes(BrokerID, encoding='ascii')
        pQrySecAgentCheckMode.InvestorID = bytes(InvestorID, encoding='ascii')
        self.nRequestID += 1
        self.h.ReqQrySecAgentCheckMode(self.api, byref(
            pQrySecAgentCheckMode), self.nRequestID)

    def RegCB(self):
        self.h.SetOnFrontConnected.argtypes = [c_void_p, c_void_p]
        self.h.SetOnFrontConnected.restype = None
        self.evOnFrontConnected = CFUNCTYPE(None)(self.__OnFrontConnected)
        self.h.SetOnFrontConnected(self.spi, self.evOnFrontConnected)

        self.h.SetOnFrontDisconnected.argtypes = [c_void_p, c_void_p]
        self.h.SetOnFrontDisconnected.restype = None
        self.evOnFrontDisconnected = CFUNCTYPE(
            None, POINTER(c_int32))(self.__OnFrontDisconnected)
        self.h.SetOnFrontDisconnected(self.spi, self.evOnFrontDisconnected)

        self.h.SetOnHeartBeatWarning.argtypes = [c_void_p, c_void_p]
        self.h.SetOnHeartBeatWarning.restype = None
        self.evOnHeartBeatWarning = CFUNCTYPE(
            None, POINTER(c_int32))(self.__OnHeartBeatWarning)
        self.h.SetOnHeartBeatWarning(self.spi, self.evOnHeartBeatWarning)

        self.h.SetOnRspError.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspError.restype = None
        self.evOnRspError = CFUNCTYPE(None, POINTER(CShfeFtdcRspInfoField), POINTER(
            c_int32), POINTER(c_bool))(self.__OnRspError)
        self.h.SetOnRspError(self.spi, self.evOnRspError)

        self.h.SetOnRtnBrokerDeposit.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnBrokerDeposit.restype = None
        self.evOnRtnBrokerDeposit = CFUNCTYPE(None, POINTER(
            CShfeFtdcBrokerDepositField))(self.__OnRtnBrokerDeposit)
        self.h.SetOnRtnBrokerDeposit(self.spi, self.evOnRtnBrokerDeposit)

        self.h.SetOnRtnInvestorSumInfo.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnInvestorSumInfo.restype = None
        self.evOnRtnInvestorSumInfo = CFUNCTYPE(None, POINTER(
            CShfeFtdcInvestorSumInfoField))(self.__OnRtnInvestorSumInfo)
        self.h.SetOnRtnInvestorSumInfo(self.spi, self.evOnRtnInvestorSumInfo)

        self.h.SetOnRtnClientSGDataSyncStart.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnClientSGDataSyncStart.restype = None
        self.evOnRtnClientSGDataSyncStart = CFUNCTYPE(None, POINTER(
            CShfeFtdcSettlementSessionField))(self.__OnRtnClientSGDataSyncStart)
        self.h.SetOnRtnClientSGDataSyncStart(
            self.spi, self.evOnRtnClientSGDataSyncStart)

        self.h.SetOnRtnClientSGDataSyncEnd.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnClientSGDataSyncEnd.restype = None
        self.evOnRtnClientSGDataSyncEnd = CFUNCTYPE(None, POINTER(
            CShfeFtdcSettlementSessionField))(self.__OnRtnClientSGDataSyncEnd)
        self.h.SetOnRtnClientSGDataSyncEnd(
            self.spi, self.evOnRtnClientSGDataSyncEnd)

        self.h.SetOnRspRiskUserLogin.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRiskUserLogin.restype = None
        self.evOnRspRiskUserLogin = CFUNCTYPE(None, POINTER(CShfeFtdcRspRiskUserLoginField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRiskUserLogin)
        self.h.SetOnRspRiskUserLogin(self.spi, self.evOnRspRiskUserLogin)

        self.h.SetOnRspQryInvestorMarginRate.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryInvestorMarginRate.restype = None
        self.evOnRspQryInvestorMarginRate = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorMarginRateField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryInvestorMarginRate)
        self.h.SetOnRspQryInvestorMarginRate(
            self.spi, self.evOnRspQryInvestorMarginRate)

        self.h.SetOnRtnProduct.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnProduct.restype = None
        self.evOnRtnProduct = CFUNCTYPE(None, POINTER(
            CShfeFtdcProductField))(self.__OnRtnProduct)
        self.h.SetOnRtnProduct(self.spi, self.evOnRtnProduct)

        self.h.SetOnRtnInstrument.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnInstrument.restype = None
        self.evOnRtnInstrument = CFUNCTYPE(None, POINTER(
            CShfeFtdcInstrumentField))(self.__OnRtnInstrument)
        self.h.SetOnRtnInstrument(self.spi, self.evOnRtnInstrument)

        self.h.SetOnRspQryOrderStat.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryOrderStat.restype = None
        self.evOnRspQryOrderStat = CFUNCTYPE(None, POINTER(CShfeFtdcOrderStatField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryOrderStat)
        self.h.SetOnRspQryOrderStat(self.spi, self.evOnRspQryOrderStat)

        self.h.SetOnRtnExchange.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnExchange.restype = None
        self.evOnRtnExchange = CFUNCTYPE(None, POINTER(
            CShfeFtdcExchangeField))(self.__OnRtnExchange)
        self.h.SetOnRtnExchange(self.spi, self.evOnRtnExchange)

        self.h.SetOnRspInvestorPositionStatic.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspInvestorPositionStatic.restype = None
        self.evOnRspInvestorPositionStatic = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorPositionStaticField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspInvestorPositionStatic)
        self.h.SetOnRspInvestorPositionStatic(
            self.spi, self.evOnRspInvestorPositionStatic)

        self.h.SetOnRspInvestorTradeStatic.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspInvestorTradeStatic.restype = None
        self.evOnRspInvestorTradeStatic = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorTradeStaticField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspInvestorTradeStatic)
        self.h.SetOnRspInvestorTradeStatic(
            self.spi, self.evOnRspInvestorTradeStatic)

        self.h.SetOnRtnRiskDepthMarketData.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnRiskDepthMarketData.restype = None
        self.evOnRtnRiskDepthMarketData = CFUNCTYPE(None, POINTER(
            CShfeFtdcDepthMarketDataField))(self.__OnRtnRiskDepthMarketData)
        self.h.SetOnRtnRiskDepthMarketData(
            self.spi, self.evOnRtnRiskDepthMarketData)

        self.h.SetOnRtnTimeSync.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnTimeSync.restype = None
        self.evOnRtnTimeSync = CFUNCTYPE(None, POINTER(
            CShfeFtdcCurrentTimeField))(self.__OnRtnTimeSync)
        self.h.SetOnRtnTimeSync(self.spi, self.evOnRtnTimeSync)

        self.h.SetOnRspInstPositionRate.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspInstPositionRate.restype = None
        self.evOnRspInstPositionRate = CFUNCTYPE(None, POINTER(CShfeFtdcRspInstPositionRateField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspInstPositionRate)
        self.h.SetOnRspInstPositionRate(self.spi, self.evOnRspInstPositionRate)

        self.h.SetOnRspProductPositionRate.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspProductPositionRate.restype = None
        self.evOnRspProductPositionRate = CFUNCTYPE(None, POINTER(CShfeFtdcRspProductPositionRateField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspProductPositionRate)
        self.h.SetOnRspProductPositionRate(
            self.spi, self.evOnRspProductPositionRate)

        self.h.SetOnRspQryTradingCodeHash.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryTradingCodeHash.restype = None
        self.evOnRspQryTradingCodeHash = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorHashField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryTradingCodeHash)
        self.h.SetOnRspQryTradingCodeHash(
            self.spi, self.evOnRspQryTradingCodeHash)

        self.h.SetOnRspQryTradingCode.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryTradingCode.restype = None
        self.evOnRspQryTradingCode = CFUNCTYPE(None, POINTER(CShfeFtdcTradingCodeField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryTradingCode)
        self.h.SetOnRspQryTradingCode(self.spi, self.evOnRspQryTradingCode)

        self.h.SetOnRtnTradingCode.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnTradingCode.restype = None
        self.evOnRtnTradingCode = CFUNCTYPE(None, POINTER(
            CShfeFtdcTradingCodeField))(self.__OnRtnTradingCode)
        self.h.SetOnRtnTradingCode(self.spi, self.evOnRtnTradingCode)

        self.h.SetOnRtnDelTradingCode.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnDelTradingCode.restype = None
        self.evOnRtnDelTradingCode = CFUNCTYPE(None, POINTER(
            CShfeFtdcTradingCodeField))(self.__OnRtnDelTradingCode)
        self.h.SetOnRtnDelTradingCode(self.spi, self.evOnRtnDelTradingCode)

        self.h.SetOnRtnSequencialBrokerUserEvent.argtypes = [
            c_void_p, c_void_p]
        self.h.SetOnRtnSequencialBrokerUserEvent.restype = None
        self.evOnRtnSequencialBrokerUserEvent = CFUNCTYPE(None, POINTER(
            CShfeFtdcSequencialBrokerUserEventField))(self.__OnRtnSequencialBrokerUserEvent)
        self.h.SetOnRtnSequencialBrokerUserEvent(
            self.spi, self.evOnRtnSequencialBrokerUserEvent)

        self.h.SetOnRtnSequencialTrade.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSequencialTrade.restype = None
        self.evOnRtnSequencialTrade = CFUNCTYPE(None, POINTER(
            CShfeFtdcSequencialTradeField))(self.__OnRtnSequencialTrade)
        self.h.SetOnRtnSequencialTrade(self.spi, self.evOnRtnSequencialTrade)

        self.h.SetOnRtnSequencialOrder.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSequencialOrder.restype = None
        self.evOnRtnSequencialOrder = CFUNCTYPE(None, POINTER(
            CShfeFtdcSequencialOrderField))(self.__OnRtnSequencialOrder)
        self.h.SetOnRtnSequencialOrder(self.spi, self.evOnRtnSequencialOrder)

        self.h.SetOnRspRiskOrderInsert.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRiskOrderInsert.restype = None
        self.evOnRspRiskOrderInsert = CFUNCTYPE(None, POINTER(CShfeFtdcInputOrderField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRiskOrderInsert)
        self.h.SetOnRspRiskOrderInsert(self.spi, self.evOnRspRiskOrderInsert)

        self.h.SetOnRspRiskOrderAction.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRiskOrderAction.restype = None
        self.evOnRspRiskOrderAction = CFUNCTYPE(None, POINTER(CShfeFtdcInputOrderActionField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRiskOrderAction)
        self.h.SetOnRspRiskOrderAction(self.spi, self.evOnRspRiskOrderAction)

        self.h.SetOnRtnSequencialPosition.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSequencialPosition.restype = None
        self.evOnRtnSequencialPosition = CFUNCTYPE(None, POINTER(
            CShfeFtdcSequencialPositionField))(self.__OnRtnSequencialPosition)
        self.h.SetOnRtnSequencialPosition(
            self.spi, self.evOnRtnSequencialPosition)

        self.h.SetOnRspRiskNotifyCommand.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRiskNotifyCommand.restype = None
        self.evOnRspRiskNotifyCommand = CFUNCTYPE(None, POINTER(CShfeFtdcRspInfoField), POINTER(
            c_int32), POINTER(c_bool))(self.__OnRspRiskNotifyCommand)
        self.h.SetOnRspRiskNotifyCommand(
            self.spi, self.evOnRspRiskNotifyCommand)

        self.h.SetOnRspBatchForceCloseCalc.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspBatchForceCloseCalc.restype = None
        self.evOnRspBatchForceCloseCalc = CFUNCTYPE(None, POINTER(CShfeFtdcRspForceClosePositionField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspBatchForceCloseCalc)
        self.h.SetOnRspBatchForceCloseCalc(
            self.spi, self.evOnRspBatchForceCloseCalc)

        self.h.SetOnRspForceCloseCalc.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspForceCloseCalc.restype = None
        self.evOnRspForceCloseCalc = CFUNCTYPE(None, POINTER(CShfeFtdcRspForceClosePositionField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspForceCloseCalc)
        self.h.SetOnRspForceCloseCalc(self.spi, self.evOnRspForceCloseCalc)

        self.h.SetOnRspSetIndexNPPParam.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspSetIndexNPPParam.restype = None
        self.evOnRspSetIndexNPPParam = CFUNCTYPE(None, POINTER(CShfeFtdcIndexNPPParamField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspSetIndexNPPParam)
        self.h.SetOnRspSetIndexNPPParam(self.spi, self.evOnRspSetIndexNPPParam)

        self.h.SetOnRtnIndexNPP.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnIndexNPP.restype = None
        self.evOnRtnIndexNPP = CFUNCTYPE(None, POINTER(
            CShfeFtdcIndexNPPField))(self.__OnRtnIndexNPP)
        self.h.SetOnRtnIndexNPP(self.spi, self.evOnRtnIndexNPP)

        self.h.SetOnRspRemIndexNPPParam.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRemIndexNPPParam.restype = None
        self.evOnRspRemIndexNPPParam = CFUNCTYPE(None, POINTER(CShfeFtdcIndexNPPParamField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRemIndexNPPParam)
        self.h.SetOnRspRemIndexNPPParam(self.spi, self.evOnRspRemIndexNPPParam)

        self.h.SetOnRspForceCloseAccount.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspForceCloseAccount.restype = None
        self.evOnRspForceCloseAccount = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorRiskAccountField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspForceCloseAccount)
        self.h.SetOnRspForceCloseAccount(
            self.spi, self.evOnRspForceCloseAccount)

        self.h.SetOnRspQryLogin.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryLogin.restype = None
        self.evOnRspQryLogin = CFUNCTYPE(None, POINTER(CShfeFtdcNormalRiskQueryField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryLogin)
        self.h.SetOnRspQryLogin(self.spi, self.evOnRspQryLogin)

        self.h.SetOnRspQrySafePriceRange.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQrySafePriceRange.restype = None
        self.evOnRspQrySafePriceRange = CFUNCTYPE(None, POINTER(CShfeFtdcSafePriceRangeField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQrySafePriceRange)
        self.h.SetOnRspQrySafePriceRange(
            self.spi, self.evOnRspQrySafePriceRange)

        self.h.SetOnRspQrySafePriceRangeAccount.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQrySafePriceRangeAccount.restype = None
        self.evOnRspQrySafePriceRangeAccount = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorRiskAccountField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQrySafePriceRangeAccount)
        self.h.SetOnRspQrySafePriceRangeAccount(
            self.spi, self.evOnRspQrySafePriceRangeAccount)

        self.h.SetOnRspQryPriceVaryEffect.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryPriceVaryEffect.restype = None
        self.evOnRspQryPriceVaryEffect = CFUNCTYPE(None, POINTER(CShfeFtdcPriceVaryParamField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryPriceVaryEffect)
        self.h.SetOnRspQryPriceVaryEffect(
            self.spi, self.evOnRspQryPriceVaryEffect)

        self.h.SetOnRtnDepartment.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnDepartment.restype = None
        self.evOnRtnDepartment = CFUNCTYPE(None, POINTER(
            CShfeFtdcDepartmentField))(self.__OnRtnDepartment)
        self.h.SetOnRtnDepartment(self.spi, self.evOnRtnDepartment)

        self.h.SetOnRspIndexNPP.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspIndexNPP.restype = None
        self.evOnRspIndexNPP = CFUNCTYPE(None, POINTER(CShfeFtdcIndexNPPField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspIndexNPP)
        self.h.SetOnRspIndexNPP(self.spi, self.evOnRspIndexNPP)

        self.h.SetOnRtnTradeParam.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnTradeParam.restype = None
        self.evOnRtnTradeParam = CFUNCTYPE(None, POINTER(
            CShfeFtdcTradeParamField))(self.__OnRtnTradeParam)
        self.h.SetOnRtnTradeParam(self.spi, self.evOnRtnTradeParam)

        self.h.SetOnRspRiskParkedOrderInsert.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRiskParkedOrderInsert.restype = None
        self.evOnRspRiskParkedOrderInsert = CFUNCTYPE(None, POINTER(CShfeFtdcRiskParkedOrderField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRiskParkedOrderInsert)
        self.h.SetOnRspRiskParkedOrderInsert(
            self.spi, self.evOnRspRiskParkedOrderInsert)

        self.h.SetOnRspRemoveRiskParkedOrder.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRemoveRiskParkedOrder.restype = None
        self.evOnRspRemoveRiskParkedOrder = CFUNCTYPE(None, POINTER(CShfeFtdcRemoveRiskParkedOrderField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRemoveRiskParkedOrder)
        self.h.SetOnRspRemoveRiskParkedOrder(
            self.spi, self.evOnRspRemoveRiskParkedOrder)

        self.h.SetOnRtnSeqRiskParkedOrder.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSeqRiskParkedOrder.restype = None
        self.evOnRtnSeqRiskParkedOrder = CFUNCTYPE(None, POINTER(
            CShfeFtdcSeqRiskParkedOrderField))(self.__OnRtnSeqRiskParkedOrder)
        self.h.SetOnRtnSeqRiskParkedOrder(
            self.spi, self.evOnRtnSeqRiskParkedOrder)

        self.h.SetOnRspRiskUserPasswordUpd.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRiskUserPasswordUpd.restype = None
        self.evOnRspRiskUserPasswordUpd = CFUNCTYPE(None, POINTER(CShfeFtdcUserPasswordUpdateField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRiskUserPasswordUpd)
        self.h.SetOnRspRiskUserPasswordUpd(
            self.spi, self.evOnRspRiskUserPasswordUpd)

        self.h.SetOnRtnSeqDeposit.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSeqDeposit.restype = None
        self.evOnRtnSeqDeposit = CFUNCTYPE(None, POINTER(
            CShfeFtdcSeqDepositField))(self.__OnRtnSeqDeposit)
        self.h.SetOnRtnSeqDeposit(self.spi, self.evOnRtnSeqDeposit)

        self.h.SetOnRspAddRiskUserEvent.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspAddRiskUserEvent.restype = None
        self.evOnRspAddRiskUserEvent = CFUNCTYPE(None, POINTER(CShfeFtdcRiskUserEventField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspAddRiskUserEvent)
        self.h.SetOnRspAddRiskUserEvent(self.spi, self.evOnRspAddRiskUserEvent)

        self.h.SetOnRspQryPredictRiskAccount.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryPredictRiskAccount.restype = None
        self.evOnRspQryPredictRiskAccount = CFUNCTYPE(None, POINTER(CShfeFtdcPredictRiskAccountField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryPredictRiskAccount)
        self.h.SetOnRspQryPredictRiskAccount(
            self.spi, self.evOnRspQryPredictRiskAccount)

        self.h.SetOnRspQryPredictRiskPosition.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryPredictRiskPosition.restype = None
        self.evOnRspQryPredictRiskPosition = CFUNCTYPE(None, POINTER(CShfeFtdcPredictRiskPositionField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryPredictRiskPosition)
        self.h.SetOnRspQryPredictRiskPosition(
            self.spi, self.evOnRspQryPredictRiskPosition)

        self.h.SetOnRtnRiskInvestor.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnRiskInvestor.restype = None
        self.evOnRtnRiskInvestor = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskSyncInvestorField))(self.__OnRtnRiskInvestor)
        self.h.SetOnRtnRiskInvestor(self.spi, self.evOnRtnRiskInvestor)

        self.h.SetOnRspQryInvestorLinkMan.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryInvestorLinkMan.restype = None
        self.evOnRspQryInvestorLinkMan = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorLinkManField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryInvestorLinkMan)
        self.h.SetOnRspQryInvestorLinkMan(
            self.spi, self.evOnRspQryInvestorLinkMan)

        self.h.SetOnRspQryInvestorDepartment.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryInvestorDepartment.restype = None
        self.evOnRspQryInvestorDepartment = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorDepartmentFlatField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryInvestorDepartment)
        self.h.SetOnRspQryInvestorDepartment(
            self.spi, self.evOnRspQryInvestorDepartment)

        self.h.SetOnRtnDelIndexNPP.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnDelIndexNPP.restype = None
        self.evOnRtnDelIndexNPP = CFUNCTYPE(None, POINTER(
            CShfeFtdcIndexNPPField))(self.__OnRtnDelIndexNPP)
        self.h.SetOnRtnDelIndexNPP(self.spi, self.evOnRtnDelIndexNPP)

        self.h.SetOnRtnRiskUserFunction.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnRiskUserFunction.restype = None
        self.evOnRtnRiskUserFunction = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskUserFunctionField))(self.__OnRtnRiskUserFunction)
        self.h.SetOnRtnRiskUserFunction(self.spi, self.evOnRtnRiskUserFunction)

        self.h.SetOnRtnDelRiskUserFunction.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnDelRiskUserFunction.restype = None
        self.evOnRtnDelRiskUserFunction = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskUserFunctionField))(self.__OnRtnDelRiskUserFunction)
        self.h.SetOnRtnDelRiskUserFunction(
            self.spi, self.evOnRtnDelRiskUserFunction)

        self.h.SetOnRtnRiskSyncAccount.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnRiskSyncAccount.restype = None
        self.evOnRtnRiskSyncAccount = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskSyncAccountField))(self.__OnRtnRiskSyncAccount)
        self.h.SetOnRtnRiskSyncAccount(self.spi, self.evOnRtnRiskSyncAccount)

        self.h.SetOnRtnSeqPreRiskAccount.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSeqPreRiskAccount.restype = None
        self.evOnRtnSeqPreRiskAccount = CFUNCTYPE(None, POINTER(
            CShfeFtdcSeqPreRiskAccountField))(self.__OnRtnSeqPreRiskAccount)
        self.h.SetOnRtnSeqPreRiskAccount(
            self.spi, self.evOnRtnSeqPreRiskAccount)

        self.h.SetOnRtnNoticeToken.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnNoticeToken.restype = None
        self.evOnRtnNoticeToken = CFUNCTYPE(None, POINTER(
            CShfeFtdcNoticeTokenField))(self.__OnRtnNoticeToken)
        self.h.SetOnRtnNoticeToken(self.spi, self.evOnRtnNoticeToken)

        self.h.SetOnRtnNoticePattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnNoticePattern.restype = None
        self.evOnRtnNoticePattern = CFUNCTYPE(None, POINTER(
            CShfeFtdcNoticePatternField))(self.__OnRtnNoticePattern)
        self.h.SetOnRtnNoticePattern(self.spi, self.evOnRtnNoticePattern)

        self.h.SetOnRspModNoticePattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspModNoticePattern.restype = None
        self.evOnRspModNoticePattern = CFUNCTYPE(None, POINTER(CShfeFtdcNoticePatternField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspModNoticePattern)
        self.h.SetOnRspModNoticePattern(self.spi, self.evOnRspModNoticePattern)

        self.h.SetOnRtnVaryMarketData.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnVaryMarketData.restype = None
        self.evOnRtnVaryMarketData = CFUNCTYPE(None, POINTER(
            CShfeFtdcVaryMarketDataField))(self.__OnRtnVaryMarketData)
        self.h.SetOnRtnVaryMarketData(self.spi, self.evOnRtnVaryMarketData)

        self.h.SetOnRspAddRiskNotifyA.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspAddRiskNotifyA.restype = None
        self.evOnRspAddRiskNotifyA = CFUNCTYPE(None, POINTER(CShfeFtdcRspInfoField), POINTER(
            c_int32), POINTER(c_bool))(self.__OnRspAddRiskNotifyA)
        self.h.SetOnRspAddRiskNotifyA(self.spi, self.evOnRspAddRiskNotifyA)

        self.h.SetOnRspAddBizNotice.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspAddBizNotice.restype = None
        self.evOnRspAddBizNotice = CFUNCTYPE(None, POINTER(CShfeFtdcRspInfoField), POINTER(
            c_int32), POINTER(c_bool))(self.__OnRspAddBizNotice)
        self.h.SetOnRspAddBizNotice(self.spi, self.evOnRspAddBizNotice)

        self.h.SetOnRtnSeqBizNotice.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSeqBizNotice.restype = None
        self.evOnRtnSeqBizNotice = CFUNCTYPE(None, POINTER(
            CShfeFtdcSeqBizNoticeField))(self.__OnRtnSeqBizNotice)
        self.h.SetOnRtnSeqBizNotice(self.spi, self.evOnRtnSeqBizNotice)

        self.h.SetOnRspRiskQryBrokerDeposit.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRiskQryBrokerDeposit.restype = None
        self.evOnRspRiskQryBrokerDeposit = CFUNCTYPE(None, POINTER(CShfeFtdcQueryBrokerDepositField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRiskQryBrokerDeposit)
        self.h.SetOnRspRiskQryBrokerDeposit(
            self.spi, self.evOnRspRiskQryBrokerDeposit)

        self.h.SetOnRtnRiskParamInfo.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnRiskParamInfo.restype = None
        self.evOnRtnRiskParamInfo = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskParamInfoField))(self.__OnRtnRiskParamInfo)
        self.h.SetOnRtnRiskParamInfo(self.spi, self.evOnRtnRiskParamInfo)

        self.h.SetOnRspModRiskInvestorParam.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspModRiskInvestorParam.restype = None
        self.evOnRspModRiskInvestorParam = CFUNCTYPE(None, POINTER(CShfeFtdcRiskInvestorParamField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspModRiskInvestorParam)
        self.h.SetOnRspModRiskInvestorParam(
            self.spi, self.evOnRspModRiskInvestorParam)

        self.h.SetOnRspRemRiskInvestorParam.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRemRiskInvestorParam.restype = None
        self.evOnRspRemRiskInvestorParam = CFUNCTYPE(None, POINTER(CShfeFtdcRiskInvestorParamField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRemRiskInvestorParam)
        self.h.SetOnRspRemRiskInvestorParam(
            self.spi, self.evOnRspRemRiskInvestorParam)

        self.h.SetOnRtnRiskInvestorParam.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnRiskInvestorParam.restype = None
        self.evOnRtnRiskInvestorParam = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskInvestorParamField))(self.__OnRtnRiskInvestorParam)
        self.h.SetOnRtnRiskInvestorParam(
            self.spi, self.evOnRtnRiskInvestorParam)

        self.h.SetOnRtnDelRiskInvestorParam.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnDelRiskInvestorParam.restype = None
        self.evOnRtnDelRiskInvestorParam = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskInvestorParamField))(self.__OnRtnDelRiskInvestorParam)
        self.h.SetOnRtnDelRiskInvestorParam(
            self.spi, self.evOnRtnDelRiskInvestorParam)

        self.h.SetOnRspForceRiskUserLogout.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspForceRiskUserLogout.restype = None
        self.evOnRspForceRiskUserLogout = CFUNCTYPE(None, POINTER(CShfeFtdcRiskLoginInfoField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspForceRiskUserLogout)
        self.h.SetOnRspForceRiskUserLogout(
            self.spi, self.evOnRspForceRiskUserLogout)

        self.h.SetOnRtnForceRiskUserLogout.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnForceRiskUserLogout.restype = None
        self.evOnRtnForceRiskUserLogout = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskLoginInfoField))(self.__OnRtnForceRiskUserLogout)
        self.h.SetOnRtnForceRiskUserLogout(
            self.spi, self.evOnRtnForceRiskUserLogout)

        self.h.SetOnRspAddRiskPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspAddRiskPattern.restype = None
        self.evOnRspAddRiskPattern = CFUNCTYPE(None, POINTER(CShfeFtdcRiskPatternField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspAddRiskPattern)
        self.h.SetOnRspAddRiskPattern(self.spi, self.evOnRspAddRiskPattern)

        self.h.SetOnRspModRiskPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspModRiskPattern.restype = None
        self.evOnRspModRiskPattern = CFUNCTYPE(None, POINTER(CShfeFtdcRiskPatternField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspModRiskPattern)
        self.h.SetOnRspModRiskPattern(self.spi, self.evOnRspModRiskPattern)

        self.h.SetOnRspRemRiskPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRemRiskPattern.restype = None
        self.evOnRspRemRiskPattern = CFUNCTYPE(None, POINTER(CShfeFtdcRiskPatternField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRemRiskPattern)
        self.h.SetOnRspRemRiskPattern(self.spi, self.evOnRspRemRiskPattern)

        self.h.SetOnRtnRiskPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnRiskPattern.restype = None
        self.evOnRtnRiskPattern = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskPatternField))(self.__OnRtnRiskPattern)
        self.h.SetOnRtnRiskPattern(self.spi, self.evOnRtnRiskPattern)

        self.h.SetOnRtnDelRiskPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnDelRiskPattern.restype = None
        self.evOnRtnDelRiskPattern = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskPatternField))(self.__OnRtnDelRiskPattern)
        self.h.SetOnRtnDelRiskPattern(self.spi, self.evOnRtnDelRiskPattern)

        self.h.SetOnRspAddInvestorPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspAddInvestorPattern.restype = None
        self.evOnRspAddInvestorPattern = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorPatternField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspAddInvestorPattern)
        self.h.SetOnRspAddInvestorPattern(
            self.spi, self.evOnRspAddInvestorPattern)

        self.h.SetOnRspModInvestorPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspModInvestorPattern.restype = None
        self.evOnRspModInvestorPattern = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorPatternField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspModInvestorPattern)
        self.h.SetOnRspModInvestorPattern(
            self.spi, self.evOnRspModInvestorPattern)

        self.h.SetOnRspRemInvestorPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspRemInvestorPattern.restype = None
        self.evOnRspRemInvestorPattern = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorPatternField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspRemInvestorPattern)
        self.h.SetOnRspRemInvestorPattern(
            self.spi, self.evOnRspRemInvestorPattern)

        self.h.SetOnRtnInvestorPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnInvestorPattern.restype = None
        self.evOnRtnInvestorPattern = CFUNCTYPE(None, POINTER(
            CShfeFtdcInvestorPatternField))(self.__OnRtnInvestorPattern)
        self.h.SetOnRtnInvestorPattern(self.spi, self.evOnRtnInvestorPattern)

        self.h.SetOnRtnDelInvestorPattern.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnDelInvestorPattern.restype = None
        self.evOnRtnDelInvestorPattern = CFUNCTYPE(None, POINTER(
            CShfeFtdcInvestorPatternField))(self.__OnRtnDelInvestorPattern)
        self.h.SetOnRtnDelInvestorPattern(
            self.spi, self.evOnRtnDelInvestorPattern)

        self.h.SetOnRtnRiskNotifyToken.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnRiskNotifyToken.restype = None
        self.evOnRtnRiskNotifyToken = CFUNCTYPE(None, POINTER(
            CShfeFtdcRiskNotifyTokenField))(self.__OnRtnRiskNotifyToken)
        self.h.SetOnRtnRiskNotifyToken(self.spi, self.evOnRtnRiskNotifyToken)

        self.h.SetOnRtnSeqRiskNotifyB.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSeqRiskNotifyB.restype = None
        self.evOnRtnSeqRiskNotifyB = CFUNCTYPE(None, POINTER(
            CShfeFtdcSeqRiskNotifyBField))(self.__OnRtnSeqRiskNotifyB)
        self.h.SetOnRtnSeqRiskNotifyB(self.spi, self.evOnRtnSeqRiskNotifyB)

        self.h.SetOnRspQryPositionStat.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryPositionStat.restype = None
        self.evOnRspQryPositionStat = CFUNCTYPE(None, POINTER(CShfeFtdcPositionStatField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryPositionStat)
        self.h.SetOnRspQryPositionStat(self.spi, self.evOnRspQryPositionStat)

        self.h.SetOnRspQryTradeStat.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryTradeStat.restype = None
        self.evOnRspQryTradeStat = CFUNCTYPE(None, POINTER(CShfeFtdcTradeStatField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryTradeStat)
        self.h.SetOnRspQryTradeStat(self.spi, self.evOnRspQryTradeStat)

        self.h.SetOnRspQryInvestorLinkManHash.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryInvestorLinkManHash.restype = None
        self.evOnRspQryInvestorLinkManHash = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorHashField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryInvestorLinkManHash)
        self.h.SetOnRspQryInvestorLinkManHash(
            self.spi, self.evOnRspQryInvestorLinkManHash)

        self.h.SetOnRspQryInvestorDepartmentHash.argtypes = [
            c_void_p, c_void_p]
        self.h.SetOnRspQryInvestorDepartmentHash.restype = None
        self.evOnRspQryInvestorDepartmentHash = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorHashField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryInvestorDepartmentHash)
        self.h.SetOnRspQryInvestorDepartmentHash(
            self.spi, self.evOnRspQryInvestorDepartmentHash)

        self.h.SetOnRspQryStressTest.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryStressTest.restype = None
        self.evOnRspQryStressTest = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorRiskAccountField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryStressTest)
        self.h.SetOnRspQryStressTest(self.spi, self.evOnRspQryStressTest)

        self.h.SetOnRspQryLowMarginInvestorHash.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryLowMarginInvestorHash.restype = None
        self.evOnRspQryLowMarginInvestorHash = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorHashField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryLowMarginInvestorHash)
        self.h.SetOnRspQryLowMarginInvestorHash(
            self.spi, self.evOnRspQryLowMarginInvestorHash)

        self.h.SetOnRspQryLowMarginInvestor.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryLowMarginInvestor.restype = None
        self.evOnRspQryLowMarginInvestor = CFUNCTYPE(None, POINTER(CShfeFtdcBrokerInvestorField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryLowMarginInvestor)
        self.h.SetOnRspQryLowMarginInvestor(
            self.spi, self.evOnRspQryLowMarginInvestor)

        self.h.SetOnRtnLowMarginInvestor.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnLowMarginInvestor.restype = None
        self.evOnRtnLowMarginInvestor = CFUNCTYPE(None, POINTER(
            CShfeFtdcBrokerInvestorField))(self.__OnRtnLowMarginInvestor)
        self.h.SetOnRtnLowMarginInvestor(
            self.spi, self.evOnRtnLowMarginInvestor)

        self.h.SetOnRtnDelLowMarginInvestor.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnDelLowMarginInvestor.restype = None
        self.evOnRtnDelLowMarginInvestor = CFUNCTYPE(None, POINTER(
            CShfeFtdcBrokerInvestorField))(self.__OnRtnDelLowMarginInvestor)
        self.h.SetOnRtnDelLowMarginInvestor(
            self.spi, self.evOnRtnDelLowMarginInvestor)

        self.h.SetOnRtnSeqSmsCustomNotify.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSeqSmsCustomNotify.restype = None
        self.evOnRtnSeqSmsCustomNotify = CFUNCTYPE(None, POINTER(
            CShfeFtdcSeqSmsCustomNotifyField))(self.__OnRtnSeqSmsCustomNotify)
        self.h.SetOnRtnSeqSmsCustomNotify(
            self.spi, self.evOnRtnSeqSmsCustomNotify)

        self.h.SetOnRspSetSmsStatus.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspSetSmsStatus.restype = None
        self.evOnRspSetSmsStatus = CFUNCTYPE(None, POINTER(CShfeFtdcRspInfoField), POINTER(
            c_int32), POINTER(c_bool))(self.__OnRspSetSmsStatus)
        self.h.SetOnRspSetSmsStatus(self.spi, self.evOnRspSetSmsStatus)

        self.h.SetOnRspQryExchMarginRate.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryExchMarginRate.restype = None
        self.evOnRspQryExchMarginRate = CFUNCTYPE(None, POINTER(CShfeFtdcExchMarginRateField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryExchMarginRate)
        self.h.SetOnRspQryExchMarginRate(
            self.spi, self.evOnRspQryExchMarginRate)

        self.h.SetOnRspReqQryCommissionRate.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspReqQryCommissionRate.restype = None
        self.evOnRspReqQryCommissionRate = CFUNCTYPE(None, POINTER(CShfeFtdcInstrumentCommissionRateField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspReqQryCommissionRate)
        self.h.SetOnRspReqQryCommissionRate(
            self.spi, self.evOnRspReqQryCommissionRate)

        self.h.SetOnRtnSeqIPGroupMargin.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSeqIPGroupMargin.restype = None
        self.evOnRtnSeqIPGroupMargin = CFUNCTYPE(None, POINTER(
            CShfeFtdcSeqIPGroupMarginField))(self.__OnRtnSeqIPGroupMargin)
        self.h.SetOnRtnSeqIPGroupMargin(self.spi, self.evOnRtnSeqIPGroupMargin)

        self.h.SetOnRspQrySecAgentInvestorHash.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQrySecAgentInvestorHash.restype = None
        self.evOnRspQrySecAgentInvestorHash = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorHashField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQrySecAgentInvestorHash)
        self.h.SetOnRspQrySecAgentInvestorHash(
            self.spi, self.evOnRspQrySecAgentInvestorHash)

        self.h.SetOnRspQrySecAgentInvestor.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQrySecAgentInvestor.restype = None
        self.evOnRspQrySecAgentInvestor = CFUNCTYPE(None, POINTER(CShfeFtdcSecAgentInvestorField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQrySecAgentInvestor)
        self.h.SetOnRspQrySecAgentInvestor(
            self.spi, self.evOnRspQrySecAgentInvestor)

        self.h.SetOnRtnSecAgentInvestor.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSecAgentInvestor.restype = None
        self.evOnRtnSecAgentInvestor = CFUNCTYPE(None, POINTER(
            CShfeFtdcSecAgentInvestorField))(self.__OnRtnSecAgentInvestor)
        self.h.SetOnRtnSecAgentInvestor(self.spi, self.evOnRtnSecAgentInvestor)

        self.h.SetOnRtnDelSecAgentInvestor.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnDelSecAgentInvestor.restype = None
        self.evOnRtnDelSecAgentInvestor = CFUNCTYPE(None, POINTER(
            CShfeFtdcSecAgentInvestorField))(self.__OnRtnDelSecAgentInvestor)
        self.h.SetOnRtnDelSecAgentInvestor(
            self.spi, self.evOnRtnDelSecAgentInvestor)

        self.h.SetOnRtnProductExchangeRate.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnProductExchangeRate.restype = None
        self.evOnRtnProductExchangeRate = CFUNCTYPE(None, POINTER(
            CShfeFtdcProductExchRateField))(self.__OnRtnProductExchangeRate)
        self.h.SetOnRtnProductExchangeRate(
            self.spi, self.evOnRtnProductExchangeRate)

        self.h.SetOnRspQryOptionInstrCommRate.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryOptionInstrCommRate.restype = None
        self.evOnRspQryOptionInstrCommRate = CFUNCTYPE(None, POINTER(CShfeFtdcOptionInstrCommRateField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryOptionInstrCommRate)
        self.h.SetOnRspQryOptionInstrCommRate(
            self.spi, self.evOnRspQryOptionInstrCommRate)

        self.h.SetOnRspQryMMOptionInstrCommRate.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryMMOptionInstrCommRate.restype = None
        self.evOnRspQryMMOptionInstrCommRate = CFUNCTYPE(None, POINTER(CShfeFtdcMMOptionInstrCommRateField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryMMOptionInstrCommRate)
        self.h.SetOnRspQryMMOptionInstrCommRate(
            self.spi, self.evOnRspQryMMOptionInstrCommRate)

        self.h.SetOnRspQryExecOrder.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryExecOrder.restype = None
        self.evOnRspQryExecOrder = CFUNCTYPE(None, POINTER(CShfeFtdcRiskExecOrderField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryExecOrder)
        self.h.SetOnRspQryExecOrder(self.spi, self.evOnRspQryExecOrder)

        self.h.SetOnRspQryLogUserLoginStat.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryLogUserLoginStat.restype = None
        self.evOnRspQryLogUserLoginStat = CFUNCTYPE(None, POINTER(CShfeFtdcRiskLogUserLoginStatField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryLogUserLoginStat)
        self.h.SetOnRspQryLogUserLoginStat(
            self.spi, self.evOnRspQryLogUserLoginStat)

        self.h.SetOnRspQryLogUserLoginInfo.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryLogUserLoginInfo.restype = None
        self.evOnRspQryLogUserLoginInfo = CFUNCTYPE(None, POINTER(CShfeFtdcRiskLogUserLoginInfoField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryLogUserLoginInfo)
        self.h.SetOnRspQryLogUserLoginInfo(
            self.spi, self.evOnRspQryLogUserLoginInfo)

        self.h.SetOnRspQryInstrumentGreeks.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryInstrumentGreeks.restype = None
        self.evOnRspQryInstrumentGreeks = CFUNCTYPE(None, POINTER(CShfeFtdcRiskInstrumentGreeksField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryInstrumentGreeks)
        self.h.SetOnRspQryInstrumentGreeks(
            self.spi, self.evOnRspQryInstrumentGreeks)

        self.h.SetOnRspQryExeciseTest.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryExeciseTest.restype = None
        self.evOnRspQryExeciseTest = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorTestResultField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryExeciseTest)
        self.h.SetOnRspQryExeciseTest(self.spi, self.evOnRspQryExeciseTest)

        self.h.SetOnRspQryUserRightsAssign.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryUserRightsAssign.restype = None
        self.evOnRspQryUserRightsAssign = CFUNCTYPE(None, POINTER(CShfeFtdcUserRightsAssignField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryUserRightsAssign)
        self.h.SetOnRspQryUserRightsAssign(
            self.spi, self.evOnRspQryUserRightsAssign)

        self.h.SetOnRspQryCurrDRIdentity.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQryCurrDRIdentity.restype = None
        self.evOnRspQryCurrDRIdentity = CFUNCTYPE(None, POINTER(CShfeFtdcCurrDRIdentityField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQryCurrDRIdentity)
        self.h.SetOnRspQryCurrDRIdentity(
            self.spi, self.evOnRspQryCurrDRIdentity)

        self.h.SetOnRspQrySecAgentTradingAccount.argtypes = [
            c_void_p, c_void_p]
        self.h.SetOnRspQrySecAgentTradingAccount.restype = None
        self.evOnRspQrySecAgentTradingAccount = CFUNCTYPE(None, POINTER(CShfeFtdcInvestorRiskAccountField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQrySecAgentTradingAccount)
        self.h.SetOnRspQrySecAgentTradingAccount(
            self.spi, self.evOnRspQrySecAgentTradingAccount)

        self.h.SetOnRspQrySyncDelaySwap.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQrySyncDelaySwap.restype = None
        self.evOnRspQrySyncDelaySwap = CFUNCTYPE(None, POINTER(CShfeFtdcSyncDelaySwapField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQrySyncDelaySwap)
        self.h.SetOnRspQrySyncDelaySwap(self.spi, self.evOnRspQrySyncDelaySwap)

        self.h.SetOnRspQrySecAgentCheckMode.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRspQrySecAgentCheckMode.restype = None
        self.evOnRspQrySecAgentCheckMode = CFUNCTYPE(None, POINTER(CShfeFtdcSecAgentCheckModeField), POINTER(
            CShfeFtdcRspInfoField), POINTER(c_int32), POINTER(c_bool))(self.__OnRspQrySecAgentCheckMode)
        self.h.SetOnRspQrySecAgentCheckMode(
            self.spi, self.evOnRspQrySecAgentCheckMode)

        self.h.SetOnRtnSecAgentCheckMode.argtypes = [c_void_p, c_void_p]
        self.h.SetOnRtnSecAgentCheckMode.restype = None
        self.evOnRtnSecAgentCheckMode = CFUNCTYPE(None, POINTER(
            CShfeFtdcSecAgentCheckModeField))(self.__OnRtnSecAgentCheckMode)
        self.h.SetOnRtnSecAgentCheckMode(
            self.spi, self.evOnRtnSecAgentCheckMode)

    def __OnFrontConnected(self):
        self.OnFrontConnected()

    def __OnFrontDisconnected(self, nReason):
        self.OnFrontDisconnected(nReason)

    def __OnHeartBeatWarning(self, nTimeLapse):
        self.OnHeartBeatWarning(nTimeLapse)

    def __OnRspError(self, pRspInfo, nRequestID, bIsLast):
        self.OnRspError(copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(
            pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnBrokerDeposit(self, pBrokerDeposit):
        self.OnRtnBrokerDeposit(copy.deepcopy(
            POINTER(CShfeFtdcBrokerDepositField).from_param(pBrokerDeposit).contents))

    def __OnRtnInvestorSumInfo(self, pInvestorSumInfo):
        self.OnRtnInvestorSumInfo(copy.deepcopy(
            POINTER(CShfeFtdcInvestorSumInfoField).from_param(pInvestorSumInfo).contents))

    def __OnRtnClientSGDataSyncStart(self, pSettlementSession):
        self.OnRtnClientSGDataSyncStart(copy.deepcopy(POINTER(
            CShfeFtdcSettlementSessionField).from_param(pSettlementSession).contents))

    def __OnRtnClientSGDataSyncEnd(self, pSettlementSession):
        self.OnRtnClientSGDataSyncEnd(copy.deepcopy(POINTER(
            CShfeFtdcSettlementSessionField).from_param(pSettlementSession).contents))

    def __OnRspRiskUserLogin(self, pRspRiskUserLogin, pRspInfo, nRequestID, bIsLast):
        self.OnRspRiskUserLogin(copy.deepcopy(POINTER(CShfeFtdcRspRiskUserLoginField).from_param(
            pRspRiskUserLogin).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryInvestorMarginRate(self, pInvestorMarginRate, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryInvestorMarginRate(copy.deepcopy(POINTER(CShfeFtdcInvestorMarginRateField).from_param(
            pInvestorMarginRate).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnProduct(self, pProduct):
        self.OnRtnProduct(copy.deepcopy(
            POINTER(CShfeFtdcProductField).from_param(pProduct).contents))

    def __OnRtnInstrument(self, pInstrument):
        self.OnRtnInstrument(copy.deepcopy(
            POINTER(CShfeFtdcInstrumentField).from_param(pInstrument).contents))

    def __OnRspQryOrderStat(self, pOrderStat, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryOrderStat(copy.deepcopy(POINTER(CShfeFtdcOrderStatField).from_param(pOrderStat).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnExchange(self, pExchange):
        self.OnRtnExchange(copy.deepcopy(
            POINTER(CShfeFtdcExchangeField).from_param(pExchange).contents))

    def __OnRspInvestorPositionStatic(self, pInvestorPositionStatic, pRspInfo, nRequestID, bIsLast):
        self.OnRspInvestorPositionStatic(copy.deepcopy(POINTER(CShfeFtdcInvestorPositionStaticField).from_param(
            pInvestorPositionStatic).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspInvestorTradeStatic(self, pInvestorTradeStatic, pRspInfo, nRequestID, bIsLast):
        self.OnRspInvestorTradeStatic(copy.deepcopy(POINTER(CShfeFtdcInvestorTradeStaticField).from_param(
            pInvestorTradeStatic).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnRiskDepthMarketData(self, pDepthMarketData):
        self.OnRtnRiskDepthMarketData(copy.deepcopy(
            POINTER(CShfeFtdcDepthMarketDataField).from_param(pDepthMarketData).contents))

    def __OnRtnTimeSync(self, pCurrentTime):
        self.OnRtnTimeSync(copy.deepcopy(
            POINTER(CShfeFtdcCurrentTimeField).from_param(pCurrentTime).contents))

    def __OnRspInstPositionRate(self, pRspInstPositionRate, pRspInfo, nRequestID, bIsLast):
        self.OnRspInstPositionRate(copy.deepcopy(POINTER(CShfeFtdcRspInstPositionRateField).from_param(
            pRspInstPositionRate).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspProductPositionRate(self, pRspProductPositionRate, pRspInfo, nRequestID, bIsLast):
        self.OnRspProductPositionRate(copy.deepcopy(POINTER(CShfeFtdcRspProductPositionRateField).from_param(
            pRspProductPositionRate).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryTradingCodeHash(self, pInvestorHash, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryTradingCodeHash(copy.deepcopy(POINTER(CShfeFtdcInvestorHashField).from_param(
            pInvestorHash).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryTradingCode(self, pTradingCode, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryTradingCode(copy.deepcopy(POINTER(CShfeFtdcTradingCodeField).from_param(pTradingCode).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnTradingCode(self, pTradingCode):
        self.OnRtnTradingCode(copy.deepcopy(
            POINTER(CShfeFtdcTradingCodeField).from_param(pTradingCode).contents))

    def __OnRtnDelTradingCode(self, pTradingCode):
        self.OnRtnDelTradingCode(copy.deepcopy(
            POINTER(CShfeFtdcTradingCodeField).from_param(pTradingCode).contents))

    def __OnRtnSequencialBrokerUserEvent(self, pSequencialBrokerUserEvent):
        self.OnRtnSequencialBrokerUserEvent(copy.deepcopy(POINTER(
            CShfeFtdcSequencialBrokerUserEventField).from_param(pSequencialBrokerUserEvent).contents))

    def __OnRtnSequencialTrade(self, pSequencialTrade):
        self.OnRtnSequencialTrade(copy.deepcopy(
            POINTER(CShfeFtdcSequencialTradeField).from_param(pSequencialTrade).contents))

    def __OnRtnSequencialOrder(self, pSequencialOrder):
        self.OnRtnSequencialOrder(copy.deepcopy(
            POINTER(CShfeFtdcSequencialOrderField).from_param(pSequencialOrder).contents))

    def __OnRspRiskOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        self.OnRspRiskOrderInsert(copy.deepcopy(POINTER(CShfeFtdcInputOrderField).from_param(pInputOrder).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspRiskOrderAction(self, pInputOrderAction, pRspInfo, nRequestID, bIsLast):
        self.OnRspRiskOrderAction(copy.deepcopy(POINTER(CShfeFtdcInputOrderActionField).from_param(
            pInputOrderAction).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnSequencialPosition(self, pSequencialPosition):
        self.OnRtnSequencialPosition(copy.deepcopy(POINTER(
            CShfeFtdcSequencialPositionField).from_param(pSequencialPosition).contents))

    def __OnRspRiskNotifyCommand(self, pRspInfo, nRequestID, bIsLast):
        self.OnRspRiskNotifyCommand(copy.deepcopy(POINTER(
            CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspBatchForceCloseCalc(self, pRspForceClosePosition, pRspInfo, nRequestID, bIsLast):
        self.OnRspBatchForceCloseCalc(copy.deepcopy(POINTER(CShfeFtdcRspForceClosePositionField).from_param(
            pRspForceClosePosition).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspForceCloseCalc(self, pRspForceClosePosition, pRspInfo, nRequestID, bIsLast):
        self.OnRspForceCloseCalc(copy.deepcopy(POINTER(CShfeFtdcRspForceClosePositionField).from_param(
            pRspForceClosePosition).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspSetIndexNPPParam(self, pIndexNPPParam, pRspInfo, nRequestID, bIsLast):
        self.OnRspSetIndexNPPParam(copy.deepcopy(POINTER(CShfeFtdcIndexNPPParamField).from_param(
            pIndexNPPParam).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnIndexNPP(self, pIndexNPP):
        self.OnRtnIndexNPP(copy.deepcopy(
            POINTER(CShfeFtdcIndexNPPField).from_param(pIndexNPP).contents))

    def __OnRspRemIndexNPPParam(self, pIndexNPPParam, pRspInfo, nRequestID, bIsLast):
        self.OnRspRemIndexNPPParam(copy.deepcopy(POINTER(CShfeFtdcIndexNPPParamField).from_param(
            pIndexNPPParam).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspForceCloseAccount(self, pInvestorRiskAccount, pRspInfo, nRequestID, bIsLast):
        self.OnRspForceCloseAccount(copy.deepcopy(POINTER(CShfeFtdcInvestorRiskAccountField).from_param(
            pInvestorRiskAccount).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryLogin(self, pNormalRiskQuery, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryLogin(copy.deepcopy(POINTER(CShfeFtdcNormalRiskQueryField).from_param(pNormalRiskQuery).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQrySafePriceRange(self, pSafePriceRange, pRspInfo, nRequestID, bIsLast):
        self.OnRspQrySafePriceRange(copy.deepcopy(POINTER(CShfeFtdcSafePriceRangeField).from_param(
            pSafePriceRange).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQrySafePriceRangeAccount(self, pInvestorRiskAccount, pRspInfo, nRequestID, bIsLast):
        self.OnRspQrySafePriceRangeAccount(copy.deepcopy(POINTER(CShfeFtdcInvestorRiskAccountField).from_param(
            pInvestorRiskAccount).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryPriceVaryEffect(self, pPriceVaryParam, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryPriceVaryEffect(copy.deepcopy(POINTER(CShfeFtdcPriceVaryParamField).from_param(
            pPriceVaryParam).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnDepartment(self, pDepartment):
        self.OnRtnDepartment(copy.deepcopy(
            POINTER(CShfeFtdcDepartmentField).from_param(pDepartment).contents))

    def __OnRspIndexNPP(self, pIndexNPP, pRspInfo, nRequestID, bIsLast):
        self.OnRspIndexNPP(copy.deepcopy(POINTER(CShfeFtdcIndexNPPField).from_param(pIndexNPP).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnTradeParam(self, pTradeParam):
        self.OnRtnTradeParam(copy.deepcopy(
            POINTER(CShfeFtdcTradeParamField).from_param(pTradeParam).contents))

    def __OnRspRiskParkedOrderInsert(self, pRiskParkedOrder, pRspInfo, nRequestID, bIsLast):
        self.OnRspRiskParkedOrderInsert(copy.deepcopy(POINTER(CShfeFtdcRiskParkedOrderField).from_param(
            pRiskParkedOrder).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspRemoveRiskParkedOrder(self, pRemoveRiskParkedOrder, pRspInfo, nRequestID, bIsLast):
        self.OnRspRemoveRiskParkedOrder(copy.deepcopy(POINTER(CShfeFtdcRemoveRiskParkedOrderField).from_param(
            pRemoveRiskParkedOrder).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnSeqRiskParkedOrder(self, pSeqRiskParkedOrder):
        self.OnRtnSeqRiskParkedOrder(copy.deepcopy(POINTER(
            CShfeFtdcSeqRiskParkedOrderField).from_param(pSeqRiskParkedOrder).contents))

    def __OnRspRiskUserPasswordUpd(self, pUserPasswordUpdate, pRspInfo, nRequestID, bIsLast):
        self.OnRspRiskUserPasswordUpd(copy.deepcopy(POINTER(CShfeFtdcUserPasswordUpdateField).from_param(
            pUserPasswordUpdate).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnSeqDeposit(self, pSeqDeposit):
        self.OnRtnSeqDeposit(copy.deepcopy(
            POINTER(CShfeFtdcSeqDepositField).from_param(pSeqDeposit).contents))

    def __OnRspAddRiskUserEvent(self, pRiskUserEvent, pRspInfo, nRequestID, bIsLast):
        self.OnRspAddRiskUserEvent(copy.deepcopy(POINTER(CShfeFtdcRiskUserEventField).from_param(
            pRiskUserEvent).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryPredictRiskAccount(self, pPredictRiskAccount, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryPredictRiskAccount(copy.deepcopy(POINTER(CShfeFtdcPredictRiskAccountField).from_param(
            pPredictRiskAccount).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryPredictRiskPosition(self, pPredictRiskPosition, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryPredictRiskPosition(copy.deepcopy(POINTER(CShfeFtdcPredictRiskPositionField).from_param(
            pPredictRiskPosition).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnRiskInvestor(self, pRiskSyncInvestor):
        self.OnRtnRiskInvestor(copy.deepcopy(
            POINTER(CShfeFtdcRiskSyncInvestorField).from_param(pRiskSyncInvestor).contents))

    def __OnRspQryInvestorLinkMan(self, pInvestorLinkMan, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryInvestorLinkMan(copy.deepcopy(POINTER(CShfeFtdcInvestorLinkManField).from_param(
            pInvestorLinkMan).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryInvestorDepartment(self, pInvestorDepartmentFlat, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryInvestorDepartment(copy.deepcopy(POINTER(CShfeFtdcInvestorDepartmentFlatField).from_param(
            pInvestorDepartmentFlat).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnDelIndexNPP(self, pIndexNPP):
        self.OnRtnDelIndexNPP(copy.deepcopy(
            POINTER(CShfeFtdcIndexNPPField).from_param(pIndexNPP).contents))

    def __OnRtnRiskUserFunction(self, pRiskUserFunction):
        self.OnRtnRiskUserFunction(copy.deepcopy(
            POINTER(CShfeFtdcRiskUserFunctionField).from_param(pRiskUserFunction).contents))

    def __OnRtnDelRiskUserFunction(self, pRiskUserFunction):
        self.OnRtnDelRiskUserFunction(copy.deepcopy(
            POINTER(CShfeFtdcRiskUserFunctionField).from_param(pRiskUserFunction).contents))

    def __OnRtnRiskSyncAccount(self, pRiskSyncAccount):
        self.OnRtnRiskSyncAccount(copy.deepcopy(
            POINTER(CShfeFtdcRiskSyncAccountField).from_param(pRiskSyncAccount).contents))

    def __OnRtnSeqPreRiskAccount(self, pSeqPreRiskAccount):
        self.OnRtnSeqPreRiskAccount(copy.deepcopy(POINTER(
            CShfeFtdcSeqPreRiskAccountField).from_param(pSeqPreRiskAccount).contents))

    def __OnRtnNoticeToken(self, pNoticeToken):
        self.OnRtnNoticeToken(copy.deepcopy(
            POINTER(CShfeFtdcNoticeTokenField).from_param(pNoticeToken).contents))

    def __OnRtnNoticePattern(self, pNoticePattern):
        self.OnRtnNoticePattern(copy.deepcopy(
            POINTER(CShfeFtdcNoticePatternField).from_param(pNoticePattern).contents))

    def __OnRspModNoticePattern(self, pNoticePattern, pRspInfo, nRequestID, bIsLast):
        self.OnRspModNoticePattern(copy.deepcopy(POINTER(CShfeFtdcNoticePatternField).from_param(
            pNoticePattern).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnVaryMarketData(self, pVaryMarketData):
        self.OnRtnVaryMarketData(copy.deepcopy(
            POINTER(CShfeFtdcVaryMarketDataField).from_param(pVaryMarketData).contents))

    def __OnRspAddRiskNotifyA(self, pRspInfo, nRequestID, bIsLast):
        self.OnRspAddRiskNotifyA(copy.deepcopy(POINTER(
            CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspAddBizNotice(self, pRspInfo, nRequestID, bIsLast):
        self.OnRspAddBizNotice(copy.deepcopy(POINTER(
            CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnSeqBizNotice(self, pSeqBizNotice):
        self.OnRtnSeqBizNotice(copy.deepcopy(
            POINTER(CShfeFtdcSeqBizNoticeField).from_param(pSeqBizNotice).contents))

    def __OnRspRiskQryBrokerDeposit(self, pQueryBrokerDeposit, pRspInfo, nRequestID, bIsLast):
        self.OnRspRiskQryBrokerDeposit(copy.deepcopy(POINTER(CShfeFtdcQueryBrokerDepositField).from_param(
            pQueryBrokerDeposit).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnRiskParamInfo(self, pRiskParamInfo):
        self.OnRtnRiskParamInfo(copy.deepcopy(
            POINTER(CShfeFtdcRiskParamInfoField).from_param(pRiskParamInfo).contents))

    def __OnRspModRiskInvestorParam(self, pRiskInvestorParam, pRspInfo, nRequestID, bIsLast):
        self.OnRspModRiskInvestorParam(copy.deepcopy(POINTER(CShfeFtdcRiskInvestorParamField).from_param(
            pRiskInvestorParam).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspRemRiskInvestorParam(self, pRiskInvestorParam, pRspInfo, nRequestID, bIsLast):
        self.OnRspRemRiskInvestorParam(copy.deepcopy(POINTER(CShfeFtdcRiskInvestorParamField).from_param(
            pRiskInvestorParam).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnRiskInvestorParam(self, pRiskInvestorParam):
        self.OnRtnRiskInvestorParam(copy.deepcopy(POINTER(
            CShfeFtdcRiskInvestorParamField).from_param(pRiskInvestorParam).contents))

    def __OnRtnDelRiskInvestorParam(self, pRiskInvestorParam):
        self.OnRtnDelRiskInvestorParam(copy.deepcopy(POINTER(
            CShfeFtdcRiskInvestorParamField).from_param(pRiskInvestorParam).contents))

    def __OnRspForceRiskUserLogout(self, pRiskLoginInfo, pRspInfo, nRequestID, bIsLast):
        self.OnRspForceRiskUserLogout(copy.deepcopy(POINTER(CShfeFtdcRiskLoginInfoField).from_param(
            pRiskLoginInfo).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnForceRiskUserLogout(self, pRiskLoginInfo):
        self.OnRtnForceRiskUserLogout(copy.deepcopy(
            POINTER(CShfeFtdcRiskLoginInfoField).from_param(pRiskLoginInfo).contents))

    def __OnRspAddRiskPattern(self, pRiskPattern, pRspInfo, nRequestID, bIsLast):
        self.OnRspAddRiskPattern(copy.deepcopy(POINTER(CShfeFtdcRiskPatternField).from_param(pRiskPattern).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspModRiskPattern(self, pRiskPattern, pRspInfo, nRequestID, bIsLast):
        self.OnRspModRiskPattern(copy.deepcopy(POINTER(CShfeFtdcRiskPatternField).from_param(pRiskPattern).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspRemRiskPattern(self, pRiskPattern, pRspInfo, nRequestID, bIsLast):
        self.OnRspRemRiskPattern(copy.deepcopy(POINTER(CShfeFtdcRiskPatternField).from_param(pRiskPattern).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnRiskPattern(self, pRiskPattern):
        self.OnRtnRiskPattern(copy.deepcopy(
            POINTER(CShfeFtdcRiskPatternField).from_param(pRiskPattern).contents))

    def __OnRtnDelRiskPattern(self, pRiskPattern):
        self.OnRtnDelRiskPattern(copy.deepcopy(
            POINTER(CShfeFtdcRiskPatternField).from_param(pRiskPattern).contents))

    def __OnRspAddInvestorPattern(self, pInvestorPattern, pRspInfo, nRequestID, bIsLast):
        self.OnRspAddInvestorPattern(copy.deepcopy(POINTER(CShfeFtdcInvestorPatternField).from_param(
            pInvestorPattern).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspModInvestorPattern(self, pInvestorPattern, pRspInfo, nRequestID, bIsLast):
        self.OnRspModInvestorPattern(copy.deepcopy(POINTER(CShfeFtdcInvestorPatternField).from_param(
            pInvestorPattern).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspRemInvestorPattern(self, pInvestorPattern, pRspInfo, nRequestID, bIsLast):
        self.OnRspRemInvestorPattern(copy.deepcopy(POINTER(CShfeFtdcInvestorPatternField).from_param(
            pInvestorPattern).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnInvestorPattern(self, pInvestorPattern):
        self.OnRtnInvestorPattern(copy.deepcopy(
            POINTER(CShfeFtdcInvestorPatternField).from_param(pInvestorPattern).contents))

    def __OnRtnDelInvestorPattern(self, pInvestorPattern):
        self.OnRtnDelInvestorPattern(copy.deepcopy(
            POINTER(CShfeFtdcInvestorPatternField).from_param(pInvestorPattern).contents))

    def __OnRtnRiskNotifyToken(self, pRiskNotifyToken):
        self.OnRtnRiskNotifyToken(copy.deepcopy(
            POINTER(CShfeFtdcRiskNotifyTokenField).from_param(pRiskNotifyToken).contents))

    def __OnRtnSeqRiskNotifyB(self, pSeqRiskNotifyB):
        self.OnRtnSeqRiskNotifyB(copy.deepcopy(
            POINTER(CShfeFtdcSeqRiskNotifyBField).from_param(pSeqRiskNotifyB).contents))

    def __OnRspQryPositionStat(self, pPositionStat, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryPositionStat(copy.deepcopy(POINTER(CShfeFtdcPositionStatField).from_param(pPositionStat).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryTradeStat(self, pTradeStat, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryTradeStat(copy.deepcopy(POINTER(CShfeFtdcTradeStatField).from_param(pTradeStat).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryInvestorLinkManHash(self, pInvestorHash, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryInvestorLinkManHash(copy.deepcopy(POINTER(CShfeFtdcInvestorHashField).from_param(
            pInvestorHash).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryInvestorDepartmentHash(self, pInvestorHash, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryInvestorDepartmentHash(copy.deepcopy(POINTER(CShfeFtdcInvestorHashField).from_param(
            pInvestorHash).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryStressTest(self, pInvestorRiskAccount, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryStressTest(copy.deepcopy(POINTER(CShfeFtdcInvestorRiskAccountField).from_param(
            pInvestorRiskAccount).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryLowMarginInvestorHash(self, pInvestorHash, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryLowMarginInvestorHash(copy.deepcopy(POINTER(CShfeFtdcInvestorHashField).from_param(
            pInvestorHash).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryLowMarginInvestor(self, pBrokerInvestor, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryLowMarginInvestor(copy.deepcopy(POINTER(CShfeFtdcBrokerInvestorField).from_param(
            pBrokerInvestor).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnLowMarginInvestor(self, pBrokerInvestor):
        self.OnRtnLowMarginInvestor(copy.deepcopy(
            POINTER(CShfeFtdcBrokerInvestorField).from_param(pBrokerInvestor).contents))

    def __OnRtnDelLowMarginInvestor(self, pBrokerInvestor):
        self.OnRtnDelLowMarginInvestor(copy.deepcopy(
            POINTER(CShfeFtdcBrokerInvestorField).from_param(pBrokerInvestor).contents))

    def __OnRtnSeqSmsCustomNotify(self, pSeqSmsCustomNotify):
        self.OnRtnSeqSmsCustomNotify(copy.deepcopy(POINTER(
            CShfeFtdcSeqSmsCustomNotifyField).from_param(pSeqSmsCustomNotify).contents))

    def __OnRspSetSmsStatus(self, pRspInfo, nRequestID, bIsLast):
        self.OnRspSetSmsStatus(copy.deepcopy(POINTER(
            CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryExchMarginRate(self, pExchMarginRate, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryExchMarginRate(copy.deepcopy(POINTER(CShfeFtdcExchMarginRateField).from_param(
            pExchMarginRate).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspReqQryCommissionRate(self, pInstrumentCommissionRate, pRspInfo, nRequestID, bIsLast):
        self.OnRspReqQryCommissionRate(copy.deepcopy(POINTER(CShfeFtdcInstrumentCommissionRateField).from_param(
            pInstrumentCommissionRate).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnSeqIPGroupMargin(self, pSeqIPGroupMargin):
        self.OnRtnSeqIPGroupMargin(copy.deepcopy(
            POINTER(CShfeFtdcSeqIPGroupMarginField).from_param(pSeqIPGroupMargin).contents))

    def __OnRspQrySecAgentInvestorHash(self, pInvestorHash, pRspInfo, nRequestID, bIsLast):
        self.OnRspQrySecAgentInvestorHash(copy.deepcopy(POINTER(CShfeFtdcInvestorHashField).from_param(
            pInvestorHash).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQrySecAgentInvestor(self, pSecAgentInvestor, pRspInfo, nRequestID, bIsLast):
        self.OnRspQrySecAgentInvestor(copy.deepcopy(POINTER(CShfeFtdcSecAgentInvestorField).from_param(
            pSecAgentInvestor).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnSecAgentInvestor(self, pSecAgentInvestor):
        self.OnRtnSecAgentInvestor(copy.deepcopy(
            POINTER(CShfeFtdcSecAgentInvestorField).from_param(pSecAgentInvestor).contents))

    def __OnRtnDelSecAgentInvestor(self, pSecAgentInvestor):
        self.OnRtnDelSecAgentInvestor(copy.deepcopy(
            POINTER(CShfeFtdcSecAgentInvestorField).from_param(pSecAgentInvestor).contents))

    def __OnRtnProductExchangeRate(self, pProductExchRate):
        self.OnRtnProductExchangeRate(copy.deepcopy(
            POINTER(CShfeFtdcProductExchRateField).from_param(pProductExchRate).contents))

    def __OnRspQryOptionInstrCommRate(self, pOptionInstrCommRate, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryOptionInstrCommRate(copy.deepcopy(POINTER(CShfeFtdcOptionInstrCommRateField).from_param(
            pOptionInstrCommRate).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryMMOptionInstrCommRate(self, pMMOptionInstrCommRate, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryMMOptionInstrCommRate(copy.deepcopy(POINTER(CShfeFtdcMMOptionInstrCommRateField).from_param(
            pMMOptionInstrCommRate).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryExecOrder(self, pRiskExecOrder, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryExecOrder(copy.deepcopy(POINTER(CShfeFtdcRiskExecOrderField).from_param(pRiskExecOrder).contents), copy.deepcopy(
            POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryLogUserLoginStat(self, pRiskLogUserLoginStat, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryLogUserLoginStat(copy.deepcopy(POINTER(CShfeFtdcRiskLogUserLoginStatField).from_param(
            pRiskLogUserLoginStat).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryLogUserLoginInfo(self, pRiskLogUserLoginInfo, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryLogUserLoginInfo(copy.deepcopy(POINTER(CShfeFtdcRiskLogUserLoginInfoField).from_param(
            pRiskLogUserLoginInfo).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryInstrumentGreeks(self, pRiskInstrumentGreeks, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryInstrumentGreeks(copy.deepcopy(POINTER(CShfeFtdcRiskInstrumentGreeksField).from_param(
            pRiskInstrumentGreeks).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryExeciseTest(self, pInvestorTestResult, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryExeciseTest(copy.deepcopy(POINTER(CShfeFtdcInvestorTestResultField).from_param(
            pInvestorTestResult).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryUserRightsAssign(self, pUserRightsAssign, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryUserRightsAssign(copy.deepcopy(POINTER(CShfeFtdcUserRightsAssignField).from_param(
            pUserRightsAssign).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQryCurrDRIdentity(self, pCurrDRIdentity, pRspInfo, nRequestID, bIsLast):
        self.OnRspQryCurrDRIdentity(copy.deepcopy(POINTER(CShfeFtdcCurrDRIdentityField).from_param(
            pCurrDRIdentity).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQrySecAgentTradingAccount(self, pInvestorRiskAccount, pRspInfo, nRequestID, bIsLast):
        self.OnRspQrySecAgentTradingAccount(copy.deepcopy(POINTER(CShfeFtdcInvestorRiskAccountField).from_param(
            pInvestorRiskAccount).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQrySyncDelaySwap(self, pSyncDelaySwap, pRspInfo, nRequestID, bIsLast):
        self.OnRspQrySyncDelaySwap(copy.deepcopy(POINTER(CShfeFtdcSyncDelaySwapField).from_param(
            pSyncDelaySwap).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRspQrySecAgentCheckMode(self, pSecAgentCheckMode, pRspInfo, nRequestID, bIsLast):
        self.OnRspQrySecAgentCheckMode(copy.deepcopy(POINTER(CShfeFtdcSecAgentCheckModeField).from_param(
            pSecAgentCheckMode).contents), copy.deepcopy(POINTER(CShfeFtdcRspInfoField).from_param(pRspInfo).contents), nRequestID, bIsLast)

    def __OnRtnSecAgentCheckMode(self, pSecAgentCheckMode):
        self.OnRtnSecAgentCheckMode(copy.deepcopy(POINTER(
            CShfeFtdcSecAgentCheckModeField).from_param(pSecAgentCheckMode).contents))

    def OnFrontConnected(self, ):
        print('===OnRspRiskUserLogin===: ')

    def OnFrontDisconnected(self, nReason: int):
        print('===OnRspRiskUserLogin===: nReason: int')

    def OnHeartBeatWarning(self, nTimeLapse: int):
        print('===OnRspRiskUserLogin===: nTimeLapse: int')

    def OnRspError(self, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnBrokerDeposit(self, pBrokerDeposit: CShfeFtdcBrokerDepositField):
        print('===OnRspRiskUserLogin===: pBrokerDeposit: CShfeFtdcBrokerDepositField')

    def OnRtnInvestorSumInfo(self, pInvestorSumInfo: CShfeFtdcInvestorSumInfoField):
        print('===OnRspRiskUserLogin===: pInvestorSumInfo: CShfeFtdcInvestorSumInfoField')

    def OnRtnClientSGDataSyncStart(self, pSettlementSession: CShfeFtdcSettlementSessionField):
        print(
            '===OnRspRiskUserLogin===: pSettlementSession: CShfeFtdcSettlementSessionField')

    def OnRtnClientSGDataSyncEnd(self, pSettlementSession: CShfeFtdcSettlementSessionField):
        print(
            '===OnRspRiskUserLogin===: pSettlementSession: CShfeFtdcSettlementSessionField')

    def OnRspRiskUserLogin(self, pRspRiskUserLogin: CShfeFtdcRspRiskUserLoginField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspRiskUserLogin: CShfeFtdcRspRiskUserLoginField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryInvestorMarginRate(self, pInvestorMarginRate: CShfeFtdcInvestorMarginRateField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorMarginRate: CShfeFtdcInvestorMarginRateField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnProduct(self, pProduct: CShfeFtdcProductField):
        print('===OnRspRiskUserLogin===: pProduct: CShfeFtdcProductField')

    def OnRtnInstrument(self, pInstrument: CShfeFtdcInstrumentField):
        print('===OnRspRiskUserLogin===: pInstrument: CShfeFtdcInstrumentField')

    def OnRspQryOrderStat(self, pOrderStat: CShfeFtdcOrderStatField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pOrderStat: CShfeFtdcOrderStatField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnExchange(self, pExchange: CShfeFtdcExchangeField):
        print('===OnRspRiskUserLogin===: pExchange: CShfeFtdcExchangeField')

    def OnRspInvestorPositionStatic(self, pInvestorPositionStatic: CShfeFtdcInvestorPositionStaticField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorPositionStatic: CShfeFtdcInvestorPositionStaticField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspInvestorTradeStatic(self, pInvestorTradeStatic: CShfeFtdcInvestorTradeStaticField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorTradeStatic: CShfeFtdcInvestorTradeStaticField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnRiskDepthMarketData(self, pDepthMarketData: CShfeFtdcDepthMarketDataField):
        print('===OnRspRiskUserLogin===: pDepthMarketData: CShfeFtdcDepthMarketDataField')

    def OnRtnTimeSync(self, pCurrentTime: CShfeFtdcCurrentTimeField):
        print('===OnRspRiskUserLogin===: pCurrentTime: CShfeFtdcCurrentTimeField')

    def OnRspInstPositionRate(self, pRspInstPositionRate: CShfeFtdcRspInstPositionRateField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspInstPositionRate: CShfeFtdcRspInstPositionRateField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspProductPositionRate(self, pRspProductPositionRate: CShfeFtdcRspProductPositionRateField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspProductPositionRate: CShfeFtdcRspProductPositionRateField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryTradingCodeHash(self, pInvestorHash: CShfeFtdcInvestorHashField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorHash: CShfeFtdcInvestorHashField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryTradingCode(self, pTradingCode: CShfeFtdcTradingCodeField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pTradingCode: CShfeFtdcTradingCodeField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnTradingCode(self, pTradingCode: CShfeFtdcTradingCodeField):
        print('===OnRspRiskUserLogin===: pTradingCode: CShfeFtdcTradingCodeField')

    def OnRtnDelTradingCode(self, pTradingCode: CShfeFtdcTradingCodeField):
        print('===OnRspRiskUserLogin===: pTradingCode: CShfeFtdcTradingCodeField')

    def OnRtnSequencialBrokerUserEvent(self, pSequencialBrokerUserEvent: CShfeFtdcSequencialBrokerUserEventField):
        print('===OnRspRiskUserLogin===: pSequencialBrokerUserEvent: CShfeFtdcSequencialBrokerUserEventField')

    def OnRtnSequencialTrade(self, pSequencialTrade: CShfeFtdcSequencialTradeField):
        print('===OnRspRiskUserLogin===: pSequencialTrade: CShfeFtdcSequencialTradeField')

    def OnRtnSequencialOrder(self, pSequencialOrder: CShfeFtdcSequencialOrderField):
        print('===OnRspRiskUserLogin===: pSequencialOrder: CShfeFtdcSequencialOrderField')

    def OnRspRiskOrderInsert(self, pInputOrder: CShfeFtdcInputOrderField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInputOrder: CShfeFtdcInputOrderField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspRiskOrderAction(self, pInputOrderAction: CShfeFtdcInputOrderActionField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInputOrderAction: CShfeFtdcInputOrderActionField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnSequencialPosition(self, pSequencialPosition: CShfeFtdcSequencialPositionField):
        print('===OnRspRiskUserLogin===: pSequencialPosition: CShfeFtdcSequencialPositionField')

    def OnRspRiskNotifyCommand(self, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspBatchForceCloseCalc(self, pRspForceClosePosition: CShfeFtdcRspForceClosePositionField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspForceClosePosition: CShfeFtdcRspForceClosePositionField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspForceCloseCalc(self, pRspForceClosePosition: CShfeFtdcRspForceClosePositionField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspForceClosePosition: CShfeFtdcRspForceClosePositionField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspSetIndexNPPParam(self, pIndexNPPParam: CShfeFtdcIndexNPPParamField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pIndexNPPParam: CShfeFtdcIndexNPPParamField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnIndexNPP(self, pIndexNPP: CShfeFtdcIndexNPPField):
        print('===OnRspRiskUserLogin===: pIndexNPP: CShfeFtdcIndexNPPField')

    def OnRspRemIndexNPPParam(self, pIndexNPPParam: CShfeFtdcIndexNPPParamField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pIndexNPPParam: CShfeFtdcIndexNPPParamField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspForceCloseAccount(self, pInvestorRiskAccount: CShfeFtdcInvestorRiskAccountField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorRiskAccount: CShfeFtdcInvestorRiskAccountField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryLogin(self, pNormalRiskQuery: CShfeFtdcNormalRiskQueryField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pNormalRiskQuery: CShfeFtdcNormalRiskQueryField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQrySafePriceRange(self, pSafePriceRange: CShfeFtdcSafePriceRangeField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pSafePriceRange: CShfeFtdcSafePriceRangeField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQrySafePriceRangeAccount(self, pInvestorRiskAccount: CShfeFtdcInvestorRiskAccountField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorRiskAccount: CShfeFtdcInvestorRiskAccountField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryPriceVaryEffect(self, pPriceVaryParam: CShfeFtdcPriceVaryParamField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pPriceVaryParam: CShfeFtdcPriceVaryParamField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnDepartment(self, pDepartment: CShfeFtdcDepartmentField):
        print('===OnRspRiskUserLogin===: pDepartment: CShfeFtdcDepartmentField')

    def OnRspIndexNPP(self, pIndexNPP: CShfeFtdcIndexNPPField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pIndexNPP: CShfeFtdcIndexNPPField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnTradeParam(self, pTradeParam: CShfeFtdcTradeParamField):
        print('===OnRspRiskUserLogin===: pTradeParam: CShfeFtdcTradeParamField')

    def OnRspRiskParkedOrderInsert(self, pRiskParkedOrder: CShfeFtdcRiskParkedOrderField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskParkedOrder: CShfeFtdcRiskParkedOrderField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspRemoveRiskParkedOrder(self, pRemoveRiskParkedOrder: CShfeFtdcRemoveRiskParkedOrderField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRemoveRiskParkedOrder: CShfeFtdcRemoveRiskParkedOrderField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnSeqRiskParkedOrder(self, pSeqRiskParkedOrder: CShfeFtdcSeqRiskParkedOrderField):
        print('===OnRspRiskUserLogin===: pSeqRiskParkedOrder: CShfeFtdcSeqRiskParkedOrderField')

    def OnRspRiskUserPasswordUpd(self, pUserPasswordUpdate: CShfeFtdcUserPasswordUpdateField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pUserPasswordUpdate: CShfeFtdcUserPasswordUpdateField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnSeqDeposit(self, pSeqDeposit: CShfeFtdcSeqDepositField):
        print('===OnRspRiskUserLogin===: pSeqDeposit: CShfeFtdcSeqDepositField')

    def OnRspAddRiskUserEvent(self, pRiskUserEvent: CShfeFtdcRiskUserEventField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskUserEvent: CShfeFtdcRiskUserEventField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryPredictRiskAccount(self, pPredictRiskAccount: CShfeFtdcPredictRiskAccountField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pPredictRiskAccount: CShfeFtdcPredictRiskAccountField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryPredictRiskPosition(self, pPredictRiskPosition: CShfeFtdcPredictRiskPositionField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pPredictRiskPosition: CShfeFtdcPredictRiskPositionField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnRiskInvestor(self, pRiskSyncInvestor: CShfeFtdcRiskSyncInvestorField):
        print('===OnRspRiskUserLogin===: pRiskSyncInvestor: CShfeFtdcRiskSyncInvestorField')

    def OnRspQryInvestorLinkMan(self, pInvestorLinkMan: CShfeFtdcInvestorLinkManField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorLinkMan: CShfeFtdcInvestorLinkManField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryInvestorDepartment(self, pInvestorDepartmentFlat: CShfeFtdcInvestorDepartmentFlatField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorDepartmentFlat: CShfeFtdcInvestorDepartmentFlatField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnDelIndexNPP(self, pIndexNPP: CShfeFtdcIndexNPPField):
        print('===OnRspRiskUserLogin===: pIndexNPP: CShfeFtdcIndexNPPField')

    def OnRtnRiskUserFunction(self, pRiskUserFunction: CShfeFtdcRiskUserFunctionField):
        print('===OnRspRiskUserLogin===: pRiskUserFunction: CShfeFtdcRiskUserFunctionField')

    def OnRtnDelRiskUserFunction(self, pRiskUserFunction: CShfeFtdcRiskUserFunctionField):
        print('===OnRspRiskUserLogin===: pRiskUserFunction: CShfeFtdcRiskUserFunctionField')

    def OnRtnRiskSyncAccount(self, pRiskSyncAccount: CShfeFtdcRiskSyncAccountField):
        print('===OnRspRiskUserLogin===: pRiskSyncAccount: CShfeFtdcRiskSyncAccountField')

    def OnRtnSeqPreRiskAccount(self, pSeqPreRiskAccount: CShfeFtdcSeqPreRiskAccountField):
        print(
            '===OnRspRiskUserLogin===: pSeqPreRiskAccount: CShfeFtdcSeqPreRiskAccountField')

    def OnRtnNoticeToken(self, pNoticeToken: CShfeFtdcNoticeTokenField):
        print('===OnRspRiskUserLogin===: pNoticeToken: CShfeFtdcNoticeTokenField')

    def OnRtnNoticePattern(self, pNoticePattern: CShfeFtdcNoticePatternField):
        print('===OnRspRiskUserLogin===: pNoticePattern: CShfeFtdcNoticePatternField')

    def OnRspModNoticePattern(self, pNoticePattern: CShfeFtdcNoticePatternField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pNoticePattern: CShfeFtdcNoticePatternField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnVaryMarketData(self, pVaryMarketData: CShfeFtdcVaryMarketDataField):
        print('===OnRspRiskUserLogin===: pVaryMarketData: CShfeFtdcVaryMarketDataField')

    def OnRspAddRiskNotifyA(self, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspAddBizNotice(self, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnSeqBizNotice(self, pSeqBizNotice: CShfeFtdcSeqBizNoticeField):
        print('===OnRspRiskUserLogin===: pSeqBizNotice: CShfeFtdcSeqBizNoticeField')

    def OnRspRiskQryBrokerDeposit(self, pQueryBrokerDeposit: CShfeFtdcQueryBrokerDepositField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pQueryBrokerDeposit: CShfeFtdcQueryBrokerDepositField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnRiskParamInfo(self, pRiskParamInfo: CShfeFtdcRiskParamInfoField):
        print('===OnRspRiskUserLogin===: pRiskParamInfo: CShfeFtdcRiskParamInfoField')

    def OnRspModRiskInvestorParam(self, pRiskInvestorParam: CShfeFtdcRiskInvestorParamField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskInvestorParam: CShfeFtdcRiskInvestorParamField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspRemRiskInvestorParam(self, pRiskInvestorParam: CShfeFtdcRiskInvestorParamField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskInvestorParam: CShfeFtdcRiskInvestorParamField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnRiskInvestorParam(self, pRiskInvestorParam: CShfeFtdcRiskInvestorParamField):
        print(
            '===OnRspRiskUserLogin===: pRiskInvestorParam: CShfeFtdcRiskInvestorParamField')

    def OnRtnDelRiskInvestorParam(self, pRiskInvestorParam: CShfeFtdcRiskInvestorParamField):
        print(
            '===OnRspRiskUserLogin===: pRiskInvestorParam: CShfeFtdcRiskInvestorParamField')

    def OnRspForceRiskUserLogout(self, pRiskLoginInfo: CShfeFtdcRiskLoginInfoField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskLoginInfo: CShfeFtdcRiskLoginInfoField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnForceRiskUserLogout(self, pRiskLoginInfo: CShfeFtdcRiskLoginInfoField):
        print('===OnRspRiskUserLogin===: pRiskLoginInfo: CShfeFtdcRiskLoginInfoField')

    def OnRspAddRiskPattern(self, pRiskPattern: CShfeFtdcRiskPatternField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskPattern: CShfeFtdcRiskPatternField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspModRiskPattern(self, pRiskPattern: CShfeFtdcRiskPatternField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskPattern: CShfeFtdcRiskPatternField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspRemRiskPattern(self, pRiskPattern: CShfeFtdcRiskPatternField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskPattern: CShfeFtdcRiskPatternField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnRiskPattern(self, pRiskPattern: CShfeFtdcRiskPatternField):
        print('===OnRspRiskUserLogin===: pRiskPattern: CShfeFtdcRiskPatternField')

    def OnRtnDelRiskPattern(self, pRiskPattern: CShfeFtdcRiskPatternField):
        print('===OnRspRiskUserLogin===: pRiskPattern: CShfeFtdcRiskPatternField')

    def OnRspAddInvestorPattern(self, pInvestorPattern: CShfeFtdcInvestorPatternField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorPattern: CShfeFtdcInvestorPatternField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspModInvestorPattern(self, pInvestorPattern: CShfeFtdcInvestorPatternField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorPattern: CShfeFtdcInvestorPatternField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspRemInvestorPattern(self, pInvestorPattern: CShfeFtdcInvestorPatternField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorPattern: CShfeFtdcInvestorPatternField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnInvestorPattern(self, pInvestorPattern: CShfeFtdcInvestorPatternField):
        print('===OnRspRiskUserLogin===: pInvestorPattern: CShfeFtdcInvestorPatternField')

    def OnRtnDelInvestorPattern(self, pInvestorPattern: CShfeFtdcInvestorPatternField):
        print('===OnRspRiskUserLogin===: pInvestorPattern: CShfeFtdcInvestorPatternField')

    def OnRtnRiskNotifyToken(self, pRiskNotifyToken: CShfeFtdcRiskNotifyTokenField):
        print('===OnRspRiskUserLogin===: pRiskNotifyToken: CShfeFtdcRiskNotifyTokenField')

    def OnRtnSeqRiskNotifyB(self, pSeqRiskNotifyB: CShfeFtdcSeqRiskNotifyBField):
        print('===OnRspRiskUserLogin===: pSeqRiskNotifyB: CShfeFtdcSeqRiskNotifyBField')

    def OnRspQryPositionStat(self, pPositionStat: CShfeFtdcPositionStatField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pPositionStat: CShfeFtdcPositionStatField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryTradeStat(self, pTradeStat: CShfeFtdcTradeStatField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pTradeStat: CShfeFtdcTradeStatField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryInvestorLinkManHash(self, pInvestorHash: CShfeFtdcInvestorHashField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorHash: CShfeFtdcInvestorHashField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryInvestorDepartmentHash(self, pInvestorHash: CShfeFtdcInvestorHashField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorHash: CShfeFtdcInvestorHashField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryStressTest(self, pInvestorRiskAccount: CShfeFtdcInvestorRiskAccountField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorRiskAccount: CShfeFtdcInvestorRiskAccountField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryLowMarginInvestorHash(self, pInvestorHash: CShfeFtdcInvestorHashField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorHash: CShfeFtdcInvestorHashField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryLowMarginInvestor(self, pBrokerInvestor: CShfeFtdcBrokerInvestorField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pBrokerInvestor: CShfeFtdcBrokerInvestorField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnLowMarginInvestor(self, pBrokerInvestor: CShfeFtdcBrokerInvestorField):
        print('===OnRspRiskUserLogin===: pBrokerInvestor: CShfeFtdcBrokerInvestorField')

    def OnRtnDelLowMarginInvestor(self, pBrokerInvestor: CShfeFtdcBrokerInvestorField):
        print('===OnRspRiskUserLogin===: pBrokerInvestor: CShfeFtdcBrokerInvestorField')

    def OnRtnSeqSmsCustomNotify(self, pSeqSmsCustomNotify: CShfeFtdcSeqSmsCustomNotifyField):
        print('===OnRspRiskUserLogin===: pSeqSmsCustomNotify: CShfeFtdcSeqSmsCustomNotifyField')

    def OnRspSetSmsStatus(self, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryExchMarginRate(self, pExchMarginRate: CShfeFtdcExchMarginRateField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pExchMarginRate: CShfeFtdcExchMarginRateField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspReqQryCommissionRate(self, pInstrumentCommissionRate: CShfeFtdcInstrumentCommissionRateField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInstrumentCommissionRate: CShfeFtdcInstrumentCommissionRateField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnSeqIPGroupMargin(self, pSeqIPGroupMargin: CShfeFtdcSeqIPGroupMarginField):
        print('===OnRspRiskUserLogin===: pSeqIPGroupMargin: CShfeFtdcSeqIPGroupMarginField')

    def OnRspQrySecAgentInvestorHash(self, pInvestorHash: CShfeFtdcInvestorHashField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorHash: CShfeFtdcInvestorHashField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQrySecAgentInvestor(self, pSecAgentInvestor: CShfeFtdcSecAgentInvestorField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pSecAgentInvestor: CShfeFtdcSecAgentInvestorField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnSecAgentInvestor(self, pSecAgentInvestor: CShfeFtdcSecAgentInvestorField):
        print('===OnRspRiskUserLogin===: pSecAgentInvestor: CShfeFtdcSecAgentInvestorField')

    def OnRtnDelSecAgentInvestor(self, pSecAgentInvestor: CShfeFtdcSecAgentInvestorField):
        print('===OnRspRiskUserLogin===: pSecAgentInvestor: CShfeFtdcSecAgentInvestorField')

    def OnRtnProductExchangeRate(self, pProductExchRate: CShfeFtdcProductExchRateField):
        print('===OnRspRiskUserLogin===: pProductExchRate: CShfeFtdcProductExchRateField')

    def OnRspQryOptionInstrCommRate(self, pOptionInstrCommRate: CShfeFtdcOptionInstrCommRateField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pOptionInstrCommRate: CShfeFtdcOptionInstrCommRateField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryMMOptionInstrCommRate(self, pMMOptionInstrCommRate: CShfeFtdcMMOptionInstrCommRateField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pMMOptionInstrCommRate: CShfeFtdcMMOptionInstrCommRateField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryExecOrder(self, pRiskExecOrder: CShfeFtdcRiskExecOrderField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskExecOrder: CShfeFtdcRiskExecOrderField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryLogUserLoginStat(self, pRiskLogUserLoginStat: CShfeFtdcRiskLogUserLoginStatField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskLogUserLoginStat: CShfeFtdcRiskLogUserLoginStatField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryLogUserLoginInfo(self, pRiskLogUserLoginInfo: CShfeFtdcRiskLogUserLoginInfoField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskLogUserLoginInfo: CShfeFtdcRiskLogUserLoginInfoField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryInstrumentGreeks(self, pRiskInstrumentGreeks: CShfeFtdcRiskInstrumentGreeksField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pRiskInstrumentGreeks: CShfeFtdcRiskInstrumentGreeksField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryExeciseTest(self, pInvestorTestResult: CShfeFtdcInvestorTestResultField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorTestResult: CShfeFtdcInvestorTestResultField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryUserRightsAssign(self, pUserRightsAssign: CShfeFtdcUserRightsAssignField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pUserRightsAssign: CShfeFtdcUserRightsAssignField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQryCurrDRIdentity(self, pCurrDRIdentity: CShfeFtdcCurrDRIdentityField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pCurrDRIdentity: CShfeFtdcCurrDRIdentityField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQrySecAgentTradingAccount(self, pInvestorRiskAccount: CShfeFtdcInvestorRiskAccountField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pInvestorRiskAccount: CShfeFtdcInvestorRiskAccountField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQrySyncDelaySwap(self, pSyncDelaySwap: CShfeFtdcSyncDelaySwapField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pSyncDelaySwap: CShfeFtdcSyncDelaySwapField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRspQrySecAgentCheckMode(self, pSecAgentCheckMode: CShfeFtdcSecAgentCheckModeField, pRspInfo: CShfeFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        print('===OnRspRiskUserLogin===: pSecAgentCheckMode: CShfeFtdcSecAgentCheckModeField,pRspInfo: CShfeFtdcRspInfoField,nRequestID: int,bIsLast: bool')

    def OnRtnSecAgentCheckMode(self, pSecAgentCheckMode: CShfeFtdcSecAgentCheckModeField):
        print(
            '===OnRspRiskUserLogin===: pSecAgentCheckMode: CShfeFtdcSecAgentCheckModeField')
