"""
Test case for matplotlib histogram issue with density=True and range parameter.

This test can be added to the matplotlib test suite to prevent regression.
"""
import numpy as np
import pytest


def test_hist_density_range_parameter():
    """
    Test that hist() respects range parameter when density=True.
    
    This addresses the bug where hist_kwargs = dict(density=density)
    would overwrite the previously set range parameter in hist_kwargs.
    
    Regression test for: https://github.com/matplotlib/matplotlib/issues/13989
    """
    # Import matplotlib components (would normally be at top of file in test suite)
    import matplotlib.pyplot as plt
    
    # Set reproducible random seed
    np.random.seed(42)
    
    # Create test data that naturally falls outside the desired range
    # This ensures the range parameter is actually tested
    data = np.random.normal(0.5, 0.3, 100)  # Mean=0.5, std=0.3
    
    # Test case 1: With density=True and range parameter
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(data, bins='auto', range=(0, 1), density=True)
    
    # Check that bins respect the range
    assert bins[0] == 0.0, f"First bin should be 0.0, got {bins[0]}"
    assert bins[-1] == 1.0, f"Last bin should be 1.0, got {bins[-1]}"
    
    # Check that density is properly normalized (integral should be ~1)
    integral = np.sum(n * np.diff(bins))
    assert abs(integral - 1.0) < 0.01, f"Density integral should be ~1, got {integral:.3f}"
    
    plt.close(fig)
    
    # Test case 2: With density=False and range parameter (should always work)
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(data, bins='auto', range=(0, 1), density=False)
    
    # Check that bins respect the range
    assert bins[0] == 0.0, f"First bin should be 0.0, got {bins[0]}"
    assert bins[-1] == 1.0, f"Last bin should be 1.0, got {bins[-1]}"
    
    plt.close(fig)
    
    # Test case 3: Compare density=True with explicit range vs without range
    fig, (ax1, ax2) = plt.subplots(1, 2)
    
    # With explicit range
    n1, bins1, _ = ax1.hist(data, bins='auto', range=(0, 1), density=True)
    
    # Without explicit range (should use data min/max)
    n2, bins2, _ = ax2.hist(data, bins='auto', density=True)
    
    # bins1 should use the explicit range
    assert bins1[0] == 0.0 and bins1[-1] == 1.0
    
    # bins2 should use data range
    assert bins2[0] != 0.0 or bins2[-1] != 1.0  # Should be different from explicit range
    
    plt.close(fig)


def test_hist_density_stacked_range():
    """Test that the fix doesn't affect stacked histograms."""
    import matplotlib.pyplot as plt
    
    np.random.seed(42)
    data1 = np.random.normal(0.3, 0.1, 100)
    data2 = np.random.normal(0.7, 0.1, 100)
    
    fig, ax = plt.subplots()
    
    # Test stacked histogram with density=True and range
    # The bug fix should not affect this case (stacked=True)
    n, bins, patches = ax.hist([data1, data2], bins='auto', range=(0, 1), 
                              density=True, stacked=True)
    
    # Check that bins respect the range
    assert bins[0] == 0.0, f"First bin should be 0.0, got {bins[0]}"
    assert bins[-1] == 1.0, f"Last bin should be 1.0, got {bins[-1]}"
    
    plt.close(fig)


if __name__ == "__main__":
    # Run the tests manually if executed directly
    print("Running matplotlib histogram range/density tests...")
    
    try:
        test_hist_density_range_parameter()
        print("✅ test_hist_density_range_parameter passed")
        
        test_hist_density_stacked_range()
        print("✅ test_hist_density_stacked_range passed")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)