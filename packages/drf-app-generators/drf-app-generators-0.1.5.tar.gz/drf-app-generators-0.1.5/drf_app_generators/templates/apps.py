__all__ = ['APP_VIEW']

APP_VIEW = """from drf_core import apps


class {{ app_name|capfirst }}Config(apps.BaseConfig):
    \"\"\"
    {{ app_name|capfirst }} Configuration
    \"\"\"
    name = '{{ app_name }}'
"""
