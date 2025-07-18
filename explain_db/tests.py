from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .views import ModelProvider


class ModelProviderTestCase(TestCase):
    """Test the ModelProvider class functionality."""
    
    def test_get_model_by_name_existing_model(self):
        """Test finding an existing model by name."""
        model = ModelProvider._get_model_by_name('User')
        self.assertEqual(model, User)
    
    def test_get_model_by_name_nonexistent_model(self):
        """Test finding a non-existent model returns None."""
        model = ModelProvider._get_model_by_name('NonExistentModel')
        self.assertIsNone(model)
    
    def test_force_str_safe_with_none(self):
        """Test force_str_safe handles None values."""
        result = ModelProvider.force_str_safe(None)
        self.assertIsNone(result)
    
    def test_force_str_safe_with_callable(self):
        """Test force_str_safe handles callable values."""
        result = ModelProvider.force_str_safe(lambda: "test")
        self.assertEqual(result, "<callable>")
    
    def test_get_ikshana_model_data_valid_model(self):
        """Test getting model data for a valid model."""
        model_data = ModelProvider.get_ikshana_model_data('User')
        self.assertIsInstance(model_data, list)
        self.assertEqual(len(model_data), 1)
        
        table_info = model_data[0]
        self.assertIn('table_name', table_info)
        self.assertIn('table_description', table_info)
        self.assertIn('columns', table_info)
        self.assertIsInstance(table_info['columns'], list)
    
    def test_get_ikshana_model_data_invalid_model(self):
        """Test getting model data for an invalid model raises ValueError."""
        with self.assertRaises(ValueError):
            ModelProvider.get_ikshana_model_data('InvalidModel')


class GetIkshanaModelDataAPITestCase(APITestCase):
    """Test the API endpoint functionality."""
    
    def test_get_valid_model_data(self):
        """Test API endpoint with a valid model name."""
        url = reverse('explain_db:get_model_data', kwargs={'model_name': 'User'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        
        table_info = response.data[0]
        self.assertIn('table_name', table_info)
        self.assertIn('columns', table_info)
    
    def test_get_invalid_model_data(self):
        """Test API endpoint with an invalid model name."""
        url = reverse('explain_db:get_model_data', kwargs={'model_name': 'InvalidModel'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data) 