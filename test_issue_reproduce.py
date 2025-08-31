"""Test script to reproduce the histogram issue with density=True and range parameter."""

import numpy as np
import matplotlib.pyplot as plt

def test_hist_range_density():
    """Test that hist respects range parameter when density=True."""
    print("Testing histogram with density=True and range=(0, 1)")
    
    # Test case from the issue
    _, bins, _ = plt.hist(np.random.rand(10), "auto", range=(0, 1), density=True)
    print("Bins:", bins)
    print("First bin:", bins[0])
    print("Last bin:", bins[-1])
    
    # Expected: bins should start at 0 and end at 1
    print("Expected first bin: 0.0")
    print("Expected last bin: 1.0")
    
    if bins[0] != 0.0 or bins[-1] != 1.0:
        print("❌ FAIL: Bins do not respect the range parameter")
        return False
    else:
        print("✅ PASS: Bins respect the range parameter")
        return True

def test_hist_range_no_density():
    """Test that hist respects range parameter when density=False (should work)."""
    print("\nTesting histogram with density=False and range=(0, 1)")
    
    # Test case to verify it works without density
    _, bins, _ = plt.hist(np.random.rand(10), "auto", range=(0, 1), density=False)
    print("Bins:", bins)
    print("First bin:", bins[0])
    print("Last bin:", bins[-1])
    
    if bins[0] != 0.0 or bins[-1] != 1.0:
        print("❌ FAIL: Bins do not respect the range parameter (even without density)")
        return False
    else:
        print("✅ PASS: Bins respect the range parameter without density")
        return True

if __name__ == "__main__":
    # Set seed for reproducible results
    np.random.seed(42)
    plt.clf()
    
    # Run tests
    test1_passed = test_hist_range_no_density()  # Should work
    test2_passed = test_hist_range_density()     # Currently broken
    
    print(f"\nSummary:")
    print(f"Test without density: {'PASSED' if test1_passed else 'FAILED'}")
    print(f"Test with density: {'PASSED' if test2_passed else 'FAILED'}")