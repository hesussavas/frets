# frets
Python 3.6.0 project

Simple API for getting some useful guitar info.

Firstly, user must register itself by going to the index page.
Then the API will be available for his credits by the address ```api/v1/frets/```

--
You can use numbers and letter 'x' as an input data array of frets.
Example of the request with the already registered user:
```
http POST http://127.0.0.1:5000/api/v1/frets/ frets:='[5, "x", "x", 5, 4, 5]' --auth test@example.com:123456
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
        "Adim",
        "Cm6(omit 5)/A",
        "D#6(b5,omit 3)/A"
    ],
    "fingers": [
        "2",
        "x",
        "x",
        "3",
        "1",
        "4"
    ],
    "greene_voicing": "V-5"
}
```
