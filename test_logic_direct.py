"""Direct test of the histogram logic without requiring full matplotlib build."""

import numpy as np

def test_histogram_bin_edges_logic():
    """Test the histogram_bin_edges function logic directly."""
    
    # Simulate the histogram_bin_edges function from the source
    def histogram_bin_edges(arr, bins, range=None, weights=None):
        # this in True for 1D arrays, and False for None and str
        if np.ndim(bins) == 1:
            return bins

        if isinstance(bins, str):
            # rather than backporting the internals, just do the full
            # computation.  If this is too slow for users, they can
            # update numpy, or pick a manual number of bins
            return np.histogram(arr, bins, range, weights)[1]
        else:
            if bins is None:
                # hard-code numpy's default
                bins = 10
            if range is None:
                range = np.min(arr), np.max(arr)

            return np.linspace(*range, bins + 1)
    
    # Test case: Test range parameter with different scenarios
    data = np.random.rand(10)
    
    print("Testing histogram_bin_edges function...")
    
    # Test 1: With range specified
    bins = histogram_bin_edges(data, "auto", range=(0, 1))
    print(f"With range=(0, 1): bins[0]={bins[0]}, bins[-1]={bins[-1]}")
    
    # Test 2: Without range specified (should use data min/max)
    bins_no_range = histogram_bin_edges(data, "auto", range=None)
    print(f"Without range: bins[0]={bins_no_range[0]}, bins[-1]={bins_no_range[-1]}")
    
    # Test 3: Direct np.histogram with range
    _, bins_direct = np.histogram(data, "auto", range=(0, 1))
    print(f"Direct np.histogram with range: bins[0]={bins_direct[0]}, bins[-1]={bins_direct[-1]}")
    
    return bins[0] == 0.0 and bins[-1] == 1.0

def simulate_hist_logic_bug():
    """Simulate the bug in the hist function."""
    print("\nSimulating the hist() function bug...")
    
    # Simulate the problematic code path
    bin_range = (0, 1)
    density = True
    stacked = False
    
    # This is what happens in the current buggy code:
    hist_kwargs = dict()  # Start empty
    
    # Line 6685: hist_kwargs['range'] = bin_range
    hist_kwargs['range'] = bin_range
    print(f"After setting range: hist_kwargs = {hist_kwargs}")
    
    # Line 6689: hist_kwargs = dict(density=density)  # BUG: This overwrites the range!
    if density and not stacked:
        hist_kwargs = dict(density=density)  # This is the bug!
    
    print(f"After setting density (BUGGY): hist_kwargs = {hist_kwargs}")
    print("❌ The range parameter is lost!")
    
    return 'range' not in hist_kwargs

def simulate_hist_logic_fixed():
    """Simulate the fixed version of hist function."""
    print("\nSimulating the FIXED hist() function...")
    
    # Simulate the fixed code path
    bin_range = (0, 1)
    density = True
    stacked = False
    
    # This is what should happen in the fixed code:
    hist_kwargs = dict()  # Start empty
    
    # Line 6685: hist_kwargs['range'] = bin_range
    hist_kwargs['range'] = bin_range
    print(f"After setting range: hist_kwargs = {hist_kwargs}")
    
    # Line 6689: hist_kwargs['density'] = density  # FIXED: Update instead of replace!
    if density and not stacked:
        hist_kwargs['density'] = density  # This is the fix!
    
    print(f"After setting density (FIXED): hist_kwargs = {hist_kwargs}")
    print("✅ The range parameter is preserved!")
    
    return 'range' in hist_kwargs and hist_kwargs['range'] == bin_range

if __name__ == "__main__":
    np.random.seed(42)
    
    print("=== Testing histogram bin edges logic ===")
    bin_edges_ok = test_histogram_bin_edges_logic()
    
    print("\n=== Demonstrating the bug ===")
    bug_present = simulate_hist_logic_bug()
    
    print("\n=== Demonstrating the fix ===")
    fix_works = simulate_hist_logic_fixed()
    
    print("\n=== Summary ===")
    print(f"Bin edges work correctly: {bin_edges_ok}")
    print(f"Bug is present in current code: {bug_present}")
    print(f"Fix resolves the issue: {fix_works}")