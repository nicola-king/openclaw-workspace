/**
 * 太一进化树可视化
 * Taiyi Evolution Tree Visualization
 */

class EvolutionTree {
    constructor(containerId, data) {
        this.containerId = containerId;
        this.data = data;
        this.width = 800;
        this.height = 600;
        this.margin = { top: 40, right: 90, bottom: 50, left: 90 };
        
        this.init();
        this.render();
    }
    
    init() {
        // 创建 SVG
        this.svg = d3.select(`#${this.containerId}`)
            .append("svg")
            .attr("width", this.width)
            .attr("height", this.height)
            .attr("viewBox", [0, 0, this.width, this.height]);
        
        // 创建分组
        this.g = this.svg.append("g")
            .attr("transform", `translate(${this.margin.left},${this.margin.top})`);
    }
    
    render() {
        // 创建树形布局
        const treeLayout = d3.tree()
            .size([this.width - this.margin.left - this.margin.right, 
                   this.height - this.margin.top - this.margin.bottom]);
        
        // 转换数据为层次结构
        const root = d3.hierarchy(this.data.tree);
        
        // 应用树形布局
        treeLayout(root);
        
        // 绘制连线
        this.g.selectAll(".link")
            .data(root.links())
            .join("path")
            .attr("class", "link")
            .attr("d", d3.linkVertical()
                .x(d => d.x)
                .y(d => d.y));
        
        // 绘制节点
        const nodes = this.g.selectAll(".node")
            .data(root.descendants())
            .join("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.x},${d.y})`);
        
        // 添加圆形节点
        nodes.append("circle")
            .attr("r", 10)
            .attr("fill", d => d.data.color || "#667eea");
        
        // 添加文本标签
        nodes.append("text")
            .attr("dy", d => d.children ? -15 : 15)
            .attr("text-anchor", "middle")
            .text(d => {
                const name = d.data.name || d.data.root.name;
                const icon = d.data.icon || d.data.root.icon || "";
                return `${icon} ${name}`;
            })
            .style("font-size", d => d.children ? "14px" : "12px")
            .style("font-weight", d => d.children ? "bold" : "normal");
        
        // 添加交互
        nodes.on("click", (event, d) => {
            this.showNodeDetails(d);
        });
        
        // 添加动画
        nodes.transition()
            .duration(1000)
            .attr("opacity", 1);
    }
    
    showNodeDetails(node) {
        const details = node.data;
        
        // 创建提示框
        const tooltip = d3.select("body")
            .append("div")
            .attr("class", "tooltip")
            .style("position", "absolute")
            .style("background", "white")
            .style("padding", "15px")
            .style("border-radius", "10px")
            .style("box-shadow", "0 4px 20px rgba(0,0,0,0.2)")
            .style("pointer-events", "none")
            .style("opacity", 0)
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 10) + "px");
        
        tooltip.html(`
            <h3 class="font-bold text-lg mb-2">${details.icon || "🌟"} ${details.name || "太一 AGI"}</h3>
            <div class="space-y-1 text-sm">
                <p>🤖 Agent: ${details.agents || "-"}</p>
                <p>📚 Skills: ${details.skills || "-"}</p>
                <p>👥 贡献者：${details.contributors || "-"}</p>
                <p>💾 提交：${details.commits || "-"}</p>
            </div>
        `);
        
        tooltip.transition()
            .duration(200)
            .style("opacity", 1);
        
        // 3 秒后隐藏
        setTimeout(() => {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0)
                .remove();
        }, 3000);
    }
    
    update(data) {
        this.data = data;
        this.g.selectAll("*").remove();
        this.render();
    }
}

// 导出
window.EvolutionTree = EvolutionTree;
