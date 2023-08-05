import re

reparam = re.compile(r"(?<=:param).*?(?=:)")
reraises = re.compile(r"(?<=:raises).*?(?=:)")
rereturns = re.compile(r"(?<=:returns).*?(?=:)")


def editdocstr(docstr, offset):
    description = []
    params = []
    paramsd = []
    raises = []
    raisesd = []
    returns = []
    returnsd = []

    lines = docstr.splitlines()
    for line in lines:
        m_param = reparam.search(line)
        m_raises = reraises.search(line)
        m_returns = rereturns.search(line)

        if m_param:
            begin, end = m_param.span()
            txt = line[end + 1:]
            paramsd.append(txt.strip())
            params.append(m_param.group().strip())
            continue
        if m_returns:
            begin, end = m_returns.span()
            txt = line[end + 1:]
            returnsd.append(txt.strip())
            returns.append(m_returns.group().strip())
            continue
        if m_raises:
            begin, end = m_raises.span()
            txt = line[end + 1:]
            raisesd.append(txt.strip())
            raises.append(m_raises.group().strip())
            continue
        description.append(line.strip())

    result = "\n"

    for line in description:
        result += " " * offset + line + "\n"

    if len(params) > 0:
        result += " " * offset + "Args:" + "\n"
        for i in range(len(params)):
            if params[i] != "":
                result += " " * (offset + 4) + params[i] + ": " + paramsd[i] + "\n"
            else:
                result += " " * (offset + 4) + paramsd[i] + "\n"
        result += "\n"

    if len(returns) > 0:
        result += " " * offset + "Returns:" + "\n"
        for i in range(len(returns)):
            if returns[i] != "":
                result += " " * (offset + 4) + returns[i] + ": " + returnsd[i] + "\n"
            else:
                result += " " * (offset + 4) + returnsd[i] + "\n"
        result += "\n"

    if len(raises) > 0:
        result += " " * offset + "Raises:" + "\n"
        for i in range(len(raises)):
            if raises[i] != "":
                result += " " * (offset + 4) + raises[i] + ": " + raisesd[i] + "\n"
            else:
                result += " " * (offset + 4) + raisesd[i] + "\n"
        result += "\n"
    result += " " * offset

    return result


def parse_file_contets(content: str) -> str:
    result = ""
    indoc = False
    atmcounter = 0
    docstr = ""
    current_offset = 0
    offset = 0
    for c in content:
        if c == "\n":
            current_offset = 0
        else:
            current_offset += 1

        if c == "\"":
            atmcounter += 1
        else:
            if atmcounter:
                atmcounter = 0

        if not indoc:
            result += c
        else:
            docstr += c

        if atmcounter == 3:
            atmcounter = 0
            if indoc:
                docstr = docstr[:-3]
                result += editdocstr(docstr, offset)
                result += "\"\"\""
                docstr = ""
            else:
                offset = current_offset - 3
            indoc = not indoc

    return result
