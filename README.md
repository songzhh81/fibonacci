#                    Project FibonacciService

==========================================================

1, Project Requirements

    Implement a web service.

    1.   to support a REST GET call.

         a.   The web service accepts a number, n, as input and returns the first
              n Fibonacci numbers, starting from 0. I.e. given n = 5, appropriate
              output would represent the sequence "0 1 1 2 3".

         b.   Given a negative number, it will respond with an appropriate error.

    2.   Include whatever instructions are necessary to build and deploy/run the
         project. "deploy/run" means the web service is accepting requests and
         responding to them as appropriate.

    3.   add enough unit tests. add some functional tests. list all other tests
         you would think of.

    4.   While this project is admittedly trivial, approach it as representing a
         more complex problem that you'll have to put into production and maintain
         for 5 years.

    5.   target to finish this in 2 days.

===========================================================

2, simple version - simpleweb_fibonacci.py

    First I write a simple web server based on socket - simpleweb_fibonacci.py
    (if you want to inspect basic network programming : ), that textbook program
    call socket(), set socket, bind(), listen() in turn, and then accept(),
    receive request, make response in a main loop.

    Usage:
        # python simpleweb_fibonacci.py (first you should update HOST, PORT with
                your environment)
    Check:
        Input http request in any browser URL address bar:
        http://192.168.9.181:8888/Fibonacci (server IP = '192.168.9.181', server
                 PORT = 8888 in my development & test environment).
    Results: "
        0 1 1 2 3 5 8 13 ...
    "

Defects or TODO

    1, This simple version did not realize complete function to return fibonacci
       numbers, either test program.
    2, can introduce multi-process/thread and IO multiplexing (e.g. epoll in linux)

==========================================================

3, tornado version - tornado_fibonacci.py

  3.1,

    Relative to native socket, I prefer to use frequently-used webserver or webapp
    framework, such as wsgi+django/flask or tornado. In this project I use tornado.
    (I don't want to explain why I chose tornado instead of wsgi+django/flask : )

    Please refer to http://www.tornadoweb.org/en/stable/ to study how to install,
    deploy and develop with tornado.

    In my develop and test environment (ubuntu 14.04 ), I first download sourcecode
    of latest stable version (tornado-4.3.tar.gz), and then compile and install
    as follows:
        # tar xvzf tornado-4.3.tar.gz
        # cd tornado-4.3
        # apt-get install build-essential python-dev
        # python setup.py build
        # sudo python setup.py install

  3.2, 

    Program tornado_fibonacci.py receive request and make response. URL regular
    expression is "/fibonacci/(-?[0-9]+)", so parameter of regular request may
    be 0, positive and negative integer, otherwise return 404 Not Found.

    Received requests are forwarded to FibonacciHandler, which first parse
    parameter, if it is negative, return error infomation, otherwise call
    function _fibonacci_string to get fibonacci string.

    Function _fibonacci_string just call function _fibonacci_string_list to get
    fibonacci list, transform to string and return. 

    Function _fibonacci_string_list will return a list consisting of the first n
    (n is the parameter) fibonacci numbers.

    The formula for the n-th fibonacci number:
        f(1) = 0
        f(2) = 1
        f(n) = f(n-2) + f(n-1), when n > 2
    We can get each fibonacci number simply in turn.

  3.3,

    HOWEVER in order to OPTIMIZE performance, we can cache the fibonacci list got
    by the maximum parameter so far. Assume the maximum request parameter so far
    is maxN, and the list of the first maxN fibonacci numbers is cached as
    max_fib_str_lst, the last two elements are former1 and former2. Given the
    following parameter of request, n, if n <= maxN, we can simply take the first
    n elements of the max_fib_str_lst, else if n > maxN, we can append the
    following fibonacci number to max_fib_str_lst and update maxN, former1 and
    former2.

    FOR EXAMPLEF, if n = maxN + 1, then we append 'former1+former2' to
    max_fib_str_lst, and update former1 = former2, former2 = former1+former2,
    maxN = n. Else if n <= maxN, we just return list = max_fib_str_lst[:n], and
    don't need to modify maxN, former1 and former2.

  3.4,

    Usage:
        # python tornado_fibonacci.py (first you should update PORT with your
                environment)

    Check:

    Input http request in any browser URL address bar: 
        http://192.168.9.181:8888/fibonacci/hello
    Result:"
        404: Not Found
        "
    Input:
        http://192.168.9.181:8888/fibonacci/-4
    Result:"
        Error: negative number: -4
        "
    Input:
        http://192.168.9.181:8888/fibonacci/0
    Result:
        (empty string)

    Input:
        http://192.168.9.181:8888/fibonacci/2
    Result: "0 1"

    Input:
        http://192.168.9.181:8888/fibonacci/7
    Result: "0 1 1 2 3 5 8"

    Input:
        http://192.168.9.181:8888/fibonacci/5
    Result: "0 1 1 2 3"

    Also check by culr:
        # curl -X GET -D - http://192.168.9.181:8888/fibonacci/3
    Result: 
        "HTTP/1.1 200 OK
         Date: Thu, 17 Mar 2016 06:11:45 GMT
         Content-Length: 5
         Etag: "6317bed78cd9420cc912b16003ec4ac2c1980972"
         Content-Type: text/html; charset=UTF-8
         Server: TornadoServer/4.3

         0 1 1"

    The related log is recorded in the file /var/log/fibonacci.log (you can
    modify the logfile path).

  3.5,

    Defects or Todo

    1, Tornado default use single process, single thread mode, and IO multiplexing
       (epoll in Linux). We can use multi-process mode to provide higher performance
        and more concurrency.

    2, Tornado is just a web server and application, we can deploy and run the
       service with more instances or containers to compose a cluster, in that
       case we can combine tornado servers with reverse proxy such as nginx, and
       nginx also provide software load blance service (rand robbin or ip hash
       mode, ...), those can provide more concurrency and higher availability.

       In addition nginx+lua script can do some simple and frequent jobs, for
       example parameter check, make simple response(when n = 0, 1, or 2) and so
       on.

    3, In order to improve the flexibility of service deployment, it is necessary
       to decouple the computation of fibonacci list from request handler.

==========================================================

4, testfibonacci.py, the test of tornado_fibonacci.py

    As in project myfloat, the program testfibonacci.py is realized based on
    unittet, it's maybe better if realized based on mock.

    The program setup test cases and perform function test for tornado_fibonacci.py.
    4 test suites test different situations when parameters were 0, negative
    integers, positive integers, other random string respectively.

    Usage:
        # python testfibonacci.py (need to start tornado_fibonacci.py first, and
                you should update ServerIP, ServerPort with your environment))

    Expected results like this: "
        ....
        ----------------------------------------------------------------------
        Ran 4 tests in 0.073s

        OK
    "

    Defects or TODO

    1, may be better if based on mock
    2, Testing was somewhat simple, and did not cover as much more URL parameters
       as possible.
    3, did not simulae more clients with a large number of high concurrent requests,
       either did performance testing.

