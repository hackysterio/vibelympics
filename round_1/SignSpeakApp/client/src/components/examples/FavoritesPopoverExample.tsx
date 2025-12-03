import { useState } from 'react';
import FavoritesPopover from '../FavoritesPopover';
import { Button } from '@/components/ui/button';

export default function FavoritesPopoverExample() {
  const [isOpen, setIsOpen] = useState(true);
  const [favorites, setFavorites] = useState(['👋🙂', '🧑‍🦯🍎➡️🛒', '❤️🙏']);

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>
        <span>⭐</span>
      </Button>
      <FavoritesPopover
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        favorites={favorites}
        onSpeak={(phrase) => console.log('Speaking:', phrase)}
        onDelete={(index) => setFavorites(f => f.filter((_, i) => i !== index))}
        onSelect={(phrase) => console.log('Selected:', phrase)}
      />
    </>
  );
}
