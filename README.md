# Simulated Annealing for the Traveling Salesman Problem (TSP)

This project implements a solution to the Traveling Salesman Problem (TSP) using **Simulated Annealing**, a stochastic optimization method inspired by statistical physics.

The goal is to find the shortest possible route that visits each city exactly once and returns to the starting point, using the Metropolis algorithm to guide the search process.

---

## Project Status

**Work in Progress** 

This project is currently under active development.  
The basic structure for simulated annealing is implemented and tested on small city sets.  
Additional features such as:
- Dynamic cooling schedules
- Visualization of optimization progress
- More complex distance generation
- Performance improvements

are planned to be added soon.

---

## How It Works

- Start with a random route through all cities.
- At each iteration:
  - Randomly swap two cities to propose a new route.
  - Accept or reject the new route based on the Metropolis criterion, using the current temperature.
- Gradually cool down the system by lowering the temperature.
- Track and update the best route found during the search.

The algorithm balances **exploration** (randomness) and **exploitation** (greediness) through a controlled cooling process.

---

## Files

- `simulated_annealing.py`: Main solver for the TSP using simulated annealing.
- `README.md`: Project overview (this file).
- (More files coming soon, as development continues.)

---

## Requirements

- Python 3.8+
- Standard libraries: `random`, `math`

Optional for plotting (future additions):
- `matplotlib`

---

## Acknowledgments

Project inspired by classical physics methods (Metropolis algorithm, canonical ensembles) and part of coursework for the Master's degree in Physics.  
Special thanks to the course instructors for guidance.

---

## License

This project is released under the MIT License.

