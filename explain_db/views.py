from django.apps import apps
from django.utils.encoding import force_str
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
import json


class ModelProvider:
    @classmethod
    def get_ikshana_model_data(cls, model_name):
        """
        Get metadata for a Django model by name.
        
        Args:
            model_name: String name of the model class
            
        Returns:
            List containing model metadata dictionary
        """
        try:
            # Try to find the model in all installed apps
            model = cls._get_model_by_name(model_name)
            if not model:
                raise ValueError(f"Model '{model_name}' not found")
                
            model_data = []
            model_meta = model._meta
            
            table_info = {
                "table_name": f'"{model_meta.db_table}"',
                "table_description": model.__doc__ if model.__doc__ else "",
                "columns": []
            }
            
            for field in model_meta.get_fields():
                if field.auto_created and not field.concrete:
                    continue

                column_info = {
                    "name": field.name,
                    "type": type(field).__name__,
                    "description": getattr(field, 'help_text', ''),
                    "is_relation": field.is_relation,
                    "nullable": getattr(field, 'null', False),
                    "blank": getattr(field, 'blank', False),
                    "default": cls.force_str_safe(cls.get_serializable_default(field))
                }

                if field.is_relation and hasattr(field, 'related_model') and field.related_model:
                    column_info["related_model"] = {
                        "app_label": field.related_model._meta.app_label,
                        "model_name": field.related_model.__name__,
                        "db_table": field.related_model._meta.db_table,
                    }

                table_info["columns"].append(column_info)
            
            model_data.append(table_info)
            return model_data
            
        except Exception as e:
            raise ValueError(f"Error processing model '{model_name}': {str(e)}")
    
    @classmethod
    def _get_model_by_name(cls, model_name):
        """
        Find a model by name across all installed Django apps.
        
        Args:
            model_name: String name of the model class
            
        Returns:
            Model class if found, None otherwise
        """
        # First try to get from globals (for backward compatibility)
        model = globals().get(model_name)
        if model:
            return model
            
        # Search through all registered models
        for app_config in apps.get_app_configs():
            try:
                model = app_config.get_model(model_name.lower())
                if model:
                    return model
            except LookupError:
                continue
                
        # Try case-insensitive search
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                if model.__name__.lower() == model_name.lower():
                    return model
                    
        return None
    
    @classmethod
    def force_str_safe(cls, value):
        """
        Safely convert a value to string, handling various types.
        
        Args:
            value: Any value to convert to string
            
        Returns:
            String representation of the value
        """
        if value is None:
            return None
        
        try:
            if callable(value):
                # For callable defaults, we can't safely evaluate them
                return "<callable>"
            
            # Handle common Django field defaults
            if hasattr(value, '__name__'):
                return f"<function: {value.__name__}>"
                
            return force_str(value)
        except Exception:
            return str(value)
    
    @classmethod
    def get_serializable_default(cls, field):
        """
        Get a JSON-serializable representation of a field's default value.
        
        Args:
            field: Django model field
            
        Returns:
            Serializable default value or None
        """
        if not hasattr(field, 'default'):
            return None
            
        default = field.default
        
        # Handle Django's NOT_PROVIDED sentinel
        from django.db import models
        if default is models.NOT_PROVIDED:
            return None
            
        # Handle callable defaults
        if callable(default):
            return "<callable>"
            
        # Try to make it JSON serializable
        try:
            json.dumps(default)
            return default
        except (TypeError, ValueError):
            return str(default)


class GetIkshanaModelData(views.APIView):
    """
    API View to get metadata for a Django model.
    
    GET /api/explain/<model_name>/
    """
    
    def get(self, request, model_name):
        """
        Retrieve metadata for the specified model.
        
        Args:
            request: HTTP request object
            model_name: Name of the Django model
            
        Returns:
            Response containing model metadata
        """
        try:
            model_data = ModelProvider.get_ikshana_model_data(model_name)
            return Response(model_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Internal server error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 