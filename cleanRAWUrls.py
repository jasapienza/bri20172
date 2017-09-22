# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 11:49:31 2016

@author: Jose Augusto Sapienza Ramos
"""

import re
import csv

with open('rawurls.txt','r') as rawfile:
    urls = re.findall("(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",rawfile.read())
    unique_urls = set([item[0]+'://'+item[1]+item[2] for item in urls])
    with open('urls_non_source.csv','wb') as csvfile:
        writer = csv.writer(csvfile,delimiter=';',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['URL'])
        for url in unique_urls:
            writer.writerow([url])
print 'Done!'