def uniConvert(uniData):
    return unicodedata.normalize('NFKD', uniData).encode('ascii','ignore')