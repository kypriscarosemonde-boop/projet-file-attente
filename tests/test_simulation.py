import unittest
from simulation import SimulationFileAttente

class TestSimulation(unittest.TestCase):
    def test_initialisation(self):
        sim = SimulationFileAttente(2.0, 0.5, 5)
        self.assertEqual(sim.lambda_arrivees, 2.0)
        self.assertAlmostEqual(sim.rho, 2.0/(5*0.5))

if __name__ == '__main__':
    unittest.main()