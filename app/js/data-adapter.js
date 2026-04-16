/**
 * Neural Observatory — Firestore Data Adapter
 *
 * Replaces NO.data.loadAll() (which used fetch() against static files)
 * with Firestore collection reads + real-time listeners.
 *
 * The adapter preserves the same NO.data shape so all 16 visualization
 * modules (cortex, org, chord, etc.) work without any changes.
 */

import { db } from './firebase-config.js';
import {
  collection,
  doc,
  getDoc,
  getDocs,
  onSnapshot,
  query,
  orderBy,
} from 'https://www.gstatic.com/firebasejs/11.7.1/firebase-firestore.js';

// ── One-shot load (replaces fetch-based loadAll) ────────────────────

export async function loadAllFromFirestore(NO) {
  const [skillsSnap, metaSnap, usageSnap, gapsSnap, evoSnap, changeSnap] =
    await Promise.all([
      getDocs(collection(db, 'skills')),
      getDoc(doc(db, 'meta', 'registry')),
      getDocs(query(collection(db, 'usage'), orderBy('timestamp', 'desc'))),
      getDocs(collection(db, 'gaps')),
      getDocs(query(collection(db, 'evolution'), orderBy('date', 'asc'))),
      getDocs(collection(db, 'changelogs')),
    ]);

  // ── Skills → registry shape ──────────────────────────────────
  const skills = {};
  skillsSnap.forEach((d) => {
    skills[d.id] = d.data();
  });

  const meta = metaSnap.exists() ? metaSnap.data() : {};

  NO.data.registry = {
    schema_version: meta.schema_version || 2,
    plugin_version: meta.plugin_version || '1.0.0',
    last_scan: meta.last_scan || null,
    skills,
    network: { domains: meta.network_domains || {} },
  };
  NO.data.skills = skills;
  NO.data.skillList = Object.values(skills);
  NO.data.domains = meta.network_domains || {};

  // ── Usage ────────────────────────────────────────────────────
  NO.data.usage = [];
  usageSnap.forEach((d) => NO.data.usage.push(d.data()));

  // ── Gaps ─────────────────────────────────────────────────────
  NO.data.gaps = [];
  gapsSnap.forEach((d) => NO.data.gaps.push(d.data()));

  // ── Evolution ────────────────────────────────────────────────
  NO.data.evolution = [];
  evoSnap.forEach((d) => NO.data.evolution.push(d.data()));

  // ── Changelogs ───────────────────────────────────────────────
  NO.data.changelogs = {};
  changeSnap.forEach((d) => {
    const data = d.data();
    NO.data.changelogs[data.skill || d.id] = data.entries || data;
  });

  // ── Derived data (same as original computeDerived) ───────────
  NO.data.skillDomain = {};
  for (const [d, skillNames] of Object.entries(NO.data.domains)) {
    for (const s of skillNames) NO.data.skillDomain[s] = d;
  }

  NO.data.domainOrder = Object.entries(NO.data.domains)
    .sort((a, b) => b[1].length - a[1].length)
    .map((d) => d[0]);

  NO.data.computeDerived();
}

// ── Real-time listener (replaces 30s polling) ───────────────────────

export function subscribeToSkills(NO, onUpdate) {
  return onSnapshot(collection(db, 'skills'), (snapshot) => {
    const skills = {};
    snapshot.forEach((d) => {
      skills[d.id] = d.data();
    });

    const oldCount = NO.data.skillList.length;
    NO.data.skills = skills;
    NO.data.skillList = Object.values(skills);

    // Rebuild domain mapping (skills may have moved)
    NO.data.skillDomain = {};
    for (const s of NO.data.skillList) {
      if (s.domain) NO.data.skillDomain[s.name] = s.domain;
    }

    NO.data.computeDerived();

    const newCount = NO.data.skillList.length;
    const delta = newCount - oldCount;

    if (onUpdate) onUpdate(delta);
  });
}
