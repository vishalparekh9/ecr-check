import common as cf
#print(cf.domain_finder('1St. Edge'))

list = [{'title': 'Data Scientist - Remote in Florida', 'location':'Remote (usa)', 'domain':'wipro.com'}]
#print(cf.get_filtered_jobs(list))

exclude_keywords = cf.get_exclude_keywords()
exclude_domains = cf.get_exclude_domains()
keywords = cf.get_keywords()
locations = cf.get_locations()
domains = ['indeed.com', 'dice.com', 'glassdoor.com']
for job in list:
    job['is_match'] = 0
    job['matched_cat'] = ''
    job['matched_keyword'] = ''
    job['matched_location'] = ''
    job['matched_exclude'] = ''
    job['matched_domain'] = ''

    mylocation = ''.join(e for e in job['location'] if e.isalpha() or e.isspace() or e.isnumeric()).strip()
    mytitle = ''.join(e for e in job['title'] if e.isalpha() or e.isspace() or e.isnumeric()).strip()
    curdomain = job['domain'].lower().strip()
    
    #match exclude
    match = set([exclude for exclude in exclude_domains if exclude.lower() == curdomain.lower().strip()])
    excludedomain = sorted(match)
    excludedomainlen = len(excludedomain)

    #match exclude
    match = set([exclude for exclude in exclude_keywords if ' ' not in exclude.lower() if exclude.lower() in mytitle.lower().strip().split()])
    match2 = set([exclude for exclude in exclude_keywords if ' ' in exclude.lower() if exclude.lower() in mytitle.lower().strip()])
    excludematch = sorted(match)
    [excludematch.append(x) for x in sorted(match2) if x not in excludematch]
    excludelen = len(excludematch)
    
    #match keywords
    match = set([keyword for keyword in keywords if ' ' not in  keyword.lower().split('|')[0].lower() if keyword.lower().split('|')[0] in mytitle.lower().strip().split()])
    match2 = set([keyword for keyword in keywords if ' ' in  keyword.lower().split('|')[0].lower() if keyword.lower().split('|')[0] in mytitle.lower().strip()])
    finalmatch = sorted(match)
    [finalmatch.append(x) for x in sorted(match2) if x not in finalmatch]
    titlelen = len(finalmatch)

    #match location
    match = [location for location in locations if ' ' not in  location.lower() if location.lower() in mylocation.lower().strip().split()]
    match2 = [location for location in locations if ' ' in  location.lower() if location.lower() in mylocation.lower().strip()]
    locmatch = sorted(match)
    locmatch.extend(x for x in sorted(match2) if x not in locmatch)
    locationlen = len(locmatch)

    if locationlen == 0 and mylocation.lower().strip() == 'remote':
        locationlen = 1
        
    domainlen = len([domain for domain in domains if domain.lower() in job['domain'].lower().strip()])

    #if titlelen > 0:
    cat = []
    uniquekey = []
    excludewords = []
    [cat.append(x.split('|')[1]) for x in finalmatch if x.split('|')[1] not in cat]
    [uniquekey.append(x.split('|')[0]) for x in finalmatch if x.split('|')[0] not in uniquekey]

    #code to check for the exclude does not available in matched keywords
    if excludelen > 0:
        excludelen = 0
        for key in excludematch:
            if len(key) > 3:
                if len([x for x in uniquekey if key.lower() in x.lower()]) == 0:
                    excludelen = 1
                    excludewords.append(key)
            else:
                excludelen = 1
                excludewords.append(key)
    
    job['matched_cat'] = ' | '.join([x for x in sorted(cat)])
    job['matched_location'] = ' | '.join([x for x in locmatch])
    job['matched_keyword'] = ' | '.join([x.replace(" ","-") for x in uniquekey])
    job['matched_exclude'] = ' | '.join([x for x in excludewords])
    #job['matched_cat'] = ' | '.join([x.split('|')[1] for x in finalmatch])
    if domainlen > 0 or excludedomainlen > 0:
        job['matched_domain'] = job['domain'].lower().strip()
    if titlelen > 0 and locationlen > 0 and domainlen == 0 and excludematch == 0 and excludedomainlen == 0:
        job['is_match'] = 1
        print(job)
    print(job['is_match'])
    print(job['matched_domain'])
    print(job['matched_cat'])
    