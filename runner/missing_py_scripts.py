import common as cf
import sitedirectory as scraper
import unicodecsv as csv
if __name__ == "__main__":
    output = []
    output2 = []
    dbtokens, tokensinlist = cf.get_sites()
    filetokens = scraper.SITEDIRECTORY('').get_object()
    for obj in dbtokens:
        if obj['token'] in filetokens:
            obj['result'] = True
        else:
            output2.append(obj)
    
    for token in filetokens:
        obj = {'token': token, 'result': False}
        if token in tokensinlist:
            obj['result'] = True
        else:
            output.append(obj)
    try:
        keys = output2[0].keys()
        filename = 'token_not_found_in_scraper_folder.csv'
        with open(filename, 'wb') as f:
            w = csv.DictWriter(f,keys)
            w.writeheader()
            w.writerows(output2)
            f.close()
            print("crawlernotfound exported")
    except:
        pass

    try:
        keys = output[0].keys()
        filename = 'token_notfound_in_db.csv'
        with open(filename, 'wb') as f:
            w = csv.DictWriter(f,keys)
            w.writeheader()
            w.writerows(output)
            f.close()
            print("crawlernotfound exported")
    except:
        pass