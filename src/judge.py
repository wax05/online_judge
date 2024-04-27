import os
import sys
import datetime
import subprocess

now_dir = os.getcwd()
RUNTIME_LIMIT_SECONDS = os.getenv("RUNTIME_LIMIT_SECONDS")


def judge(
    correct_file_path: str,
    judge_file_path: str,
    exam_name: str,
    time_limit: datetime.timedelta = datetime.timedelta(seconds=3),
) -> tuple[dict, list[str]]:
    """
    Python Judge Function\n
    Return index 0 is dictionary\n
    Index 0 dictionary is status of exam\n
    Dictionary structure:\n
    \t"student_id" : str {\n
    \t"correct" : bool\n
    \t"error":str\n}
    Index 1 is csv list\n
    using util/csv/csv_write custom function
    """

    exams_files = os.listdir(judge_file_path)

    proc = subprocess.Popen(
        ["python", correct_file_path],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    while proc.poll() is None:
        pass
    out, err = proc.communicate()
    if err != None:
        print(err)
        raise RuntimeError("Correct Python File have ERROR. Check file")
    exam_correct = out
    csv_result = [["학번", "결과", "에러"]]
    result = {}

    for exam in exams_files:
        is_exam = False
        number = exam.split(".")[0]
        file_form = exam.split(".")[1]

        if file_form == "py":
            is_exam = True

        if is_exam:
            proc = subprocess.Popen(
                ["python", judge_file_path + "/" + str(exam)],
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            before_run_time = datetime.datetime.now(datetime.UTC)
            running_time = None

            while proc.poll() is None:
                running_time = datetime.datetime.now(datetime.UTC) - before_run_time
                if (
                    running_time >= time_limit * 20
                    or running_time
                    >= datetime.timedelta(seconds=int(RUNTIME_LIMIT_SECONDS))
                ):
                    break
                pass

            if running_time >= time_limit:
                result[str(number)] = {"correct": False, "error": "time out"}
                continue
            out, err = proc.communicate()

            if out == exam_correct:
                csv_result.append([str(number), "통과", ""])
                result[str(number)] = {"correct": True}
            else:
                csv_result.append([str(number), "실패"])
                result[str(number)] = {"correct": False}
                if err != None:
                    result[str(number)]["error"] = str(err)
                    csv_result[-1].append(str(err))

    return (result, csv_result)

    # TODO:Export Csv Write Custom Function
    with open(exam_name + ".csv", "w", encoding="utf-8") as file:
        for row in csv_result:
            for index, row_element in enumerate(row):
                if index == 1:
                    file.write(row_element)
                else:
                    file.write(row_element + ",")
            file.write("\n")
