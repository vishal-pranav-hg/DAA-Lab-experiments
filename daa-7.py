import streamlit as st


# =========================================================
#                  CHECK IF POSITION IS SAFE
# =========================================================

def is_safe(board, row, col):

    for prev_row in range(row):

        placed = board[prev_row]

        # Same column
        if placed == col:
            return False

        # Same diagonal
        if abs(prev_row - row) == abs(placed - col):
            return False

    return True


# =========================================================
#                  SOLVE N-QUEENS
# =========================================================

def solve_n_queens(n):

    board = [-1] * n

    solutions = []

    backtrack_count = [0]

    def backtrack(row):

        # All queens placed
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):

            if is_safe(board, row, col):

                # Place queen
                board[row] = col

                backtrack(row + 1)

                # Undo
                board[row] = -1

                backtrack_count[0] += 1

    backtrack(0)

    return solutions, backtrack_count[0]


# =========================================================
#                  DISPLAY CHESS BOARD
# =========================================================

def display_board(solution, n):

    board_display = []

    for row in range(n):

        row_data = []

        for col in range(n):

            if solution[row] == col:
                row_data.append("♛")
            else:
                row_data.append(".")

        board_display.append(row_data)

    return board_display


# =========================================================
#                    STREAMLIT UI
# =========================================================

st.set_page_config(
    page_title="N-Queens Backtracking",
    page_icon="♛",
    layout="wide"
)

st.title("♛ N-Queens Problem")
st.subheader("Solving N-Queens using Backtracking")

st.write(
    "Place N queens on an N × N chessboard such that "
    "no two queens attack each other."
)

st.divider()


# =========================================================
#                    SELECT N
# =========================================================

st.subheader("🔢 Select N")

n = st.selectbox(
    "Number of Queens",
    [4, 5, 6, 7, 8]
)


# =========================================================
#                    SOLVE
# =========================================================

if st.button("🚀 Solve N-Queens"):

    solutions, backtracks = solve_n_queens(n)

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    st.divider()

    st.subheader("📊 Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Number of Solutions",
            len(solutions)
        )

    with col2:
        st.metric(
            "Backtracks",
            backtracks
        )


    # -----------------------------------------------------
    # Display solutions
    # -----------------------------------------------------

    st.divider()

    if n <= 6:

        st.subheader(
            f"♛ All Solutions for {n}-Queens"
        )

        for i, solution in enumerate(
            solutions,
            start=1
        ):

            st.write(
                f"### Solution {i}"
            )

            st.write(
                f"Position representation: `{solution}`"
            )

            board = display_board(
                solution,
                n
            )

            for row in board:

                st.markdown(
                    " | ".join(row)
                )

            st.divider()

    else:

        st.info(
            f"There are {len(solutions)} solutions "
            f"for {n}-Queens. "
            "Only the solution count is displayed "
            "to avoid a very large output."
        )


# =========================================================
#                    COMPLEXITY
# =========================================================

st.divider()

st.subheader("⏱️ Complexity")

st.write(
    "Time Complexity: **O(N!)**"
)

st.write(
    "Space Complexity: **O(N)** for the recursion/board "
    "representation (excluding stored solutions)."
)