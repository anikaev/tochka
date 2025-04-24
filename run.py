import json

def check_capacity(max_capacity: int, guests: list) -> bool:
    inn = sorted(gs['check-in'] for gs in guests)
    out = sorted(gs['check-out'] for gs in guests)

    cur = 0
    i,j = 0,0
    while i < len(guests):
        if inn[i] >= out[j]:
            cur -=1
            j +=1
        cur += 1
        if cur> max_capacity:
            return False
        i += 1

    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)

    result = check_capacity(max_capacity, guests)
    print(result)