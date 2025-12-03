# SignSpeak - Emoji-Only Communication App

## Overview

SignSpeak is an emoji-only sign language communication web application that converts emoji sequences into spoken sentences using the Web Speech API. The app features a completely text-free interface where all communication, navigation, and feedback is delivered through emojis. Users tap emojis to build phrases, which are then interpreted and spoken aloud through intelligent emoji-to-sentence mapping.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework & Build System**
- React 18 with TypeScript for type-safe component development
- Vite as the build tool and development server for fast HMR and optimized production builds
- React Router (wouter) for lightweight client-side routing
- TanStack Query for server state management and caching

**UI Component System**
- Radix UI primitives for accessible, unstyled component foundations
- shadcn/ui component library built on Radix UI with Tailwind CSS styling
- Custom emoji-focused components with mobile-first responsive design
- TailwindCSS for utility-first styling with custom design tokens

**State Management Strategy**
- Local state with React hooks (useState, useCallback) for component-level state
- Custom hooks for reusable logic:
  - `useLocalStorage`: Persistent client-side storage for favorites and history
  - `useSpeechSynthesis`: Web Speech API integration for text-to-speech
  - `useToast`: User feedback via emoji-only toast notifications
- No global state management library needed due to simple data flow

**Emoji Interpretation System**
- Two-tier interpretation approach:
  1. Exact match lookups in `mappings.json` for predefined emoji sequences (40+ common phrases)
  2. Grammar-based fallback using `emojiMeanings` dictionary that categorizes emojis as subjects, actions, or objects
- Smart sentence construction when exact matches aren't found
- Supports complex multi-emoji phrases with contextual understanding

**Data Persistence**
- Browser LocalStorage for favorites and phrase history
- No backend database required for core functionality
- All user data stored client-side for privacy and offline capability

### Backend Architecture

**Server Framework**
- Express.js with TypeScript for API routes (currently minimal/placeholder)
- HTTP server setup via Node's `http` module
- Development hot-reload via Vite middleware integration

**Storage Abstraction**
- Interface-based storage design (`IStorage`) allows for future database integration
- Current implementation uses in-memory storage (`MemStorage`)
- Ready to swap to PostgreSQL via Drizzle ORM when needed

**Build & Deployment**
- ESBuild for server bundling with selective dependency bundling
- Separate client and server builds
- Production build outputs to `dist/` directory
- Chainguard-based Docker container support for secure deployment

### Key Architectural Decisions

**Emoji-Only Interface**
- Design constraint: Absolutely no visible text in the UI
- All navigation, actions, and feedback use emojis exclusively
- Accessibility through ARIA labels (text exists in markup, not visually)
- This creates a universal interface that transcends language barriers

**Mobile-First Design**
- Primary target: 320px-768px touch devices
- Large tap targets (minimum 64px × 64px) for accessibility
- Touch-optimized interactions with visual feedback
- Desktop serves as enhancement, not primary experience

**Client-Side Speech Synthesis**
- Browser's native Web Speech API eliminates need for external TTS services
- Zero latency for speech output
- Privacy-preserving (no audio sent to servers)
- Fallback messaging when API unavailable
- Trade-off: Voice quality and availability varies by browser/platform

**No Authentication Required**
- Completely client-side application for core features
- LocalStorage provides persistence without accounts
- User schema exists in codebase but currently unused
- Simplifies deployment and enhances privacy

**Static JSON Data Files**
- Emoji categories and mappings stored as JSON for easy editing
- No database queries needed for emoji data
- Fast load times and offline capability
- Trade-off: Requires rebuild to update emoji mappings (acceptable for this use case)

### Layout Structure

The app follows a fixed 5-section mobile layout:
1. **TopBar**: Navigation (home, TTS toggle, favorites)
2. **PhrasePanel**: Large display of current emoji sequence
3. **CategoryTabs**: Horizontally scrollable emoji category selector
4. **EmojiGrid**: Main interaction area with categorized emoji buttons
5. **ActionBar**: Primary actions (speak, delete, clear, save favorite)

## External Dependencies

### UI & Component Libraries
- **Radix UI**: Comprehensive set of unstyled, accessible React components (@radix-ui/react-*)
- **shadcn/ui**: Pre-built component system using Radix primitives
- **Lucide React**: Icon library for system icons
- **Tailwind CSS**: Utility-first CSS framework with PostCSS

### State & Data Management
- **TanStack Query (React Query)**: Server state management and caching
- **Wouter**: Lightweight React routing library
- **React Hook Form** with **Zod resolvers**: Form handling and validation (infrastructure present but not actively used)

### Database & ORM
- **Drizzle ORM**: TypeScript ORM configured for PostgreSQL
- **@neondatabase/serverless**: PostgreSQL client for serverless environments
- **Drizzle-Zod**: Schema validation integration
- Note: Database configured but not actively used in current implementation

### Build Tools & Development
- **Vite**: Build tool and dev server with React plugin
- **ESBuild**: JavaScript bundler for production server builds
- **TypeScript**: Type checking and compilation
- **Replit plugins**: Dev banner, cartographer, and error overlay for Replit environment

### Runtime APIs
- **Web Speech API**: Browser-native text-to-speech (no external dependency)
- **LocalStorage API**: Browser-native client-side persistence

### Utility Libraries
- **clsx + tailwind-merge**: Conditional CSS class handling
- **class-variance-authority**: Type-safe variant styling
- **date-fns**: Date manipulation utilities

### Testing & Quality
- All components include data-testid attributes for testing
- Accessibility features via ARIA labels throughout