import http.cookies
C = http.cookies.SimpleCookie()
C.load('keebler="E=everybody; L=\\"Loves\\"; fudge=\\012;";')
print (C)
C = http.cookies.SimpleCookie()
C.load("chips=ahoy; vienna=finger")
print (C)
