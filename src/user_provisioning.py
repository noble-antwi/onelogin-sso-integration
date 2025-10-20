"""
User Provisioning Automation for OneLogin SSO Integration

This module handles:
- Automated user provisioning workflows
- Attribute mapping between systems
- Bulk user creation and management
- Integration with multiple applications
"""

import logging
import json
import csv
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
from pathlib import Path

from config.settings import config
from src.onelogin_connector import OneLoginConnector
from src.saml_handler import SAMLHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserProvisioningEngine:
    """Automated user provisioning and management system"""
    
    def __init__(self):
        """Initialize the provisioning engine"""
        self.config = config
        self.onelogin = OneLoginConnector(config)
        self.saml_handler = SAMLHandler(config)
        
        # Statistics tracking
        self.stats = {
            "total_processed": 0,
            "successful_provisions": 0,
            "failed_provisions": 0,
            "start_time": None,
            "end_time": None
        }
        
        logger.info("User Provisioning Engine initialized")
    
    def generate_test_users(self, count: int = 100) -> List[Dict[str, str]]:
        """
        Generate test user data for demonstration
        
        Args:
            count: Number of test users to generate
            
        Returns:
            List of user dictionaries
        """
        departments = ["IT", "HR", "Finance", "Marketing", "Operations", "Sales"]
        roles = ["Administrator", "Manager", "Analyst", "Specialist", "Coordinator"]
        
        users = []
        for i in range(1, count + 1):
            user = {
                "email": f"testuser{i:03d}@example.com",
                "firstname": f"Test{i:03d}",
                "lastname": "User",
                "department": departments[i % len(departments)],
                "role": roles[i % len(roles)],
                "employee_id": f"EMP{i:04d}",
                "status": "active"
            }
            users.append(user)
        
        logger.info(f"Generated {count} test users")
        return users
    
    def map_user_attributes(self, user_data: Dict[str, str]) -> Dict[str, str]:
        """
        Map user attributes between different systems
        
        Args:
            user_data: Raw user data
            
        Returns:
            Mapped user attributes for OneLogin
        """
        mapped_attributes = {
            "email": user_data.get("email", ""),
            "firstname": user_data.get("firstname", ""),
            "lastname": user_data.get("lastname", ""),
            "username": user_data.get("email", "").split("@")[0],
            "title": user_data.get("role", ""),
            "department": user_data.get("department", ""),
            "employee_id": user_data.get("employee_id", ""),
            "status": user_data.get("status", "active")
        }
        
        # Add computed fields
        mapped_attributes["display_name"] = f"{mapped_attributes['firstname']} {mapped_attributes['lastname']}"
        mapped_attributes["created_at"] = datetime.utcnow().isoformat()
        
        return mapped_attributes
    
    def provision_single_user(self, user_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Provision a single user through the complete workflow
        
        Args:
            user_data: User information
            
        Returns:
            Provisioning result
        """
        try:
            # Map attributes
            mapped_user = self.map_user_attributes(user_data)
            
            # Create user in OneLogin
            onelogin_result = self.onelogin.create_user(mapped_user)
            
            if onelogin_result.get("success"):
                # Create SAML session for the user
                session_id = self.saml_handler.create_user_session(mapped_user)
                
                result = {
                    "success": True,
                    "user_email": mapped_user["email"],
                    "onelogin_id": onelogin_result.get("user_id"),
                    "session_id": session_id,
                    "attributes": mapped_user,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                self.stats["successful_provisions"] += 1
                logger.info(f"Successfully provisioned user: {mapped_user['email']}")
                return result
            else:
                self.stats["failed_provisions"] += 1
                return {
                    "success": False,
                    "error": "OneLogin user creation failed",
                    "user_email": mapped_user["email"]
                }
                
        except Exception as e:
            self.stats["failed_provisions"] += 1
            logger.error(f"Error provisioning user {user_data.get('email', 'unknown')}: {e}")
            return {
                "success": False,
                "error": str(e),
                "user_email": user_data.get("email", "unknown")
            }
        finally:
            self.stats["total_processed"] += 1
    
    def provision_users_bulk(self, users_list: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Provision multiple users in bulk with comprehensive reporting
        
        Args:
            users_list: List of user dictionaries
            
        Returns:
            Bulk provisioning results with metrics
        """
        self.stats["start_time"] = datetime.utcnow()
        
        results = {
            "total_users": len(users_list),
            "successful": 0,
            "failed": 0,
            "results": [],
            "errors": [],
            "performance_metrics": {}
        }
        
        logger.info(f"Starting bulk provisioning for {len(users_list)} users")
        
        for user_data in users_list:
            result = self.provision_single_user(user_data)
            results["results"].append(result)
            
            if result.get("success"):
                results["successful"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(result.get("error", "Unknown error"))
        
        self.stats["end_time"] = datetime.utcnow()
        
        # Calculate performance metrics
        processing_time = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
        traditional_time_estimate = len(users_list) * 4 * 60  # 4 minutes per user in seconds
        
        results["performance_metrics"] = {
            "processing_time_seconds": round(processing_time, 2),
            "processing_time_minutes": round(processing_time / 60, 2),
            "traditional_time_minutes": traditional_time_estimate / 60,
            "time_saved_minutes": round((traditional_time_estimate - processing_time) / 60, 2),
            "efficiency_gain_percentage": round(((traditional_time_estimate - processing_time) / traditional_time_estimate) * 100, 1),
            "users_per_minute": round(len(users_list) / (processing_time / 60), 2)
        }
        
        logger.info(f"Bulk provisioning complete: {results['successful']}/{results['total_users']} users")
        return results
    
    def provision_applications(self, user_session_id: str) -> Dict[str, bool]:
        """
        Provision user access to configured applications
        
        Args:
            user_session_id: User session identifier
            
        Returns:
            Application provisioning results
        """
        applications = self.config.get_enabled_applications()
        app_results = {}
        
        for app_key, app_config in applications.items():
            try:
                # Simulate application provisioning
                app_results[app_config["name"]] = True
                logger.info(f"Provisioned access to {app_config['name']} for session {user_session_id}")
            except Exception as e:
                app_results[app_config["name"]] = False
                logger.error(f"Failed to provision {app_config['name']}: {e}")
        
        return app_results
    
    def export_provisioning_report(self, results: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Export provisioning results to a detailed report
        
        Args:
            results: Provisioning results dictionary
            filename: Optional custom filename
            
        Returns:
            Report file path
        """
        if not filename:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"provisioning_report_{timestamp}.json"
        
        # Ensure logs directory exists
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        report_path = logs_dir / filename
        
        # Create comprehensive report
        report = {
            "summary": {
                "total_users": results.get("total_users", 0),
                "successful": results.get("successful", 0),
                "failed": results.get("failed", 0),
                "success_rate_percentage": round((results.get("successful", 0) / max(results.get("total_users", 1), 1)) * 100, 2)
            },
            "performance_metrics": results.get("performance_metrics", {}),
            "detailed_results": results.get("results", []),
            "errors": results.get("errors", []),
            "generated_at": datetime.utcnow().isoformat(),
            "system_stats": self.get_system_stats()
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Provisioning report saved to {report_path}")
        return str(report_path)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive system statistics
        
        Returns:
            System statistics dictionary
        """
        onelogin_stats = self.onelogin.get_api_stats()
        saml_stats = self.saml_handler.get_session_stats()
        
        # Convert datetime objects to strings for JSON serialization
        stats_copy = self.stats.copy()
        if stats_copy.get('start_time'):
            stats_copy['start_time'] = stats_copy['start_time'].isoformat()
        if stats_copy.get('end_time'):
            stats_copy['end_time'] = stats_copy['end_time'].isoformat()
        
        return {
            "provisioning_engine": stats_copy,
            "onelogin_connector": onelogin_stats,
            "saml_handler": saml_stats,
            "configuration": {
                "enabled_applications": len(self.config.get_enabled_applications()),
                "configured": self.config.is_configured()
            }
        }
    
    def reset_stats(self):
        """Reset statistics counters"""
        self.stats = {
            "total_processed": 0,
            "successful_provisions": 0,
            "failed_provisions": 0,
            "start_time": None,
            "end_time": None
        }
        logger.info("Statistics reset")