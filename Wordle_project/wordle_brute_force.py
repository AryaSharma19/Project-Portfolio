from typing import List


def main() -> None:
    known: str = input("enter known letters: ")
    eliminated: str = input("enter eliminated letters: ")
    print(runner_known_and_unknown(parse_known_letters(known), parse_known_positions(known), parse_eliminated(eliminated)))
    return

def generate_list() -> List[str]:
    path = 'C:\\Users\\arya19\\OneDrive - University of North Carolina at Chapel Hill\\Documents\\AryaS_Coding_Stuff\\wordle_list.txt' # save the file in your own local path
    file = open(path, 'r')
    list: List[str] = []
    line = file.readline()
    while line:
        list.append(line)
        line = file.readline()
    return list

def letter(list: List[str], letter: str, position: int) -> List[str]:
    for i in range(len(list) - 1, -1, -1):
        if list[i][position] != letter:
            list.pop(i)
    return list

def remove(list: List[str], letters: List[str]) -> List[str]:
    for i in range(len(list) - 1, -1, -1):
        for l in letters:
            if l in list[i]:
                list.pop(i)
                break
    return list

def parse_known_letters(string: str) -> List[str]:
    list: List[str] = []
    for i in range(0, 5):
        if string[i] != "0":
            list.append(string[i])
    return list

def parse_known_positions(string: str) -> List[int]:
    list: List[int] = []
    for i in range(0, 5):
        if string[i] != "0":
            list.append(i)
    return list

def parse_eliminated(string: str) -> List[str]:
    list: List[str] = []
    for c in string:
        list.append(c)
    return list

def runner_known_and_unknown(letters: List[str], positions: List[int], errors: List[str]) -> List[str]:
    nums_known: int = len(letters)
    list: List[str] = generate_list()
    i: int = 0
    while i < nums_known:
        list = letter(list, letters[i], positions[i])
        i += 1
    remove(list, errors)
    return list

if __name__ == "__main__":
    main()