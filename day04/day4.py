# Day 4: Secure Container
# No ranks this time


def main():
    passwords = set()
    passwords2 = set()

    for num in range(156218, 652527):
        password = str(num)

        # check for ascending
        ascending = True
        for j in range(5):
            if int(password[j]) > int(password[j + 1]):
                ascending = False
                break
        if not ascending:
            continue

        # Check for adjacent pairs
        adjacent, isolated = False, False
        for j in range(10):
            if str(j) * 2 in password:
                adjacent = True
                if str(j) * 3 not in password:
                    isolated = True

        # add to valid passwords
        if adjacent:
            passwords.add(num)
            if isolated:
                passwords2.add(num)

    print('Part 1:', len(passwords))
    print('Part 2:', len(passwords2))


if __name__ == '__main__':
    main()
