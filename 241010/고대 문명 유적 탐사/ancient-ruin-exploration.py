from collections import deque

# 90도 회전
def rotate(arr, si, sj):
    narr = [x[:] for x in arr]

    narr[si][sj:sj+3] = [arr[si+2][sj], arr[si+1][sj], arr[si][sj]]
    narr[si+1][sj:sj+3] = [arr[si+2][sj+1], arr[si+1][sj+1], arr[si][sj+1]]
    narr[si+2][sj:sj+3] = [arr[si+2][sj+2], arr[si+1][sj+2], arr[si][sj+2]]

    return narr

# 유물 개수 세기 후 flag에 때라 remove 판단
def count_clear(arr, flag):
    v = [[0]*5 for _ in range(5)]
    cnt = 0
    for i in range(5):
        for j in range(5):
            if v[i][j] == 0:
                t = bfs(arr, v, i, j, flag) # 유물개수 return
                cnt += t
    return cnt

def bfs(arr, v, si, sj, flag):
    q = deque()
    # 방문한 좌표
    sset = set()
    # 유물 개수 세는 변수
    cnt = 0

    q.append((si, sj))
    v[si][sj] = 1
    sset.add((si, sj))
    cnt += 1

    while q:
        ci, cj = q.popleft()
        # 4방향, 미방문, 같은 값
        for di, dj in ((-1,0), (0,1), (1,0), (0,-1)):
            ni, nj = ci+di, cj+dj
            if 0<=ni<5 and 0<=nj<5 and v[ni][nj]==0 and arr[ci][cj]==arr[ni][nj]:
                q.append((ni, nj))
                v[ni][nj] = 1
                sset.add((ni, nj))
                cnt += 1

    if cnt >= 3: # 유물 3개 이상이면 개수 리턴, flag 1이면 remove까지
        if flag == 1: # 해당위치 0으로 해주고 개수 리턴
            for fi, fj in sset:
                arr[fi][fj] = 0
        return cnt

    else: # 3개 미만인 경우 0 return
        return 0



# k: 탐사 반복 횟수, m: 벽면에 적힌 유물 개수
k, m = map(int, input().split())
# 5x5 배열 정보
arr = [list(map(int, input().split())) for _ in range(5)]
# 유물 리스트 m개
lst = list(map(int, input().split()))

# 최종 정답
ans = []

# 탐사 반복 횟수
for kk in range(k):
    # 최댓값은 탐사 1회차마다 갱신됨
    mx_cnt = 0
    # 회전수 -> 열 -> 행
    for rot in range(1,4): # 회전수(작은게 우선) 한번회전->두번회전->세번회전
        for j in range(3): # 열 작은게 우선
            for i in range(3): # 행 작은게 우선
                # 회전할때마다 원본 맵 가져와야하므로
                narr = [x[:] for x in arr]
                # 복사한거 가져와서 회전 -> bfs 개수 세기 -> max값보다 개수가 크다면 갱신
                # 복사한거 가져와서 회전
                for _ in range(rot):
                    narr = rotate(narr, i, j)
                # bfs 개수 세기
                t = count_clear(narr, 0) # bfs 함수(3개조건 넣어줘야함), flag:0 지우기 x
                # max값보다 개수가 크다면 갱신 & 그때의 맵 기억해두기(나중에 해당 위치 지우기 위해)
                if mx_cnt < t:
                    mx_cnt = t
                    marr = narr

    # 만약 유물이 없다면
    if mx_cnt == 0:
        break

    # 유물의 개수가 3보다 크다면 유물위치 사라지고 유물 만들어지지 않을 때까지 새로운 유물 넣는것 무한반복
    cnt = 0
    arr = marr
    while True:
        t = count_clear(arr, 1) # bfs + remove (3개 조건 넣어줘야함), flag:1 지우기 o
        # 연쇄적으로 삭제했다가 더이상 안만들어질경우
        # 무한루프 나오고 그다음 턴으로 이동
        if t == 0:
            break
        cnt += t
        # lst숫자 하나씩 넣기
        for j in range(5): # 열번호 작은순으로
            for i in range(4, -1, -1): # 행번호 큰 순으로(내림차순)
                if arr[i][j] == 0:
                    arr[i][j] = lst.pop(0)
    # 이번 턴에서 얻은 갯수 넣기
    ans.append(cnt)

print(*ans)