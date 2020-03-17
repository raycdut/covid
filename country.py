class country_trend():
    def __init__(self, _id,_confirmedCount, _confirmedIncr, _curedCount, _curedIncr, _currentConfirmedCount, _currentconfirmedIncr, _dateid, _deadCount, _deadIncr):
        self.id=_id 
        self.confirmedCount = _confirmedCount
        self.confirmedIncr = _confirmedIncr
        self.curedCount = _curedCount
        self.curedIncr = _curedIncr
        self.currentConfirmedCount = _currentConfirmedCount
        self.currentConfirmedIncr = _currentconfirmedIncr
        self.date = _dateid
        self.deadCount = _deadCount
        self.deadIncr = _deadIncr
    

class country():
    def __init__(self, _id, _continents, _countryNameCN, _countryNameEN, _countryShortNameEN, _statisticData):
        if _countryShortNameEN == 'CHN':
            self.id = 100000000
        else:
            self.id = _id
        self.continents = _continents
        self.countryNameCN = _countryNameCN
        self.countryNameEN = _countryNameEN
        self.countryShortNameEN = _countryShortNameEN
        self.statisticData = _statisticData
