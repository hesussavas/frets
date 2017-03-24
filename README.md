# frets
Python 3.6.0 project

Simple API for getting some useful guitar info.

Firstly, user must register itself by going to the index page.
Then the API will be available for his credits by the address ```api/v1/frets/```

--
Example of the request with the already registered user:
```
http POST http://127.0.0.1:5000/api/v1/frets/ frets:=[1,1,1,1,1,1] --auth test@example.com:123456
```

For now the API will respond with the mocked result like this:
```
HTTP/1.0 200 OK
Content-Length: 204
Content-Type: application/json
Date: Sat, 25 Feb 2017 02:17:34 GMT
Server: Werkzeug/0.11.15 Python/3.5.2

{
    "caged": "C",
    "chord_names": [
        "C7",
        "E#m(b13)",
        "Badd13"
    ],
    "fingers": [
        0,
        1,
        4,
        2,
        3,
        0
    ],
    "greene_voicing": "V-2",
    "voicing": "drop 3"
}
```
