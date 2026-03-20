/**
 * CodeEditor — Professional code editor mockup with typing animation
 *
 * Features:
 * - VS Code-style chrome (title bar, traffic light dots, file name)
 * - Line numbers in muted color
 * - Character-by-character typing with blinking cursor
 * - State transitions: typing → error (red glow) → success (green glow)
 * - Syntax-colored lines via per-line color prop
 *
 * Usage:
 * <CodeEditor
 *   lines={[
 *     { text: "---", color: "#4A4540" },
 *     { text: "name: my-skill", color: "#C4703F" },
 *     { text: "type: skill", color: "#5B9BD5" },
 *   ]}
 *   fileName="skill.md"
 *   delay={10}
 *   charsPerFrame={2}
 *   state="success"
 *   stateStartFrame={80}
 * />
 */
import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

interface CodeLine {
  text: string;
  color?: string;
  indent?: number;
}

interface Props {
  lines: CodeLine[];
  fileName?: string;
  delay?: number;
  charsPerFrame?: number;
  state?: "typing" | "error" | "success";
  stateStartFrame?: number;
  width?: number;
}

export const CodeEditor: React.FC<Props> = ({
  lines,
  fileName = "skill.md",
  delay = 0,
  charsPerFrame = 1.5,
  state = "typing",
  stateStartFrame = 999,
  width = 860,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const CLAMP = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
  const FG = "#F5F0EB";
  const MUTED = "#7A756F";
  const DIM = "#4A4540";
  const ACCENT = "#C4703F";
  const RED = "#E74C3C";
  const GREEN = "#4FC47B";
  const MONO = "JetBrains Mono";

  const entrance = spring({ frame: frame - delay, fps, config: { damping: 16, stiffness: 80, mass: 1 } });
  const slideY = interpolate(entrance, [0, 1], [60, 0], CLAMP);
  const opacity = interpolate(entrance, [0, 1], [0, 1], CLAMP);

  const typingFrame = Math.max(0, frame - delay - 10);
  const totalChars = lines.reduce((sum, l) => sum + (l.indent || 0) + l.text.length + 1, 0);
  const charsRevealed = Math.min(totalChars, Math.floor(typingFrame * charsPerFrame));

  let borderColor = "rgba(255,255,255,0.06)";
  let glowColor = "transparent";
  if (frame >= stateStartFrame) {
    const sp = interpolate(frame, [stateStartFrame, stateStartFrame + 8], [0, 1], CLAMP);
    if (state === "error") { borderColor = `rgba(231,76,60,${sp * 0.8})`; glowColor = `rgba(231,76,60,${sp * 0.25})`; }
    else if (state === "success") { borderColor = `rgba(79,196,123,${sp * 0.8})`; glowColor = `rgba(79,196,123,${sp * 0.25})`; }
  }

  let charCounter = 0;
  const renderedLines = lines.map((line, idx) => {
    const prefix = " ".repeat(line.indent || 0);
    const full = prefix + line.text;
    const start = charCounter;
    charCounter += full.length + 1;
    const visible = Math.max(0, Math.min(full.length, charsRevealed - start));
    const showCursor = charsRevealed >= start && charsRevealed < start + full.length + 1;
    return (
      <div key={idx} style={{ display: "flex", lineHeight: 1.8, minHeight: 28 }}>
        <span style={{ color: DIM, width: 40, textAlign: "right", marginRight: 16, fontSize: 16, fontFamily: MONO }}>{idx + 1}</span>
        <span style={{ color: line.color || FG, fontFamily: MONO, fontSize: 18, whiteSpace: "pre" }}>
          {full.substring(0, visible)}
          {showCursor && <span style={{ display: "inline-block", width: 2, height: 20, background: ACCENT, marginLeft: 1, opacity: Math.sin(frame * 0.3) > 0 ? 1 : 0, verticalAlign: "middle" }} />}
        </span>
      </div>
    );
  });

  return (
    <div style={{ width, borderRadius: 16, background: "#0D0D14", border: `1.5px solid ${borderColor}`, boxShadow: `0 0 40px ${glowColor}, 0 20px 60px rgba(0,0,0,0.4)`, overflow: "hidden", opacity, transform: `translateY(${slideY}px)` }}>
      <div style={{ padding: "14px 20px", background: "rgba(255,255,255,0.03)", display: "flex", alignItems: "center", gap: 8, borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
        <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#FF5F57" }} />
        <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#FEBC2E" }} />
        <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#28C840" }} />
        <span style={{ marginLeft: 12, color: MUTED, fontFamily: MONO, fontSize: 14 }}>{fileName}</span>
      </div>
      <div style={{ padding: "20px 16px" }}>{renderedLines}</div>
      {frame >= stateStartFrame && (
        <div style={{ padding: "10px 20px", background: state === "error" ? "rgba(231,76,60,0.1)" : "rgba(79,196,123,0.1)", borderTop: `1px solid ${state === "error" ? "rgba(231,76,60,0.2)" : "rgba(79,196,123,0.2)"}`, display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 16 }}>{state === "error" ? "✕" : "✓"}</span>
          <span style={{ fontFamily: MONO, fontSize: 14, color: state === "error" ? RED : GREEN }}>{state === "error" ? "Build Failed" : "Build Succeeded"}</span>
        </div>
      )}
    </div>
  );
};
