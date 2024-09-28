import unittest
from src.ai_integration import AI

class TestAIIntegration(unittest.TestCase):
    def setUp(self):
        self.ai = AI()

    def test_generate_advice(self):
        prompt = "What should I do next in the game?"
        advice = self.ai.generate_advice(prompt)
        self.assertIsInstance(advice, str)  # Check if the output is a string

if __name__ == '__main__':
    unittest.main()
