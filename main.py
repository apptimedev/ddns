from ddns import DDNS

ddns = DDNS()
domain = 'domain.com'  # domain
subs = [
    {
        'domain': 'sub1',
        'user': 'abc',
        'password': 'abc'
    },
    {
        'domain': 'sub2',
        'user': 'abc',
        'password': 'abc'
    },
    {
        'domain': 'sub3',
        'user': 'abc',
        'password': 'abc'
    }
]  # sub domains
iptime = 60  # secs verify

#  ddns.set_domain(domain, user, password)  # to set domain

for value in subs:
    sub = value['domain']
    user = value['user']
    password = value['password']
    ddns.set_domain(("%s.%s" % (sub, domain)), user, password)  # to set sub domains

ddns.set_time(iptime)

ddns.init()
