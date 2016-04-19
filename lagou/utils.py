
def dict2str(dataDict):
    res = ''
    for key in dataDict:
        res += key + '='
        if isinstance(dataDict[key], str):
            res += '"' + dataDict[key] + '"'
        else:
            res += str(dataDict[key]) 
        res += ','
    return res[0:-1]

if __name__ == '__main__':
    print(dict2str({"job_id": 1}))
    s = '8k-1'
    low, high = s.split('-')
    print(high[0: -1])