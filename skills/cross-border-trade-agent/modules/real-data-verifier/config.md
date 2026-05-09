{
  "module": "real-data-verifier",
  "version": "9.0.0",
  "company": {
    "enabled": true,
    "sources": ["website", "linkedin", "registry"],
    "min_confidence": 0.8
  },
  "phone": {
    "enabled": true,
    "format_check": true,
    "country_code": true,
    "patterns": ["international", "local"]
  },
  "email": {
    "enabled": true,
    "format_check": true,
    "mx_record": true,
    "disposable_check": true
  },
  "website": {
    "enabled": true,
    "status_check": true,
    "content_check": true,
    "ssl_check": true
  }
}
