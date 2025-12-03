# SignSpeak Design Guidelines

## Design Approach: Minimal Icon-First Communication Interface

**Core Principle**: Create an intuitive, emoji-only visual language system that feels like a specialized communication tool, not a typical web app. Draw inspiration from accessibility tools and modern messaging interfaces while maintaining zero visible text.

## Critical Design Constraints

**Emoji-Only Rule**: Absolutely NO text visible anywhere in the UI. All navigation, actions, labels, and feedback must use emojis exclusively. This is non-negotiable.

## Layout Architecture

**Mobile-First Structure** (320px - 768px primary, desktop enhances):

1. **Top Navigation Bar** (h-16 fixed top)
   - 🏁 (home/reset) - left aligned
   - 🎧/🔇 (TTS toggle) - center
   - ⭐ (favorites) - right aligned
   - Full-width, subtle separator below

2. **Phrase Display Panel** (h-32 to h-40)
   - Large emoji sequence display (text-6xl to text-8xl)
   - Horizontally scrollable for long sequences
   - Centered vertically and horizontally
   - Subtle container with rounded corners

3. **Category Tabs** (h-14)
   - Horizontal scroll of emoji category buttons
   - 👥 🍔 🚕 ❤️ ⚕️ 😀 (each text-3xl)
   - Active tab gets prominent visual treatment
   - Smooth slide indicator underneath

4. **Emoji Grid** (flex-1, main content area)
   - 4-5 columns on mobile, 6-8 on tablet, 8-10 on desktop
   - Large tap targets (min 64px × 64px)
   - Generous padding between emojis (p-3 to p-4)
   - Smooth scroll, no pagination

5. **Action Bar** (h-20, fixed bottom)
   - Primary actions: 🔊/⏹️ (speak, largest, center)
   - Secondary: ⌫ (delete) | 🗑️ (clear) | ⭐ (save)
   - Generous spacing between actions

## Typography & Sizing

**Emoji Scale Hierarchy**:
- Phrase Display: text-6xl to text-8xl (96px-128px)
- Category Tabs: text-3xl (48px)
- Emoji Grid: text-4xl to text-5xl (56px-72px)
- Action Bar: text-5xl (72px) for primary, text-3xl (48px) for secondary
- Navigation: text-3xl (48px)

## Spacing System

Use Tailwind units: **4, 6, 8, 12, 16** for consistency
- Component padding: p-4 to p-6
- Section gaps: gap-4 to gap-8
- Button spacing: space-x-4 or space-x-6
- Container margins: mx-4 on mobile, mx-auto max-w-6xl on desktop

## Component Specifications

**Emoji Buttons**:
- Large, circular or soft-rounded (rounded-2xl) containers
- Ample touch target (min-h-16 min-w-16)
- Subtle depth through shadows, not borders
- Emoji centered within button

**Phrase Panel**:
- Prominent container (rounded-3xl, subtle depth)
- Generous padding (p-6 to p-8)
- Emoji sequence flows left-to-right, wraps naturally
- Empty state shows placeholder emoji like 👆 or ✨

**Action Buttons**:
- Speak button (🔊): Largest, most prominent (w-20 h-20)
- Stop button (⏹️): Same size, replaces speak when active
- Utility buttons: Smaller but still generous (w-14 h-14)
- Circular shape for primary actions

**Favorites Popover**:
- Slides up from bottom or drops from ⭐ button
- Shows emoji sequences in cards (rounded-2xl)
- Each card: emoji sequence + 🔊 + 🗑️ actions
- Scrollable if many favorites, max-h-96

**Category Tabs**:
- Horizontal scroll container
- Active tab: elevated appearance, distinct visual state
- Inactive tabs: muted/transparent appearance
- Slide indicator beneath active tab

## Animations & Interactions

**Micro-Animations** (use sparingly, keep smooth):
- 🔊 Speak: Gentle pulse during speech (scale 1.0 to 1.1, 1.5s ease)
- ⭐ Save: Quick sparkle/scale animation (scale up to 1.3, snap back)
- Emoji button tap: Subtle scale down (0.95) on press
- Category tab switch: Smooth slide of indicator (300ms ease)
- Popover: Slide-up with slight bounce (spring animation)

**Transitions**:
- All state changes: 200-300ms ease
- No jarring movements
- Respect reduced motion preferences

## Visual Depth & Hierarchy

**Layering Strategy**:
- Navigation & action bars: Highest layer (z-50)
- Popovers/modals: High layer (z-40)
- Phrase panel: Elevated (z-10)
- Emoji grid: Base layer (z-0)

**Depth Through Shadows**:
- Elevated elements: Soft, larger shadows
- Interactive elements: Sharper, smaller shadows
- Containers: Very subtle shadows for definition
- No borders - use shadows and background contrast exclusively

## Responsive Behavior

**Breakpoints**:
- Mobile: 320px-640px (base styles)
- Tablet: 640px-1024px (md:)
- Desktop: 1024px+ (lg:)

**Adaptive Grid**:
- Mobile: 4 emoji columns, compact spacing
- Tablet: 6-7 columns, increased spacing
- Desktop: 8-10 columns, generous spacing, centered max-width container

**Touch Targets**:
- Minimum 44px × 44px everywhere
- Prefer 56px-64px for primary interactive elements
- Generous spacing between touch targets (min 8px gaps)

## Accessibility (Beyond Color)

- All interactive elements have focus states (ring with offset)
- Keyboard navigation: Tab through all controls
- Emoji buttons announce emoji name via aria-label
- Speech synthesis status communicated through visual changes (🔊 ↔ ⏹️)
- High contrast between interactive and static elements
- Size differentiation for importance hierarchy

## Images

**No Hero Images**: This is a utility app focused on communication, not marketing. No decorative images needed - emoji are the visual language throughout.

---

**Design Philosophy**: Create a specialized tool that feels purposeful and accessible. The emoji-only constraint is a feature, not a limitation - lean into it to create a unique, memorable interface that communicates through universal symbols.