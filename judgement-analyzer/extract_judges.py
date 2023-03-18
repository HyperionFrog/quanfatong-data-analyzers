import os
from multiprocessing import Pool, cpu_count

def filter_lines_with_keywords(input_filename, output_filename, keyword1, keyword2):
    total_lines = 0
    count = 0
    first_line = True
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                total_lines += 1
                if first_line:
                    output_file.write(line)
                    first_line = False
                if keyword1 in line and keyword2 in line:
                    count += 1
                    output_file.write(line)
    return input_filename, total_lines, count

def process_file(args):
    input_file, input_folder, output_folder, keyword1, keyword2 = args
    input_filename = os.path.join(input_folder, input_file)
    output_filename = os.path.join(output_folder, input_file)
    return filter_lines_with_keywords(input_filename, output_filename, keyword1, keyword2)

def process_files(input_folder, output_folder, keyword1, keyword2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    num_processes = cpu_count()

    with Pool(processes=num_processes) as pool:
        results = pool.map(process_file, [(input_file, input_folder, output_folder, keyword1, keyword2) for input_file in input_files])

    for result in results:
        input_file, total_lines, count = result
        print(f"{os.path.basename(input_file)}:")
        print(f"  原文件总行数为: {total_lines}")
        print(f"  包含 '{keyword1}' 和 '{keyword2}' 的行数为: {count}")

if __name__ == "__main__":
    input_folder = "./judge_input"  # 请将此处替换为你的输入文件夹路径
    output_folder = "./judge_output"  # 请将此处替换为你的输出文件夹路径
    keyword1 = '"劳动争议"'
    keyword2 = '判决书""'
    process_files(input_folder, output_folder, keyword1, keyword2)