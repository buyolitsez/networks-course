import matplotlib.pyplot as plt
import numpy as np

# Параметры
F = 15 * 1024  # Размер файла в Мбит
us = 30  # Скорость отдачи сервера в Мбит/с
di = 2  # Скорость загрузки каждого узла в Мбит/с
N_values = [10, 100, 1000]  # Количество узлов
u_values = [0.3, 0.7, 2]  # Скорость отдачи каждого узла в Мбит/с

# Функции для расчета времени раздачи
def client_server_time(F, us, di, N):
    ans = max(N * F / us, F/ di)
    print(f'client-server, N = {N}, equals ', ans)
    return ans

def p2p_time(F, us, di, u, N):
    ans = max(F/us, F/ di, N * F / (us + u * N))
    print(f'p2p, N={N}, U={u}, equals {ans}')
    return ans

fig, ax = plt.subplots()
# plt.ylabel('time (sec)')
# plt.xticks(3, N_values)
# plt.xlabel('users')

ax.plot(N_values, [client_server_time(F, us, di, n) for n in N_values], label=f'Клиент-сервер')

for u in u_values:
    y_p2p = [p2p_time(F, us, di, u, n) for n in N_values]
    ax.plot(N_values, y_p2p, label=f'P2P, u={u} Мбит/с')

plt.legend()
plt.savefig("img.png")
