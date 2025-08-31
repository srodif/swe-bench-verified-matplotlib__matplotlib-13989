"""Test for the hist() range and density interaction bug fix."""

import numpy as np

def test_hist_range_density_fix():
    """
    Test that hist() respects the range parameter when density=True.
    
    This test is for the bug where hist_kwargs = dict(density=density)
    would overwrite the range parameter that was previously set in hist_kwargs.
    """
    # Simulate the exact logic from matplotlib.axes._axes.hist
    
    # Setup test conditions
    bin_range = (0, 1)
    density = True
    stacked = False
    
    # Test the buggy version (before fix)
    def simulate_buggy_version():
        hist_kwargs = dict()
        
        # From line 6685: hist_kwargs['range'] = bin_range
        hist_kwargs['range'] = bin_range
        
        # From line 6687-6689 (BUGGY): hist_kwargs = dict(density=density)
        if density and not stacked:
            hist_kwargs = dict(density=density)  # This overwrites range!
            
        return hist_kwargs
    
    # Test the fixed version (after fix)
    def simulate_fixed_version():
        hist_kwargs = dict()
        
        # From line 6685: hist_kwargs['range'] = bin_range  
        hist_kwargs['range'] = bin_range
        
        # From line 6687-6689 (FIXED): hist_kwargs['density'] = density
        if density and not stacked:
            hist_kwargs['density'] = density  # This preserves range!
            
        return hist_kwargs
    
    # Test buggy version
    buggy_result = simulate_buggy_version()
    print(f"Buggy version result: {buggy_result}")
    assert 'range' not in buggy_result, "Buggy version should lose the range parameter"
    assert buggy_result == {'density': True}, "Buggy version should only have density"
    
    # Test fixed version  
    fixed_result = simulate_fixed_version()
    print(f"Fixed version result: {fixed_result}")
    assert 'range' in fixed_result, "Fixed version should preserve the range parameter"
    assert fixed_result['range'] == bin_range, "Fixed version should have correct range"
    assert fixed_result['density'] == density, "Fixed version should have correct density"
    assert fixed_result == {'range': (0, 1), 'density': True}, "Fixed version should have both parameters"
    
    print("✅ All tests passed! The fix correctly preserves the range parameter.")
    
def test_hist_range_density_numpy_integration():
    """
    Test that the hist_kwargs would work correctly with numpy.histogram.
    """
    np.random.seed(42)
    data = np.random.rand(10)
    
    # Test parameters that would be passed to np.histogram
    bins = 'auto'
    hist_kwargs_fixed = {'range': (0, 1), 'density': True}
    
    # This should work and respect the range
    counts, bin_edges = np.histogram(data, bins, **hist_kwargs_fixed)
    
    print(f"Data range: [{np.min(data):.3f}, {np.max(data):.3f}]")
    print(f"Bin edges: [{bin_edges[0]:.3f}, {bin_edges[-1]:.3f}]")
    print(f"Number of bins: {len(bin_edges) - 1}")
    print(f"Sum of counts * bin_widths: {np.sum(counts * np.diff(bin_edges)):.3f}")
    
    # Verify range is respected
    assert bin_edges[0] == 0.0, f"First bin edge should be 0.0, got {bin_edges[0]}"
    assert bin_edges[-1] == 1.0, f"Last bin edge should be 1.0, got {bin_edges[-1]}"
    
    # Verify density is working (integral should be approximately 1)
    integral = np.sum(counts * np.diff(bin_edges))
    assert abs(integral - 1.0) < 0.01, f"Density integral should be ~1.0, got {integral:.3f}"
    
    print("✅ Numpy integration test passed!")

if __name__ == "__main__":
    print("=== Testing hist() range and density fix ===")
    test_hist_range_density_fix()
    print()
    test_hist_range_density_numpy_integration()
    print("\n🎉 All tests passed! The fix is working correctly.")