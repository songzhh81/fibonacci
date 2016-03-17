# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web

import os
import sys
import logging

# server PORT
PORT = 8888

# logfile and format
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='/var/log/fibonacci.log',
                filemode='a+')

# request handler for Fibonacci Get API
class FibonacciHandler(tornado.web.RequestHandler):
    # In order to optimize performance, we can cache the fibonacci list 
    # got by the maximum parameter so far. Assume the maximum request 
    # parameter so far is maxN, and the list of the first maxN fibonacci
    # numbers is cached as max_fib_str_lst, the last two elements are 
    # former1 and former2. 
    # Given the following parameter of request, n, 
    #     if n <= maxN, we can simply take the first n elements of 
    # max_fib_str_lst, 
    #     else if n > maxN, we can append the following fibonacci number 
    # to max_fib_str_lst and update maxN, former1 and former2.
    #
    # For example, 
    #     if n = maxN + 1, then we append 'former1+former2' to max_fib_str_lst, 
    # and update former1 = former2, former2 = former1+former2, maxN = n. 
    #     Else if n <= maxN, we just return list = max_fib_str_lst[:n], and 
    # don't need to modify maxN, former1 and former2.
    max_fib_str_lst = ['0', '1']
    global_val = [2, 0, 1] # maxN, former1, former2

    def _fibonacci_string_list(self, n):
        fibs = []
        maxN = self.global_val[0]
        if n <= maxN :
            logging.debug("{0} <= {1}, we can get list from cache".format(n, maxN))
            fibs = self.max_fib_str_lst[:n]
        else:
            former1 = self.global_val[1]
            former2 = self.global_val[2]
            logging.debug("{0} > {1}, we should append cache".format(n, maxN))
            logging.debug("Now maxN={0}, former1={1}, former2={2}" 
                    .format(maxN, former1, former2))
            while maxN < n:
                this = former1 + former2
                former1 = former2
                former2 = this
                self.max_fib_str_lst.append(str(this))
                logging.debug("i = {0}, append {1}".format(maxN, this))
                maxN += 1

            self.global_val[0] = maxN
            self.global_val[1] = former1
            self.global_val[2] = former2
            logging.debug("Now maxN={0}, former1={1}, former2={2}"
                    .format(self.global_val[0], self.global_val[1], self.global_val[2]))
            fibs = self.max_fib_str_lst

        return fibs

    def _fibonacci_string(self, num):
        logging.debug("to get fibonacci_string for {0}".format(num))
        # get first num fibonacci numbers list
        fibs = self._fibonacci_string_list(num)
        # transform list to string
        return ' '.join(fibs)

    def get(self, num):
        try:
            n = int(num)
            if n < 0:
                # negative integer
                logging.error("Error: negative number: {0}".format(n))
                self.write("Error: negative number: {0}".format(n))
            else:
                # 0 or positive integer
                logging.debug("to get the first {0} Fibonacci numbers".format(n))
                fibs = self._fibonacci_string(n)
                logging.debug("the first {0} Fibonacci numbers: {1}".format(n, fibs))
                self.write(fibs)
        except:
            logging.exception("Any Format Error")
            self.write("Any Format Error")

application = tornado.web.Application([
    (r"/fibonacci/(-?[0-9]+)", FibonacciHandler), # URL format, only supports integer
])

if __name__ == "__main__":
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
