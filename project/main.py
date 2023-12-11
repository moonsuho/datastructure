import heapq
import math

# 미술관 1층 위치의 좌표
locations_f1 = {
    '열린마당': (2, -2.5),
    '미술관마당': (0, 4),
    '두레': (-6.5, 0.5),
    '아트존1': (6, -2.5),
    '아트존2': (16, -2.5),
    '로비': (6.5, 7),
    '카페': (0, 10.5),
    '1전시실': (15.5, 11.5),
    '서울박스': (5.5, 17)
}



# 미술관 지하1층 및 계단의 위치 정보
locations_b1 = {
    '2전시실': (15, 11),
    '3전시실': (10, 20),
    '4전시실': (3.5, 18.5),
    '5전시실': (-4, 13.5),
    '6전시실': (-4, 7),
    '7전시실': (-11.5, -1),
    '미디어랩': (-16, -1),
    '영상관': (-17, 7),
    '다윈공간': (-12.5, 16),
    '전시마당': (-11.5, 6),
    'stair1': (7, 15),
    'stair2': (19, 20),
    'stair3': (4.5, 8),
    'stair4': (-11.5, 9.5),
    'stair5': (-15, 4),
    'stair6': (-18, 2),
}

# 미술관 2층 및 계단의 위치 정보
locations_f2 = {
    '8전시실': (9, 5),
    '종친부': (-1, 19.5),
    '디지털도서관': (-9, 17.5),
    '라운지': (-6, 12),
    '티하우스': (-13, 12),
    '교육동로비': (-14, 2.5),
    '1작업실': (-6, 0),
    '1강의실': (-13.5, 7),
    '2강의실': (-14.5, -2.5),
    '3강의실': (-11.5, -2.5),
    'stair2': (8, 8.5),
    'stair3': (8, 1),
    'stair4': (-8, 14.5),
    'stair5': (-15.5, 13),
    'stair6': (-10, 2.5),
}


# 입출구의 위치
exit_location = (0, 0)

# 다익스트라 알고리즘을 이용하여 최단거리 계산
def dijkstra(graph, start, end):
    heap = [(0, start)]
    visited = set()

    while heap:
        (cost, current) = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)

        if current == end:
            return cost

        for neighbor in graph[current]:
            heapq.heappush(heap, (cost + graph[current][neighbor], neighbor))

    return float('inf')

# 지하 1층 그래프 생성
graph_b1 = {location: {} for location in locations_b1}
for location in locations_b1:
    for neighbor in locations_b1:
        if location != neighbor:
            distance = ((locations_b1[location][0] - locations_b1[neighbor][0]) ** 2 +
                        (locations_b1[location][1] - locations_b1[neighbor][1]) ** 2) ** 0.5
            graph_b1[location][neighbor] = distance

# 2층 그래프 생성
graph_f2 = {location: {} for location in locations_f2}
for location in locations_f2:
    for neighbor in locations_f2:
        if location != neighbor:
            distance = ((locations_f2[location][0] - locations_f2[neighbor][0]) ** 2 +
                        (locations_f2[location][1] - locations_f2[neighbor][1]) ** 2) ** 0.5
            graph_f2[location][neighbor] = distance

# 사용자 위치 입력
user_floor= input("사용자는 몇층입니까: ")


if user_floor=="1":
    input_location = input("사용자의 위치를 입력해주세요(ex.열린마당): ")
    # 최단 거리 계산 함수
    def calculate_distance(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance


    # 입구(0,0)까지의 최단 거리 계산 함수
    def find_shortest_distance(location):
        entrance = (0, 0)
        if location in locations_f1:
            distance = calculate_distance(locations_f1[location], entrance)
            return distance
        else:
            return "해당 위치가 존재하지 않습니다."


    #최단거리 출력
    result = find_shortest_distance(input_location)
    print(f"{input_location}에서 입출구까지의 최단 거리는 {result}입니다.")

elif user_floor=="-1":
    user_location = input("사용자의 위치를 입력해주세요(ex.2전시실):")
    # 최단거리 계산
    min_distance = float('inf')
    chosen_stair = None

    for stair in ['stair1', 'stair2', 'stair3', 'stair4', 'stair5', 'stair6']:
        distance_to_stair = dijkstra(graph_b1, user_location, stair)
        distance_from_stair_to_exit = ((locations_b1[stair][0] - exit_location[0]) ** 2 +
                                       (locations_b1[stair][1] - exit_location[1]) ** 2) ** 0.5
        total_distance = distance_to_stair + distance_from_stair_to_exit

        if total_distance < min_distance:
            min_distance = total_distance
            chosen_stair = stair

    # 결과 출력
    print(f"1층의 입출구까지 최단거리: {min_distance}")
    print(f"{chosen_stair} 계단을 이용해주십시오.")

elif user_floor=="2":
    user_location = input("사용자의 위치를 입력해주세요(ex.1강의실): ")
    # 최단거리 계산
    min_distance = float('inf')
    chosen_stair = None

    for stair in ['stair2', 'stair3', 'stair4', 'stair5', 'stair6']:
        distance_to_stair = dijkstra(graph_f2, user_location, stair)
        distance_from_stair_to_exit = ((locations_f2[stair][0] - exit_location[0]) ** 2 +
                                       (locations_f2[stair][1] - exit_location[1]) ** 2) ** 0.5
        total_distance = distance_to_stair + distance_from_stair_to_exit

        if total_distance < min_distance:
            min_distance = total_distance
            chosen_stair = stair

    # 결과 출력
    print(f"1층의 입출구까지 최단거리: {min_distance}")
    print(f"{chosen_stair} 계단을 이용해주십시오.")



if user_floor=="-1" or user_floor=="2":
    #유저 위치와 계단 위치의 상대적인 위치 판단
    user_x, user_y = locations_b1[user_location] if user_floor == "-1" else locations_f2[user_location]
    stair_x, stair_y = locations_b1[chosen_stair]
    # 계단의 상대적 위치 판단 출력
    if user_x > stair_x:
        if user_y > stair_y:
            print(f"{chosen_stair}은(는) {user_location}의 남서쪽에 위치해있습니다.")
        elif user_y < stair_y:
            print(f"{chosen_stair}은(는) {user_location}의 북서쪽에 위치해있습니다.")
        else:
            print(f"{chosen_stair}은(는) {user_location}의 서쪽에 위치해있습니다.")
    elif user_x < stair_x:
        if user_y > stair_y:
            print(f"{chosen_stair}은(는) {user_location}의 남동쪽에 위치해있습니다.")
        elif user_y < stair_y:
            print(f"{chosen_stair}은(는) {user_location}의 북동쪽에 위치해있습니다.")
        else:
            print(f"{chosen_stair}은(는) {user_location}의 동쪽에 위치해있습니다.")
    else:
        if user_y > stair_y:
            print(f"{chosen_stair}은(는) {user_location}의 남쪽에 위치해있습니다.")
        else:
            print(f"{chosen_stair}은(는) {user_location}의 북쪽에 위치해있습니다.")

elif user_floor=="1":
    user_x, user_y = locations_f1[input_location]
    #출구는 (0,0)에 위치
    if user_x > 0:
        if user_y > 0:
            print(f"입출구는 {input_location}의 남서쪽에 위치해있습니다.")
        elif user_y < 0:
            print(f"입출구는 {input_location}의 북서쪽에 위치해있습니다.")
        else:
            print(f"입출구는 {input_location}의 서쪽에 위치해있습니다.")
    elif user_x < 0:
        if user_y > 0:
            print(f"입출구는 {input_location}의 남동쪽에 위치해있습니다.")
        elif user_y < 0:
            print(f"입출구는 {input_location}의 북동쪽에 위치해있습니다.")
        else:
            print(f"입출구는 {input_location}의 동쪽에 위치해있습니다.")
    else:
        if user_y > 0:
            print(f"입출구는 {input_location}의 남쪽에 위치해있습니다.")
        else:
            print(f"입출구는 {input_location}의 북쪽에 위치해있습니다.")

