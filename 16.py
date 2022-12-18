import functools

# Valve KN has flow rate=0; tunnels lead to valves SZ, OU

v = {}
flows = {}
with open("input2") as f:
    for line in f:
        a, b = line.strip().split("; ")
        rate = int(a.split("=")[-1])
        name = a[len("Valve "):len("Valve ")+2]
        if b[:len("tunnels")] == "tunnels":
            edges = b.split("valves ")[-1].split(", ")
        else:
            edges = [b[-2:]]
        v[name] = edges
        flows[name] = rate


@functools.lru_cache(maxsize=None)
def explore(curr1, curr2, min, opened):
    if min == 26:
        return 0
    # open curr if unopened and > 0
    # go to a different node
    maxTotal = float("-inf")
    edges1 = v[curr1]
    edges2 = v[curr2]
    for e1 in edges1:
        for e2 in edges2:
            newTotal = explore(e1, e2, min+1, opened)
            maxTotal = max(newTotal, maxTotal)
    if flows[curr1] > 0 and curr1 not in opened:
        if flows[curr2] > 0 and curr2 not in opened:
            newOpened = tuple(sorted(opened + (curr2,curr1)))
            newTotal = explore(curr1, curr2, min+1, newOpened)
            maxTotal = max(maxTotal, newTotal+(flows[curr1]+flows[curr2])*(30-min))
        else:
            newOpened = tuple(sorted(opened + (curr1,)))
            newTotal = explore(curr1, curr2, min+1, newOpened)
            maxTotal = max(maxTotal, newTotal+flows[curr1]*(30-min))
    elif flows[curr2] > 0 and curr2 not in opened:
        newOpened = tuple(sorted(opened + (curr2,)))
        newTotal = explore(curr1, curr2, min+1, newOpened)
        maxTotal = max(maxTotal, newTotal+flows[curr2]*(30-min))
    return maxTotal

print(explore("AA", "AA", 1, ()))


# v = {}
# flows = {}
# with open("input") as f:
#     for line in f:
#         a, b = line.strip().split("; ")
#         rate = int(a.split("=")[-1])
#         name = a[len("Valve "):len("Valve ")+2]
#         if b[:len("tunnels")] == "tunnels":
#             edges = b.split("valves ")[-1].split(", ")
#         else:
#             edges = [b[-2:]]
#         v[name] = edges
#         flows[name] = rate
#
#
# @functools.lru_cache(maxsize=None)
# def explore(curr, min, opened):
#     if min == 30:
#         return 0
#     # open curr if unopened and > 0
#     # go to a different node
#     maxTotal = float("-inf")
#     edges = v[curr]
#     for e in edges:
#         newTotal = explore(e,  min+1, opened)
#         maxTotal = max(newTotal, maxTotal)
#     if flows[curr] > 0 and curr not in opened:
#         newOpened = tuple(sorted(opened + (curr,)))
#         newTotal = explore(curr, min+1, newOpened)
#         maxTotal = max(maxTotal, newTotal+flows[curr]*(30-min))
#     return maxTotal
#
# print(explore("AA", 1, ()))



# rev = {}
# for name, n in v.items():
#     for edge in n.edges:
#         if edge not in rev:
#             rev[edge] = Node(v[edge].flow, [])
#         rev[edge].edges.append(name)
#
# # for name, node in rev.items():
# #     print(name, node.flow, ":", node.edges)
#
# dp = [{} for i in range(30)]
# dp[0]["AA"] = {}
# dp[0]["AA"][()] = [0, 0] # dp[min][node][opened] = [flowTotal, fps]
#
# """
# dp[i][node][opened] = max(dp[i-1][node][opened]+node.flow, dp[i-1][prev][opened1], dp[i-1][prev][opened2],...)
# """
#
# print("------------------------------------------------------------------")
# for i in range(1, 30):
#     print("*****", i+1, "*****")
#     for name, n in rev.items():
#         for parent in n.edges:
#             if parent in dp[i-1]:
#                 for openValves, totals in dp[i-1][parent].items():
#                     total, fps = totals
#                     dp[i][name] = {openValves : [total + fps, fps]}
#         if name in dp[i-1] and n.flow > 0:
#             for openValves, totals in dp[i-1][name].items():
#                 total, fps = totals
#                 newValves = set(openValves)
#                 newValves.add(name)
#                 newValvesT = tuple(newValves)
#                 if name in dp[i] and newValvesT in dp[i][name]:
#                     if dp[i][name][newValvesT][0] < total+fps:
#                         dp[i][name][newValvesT] = [total+fps, fps+n.flow]
#                 else:
#                     dp[i][name] = {}
#                     dp[i][name][newValvesT] = [total+fps, fps+n.flow]
#     print(dp[i])
#     if i > 6:
#         exit()
# print(dp[-1].items())
