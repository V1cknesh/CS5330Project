from twitter import *
#pip install twitter

t = Twitter(auth=OAuth('1251440497257672705-datdho4HgxFZoj4AkA8c9cmi0skf8b', 'Gw9RnSjfeMzc4P415gbv494VO33fIPU5uGMCXg8qINLl1', 'ew0pmbxpjcfgMTSZcywA0Fgb7', 'fO0t6AmR2RvOoAV6aSnVzheDyzCDZz2GJmSWCDsIfjQUXk45fD'))

my_dict = t.search.tweets(q="#Avengers")

print(len(my_dict['statuses']))

for i in range(0,len(my_dict['statuses'])):
    print(my_dict['statuses'][i]['text'])






