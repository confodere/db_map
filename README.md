# db_map
Creates an ER diagram from a mysql database schema dump.

## Dependencies
- mysql
- pyparsing
`pip install pyparsing`

## Sample usage
Inputting SQL yourself:

    mysqldump YOUR_DATABASE --compact --no-data --password=YOUR_PASSWORD > example.sql
    python create.py --file=example.sql | dot -Tsvg > example.svg

or indirectly through mysqldump:

    python create.py --password=YOUR_PASSWORD -d YOUR_DATABASE | dot -Tpng > output.png

## Example
![SVG](https://raw.githubusercontent.com/confodere/db_map/main/examples/cinema.svg)

## Credits
Extended from [https://github.com/rm-hull/sql_graphviz](github.com/rm-hull/sql_graphviz).