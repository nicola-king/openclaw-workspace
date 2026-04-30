/**
 * 太一进化树应用主逻辑
 * Taiyi Evolution Tree Main Application
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🌳 太一进化树启动...');
    
    // 1. 初始化进化树可视化
    const tree = new EvolutionTree('tree-viz', TAIYI_DATA);
    
    // 2. 加载统计数据
    loadStatistics();
    
    // 3. 加载进化事件
    loadEvents();
    
    // 4. 加载贡献者墙
    loadContributors();
    
    // 5. 实时更新（每 5 分钟）
    setInterval(updateData, 300000);
    
    console.log('✅ 太一进化树启动完成');
});

/**
 * 加载统计数据
 */
function loadStatistics() {
    const stats = TAIYI_DATA.statistics;
    
    animateValue('stat-agents', 0, stats.total_agents, 2000);
    animateValue('stat-skills', 0, stats.total_skills, 2000);
    animateValue('stat-contributors', 0, stats.total_contributors, 2000);
    document.getElementById('stat-commits').textContent = stats.total_commits + '+';
}

/**
 * 加载进化事件
 */
function loadEvents() {
    const eventsContainer = document.getElementById('events-timeline');
    const events = TAIYI_DATA.events.slice(0, 10); // 最近 10 个事件
    
    eventsContainer.innerHTML = events.map(event => `
        <div class="event-item growing">
            <div class="font-semibold text-gray-800">${getEventIcon(event.type)} ${getEventTitle(event.type)}</div>
            <div class="text-sm text-gray-600 mt-1">${event.description}</div>
            <div class="text-xs text-gray-400 mt-1">${event.date} · ${event.creator}</div>
        </div>
    `).join('');
}

/**
 * 加载贡献者墙
 */
function loadContributors() {
    const contributorsContainer = document.getElementById('contributors-wall');
    const contributors = TAIYI_DATA.contributors;
    
    contributorsContainer.innerHTML = contributors.map(contributor => `
        <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
            <img src="${contributor.avatar}" alt="${contributor.username}" 
                 class="w-12 h-12 rounded-full"
                 onerror="this.src='https://ui-avatars.com/api/?name=${contributor.username}&background=667eea&color=fff'">
            <div class="flex-1">
                <div class="font-semibold text-gray-800">${contributor.username}</div>
                <div class="text-xs text-gray-500">${contributor.role}</div>
            </div>
            <div class="text-right">
                <div class="text-sm font-bold text-purple-600">${contributor.commits}</div>
                <div class="text-xs text-gray-400">commits</div>
            </div>
        </div>
    `).join('');
}

/**
 * 动画数字增长
 */
function animateValue(id, start, end, duration) {
    const element = document.getElementById(id);
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

/**
 * 获取事件图标
 */
function getEventIcon(type) {
    const icons = {
        'agent_created': '🤖',
        'skill_added': '📚',
        'constitution_added': '⚖️',
        'milestone': '🎯',
        'project_start': '🚀'
    };
    return icons[type] || '📝';
}

/**
 * 获取事件标题
 */
function getEventTitle(type) {
    const titles = {
        'agent_created': 'Agent 创建',
        'skill_added': '技能添加',
        'constitution_added': '宪法建立',
        'milestone': '里程碑',
        'project_start': '项目启动'
    };
    return titles[type] || '事件';
}

/**
 * 更新数据
 */
function updateData() {
    console.log('🔄 更新数据...');
    
    // 从 GitHub API 获取最新数据
    fetch('https://api.github.com/repos/nicola-king/taiyi-agents')
        .then(response => response.json())
        .then(data => {
            // 更新统计数据
            TAIYI_DATA.statistics.total_stars = data.stargazers_count;
            TAIYI_DATA.statistics.total_forks = data.forks_count;
            
            // 更新 UI
            loadStatistics();
        })
        .catch(error => {
            console.error('更新数据失败:', error);
        });
}

/**
 * 添加新事件
 */
function addEvent(event) {
    TAIYI_DATA.events.unshift(event);
    loadEvents();
}

/**
 * 添加贡献者
 */
function addContributor(contributor) {
    TAIYI_DATA.contributors.push(contributor);
    loadContributors();
}

// 导出全局函数
window.addEvent = addEvent;
window.addContributor = addContributor;
window.updateData = updateData;
