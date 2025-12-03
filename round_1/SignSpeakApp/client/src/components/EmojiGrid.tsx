import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import categories from '../data/categories.json';

interface EmojiGridProps {
  category: string;
  onEmojiClick: (emoji: string) => void;
}

export default function EmojiGrid({ category, onEmojiClick }: EmojiGridProps) {
  const categoryData = categories[category as keyof typeof categories];
  const emojis = categoryData?.emojis || [];

  return (
    <div className="flex-1 min-h-0" data-testid="emoji-grid">
      <ScrollArea className="h-full">
        <div className="grid grid-cols-4 sm:grid-cols-5 md:grid-cols-6 lg:grid-cols-8 gap-2 p-4">
          {emojis.map((emoji, index) => (
            <Button
              key={`${emoji}-${index}`}
              variant="ghost"
              onClick={() => onEmojiClick(emoji)}
              className="text-4xl md:text-5xl w-16 h-16 md:w-18 md:h-18 p-0 hover-elevate active-elevate-2 transition-transform active:scale-95"
              data-testid={`button-emoji-${index}`}
              aria-label={emoji}
            >
              <span role="img">{emoji}</span>
            </Button>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
