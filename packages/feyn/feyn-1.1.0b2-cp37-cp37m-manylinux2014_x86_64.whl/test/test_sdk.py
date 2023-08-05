import unittest
import pandas as pd
import numpy as np

import feyn.losses
from feyn import QLattice


class TestSDK(unittest.TestCase):
    def setUp(self):
        self.lt = QLattice()
        self.lt.reset()

    def test_get_registers_validation(self):
        with self.subTest("should give friendly message, when tpe is wrong"):
            with self.assertRaises(ValueError) as ex:
                self.lt.get_register("Age", register_type="bad")

                # The error message explains the available types
                self.assertIn("fixed", str(ex.exception))
                self.assertIn("cat", str(ex.exception))

    def test_can_add_new_registers(self):
        self.assertEqual(len(self.lt.registers), 0)

        self.lt.get_register("Age",)
        self.lt.get_register("Smoker",)
        self.lt.get_register("bmi",)

        self.assertEqual(len(self.lt.registers), 3)

    def test_location_is_assigned_to_registers_automatically(self):
        r1 = self.lt.get_register("Age",)
        r2 = self.lt.get_register("Smoker",)

        self.assertNotEqual(r1.location, r2.location)

    def test_register_is_reused(self):
        self.lt.get_register("Age")
        self.lt.get_register("Smoker")
        self.assertEqual(len(self.lt.registers), 2)

        self.lt.get_register("Smoker")

        self.assertEqual(len(self.lt.registers), 2)

    def test_qlattice_extracts_qgraphs(self):
        r1 = self.lt.get_register("Age")
        r2 = self.lt.get_register("Smoker")
        r3 = self.lt.get_register("insurable")

        qgraph = self.lt.get_qgraph([r1, r2], r3)

        qgraph._extract_graphs()

        self.assertGreater(len(qgraph._graphs), 0)

    def test_fit_qgraph(self):
        r1 = self.lt.get_register("Age")
        r2 = self.lt.get_register("Smoker")
        r3 = self.lt.get_register("insurable")

        qgraph = self.lt.get_qgraph([r1, r2], r3)

        data = pd.DataFrame(np.array([
                [10, 16, 30, 60],
                [0, 1, 0, 1],
                [1, 1, 1, 0]
            ]).T,
            columns=["Age", "Smoker", "insurable"]).astype({
                "Age": "float32",
                "Smoker": "float32",
                "insurable": "float32"
            })

        with self.subTest("Can fit with default arguments"):
            qgraph.fit(data, show=None)

        with self.subTest("Can fit with named loss function"):
            qgraph.fit(data, loss_function="mean_absolute_error", show=None)

        with self.subTest("Can fit with loss function"):
            qgraph.fit(data, loss_function=feyn.losses.mean_absolute_error, show=None)

    def test_can_fetch_graphs_after_updates(self):
        r1 = self.lt.get_register("Age")
        r2 = self.lt.get_register("Smoker")
        r3 = self.lt.get_register("insurable")

        data = {
            "Age": [34],
            "Smoker": [0],
            "insurable": [1]
        }

        qgraph = self.lt.get_qgraph([r1, r2], r3)
        graph = qgraph.select(data)[0]
        self.lt.update(graph)

        qgraph = self.lt.get_qgraph([r1, r2], r3)

        self.assertGreater(len(qgraph._graphs), 0)

    def test_qgraph_select(self):
        r1 = self.lt.get_register("Age")
        r2 = self.lt.get_register("Smoker")
        r3 = self.lt.get_register("insurable")

        qgraph = self.lt.get_qgraph([r1, r2], r3)

        data = pd.DataFrame(np.array([
                [10, 16, 30, 60],
                [0, 1, 0, 1],
                [1, 1, 1, 0]
            ]).T,
            columns=["Age", "Smoker", "insurable"]).astype({
                "Age": "float32",
                "Smoker": "float32",
                "insurable": "float32"
            })

        qgraph.fit(data, show=None)

        testdata = pd.DataFrame(np.array([
        [8, 16, 25, 50],
        [0, 0, 1, 1],
        [1, 0, 1, 0]
            ]).T,
            columns=["Age", "Smoker", "insurable"]).astype({
                "Age": "float32",
                "Smoker": "float32",
                "insurable": "float32"
            })


        with self.subTest("Can select with default arguments"):
            graphs = qgraph.select(testdata)
            self.assertEqual(len(graphs), 5)  # Default limit

        with self.subTest("Can filter with lambda"):
            graphs = qgraph.select(testdata, filter_func=lambda g: False )
            self.assertEqual(len(graphs), 0)

        with self.subTest("Can provide a sort function"):
            graphs = qgraph.select(testdata, sort=lambda g, loss: loss, n=5)
            # TODO: Test that they actually got sorted
            self.assertEqual(len(graphs), 5)

        with self.subTest("Can provide a loss function"):
            graphs = qgraph.select(testdata, loss_function=feyn.losses.mean_absolute_error, n=5)
            # TODO: Test that they actually got sorted/filtered by that loss function
            self.assertEqual(len(graphs), 5)

        with self.subTest("Can provide the name of a loss function"):
            graphs = qgraph.select(testdata, loss_function="mean_absolute_error", n=5)
            # TODO: Test that they actually got sorted/filtered by that loss function
            self.assertEqual(len(graphs), 5)
