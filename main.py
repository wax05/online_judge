import os
import sys
import subprocess

now_dir = os.getcwd()

exam_name = "시험_테스트"

if not os.path.exists(now_dir+"/"+exam_name):
    try:
        os.makedirs("./"+exam_name)
    except FileExistsError:
        pass

print(now_dir+"/"+exam_name)
exams = os.listdir(now_dir+"/"+exam_name)
exams_dir = now_dir+"/"+exam_name

correct_file = "test.py"

proc = subprocess.Popen(["python",now_dir+"/"+correct_file],stdout=subprocess.PIPE)
while proc.poll() is None:
    pass
out, err = proc.communicate()
if err != None:
    print(err)
    sys.exit(1)
exam_correct = out
result = [["학번","결과"]]

for exam in exams:
    is_exam = False
    number = exam.split(".")[0]
    file_form = exam.split(".")[1]
    if file_form == "py":
        is_exam = True
    if is_exam:
        proc = subprocess.Popen(["python",exams_dir+"/"+str(exam)],stdout=subprocess.PIPE)
        while proc.poll() is None:
            pass
        out, err = proc.communicate()
        if out == exam_correct:
            result.append([str(number),"통과"])
        else:
            result.append([str(number),"실패"])


with open(exam_name+".csv", "w", encoding="utf-8") as file:
    for row in result:
        for index, row_element in enumerate(row):
            if index == 1:
                file.write(row_element)
            else:
                file.write(row_element+",")
        file.write("\n")

print("complete")