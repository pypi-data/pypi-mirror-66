import requests
import json
import numpy as np
import threading


class QuestradeData:
    loginUrl = 'https://login.questrade.com/oauth2/'

    def __init__(self):
        self.data = []
        self.accessToken = ''
        self.refreshToken = ''
        self.apiServer = ''
        self.tokenInterval = ''

    def login(self, token):
        url = QuestradeData.loginUrl + 'token?grant_type=refresh_token&refresh_token={}'.format(token)
        resp = requests.get(url)
        print('renewing ' + self.accessToken)
        if resp.ok:
            jData = json.loads(resp.content)
            self.accessToken = jData['access_token']
            self.refreshToken = jData['refresh_token']
            self.apiServer = jData['api_server']
            self.tokenInterval = jData['expires_in']
            timer = threading.Timer(self.tokenInterval/2, QuestradeData.login, [self, self.refreshToken])
            timer.start()
        else:
            print('authentication fails')

    def getCandlesWithSymbolId(self, symbolId, startTime, endTime, interval):
        url = self.apiServer + 'v1/markets/candles/{}?startTime={}&endTime={}&interval={}' \
            .format(symbolId, startTime, endTime, interval)
        headers = {'Authorization': 'Bearer {}'.format(self.accessToken)}
        resp = requests.get(url, headers=headers)
        if resp.ok:
            jData = json.loads(resp.content)
            return jData

    def searchSymbol(self, symbol):
        url = self.apiServer + 'v1/symbols/search?prefix={}'.format(symbol)
        headers = {'Authorization': 'Bearer {}'.format(self.accessToken)}
        resp = requests.get(url, headers=headers)
        if resp.ok:
            jData = json.loads(resp.content)
            return jData["symbols"][0]

    def getCandles(self, symbol, startTime, endTime, interval):
        symbol = self.searchSymbol(symbol)
        return self.getCandlesWithSymbolId(symbol['symbolId'], startTime, endTime, interval)
