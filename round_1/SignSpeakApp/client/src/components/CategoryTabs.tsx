import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';

const CATEGORIES = ['👥', '🍔', '🚕', '❤️', '⚕️', '😀'] as const;

interface CategoryTabsProps {
  activeCategory: string;
  onCategoryChange: (category: string) => void;
}

export default function CategoryTabs({ activeCategory, onCategoryChange }: CategoryTabsProps) {
  return (
    <div className="h-16 border-b border-border/50 bg-card/30" data-testid="category-tabs">
      <ScrollArea className="w-full h-full">
        <div className="flex items-center justify-center gap-2 px-4 h-full min-w-max">
          {CATEGORIES.map((category) => (
            <Button
              key={category}
              variant={activeCategory === category ? 'default' : 'ghost'}
              size="icon"
              onClick={() => onCategoryChange(category)}
              className={`text-3xl w-12 h-12 transition-all ${
                activeCategory === category 
                  ? 'shadow-md scale-110' 
                  : 'opacity-70 hover:opacity-100'
              }`}
              data-testid={`button-category-${category}`}
              aria-label={`Category ${category}`}
              aria-pressed={activeCategory === category}
            >
              <span role="img">{category}</span>
            </Button>
          ))}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </div>
  );
}
