import requests
import time


class DDNS():
    first = True
    domains = []
    ipr = 'http://whatismyip.akamai.com/'
    dip = 'domains.google.com'
    iptime = 3600

    myip = requests.get(ipr).text
    lastip = myip

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
            print('IP is %s' % self.myip)
            self.first = False
        else:
            while self.myip == self.lastip:
                self.lastip = self.myip
                self.myip = requests.get(self.ipr).text
                if self.myip != self.lastip:
                    print('IP is %s' % self.myip)
                if len(self.myip) > 18:
                    print('IP error')
                time.sleep(self.iptime)


    def write(self):
        for value in self.domains:
            domain = value['domain']
            user = value['user']

            request = 'https://%s@%s/nic/update?hostname=%s&myip=%s' % (user, self.dip, domain, self.myip)

            if self.myip != '':
                response = requests.get(request).text
                if response == "good %s" % self.myip:
                    print('Changed IP on %s' % domain)
                elif response == "nochg %s" % self.myip:
                    print('No changes on %s' % domain)
                else:
                    print("Error on %s:\n%s" % (domain, response))
            else:
                print('No changes on %s' % domain)
