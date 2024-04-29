

def write_csv(csv_file_name:str, data:list):
    with open(csv_file_name + ".csv", "w", encoding="utf-8") as file:
        for row in data:
            for index, row_element in enumerate(row):
                if index == 1:
                    file.write(row_element)
                else:
                    file.write(row_element + ",")
            file.write("\n")
