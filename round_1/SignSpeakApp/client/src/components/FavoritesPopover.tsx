import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { VisuallyHidden } from '@radix-ui/react-visually-hidden';

interface FavoritesPopoverProps {
  isOpen: boolean;
  onClose: () => void;
  favorites: string[];
  onSpeak: (phrase: string) => void;
  onDelete: (index: number) => void;
  onSelect: (phrase: string) => void;
}

export default function FavoritesPopover({
  isOpen,
  onClose,
  favorites,
  onSpeak,
  onDelete,
  onSelect,
}: FavoritesPopoverProps) {
  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent 
        className="max-w-md w-[90vw] max-h-[80vh] p-0 rounded-3xl overflow-hidden"
        data-testid="favorites-popover"
      >
        <VisuallyHidden>
          <DialogTitle>Favorites</DialogTitle>
        </VisuallyHidden>
        
        <div className="flex items-center justify-center p-4 border-b border-border/50 bg-card">
          <span className="text-4xl" role="img" aria-label="Favorites">⭐</span>
        </div>

        <ScrollArea className="max-h-96">
          <div className="p-4 space-y-3">
            {favorites.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
                <span className="text-6xl mb-4 opacity-50" role="img">📭</span>
              </div>
            ) : (
              favorites.map((phrase, index) => (
                <div 
                  key={index}
                  className="flex items-center gap-3 p-4 bg-muted/50 rounded-2xl animate-fade-in"
                  data-testid={`favorite-item-${index}`}
                >
                  <Button
                    variant="ghost"
                    onClick={() => {
                      onSelect(phrase);
                      onClose();
                    }}
                    className="flex-1 text-3xl justify-start h-auto py-2 px-3 hover-elevate"
                    data-testid={`button-select-favorite-${index}`}
                  >
                    <span className="truncate">{phrase}</span>
                  </Button>

                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => onSpeak(phrase)}
                    className="text-2xl w-12 h-12 flex-shrink-0"
                    data-testid={`button-speak-favorite-${index}`}
                    aria-label="Speak this favorite"
                  >
                    <span role="img" aria-label="Speak">🔊</span>
                  </Button>

                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => onDelete(index)}
                    className="text-2xl w-12 h-12 flex-shrink-0 hover:bg-destructive/20"
                    data-testid={`button-delete-favorite-${index}`}
                    aria-label="Delete this favorite"
                  >
                    <span role="img" aria-label="Delete">🗑️</span>
                  </Button>
                </div>
              ))
            )}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
