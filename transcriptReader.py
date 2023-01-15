import PyPDF2
import os
warnings = []
classes = dict()
semesterGpas = dict()
numSemesterGpas = dict()
numTranscripts = 0
#iterates through all files under data directory
for filename in os.listdir("data"):
    numTranscripts += 1
    pdfFileObj = open("data/" + filename, 'rb')
    
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    # creating a page object
    pageObj = pdfReader.pages[0]
    # extracting text from page
    pageText = pageObj.extract_text()
    name = ""
    pageText = pageText.split("\n")
    #Get name
    for line in pageText:
        if "Name: " in line:
            name = line[6:]
            name = name.split(",")
            name = name[1] + " " + name[0]
            break
    print(name)

    skip = True
    recordClass = False
    semester = ""
    finishedSemester = ""
    #read each page
    for num in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[num]
        # extracting text from page
        pageText = pageObj.extract_text()
        #print(pageText)
        pageText = pageText.split("\n")
        warning = False
        gpa = 0.00
        for line in pageText:
            #Get semester gpa, has to check if semester was completed
            if "Academic Standing Effective" in line:
                if gpa < 2.5:
                    warning = True
                else:
                    warning = False
            #Gets name of each semester
            if  "Fall" in line:
                semester = line[line.find("Fall"):]
            if  "Spring" in line:
                semester = line[line.find("Spring"):]
            if  "Summer" in line:
                semester = line[line.find("Summer"):]
            #Record gpa
            if "UW-Madison Term Summary: " in line:
                gpa = float(line[25:30])
                if semester in semesterGpas:
                    semesterGpas[semester] += gpa
                    numSemesterGpas[semester] += 1
                else:
                    semesterGpas[semester] = gpa
                    numSemesterGpas[semester] = 1
            #ignore certain lines
            if "Session: " in line:
                skip = False
            if skip:
                continue
            #Record class names
            if line == "Course Description Attempted Earned Grade Points":
                recordClass = True
                continue
            if line == "GPA Attempted Earned GPA Units Points":
                recordClass = False
                continue
            if recordClass:
                number = 0
                classCode = ""
                #system to get only class code from line
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
                continue
    if warning == True:
        warnings.append(name)
    # closing the pdf file object
    pdfFileObj.close()
#test.sort(key=lambda x:float(x[-4:]) + .5 * (x[0:6] == "Spring"))
semesters = list(semesterGpas.keys())
#Sorts semester names chronologically
semesters.sort(key=lambda x:float(x[-4:]) + .5 * (x[0:6] == "Spring"))

#writes results to files
fWarning = open("warnings.txt", "w+")
fSemesterGpa = open("semesterGpas.txt", "w+")
fClasses = open("classes.txt" , "w+")
for name in warnings:
    fWarning.write(name + "\n")
for semester in semesters:
    fSemesterGpa.write(semester + " " + "%.3f" % (semesterGpas[semester]/numSemesterGpas[semester]) + "\n")
for classCode in classes:
    students = ""
    for student in classes[classCode]:
        students += student + ", "
    fClasses.write(classCode  + " " + students[0:len(students) - 2] + "\n")