# frets
Python 3.6.0 project

Simple API for getting some useful guitar info.

Firstly, user must register itself by going to the index page.
Then the API will be available for his credits by the address ```api/v1/frets/```

--
Example of the request with the already registered user:
```
http POST http://127.0.0.1:5000/api/v1/frets/ frets:='["0", "3", "1", "2", "1", "0"]' --auth test@example.com:123456
```

Response:
```
HTTP/1.0 200 OK
Content-Length: 204
Content-Type: application/json
Date: Sat, 25 Feb 2017 02:17:34 GMT
Server: Werkzeug/0.11.15 Python/3.5.2

{
    "chord_names": [
        "Adim/C",
        "Cm6(omit 5)",
        "D#6(b5,omit 3)/C"
    ],
    "fingers": [
        "0",
        "4",
        "1",
        "3",
        "2",
        "0"
    ],
    "greene_voicing": "V-11"
}
```
