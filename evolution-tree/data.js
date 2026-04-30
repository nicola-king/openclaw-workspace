/**
 * 太一进化树数据
 * Taiyi Evolution Tree Data
 */

const TAIYI_DATA = {
    // 树结构数据
    tree: {
        root: {
            name: "太一 AGI",
            created: "2026-01-01",
            contributors: 1,
            commits: 1000,
            icon: "🌟"
        },
        branches: [
            {
                name: "工程类",
                icon: "🛠️",
                agents: 28,
                skills: 150,
                contributors: 5,
                commits: 300,
                color: "#667eea",
                children: [
                    { name: "Frontend Developer", icon: "🖥️", commits: 50 },
                    { name: "Backend Architect", icon: "🏗️", commits: 45 },
                    { name: "Mobile App Builder", icon: "📱", commits: 40 },
                    { name: "AI Engineer", icon: "🤖", commits: 55 },
                    { name: "Data Engineer", icon: "📊", commits: 35 },
                    { name: "QA Automation", icon: "🧪", commits: 30 },
                    { name: "DevOps Automator", icon: "🚀", commits: 40 },
                    { name: "Security Engineer", icon: "🔒", commits: 35 },
                    { name: "Smart Contract Engineer", icon: "⛓️", commits: 25 },
                    { name: "Incident Response", icon: "🚨", commits: 30 }
                ]
            },
            {
                name: "市场类",
                icon: "📢",
                agents: 25,
                skills: 120,
                contributors: 3,
                commits: 200,
                color: "#764ba2",
                children: [
                    { name: "Growth Hacker", icon: "🚀", commits: 40 },
                    { name: "SEO Specialist", icon: "🔍", commits: 35 },
                    { name: "Content Creator", icon: "📝", commits: 45 },
                    { name: "TikTok Strategist", icon: "📱", commits: 30 },
                    { name: "Xiaohongshu", icon: "📕", commits: 35 },
                    { name: "WeChat Official", icon: "💬", commits: 30 },
                    { name: "Zhihu Strategist", icon: "🧠", commits: 25 },
                    { name: "Bilibili Strategist", icon: "🎬", commits: 25 },
                    { name: "LinkedIn Creator", icon: "💼", commits: 20 },
                    { name: "Twitter Engager", icon: "🐦", commits: 20 }
                ]
            },
            {
                name: "销售类",
                icon: "💼",
                agents: 9,
                skills: 50,
                contributors: 2,
                commits: 150,
                color: "#f093fb",
                children: [
                    { name: "Outbound Strategist", icon: "🎯", commits: 30 },
                    { name: "Account Executive", icon: "💼", commits: 35 },
                    { name: "Sales Engineer", icon: "🛠️", commits: 25 },
                    { name: "Discovery Coach", icon: "🔍", commits: 20 },
                    { name: "Deal Strategist", icon: "♟️", commits: 25 },
                    { name: "Pipeline Analyst", icon: "📊", commits: 15 }
                ]
            },
            {
                name: "产品类",
                icon: "📦",
                agents: 6,
                skills: 40,
                contributors: 2,
                commits: 120,
                color: "#f5576c",
                children: [
                    { name: "Product Manager", icon: "📦", commits: 30 },
                    { name: "UX Researcher", icon: "🔍", commits: 25 },
                    { name: "Trend Researcher", icon: "📈", commits: 20 },
                    { name: "Product Owner", icon: "🎯", commits: 25 },
                    { name: "Product Designer", icon: "🎨", commits: 20 }
                ]
            },
            {
                name: "设计类",
                icon: "🎨",
                agents: 8,
                skills: 45,
                contributors: 2,
                commits: 100,
                color: "#4facfe",
                children: [
                    { name: "UI Designer", icon: "🎯", commits: 25 },
                    { name: "UX Writer", icon: "✍️", commits: 20 },
                    { name: "Brand Guardian", icon: "🎭", commits: 15 },
                    { name: "Visual Storyteller", icon: "📖", commits: 20 },
                    { name: "Image Prompt", icon: "📷", commits: 20 }
                ]
            },
            {
                name: "支持类",
                icon: "🤝",
                agents: 8,
                skills: 50,
                contributors: 2,
                commits: 90,
                color: "#43e97b",
                children: [
                    { name: "Customer Success", icon: "🤝", commits: 20 },
                    { name: "Technical Support", icon: "🎧", commits: 25 },
                    { name: "Community Manager", icon: "👥", commits: 15 },
                    { name: "Training Specialist", icon: "🎓", commits: 15 },
                    { name: "Implementation", icon: "⚙️", commits: 15 }
                ]
            },
            {
                name: "运营类",
                icon: "📊",
                agents: 10,
                skills: 60,
                contributors: 2,
                commits: 110,
                color: "#fa709a",
                children: [
                    { name: "Operations Manager", icon: "📊", commits: 25 },
                    { name: "Supply Chain", icon: "📦", commits: 20 },
                    { name: "Admin Assistant", icon: "📋", commits: 15 },
                    { name: "Business Analyst", icon: "📈", commits: 20 },
                    { name: "Compliance Officer", icon: "⚖️", commits: 15 },
                    { name: "HR Recruiter", icon: "👥", commits: 15 }
                ]
            },
            {
                name: "交易类",
                icon: "📈",
                agents: 15,
                skills: 80,
                contributors: 3,
                commits: 250,
                color: "#fee140",
                children: [
                    { name: "Polymarket Agent", icon: "🔮", commits: 50 },
                    { name: "GMGN Agent", icon: "💹", commits: 45 },
                    { name: "Binance Agent", icon: "₿", commits: 55 },
                    { name: "Rapid Prototyper", icon: "⚡", commits: 30 },
                    { name: "Senior Developer", icon: "💎", commits: 40 },
                    { name: "Technical Writer", icon: "📚", commits: 30 }
                ]
            }
        ]
    },
    
    // 贡献者数据
    contributors: [
        {
            username: "nicola-king",
            role: "Creator",
            commits: 1000,
            prs: 100,
            issues: 50,
            join_date: "2026-01-01",
            avatar: "https://avatars.githubusercontent.com/u/nicola-king",
            bio: "太一 AGI 创始人"
        }
    ],
    
    // 进化事件
    events: [
        {
            type: "agent_created",
            agent: "Supply Chain Manager",
            creator: "nicola-king",
            date: "2026-04-17 00:20",
            commit: "abc123",
            description: "第 35 个新增 Agent 已创建"
        },
        {
            type: "agent_created",
            agent: "Admin Assistant",
            creator: "nicola-king",
            date: "2026-04-17 00:18",
            commit: "def456",
            description: "行政支持 Agent 已创建"
        },
        {
            type: "agent_created",
            agent: "Compliance Officer",
            creator: "nicola-king",
            date: "2026-04-17 00:16",
            commit: "ghi789",
            description: "法务合规 Agent 已创建"
        },
        {
            type: "skill_added",
            skill: "全域自进化方案",
            creator: "nicola-king",
            date: "2026-04-16 23:39",
            commit: "jkl012",
            description: "全域自进化方案文档已创建"
        },
        {
            type: "constitution_added",
            constitution: "AGENT-EVOLUTION.md",
            creator: "nicola-king",
            date: "2026-04-16 23:35",
            commit: "mno345",
            description: "Agent 全域自进化宪法已建立"
        },
        {
            type: "milestone",
            milestone: "548 Skills",
            creator: "nicola-king",
            date: "2026-04-16 23:30",
            commit: "pqr678",
            description: "技能数量突破 548 个"
        },
        {
            type: "milestone",
            milestone: "189 Agents",
            creator: "nicola-king",
            date: "2026-04-16 23:25",
            commit: "stu901",
            description: "Agent 总数达到 189 个"
        },
        {
            type: "project_start",
            milestone: "全域自进化启动",
            creator: "nicola-king",
            date: "2026-04-16 23:21",
            commit: "vwx234",
            description: "太一全域自进化项目正式启动"
        }
    ],
    
    // 统计数据
    statistics: {
        total_agents: 189,
        total_skills: 548,
        total_contributors: 1,
        total_commits: 1000,
        total_forks: 0,
        total_stars: 0,
        growth_rate: "100%",
        last_updated: "2026-04-17 00:20"
    }
};

// 导出为全局变量
window.TAIYI_DATA = TAIYI_DATA;
