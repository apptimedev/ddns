from ddns import DDNS

ddns = DDNS()
user = 'youremail@gmail.com'
password = ''
domain = 'domain.com'  # domain
subs = ['sub1', 'sub2', 'sub3']  # sub domains
iptime = 60  # secs verify

ddns.set_userpss(user, password)

ddns.set_domain(domain)  # to set domain

for sub in subs:
    ddns.set_domain("%s.%s" % (sub, domain))  # to set sub domains

ddns.set_time(iptime)

ddns.init()
