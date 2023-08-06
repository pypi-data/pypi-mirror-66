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

        age = self.lt.get_register("Age")
        smoker = self.lt.get_register("Smoker")
        bmi = self.lt.get_register("bmi")

        with self.subTest("Registers are available in the qlattice after addition"):
            self.assertEqual(len(self.lt.registers), 3)

        with self.subTest("Registers are put in different locations"):
            unique_locations = {age._latticeloc, smoker._latticeloc, bmi._latticeloc}
            self.assertEqual(len(unique_locations), 3)

    def test_register_is_reused(self):
        self.lt.get_register("Age")
        self.lt.get_register("Smoker")
        self.assertEqual(len(self.lt.registers), 2)

        self.lt.get_register("Smoker")

        self.assertEqual(len(self.lt.registers), 2)

    def test_qlattice_can_get_qgraph(self):
        r1 = self.lt.get_register("Age")
        r2 = self.lt.get_register("Smoker")
        r3 = self.lt.get_register("insurable")

        qgraph = self.lt.get_qgraph([r1, r2], r3)

        self.assertGreater(len(qgraph._graphs), 0)

    def test_qlattice_extract_graph_with_string_registers(self):
        r1 = self.lt.get_register("Age")
        r2 = self.lt.get_register("Smoker")
        r3 = self.lt.get_register("insurable")

        qgraph = self.lt.get_qgraph(["Age", "Smoker"], "insurable")

        self.assertGreater(len(qgraph._graphs), 0)

    def test_qlattice_extract_fails_if_invalid_register(self):
        r1 = self.lt.get_register("Age")
        r2 = self.lt.get_register("Smoker")
        r3 = self.lt.get_register("insurable")

        with self.assertRaises(ValueError) as ex:
            self.lt.get_qgraph(["Age", "Smoker", "Shoesize"], "insurable")
        self.assertRegex(str(ex.exception), "Shoesize")

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

        with self.subTest("Can provide a loss function"):
            graphs = qgraph.select(testdata, loss_function=feyn.losses.mean_absolute_error, n=5)
            # TODO: Test that they actually got sorted/filtered by that loss function
            self.assertEqual(len(graphs), 5)

        with self.subTest("Can provide the name of a loss function"):
            graphs = qgraph.select(testdata, loss_function="mean_absolute_error", n=5)
            # TODO: Test that they actually got sorted/filtered by that loss function
            self.assertEqual(len(graphs), 5)
