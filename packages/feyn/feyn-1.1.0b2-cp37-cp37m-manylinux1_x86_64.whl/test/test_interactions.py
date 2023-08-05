from sys import intern
import unittest
import pandas as pd
import numpy as np

import _feyn
import feyn

# This is a test to implement all interaction state logic.
# It is not meant to test, at least for now, the logic of the interations.
class TestInteractions(unittest.TestCase):

    def test_invalid_interaction_fails(self):
        with self.assertRaises(ValueError):
            fail = _feyn.Interaction('non-existing')

    def test_tanh_assign_to_state_is_not_allowed(self):
        with self.assertRaises(AttributeError):
            fail = _feyn.Interaction('tanh')
            fail.state = {}

    def test_tanh_interaction_attributes(self):
        interaction = _feyn.Interaction('tanh')
        self.assertEqual(interaction.state.bias, 0)

        d = interaction.state._to_dict()
        self.assertListEqual(list(d), ["w0","w1", "bias"])

    def test_tanh_state_update(self):
        interaction = _feyn.Interaction('tanh')
        self.assertEqual(interaction.state.bias, 0)

        d = {"w0": 1, "w1": 2, "bias": 3}
        d = interaction.state._from_dict(d)

        self.assertEqual(interaction.state.w0, 1)
        self.assertEqual(interaction.state.w1, 2)
        self.assertEqual(interaction.state.bias, 3)


    def test_sine_interaction_state(self):
        sine_interaction = _feyn.Interaction('sine')
        state = {
            'x0': 0,
            'k': 1.0
        }
        sine_interaction.state._from_dict(state)

        self.assertAlmostEqual(sine_interaction.state.x0, 0)
        self.assertAlmostEqual(sine_interaction.state.k, 1)


    def test_gaussian_interaction_state(self):
        gaussian_interaction = _feyn.Interaction('gaussian')
        state = {
            'center0': 0,
            'center1': 1.0,
            'w0': 0.2,
            'w1': 0.3
        }
        gaussian_interaction.state._from_dict(state)

        self.assertAlmostEqual(gaussian_interaction.state.center0, state['center0'])
        self.assertAlmostEqual(gaussian_interaction.state.center1, state['center1'])
        self.assertAlmostEqual(gaussian_interaction.state.w0, state['w0'])
        self.assertAlmostEqual(gaussian_interaction.state.w1, state['w1'])


    def test_handle_unsupported_properties(self):
        multiply_interaction = _feyn.Interaction('multiply')

        state = {
            'random_prop': 0
        }

        with self.assertRaises(AttributeError):
            multiply_interaction.state.random_prop = state['random_prop']

        with self.assertRaises(AttributeError):
            multiply_interaction.state._from_dict({'random_prop': 0})

        # from_dict ok if the dict is empty
        try:
            multiply_interaction.state._from_dict({})
        except:
            self.fail("Empty dict should be allowed")

        self.assertEqual(multiply_interaction.state._to_dict(), {})


    def test_category_register_interaction_state(self):
        register_cat_interaction = _feyn.Interaction('cat')
        state = {
            'categories': [
                ('red', 0.1),
                ('blue', 0.15),
                ('none', 0.001)
            ]
        }

        register_cat_interaction.state._from_dict(state)

        self.assertListEqual(sorted(state['categories']), sorted(register_cat_interaction.state.categories))


    def test_category_register_interaction_update(self):
        register_cat = _feyn.Interaction('cat', label='myinput')
        register_cat.state.categories = [
            ('red', 0.1),
            ('blue', 0.15),
        ]

        register_cat.set_source(0, -1)

        out = _feyn.Interaction("fixed", label="out")
        out.set_source(0,0)

        g = feyn.Graph(2)
        g[0] = register_cat
        g[1] = out
        o = g.predict({"myinput": np.array(["red", "blue", "purple", 42], dtype=object)})

        self.assertAlmostEqual(o[0],0.1)
        self.assertAlmostEqual(o[1],0.15)
        self.assertAlmostEqual(o[2],0.0)
        self.assertAlmostEqual(o[3],0.0)

        newstate = {i[0]: i[1] for i in register_cat.state.categories}
        self.assertAlmostEqual(newstate["purple"], 0.0)
        self.assertAlmostEqual(newstate[42], 0.0)

    def test_interaction_depth(self):
        reg = _feyn.Interaction("fixed")
        tanh = _feyn.Interaction("tanh")

        with self.assertRaises(RuntimeError):
            # Depth doesn't work outside of graphs
            d = reg.depth


        with self.subTest("Depth works in graphs"):
            g = _feyn.Graph(2)
            g[0]=reg
            g[1]=tanh
            tanh.set_source(0,reg.location)

            self.assertEqual(reg.depth, -1)
            self.assertEqual(tanh.depth, 0)

        
        with self.assertRaises(RuntimeError):
            # Depth doesnt work if the interaction has been implicitly removed
            g = _feyn.Graph(2)
            g[0]=reg
            g[1]=tanh

            del(g)
            reg.depth