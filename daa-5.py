import random
import streamlit as st


# =========================================================
#              DIVIDE AND CONQUER MIN-MAX
# =========================================================

comparison_count = 0


def min_max_dc(arr, low, high):
    global comparison_count

    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:

        comparison_count += 1

        if arr[low] < arr[high]:
            return arr[low], arr[high]

        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2

    lmin, lmax = min_max_dc(
        arr,
        low,
        mid
    )

    rmin, rmax = min_max_dc(
        arr,
        mid + 1,
        high
    )

    # Conquer: compare minimum values
    comparison_count += 1

    if lmin < rmin:
        overall_min = lmin
    else:
        overall_min = rmin

    # Conquer: compare maximum values
    comparison_count += 1

    if lmax > rmax:
        overall_max = lmax
    else:
        overall_max = rmax

    return overall_min, overall_max


# =========================================================
#                    NAIVE APPROACH
# =========================================================

def min_max_naive(arr):

    mn = arr[0]
    mx = arr[0]

    comps = 0

    for x in arr[1:]:

        # Compare for minimum
        comps += 1

        if x < mn:
            mn = x

        # Compare for maximum
        comps += 1

        if x > mx:
            mx = x

    return mn, mx, comps


# =========================================================
#                    STREAMLIT UI
# =========================================================

st.set_page_config(
    page_title="Min-Max Comparison",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Min-Max using Divide & Conquer")

st.subheader(
    "Comparison between Divide & Conquer and Naive Approach"
)

st.write(
    "This application finds the minimum and maximum elements "
    "of an array and compares the number of comparisons used "
    "by both approaches."
)

st.divider()


# =========================================================
#                    USER INPUT
# =========================================================

st.subheader("🔢 Enter Array")

array_input = st.text_input(
    "Enter integers separated by commas",
    "3,1,7,4,9,2,8,5,6,0"
)


if st.button("🚀 Analyze Array"):

    try:

        arr = [
            int(x.strip())
            for x in array_input.split(",")
        ]

        if len(arr) == 0:
            st.error("Please enter at least one number.")
            st.stop()

        # =================================================
        #              DIVIDE & CONQUER
        # =================================================

        comparison_count = 0

        mn, mx = min_max_dc(
            arr,
            0,
            len(arr) - 1
        )

        dc_comps = comparison_count


        # =================================================
        #                    NAIVE
        # =================================================

        naive_min, naive_max, naive_comps = (
            min_max_naive(arr)
        )


        # =================================================
        #                    RESULTS
        # =================================================

        st.divider()

        st.subheader("📌 Array")

        st.write(arr)


        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Minimum",
                mn
            )

        with col2:
            st.metric(
                "Maximum",
                mx
            )

        with col3:
            st.metric(
                "Array Size",
                len(arr)
            )


        # =================================================
        #                COMPARISON RESULTS
        # =================================================

        st.divider()

        st.subheader("⚖️ Comparison Count")

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                f"Divide & Conquer Comparisons: "
                f"**{dc_comps}**"
            )

        with col2:

            st.info(
                f"Naive Comparisons: "
                f"**{naive_comps}**"
            )


        # =================================================
        #                    FORMULA
        # =================================================

        n = len(arr)

        if n % 2 == 0:
            formula = (3 * n // 2) - 2
        else:
            formula = (3 * (n - 1) // 2) + 1


        st.subheader("📐 Theoretical Comparison Count")

        st.write(
            f"For n = **{n}**, the theoretical "
            f"Divide & Conquer comparison count is approximately:"
        )

        st.success(
            f"Formula Result = {formula}"
        )


        # =================================================
        #                 PERFORMANCE TABLE
        # =================================================

        st.divider()

        st.subheader("📈 Performance Analysis")

        sizes = [
            10,
            100,
            1000,
            10000
        ]

        performance = []

        for size in sizes:

            test_arr = [
                random.randint(1, 10000)
                for _ in range(size)
            ]

            # Divide & Conquer
            comparison_count = 0

            min_max_dc(
                test_arr,
                0,
                len(test_arr) - 1
            )

            dc = comparison_count

            # Naive
            _, _, naive = min_max_naive(
                test_arr
            )

            # Theoretical formula
            if size % 2 == 0:
                formula = (3 * size // 2) - 2
            else:
                formula = (3 * (size - 1) // 2) + 1

            performance.append({
                "Array Size": size,
                "D&C Comparisons": dc,
                "Naive Comparisons": naive,
                "Formula": formula
            })


        st.dataframe(
            performance,
            use_container_width=True,
            hide_index=True
        )


        # =================================================
        #                  COMPLEXITY
        # =================================================

        st.divider()

        st.subheader("⏱️ Complexity Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Divide & Conquer")

            st.write(
                "Time Complexity: **O(n)**"
            )

            st.write(
                "Space Complexity: **O(log n)**"
            )

        with col2:

            st.markdown("### Naive Approach")

            st.write(
                "Time Complexity: **O(n)**"
            )

            st.write(
                "Space Complexity: **O(1)**"
            )


    except ValueError:

        st.error(
            "Invalid input! Please enter only integers "
            "separated by commas."
        )