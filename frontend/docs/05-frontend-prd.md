# CodeMind: Frontend Product Requirements Document (PRD)

## 1. Product Vision & Positioning

CodeMind is a premium retrieval-augmented generation (RAG) tool designed specifically for software engineers. It treats entire code repositories as a unified knowledge base, allowing developers to ask complex architectural and logic questions and receive precisely cited answers.

**Core Positioning:**
- **Software First, Intelligence Second:** The UI must feel like a native IDE or high-end developer tool (e.g., Linear, Raycast, Vercel). CodeMind is an application that happens to use AI, not an "AI application".
- **Anti-Marketing Aesthetic:** Zero sparkles (✨), zero brain icons, zero neon gradients. 
- **Timeless Design:** Monochromatic color scales, exceptional typography (Geist), negative space as a primary layout tool, and purposeful, snappy motion (160–220ms).

---

## 2. Target Audience & Personas

- **The Senior Engineer (Primary):** Needs to onboard onto massive, legacy, or complex codebases quickly. Values exact file citations and line numbers over generic summaries. Has zero tolerance for latency or layout shifts.
- **The Architect:** Evaluates system boundaries and dependencies. Needs holistic answers across multiple repositories or microservices.
- **The Code Reviewer:** Uses CodeMind to understand the blast radius of a pull request.

---

## 3. Frontend Architecture

### 3.1 Stack
- **Framework:** React 19 (via Vite).
- **Language:** TypeScript (Strict mode enabled, no `any`).
- **Styling:** Tailwind CSS v4 (Custom `@theme` configuration, zero utility-bloat).
- **State Management (Client):** Zustand (For transient UI state like sidebar toggles, command palette visibility).
- **State Management (Server):** TanStack Query (React Query) for fetching, caching, synchronizing, and updating server state.
- **Routing:** React Router v7.
- **Motion:** Framer Motion (Strict duration constraints: `0.15s` - `0.22s`, `easeOut` curves).
- **Forms & Validation:** React Hook Form + Zod.

### 3.2 Directory Structure
```text
frontend/
├── src/
│   ├── components/
│   │   ├── ui/          # Low-level primitives (Button, Input, Card)
│   │   ├── layout/      # App layouts (Sidebar, Header)
│   │   ├── navigation/  # Breadcrumbs, Links
│   │   ├── workspace/   # Domain-specific structural wrappers
│   │   ├── search/      # Command Palette, Search inputs
│   │   ├── feedback/    # EmptyState, ErrorState, LoadingState
│   │   └── shared/      # Reusable composed components (ThemeToggle)
│   ├── features/        # Business logic domains (auth, chat, projects)
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Pure utilities (axios instance, tailwind cn merger)
│   ├── providers/       # Context Providers (Theme, QueryClient, Router)
│   ├── routes/          # Top-level page components mapping to URLs
│   └── store/           # Zustand global stores
```

---

## 4. Design System & UX Guidelines

### 4.1 Typography
- **Primary Font:** Geist (Sans).
- **Code/Data Font:** Geist Mono.
- **Hierarchy Rules:** Hierarchy is established through font-weight and color contrast (e.g., `text-foreground` vs `text-muted-foreground`) rather than excessive font-size variations.

### 4.2 Color Palette
- **Monochrome Dominance:** The UI operates on a strictly neutral grayscale (Tailwind's `zinc` or `gray`). 
- **The Accent:** A singular, vibrant blue (`#0070F3`). Used exclusively for primary actions, focus states, and selection indicators. No secondary or tertiary brand colors.
- **Dark Mode:** Deep blacks (`#000000`) for the background, with `rgba(255, 255, 255, 0.1)` inset shadows to create depth without relying on harsh drop shadows.

### 4.3 Motion constraints
- Animations must reflect precision engineering.
- **Duration:** 160ms (micro-interactions) to 220ms (layout shifts).
- **Easing:** `easeOut` (`cubic-bezier(0.0, 0.0, 0.2, 1)`).
- **Banned:** Bouncing (springs with low damping), pulsating, arbitrary floating.

### 4.4 Component Engineering Standards
- **Headless First:** UI primitives are built atop robust accessibility primitives (e.g., Radix UI via `shadcn/ui` patterns).
- **CVA:** Component variants (e.g., Button sizes/colors) are strictly managed via `class-variance-authority`.
- **Focus Rings:** Global, consistent focus rings (`focus-visible:ring-1 focus-visible:ring-ring`) are mandatory. Keyboard navigation must be flawless.

---

## 5. Core Features & UX Flows

### 5.1 Global Application Shell
- **Sidebar:** Collapsible (260px expanded, 64px collapsed). Contains workspace navigation (Projects, Settings). Handled globally via Zustand.
- **Header:** Contextual breadcrumbs reflecting the exact route depth.
- **Command Palette (⌘K):** The central nervous system of the app. Accessible from anywhere. Used for navigating between projects, executing quick actions, and jumping to settings.

### 5.2 Authentication (Sprint 3)
- **UX Flow:** Minimalist login/register screens. No marketing fluff. Email/Password standard inputs with immediate inline Zod validation.
- **Technical:** JWT-based. Tokens stored securely. Axios interceptors automatically handle `401 Unauthorized` responses by redirecting to `/login` and triggering a silent refresh if applicable.

### 5.3 Workspace & Project Management (Sprint 4)
- **Dashboard:** A grid or list view of active projects (repositories).
- **Project Detail View:** Displays indexing status (Syncing, Indexed, Failed), recent queries, and repository metadata.
- **Empty States:** Highly intentional `EmptyState` components with Lucide icons guiding the user to connect their first repository.

### 5.4 The AI Chat Interface (Sprint 5)
- **UX Flow:** The core utility. Modeled after IDE split-panes.
- **Input:** A multi-line textarea that auto-expands. Supports `Enter` to submit, `Shift+Enter` for newlines.
- **Response Streaming:** UI must support streaming responses for low Time-To-First-Token (TTFT). 
- **Citations:** The most critical feature. When the model references a file, the frontend renders an interactive, inline citation block (e.g., `src/utils/auth.ts`). Clicking the citation opens a code-viewer modal or side-panel showing the exact chunk retrieved from Qdrant.
- **Markdown Parsing:** Full support for GitHub Flavored Markdown, syntax highlighting for code blocks (using `shiki` or `prism`), and tables.

---

## 6. Engineering Requirements

### 6.1 Performance
- **Zero Layout Shift (CLS):** Loading states must perfectly match the dimensions of the final content (via Skeleton components) to prevent layout jumping.
- **Bundle Size:** Lazy load heavy dependencies (e.g., Syntax highlighters, Markdown parsers) at the route level.

### 6.2 Error Handling
- **API Errors:** Global Axios interceptor catches non-200 responses. Toast notifications (via `sonner`) inform the user of transient errors.
- **React Error Boundaries:** Top-level route error boundaries catch rendering crashes and display the `ErrorState` component with a "Reload Application" action.

### 6.3 Accessibility (a11y)
- **ARIA Attributes:** Mandatory for all custom interactive elements.
- **Contrast:** Strict adherence to WCAG AA contrast ratios (4.5:1 for normal text).
- **Screen Readers:** Hidden "Skip to main content" links and properly structured semantic HTML (`<main>`, `<nav>`, `<aside>`).

---

## 7. Sprint Roadmap

- **Sprint 1:** Landing Experience (Completed).
- **Sprint 2:** Application Shell (Completed).
- **Sprint 3:** Authentication Flow (Login, Register, JWT integration).
- **Sprint 4:** Project Management (Dashboard, Creation, Document List).
- **Sprint 5:** AI Chat Interface (Markdown rendering, Streaming, Citations).
- **Sprint 6:** Settings & Polish (Profile management, advanced configuration).

---
*This document acts as the immutable source of truth for the CodeMind frontend team. Any deviations from the design system or architectural patterns must be formally proposed and merged into this document.*
