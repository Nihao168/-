def process_string(input_str, k):
    output_str = ""
    char_index_map = {}  # 使用map来存储读取过的字符，key为该字符，value为最新的索引下标

    for i, char in enumerate(input_str):
        if char in char_index_map and i - char_index_map[char] <= k:   # 若出现过，且距离当前下标不超过k的距离，换为‘-’
            output_str += "-"
        else:   # 否则，原样加入待输出string
            output_str += char

        char_index_map[char] = i  # 每一次读到的字符都要更新map

    return output_str


# 测试示例
input_str1 = "abcdefaxc"
k1 = 10
output_str1 = process_string(input_str1, k1)
print("Input:", input_str1, k1)
print("Output:", output_str1)

input_str2 = "abcdefaxcqwertba"
k2 = 10
output_str2 = process_string(input_str2, k2)
print("Input:", input_str2, k2)
print("Output:", output_str2)

input_str3 = "abcabcdabcdeabcdef"
k3 = 4
output_str3 = process_string(input_str3, k3)
print("Input:", input_str3, k3)
print("Output:", output_str3)