import express from 'express';
import { SessionLogger, TreeNode } from './session-logger';

/**
 * Tree visualization options
 */
export interface VisualizationOptions {
  width?: number;
  height?: number;
  zoomable?: boolean;
  searchable?: boolean;
  exportable?: boolean;
}

/**
 * Session Tree Visualizer
 *
 * Provides web-based D3.js tree visualization for OpenClaw sessions.
 */
export class SessionTreeVisualizer {
  private readonly defaultOptions: VisualizationOptions = {
    width: 1200,
    height: 800,
    zoomable: true,
    searchable: true,
    exportable: true
  };

  constructor(
    private logger: SessionLogger,
    private app: express.Application,
    private options: VisualizationOptions = {}
  ) {
    this.options = { ...this.defaultOptions, ...options };
    this.setupRoutes();
  }

  /**
   * Setup express routes for visualization
   */
  private setupRoutes(): void {
    // HTML tree page
    this.app.get('/_admin/sessions/:id/tree.html', async (req, res) => {
      const { id } = req.params;
      try {
        const tree = await this.logger.exportTree();
        const html = this.generateTreeHTML(tree, id);
        res.set('Content-Type', 'text/html');
        res.send(html);
      } catch (error) {
        res.status(500).json({ error: 'Failed to load tree' });
      }
    });

    // JSON tree export
    this.app.get('/_admin/sessions/:id/tree.json', async (req, res) => {
      const { id } = req.params;
      try {
        const tree = await this.logger.exportTree();
        res.json(tree);
      } catch (error) {
        res.status(500).json({ error: 'Failed to export tree' });
      }
    });

    // Switch branch (web UI)
    this.app.post('/_admin/sessions/:id/switch', async (req, res) => {
      const { id } = req.params;
      const { leafId } = req.body;

      try {
        await this.logger.switchBranch(leafId);
        res.json({ success: true });
      } catch (error) {
        res.status(400).json({ error: (error as Error).message });
      }
    });

    // Text tree export
    this.app.get('/_admin/sessions/:id/tree.txt', async (req, res) => {
      const { id } = req.params;
      try {
        const tree = await this.logger.exportTree();
        const text = this.treeToText(tree);
        res.set('Content-Type', 'text/plain');
        res.send(text);
      } catch (error) {
        res.status(500).json({ error: 'Failed to export tree' });
      }
    });
  }

  /**
   * Generate interactive D3.js tree HTML
   */
  private generateTreeHTML(tree: TreeNode, sessionId: string): string {
    const width = this.options.width || 1200;
    const height = this.options.height || 800;
    const zoomable = this.options.zoomable;
    const searchable = this.options.searchable;
    const exportable = this.options.exportable;

    return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Conversation Tree - Session ${sessionId}</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      color: #eee;
      height: 100vh;
      overflow: hidden;
    }

    #header {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      padding: 1rem 2rem;
      background: rgba(0, 0, 0, 0.3);
      backdrop-filter: blur(10px);
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 1000;
    }

    #title {
      font-size: 1.25rem;
      font-weight: 600;
      color: #10b981;
    }

    #controls {
      display: flex;
      gap: 1rem;
    }

    button {
      background: #10b981;
      color: white;
      padding: 0.5rem 1rem;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.875rem;
      transition: background 0.2s;
    }

    button:hover { background: #059669; }

    button.secondary {
      background: #3b82f6;
    }
    button.secondary:hover { background: #2563eb; }

    button.danger {
      background: #ef4444;
    }
    button.danger:hover { background: #dc2626; }

    #search {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 6px;
      padding: 0.5rem 1rem;
      color: #eee;
      font-size: 0.875rem;
      width: 300px;
    }

    #tree {
      width: 100vw;
      height: 100vh;
      cursor: grab;
    }
    #tree:active { cursor: grabbing; }

    .node circle {
      fill: #10b981;
      stroke: #fff;
      stroke-width: 2px;
      cursor: pointer;
      transition: all 0.3s;
    }

    .node circle:hover {
      fill: #34d399;
      r: 8;
    }

    .node circle.current {
      fill: #f59e0b;
      stroke: #fbbf24;
      stroke-width: 4px;
    }

    .node text {
      fill: #eee;
      font-size: 12px;
      pointer-events: none;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }

    .link {
      fill: none;
      stroke: #4a5568;
      stroke-width: 2px;
      opacity: 0.6;
    }

    #message-panel {
      position: fixed;
      right: 20px;
      bottom: 20px;
      width: 400px;
      max-height: 60vh;
      background: rgba(26, 26, 46, 0.95);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 1.5rem;
      overflow-y: auto;
      display: none;
      z-index: 1000;
    }

    #message-panel.visible { display: block; }

    .message-role {
      font-size: 0.75rem;
      color: #10b981;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.5rem;
    }

    .message-content {
      font-size: 0.9rem;
      line-height: 1.6;
      margin-bottom: 0.5rem;
    }

    .message-meta {
      font-size: 0.75rem;
      color: #6b7280;
    }

    .close-panel {
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: #eee;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      cursor: pointer;
    }

    #legend {
      position: fixed;
      left: 20px;
      bottom: 20px;
      background: rgba(26, 26, 46, 0.95);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 1rem;
      font-size: 0.875rem;
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin: 0.5rem 0;
    }

    .legend-color {
      width: 12px;
      height: 12px;
      border-radius: 50%;
    }
  </style>
</head>
<body>
  <div id="header">
    <div id="title">🌳 Conversation Tree - ${sessionId}</div>
    <div id="controls">
      ${searchable ? '<input type="text" id="search" placeholder="Search messages...">' : ''}
      ${exportable ? '<button onclick="exportSVG()">Export SVG</button>' : ''}
      ${exportable ? '<button onclick="exportPDF()">Export PDF</button>' : ''}
      <button class="secondary" onclick="resetView()">Reset View</button>
    </div>
  </div>

  <div id="tree"></div>

  <div id="message-panel">
    <button class="close-panel" onclick="closePanel()">×</button>
    <div class="message-role" id="panel-role"></div>
    <div class="message-content" id="panel-content"></div>
    <div class="message-meta" id="panel-meta"></div>
  </div>

  <div id="legend">
    <div class="legend-item">
      <div class="legend-color" style="background: #10b981;"></div>
      <span>User message</span>
    </div>
    <div class="legend-item">
      <div class="legend-color" style="background: #3b82f6;"></div>
      <span>Assistant message</span>
    </div>
    <div class="legend-item">
      <div class="legend-color" style="background: #f59e0b;"></div>
      <span>Current branch</span>
    </div>
  </div>

  <script>
    // Tree data
    const tree = ${JSON.stringify(tree)};

    // SVG dimensions
    const width = ${width};
    const height = ${height};
    const margin = { top: 20, right: 90, bottom: 30, left: 90 };

    // Create SVG
    const svg = d3.select("#tree")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height]);

    ${zoomable ? `
    // Add zoom
    const g = svg.append("g");
    const zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => g.attr("transform", event.transform));
    svg.call(zoom);
    ` : `
    const g = svg.append("g");
    `}

    // Tree layout
    const root = d3.hierarchy(tree);
    const treeLayout = d3.tree().size([height - margin.top - margin.bottom, width - margin.left - margin.right]);
    treeLayout(root);

    // Color scale for roles
    const colorScale = d3.scaleOrdinal()
      .domain(["user", "assistant", "system"])
      .range(["#10b981", "#3b82f6", "#6b7280"]);

    // Draw links
    g.selectAll(".link")
      .data(root.links())
      .join("path")
      .attr("class", "link")
      .attr("d", d3.linkHorizontal()
        .x(d => d.y + margin.left)
        .y(d => d.x + margin.top)
      );

    // Draw nodes
    const node = g.selectAll(".node")
      .data(root.descendants())
      .join("g")
      .attr("class", "node")
      .attr("transform", d => \`translate(\${d.y + margin.left},\${d.x + margin.top})\`);

    // Node circles
    node.append("circle")
      .attr("r", 6)
      .attr("fill", d => colorScale(d.data.role || "system"))
      .on("click", function(event, d) {
        showMessage(d.data);
        d3.selectAll(".node circle").classed("current", false);
        d3.select(this).classed("current", true);
      });

    // Node labels (first part of content)
    node.append("text")
      .attr("dy", "0.35em")
      .attr("x", d => d.children ? -10 : 10)
      .attr("text-anchor", d => d.children ? "end" : "start")
      .text(d => (d.data.content || "").substring(0, 30) + "...");

    // Message panel
    function showMessage(data) {
      const panel = document.getElementById("message-panel");
      document.getElementById("panel-role").textContent = data.role || "system";
      document.getElementById("panel-content").textContent = data.content || "";
      document.getElementById("panel-meta").textContent = new Date(data.timestamp || "").toLocaleString();
      panel.classList.add("visible");
    }

    function closePanel() {
      document.getElementById("message-panel").classList.remove("visible");
    }

    ${zoomable ? `
    function resetView() {
      svg.transition().duration(750).call(
        zoom.transform,
        d3.zoomIdentity,
        d3.zoomTransform(svg.node()).invert([width / 2, height / 2])
      );
    }
    ` : `
    function resetView() {
      window.location.reload();
    }
    `}

    ${exportable ? `
    function exportSVG() {
      const svgData = document.querySelector("svg").outerHTML;
      const blob = new Blob([svgData], { type: "image/svg+xml" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "conversation-tree.svg";
      a.click();
    }

    function exportPDF() {
      window.print();
    }
    ` : ''}

    ${searchable ? `
    // Search functionality
    document.getElementById("search").addEventListener("input", function(e) {
      const query = e.target.value.toLowerCase();
      const nodes = document.querySelectorAll(".node circle");
      nodes.forEach(node => {
        const text = node.parentElement.querySelector("text").textContent.toLowerCase();
        if (query && text.includes(query)) {
          node.style.fill = "#f59e0b";
          node.setAttribute("r", 10);
        } else {
          node.style.fill = "";
          node.setAttribute("r", 6);
        }
      });
    });
    ` : ''}
  </script>
</body>
</html>
    `;
  }

  /**
   * Convert tree to text format
   */
  private treeToText(tree: TreeNode, indent = 0): string {
    const padding = '  '.repeat(indent);
    let text = '';

    if (tree.id !== 'root') {
      const roleIcon = tree.role === 'user' ? '👤' : tree.role === 'assistant' ? '🤖' : '⚙️';
      const content = (tree.content || '').substring(0, 60);
      const timestamp = tree.timestamp ? new Date(tree.timestamp).toLocaleTimeString() : '';
      text += `${padding}${roleIcon} ${content}... [${timestamp}]\n`;
    }

    if (tree.children && tree.children.length > 0) {
      for (const child of tree.children) {
        text += this.treeToText(child, indent + 1);
      }
    }

    return text;
  }
}

/**
 * Create tree visualizer for a session
 */
export function createTreeVisualizer(
  logger: SessionLogger,
  app: express.Application,
  options?: VisualizationOptions
): SessionTreeVisualizer {
  return new SessionTreeVisualizer(logger, app, options);
}
