# Frontend Architecture

## Overview
The CodeMind frontend is built with React 19, TypeScript, and Vite. It heavily relies on a component-driven architecture, separating concerns into strict modular domains.

## Directory Structure
- `src/components/`: The core UI building blocks.
  - `ui/`: Base primitives (Buttons, Inputs, Cards).
  - `layout/`: Global wrappers (`AppLayout`, `Header`, `Sidebar`).
  - `navigation/`: Links and breadcrumbs.
  - `search/`: Global search utilities (`CommandPalette`).
  - `feedback/`: Empty, Loading, and Error states.
  - `shared/`: Reusable cross-domain components (`ThemeToggle`).
- `src/store/`: Global client-side state management using Zustand.
- `src/routes/`: Top-level page components and layouts.
- `src/lib/`: Reusable utilities (e.g., Tailwind `cn` merger).

## State Management
- **Zustand**: Used for global UI state (Sidebar collapse state, Command Palette visibility).
- **TanStack Query (Planned)**: Will be used for all server state (API fetching, caching, mutations).
- **React Hook Form**: For complex form state and validation.

## Routing
- We use React Router's `<BrowserRouter>` with nested routes.
- The `<AppLayout>` acts as a wrapper around the `<Outlet />` for all authenticated application routes, maintaining the persistent Sidebar and Header.
