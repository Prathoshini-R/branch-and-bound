# Travelling Salesman Problem using Branch and Bound

INF = float('inf')


def tsp_branch_and_bound(graph):
    n = len(graph)

    # Find the minimum edge from each city
    first_min = []
    second_min = []

    for i in range(n):
        edges = sorted(graph[i][j] for j in range(n) if i != j)
        first_min.append(edges[0])
        second_min.append(edges[1])

    # Initial lower bound
    bound = 0
    for i in range(n):
        bound += first_min[i] + second_min[i]

    bound = (bound + 1) // 2

    visited = [False] * n
    visited[0] = True

    current_path = [0]
    best_path = []
    best_cost = INF

    def branch(level, current_cost, bound):
        nonlocal best_cost, best_path

        # If all cities are visited
        if level == n:
            last_city = current_path[-1]

            # Cost to return to starting city
            if graph[last_city][0] != 0:
                total_cost = current_cost + graph[last_city][0]

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_path = current_path[:] + [0]
            return

        last_city = current_path[-1]

        # Try every unvisited city
        for city in range(n):
            if not visited[city] and graph[last_city][city] != 0:

                new_cost = current_cost + graph[last_city][city]

                # Calculate new lower bound
                if level == 1:
                    new_bound = bound - (
                        (first_min[last_city] + first_min[city]) / 2
                    )
                else:
                    new_bound = bound - (
                        (second_min[last_city] + first_min[city]) / 2
                    )

                # Branch only if it can improve the current answer
                if new_cost + new_bound < best_cost:
                    visited[city] = True
                    current_path.append(city)

                    branch(level + 1, new_cost, new_bound)

                    current_path.pop()
                    visited[city] = False

    branch(1, 0, bound)

    return best_path, best_cost


# Example cost matrix
graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

path, cost = tsp_branch_and_bound(graph)

print("Optimal Path:", " -> ".join(map(str, path)))
print("Minimum Cost:", cost)
