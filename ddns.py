import requests
import time
import datetime


class DDNS():
    iperror = 0
    first = True
    domains = []
    ipr1 = 'http://myexternalip.com/raw'
    ipr2 = 'http://whatismyip.akamai.com/'
    ipr3 = 'https://api.ipify.org'
    ipr4 = 'https://domains.google.com/checkip'
    dip = 'domains.google.com'
    iptime = 3600

    myip = ''
    lastip = ''

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
                if self.first:
                    self.first = False
        else:
            print('First set fields')

    def get_ip(self):
        if self.first:
            api = self.iperror + 1
            now = datetime.datetime.now()
            self.myip = self.request_ip()
            self.lastip = self.myip
            print("\nAPI %s" % api)
            print('Time: %s' % now)
            print('IP is %s' % self.myip)
        else:
            if self.myip != self.lastip:
                time.sleep(self.iptime)
            while self.myip == self.lastip:
                api = self.iperror + 1
                now = datetime.datetime.now()
                self.lastip = self.myip
                self.myip = self.request_ip()
                if now.minute == 0 or self.myip != self.lastip:
                    print("\nAPI %s" % api)
                    print('Time: %s' % now)
                    print('IP is %s' % self.myip)
                time.sleep(self.iptime)

    def write(self):
        for value in self.domains:
            domain = value['domain']
            user = value['user']

            request = 'https://%s@%s/nic/update?hostname=%s&myip=%s' % (user, self.dip, domain, self.myip)

            if self.myip != self.lastip or self.first:
                response = requests.get(request).text
                if response == "good %s" % self.myip:
                    print('Changed IP on %s' % domain)
                elif response == "nochg %s" % self.myip:
                    print('No changes on %s' % domain)
                else:
                    print("Error on %s:\n%s" % (domain, response))

    def request_ip(self):
        if self.iperror == 1:
            ipr = self.ipr2
        elif self.iperror == 2:
            ipr = self.ipr3
        else:
            ipr = self.ipr1
        try:
            reqip = requests.get(ipr).text
        except:
            if self.iperror >= 2:
                self.iperror = 0
            else:
                self.iperror += 1
            print('Request error\nChanging api')
            reqip = self.myip
        return reqip
