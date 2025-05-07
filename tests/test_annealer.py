import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import math
import pytest
from tsp.annealer import SimulatedAnnealingTSP

# Sample cities with distances to each other city a adj. matrix 
cities = ['A', 'B', 'C']
distances = [
    [0, 2, 9],
    [2, 0, 6],
    [9, 6, 0]
]

# Test route distance calculation for both open and closed
def test_route_distance_closed_loop():
    tsp = SimulatedAnnealingTSP(cities, distances, closed_loop=True)
    assert tsp.route_distance([0, 1, 2]) == 2 + 6 + 9

def test_route_distance_open_loop():
    tsp = SimulatedAnnealingTSP(cities, distances, closed_loop=False)
    assert tsp.route_distance([0, 1, 2]) == 2 + 6

# Test to ensure temperature is decreasing
def test_run_returns_expected_keys():
    tsp = SimulatedAnnealingTSP(cities, distances, seed=1)
    result = tsp.run()
    expected_keys = {
        'best_route',
        'best_distance',
        'temperature_at_best',
        'temperatures',
        'distances_over_time',
        'acceptance_pressures',
        'pressure_temperatures'
    }
    assert expected_keys.issubset(result.keys())

# Test energy transformation methods
@pytest.mark.parametrize('method', ['log', 'square', 'sqrt', 'linear'])
def test_energy_methods_supported(method):
    tsp = SimulatedAnnealingTSP(cities, distances, energy_method=method)
    assert isinstance(tsp.compute_energy(100), float)


def test_compute_energy_invalid():
    tsp = SimulatedAnnealingTSP(cities, distances, energy_method='nonexistent')
    with pytest.raises(ValueError):
        tsp.compute_energy(10)

# Test acceptance probability behavior
def test_acceptance_probability_behavior():
    tsp = SimulatedAnnealingTSP(cities, distances)
    prob_low_temp = tsp.acceptance_probability(delta_E=10, T=1)
    prob_high_temp = tsp.acceptance_probability(delta_E=10, T=100)
    assert prob_high_temp > prob_low_temp

# Test reproducibility by fixing seed
def test_reproducible_results_with_seed():
    tsp1 = SimulatedAnnealingTSP(cities, distances, seed=42)
    tsp2 = SimulatedAnnealingTSP(cities, distances, seed=42)
    result1 = tsp1.run()
    result2 = tsp2.run()
    assert result1['best_route'] == result2['best_route']
    assert math.isclose(result1['best_distance'], result2['best_distance'])

# Test output structure
def test_run_returns_expected_keys():
    tsp = SimulatedAnnealingTSP(cities, distances, seed=1)
    result = tsp.run()
    expected_keys = {
        'best_route',
        'best_distance',
        'temperature_at_best',
        'temperatures',
        'distances_over_time',
        'acceptance_pressures',
        'pressure_temperatures'
    }
    assert expected_keys.issubset(result.keys())
