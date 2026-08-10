# Frontend Design Principles

This document outlines the core aesthetic and functional design principles for the CodeMind frontend. CodeMind is a premium developer tool, and its UI must reflect the maturity and precision of modern software engineering.

## 1. The Anti-"AI-Website" Philosophy

While CodeMind uses advanced retrieval-augmented generation to power its features, **AI is a capability, not the identity.**
- **No AI Clichés:** We strictly avoid robot icons, brain graphics, neural network backgrounds, sparkles (✨), or glowing chips.
- **No Neon Gradients:** We do not use "futuristic" purple/pink/cyan gradients or heavy glassmorphism designed to look "cyberpunk".
- **Focus on Utility:** The interface should look and function like a native, professional IDE or productivity app (e.g., Linear, Arc, Raycast).

## 2. Visual Language

- **Monochrome Foundation:** The primary interface utilizes grayscale colors (`zinc` or `gray` neutral tones). Contrast is used to establish hierarchy rather than color.
- **Single Accent Color:** We use a single, premium blue (`#0070F3` or similar) to indicate primary actions, focus states, and active selections.
- **Subtle Elevation:** Harsh drop-shadows are avoided. Instead, we use very subtle, diffuse shadows combined with 1px borders to separate layers (e.g., floating navs, modal windows). In dark mode, we use `box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.1)` to define top edges.
- **Soft Borders:** Rounded corners are used purposefully. Modals/Cards use `rounded-xl` or `rounded-lg`, while smaller interactive elements use `rounded-md`.

## 3. Typography

- **Geist & Geist Mono:** We use Vercel's Geist font family exclusively. It provides exceptional legibility and a modern, geometric feel that screams "developer tool."
- **Spacious Layouts:** Whitespace is a primary design element. High line-heights (`leading-relaxed`) and large margins separate distinct ideas.
- **Hierarchy:** We rely heavily on font weights (`font-medium`, `font-semibold`) and color muting (`text-muted-foreground`) to establish visual hierarchy without altering font size excessively.

## 4. Motion and Interaction

- **Purposeful Animation:** Animations must be fast, subtle, and tied to user intent. 
- **Framer Motion Constraints:** Transitions should feel snappy. The standard transition is `duration: 0.2` (200ms) with an `easeOut` curve.
- **No Decorative Animations:** Elements should not pulse, bounce, or float aimlessly without interaction.

## 5. UI Primitives

- **Lucide Icons:** Used exclusively for all iconography. Line weight must remain consistent.
- **Buttons:** Solid, geometric, with slight hover states. No heavy shadows or active state shrinking unless functionally necessary.
- **Mock Windows:** Any product preview or documentation utilizing fake application windows must accurately reflect a realistic state (file trees, code syntax, precise citations) rather than abstract visual representations.
