"""
Final demonstration showing the matplotlib histogram fix.

This script shows the before/after behavior for the bug where
hist() didn't respect range when density=True.
"""
import numpy as np

def demonstrate_fix():
    """Show the fix working by simulating the matplotlib logic."""
    
    print("=== Demonstrating the matplotlib histogram fix ===\n")
    
    # Simulate the test case from the issue
    np.random.seed(42)  # For reproducible results
    data = np.random.rand(10)
    bins = "auto"
    bin_range = (0, 1)  # This is the range parameter that was getting lost
    density = True
    stacked = False
    
    print(f"Test data: {data}")
    print(f"Data actual range: [{data.min():.3f}, {data.max():.3f}]")
    print(f"Desired range parameter: {bin_range}")
    print(f"Density parameter: {density}")
    print()
    
    # Show what happened BEFORE the fix (buggy behavior)
    print("🐛 BEFORE fix (buggy behavior):")
    hist_kwargs_buggy = {}
    
    # Step 1: Set the range (line 6685 in _axes.py)
    hist_kwargs_buggy['range'] = bin_range
    print(f"   After setting range: {hist_kwargs_buggy}")
    
    # Step 2: The buggy line (old line 6689)
    if density and not stacked:
        hist_kwargs_buggy = dict(density=density)  # BUG: overwrites range!
    print(f"   After setting density (BUGGY): {hist_kwargs_buggy}")
    print("   ❌ Range parameter lost!")
    
    # What would be passed to numpy.histogram
    counts_buggy, bins_buggy = np.histogram(data, bins, **hist_kwargs_buggy)
    print(f"   Resulting bins: [{bins_buggy[0]:.3f}, {bins_buggy[-1]:.3f}]")
    print(f"   ❌ Bins do NOT respect range=(0, 1)\n")
    
    # Show what happens AFTER the fix (correct behavior)
    print("✅ AFTER fix (correct behavior):")
    hist_kwargs_fixed = {}
    
    # Step 1: Set the range (line 6685 in _axes.py)
    hist_kwargs_fixed['range'] = bin_range
    print(f"   After setting range: {hist_kwargs_fixed}")
    
    # Step 2: The fixed line (new line 6689)
    if density and not stacked:
        hist_kwargs_fixed['density'] = density  # FIXED: preserves range!
    print(f"   After setting density (FIXED): {hist_kwargs_fixed}")
    print("   ✅ Range parameter preserved!")
    
    # What would be passed to numpy.histogram
    counts_fixed, bins_fixed = np.histogram(data, bins, **hist_kwargs_fixed)
    print(f"   Resulting bins: [{bins_fixed[0]:.3f}, {bins_fixed[-1]:.3f}]")
    print(f"   ✅ Bins DO respect range=(0, 1)")
    
    # Verify density normalization still works
    integral = np.sum(counts_fixed * np.diff(bins_fixed))
    print(f"   ✅ Density integral: {integral:.3f} (should be ~1.0)")
    print()
    
    # Summary
    print("📊 SUMMARY:")
    print(f"   Original issue: hist(data, 'auto', range=(0,1), density=True)")
    print(f"   Before fix: bins=[{bins_buggy[0]:.3f}, {bins_buggy[-1]:.3f}] ❌")
    print(f"   After fix:  bins=[{bins_fixed[0]:.3f}, {bins_fixed[-1]:.3f}] ✅")
    print()
    print("🎉 The fix successfully preserves the range parameter!")
    print("   Changed line 6689 in lib/matplotlib/axes/_axes.py:")
    print("   OLD: hist_kwargs = dict(density=density)")
    print("   NEW: hist_kwargs['density'] = density")
    
    return bins_fixed[0] == 0.0 and bins_fixed[-1] == 1.0

if __name__ == "__main__":
    success = demonstrate_fix()
    exit(0 if success else 1)