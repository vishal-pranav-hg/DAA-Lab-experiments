import streamlit as st
import time
import random

st.set_page_config(
    page_title="Interpolation Search Analysis",
    page_icon="🔍",
    layout="wide"
)

def interpolation_search(arr, target):
    """
    Perform Interpolation Search on a sorted array.
    Returns: (target_index, probe_count, step_logs)
    """
    low = 0
    high = len(arr) - 1
    step_logs = []
    probes = 0

    while low <= high and arr[low] <= target <= arr[high]:
        probes += 1
        if arr[low] == arr[high]:
            if arr[low] == target:
                step_logs.append({
                    "Step": probes,
                    "Low Index": low,
                    "High Index": high,
                    "Low Val": arr[low],
                    "High Val": arr[high],
                    "Probe Index (pos)": low,
                    "Probe Val": arr[low],
                    "Action": f"Found target {target} (equal endpoints)"
                })
                return low, probes, step_logs
            else:
                step_logs.append({
                    "Step": probes,
                    "Low Index": low,
                    "High Index": high,
                    "Low Val": arr[low],
                    "High Val": arr[high],
                    "Probe Index (pos)": low,
                    "Probe Val": arr[low],
                    "Action": "Target not present (equal endpoints)"
                })
                return -1, probes, step_logs

        # Calculate probe position using interpolation formula
        pos = low + int(((float(high - low) / (arr[high] - arr[low])) * (target - arr[low])))

        # Boundary safety check
        if pos < low or pos > high:
            step_logs.append({
                "Step": probes,
                "Low Index": low,
                "High Index": high,
                "Low Val": arr[low],
                "High Val": arr[high],
                "Probe Index (pos)": pos,
                "Probe Val": "Out of bounds",
                "Action": "Calculated position out of range"
            })
            return -1, probes, step_logs

        probe_val = arr[pos]

        if probe_val == target:
            step_logs.append({
                "Step": probes,
                "Low Index": low,
                "High Index": high,
                "Low Val": arr[low],
                "High Val": arr[high],
                "Probe Index (pos)": pos,
                "Probe Val": probe_val,
                "Action": f"Target {target} found at index {pos}!"
            })
            return pos, probes, step_logs

        if probe_val < target:
            step_logs.append({
                "Step": probes,
                "Low Index": low,
                "High Index": high,
                "Low Val": arr[low],
                "High Val": arr[high],
                "Probe Index (pos)": pos,
                "Probe Val": probe_val,
                "Action": f"arr[{pos}] = {probe_val} < {target} -> Move low to {pos + 1}"
            })
            low = pos + 1
        else:
            step_logs.append({
                "Step": probes,
                "Low Index": low,
                "High Index": high,
                "Low Val": arr[low],
                "High Val": arr[high],
                "Probe Index (pos)": pos,
                "Probe Val": probe_val,
                "Action": f"arr[{pos}] = {probe_val} > {target} -> Move high to {pos - 1}"
            })
            high = pos - 1

    step_logs.append({
        "Step": probes + 1,
        "Low Index": low,
        "High Index": high,
        "Low Val": arr[low] if 0 <= low < len(arr) else "N/A",
        "High Val": arr[high] if 0 <= high < len(arr) else "N/A",
        "Probe Index (pos)": "N/A",
        "Probe Val": "N/A",
        "Action": f"Target {target} is outside remaining search range"
    })
    return -1, probes, step_logs

def binary_search(arr, target):
    """
    Perform standard Binary Search for comparative analysis.
    Returns: (target_index, probe_count, step_logs)
    """
    low = 0
    high = len(arr) - 1
    step_logs = []
    probes = 0

    while low <= high:
        probes += 1
        mid = (low + high) // 2
        mid_val = arr[mid]

        if mid_val == target:
            step_logs.append({
                "Step": probes,
                "Low Index": low,
                "High Index": high,
                "Mid Index": mid,
                "Mid Val": mid_val,
                "Action": f"Target {target} found at index {mid}!"
            })
            return mid, probes, step_logs
        elif mid_val < target:
            step_logs.append({
                "Step": probes,
                "Low Index": low,
                "High Index": high,
                "Mid Index": mid,
                "Mid Val": mid_val,
                "Action": f"arr[{mid}] = {mid_val} < {target} -> Move low to {mid + 1}"
            })
            low = mid + 1
        else:
            step_logs.append({
                "Step": probes,
                "Low Index": low,
                "High Index": high,
                "Mid Index": mid,
                "Mid Val": mid_val,
                "Action": f"arr[{mid}] = {mid_val} > {target} -> Move high to {mid - 1}"
            })
            high = mid - 1

    return -1, probes, step_logs

# Header Section
st.title("⚡ Interpolation Search Analysis & Comparison")
st.markdown("An interactive web application to analyze, visualize, and compare **Interpolation Search** against **Binary Search**.")

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")
data_option = st.sidebar.radio(
    "Data Source",
    ("Uniform Dataset", "Custom Input", "Random / Non-Uniform Dataset")
)

arr = []
if data_option == "Uniform Dataset":
    size = st.sidebar.number_input("Array Size", min_value=5, max_value=1000, value=20, step=5)
    step = st.sidebar.number_input("Step Increment", min_value=1, max_value=50, value=5, step=1)
    start_val = st.sidebar.number_input("Start Value", min_value=0, max_value=100, value=10, step=5)
    arr = [start_val + i * step for i in range(size)]

elif data_option == "Custom Input":
    user_str = st.sidebar.text_area("Enter comma-separated integers:", "10, 20, 30, 40, 50, 60, 70, 80, 90, 100")
    try:
        arr = sorted(list(set([int(x.strip()) for x in user_str.split(",") if x.strip()])))
    except ValueError:
        st.error("Please enter valid comma-separated integers.")
        arr = [10, 20, 30, 40, 50]

else:
    size = st.sidebar.number_input("Array Size", min_value=5, max_value=1000, value=25, step=5)
    random_seed = st.sidebar.number_input("Random Seed", min_value=0, max_value=9999, value=42, step=1)
    random.seed(random_seed)
    arr = sorted([random.randint(1, 500) for _ in range(size)])

if not arr:
    st.warning("Array is empty. Please provide valid elements.")
    st.stop()

# Target Selection
st.sidebar.subheader("🎯 Search Target")
default_target = arr[len(arr) // 2] if arr else 50
target = st.sidebar.number_input("Target Value to Search", value=default_target, step=1)

# Display Current Dataset
with st.expander("📊 View Array Dataset", expanded=True):
    st.write(f"**Sorted Array Size:** `{len(arr)}`")
    st.write(arr)

# Run Algorithms & Measure Execution Time
start_time_interp = time.perf_counter()
idx_interp, probes_interp, logs_interp = interpolation_search(arr, target)
end_time_interp = time.perf_counter()
dur_interp_us = (end_time_interp - start_time_interp) * 1e6

start_time_bin = time.perf_counter()
idx_bin, probes_bin, logs_bin = binary_search(arr, target)
end_time_bin = time.perf_counter()
dur_bin_us = (end_time_bin - start_time_bin) * 1e6

# Results Summary Cards
st.subheader("📌 Search Results & Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if idx_interp != -1:
        st.success(f"Found Target at Index {idx_interp}")
    else:
        st.error("Target Not Found")

with col2:
    st.metric("Interpolation Search Probes", f"{probes_interp} step(s)")

with col3:
    st.metric("Binary Search Probes", f"{probes_bin} step(s)")

with col4:
    diff_probes = probes_bin - probes_interp
    if diff_probes > 0:
        st.metric("Probe Difference", f"{probes_interp} vs {probes_bin}", f"-{diff_probes} probes saved", delta_color="normal")
    elif diff_probes < 0:
        st.metric("Probe Difference", f"{probes_interp} vs {probes_bin}", f"+{abs(diff_probes)} probes extra", delta_color="inverse")
    else:
        st.metric("Probe Difference", f"{probes_interp} vs {probes_bin}", "Equal probes")

# Detailed Execution Tracing Tabs
tab1, tab2, tab3 = st.columns([1, 1, 1])

t1, t2, t3 = st.tabs(["🔎 Interpolation Search Trace", "🌲 Binary Search Trace", "📖 Algorithm Mechanics & Formula"])

with t1:
    st.markdown("### Step-by-Step Execution Log (Interpolation Search)")
    if logs_interp:
        st.dataframe(logs_interp, use_container_width=True)
    else:
        st.info("No steps recorded.")

with t2:
    st.markdown("### Step-by-Step Execution Log (Binary Search)")
    if logs_bin:
        st.dataframe(logs_bin, use_container_width=True)
    else:
        st.info("No steps recorded.")

with t3:
    st.markdown("### 🧮 Interpolation Search Formula")
    st.latex(r"\text{pos} = \text{low} + \left( \frac{\text{target} - \text{arr}[\text{low}]}{\text{arr}[\text{high}] - \text{arr}[\text{low}]} \right) \times (\text{high} - \text{low})")
    
    st.markdown(r"""
    #### 💡 Key Concepts & Complexity Analysis:
    - **Uniform Distribution**: When elements are evenly spaced (e.g. `[10, 20, 30, 40, ...]`), Interpolation Search narrows down target locations in **$O(\log(\log n))$** time.
    - **Worst Case**: If data distribution is heavily skewed (e.g. exponential distribution), performance degrades to **$O(n)$**.
    - **Comparison with Binary Search**: Binary search always divides the array into half ($O(\log n)$), whereas Interpolation Search tries to estimate the target's position based on its value.
    """)
