def calculate_mac(pattern, filter_data):
    score = 0.0

    for row in range(len(pattern)):
        for column in range(len(pattern[row])):
            score += pattern[row][column] * filter_data[row][column]

    return score

def main():
    cross_pattern = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    cross_filter = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    x_filter = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]

    cross_score = calculate_mac(cross_pattern, cross_filter)
    x_score = calculate_mac(cross_pattern, x_filter)

    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {x_score}")

if __name__ == "__main__":
    main()