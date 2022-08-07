def parse(xml):
    if type(xml) == list:
        for i in range(len(xml)):
            xml[i] = parse(xml[i])
        return xml
    openTag = False # Currently reading a tag
    inTag = False # Currently in a tag
    isClosingTag = False # Is closing tag. Extremely helpful comment.
    newTag = ""
    tag = ""
    tagUnModified = ""
    index = 0
    dataInTag = ""
    data = {}
    if "<" not in xml:
        return xml
    for character in xml:
        try:
            prevCharacter = xml[index-1]
        except:
            prevCharacter = ""
        try:
            nextCharacter = xml[index+1]
        except:
            nextCharacter = ""
        if character == "<" and nextCharacter != "?":
            inTag = True
            openTag = True
            if nextCharacter == "/":
                isClosingTag = True
            else:
                isClosingTag = False

        if openTag:

            newTag += character

        if inTag:
            dataInTag += character
        if character == ">":

            if tag == "":
                # Code to handle self closing tags

               
                if len(newTag) > 0 and newTag[-2] == "/":

                    dataInTag = dataInTag.replace(newTag, "")
                    inTag = False

                else:
                    tagUnModified = newTag
                    if " " in newTag:
                        split = newTag.split(" ")
                        newTag = split[0] + ">"

                    tag = newTag



                
            if isClosingTag:
                if newTag[0] + newTag[2:] == tag:
                    inTag = False
                    if tag[1:-1] in data:
                        if type(data[tag[1:-1]]) != list:
                            original = data[tag[1:-1]]
                            data[tag[1:-1]] = list([original, dataInTag[len(tagUnModified):-len(newTag)]])
                        else:
                            data[tag[1:-1]].append(dataInTag[len(tagUnModified):-len(newTag)])
                    else:
                        data[tag[1:-1]] = dataInTag[len(tagUnModified):-len(newTag)]
                    dataInTag = ""
                    tag = ""
            newTag = ""
            openTag = False
        index += 1
    for i in data:
        data[i] = parse(data[i])
    return data
