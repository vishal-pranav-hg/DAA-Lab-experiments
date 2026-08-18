import streamlit as st
import time
import random
import pandas as pd


# ----------------------------
# Interpolation Search
# ----------------------------
def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1

        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        if arr[high] == arr[low]:
            break

        pos = low + int(
            ((target - arr[low]) * (high - low))
            / (arr[high] - arr[low])
        )

        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons


# ----------------------------
# Binary Search
# ----------------------------
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


# ----------------------------
# Performance Analysis
# ----------------------------
def performance_analysis():
    sizes = [1000, 5000, 10000, 50000, 100000]
    results = []

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        start = time.perf_counter()
        for _ in range(100):
            idx_is, comp_is = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000

        start = time.perf_counter()
        for _ in range(100):
            idx_bs, comp_bs = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000

        results.append({
            "Size": size,
            "IS Time (ms)": round(is_time, 6),
            "BS Time (ms)": round(bs_time, 6),
            "IS Comparisons": comp_is,
            "BS Comparisons": comp_bs
        })

    return pd.DataFrame(results)


# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(
    page_title="Interpolation Search Analyzer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Interpolation Search Analyzer")
st.write("Compare Interpolation Search and Binary Search")

st.subheader("Search in Custom Array")

array_input = st.text_input(
    "Enter a SORTED array (comma separated)",
    "2,5,10,15,23,35,48,60,75,90,105,120"
)

target = st.number_input(
    "Enter Target Value",
    value=35,
    step=1
)

if st.button("Run Search"):
    try:
        arr = list(map(int, array_input.split(",")))

        start = time.perf_counter()
        idx_i, comp_i = interpolation_search(arr, target)
        interp_time = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        idx_b, comp_b = binary_search(arr, target)
        binary_time = (time.perf_counter() - start) * 1000

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Interpolation Search")
            st.write(f"Index Found: {idx_i}")
            st.write(f"Comparisons: {comp_i}")
            st.write(f"Execution Time: {interp_time:.6f} ms")

        with col2:
            st.subheader("Binary Search")
            st.write(f"Index Found: {idx_b}")
            st.write(f"Comparisons: {comp_b}")
            st.write(f"Execution Time: {binary_time:.6f} ms")

    except:
        st.error("Please enter a valid sorted integer array.")

st.divider()

st.subheader("Performance Analysis")

if st.button("Generate Performance Table"):
    df = performance_analysis()
    st.dataframe(df, use_container_width=True)

    st.line_chart(
        df.set_index("Size")[["IS Time (ms)", "BS Time (ms)"]]
    )

st.divider()

st.markdown("""
### Complexity

*Interpolation Search*
- Average Case: O(log log n)
- Worst Case: O(n)
- Space Complexity: O(1)

*Binary Search*
- Average Case: O(log n)
- Worst Case: O(log n)
- Space Complexity: O(1)
""")