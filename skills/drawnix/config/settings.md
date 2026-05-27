{
  "_comment": "Drawnix Skill 配置 — 2026-05-27",
  "version": "1.0.0",
  "service": {
    "type": "webapp",
    "online_url": "https://drawnix.com",
    "local_port": 3800,
    "local_url": "http://localhost:3800",
    "deploy_method": "docker"
  },
  "features": {
    "markdown_to_mindmap": true,
    "mermaid_to_flowchart": true,
    "export_png": true,
    "export_json": true,
    "auto_save": true,
    "infinite_canvas": true
  },
  "auto_trigger": {
    "market_analysis": "mindmap",
    "buyer_relationship": "mindmap",
    "competition_landscape": "flowchart",
    "business_process": "flowchart",
    "background_check_results": "mindmap",
    "project_roadmap": "gantt"
  },
  "docker": {
    "image": "pubuzhixing/drawnix:latest",
    "port_mapping": "3800:80",
    "status": "not_deployed"
  },
  "status": "skill_defined_ready_for_deploy"
}
