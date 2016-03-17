# -*- coding: utf-8 -*-
import unittest
import httplib
import os
import random
import string

PN = 10         # number of positive integers for testing
NN = 3          # number of negative integers for testing
SN = 3          # number of random strings for testing
minN = -100     # min negative integer for testing
maxN = 500      # max positive integer for testing
ServerIP = '192.168.9.181'     # server IP
ServerPort = 8888              # server PORT

class FibonacciTest(unittest.TestCase):

    def setUp(self):

        # test cases for positive integer
        self.checkpos = []
        i = 0
        while i < PN:
            n = random.randint(1, maxN)
            self.checkpos.append(n)
            i += 1

        # test cases for negative integer
        self.checkneg = []
        i = 0
        while i < NN:
            n = random.randint(minN, -1)
            self.checkneg.append(n)
            i += 1

        # test cases for random strings
        self.checkstr = []
        i = 0
        while i < SN:
            s = string.join(random.sample(['m','l','k','j','i','h','g','f','e','d','c','b','a',
                                           '!', '@', '#', '$'], random.randint(1,10))).replace(' ','')
            self.checkstr.append(s)
            i += 1

    # test zero
    def test_fibonacci_zero(self):
        httpClient = None
        try:
            httpClient = httplib.HTTPConnection(ServerIP, ServerPort, timeout=30)
            httpClient.request('GET', '/fibonacci/0')
            response = httpClient.getresponse()
            self.assertTupleEqual((response.status, response.reason), (200, 'OK'))
            # n = 0, return 0 fibonacci numbers, nothing in other words
            self.assertEqual(response.read(), '')
        except Exception, e:
            print e
        finally:
            if httpClient:
                httpClient.close()

    # test negative integers
    def test_fibonacci_neg(self):
        i = 0
        httpClient = None
        while i < NN:
            n = self.checkneg[i]
            try:
                httpClient = httplib.HTTPConnection(ServerIP, ServerPort, timeout=30)
                httpClient.request('GET', '/fibonacci/' + str(n))

                response = httpClient.getresponse()
                self.assertTupleEqual((response.status, response.reason), (200, 'OK'))
                # if n < 0, return such warning
                self.assertEqual(response.read(), 'Error: negative number: {0}'.format(n))

            except Exception, e:
                print e
            finally:
                if httpClient:
                    httpClient.close()

            i += 1

    # test positive integers
    def test_fibonacci_pos(self):
        i = 0
        httpClient = None
        while i < PN:
            n = self.checkpos[i]
            try:
                httpClient = httplib.HTTPConnection(ServerIP, ServerPort, timeout=30)
                httpClient.request('GET', '/fibonacci/' + str(n))

                response = httpClient.getresponse()
                self.assertTupleEqual((response.status, response.reason), (200, 'OK'))

                fibstr = response.read()
                fibs = fibstr.split()
                # the 1st fibonacci number
                self.assertEqual(fibs[0], '0')

                if (n > 1):
                    # the 2nd fibonacci number
                    self.assertEqual(fibs[1], '1')
                if (n > 2):
                    j = 2
                    while j < n:
                        # the (n > 2)th fibonacci number
                        self.assertEqual(int(fibs[j]), int(fibs[j-1]) + int(fibs[j-2]))
                        j += 1

            except Exception, e:
                print e
            finally:
                if httpClient:
                    httpClient.close()

            i += 1

    # test random strings
    def test_fibonacci_str(self):
        i = 0
        httpClient = None
        while i < SN:
            s = self.checkstr[i]
            try:
                httpClient = httplib.HTTPConnection(ServerIP, ServerPort, timeout=30)
                httpClient.request('GET', '/fibonacci/' + s)

                response = httpClient.getresponse()
                self.assertTupleEqual((response.status, response.reason), (404, 'Not Found'))
                # if n < 0, return such warning
                self.assertEqual(response.read(),
                        '<html><title>404: Not Found</title><body>404: Not Found</body></html>')

            except Exception, e:
                print e
            finally:
                if httpClient:
                    httpClient.close()

            i += 1

if __name__ =='__main__': 
  unittest.main()
