import streamlit as st
from itertools import permutations

INF = float("inf")



def reduce_matrix(mat):
    """Reduce matrix and return reduced matrix and reduction cost."""

    m = [row[:] for row in mat]
    n = len(m)
    cost = 0

    # Row reduction
    for i in range(n):

        row_min = min(m[i])

        if row_min != INF and row_min != 0:
            cost += row_min

            m[i] = [
                x - row_min if x != INF else INF
                for x in m[i]
            ]

    # Column reduction
    for j in range(n):

        col_min = min(
            m[i][j]
            for i in range(n)
        )

        if col_min != INF and col_min != 0:

            cost += col_min

            for i in range(n):

                if m[i][j] != INF:
                    m[i][j] -= col_min

    return m, cost


def tsp_brute_force(cost, n):
    """Brute force solution for TSP."""

    cities = list(range(1, n))

    best_cost = INF
    best_path = None

    for perm in permutations(cities):

        path = [0] + list(perm) + [0]

        current_cost = sum(
            cost[path[i]][path[i + 1]]
            for i in range(n)
        )

        if current_cost < best_cost:

            best_cost = current_cost
            best_path = path

    return best_path, best_cost



st.set_page_config(
    page_title="5-City TSP",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Travelling Salesman Problem")
st.subheader("5-City TSP using Brute Force")


st.write(
    "This application finds the optimal tour for a 5-city "
    "Travelling Salesman Problem using brute force."
)


# ---------------------------------------
# Cost Matrix
# ---------------------------------------

cities = ["A", "B", "C", "D", "E"]

cost = [
    [INF, 10, 8, 9, 7],
    [10, INF, 5, 6, 10],
    [8, 5, INF, 7, 9],
    [9, 6, 7, INF, 6],
    [7, 10, 9, 6, INF]
]


st.header("📊 Cost Matrix")

# Display matrix
display_matrix = []

for i in range(5):

    row = []

    for j in range(5):

        if cost[i][j] == INF:
            row.append("INF")
        else:
            row.append(cost[i][j])

    display_matrix.append(row)


st.dataframe(
    {
        "": cities,
        "A": [row[0] for row in display_matrix],
        "B": [row[1] for row in display_matrix],
        "C": [row[2] for row in display_matrix],
        "D": [row[3] for row in display_matrix],
        "E": [row[4] for row in display_matrix]
    },
    hide_index=True,
    use_container_width=True
)


# ---------------------------------------
# Run TSP
# ---------------------------------------

if st.button(
    "🚀 Find Optimal Tour",
    use_container_width=True
):

    best_path, best_cost = tsp_brute_force(
        cost,
        5
    )

    # -----------------------------------
    # Optimal Tour
    # -----------------------------------

    st.header("🏆 Optimal Solution")

    tour = " → ".join(
        cities[i]
        for i in best_path
    )

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"**Optimal Tour:** {tour}"
        )

    with col2:

        st.success(
            f"**Minimum Cost:** {best_cost}"
        )


    # -----------------------------------
    # Path Verification
    # -----------------------------------

    st.header("🔍 Path Verification")

    verification = []

    for i in range(5):

        u = best_path[i]
        v = best_path[i + 1]

        verification.append(
            {
                "From": cities[u],
                "To": cities[v],
                "Cost": cost[u][v]
            }
        )

    st.dataframe(
        verification,
        hide_index=True,
        use_container_width=True
    )


# ---------------------------------------
# Algorithm Information
# ---------------------------------------

st.divider()

st.header("📚 Algorithm Information")

st.markdown("""
### Brute Force TSP

The brute force approach generates every possible permutation
of the cities and calculates the total cost of each tour.

**Time Complexity:** `O(n!)`

**Space Complexity:** `O(n)`

For 5 cities, the number of possible tours checked is:

`(n - 1)! = 4! = 24`
""")


# ---------------------------------------
# Matrix Reduction
# ---------------------------------------

st.divider()

st.header("🔽 Matrix Reduction")

if st.button(
    "Perform Matrix Reduction",
    use_container_width=True
):

    reduced_matrix, reduction_cost = reduce_matrix(cost)

    st.write(
        f"**Reduction Cost:** {reduction_cost}"
    )

    reduced_display = []

    for row in reduced_matrix:

        reduced_row = []

        for value in row:

            if value == INF:
                reduced_row.append("INF")
            else:
                reduced_row.append(value)

        reduced_display.append(reduced_row)

    st.dataframe(
        {
            "": cities,
            "A": [row[0] for row in reduced_display],
            "B": [row[1] for row in reduced_display],
            "C": [row[2] for row in reduced_display],
            "D": [row[3] for row in reduced_display],
            "E": [row[4] for row in reduced_display]
        },
        hide_index=True,
        use_container_width=True
    )


st.divider()

st.caption(
    "AD5303 – DAA Lab | Travelling Salesman Problem"
)