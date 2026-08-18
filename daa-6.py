import streamlit as st


# ---------- Matrix Chain Multiplication ----------
def matrix_chain_order(dims):
    """
    Matrix Chain Multiplication using Dynamic Programming.

    dims:
    Matrix i has dimensions dims[i-1] x dims[i]

    Time Complexity: O(n^3)
    Space Complexity: O(n^2)
    """

    n = len(dims) - 1

    # m[i][j] = minimum scalar multiplications
    # for matrices i through j
    m = [[0] * (n + 1) for _ in range(n + 1)]

    # s[i][j] = split position
    s = [[0] * (n + 1) for _ in range(n + 1)]

    # Chain length
    for length in range(2, n + 1):

        for i in range(1, n - length + 2):

            j = i + length - 1

            m[i][j] = float("inf")

            for k in range(i, j):

                cost = (
                    m[i][k]
                    + m[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]
                )

                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k

    return m, s


# ---------- Print Optimal Parenthesization ----------
def print_optimal_parens(s, i, j):

    if i == j:
        return f"A{i}"

    k = s[i][j]

    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)

    return f"({left} × {right})"


# ---------- Streamlit UI ----------

st.set_page_config(
    page_title="Matrix Chain Multiplication",
    page_icon="🔢",
    layout="wide"
)

st.title("🔢 Matrix Chain Multiplication")
st.subheader("Dynamic Programming")

st.write(
    "Find the optimal order of multiplying a sequence of matrices "
    "to minimize the number of scalar multiplications."
)

st.divider()


# ---------- Input ----------

st.subheader("📐 Matrix Dimensions")

dims = st.text_input(
    "Enter dimensions separated by commas",
    "10,30,5,60,10"
)

st.caption(
    "Example: 10,30,5,60,10 represents "
    "A1 = 10×30, A2 = 30×5, A3 = 5×60, A4 = 60×10"
)


if st.button("🚀 Calculate Optimal Order"):

    try:

        # Convert input into integer list
        dims = [int(x.strip()) for x in dims.split(",")]

        if len(dims) < 2:
            st.error("Please enter at least 2 dimensions.")
            st.stop()

        if any(x <= 0 for x in dims):
            st.error("Dimensions must be positive integers.")
            st.stop()

        n = len(dims) - 1


        # ---------- Matrix Dimensions ----------

        st.subheader("📋 Matrix List")

        matrix_data = []

        for i in range(n):

            matrix_data.append({
                "Matrix": f"A{i + 1}",
                "Dimensions": f"{dims[i]} × {dims[i + 1]}"
            })

        st.table(matrix_data)


        # ---------- Run DP ----------

        m, s = matrix_chain_order(dims)


        # ---------- Results ----------

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("💰 Minimum Cost")

            st.success(
                f"{m[1][n]:,} scalar multiplications"
            )

        with col2:

            st.subheader("🎯 Optimal Parenthesization")

            optimal = print_optimal_parens(s, 1, n)

            st.info(optimal)


        # ---------- DP Cost Table ----------

        st.divider()

        st.subheader("📊 DP Cost Table")

        table = []

        for i in range(1, n + 1):

            row = {}

            for j in range(1, n + 1):

                if j < i:
                    row[f"A{j}"] = "---"

                else:
                    row[f"A{j}"] = m[i][j]

            table.append(row)

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )


        # ---------- Split Table ----------

        st.subheader("🔀 Split Table")

        split_table = []

        for i in range(1, n + 1):

            row = {}

            for j in range(1, n + 1):

                if j <= i:
                    row[f"A{j}"] = "---"

                else:
                    row[f"A{j}"] = s[i][j]

            split_table.append(row)

        st.dataframe(
            split_table,
            use_container_width=True,
            hide_index=True
        )


        # ---------- Complexity ----------

        st.divider()

        st.subheader("⏱️ Complexity")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Time Complexity",
                "O(n³)"
            )

        with col2:
            st.metric(
                "Space Complexity",
                "O(n²)"
            )


    except ValueError:

        st.error(
            "Invalid input! Please enter numbers separated by commas."
        )