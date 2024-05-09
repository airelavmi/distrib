import pytest
import requests

class TestRecommendationsAPI:
    @pytest.fixture(scope='module')
    def api_url(self):
        return "http://127.0.0.1:5000/recommend"

    def test_recommendations_for_genre(self, api_url):
        response = requests.get(api_url, params={"genre": "Fantastic"})
        assert response.status_code == 200
        expected_response = [
            ["1984", 1.0],
            ["The Martian", 1.0],
            ["Neuromancer", 1.0],
            ["A Time to Live and a Time to Die", 1.0],
            ["Childhood's End", 1.0]
        ]
        assert response.json() == expected_response

    def test_recommendations_for_author(self, api_url):
        response = requests.get(api_url, params={"author": "George Orwell"})
        assert response.status_code == 200
        expected_response = [
            ["1984", 1.0000000000000002],
            ["The Martian", 0.0],
            ["Neuromancer", 0.0],
            ["A Time to Live and a Time to Die", 0.0],
            ["Childhood's End", 0.0]
        ]
        assert response.json() == expected_response

    def test_recommendations_for_title(self, api_url):
        response = requests.get(api_url, params={"title": "A Time to Live and a Time to Die"})
        assert response.status_code == 200
        expected_response = [
            ["1984", 1.0],
            ["The Martian", 1.0],
            ["Neuromancer", 1.0],
            ["Childhood's End", 1.0],
            ["Crime and Punishment", 0.0]
        ]
        assert response.json() == expected_response
