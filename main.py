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

    if abs(cross_score - x_score) < epsilon:
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
    total_count = 0
    pass_count = 0
    fail_cases = []

    data = load_data()

    for pattern_name, pattern_data in data["patterns"].items():
        print(f"\n--- {pattern_name} ---")

        parts = pattern_name.split("_")
        size = parts[1]

        filter_key = f"size_{size}"

        cross_filter = data["filters"][filter_key]["cross"]
        x_filter = data["filters"][filter_key]["x"]

        pattern = pattern_data["input"]
        expected = normalize_label(pattern_data["expected"])

        cross_score = calculate_mac(pattern, cross_filter)
        x_score = calculate_mac(pattern, x_filter)

        result = classify(cross_score, x_score)

        print(f"Cross 점수: {cross_score}")
        print(f"X 점수: {x_score}")
        print(f"판정: {result}")
        print(f"expected: {expected}")

        total_count += 1

        if result == expected:
            print("PASS")
            pass_count += 1
        else:
            print("FAIL")
            fail_cases.append(pattern_name)

    fail_count = total_count - pass_count

    print("\n=== 결과 요약 ===")
    print(f"총 테스트: {total_count}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {fail_count}개")

    if fail_cases:
        print("실패 케이스")
        for c in fail_cases:
            print(f"- {c}")

if __name__ == "__main__":
    main()