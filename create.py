from subprocess import Popen, PIPE
import getopt
import sys
import pyparsing as pp


def getDump(dbName="mydb", password=None):
    dump = Popen(
        ["mysqldump", dbName, "--compact", "--no-data", f"--password={password}"], stdout=PIPE, stdin=PIPE, stderr=PIPE
    )
    return dump.communicate()[0].decode()


def actField(s, loc, tok):
    fieldName = tok[0].replace('"', "")
    return fieldName.replace("`", "")


def actConstraint(s, loc, tok):
    return (tok["pseudoName"], tok["fkTable"])


def actTable(s, loc, tok):
    tableName = tok["tableName"].replace("`", "")

    ## Fields
    fieldList = ['\t{node [shape=ellipse, style=filled, color="mediumpurple1", fillcolor="#EFE6FF"];']
    fieldNamesList = []
    for tokField in tok["fields"]:
        field = tokField.replace("`", "")
        if field != "":
            fieldName = f'"{tableName}.{field}"'
            fieldList.append(f'{{node[label="{field}"] {fieldName}}};')
            fieldNamesList.append(fieldName)
    fieldList.append("}; ")
    fieldStr = " ".join(fieldList)
    fieldNameStr = "; ".join(fieldNamesList)

    ## Constraints
    if "constraints" in tok:
        constraintList = []
        for constraint in tok["constraints"]:
            constraintName = constraint[0].replace("`", "")
            otherTableName = constraint[1].replace("`", "")
            constraintNode = f'\t{{node [shape=diamond,style=filled,color="chartreuse2", fillcolor="#E4FCCC"]; {{node[label="Knows"] {constraintName}}}; }};'
            rel = f"{tableName} -- {constraintName};"
            rel2 = f"{otherTableName} -- {constraintName};"
            constraintList.append(constraintNode + "\n\t\t" + rel + "\n\t\t" + rel2)
        constraint = "\n\t\t".join(constraintList)
    else:
        constraint = ""

    tbl = f'\t{{node [shape=box, fontsize=24, height=1, width=1.5, style=filled, color="orange", fillcolor="#FFE6CC"]; {tableName};}};'
    fieldRel = f"\t{tableName} -- {{ {fieldNameStr} }};"
    return {"tbl": tbl, "field": fieldStr, "rel": fieldRel, "con": constraint}


def actCriteria(s, loc, tok):
    listDict = {"tbl": [], "field": [], "rel": [], "con": []}
    for elem in tok:
        if type(elem) == dict:
            for key in elem:
                listDict[key].append(elem[key])

    strList = []
    for key in ["tbl", "con", "field", "rel"]:
        for item in listDict[key]:
            strList.append(item)
        strList.append("\n")
    return strList


class parse:
    comment = pp.nestedExpr("/*", "*/;")
    comment.setParseAction(lambda x: "")
    other = pp.OneOrMore(pp.CharsNotIn(";")) + ";"
    other.setParseAction(lambda x: "")

    fkey_cols = pp.Word(pp.alphanums + "_`.") + pp.ZeroOrMore(pp.Suppress(",") + pp.Word(pp.alphanums + "_`."))
    constraint = (
        pp.CaselessLiteral("CONSTRAINT")
        + pp.Word(pp.alphanums + "_`.").setResultsName("pseudoName")
        + pp.CaselessLiteral("FOREIGN")
        + pp.CaselessLiteral("KEY")
        + "("
        + fkey_cols.setResultsName("keyName")
        + ")"
        + "REFERENCES"
        + pp.Word(pp.alphanums + "_`.").setResultsName("fkTable")
        + "("
        + fkey_cols.setResultsName("fkCol")
        + ")"
    )
    constraint.setParseAction(actConstraint)
    constraintList = constraint + pp.ZeroOrMore(pp.Suppress(",") + constraint)

    invalidLiteral = pp.OneOrMore(pp.CaselessLiteral("PRIMARY") | pp.CaselessLiteral("KEY")) + pp.ZeroOrMore(
        pp.CharsNotIn("\n")
    )
    invalidLiteral.setParseAction(lambda x: "")

    parenthesis = pp.Forward()
    parenthesis <<= "(" + pp.ZeroOrMore(pp.CharsNotIn("()") | parenthesis) + ")"
    parenthesis.setParseAction(lambda x, y, z: "".join(z).replace("\n", "\\n"))

    qouted_string = "'" + pp.OneOrMore(pp.CharsNotIn("'")) + "'"
    qouted_string.setParseAction(lambda x, y, z: "".join(z).replace("\n", "\\n"))

    qouted_default_value = pp.CaselessLiteral("DEFAULT") + qouted_string + pp.OneOrMore(pp.CharsNotIn(", \n\t"))
    qouted_default_value.setParseAction(lambda x, y, z: z[0] + " " + "".join(z[1::]))

    field = ~constraint + pp.OneOrMore(
        invalidLiteral
        | qouted_default_value
        | ~pp.CaselessLiteral("CONSTRAINT") + pp.Word(pp.alphanums + "_\"'`:-/[].")
        | parenthesis
    )
    field.setParseAction(actField)
    fieldList = field + pp.ZeroOrMore(pp.Suppress(",") + field)

    tableName = pp.Word(pp.alphanums + "`_.") | pp.QuotedString('"')
    table = (
        pp.CaselessLiteral("CREATE")
        + pp.CaselessLiteral("TABLE")
        + tableName.setResultsName("tableName")
        + "("
        + fieldList.setResultsName("fields")
        + pp.Optional(constraintList.setResultsName("constraints"))
        + ")"
        + pp.ZeroOrMore(pp.CharsNotIn(";\n"))
        + ";"
    ).setResultsName("tbl")
    table.setParseAction(actTable)

    def __init__(self, text):
        self.text = text

    def process(self):
        criteria = pp.OneOrMore(self.comment | self.table | self.other)
        criteria.setParseAction(actCriteria)
        return criteria.parseString(self.text)


def printDot(result):
    print(
        """graph ER {
    graph [ rankdir = "LR" ];
    layout=neato;
    overlap=scale;
    splines=true;
    pad="0.25,0.25";
"""
    )
    for line in result:
        if line != "":
            print(line)
    print("}")


def main(argv):
    file = None
    databaseName = "mydb"
    sqlPassword = None

    helpText = "main.py --file=<fileName> OR --password=<password> --database=<databaseName>"
    try:
        opts, args = getopt.getopt(argv, "pd:0", ["file=", "password=", "database="])
    except getopt.GetoptError:
        print(helpText)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(helpText)
            sys.exit()
        elif opt in ("-f", "--file"):
            with open(arg) as f:
                file = f.read()
        elif opt in ("-d", "--database"):
            databaseName = arg
        elif opt in ("-p", "--password"):
            sqlPassword = arg

    if file is None:
        dump = getDump(dbName=databaseName, password=sqlPassword)
    else:
        dump = file
    p = parse(dump)
    result = p.process()
    printDot(result)


if __name__ == "__main__":
    main(sys.argv[1:])
