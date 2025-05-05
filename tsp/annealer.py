import random
import math

class SimulatedAnnealingTSP:
    def __init__(self, cities, distances, energy_method='log', T=1000, T_min=1e-3, alpha=0.9,
                 max_iter=100000, closed_loop=True, seed=None):
        """
        Initializes the SimulatedAnnealingTSP solver.

        Parameters:
            cities (list[str]): List of city names.
            distances (list[list[float]]): Matrix of distances between cities.
            energy_method (str): Energy method ('log', 'square', 'sqrt', 'linear').
            T (float): Initial temperature.
            T_min (float): Minimum temperature.
            alpha (float): Cooling rate.
            max_iter (int): Maximum number of iterations.
            closed_loop (bool): If True, finds a closed-loop route; otherwise, an open route.
            seed (int): Random seed for reproducibility.
        """
        self.cities = cities
        self.distances = distances
        self.energy_method = energy_method
        self.T = T
        self.T_min = T_min
        self.alpha = alpha
        self.max_iter = max_iter
        self.closed_loop = closed_loop
        if seed is not None:
            random.seed(seed)

        self.n = len(cities)
        self.city_indices = list(range(self.n))

    def route_distance(self, route_indices):
        """Calculates the total route distance."""
        dist = sum(self.distances[route_indices[i]][route_indices[i + 1]] for i in range(self.n - 1))
        if self.closed_loop:
            dist += self.distances[route_indices[-1]][route_indices[0]]
        return dist

    def propose_new_route(self, route):
        """Proposes a new route by swapping two cities."""
        new_route = route.copy()
        i, j = random.sample(range(self.n), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def compute_energy(self, cost):
        """Applies the energy transformation."""
        if self.energy_method == 'log':
            return math.log(cost)
        elif self.energy_method == 'square':
            return cost ** 2
        elif self.energy_method == 'sqrt':
            return math.sqrt(cost)
        elif self.energy_method == 'linear':
            return cost
        else:
            raise ValueError(f"Unsupported energy method: {self.energy_method}")

    def run(self):
        """Runs the simulated annealing optimization."""
        current_route = self.city_indices.copy()
        random.shuffle(current_route)
        current_distance = self.route_distance(current_route)

        best_route = current_route.copy()
        best_distance = current_distance
        temperature_at_best = self.T

        temperatures = []
        distances_over_time = []
        acceptance_pressures = []
        pressure_temperatures = []

        iteration = 0
        T = self.T

        while T > self.T_min and iteration < self.max_iter:
            iteration += 1
            temperatures.append(T)
            distances_over_time.append(current_distance)

            candidate_route = self.propose_new_route(current_route)
            candidate_distance = self.route_distance(candidate_route)

            current_energy = self.compute_energy(current_distance)
            candidate_energy = self.compute_energy(candidate_distance)

            delta_E = candidate_energy - current_energy

            if delta_E < 0:
                current_route = candidate_route
                current_distance = candidate_distance
            else:
                acceptance_probability = math.exp(-delta_E / T)
                acceptance_pressures.append(acceptance_probability)
                pressure_temperatures.append(T)

                if random.random() < acceptance_probability:
                    current_route = candidate_route
                    current_distance = candidate_distance

            if current_distance < best_distance:
                best_distance = current_distance
                best_route = current_route.copy()
                temperature_at_best = T

            T *= self.alpha

        best_route_named = [self.cities[idx] for idx in best_route]
        if self.closed_loop:
            best_route_named.append(self.cities[best_route[0]])

        return {
            'best_route': best_route_named,
            'best_distance': best_distance,
            'temperature_at_best': temperature_at_best,
            'temperatures': temperatures,
            'distances_over_time': distances_over_time,
            'acceptance_pressures': acceptance_pressures,
            'pressure_temperatures': pressure_temperatures
        }
