# -*- coding: utf-8 -*-
"""
Manifest parser
"""
import json
import xml.etree.cElementTree as ET

class ManifestParser(object):
    """
    Recalbox XML manifest parser
    """
    def __init__(self, filepath):
        self.filepath = filepath
    
    def get_system_extensions(self, node):
        if node.find("extensions") is None:
            return []
        return [item.text for item in node.find("extensions").findall("extension")]
    
    def get_system_download_links(self, node):
        if node.find("download_links") is None:
            return []
        return [item.text for item in node.find("download_links").findall("link")]
    
    def get_system_bios(self, node):
        if node.find("bios") is None:
            return []
        return [(item.get('md5', ''), item.text) for item in node.find("bios").findall("file")]
    
    def get_system_extra_comments(self, node):
        if node.find("extra_comments") is None:
            return []
        return [item.text for item in node.find("extra_comments").findall("comment")]
    
    def read(self):
        """
        Return the manifest as a Python dictionnary
        """
        manifest = {}
        
        tree = ET.parse(self.filepath)
        
        root = tree.getroot()

        for node in root:
            system_key = node.get('key')
            manifest[system_key] = {
                'name': node.get('name'),
                'extensions': self.get_system_extensions(node),
                'download_links': self.get_system_download_links(node),
                'bios': self.get_system_bios(node),
                'extra_comments': self.get_system_extra_comments(node),
            }
        
        return manifest
    
    def json(self):
        """
        Return the manifest as a JSON string
        """
        return json.dumps(self.read(), indent=4)
