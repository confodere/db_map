from subprocess import Popen, PIPE
import getopt
import sys
import pyparsing as pp
import collections


def getDump(dbName="mydb", password=None):
    dump = Popen(
        ["mysqldump", dbName, "--compact", "--no-data", f"--password={password}"], stdout=PIPE, stdin=PIPE, stderr=PIPE
    )
    return dump.communicate()[0].decode()


def actPrimaryKey(s, loc, tok):
    return [word.replace("`", "") for word in tok["param"][1:-1].split(",")]


def actField(s, loc, tok):
    fieldName = tok[0].replace('"', "")
    return fieldName.replace("`", "")


def actConstraint(s, loc, tok):
    return (tok["pseudoName"], tok["fkTable"])


def actTable(s, loc, tok):
    tableName = tok["tableName"].replace("`", "")

    ## Fields
    fieldList = []
    fieldNamesList = []
    for tokField in tok["fields"]:
        field = tokField.replace("`", "")
        if field != "":
            fieldName = f'"{tableName}.{field}"'
            if "PK" in tok and field in list(tok["PK"]):
                label = f"<<u>{field}</u>>"
            else:
                label = field
            fieldList.append(f"{{node[label={label}] {fieldName}}};")
            fieldNamesList.append(fieldName)
    fieldStr = " ".join(fieldList)
    fieldNameStr = "; ".join(fieldNamesList)

    ## Constraints
    if "constraints" in tok:
        constraintList = [""]
        nodeList = ['\n\t{node [shape=diamond, style=filled, color="chartreuse2", fillcolor="#E4FCCC"];\n\t\t']
        for constraint in tok["constraints"]:
            constraintName = constraint[0].replace("`", "")
            otherTableName = constraint[1].replace("`", "")
            constraintNode = f'{{node[label="Knows"] {constraintName}}}; '
            rel = f"{tableName} -> {constraintName};"
            rel2 = f'{{edge [arrowhead="none"]; {otherTableName} -> {constraintName}; }};'
            nodeList.append(constraintNode)
            constraintList.append(rel)
            constraintList.append(rel2)
        nodeList.append("\n\t};")
        constraint = "".join(nodeList) + "\n\t".join(constraintList)
    else:
        constraint = ""

    # tbl = f'\t{{node [shape=box, fontsize=24, height=1, width=1.5, style=filled, color="orange", fillcolor="#FFE6CC"]; {tableName};}};'
    tbl = tableName
    fieldRel = f"\t{tableName} -> {{ {fieldNameStr} }};\n"
    return {"tbl": tbl, "field": fieldStr, "rel": fieldRel, "con": constraint}


def orgTbl(tbl: list[str]):
    out = collections.deque()
    for item in tbl:
        out.append(item)
    out.appendleft(
        '\t{node [shape=box, fontsize=24, height=1, width=1.5, style=filled, color="orange", fillcolor="#FFE6CC"]'
    )
    out.append("};")

    return "; ".join(out)


def orgField(field: list[str]):
    out = collections.deque()
    for item in field:
        out.append(item)
    out.appendleft('\t{node [shape=ellipse, style=filled, color="mediumpurple1", fillcolor="#EFE6FF"];')
    out.append("};")

    return "\n\t\t".join(out)


def orgRel(rel: list[str]):
    out = collections.deque()
    for item in rel:
        out.append(item)
    out.appendleft('\tedge [arrowhead="none"]\n')

    return "".join(out)


def orgCon(con: list[str]):
    out = collections.deque()
    for item in con:
        out.append(item)

    return "".join(out)


def actCriteria(s, loc, tok):
    listDict = {"tbl": [], "field": [], "rel": [], "con": []}
    for elem in tok:
        if type(elem) == dict:
            for key in elem:
                listDict[key].append(elem[key])

    strList = []
    for key in ["tbl", "con", "field", "rel"]:
        if key == "tbl":
            out = orgTbl(listDict[key])
        elif key == "field":
            out = orgField(listDict[key])
        elif key == "rel":
            out = orgRel(listDict[key])
        elif key == "con":
            out = orgCon(listDict[key])

        strList.append(out)
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

    # invalidLiteral = pp.OneOrMore(pp.Keyword("KEY")) + pp.ZeroOrMore(pp.CharsNotIn("\n"))
    # invalidLiteral.setParseAction(lambda x: "")

    parenthesis = pp.Forward()
    parenthesis <<= "(" + pp.ZeroOrMore(pp.CharsNotIn("()") | parenthesis).setResultsName("paramContains") + ")"
    parenthesis.setParseAction(lambda x, y, z: "".join(z).replace("\n", "\\n"))

    qouted_string = "'" + pp.OneOrMore(pp.CharsNotIn("'")) + "'"
    qouted_string.setParseAction(lambda x, y, z: "".join(z).replace("\n", "\\n"))

    qouted_default_value = pp.CaselessLiteral("DEFAULT") + qouted_string + pp.OneOrMore(pp.CharsNotIn(", \n\t"))
    qouted_default_value.setParseAction(lambda x, y, z: z[0] + " " + "".join(z[1::]))

    keys = list(map(pp.CaselessKeyword, "NOT NULL COLLATE DEFAULT utf8mb4_unicode_ci".split()))
    types = list(map(pp.CaselessKeyword, "VARCHAR INT ENUM DATE".split()))
    field = (
        ~pp.CaselessKeyword("PRIMARY")
        + pp.Word(pp.alphanums + "`._@$")
        + pp.ZeroOrMore(pp.Or(keys) | pp.Or(types) | parenthesis)
        + pp.Optional(pp.Char(","))
    ).setResultsName("fieldtre")

    field.setParseAction(actField)

    key = pp.CaselessKeyword("KEY") + pp.Word(pp.alphanums + "`._") + parenthesis + pp.Optional(",")
    primaryKey = (
        pp.CaselessKeyword("PRIMARY")
        + pp.CaselessKeyword("KEY")
        + parenthesis.setResultsName("param")
        + pp.Optional(",")
    )
    primaryKey.setParseAction(actPrimaryKey)

    tableName = pp.Word(pp.alphanums + "`_.") | pp.QuotedString('"')
    table = (
        pp.CaselessLiteral("CREATE")
        + pp.CaselessLiteral("TABLE")
        + tableName.setResultsName("tableName")
        + "("
        + pp.ZeroOrMore(field).setResultsName("fields")
        + pp.ZeroOrMore(qouted_default_value | parenthesis)
        + pp.ZeroOrMore(primaryKey).setResultsName("PK")
        + pp.ZeroOrMore(key)
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
        """digraph ER {
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
