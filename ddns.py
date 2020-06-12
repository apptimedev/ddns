import requests
import time


class DDNS():
    first = True
    domains = []
    ipr = 'https://domains.google.com/checkip'
    dip = 'domains.google.com'
    iptime = 3600

    currentip = requests.get(ipr).text
    myip = currentip

    def set_domain(self, domain, user, password):
        value = {
            'domain': domain,
            'user': '%s:%s' % (user, password)
        }
        self.domains.append(value)

    def set_dip(self, domain):
        self.dip = domain

    def set_time(self, iptime):
        self.iptime = iptime

    def init(self):
        print('Starting ddns')
        if len(self.domains) > 0:
            while True:
                self.get_ip()
                self.write()
        else:
            print('First set fields')

    def get_ip(self):
        if self.first:
            print('IP is %s' % self.currentip)
            self.first = False
        else:
            while self.myip == self.currentip:
                self.myip = requests.get(self.ipr).text
                print('IP is %s' % self.myip)
                if self.myip == self.currentip:
                    time.sleep(self.iptime)

    def write(self):
        for value in self.domains:
            domain = value['domain']
            user = value['user']

            print('Starting get IP on %s' % domain)

            request = 'https://%s@%s/nic/update?hostname=%s&myip=%s' % (user, self.dip, domain, self.myip)

            print('Current External IP is %s' % self.myip)

            if self.myip != '':
                print('IP has changed!! Updating on Google Domains')
                response = requests.get(request).text
                if response == "good %s" % self.myip:
                    print('Changed IP on %s' % domain)
                else:
                    print("Error: %s" % response)
            else:
                print('No changes on %s' % domain)
