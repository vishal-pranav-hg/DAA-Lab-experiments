import streamlit as st
import math


# ---------------------------------------
# First Fit
# ---------------------------------------
def first_fit(items, capacity=1.0):
    bins = []
    bin_contents = []

    for item in items:

        placed = False

        for i, space in enumerate(bins):

            if space >= item:

                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break

        if not placed:

            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ---------------------------------------
# First Fit Decreasing
# ---------------------------------------
def first_fit_decreasing(items, capacity=1.0):

    sorted_items = sorted(items, reverse=True)

    return first_fit(sorted_items, capacity)


# ---------------------------------------
# Best Fit Decreasing
# ---------------------------------------
def best_fit_decreasing(items, capacity=1.0):

    sorted_items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in sorted_items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):

            if space >= item and space - item < best_space:

                best_space = space - item
                best_idx = i

        if best_idx >= 0:

            bins[best_idx] -= item
            bin_contents[best_idx].append(item)

        else:

            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ---------------------------------------
# Streamlit Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="Bin Packing Analysis",
    page_icon="📦",
    layout="wide"
)


# ---------------------------------------
# Title
# ---------------------------------------

st.title("📦 Bin Packing Problem")

st.subheader(
    "First Fit, First Fit Decreasing & Best Fit Decreasing"
)

st.write(
    "Compare different bin packing heuristics and "
    "analyze the number of bins used."
)


# ---------------------------------------
# Sidebar
# ---------------------------------------

st.sidebar.header("⚙️ Input Configuration")

capacity = st.sidebar.number_input(
    "Bin Capacity",
    min_value=0.1,
    max_value=100.0,
    value=1.0,
    step=0.1
)


items_input = st.sidebar.text_area(
    "Enter Items",
    value="0.5, 0.7, 0.3, 0.9, 0.2, 0.6, 0.8, 0.4, 0.1, 0.5"
)


# ---------------------------------------
# Convert Input
# ---------------------------------------

try:

    items = [
        float(x.strip())
        for x in items_input.split(",")
        if x.strip()
    ]

except ValueError:

    st.error(
        "Please enter valid numbers separated by commas."
    )

    st.stop()


# Check item size
if any(item > capacity for item in items):

    st.error(
        "An item is larger than the bin capacity."
    )

    st.stop()


# ---------------------------------------
# Input Information
# ---------------------------------------

st.header("📋 Input")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Number of Items",
        len(items)
    )

with col2:
    st.metric(
        "Total Item Size",
        f"{sum(items):.2f}"
    )

with col3:

    lower_bound = math.ceil(
        sum(items) / capacity
    )

    st.metric(
        "Lower Bound",
        lower_bound
    )


st.write("**Items:**")

st.code(
    str([round(x, 2) for x in items])
)


# ---------------------------------------
# Run Algorithms
# ---------------------------------------

if st.button(
    "🚀 Run Bin Packing Algorithms",
    use_container_width=True
):

    ff_bins = first_fit(
        items,
        capacity
    )

    ffd_bins = first_fit_decreasing(
        items,
        capacity
    )

    bfd_bins = best_fit_decreasing(
        items,
        capacity
    )


    # -----------------------------------
    # Summary
    # -----------------------------------

    st.header("📊 Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Lower Bound",
            lower_bound
        )

    with col2:
        st.metric(
            "First Fit",
            len(ff_bins)
        )

    with col3:
        st.metric(
            "First Fit Decreasing",
            len(ffd_bins)
        )

    with col4:
        st.metric(
            "Best Fit Decreasing",
            len(bfd_bins)
        )


    # -----------------------------------
    # Display Function
    # -----------------------------------

    def display_bins(label, bins):

        st.subheader(
            f"{label} — {len(bins)} bins"
        )

        for i, b in enumerate(bins, 1):

            used = sum(b)
            remaining = capacity - used

            percentage = (
                used / capacity
            ) * 100

            st.write(
                f"**Bin {i}:** "
                f"{[round(x, 2) for x in b]}"
            )

            st.progress(
                min(percentage / 100, 1.0)
            )

            st.caption(
                f"Used: {used:.2f} / {capacity:.2f} "
                f"| Remaining: {remaining:.2f}"
            )


    # -----------------------------------
    # Results
    # -----------------------------------

    st.divider()

    st.header("🔎 Detailed Results")

    tab1, tab2, tab3 = st.tabs(
        [
            "First Fit",
            "First Fit Decreasing",
            "Best Fit Decreasing"
        ]
    )


    with tab1:

        display_bins(
            "First Fit (FF)",
            ff_bins
        )


    with tab2:

        display_bins(
            "First Fit Decreasing (FFD)",
            ffd_bins
        )


    with tab3:

        display_bins(
            "Best Fit Decreasing (BFD)",
            bfd_bins
        )


    # -----------------------------------
    # Comparison
    # -----------------------------------

    st.divider()

    st.header("📈 Algorithm Comparison")

    comparison = {
        "Algorithm": [
            "First Fit (FF)",
            "First Fit Decreasing (FFD)",
            "Best Fit Decreasing (BFD)"
        ],

        "Bins Used": [
            len(ff_bins),
            len(ffd_bins),
            len(bfd_bins)
        ],

        "Difference from Lower Bound": [
            len(ff_bins) - lower_bound,
            len(ffd_bins) - lower_bound,
            len(bfd_bins) - lower_bound
        ]
    }

    st.dataframe(
        comparison,
        hide_index=True,
        use_container_width=True
    )


    # -----------------------------------
    # Best Algorithm
    # -----------------------------------

    results = {
        "First Fit": len(ff_bins),
        "First Fit Decreasing": len(ffd_bins),
        "Best Fit Decreasing": len(bfd_bins)
    }

    best_algorithm = min(
        results,
        key=results.get
    )

    best_count = results[best_algorithm]

    st.success(
        f"🏆 Best result: **{best_algorithm}** "
        f"using **{best_count} bins**."
    )


# ---------------------------------------
# Complexity
# ---------------------------------------

st.divider()

st.header("📚 Time Complexity")

complexity = {
    "Algorithm": [
        "First Fit",
        "First Fit Decreasing",
        "Best Fit Decreasing"
    ],

    "Time Complexity": [
        "O(n²)",
        "O(n log n + n²)",
        "O(n log n + n²)"
    ],

    "Space Complexity": [
        "O(n)",
        "O(n)",
        "O(n)"
    ]
}

st.table(complexity)


st.divider()

st.caption(
    "AD5303 – DAA Lab | Bin Packing Problem"
)