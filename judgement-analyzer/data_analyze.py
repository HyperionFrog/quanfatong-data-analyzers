def count_lines_with_keywords(filename, keyword1, keyword2):
    count, count_sum = 0, 0
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            count_sum += 1
            if keyword1 in line and keyword2 in line:
                count += 1
    return count, count_sum


if __name__ == "__main__":
    filename = "output.txt"  # 请将此处替换为你的文件名
    keyword1 = "判决书"
    keyword2 = "判决书"
    result, sum = count_lines_with_keywords(filename, keyword1, keyword2)
    print(f"包含 '{keyword1}' 和 '{keyword2}' 的行数为: {result}")
    print("总行数为", sum)