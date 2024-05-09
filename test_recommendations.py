import pytest
import requests

class TestRecommendationsAPI:
    @pytest.fixture(scope='module')
    def api_url(self):
        return "http://127.0.0.1:5000/recommend"

    def test_recommendations_for_genre(self, api_url):
        response = requests.get(api_url, params={"genre": "Detective"})
        assert response.status_code == 200

    def test_recommendations_for_author(self, api_url):
        response = requests.get(api_url, params={"author": "George Orwell"})
        assert response.status_code == 200


