#!/usr/bin/env python3

# -*- coding: utf-8 -*-



"""
太一旅行 - 供应商注册/审核管理
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from src.provider.models import Provider, ProviderType, ProviderStatus


class ProviderRegistry:
    """供应商注册中心"""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent.parent.parent / "data" / "providers"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._db: Dict[str, List[Provider]] = {}
        self._load_all()

    def _get_file(self, ptype: str) -> Path:
        return self.data_dir / f"{ptype}s.json"

    def _load_all(self) -> None:
        for ptype in ProviderType:
            file = self._get_file(ptype.value)
            if file.exists():
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._db[ptype.value] = [Provider.from_dict(d) for d in data]
            else:
                self._db[ptype.value] = []

    def _save(self, ptype: str) -> None:
        file = self._get_file(ptype)
        with open(file, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self._db.get(ptype, [])], f, indent=2, ensure_ascii=False)

    def register(self, provider: Provider) -> Provider:
        """注册供应商"""
        ptype = provider.provider_type.value
        if ptype not in self._db:
            self._db[ptype] = []
        self._db[ptype].append(provider)
        self._save(ptype)
        return provider

    def list_providers(
        self, ptype: ProviderType, location: Optional[str] = None, status: Optional[ProviderStatus] = None
    ) -> List[Provider]:
        """列出供应商"""
        providers = self._db.get(ptype.value, [])
        if location:
            providers = [p for p in providers if p.location == location]
        if status:
            providers = [p for p in providers if p.status == status]
        return providers

    def approve(self, ptype: ProviderType, provider_id: str) -> bool:
        """审核通过"""
        providers = self._db.get(ptype.value, [])
        for p in providers:
            if p.id == provider_id:
                p.status = ProviderStatus.APPROVED
                p.approved_at = datetime.now().isoformat()
                self._save(ptype.value)
                return True
        return False

    def search(self, ptype: ProviderType, **kwargs) -> List[Provider]:
        """搜索已审核供应商"""
        providers = self.list_providers(ptype, status=ProviderStatus.APPROVED)
        for key, value in kwargs.items():
            if value:
                providers = [p for p in providers if getattr(p, key, None) == value]
        providers.sort(key=lambda x: x.rating, reverse=True)
        return providers[:10]








---

> **太一美学 · 品质保证**
> 美学过滤器自动处理 · 2026-04-25 18:48