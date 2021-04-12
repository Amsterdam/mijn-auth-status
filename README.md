Authentication status check API
==============

Indicates if user is authenticated and shows the user type.
Allows checking authentication status through authentication layer.


## Development

From the project root run:

`PYTHONPATH=. python authstatus/server.py`


## Testing

Run tests with

` ./test.sh `

## Swagger UI

Swagger UI is available at `{base_path}/ui`.
Where the`base_path` is defined in the swagger specification.

In development try:

[http://localhost:8765/auth/ui/](http://localhost:8763/auth/ui/)
