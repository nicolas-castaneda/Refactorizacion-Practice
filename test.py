import unittest
from main import ElectionResultsProcessor, Vote

class TestElectionResultsProcessor(unittest.TestCase):
    def setUp(self):
        self.election_processor = ElectionResultsProcessor()

    def test_majority_winner(self):
        data_test = [
            ['Áncash', 'Asunción', 'Acochaca', '40810062', 'Aundrea Grace', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '86777322', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Eddie Hinesley', '1']
        ]
        winners = self.election_processor.process_votes(data_test)
        self.assertEqual(winners, ['Eddie Hinesley'])

    def test_tie_winner_is_first_in_file(self):
            data_test = [
                ['Áncash', 'Asunción', 'Acochaca', '40810062', 'Aundrea Grace', '1'],
                ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
                ['Áncash', 'Asunción', 'Acochaca', '86777322', 'Aundrea Grace', '1'],
                ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Eddie Hinesley', '1'],
                ['Áncash', 'Asunción', 'Acochaca', '78654323', 'Eddie Hinesley', '1'],
                ['Áncash', 'Asunción', 'Acochaca', '98654321', 'Aundrea Grace', '1']
            ]
            winners = self.election_processor.process_votes(data_test)
            self.assertEqual(winners, ['Aundrea Grace'])

    def test_no_majority_two_winners(self):
        data_test = [
            ['Áncash', 'Asunción', 'Acochaca', '40810062', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Aundrea Grace', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '86777322', 'Aundrea Grace', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '23017966', 'Alan Garcia', '1']
        ]
        winners = self.election_processor.process_votes(data_test)
        self.assertEqual(sorted(winners), ['Aundrea Grace', 'Eddie Hinesley'])

    def test_invalid_dni_is_not_counted(self):
        data_test = [
            ['Áncash', 'Asunción', 'Acochaca', '4081006', 'Eddie Hinesley', '1'],  # DNI invalido
            ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '86777322', 'Aundrea Grace', '1'],
            ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Aundrea Grace', '1']
        ]
        winners = self.election_processor.process_votes(data_test)
        self.assertEqual(winners, ['Aundrea Grace'])

    def test_valid_vote(self):
        vote = Vote(['Áncash', 'Asunción', 'Acochaca', '40810062', 'Eddie Hinesley', '1'])
        self.assertTrue(vote.is_valid)

    def test_invalid_dni_vote(self):
        vote = Vote(['Áncash', 'Asunción', 'Acochaca', '4081006', 'Eddie Hinesley', '1'])
        self.assertFalse(vote.is_valid) 
    
    def test_invalid_vote(self):
        vote = Vote(['Áncash', 'Asunción', 'Acochaca', '40810062', 'Eddie Hinesley', '0'])
        self.assertFalse(vote.is_valid)

if __name__ == '__main__':
    unittest.main()
