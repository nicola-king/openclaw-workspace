{
  "schema_version": "1.0",
  "description": "产品品类 → 终端买家类型自动匹配表",
  "updated": "2026-05-20",
  "rule": "默认搜索终端买家，除非用户明确要求搜供应商",

  "mappings": [
    {
      "product": "钢结构折叠集成房屋",
      "aliases": ["钢结构", "折叠房屋", "集成房屋", "预制房屋", "模块化建筑", "prefab house", "steel structure", "foldable house", "modular building"],
      "hs_code": ["7308.90", "9406.10"],
      "end_buyers": [
        {"type": "矿业公司", "priority": "P0", "reason": "澳洲矿业营地最大需求方，矿工营房持续采购"},
        {"type": "酒店集团/度假村", "priority": "P0", "reason": "模块化酒店已成趋势，Hilton已建首个"},
        {"type": "政府/住房署", "priority": "P0", "reason": "保障房+应急住房+国防采购"},
        {"type": "地产开发商", "priority": "P1", "reason": "住宅/商业开发项目"},
        {"type": "个人终端", "priority": "P2", "reason": "自建房/祖母房/度假屋"}
      ],
      "search_keywords": [
        "mining camp accommodation procurement",
        "hotel modular construction development",
        "government housing prefab tender",
        "property developer modular building"
      ]
    },
    {
      "product": "变压器",
      "aliases": ["transformer", "power transformer", "变电站", "电力变压器"],
      "hs_code": ["8504.21", "8504.22", "8504.23"],
      "end_buyers": [
        {"type": "电力公司/电网运营商", "priority": "P0", "reason": "电网升级+新能源并网最大需求"},
        {"type": "矿业公司", "priority": "P0", "reason": "矿区配电+远程供电"},
        {"type": "政府/公共事业", "priority": "P1", "reason": "基建招标+农村电网"},
        {"type": "工业园/大型工厂", "priority": "P1", "reason": "工厂配电+扩容"},
        {"type": "EPC总包商", "priority": "P1", "reason": "项目级采购"}
      ],
      "search_keywords": [
        "power utility procurement transformer tender",
        "mining electrical equipment supplier registration",
        "government grid upgrade tender"
      ]
    },
    {
      "product": "移动电源",
      "aliases": ["power bank", "portable charger", "便携电源", "充电宝", "储能电源"],
      "hs_code": ["8507.60", "8507.80"],
      "end_buyers": [
        {"type": "零售商/电商平台", "priority": "P0", "reason": "B2C销售主渠道"},
        {"type": "批发商/进口商", "priority": "P0", "reason": "B2B批量采购"},
        {"type": "政府/应急部门", "priority": "P1", "reason": "应急保障+灾备采购"},
        {"type": "军队/警察", "priority": "P1", "reason": "野外电源需求"},
        {"type": "户外品牌/连锁店", "priority": "P2", "reason": "运动户外渠道"}
      ],
      "search_keywords": [
        "power bank wholesale distributor Australia",
        "portable charger importer buyer",
        "emergency power supply government procurement"
      ]
    },
    {
      "product": "通用发动机",
      "aliases": ["engine", "diesel engine", "gasoline engine", "发电机", "引擎"],
      "hs_code": ["8408.20", "8409.91", "8502.11"],
      "end_buyers": [
        {"type": "农机/工程机械制造商", "priority": "P0", "reason": "OEM配套需求"},
        {"type": "矿业公司", "priority": "P0", "reason": "矿区发电+设备动力"},
        {"type": "农业/养殖业", "priority": "P1", "reason": "灌溉+发电+设备"},
        {"type": "船舶/渔业", "priority": "P1", "reason": "船用发动机"},
        {"type": "政府/基建", "priority": "P1", "reason": "应急发电+基建设备"}
      ],
      "search_keywords": [
        "diesel engine distributor Australia",
        "mining generator procurement",
        "agricultural engine buyer"
      ]
    }
  ],

  "country_matrix": {
    "australia": {
      "label": "🇦🇺 澳大利亚",
      "procurement_platforms": ["austender.gov.au", "tenders.nsw.gov.au", "tenders.vic.gov.au", "tenders.wa.gov.au", "qtenders.qld.gov.au"],
      "certifications": ["NCC", "CodeMark"],
      "trade_agreement": "中澳FTA零关税"
    },
    "new_zealand": {
      "label": "🇳🇿 新西兰",
      "procurement_platforms": ["gets.govt.nz", "tenderlink.com/kaingaora"],
      "certifications": ["NZBC", "NZ53604抗震"],
      "trade_agreement": "中新FTA"
    },
    "ukraine": {
      "label": "🇺🇦 乌克兰",
      "procurement_platforms": ["prozorro.gov.ua"],
      "certifications": ["UkrSEPRO"],
      "note": "战后重建市场，平台B2B为主Prom.ua"
    },
    "poland": {
      "label": "🇵🇱 波兰",
      "procurement_platforms": ["ezamowienia.gov.pl", "ted.europa.eu"],
      "certifications": ["CE"],
      "note": "能源转型$250B市场"
    }
  }
}
