#!/usr/bin/env python3
"""
Google Maps 集成 - 地理编码/路线/地点/地图

🆕 2026-04-08: 创建
- 地理编码 (地址→坐标)
- 逆地理编码 (坐标→地址)
- 地点搜索
- 路线规划
- 距离矩阵
- 静态地图
"""

import os
import sys
import json
import time
import requests
from typing import Dict, Any, List, Optional
from urllib.parse import quote

class GoogleMapsIntegration:
    """Google Maps 集成"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or self._load_api_key()
        self.base_url = "https://maps.googleapis.com/maps/api"
        self.config = self._load_config()
        
        # 代理配置 (海外 API 需要)
        self.proxy = os.environ.get('HTTP_PROXY', 'http://127.0.0.1:7890')
    
    def _load_api_key(self) -> Optional[str]:
        """从配置加载 API Key"""
        try:
            config_path = os.path.expanduser("~/.openclaw/workspace-taiyi/config/google-integration.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                maps_config = config.get('maps', {})
                if maps_config.get('enabled', False):
                    return maps_config.get('apiKey', '')
        except Exception as e:
            print(f"警告：无法加载配置 {e}")
        return None
    
    def _load_config(self) -> Dict:
        """加载配置"""
        try:
            config_path = os.path.expanduser("~/.openclaw/workspace-taiyi/config/google-integration.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """发送 API 请求"""
        if not self.api_key:
            return {
                'success': False,
                'error': 'API Key 未配置',
                'help': '请在 google-integration.json 中配置 maps.apiKey'
            }
        
        params['key'] = self.api_key
        
        url = f"{self.base_url}/{endpoint}/json"
        proxies = {'http': self.proxy, 'https': self.proxy}
        
        try:
            response = requests.get(url, params=params, proxies=proxies, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def geocode(self, address: str) -> Dict[str, Any]:
        """
        地理编码：地址→坐标
        
        Args:
            address: 地址
        
        Returns:
            坐标信息
        """
        result = self._make_request('geocode', {'address': address})
        
        if 'error' in result:
            return result
        
        if result.get('status') != 'OK':
            return {
                'success': False,
                'error': f"API 错误：{result.get('status')}",
                'error_message': result.get('error_message', '')
            }
        
        location = result['results'][0]['geometry']['location']
        
        return {
            'success': True,
            'address': result['results'][0]['formatted_address'],
            'latitude': location['lat'],
            'longitude': location['lng'],
            'place_id': result['results'][0].get('place_id'),
            'types': result['results'][0].get('types', []),
            'timestamp': time.time()
        }
    
    def reverse_geocode(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        逆地理编码：坐标→地址
        
        Args:
            lat: 纬度
            lng: 经度
        
        Returns:
            地址信息
        """
        result = self._make_request('geocode', {
            'latlng': f"{lat},{lng}"
        })
        
        if 'error' in result:
            return result
        
        if result.get('status') != 'OK':
            return {
                'success': False,
                'error': f"API 错误：{result.get('status')}",
                'error_message': result.get('error_message', '')
            }
        
        return {
            'success': True,
            'address': result['results'][0]['formatted_address'],
            'latitude': lat,
            'longitude': lng,
            'place_id': result['results'][0].get('place_id'),
            'address_components': result['results'][0].get('address_components', []),
            'timestamp': time.time()
        }
    
    def search_places(self, query: str, location: Optional[str] = None, 
                     radius: Optional[int] = None, type: Optional[str] = None) -> Dict[str, Any]:
        """
        地点搜索
        
        Args:
            query: 搜索关键词
            location: 位置 (lat,lng)
            radius: 半径 (米)
            type: 类型 (如 restaurant, cafe, bank 等)
        
        Returns:
            地点列表
        """
        params = {'query': query}
        
        if location:
            params['location'] = location
        if radius:
            params['radius'] = radius
        if type:
            params['type'] = type
        
        result = self._make_request('place/textsearch', params)
        
        if 'error' in result:
            return result
        
        if result.get('status') != 'OK':
            return {
                'success': False,
                'error': f"API 错误：{result.get('status')}",
                'error_message': result.get('error_message', '')
            }
        
        places = []
        for place in result.get('results', []):
            places.append({
                'name': place.get('name', ''),
                'formatted_address': place.get('formatted_address', ''),
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'place_id': place.get('place_id'),
                'rating': place.get('rating'),
                'types': place.get('types', [])
            })
        
        return {
            'success': True,
            'query': query,
            'count': len(places),
            'places': places,
            'timestamp': time.time()
        }
    
    def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """
        获取地点详情
        
        Args:
            place_id: 地点 ID
        
        Returns:
            地点详情
        """
        result = self._make_request('place/details', {
            'place_id': place_id,
            'fields': 'name,formatted_address,geometry,rating,opening_hours,formatted_phone_number,website,reviews'
        })
        
        if 'error' in result:
            return result
        
        if result.get('status') != 'OK':
            return {
                'success': False,
                'error': f"API 错误：{result.get('status')}",
                'error_message': result.get('error_message', '')
            }
        
        details = result.get('result', {})
        
        return {
            'success': True,
            'name': details.get('name', ''),
            'formatted_address': details.get('formatted_address', ''),
            'latitude': details.get('geometry', {}).get('location', {}).get('lat'),
            'longitude': details.get('geometry', {}).get('location', {}).get('lng'),
            'rating': details.get('rating'),
            'user_ratings_total': details.get('user_ratings_total'),
            'opening_hours': details.get('opening_hours'),
            'phone': details.get('formatted_phone_number'),
            'website': details.get('website'),
            'reviews': details.get('reviews', [])[:5],  # 最多 5 条评价
            'timestamp': time.time()
        }
    
    def directions(self, origin: str, destination: str, 
                  mode: str = 'driving', alternatives: bool = False) -> Dict[str, Any]:
        """
        路线规划
        
        Args:
            origin: 起点 (地址或坐标)
            destination: 终点 (地址或坐标)
            mode: 交通方式 (driving, walking, bicycling, transit)
            alternatives: 是否返回备选路线
        
        Returns:
            路线信息
        """
        params = {
            'origin': origin,
            'destination': destination,
            'mode': mode,
            'alternatives': 'true' if alternatives else 'false'
        }
        
        result = self._make_request('directions', params)
        
        if 'error' in result:
            return result
        
        if result.get('status') != 'OK':
            return {
                'success': False,
                'error': f"API 错误：{result.get('status')}",
                'error_message': result.get('error_message', '')
            }
        
        routes = []
        for route in result.get('routes', []):
            leg = route['legs'][0]
            routes.append({
                'summary': route.get('summary', ''),
                'distance': leg['distance']['text'],
                'distance_meters': leg['distance']['value'],
                'duration': leg['duration']['text'],
                'duration_seconds': leg['duration']['value'],
                'start_address': leg['start_address'],
                'end_address': leg['end_address'],
                'steps': self._simplify_steps(leg.get('steps', []))
            })
        
        return {
            'success': True,
            'origin': origin,
            'destination': destination,
            'mode': mode,
            'route_count': len(routes),
            'routes': routes,
            'timestamp': time.time()
        }
    
    def _simplify_steps(self, steps: List[Dict]) -> List[Dict]:
        """简化路线步骤"""
        simplified = []
        for step in steps[:10]:  # 最多 10 步
            simplified.append({
                'instruction': step['html_instructions'].replace('<b>', '').replace('</b>', ''),
                'distance': step['distance']['text'],
                'duration': step['duration']['text']
            })
        return simplified
    
    def distance_matrix(self, origins: List[str], destinations: List[str], 
                       mode: str = 'driving') -> Dict[str, Any]:
        """
        距离矩阵
        
        Args:
            origins: 起点列表
            destinations: 终点列表
            mode: 交通方式
        
        Returns:
            距离矩阵
        """
        params = {
            'origins': '|'.join(origins),
            'destinations': '|'.join(destinations),
            'mode': mode
        }
        
        result = self._make_request('distancematrix', params)
        
        if 'error' in result:
            return result
        
        if result.get('status') != 'OK':
            return {
                'success': False,
                'error': f"API 错误：{result.get('status')}",
                'error_message': result.get('error_message', '')
            }
        
        matrix = []
        for i, row in enumerate(result.get('rows', [])):
            row_data = {'origin': origins[i], 'destinations': []}
            for j, element in enumerate(row.get('elements', [])):
                row_data['destinations'].append({
                    'destination': destinations[j],
                    'status': element.get('status'),
                    'distance': element.get('distance', {}).get('text'),
                    'duration': element.get('duration', {}).get('text')
                })
            matrix.append(row_data)
        
        return {
            'success': True,
            'mode': mode,
            'matrix': matrix,
            'timestamp': time.time()
        }
    
    def static_map(self, center: str, zoom: int = 12, size: str = '600x400', 
                  maptype: str = 'roadmap', markers: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        静态地图
        
        Args:
            center: 中心点 (地址或坐标)
            zoom: 缩放级别 (1-20)
            size: 图片尺寸 (如 600x400)
            maptype: 地图类型 (roadmap, satellite, terrain, hybrid)
            markers: 标记点列表
        
        Returns:
            地图 URL 和元数据
        """
        params = {
            'center': center,
            'zoom': zoom,
            'size': size,
            'maptype': maptype,
            'key': self.api_key or ''
        }
        
        if markers:
            params['markers'] = '|'.join(markers)
        
        # 构建 URL (不需要请求，直接返回)
        base = f"{self.base_url}/staticmap"
        url_parts = [f"{k}={quote(str(v))}" for k, v in params.items()]
        map_url = f"{base}?{'&'.join(url_parts)}"
        
        return {
            'success': True,
            'url': map_url,
            'center': center,
            'zoom': zoom,
            'size': size,
            'maptype': maptype,
            'markers': markers,
            'timestamp': time.time()
        }


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Google Maps 集成')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # geocode
    p_geocode = subparsers.add_parser('geocode', help='地址→坐标')
    p_geocode.add_argument('address', help='地址')
    
    # reverse-geocode
    p_reverse = subparsers.add_parser('reverse-geocode', help='坐标→地址')
    p_reverse.add_argument('lat', type=float, help='纬度')
    p_reverse.add_argument('lng', type=float, help='经度')
    
    # search
    p_search = subparsers.add_parser('search', help='地点搜索')
    p_search.add_argument('query', help='搜索词')
    p_search.add_argument('--location', '-l', help='位置 (lat,lng)')
    p_search.add_argument('--radius', '-r', type=int, help='半径 (米)')
    p_search.add_argument('--type', '-t', help='类型')
    
    # directions
    p_directions = subparsers.add_parser('directions', help='路线规划')
    p_directions.add_argument('origin', help='起点')
    p_directions.add_argument('destination', help='终点')
    p_directions.add_argument('--mode', '-m', default='driving', 
                             choices=['driving', 'walking', 'bicycling', 'transit'])
    p_directions.add_argument('--alternatives', '-a', action='store_true')
    
    # distance
    p_distance = subparsers.add_parser('distance', help='距离矩阵')
    p_distance.add_argument('origins', nargs='+', help='起点')
    p_distance.add_argument('--destinations', '-d', nargs='+', required=True, help='终点')
    p_distance.add_argument('--mode', '-m', default='driving')
    
    # static-map
    p_static = subparsers.add_parser('static-map', help='静态地图')
    p_static.add_argument('--center', '-c', required=True, help='中心点')
    p_static.add_argument('--zoom', '-z', type=int, default=12, help='缩放')
    p_static.add_argument('--size', '-s', default='600x400', help='尺寸')
    p_static.add_argument('--maptype', '-t', default='roadmap')
    p_static.add_argument('--markers', '-m', nargs='+', help='标记')
    
    args = parser.parse_args()
    
    maps = GoogleMapsIntegration()
    
    if args.command == 'geocode':
        result = maps.geocode(args.address)
    
    elif args.command == 'reverse-geocode':
        result = maps.reverse_geocode(args.lat, args.lng)
    
    elif args.command == 'search':
        result = maps.search_places(args.query, args.location, args.radius, args.type)
    
    elif args.command == 'directions':
        result = maps.directions(args.origin, args.destination, args.mode, args.alternatives)
    
    elif args.command == 'distance':
        result = maps.distance_matrix(args.origins, args.destinations, args.mode)
    
    elif args.command == 'static-map':
        result = maps.static_map(args.center, args.zoom, args.size, args.maptype, args.markers)
    
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
