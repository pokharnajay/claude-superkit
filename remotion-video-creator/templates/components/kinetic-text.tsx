/**
 * KineticText — Professional text animation with multiple modes
 *
 * Modes:
 * - wordByWord: each word springs in sequentially (default, most cinematic)
 * - fadeUp: entire text fades in + slides up (clean, simple)
 * - lineReveal: multi-line text reveals line by line
 *
 * Emphasis: highlight specific words in accent color for visual storytelling.
 *
 * Usage:
 * <KineticText
 *   text="That moment felt like magic."
 *   fontSize={48}
 *   delay={10}
 *   stagger={4}
 *   emphasisWords={["magic"]}
 *   emphasisColor="#C4703F"
 * />
 */
import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

interface Props {
  text: string;
  delay?: number;
  fontSize?: number;
  fontFamily?: string;
  color?: string;
  emphasisWords?: string[];
  emphasisColor?: string;
  mode?: "wordByWord" | "fadeUp" | "lineReveal";
  stagger?: number;
  style?: React.CSSProperties;
  fontWeight?: number;
  lineHeight?: number;
  letterSpacing?: number;
  textAlign?: React.CSSProperties["textAlign"];
}

export const KineticText: React.FC<Props> = ({
  text,
  delay = 0,
  fontSize = 48,
  fontFamily = "Playfair Display",
  color = "#F5F0EB",
  emphasisWords = [],
  emphasisColor = "#C4703F",
  mode = "wordByWord",
  stagger = 3,
  style,
  fontWeight = 700,
  lineHeight = 1.3,
  letterSpacing = -0.5,
  textAlign = "center",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const CLAMP = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

  if (mode === "fadeUp") {
    const s = spring({ frame: frame - delay, fps, config: { damping: 15, stiffness: 100 } });
    const y = interpolate(s, [0, 1], [30, 0], CLAMP);
    const o = interpolate(s, [0, 1], [0, 1], CLAMP);
    return (
      <div style={{ fontSize, fontFamily, color, fontWeight, lineHeight, letterSpacing, textAlign, opacity: o, transform: `translateY(${y}px)`, ...style }}>
        {text}
      </div>
    );
  }

  if (mode === "lineReveal") {
    const lines = text.split("\n");
    return (
      <div style={{ textAlign, ...style }}>
        {lines.map((line, i) => {
          const s = spring({ frame: frame - delay - i * stagger * 3, fps, config: { damping: 14, stiffness: 100 } });
          const y = interpolate(s, [0, 1], [20, 0], CLAMP);
          return (
            <div key={i} style={{ fontSize, fontFamily, color, fontWeight, lineHeight, letterSpacing, opacity: interpolate(s, [0, 1], [0, 1], CLAMP), transform: `translateY(${y}px)` }}>
              {line}
            </div>
          );
        })}
      </div>
    );
  }

  // wordByWord
  const words = text.split(" ");
  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: textAlign === "center" ? "center" : "flex-start", gap: `0 ${fontSize * 0.28}px`, ...style }}>
      {words.map((word, i) => {
        const s = spring({ frame: frame - delay - i * stagger, fps, config: { damping: 14, stiffness: 120 } });
        const y = interpolate(s, [0, 1], [25, 0], CLAMP);
        const o = interpolate(s, [0, 1], [0, 1], CLAMP);
        const isEmphasis = emphasisWords.some((w) => word.toLowerCase().replace(/[^a-z]/g, "") === w.toLowerCase());
        return (
          <span key={i} style={{ fontSize, fontFamily, fontWeight, lineHeight, letterSpacing, color: isEmphasis ? emphasisColor : color, opacity: o, transform: `translateY(${y}px)`, display: "inline-block" }}>
            {word}
          </span>
        );
      })}
    </div>
  );
};
