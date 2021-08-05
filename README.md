# db_map
Creates an ER diagram from a mysql database schema dump.

## Dependencies
- mysql
- pyparsing
`pip install pyparsing`

## Sample usage
`python create.py --password=YOUR_PASSWORD -d YOUR_DATABASE | dot -Tpng > output.png`