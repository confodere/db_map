# db_map
Creates an ER diagram from a mysql database schema dump.

## Dependencies
- mysql
- pyparsing
`pip install pyparsing`

## Sample usage
    python create.py --password=YOUR_PASSWORD -d YOUR_DATABASE | dot -Tpng > output.png

## Example
![SVG](https://raw.githubusercontent.com/confodere/db_map/main/example.svg)

## Credits
Extended from [https://github.com/rm-hull/sql_graphviz](github.com/rm-hull/sql_graphviz).