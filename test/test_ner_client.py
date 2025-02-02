import unittest
from nerclient import NamedEntityClient
from test_doubles import NerModelTestDouble

class MockDisplayy:
    def render(self, doc, style=None):
        return "<span>mock render</span>"

class TestNerClient(unittest.TestCase):
    def setUp(self):
        self.mock_displacy = MockDisplayy()

    def test_get_ents_returns_dictionary_given_empty_string_causes_empty_sapcy_doc_ents(self):
        model = NerModelTestDouble('eng')
        model.returns_doc_ents([])
        ner = NamedEntityClient(model, self.mock_displacy)
        ents = ner.get_ents("")
        self.assertIsInstance(ents, dict)

    def test_get_ents_returns_dictionary_given_nonempty_string_causes_empty_spacy_doc_ents(self):
        model = NerModelTestDouble('eng')
        model.returns_doc_ents([])
        ner = NamedEntityClient(model, self.mock_displacy)
        ents = ner.get_ents("Madison is a city in Wisconsin")
        self.assertIsInstance(ents, dict)

    def test_get_ents_given_spacy_PERSON_is_returned_serializes_to_Person(self):
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'Laurent Fressinet','label_':'PERSON'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model, self.mock_displacy)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'Laurent Fressinet', 'label': 'Person'}], 'html': '<span>mock render</span>' }
        self.assertListEqual(result['ents'], expected_result['ents'])

    def test_get_ents_given_spacy_NORP_is_returned_serializes_to_Group(self):
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'Lithuanian', 'label_':'NORP'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model, self.mock_displacy)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'Lithuanian', 'label': 'Group'}], 'html': '<span>mock render</span>' }
        self.assertListEqual(result['ents'], expected_result['ents'])

    def test_get_ents_given_spacy_LOC_is_returned_serializes_to_Location(self):
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'the ocean', 'label_':'LOC'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model, self.mock_displacy)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'the ocean', 'label': 'Location'}], 'html': '<span>mock render</span>' }
        self.assertListEqual(result['ents'], expected_result['ents'])

    def test_get_ents_given_spacy_LANGUAGE_is_returned_serializes_to_Langauge(self):
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'ASL', 'label_':'LANGUAGE'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model, self.mock_displacy)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'ASL', 'label': 'Language'}], 'html': '<span>mock render</span>' }
        self.assertListEqual(result['ents'], expected_result['ents'])

    def test_get_ents_given_spacy_GPE_is_returned_serializes_to_Location(self):
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'Australia', 'label_':'GPE'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model, self.mock_displacy)
        result = ner.get_ents('...')
        expected_result = { 'ents': [{'ent': 'Australia', 'label': 'Location'}], 'html': '<span>mock render</span>' }
        self.assertListEqual(result['ents'], expected_result['ents'])

    def test_get_ents_given_multiple_ents_serializes_all(self):
        model = NerModelTestDouble('eng')
        doc_ents = [{'text': 'Australia', 'label_':'GPE'},
                    {'text': 'Judith Polgar', 'label_':'PERSON'}]
        model.returns_doc_ents(doc_ents)
        ner = NamedEntityClient(model, self.mock_displacy)
        result = ner.get_ents('...')
        expected_result = { 
            'ents': [
                {'ent': 'Australia', 'label': 'Location'},
                {'ent': 'Judith Polgar', 'label': 'Person'}
            ],
            'html': '<span>mock render</span>'
        }
        self.assertListEqual(result['ents'], expected_result['ents'])

if __name__ == '__main__':
    unittest.main()