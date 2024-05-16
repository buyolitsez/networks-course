import random
import sys

NUM = 5

class Router:
    def __init__(self, ip):
        self.ip = ip
        self.neighbors = []
        self.routing_table = {}

    def add(self, neighbor_ip, metric):
        self.routing_table[neighbor_ip] = {"next_hop": neighbor_ip, "metric": metric}

    def update(self, received_table, next_hop, step):
        flag = False
        for dest_ip, info in received_table.items():
            new_metric = info["metric"] + self.routing_table[next_hop]["metric"]
            if dest_ip not in self.routing_table or self.routing_table[dest_ip]["metric"] > new_metric:
                self.routing_table[dest_ip] = {"next_hop": next_hop, "metric": new_metric}
                flag = True
        if flag:
            self.log_step(step)
        return flag

    def get_table(self):
        result = f"{'[Source IP]':<17} {'[Destination IP]':<20} {'[Next Hop]':<17} {'[Metric]':>8}\n"
        for dest_ip, info in self.routing_table.items():
            result += f"{self.ip:<17} {dest_ip:<20} {info['next_hop']:<17} {info['metric']:>8}\n"
        return result

    def log_step(self, step):
        print(f"Simulation step {step} of router {self.ip}\n" + self.get_table())

    def log_final(self):
        print(f"Final state of router {self.ip} table:\n" + self.get_table())

    def log_init(self):
        print(f"Initial state of router {self.ip} table:\n" + self.get_table())


def generate():
    routers = {}
    for i in range(NUM):
        new_router = Router(f"192.168.1.{i}")
        routers[new_router.ip] = new_router
        for _ in range(random.randint(1, NUM)):
            dest = f"192.168.1.{random.randint(0, NUM-1)}"
            metric = random.randint(1, 10)
            routers[new_router.ip].add(dest, metric)
    return routers


def simulate_rip(routers):
    updated = True
    step = 0
    while updated:
        updated = False
        step += 1
        for router in routers.values():
            cc = router.routing_table.copy()
            for x in cc.values():
                next_hop = x['next_hop']
                if router.update(routers[next_hop].routing_table, next_hop, step):
                    updated = True


def main():
    routers = generate()
    for router in routers.values():
        router.log_init()
    simulate_rip(routers)
    for router in routers.values():
        router.log_final()


if __name__ == "__main__":
    main()
