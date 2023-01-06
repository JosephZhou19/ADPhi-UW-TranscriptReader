import PyPDF2
pdfFileObj = open('data/unofficialTranscriptFall2022.pdf', 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)
# printing number of pages in pdf file
classes = dict()
# creating a page object
pageObj = pdfReader.pages[0]
# extracting text from page
pageText = pageObj.extract_text()
name = ""
pageText = pageText.split("\n")
for line in pageText:
    if "Name: " in line:
        name = line[6:]
print(name)
skip = True
recordClass = False
for num in range(len(pdfReader.pages)):
    pageObj = pdfReader.pages[num]
    # extracting text from page
    pageText = pageObj.extract_text()
    print(pageText)
    pageText = pageText.split("\n")

    for line in pageText:
        if "Session: " in line:
            skip = False
        if skip:
            continue
        if line == "Course Description Attempted Earned Grade Points":
            recordClass = True
            continue
        if line == "GPA Attempted Earned GPA Units Points":
            recordClass = False
        if recordClass:
            number = 0
            classCode = ""
            for char in line:
                classCode += char
                if char.isnumeric():
                    if number == 2:
                        if classCode in classes:
                            if name not in classes[classCode]:
                                classes[classCode].append(name)
                        else:
                            classes[classCode] = [name]
                    number += 1
                elif char != " " and not char.isupper():
                    break
for classCode in classes:
    print(classCode  + " " + str(classes[classCode]))
# closing the pdf file object
pdfFileObj.close()