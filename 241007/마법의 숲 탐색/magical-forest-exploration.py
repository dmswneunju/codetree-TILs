from collections import deque

r, c, k = map(int, input().split())
# 골렘 위치 정보
# cj(열 번호) dr(출구 방향)
unit = [list(map(int, input().split())) for _ in range(k)]
# 초기맵
arr = [[1]+[0]*c+[1] for _ in range(r+3)] + [[1] * (c+2)]
# 출구 정보
exit_set = set()

# 0:북, 1:동, 2:남, 3:서 (시계방향)
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def bfs(si, sj):
    q = deque()
    visited = [[0]*(c+2) for _ in range(r+4)]
    max_i = 0 # -2해서 return!!
    # 큐에 삽입
    q.append((si, sj))
    visited[si][sj] = 1
    # 큐에 데이터가 있는 동안
    while q:
        ci, cj = q.popleft()
        max_i = max(max_i, ci)

        # 네방향, 미방문, 조건(같은 값 또는 내가 출구 - 상대방이 골렘)
        for di, dj in ((-1,0), (0,1), (1,0), (0,-1)):
            ni, nj = ci+di, cj+dj
            #  미방문                   같은 골렘 내에서는 이동 가능         현재좌표가 출구에 포함         이동할 위치가 골렘이면
            if visited[ni][nj]==0 and (arr[ci][cj]==arr[ni][nj] or ((ci,cj) in exit_set) and arr[ni][nj]>1) :
                q.append((ni,nj))
                visited[ni][nj] = 1

    return max_i-2

# 최종 답
ans = 0
# 골렘 번호(1: 외곽)
num = 2
# 골렘 입력 좌표/방향에 따라서 남쪽이동 및 정령 최대좌표 계산해서 누적
for cj, dr in unit:
    ci = 1
    # [1] 남쪽으로 최대한 이동(남->서->동)
    while True:
        # 남쪽이동
        if arr[ci+1][cj-1]+arr[ci+2][cj]+arr[ci+1][cj+1] == 0:
            ci += 1
        # 서쪽이동
        elif arr[ci-1][cj-1]+arr[ci][cj-2]+arr[ci+1][cj-2]+arr[ci+1][cj-1]+arr[ci+2][cj-1] == 0:
            ci += 1
            cj -= 1
            dr = (dr-1)%4
        # 동쪽이동
        elif arr[ci-1][cj+1]+arr[ci][cj+2]+arr[ci+1][cj+2]+arr[ci+1][cj+1]+arr[ci+2][cj+1] == 0:
            ci += 1
            cj += 1
            dr = (dr+1) % 4
        else: # 최대한 남쪽으로 이동 or 기존에 있던 골렘만나서 더이상 움직임 불가
            break

    if ci < 4: # 몸이 범위 밖(새롭게 탐색 시작. arr 등 모두 초기화)
        arr = [[1]+[0]*c+[1] for _ in range(r+3)] + [[1] * (c+2)]
        exit_set = set()
        num = 2
    else: # [2] 골렘을 표시 + 비상구위치 추가
        # 한칸 아래, 한칸 위
        arr[ci+1][cj] = arr[ci-1][cj] = num
        # 왼쪽, 오른쪽
        arr[ci][cj-1:cj+2] = [num]*3
        num += 1
        # 출구 정보
        exit_set.add((ci+dx[dr], cj+dy[dr]))

        # 남쪽으로 가기 bfs(2를 뺀 return 값!!)
        ans += bfs(ci, cj)

print(ans)