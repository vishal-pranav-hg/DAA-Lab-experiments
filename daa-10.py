import streamlit as st
import random
import time
import pandas as pd
import sys

sys.setrecursionlimit(20000)


# ==========================================
# Global comparison counter
# ==========================================

comparisons = 0


# ==========================================
# Partition
# ==========================================

def partition(arr, low, high):
    global comparisons

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):

        comparisons += 1

        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


# ==========================================
# Deterministic QuickSort
# ==========================================

def deterministic_quicksort(arr, low, high):

    if low < high:

        pi = partition(arr, low, high)

        deterministic_quicksort(
            arr,
            low,
            pi - 1
        )

        deterministic_quicksort(
            arr,
            pi + 1,
            high
        )


# ==========================================
# Randomized QuickSort
# ==========================================

def randomized_quicksort(arr, low, high):

    if low < high:

        # Select a random pivot
        rand_idx = random.randint(
            low,
            high
        )

        # Move random pivot to the end
        arr[rand_idx], arr[high] = (
            arr[high],
            arr[rand_idx]
        )

        pi = partition(
            arr,
            low,
            high
        )

        randomized_quicksort(
            arr,
            low,
            pi - 1
        )

        randomized_quicksort(
            arr,
            pi + 1,
            high
        )


# ==========================================
# Run Test
# ==========================================

def run_test(sort_fn, arr):

    global comparisons

    a = arr[:]

    comparisons = 0

    start = time.perf_counter()

    sort_fn(
        a,
        0,
        len(a) - 1
    )

    elapsed = (
        time.perf_counter() - start
    ) * 1000

    return comparisons, elapsed


# ==========================================
# Generate Test Cases
# ==========================================

def generate_test_cases(n):

    test_cases = {

        "Random": [
            random.randint(1, 100000)
            for _ in range(n)
        ],

        "Sorted": list(range(n)),

        "Reverse": list(
            range(n, 0, -1)
        ),

        "Nearly Sorted": list(range(n))
    }

    # Slightly shuffle nearly sorted array
    ns = test_cases["Nearly Sorted"]

    for _ in range(n // 20):

        i = random.randint(
            0,
            n - 1
        )

        j = random.randint(
            0,
            n - 1
        )

        ns[i], ns[j] = (
            ns[j],
            ns[i]
        )

    return test_cases


# ==========================================
# Streamlit Configuration
# ==========================================

st.set_page_config(
    page_title="QuickSort Performance",
    page_icon="⚡",
    layout="wide"
)


# ==========================================
# Title
# ==========================================

st.title(
    "⚡ Deterministic vs Randomized QuickSort"
)

st.subheader(
    "Performance Analysis"
)

st.write(
    "Compare Deterministic QuickSort and "
    "Randomized QuickSort using different input cases."
)


# ==========================================
# Sidebar
# ==========================================

st.sidebar.header(
    "⚙️ Test Configuration"
)

N = st.sidebar.number_input(
    "Number of Elements",
    min_value=100,
    max_value=10000,
    value=5000,
    step=100
)


# ==========================================
# Input Types
# ==========================================

st.header("📋 Test Cases")

st.write(
    "The following four input types will be tested:"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("🎲 Random")

with col2:
    st.info("📈 Sorted")

with col3:
    st.info("📉 Reverse")

with col4:
    st.info("🔀 Nearly Sorted")


# ==========================================
# Run Analysis
# ==========================================

if st.button(
    "🚀 Run Performance Analysis",
    use_container_width=True
):

    test_cases = generate_test_cases(N)

    results = []

    progress = st.progress(0)

    total_cases = len(test_cases)

    for index, (case, arr) in enumerate(
        test_cases.items()
    ):

        # Deterministic QuickSort
        d_comps, d_time = run_test(
            deterministic_quicksort,
            arr
        )

        # Randomized QuickSort
        r_comps, r_time = run_test(
            randomized_quicksort,
            arr
        )

        results.append({

            "Input Type": case,

            "DQS Comparisons": d_comps,

            "DQS Time (ms)": round(
                d_time,
                2
            ),

            "RQS Comparisons": r_comps,

            "RQS Time (ms)": round(
                r_time,
                2
            )
        })

        progress.progress(
            (index + 1) / total_cases
        )

    st.success(
        "Performance analysis completed!"
    )


    # ======================================
    # Results Table
    # ======================================

    st.header("📊 Performance Results")

    df = pd.DataFrame(results)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )


    # ======================================
    # Comparison Charts
    # ======================================

    st.divider()

    st.header("📈 Comparison")


    # Time comparison
    st.subheader(
        "⏱️ Execution Time"
    )

    time_df = df.set_index(
        "Input Type"
    )[
        [
            "DQS Time (ms)",
            "RQS Time (ms)"
        ]
    ]

    st.bar_chart(time_df)


    # Comparison count
    st.subheader(
        "🔢 Number of Comparisons"
    )

    comparison_df = df.set_index(
        "Input Type"
    )[
        [
            "DQS Comparisons",
            "RQS Comparisons"
        ]
    ]

    st.bar_chart(comparison_df)


    # ======================================
    # Best Results
    # ======================================

    st.divider()

    st.header("🏆 Analysis")

    for _, row in df.iterrows():

        case = row["Input Type"]

        d_time = row["DQS Time (ms)"]
        r_time = row["RQS Time (ms)"]

        if d_time < r_time:
            faster = "Deterministic QuickSort"
        else:
            faster = "Randomized QuickSort"

        st.write(
            f"**{case}:** {faster} was faster "
            f"({min(d_time, r_time):.2f} ms)"
        )


# ==========================================
# Complexity
# ==========================================

st.divider()

st.header("📚 Time Complexity")

complexity = {

    "Algorithm": [
        "Deterministic QuickSort",
        "Randomized QuickSort"
    ],

    "Best Case": [
        "O(n log n)",
        "O(n log n)"
    ],

    "Average Case": [
        "O(n log n)",
        "O(n log n)"
    ],

    "Worst Case": [
        "O(n²)",
        "O(n²)"
    ],

    "Space": [
        "O(log n)",
        "O(log n)"
    ]
}

st.table(complexity)


# ==========================================
# Footer
# ==========================================

st.divider()

st.caption(
    "AD5303 – DAA Lab | Deterministic and "
    "Randomized QuickSort Performance Analysis"
)