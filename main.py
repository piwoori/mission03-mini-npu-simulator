import json
import time

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

def is_valid_size(matrix, size):
    if len(matrix) != size:
        return False

    for row in matrix:
        if len(row) != size:
            return False
        
    return True

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
    elif label == "x":
        return "X"
    else:
        return label

def measure_performance(pattern, filter_data, repeat=10):
    total_time = 0

    for _ in range(repeat):
        start = time.perf_counter()

        calculate_mac(pattern, filter_data)

        end = time.perf_counter()

        total_time += end - start

    average_seconds = total_time / repeat
    average_ms = average_seconds * 1000

    return average_ms

def run_json_mode():
    total_count = 0
    pass_count = 0
    fail_cases = []

    data = load_data()

    print("\n=== 필터 로드 ===")

    for filter_name in data["filters"]:
        print(f"✓ {filter_name} 필터 로드 완료 (Cross, X)")

    print("\n=== 패턴 분석 ===")

    for pattern_name, pattern_data in data["patterns"].items():
        print(f"\n--- {pattern_name} ---")

        parts = pattern_name.split("_")
        size = int(parts[1])

        filter_key = f"size_{size}"

        cross_filter = data["filters"][filter_key]["cross"]
        x_filter = data["filters"][filter_key]["x"]

        pattern = pattern_data["input"]
        expected = normalize_label(pattern_data["expected"])

        if (
            not is_valid_size(pattern, size)
            or not is_valid_size(cross_filter, size)
            or not is_valid_size(x_filter, size)
        ):
            print("FAIL")
            print("원인: 필터와 패턴의 크기가 일치하지 않습니다.")

            total_count += 1
            fail_cases.append(
                (pattern_name, "필터와 패턴의 크기 불일치")
            )
            continue

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

            if result == "UNDECIDED":
                reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
            else:
                reason = f"판정 결과({result})와 expected({expected}) 불일치"

            fail_cases.append((pattern_name, reason))

    print("\n=== 성능 분석 ===")
    print("크기\t평균 시간(ms)\t연산 횟수")

    pattern_3 = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    filter_3 = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    average_ms = measure_performance(pattern_3, filter_3)
    print(f"3x3\t{average_ms:.6f}\t9")

    for size in [5, 13, 25]:
        filter_key = f"size_{size}"

        cross_filter = data["filters"][filter_key]["cross"]

        pattern_key = f"size_{size}_1"
        pattern = data["patterns"][pattern_key]["input"]

        average_ms = measure_performance(pattern, cross_filter)

        operation_count = size * size

        print(f"{size}x{size}\t{average_ms:.6f}\t{operation_count}")


    fail_count = total_count - pass_count
    
    print("\n=== 결과 요약 ===")
    print(f"총 테스트: {total_count}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {fail_count}개")
    
    if fail_cases:
        print("\n*실패 케이스*")

        for case_name, reason in fail_cases:
            print(f"- {case_name}: {reason}")

def run_user_mode():
    print("\n=== 사용자 입력 모드 ===")

    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")

    print("\n필터가 입력되었습니다.")

    pattern = input_matrix("패턴")

    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)

    if abs(score_a - score_b) < 1e-9:
        result = "판정 불가"
    elif score_a > score_b:
        result = "A"
    else:
        result = "B"

    average_ms = measure_performance(pattern, filter_a)

    print("\n=== MAC 판정 결과 ===")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {average_ms:.6f} ms")
    print(f"판정: {result}")


def main():
    print("=== Mini NPU Simulator ===")
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    choice = input("선택: ")

    if choice == "1":
        run_user_mode()
    elif choice == "2":
        run_json_mode()
    else:
        print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()