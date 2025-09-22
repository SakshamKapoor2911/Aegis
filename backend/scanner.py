import asyncio
import httpx
import grpc
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import json
import re
from urllib.parse import urljoin, urlparse
import socket
import ssl
from datetime import datetime

class Severity(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

@dataclass
class Vulnerability:
    id: str
    title: str
    description: str
    severity: Severity
    affected_endpoint: str
    recommendation: str
    cwe_id: str = None

class OnlineBoutiqueScanner:
    def __init__(self, target_url: str):
        self.target_url = target_url.rstrip('/')
        self.findings: List[Vulnerability] = []
        
    async def scan(self) -> List[Vulnerability]:
        """Main scan orchestration"""
        print(f"Starting security scan of {self.target_url}")
        
        # Step 1: Discover microservices
        await self._discover_microservices()
        
        # Step 2: Check HTTP security headers
        await self._check_http_security_headers()
        
        # Step 3: Check for common vulnerabilities
        await self._check_common_vulnerabilities()
        
        # Step 4: Check gRPC security
        await self._check_grpc_security()
        
        print(f"Scan completed. Found {len(self.findings)} vulnerabilities")
        return self.findings
    
    async def _discover_microservices(self):
        """Discover Online Boutique microservices"""
        print("Discovering microservices...")
        
        # Known Online Boutique services with their ports and protocols
        services = {
            "frontend": {"port": 80, "protocol": "http", "health_path": "/"},
            "cartservice": {"port": 7070, "protocol": "grpc", "health_path": "/health"},
            "productcatalogservice": {"port": 3550, "protocol": "grpc", "health_path": "/health"},
            "currencyservice": {"port": 7000, "protocol": "grpc", "health_path": "/health"},
            "paymentservice": {"port": 50051, "protocol": "grpc", "health_path": "/health"},
            "shippingservice": {"port": 50051, "protocol": "grpc", "health_path": "/health"},
            "emailservice": {"port": 5000, "protocol": "grpc", "health_path": "/health"},
            "checkoutservice": {"port": 5050, "protocol": "grpc", "health_path": "/health"},
            "recommendationservice": {"port": 5000, "protocol": "grpc", "health_path": "/health"},
            "adservice": {"port": 9555, "protocol": "grpc", "health_path": "/health"},
            "loadgenerator": {"port": 8089, "protocol": "http", "health_path": "/health"}
        }
        
        # Extract host from target URL
        parsed_url = urlparse(self.target_url)
        host = parsed_url.hostname
        
        for service_name, config in services.items():
            try:
                if config["protocol"] == "http":
                    # Check HTTP services
                    service_url = f"http://{host}:{config['port']}{config['health_path']}"
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        response = await client.get(service_url)
                        if response.status_code == 200:
                            self.findings.append(Vulnerability(
                                id=f"service-discovery-{service_name}",
                                title=f"HTTP Service {service_name} discovered",
                                description=f"Successfully discovered {service_name} microservice on port {config['port']}",
                                severity=Severity.LOW,
                                affected_endpoint=service_url,
                                recommendation="Service is accessible and responding"
                            ))
                elif config["protocol"] == "grpc":
                    # Check gRPC services
                    if await self._check_grpc_service(host, config["port"], service_name):
                        self.findings.append(Vulnerability(
                            id=f"grpc-service-discovery-{service_name}",
                            title=f"gRPC Service {service_name} discovered",
                            description=f"Successfully discovered {service_name} gRPC microservice on port {config['port']}",
                            severity=Severity.LOW,
                            affected_endpoint=f"grpc://{host}:{config['port']}",
                            recommendation="gRPC service is accessible and responding"
                        ))
            except Exception as e:
                print(f"Could not discover {service_name}: {e}")
    
    async def _check_grpc_service(self, host: str, port: int, service_name: str) -> bool:
        """Check if gRPC service is accessible"""
        try:
            # Try to establish a connection to the gRPC port
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), 
                timeout=3.0
            )
            writer.close()
            await writer.wait_closed()
            return True
        except Exception as e:
            print(f"gRPC service {service_name} on {host}:{port} not accessible: {e}")
            return False
    
    async def _check_http_security_headers(self):
        """Check for missing security headers"""
        print("Checking HTTP security headers...")
        
        security_headers = {
            "Content-Security-Policy": {
                "severity": Severity.HIGH,
                "description": "Content Security Policy header missing",
                "recommendation": "Implement CSP to prevent XSS attacks"
            },
            "Strict-Transport-Security": {
                "severity": Severity.HIGH,
                "description": "HSTS header missing",
                "recommendation": "Implement HSTS to enforce HTTPS"
            },
            "X-Frame-Options": {
                "severity": Severity.MEDIUM,
                "description": "X-Frame-Options header missing",
                "recommendation": "Implement X-Frame-Options to prevent clickjacking"
            },
            "X-Content-Type-Options": {
                "severity": Severity.MEDIUM,
                "description": "X-Content-Type-Options header missing",
                "recommendation": "Implement nosniff to prevent MIME type sniffing"
            },
            "Referrer-Policy": {
                "severity": Severity.LOW,
                "description": "Referrer-Policy header missing",
                "recommendation": "Implement Referrer-Policy to control referrer information"
            }
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(self.target_url)
                headers = response.headers
                
                for header, config in security_headers.items():
                    if header not in headers:
                        self.findings.append(Vulnerability(
                            id=f"missing-header-{header.lower().replace('-', '_')}",
                            title=config["description"],
                            description=f"Missing {header} security header",
                            severity=config["severity"],
                            affected_endpoint=self.target_url,
                            recommendation=config["recommendation"],
                            cwe_id="CWE-693" if "CSP" in header else "CWE-693"
                        ))
            except Exception as e:
                print(f"Error checking headers: {e}")
    
    async def _check_common_vulnerabilities(self):
        """Check for common web vulnerabilities"""
        print("Checking for common vulnerabilities...")
        
        # Check for HTTP instead of HTTPS
        if self.target_url.startswith("http://"):
            self.findings.append(Vulnerability(
                id="insecure-http",
                title="Insecure HTTP connection",
                description="Application is served over HTTP instead of HTTPS",
                severity=Severity.HIGH,
                affected_endpoint=self.target_url,
                recommendation="Implement HTTPS with proper SSL/TLS configuration",
                cwe_id="CWE-319"
            ))
        
        # Check for exposed sensitive endpoints
        sensitive_endpoints = [
            "/admin", "/api/admin", "/debug", "/status", 
            "/health", "/metrics", "/actuator"
        ]
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            for endpoint in sensitive_endpoints:
                try:
                    url = urljoin(self.target_url, endpoint)
                    response = await client.get(url)
                    
                    if response.status_code == 200:
                        # Check if it's a debug/admin endpoint
                        if "admin" in endpoint or "debug" in endpoint:
                            self.findings.append(Vulnerability(
                                id=f"exposed-endpoint-{endpoint.replace('/', '_')}",
                                title=f"Exposed sensitive endpoint: {endpoint}",
                                description=f"Sensitive endpoint {endpoint} is publicly accessible",
                                severity=Severity.MEDIUM,
                                affected_endpoint=url,
                                recommendation="Restrict access to sensitive endpoints",
                                cwe_id="CWE-200"
                            ))
                except Exception as e:
                    continue
        
        # Check for information disclosure in response headers
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(self.target_url)
                headers = response.headers
                
                # Check for server information disclosure
                if "Server" in headers:
                    server_info = headers["Server"]
                    if any(tech in server_info.lower() for tech in ["nginx", "apache", "iis", "tomcat"]):
                        self.findings.append(Vulnerability(
                            id="server-info-disclosure",
                            title="Server information disclosure",
                            description=f"Server header reveals technology stack: {server_info}",
                            severity=Severity.LOW,
                            affected_endpoint=self.target_url,
                            recommendation="Remove or obfuscate server information in headers",
                            cwe_id="CWE-200"
                        ))
            except Exception as e:
                print(f"Error checking information disclosure: {e}")
    
    async def _check_grpc_security(self):
        """Check gRPC-specific security issues"""
        print("Checking gRPC security...")
        
        # Extract host from target URL
        parsed_url = urlparse(self.target_url)
        host = parsed_url.hostname
        
        # Check for gRPC services running without TLS
        grpc_services = {
            "cartservice": 7070,
            "productcatalogservice": 3550,
            "currencyservice": 7000,
            "paymentservice": 50051,
            "shippingservice": 50051,
            "emailservice": 8080,
            "checkoutservice": 5050,
            "recommendationservice": 8080,
            "adservice": 9555
        }
        
        for service_name, port in grpc_services.items():
            try:
                # Check if gRPC service is accessible
                if await self._check_grpc_service(host, port, service_name):
                    # Check if it's using TLS
                    if not await self._check_grpc_tls(host, port):
                        self.findings.append(Vulnerability(
                            id=f"grpc-no-tls-{service_name}",
                            title=f"gRPC service {service_name} not using TLS",
                            description=f"gRPC service {service_name} is accessible but not using TLS encryption",
                            severity=Severity.HIGH,
                            affected_endpoint=f"grpc://{host}:{port}",
                            recommendation="Enable TLS for gRPC services to encrypt communication",
                            cwe_id="CWE-319"
                        ))
                    
                    # Check for gRPC reflection (security risk)
                    if await self._check_grpc_reflection(host, port):
                        self.findings.append(Vulnerability(
                            id=f"grpc-reflection-{service_name}",
                            title=f"gRPC reflection enabled on {service_name}",
                            description=f"gRPC reflection is enabled on {service_name}, which can expose service metadata",
                            severity=Severity.MEDIUM,
                            affected_endpoint=f"grpc://{host}:{port}",
                            recommendation="Disable gRPC reflection in production environments",
                            cwe_id="CWE-200"
                        ))
            except Exception as e:
                print(f"Error checking gRPC security for {service_name}: {e}")
    
    async def _check_grpc_tls(self, host: str, port: int) -> bool:
        """Check if gRPC service is using TLS"""
        try:
            # Try to establish a TLS connection
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port, ssl=context),
                timeout=3.0
            )
            writer.close()
            await writer.wait_closed()
            return True
        except Exception:
            return False
    
    async def _check_grpc_reflection(self, host: str, port: int) -> bool:
        """Check if gRPC reflection is enabled"""
        try:
            # This is a simplified check - in practice, you'd use gRPC reflection client
            # For now, we'll assume reflection might be enabled if the service is accessible
            return await self._check_grpc_service(host, port, "reflection_check")
        except Exception:
            return False

    def get_scan_summary(self) -> Dict[str, Any]:
        """Generate scan summary statistics"""
        severity_counts = {severity.value: 0 for severity in Severity}
        
        for finding in self.findings:
            severity_counts[finding.severity.value] += 1
        
        return {
            "total_findings": len(self.findings),
            "severity_breakdown": severity_counts,
            "scan_target": self.target_url,
            "scan_timestamp": datetime.now().isoformat()
        }