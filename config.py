"""
Configuration module for AI Resume Analyzer

This module provides centralized configuration management for the Flask application,
including upload settings, security parameters, ATS scoring weights, and environment-specific settings.

Environment Variables:
    FLASK_ENV: Application environment (development/production)
    MAX_UPLOAD_SIZE: Maximum file upload size in MB (default: 16)
    UPLOAD_DIR: Directory for temporary file uploads (default: uploads)
    DEBUG: Enable Flask debug mode (default: False)
    ALLOWED_EXTENSIONS: Allowed file extensions for uploads (default: pdf,docx)
"""

import os
from typing import Set


class Config:
    """Base configuration class with shared settings."""
    
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # File upload settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', 16)) * 1024 * 1024  # 16MB default
    UPLOAD_FOLDER = os.getenv('UPLOAD_DIR', 'uploads')
    ALLOWED_EXTENSIONS: Set[str] = {'pdf', 'docx', 'doc', 'txt'}
    
    # ATS Scoring weights (must sum to 1.0)
    ATS_WEIGHTS = {
        'keyword_match': 0.30,      # 30% - Keyword alignment with JD
        'skills_alignment': 0.25,   # 25% - Technical skills match
        'seniority_match': 0.15,    # 15% - Experience level alignment
        'education_score': 0.10,    # 10% - Education credentials
        'experience_score': 0.10,   # 10% - Professional experience
        'formatting_score': 0.10    # 10% - Document formatting quality
    }
    
    # Skill taxonomy categories for better matching
    SKILL_CATEGORIES = {
        'programming_languages': ['python', 'javascript', 'java', 'c#', 'c++', 'ruby', 'php', 'go', 'rust'],
        'web_frameworks': ['react', 'angular', 'vue', 'flask', 'django', 'express', 'spring'],
        'databases': ['sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch'],
        'cloud_platforms': ['aws', 'azure', 'gcp', 'heroku', 'docker', 'kubernetes'],
        'devops_tools': ['jenkins', 'gitlab', 'github', 'git', 'terraform', 'ansible'],
        'soft_skills': ['leadership', 'communication', 'teamwork', 'problem-solving', 'project management']
    }
    
    # Seniority level keywords and minimum years
    SENIORITY_LEVELS = {
        'entry': {'keywords': ['junior', 'entry-level', 'graduate'], 'min_years': 0, 'max_years': 2},
        'mid': {'keywords': ['mid-level', 'intermediate', 'senior'], 'min_years': 2, 'max_years': 7},
        'senior': {'keywords': ['senior', 'lead', 'principal'], 'min_years': 7, 'max_years': 15},
        'executive': {'keywords': ['director', 'manager', 'vp', 'cto', 'cfo'], 'min_years': 10}
    }


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # Stricter limit in production


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    UPLOAD_FOLDER = '/tmp/test_uploads'


# Configuration factory
def get_config(env: str = None) -> Config:
    """
    Get configuration object based on environment.
    
    Args:
        env: Environment name ('development', 'production', 'testing')
        
    Returns:
        Appropriate Config class instance
        
    Raises:
        ValueError: If invalid environment specified
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    if env not in config_map:
        raise ValueError(f"Invalid environment: {env}. Must be one of {list(config_map.keys())}")
    
    return config_map[env]()
