## httpz - A handy HTTP status code library

#### Installation

```shell script
pip install httpz
```

#### API

Get an HTTP status code

```pycon
>>> HTTPStatusCodes.get("200")
HTTPStatusCode(code=200, message=OK, description=The request has succeeded)
```

`HTTPStatusCode` objects have several useful attributes:

| Attribute | Type | Example |
| --------- | ---- | ------- |
| `code` | `int` | 200 |
| `message` | `str` | OK |
| `description` | `str` | The request has succeeded |
| `category` | `str` | successful |
| `webdav` | `bool` | `False` |
| `experimental` | `bool` | `False` |


For example:

```pycon
>>> code = HTTPStatusCodes.get("100")
>>> code.code
100
>>> code.message
'Continue'
>>> code.category
'informational'
>>> code.description
'This interim response indicates that everything so far is OK and that the client should continue the request, or ignore the response if the request is already fi
nished'
```

Calling `to_dict()` on an `HTTPStatusCode` object will return a dict:

```pycon
>>> code = HTTPStatusCodes.get("200")
>>> code.to_dict()
{'description': 'The request has succeeded', 'code': 200, 'message': 'OK', 'webdav': False, 'category': 'successful'}
```

Get a list of `HTTPStatusCode` objects by category

```pycon
>>> HTTPStatusCodes.get_category("informational")
[HTTPStatusCode(code=100, message=Continue, description=This interim response indicates that everything so far is OK and that the client should continue the reque
st, or ignore the response if the request is already finished), HTTPStatusCode(code=101, message=Switching Protocol, description=This code is sent in response to
an Upgrade request header from the client, and indicates the protocol the server is switching to), HTTPStatusCode(code=102, message=Processing, description=This c
ode indicates that the server has received and is processing the request, but no response is available yet), HTTPStatusCode(code=103, message=Early Hints, descrip
tion=This status code is primarily intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a respons
e)]
```

Categories:

- `informational` - 100 range
- `successful` - 200 range
- `redirection` - 300 range
- `client_error` - 400 range
- `server_error` - 500 range

An enum of categories is also available:

```pycon
>>> from httpz import HTTPStatusCodeCategory
>>> HTTPStatusCodeCategory.CLIENT_ERROR
<HTTPStatusCodeCategory.CLIENT_ERROR: 'client_error'>
>>> HTTPStatusCodeCategory.CLIENT_ERROR.value
'client_error'
```

An ordered list of all `HTTPStatusCode` objects (from low to high) can be obtained with:

```pycon
>>> from httpz import HTTPStatusCodes
>>> all_codes = HTTPStatusCodes.get_all()
>>> for status_code in all_codes:
...     print(status_code.code, status_code.message)
100 Continue
101 Switching Protocol
102 Processing
103 Early Hints
200 OK
201 Created
202 Accepted
203 Non-Authoritative Information
204 No Content
205 Reset Content
206 Partial Content
207 Multi-Status
208 Already Reported
226 IM Used
300 Multiple Choice
301 Moved Permanently
302 Found
303 See Other
304 Not Modified
305 Use Proxy
306 Unused
307 Temporary Redirect
308 Permanent Redirect
400 Bad Request
401 Unauthorized
402 Payment Required
403 Forbidden
404 Not Found
405 Method Not Allowed
406 Not Acceptable
407 Proxy Authentication Required
408 Request Timeout
409 Conflict
410 Gone
411 Length Required
412 Precondition Failed
413 Payload Too Large
414 URI Too Long
415 Unsupported Media Type
416 Range Not Satisfiable
417 Expectation Failed
418 I'm a teapot
421 Misdirected Request
422 Unprocessable Entity
423 Locked
424 Failed Dependency
425 Too Early
426 Upgrade Required
428 Precondition Required
429 Too Many Requests
431 Request Header Fields Too Large
451 Unavailable For Legal Reasons
500 Internal Server Error
501 Not Implemented
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
505 HTTP Version Not Supported
506 Variant Also Negotiates
507 Insufficient Storage
508 Loop Detected
510 Not Extended
511 Network Authentication Required
```