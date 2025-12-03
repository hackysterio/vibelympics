import { Button } from '@/components/ui/button';

interface TopBarProps {
  ttsEnabled: boolean;
  onTtsToggle: () => void;
  onHomeClick: () => void;
  onFavoritesClick: () => void;
}

export default function TopBar({ ttsEnabled, onTtsToggle, onHomeClick, onFavoritesClick }: TopBarProps) {
  return (
    <header 
      className="h-16 flex items-center justify-between px-4 bg-card/50 backdrop-blur-sm border-b border-border/50 sticky top-0 z-50"
      data-testid="topbar"
    >
      <Button
        variant="ghost"
        size="icon"
        onClick={onHomeClick}
        className="text-4xl w-14 h-14"
        data-testid="button-home"
        aria-label="Home"
      >
        <span role="img" aria-label="Home">🏁</span>
      </Button>

      <Button
        variant="ghost"
        size="icon"
        onClick={onTtsToggle}
        className="text-4xl w-14 h-14"
        data-testid="button-tts-toggle"
        aria-label={ttsEnabled ? 'Disable speech' : 'Enable speech'}
      >
        <span role="img" aria-label={ttsEnabled ? 'Sound on' : 'Sound off'}>
          {ttsEnabled ? '🎧' : '🔇'}
        </span>
      </Button>

      <Button
        variant="ghost"
        size="icon"
        onClick={onFavoritesClick}
        className="text-4xl w-14 h-14"
        data-testid="button-favorites"
        aria-label="Favorites"
      >
        <span role="img" aria-label="Favorites">⭐</span>
      </Button>
    </header>
  );
}
