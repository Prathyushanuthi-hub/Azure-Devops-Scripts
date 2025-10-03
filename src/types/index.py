"""
Type definitions for GitHub Organization Analysis
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

class Repository:
    def __init__(self, name, size, url, description):
        self.name = name
        self.size = size
        self.url = url
        self.description = description

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members

class Organization:
    def __init__(self, name, repositories, teams):
        self.name = name
        self.repositories = repositories
        self.teams = teams

@dataclass
class RepositoryDetails:
    """Repository details data class"""
    name: str
    full_name: str
    description: Optional[str]
    size: int
    language: Optional[str]
    default_branch: str
    private: bool
    fork: bool
    archived: bool
    disabled: bool
    html_url: str
    clone_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    stargazers_count: int
    watchers_count: int
    forks_count: int
    open_issues_count: int
    teams: List[Dict[str, Any]]
    collaborators: List[Dict[str, Any]]

@dataclass
class AnalysisResult:
    """Complete analysis result data class"""
    organization: Dict[str, Any]
    repositories: List[Dict[str, Any]]
    teams: List[Dict[str, Any]]
    members: List[Dict[str, Any]]
    analysis_timestamp: datetime
    total_size_kb: int
    languages_distribution: Dict[str, int]