"""CLI Toolkit - Unified command-line interface toolkit"""

from .cloud import AWSClient, AzureClient, GCPClient
from .devops import DockerClient, K8sClient
from .wrappers import GeminiClient, JimengClient


class CLIToolkit:
    """CLI 工具集统一入口"""
    
    def __init__(self):
        # Cloud services
        self.cloud = type('CloudModule', (), {
            'aws': AWSClient(),
            'azure': AzureClient(),
            'gcp': GCPClient()
        })()
        
        # DevOps tools
        self.devops = type('DevOpsModule', (), {
            'docker': DockerClient(),
            'k8s': K8sClient()
        })()
        
        # CLI wrappers
        self.wrappers = type('WrappersModule', (), {
            'gemini': GeminiClient(),
            'jimeng': JimengClient()
        })()


__all__ = [
    'CLIToolkit',
    'AWSClient', 'AzureClient', 'GCPClient',
    'DockerClient', 'K8sClient',
    'GeminiClient', 'JimengClient'
]
