def count_candidates(min_val, max_val):
    count = 0
    for num in range(min_val, max_val + 1):
        digits = [int(c) for c in str(num)]
        double = False
        increasing = True
        for i in range(len(digits) - 1):
            if digits[i] > digits[i + 1]:
                increasing = False
                break
            if (
                digits[i] == digits[i + 1] 
                and (i == 0 or digits[i - 1] != digits[i]) 
                and (i == len(digits) - 2 or digits[i + 2] != digits[i + 1])
            ):
                double = True
        if double and increasing:
            count += 1
    return count

if __name__ == "__main__":
    print(count_candidates(234208, 765869))
