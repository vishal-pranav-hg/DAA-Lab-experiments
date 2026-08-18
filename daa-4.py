import heapq
import streamlit as st


# ---------- Dijkstra's Algorithm ----------
def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using Min-Heap

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    """

    n = len(graph)

    dist = [float("inf")] * n
    prev = [None] * n

    dist[source] = 0

    # (distance, vertex)
    pq = [(0, source)]

    visited = set()

    while pq:

        d, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, w in graph[u]:

            if dist[u] + w < dist[v]:

                dist[v] = dist[u] + w
                prev[v] = u

                heapq.heappush(
                    pq,
                    (dist[v], v)
                )

    return dist, prev


# ---------- Reconstruct Shortest Path ----------
def reconstruct_path(prev, source, target):

    path = []

    node = target

    while node is not None:

        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path

    return []


# =========================================================
#                    STREAMLIT UI
# =========================================================

st.set_page_config(
    page_title="Dijkstra's Algorithm",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ Dijkstra's Shortest Path Algorithm")

st.subheader("Shortest Path using Min-Heap")

st.write(
    "This application finds the shortest paths from a selected "
    "source vertex to all other vertices using Dijkstra's Algorithm."
)

st.divider()


# ---------- Graph Definition ----------

graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}


# ---------- Display Graph ----------

st.subheader("📌 Graph")

graph_data = []

for u in graph:

    for v, w in graph[u]:

        graph_data.append({
            "Source": u,
            "Destination": v,
            "Weight": w
        })

st.dataframe(
    graph_data,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ---------- Source Selection ----------

st.subheader("🎯 Select Source Vertex")

source = st.selectbox(
    "Source Vertex",
    list(graph.keys())
)


# ---------- Run Dijkstra ----------

if st.button("🚀 Find Shortest Paths"):

    dist, prev = dijkstra(graph, source)

    st.divider()

    st.subheader(
        f"📍 Shortest Paths from Vertex {source}"
    )


    # ---------- Results ----------

    results = []

    for v in range(len(graph)):

        path = reconstruct_path(
            prev,
            source,
            v
        )

        if path:
            path_str = " → ".join(
                map(str, path)
            )
        else:
            path_str = "No path"

        if dist[v] == float("inf"):
            distance = "INF"
        else:
            distance = dist[v]

        results.append({
            "Vertex": v,
            "Distance": distance,
            "Shortest Path": path_str
        })


    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )


    # ---------- Individual Results ----------

    st.subheader("📊 Path Details")

    for v in range(len(graph)):

        path = reconstruct_path(
            prev,
            source,
            v
        )

        if path:

            path_str = " → ".join(
                map(str, path)
            )

            st.success(
                f"Vertex {v}: "
                f"Distance = {dist[v]}, "
                f"Path = {path_str}"
            )

        else:

            st.warning(
                f"Vertex {v}: No path available"
            )


# ---------- Complexity ----------

st.divider()

st.subheader("⏱️ Algorithm Complexity")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Time Complexity",
        "O((V + E) log V)"
    )

with col2:

    st.metric(
        "Space Complexity",
        "O(V)"
    )