import json

def calculate_mac(pattern, filter_data):
    score = 0.0

    for row in range(len(pattern)):
        for column in range(len(pattern[row])):
            score += pattern[row][column] * filter_data[row][column]

    return score

def input_matrix(name):
    print(f"\n{name} (3줄 입력, 공백 구분)")

    matrix = []

    while len(matrix) < 3:
        try:
            row = list(map(int, input().split()))

            if len(row) != 3:
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
                continue

            matrix.append(row)

        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요.")

    return matrix

def load_data():
    with open("data.json", "r", encoding="utf-8") as file:
        return json.load(file)

def classify(cross_score, x_score):
    epsilon = 1e-9

    if abs(cross_score - x_score < epsilon):
        return "UNDECIDED"

    if cross_score > x_score:
        return "Cross"

    return "X"

def normalize_label(label):
    if label == "+":
        return "Cross"

    if label == "x":
        return "X"

    return label

def main():
    data = load_data()

    cross_filter = data["filters"]["size_5"]["cross"]
    x_filter = data["filters"]["size_5"]["x"]

    pattern_data = data["patterns"]["size_5_1"]
    pattern = pattern_data["input"]
    expected = pattern_data["expected"]

    cross_score = calculate_mac(pattern, cross_filter)
    x_score = calculate_mac(pattern, x_filter)

    excepted =normalize_label(pattern_data["expected"])

    result = classify(cross_score, x_score)

    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {x_score}")
    print(f"판정: {result}")
    print(f"expected: {expected}")

    if result == excepted:
        print("PASS")
    else:
        print("FAIL")

if __name__ == "__main__":
    main()