import { Button } from '@/components/ui/button';
import { useState } from 'react';

interface ActionBarProps {
  onSpeak: () => void;
  onStop: () => void;
  onDelete: () => void;
  onClear: () => void;
  onSaveFavorite: () => void;
  isSpeaking: boolean;
  hasPhrase: boolean;
}

export default function ActionBar({
  onSpeak,
  onStop,
  onDelete,
  onClear,
  onSaveFavorite,
  isSpeaking,
  hasPhrase,
}: ActionBarProps) {
  const [showSparkle, setShowSparkle] = useState(false);

  const handleSaveFavorite = () => {
    setShowSparkle(true);
    onSaveFavorite();
    setTimeout(() => setShowSparkle(false), 400);
  };

  return (
    <div 
      className="h-24 flex items-center justify-center gap-4 px-4 bg-card/50 backdrop-blur-sm border-t border-border/50 sticky bottom-0 z-50"
      data-testid="action-bar"
    >
      <Button
        variant="ghost"
        size="icon"
        onClick={onDelete}
        disabled={!hasPhrase}
        className="text-3xl w-14 h-14 disabled:opacity-30"
        data-testid="button-delete"
        aria-label="Delete last emoji"
      >
        <span role="img" aria-label="Delete">⌫</span>
      </Button>

      <Button
        variant="ghost"
        size="icon"
        onClick={onClear}
        disabled={!hasPhrase}
        className="text-3xl w-14 h-14 disabled:opacity-30"
        data-testid="button-clear"
        aria-label="Clear all"
      >
        <span role="img" aria-label="Clear">🗑️</span>
      </Button>

      <Button
        variant="default"
        size="icon"
        onClick={isSpeaking ? onStop : onSpeak}
        disabled={!hasPhrase && !isSpeaking}
        className={`text-5xl w-20 h-20 rounded-full shadow-lg disabled:opacity-30 ${
          isSpeaking ? 'animate-pulse-speak bg-destructive hover:bg-destructive/90' : ''
        }`}
        data-testid="button-speak"
        aria-label={isSpeaking ? 'Stop speaking' : 'Speak phrase'}
      >
        <span role="img" aria-label={isSpeaking ? 'Stop' : 'Speak'}>
          {isSpeaking ? '⏹️' : '🔊'}
        </span>
      </Button>

      <Button
        variant="ghost"
        size="icon"
        onClick={handleSaveFavorite}
        disabled={!hasPhrase}
        className={`text-3xl w-14 h-14 disabled:opacity-30 ${
          showSparkle ? 'animate-sparkle' : ''
        }`}
        data-testid="button-save-favorite"
        aria-label="Save to favorites"
      >
        <span role="img" aria-label="Save favorite">⭐</span>
      </Button>

      <Button
        variant="ghost"
        size="icon"
        onClick={() => {
          if (navigator.share && hasPhrase) {
            navigator.share({ text: 'Check out my SignSpeak message!' });
          }
        }}
        disabled={!hasPhrase}
        className="text-3xl w-14 h-14 disabled:opacity-30"
        data-testid="button-share"
        aria-label="Share"
      >
        <span role="img" aria-label="Share">📤</span>
      </Button>
    </div>
  );
}
