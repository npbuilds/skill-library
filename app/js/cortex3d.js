/**
 * Neural Observatory — 3D Cortex Map
 *
 * WebGL force-directed graph rendered with 3d-force-graph
 * (Three.js + d3-force-3d). Loaded as a plain (non-module) script
 * so it can attach to the global `NO`-style namespace used by the
 * inline app code in index.html. Exposes `window.Cortex3D`.
 */
(function () {
  const RADIUS = 220;             // sphere-shell radius for domain cluster centers
  const CLUSTER_PULL = 0.08;      // per-tick pull strength toward cluster center
  const CHARGE_STRENGTH = -60;    // mirrors 2D NO.cortex setup
  const CHARGE_DIST_MAX = 180;
  const LINK_DISTANCE = 35;
  const LINK_STRENGTH = 0.2;
  const PULSE_RECENT_N = 15;      // last N usage events get a pulse (mirrors 2D)
  const PULSE_DURATION_MS = 2000; // matches 2s 2D keyframe
  const PULSE_MIN_SCALE = 0.1;
  const PULSE_MAX_SCALE = 3.0;
  const PULSE_PEAK_OPACITY = 0.6; // matches 2D 0.6 → 0 fade
  const TRAIL_COLOR = '#5acece';  // matches --cyan-bright; learning-trail accent
  const TRAIL_WIDTH = 1.4;        // ~4× the intra-edge width — visually distinct
  const NODE_RESOLUTION = 24;     // smoother spheres when zoomed in (default 8)

  // Type-based shape segments: (widthSegments, heightSegments) for SphereGeometry.
  // Low segment counts make the sphere render as a polyhedron — a free way to get
  // diamonds/tetrahedra without needing direct access to THREE's geometry classes.
  // Matches the 2D type→shape mapping: diamond/square/circle/triangle.
  const SHAPE_BY_TYPE = {
    orchestrator: [4, 2],   // 4-sided diamond (octahedron-like) ◇
    director:     [4, 4],   // angular sphere (cube-ish look)
    observer:     [3, 2],   // triangular bipyramid (3-sided pyramid)
    // action / knowledge: default smooth sphere (no entry → no swap)
  };

  // Theme-driven colors read from CSS variables on <html>. Re-read on theme change.
  function readTheme() {
    const css = getComputedStyle(document.documentElement);
    const v = (name, fallback) => (css.getPropertyValue(name).trim() || fallback);
    return {
      bg: v('--bg-deep', '#06070d'),
      cross: v('--magenta-faded', '#8a3a6a'),
      intra: v('--border-dim', '#1a1d3a'),
    };
  }

  function fibonacciSphere(n, radius) {
    if (n <= 0) return [];
    if (n === 1) return [{ x: 0, y: 0, z: 0 }];
    const pts = [];
    const phi = Math.PI * (3 - Math.sqrt(5));
    for (let i = 0; i < n; i++) {
      const y = 1 - (i / (n - 1)) * 2;
      const r = Math.sqrt(1 - y * y);
      const t = phi * i;
      pts.push({ x: Math.cos(t) * r * radius, y: y * radius, z: Math.sin(t) * r * radius });
    }
    return pts;
  }

  function buildGraphData(noData) {
    // NO.data.usage is merged newest-first in NO.data.computeDerived (the
    // committed meta/usage_rollup tail plus the live Firestore tail).
    // Take the newest N from index 0, then reverse so the trail walks
    // oldest → newest (matches learning-progression direction).
    const recentUsage = (noData.usage || []).slice(0, PULSE_RECENT_N).reverse();
    const recentIds = new Set(recentUsage.map(e => e.skill));
    const nodes = noData.skillList.map(s => ({
      id: s.name,
      domain: noData.skillDomain[s.name] || 'unknown',
      type: s.type,
      score: s.composite_score || 0,
      recent: recentIds.has(s.name),
    }));
    const idSet = new Set(nodes.map(n => n.id));
    const links = [];
    for (const s of noData.skillList) {
      for (const dep of (s.depends_on || [])) {
        if (!idSet.has(dep)) continue;
        const sd = noData.skillDomain[s.name];
        const td = noData.skillDomain[dep];
        links.push({
          source: s.name,
          target: dep,
          crossDomain: !!(sd && td && sd !== td),
        });
      }
    }
    // Learning trail: connect consecutive recent skills in usage order.
    // Marked `trail: true` so the link-color/width callbacks can style them
    // distinctly without disturbing the dependency graph.
    for (let i = 0; i < recentUsage.length - 1; i++) {
      const src = recentUsage[i].skill;
      const tgt = recentUsage[i + 1].skill;
      if (src === tgt) continue;
      if (!idSet.has(src) || !idSet.has(tgt)) continue;
      links.push({ source: src, target: tgt, trail: true });
    }
    // Constellation edges: star topology (radial spokes) + tangential ring chain
    // per domain. Together these form a spider-web pattern per cluster:
    //   - Radial: each non-anchor node → domain anchor (highest-score node)
    //   - Tangential: closed ring through the non-anchor nodes (in id order)
    // Both tagged `constellation: true` so they share the constellation toggle.
    const anchorByDomain = {};
    for (const n of nodes) {
      if (!anchorByDomain[n.domain] || n.score > anchorByDomain[n.domain].score) {
        anchorByDomain[n.domain] = n;
      }
    }
    const nonAnchorsByDomain = {};
    for (const n of nodes) {
      const anchor = anchorByDomain[n.domain];
      if (!anchor || anchor.id === n.id) continue;
      links.push({ source: n.id, target: anchor.id, constellation: true });
      (nonAnchorsByDomain[n.domain] = nonAnchorsByDomain[n.domain] || []).push(n.id);
    }
    for (const dom of Object.keys(nonAnchorsByDomain)) {
      const ring = nonAnchorsByDomain[dom];
      if (ring.length < 2) continue;
      for (let i = 0; i < ring.length; i++) {
        const a = ring[i];
        const b = ring[(i + 1) % ring.length];  // close the loop on last → first
        links.push({ source: a, target: b, constellation: true, webRing: true });
      }
    }
    return { nodes, links };
  }

  let graphInstance = null;
  let containerEl = null;
  let resizeBound = false;
  let themeObserverBound = false;
  let currentTheme = null;  // mutated in place so the link-color callback sees fresh values
  let pulseMeshes = [];     // { mesh, mat, startTime } per recent node
  let pulseRafHandle = null;
  let paused = false;
  // Highlight state — mutated by hover, domain filter, and constellation toggle.
  let hoveredId = null;
  let neighborIds = new Set();
  let filteredDomain = null;
  let constellationMode = false;

  function init(containerSel, noData, domainColors, options) {
    containerEl = document.querySelector(containerSel);
    if (!containerEl) {
      console.error('[Cortex3D] container not found:', containerSel);
      return null;
    }
    if (typeof ForceGraph3D === 'undefined') {
      console.error('[Cortex3D] 3d-force-graph library not loaded');
      containerEl.innerHTML =
        '<div style="padding:24px;color:#ce5a5a;font-family:var(--font-mono);font-size:11px">' +
        '3D library failed to load. Check network / CDN.</div>';
      return null;
    }

    const { nodes, links } = buildGraphData(noData);
    const domains = [...new Set(nodes.map(n => n.domain))];
    const centers = fibonacciSphere(domains.length, RADIUS);
    const centerByDomain = Object.fromEntries(domains.map((d, i) => [d, centers[i]]));
    currentTheme = readTheme();

    graphInstance = ForceGraph3D()(containerEl)
      .backgroundColor(currentTheme.bg)
      .graphData({ nodes, links })
      .nodeColor(n => domainColors[n.domain] || '#888')
      .nodeVal(n => Math.max(1, (n.score || 0) / 20))
      .nodeOpacity(0.85)
      .nodeResolution(NODE_RESOLUTION)
      .linkColor(l => l.trail ? TRAIL_COLOR : (l.crossDomain ? currentTheme.cross : currentTheme.intra))
      .linkOpacity(0.35)
      .linkWidth(l => l.trail ? TRAIL_WIDTH : (l.crossDomain ? 0.6 : 0.25))
      // Flowing particles along the trail — directional, conveying skill-usage sequence.
      .linkDirectionalParticles(l => l.trail ? 3 : 0)
      .linkDirectionalParticleSpeed(0.008)
      .linkDirectionalParticleWidth(1.8)
      .linkDirectionalParticleColor(() => TRAIL_COLOR)
      .enableNodeDrag(false)
      .showNavInfo(false);

    if (options && typeof options.onNodeClick === 'function') {
      graphInstance.onNodeClick((node) => options.onNodeClick(node.id, node));
    }

    // Hover-highlight: dim non-neighbors when hovering a node.
    graphInstance.onNodeHover((node) => {
      hoveredId = node ? node.id : null;
      neighborIds = node ? buildNeighborSet(node.id, graphInstance.graphData().links) : new Set();
      applyHighlight();
    });

    // Custom 3D radial-clustering force — pulls each node toward its
    // domain's point on the sphere shell.
    graphInstance.d3Force('cluster', (alpha) => {
      for (const n of nodes) {
        const c = centerByDomain[n.domain];
        if (!c) continue;
        n.vx += (c.x - (n.x || 0)) * CLUSTER_PULL * alpha;
        n.vy += (c.y - (n.y || 0)) * CLUSTER_PULL * alpha;
        n.vz += (c.z - (n.z || 0)) * CLUSTER_PULL * alpha;
      }
    });

    const chargeForce = graphInstance.d3Force('charge');
    if (chargeForce) chargeForce.strength(CHARGE_STRENGTH).distanceMax(CHARGE_DIST_MAX);
    const linkForce = graphInstance.d3Force('link');
    if (linkForce) linkForce.distance(LINK_DISTANCE).strength(l => l.constellation ? 0 : LINK_STRENGTH);

    handleResize();
    if (!resizeBound) {
      window.addEventListener('resize', handleResize);
      resizeBound = true;
    }
    bindThemeObserver();
    // Honor an already-active theme (e.g. spider-verse from localStorage) since
    // the MutationObserver only fires on subsequent changes.
    applyTheme();

    // Library populates node.__threeObj asynchronously over the first few
    // render frames. Poll until at least one recent node has a base mesh,
    // then attach pulses to all of them.
    paused = false;
    waitForBaseMeshes(nodes, domainColors, 60);

    return graphInstance;
  }

  function waitForBaseMeshes(nodes, domainColors, attemptsLeft) {
    const ready = nodes.some(n => n.__threeObj && n.__threeObj.material);
    if (ready) {
      applyShapesByType(nodes);
      attachPulses(nodes, domainColors);
      // Hide constellation edges (default off) once their __lineObj refs exist.
      // Link meshes can lag node meshes by a frame or two, so try a few times.
      retryHighlight(20);
      return;
    }
    if (attemptsLeft <= 0) {
      console.warn('[Cortex3D] gave up waiting for base meshes — no pulses or shape swaps attached');
      return;
    }
    // setTimeout instead of rAF — survives tab-throttling and headless preview environments.
    setTimeout(() => waitForBaseMeshes(nodes, domainColors, attemptsLeft - 1), 50);
  }

  function retryHighlight(attemptsLeft) {
    applyHighlight();
    // Re-apply scene lighting in the retry window — the library may add its
    // AmbientLight/DirectionalLight a frame or two after init, so the initial
    // applyTheme call can miss them.
    const isSpiderverse = document.documentElement.getAttribute('data-theme') === 'spiderverse';
    applySceneLighting(isSpiderverse);
    if (attemptsLeft > 0) setTimeout(() => retryHighlight(attemptsLeft - 1), 100);
  }

  function applyShapesByType(nodes) {
    // Find any node with __threeObj to extract the SphereGeometry constructor —
    // avoids needing direct access to the THREE namespace.
    const sample = nodes.find(n => n.__threeObj && n.__threeObj.geometry);
    if (!sample) return;
    const SphereGeometry = sample.__threeObj.geometry.constructor;
    const baseRadius = (sample.__threeObj.geometry.parameters && sample.__threeObj.geometry.parameters.radius) || 1;
    for (const n of nodes) {
      const base = n.__threeObj;
      if (!base) continue;
      // 3d-force-graph caches materials by color, so multiple nodes can share
      // one material instance. Clone it so per-node opacity (for hover/filter
      // highlight) doesn't cascade across same-color nodes.
      if (base.material && base.material.clone) {
        base.material = base.material.clone();
      }
      const segs = SHAPE_BY_TYPE[n.type];
      if (!segs || !base.geometry) continue;
      const oldGeom = base.geometry;
      const radius = (oldGeom.parameters && oldGeom.parameters.radius) || baseRadius;
      try {
        base.geometry = new SphereGeometry(radius, segs[0], segs[1]);
        oldGeom.dispose();
      } catch (e) {
        // If geometry swap fails (constructor signature mismatch), leave the default.
      }
    }
  }

  function attachPulses(nodes, domainColors) {
    disposePulses();
    for (const n of nodes) {
      if (!n.recent) continue;
      const base = n.__threeObj;
      if (!base || !base.material) continue;

      // Clone the base mesh — shares geometry, but we clone the material
      // so opacity/color can be mutated independently.
      const pulse = base.clone();
      pulse.material = base.material.clone();
      pulse.material.wireframe = true;
      pulse.material.transparent = true;
      pulse.material.opacity = PULSE_PEAK_OPACITY;
      pulse.material.depthWrite = false;
      if (pulse.material.color && pulse.material.color.set) {
        pulse.material.color.set(domainColors[n.domain] || '#888888');
      }
      pulse.scale.setScalar(PULSE_MIN_SCALE);

      // Parent to the base mesh so the pulse follows node motion automatically.
      base.add(pulse);

      pulseMeshes.push({
        mesh: pulse,
        mat: pulse.material,
        startTime: performance.now() + Math.random() * PULSE_DURATION_MS,
      });
    }
    if (!paused) startPulseLoop();
  }

  function pulseTick() {
    const now = performance.now();
    const scaleSpan = PULSE_MAX_SCALE - PULSE_MIN_SCALE;
    for (const p of pulseMeshes) {
      const phase = ((now - p.startTime) % PULSE_DURATION_MS) / PULSE_DURATION_MS;
      p.mesh.scale.setScalar(PULSE_MIN_SCALE + phase * scaleSpan);
      p.mat.opacity = PULSE_PEAK_OPACITY * (1 - phase);
    }
    pulseRafHandle = requestAnimationFrame(pulseTick);
  }

  function startPulseLoop() {
    if (pulseRafHandle !== null) return;
    if (pulseMeshes.length === 0) return;
    pulseRafHandle = requestAnimationFrame(pulseTick);
  }

  function stopPulseLoop() {
    if (pulseRafHandle === null) return;
    cancelAnimationFrame(pulseRafHandle);
    pulseRafHandle = null;
  }

  function disposePulses() {
    stopPulseLoop();
    for (const p of pulseMeshes) {
      if (p.mesh.parent) p.mesh.parent.remove(p.mesh);
      if (p.mat && p.mat.dispose) p.mat.dispose();
    }
    pulseMeshes = [];
  }

  function buildNeighborSet(id, links) {
    const s = new Set([id]);
    for (const l of links) {
      if (l.constellation) continue; // constellation edges aren't real neighbors
      const srcId = typeof l.source === 'object' ? l.source.id : l.source;
      const tgtId = typeof l.target === 'object' ? l.target.id : l.target;
      if (srcId === id) s.add(tgtId);
      if (tgtId === id) s.add(srcId);
    }
    return s;
  }

  function applyHighlight() {
    if (!graphInstance) return;
    const data = graphInstance.graphData();
    const idToDomain = {};
    for (const n of data.nodes) idToDomain[n.id] = n.domain;

    for (const n of data.nodes) {
      const obj = n.__threeObj;
      if (!obj || !obj.material) continue;
      const dim =
        (hoveredId && !neighborIds.has(n.id)) ||
        (filteredDomain && n.domain !== filteredDomain);
      obj.material.transparent = true;
      obj.material.opacity = dim ? 0.07 : 0.85;
    }

    for (const l of data.links) {
      const obj = l.__lineObj || l.__threeObj;
      if (!obj || !obj.material) continue;
      const srcId = typeof l.source === 'object' ? l.source.id : l.source;
      const tgtId = typeof l.target === 'object' ? l.target.id : l.target;
      obj.material.transparent = true;
      if (l.constellation) {
        // Constellation edges visible only when mode is on. Honor filter if active.
        const visibleByFilter = !filteredDomain ||
          (idToDomain[srcId] === filteredDomain && idToDomain[tgtId] === filteredDomain);
        const isSpiderverse = document.documentElement.getAttribute('data-theme') === 'spiderverse';
        const opaq = isSpiderverse ? 0.55 : 0.18;
        obj.material.opacity = (constellationMode && visibleByFilter) ? opaq : 0;
        continue;
      }
      let dim = false;
      if (hoveredId) {
        dim = !(neighborIds.has(srcId) && neighborIds.has(tgtId));
      } else if (filteredDomain) {
        dim = !(idToDomain[srcId] === filteredDomain || idToDomain[tgtId] === filteredDomain);
      }
      obj.material.opacity = dim ? 0.03 : 0.35;
    }
  }

  function handleResize() {
    if (!graphInstance || !containerEl) return;
    const w = containerEl.clientWidth;
    const h = containerEl.clientHeight;
    if (w > 0 && h > 0) graphInstance.width(w).height(h);
  }

  function applyTheme() {
    if (!graphInstance) return;
    currentTheme = readTheme();
    const themeName = document.documentElement.getAttribute('data-theme') || 'dark';
    const isSpiderverse = themeName === 'spiderverse';
    graphInstance.backgroundColor(currentTheme.bg);
    // Spider-Verse: bright magenta border for constellation/web; otherwise default.
    const webColor = isSpiderverse ? '#ff2d95' : (currentTheme.cross || '#8a3a6a');
    graphInstance.linkColor(l => {
      if (l.trail) return TRAIL_COLOR;
      if (l.constellation) return webColor;
      return l.crossDomain ? currentTheme.cross : currentTheme.intra;
    });
    // Auto-enable constellation when entering Spider-Verse theme (the web is the point).
    if (isSpiderverse && !constellationMode) constellationMode = true;
    // Flatten lighting in spider-verse: push ambient light to ~full so spheres
    // render as comic-book flat color blocks rather than gradient-shaded balls.
    applySceneLighting(isSpiderverse);
    applyHighlight();
  }

  function applySceneLighting(flat) {
    if (!graphInstance) return;
    const scene = graphInstance.scene();
    if (!scene || !scene.traverse) return;
    // Spider-Verse / flat mode: max ambient + zero directional → no shading
    // gradient, comic-panel-flat color blocks. Library default is π ambient
    // + ~0.6π directional, so we have to push ambient higher than default
    // (not lower) to actually flatten.
    scene.traverse((obj) => {
      if (obj.isAmbientLight) obj.intensity = flat ? 5.0 : Math.PI;
      else if (obj.isDirectionalLight || obj.isPointLight || obj.isHemisphereLight) {
        obj.intensity = flat ? 0 : 0.6 * Math.PI;
      }
    });
  }

  function bindThemeObserver() {
    if (themeObserverBound) return;
    const obs = new MutationObserver(applyTheme);
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    themeObserverBound = true;
  }

  window.Cortex3D = {
    init,
    pause: () => {
      paused = true;
      stopPulseLoop();
      if (graphInstance) graphInstance.pauseAnimation();
    },
    resume: () => {
      paused = false;
      if (graphInstance) graphInstance.resumeAnimation();
      startPulseLoop();
    },
    resize: handleResize,
    applyTheme,
    setFilteredDomain: (d) => { filteredDomain = d || null; applyHighlight(); },
    setConstellationMode: (b) => { constellationMode = !!b; applyHighlight(); },
    isConstellationMode: () => constellationMode,
    instance: () => graphInstance,
  };
})();
