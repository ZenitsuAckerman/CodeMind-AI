# Component Library

The CodeMind frontend employs a custom implementation of structural UI components inspired by `shadcn/ui`, tailored specifically to fit the "Timeless Software" design principles.

## Core Principles
- **No AI Clichés:** Components prioritize functionality and data density over flashy gradients.
- **Micro-interactions:** Interactive components (Buttons, Links, NavItems) feature extremely subtle state changes (`transition-all duration-200`).
- **Composition:** Complex layouts are built by composing small, single-responsibility components (e.g., `AppLayout` is just a composition of `Sidebar`, `Header`, and `Outlet`).

## Component Categories

### UI Primitives (`components/ui`)
- **Button:** Powered by `cva` (Class Variance Authority) to support variants (`primary`, `outline`, `ghost`, `destructive`) and sizes (`default`, `sm`, `icon`).

### Layout & Navigation (`components/layout`, `components/navigation`)
- **Sidebar:** Managed via global Zustand state to handle expansive vs collapsed views without prop-drilling.
- **Header:** Contains contextual Breadcrumbs reflecting the active router state.
- **Command Palette:** A global search overlay built with Framer Motion to provide instantaneous navigation and action execution.

### Feedback States (`components/feedback`)
- **EmptyState:** Provides calm, instructive feedback when no data is present.
- **LoadingState:** Uses standard un-intrusive spinners rather than complex skeleton screens unless rendering dense data tables.
- **ErrorState:** Provides clear boundaries and recovery actions (retries) when something fails.
