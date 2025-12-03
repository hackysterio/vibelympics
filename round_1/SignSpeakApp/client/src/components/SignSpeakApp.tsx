import { useState, useCallback } from 'react';
import TopBar from './TopBar';
import PhrasePanel from './PhrasePanel';
import CategoryTabs from './CategoryTabs';
import EmojiGrid from './EmojiGrid';
import ActionBar from './ActionBar';
import FavoritesPopover from './FavoritesPopover';
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis';
import { useLocalStorage } from '@/hooks/useLocalStorage';
import { interpretEmojis } from '@/lib/interpreter';
import { useToast } from '@/hooks/use-toast';

export default function SignSpeakApp() {
  const [phrase, setPhrase] = useState('');
  const [activeCategory, setActiveCategory] = useState('👥');
  const [showFavorites, setShowFavorites] = useState(false);
  const [ttsEnabled, setTtsEnabled] = useLocalStorage('signspeak-tts', true);
  const [favorites, setFavorites] = useLocalStorage<string[]>('signspeak-favorites', []);
  const [history, setHistory] = useLocalStorage<string[]>('signspeak-history', []);

  const { speak, stop, isSpeaking, isSupported } = useSpeechSynthesis();
  const { toast } = useToast();

  const handleEmojiClick = useCallback((emoji: string) => {
    setPhrase((prev) => prev + emoji);
  }, []);

  const handleSpeak = useCallback(() => {
    if (!phrase) return;

    if (!ttsEnabled) {
      toast({
        title: '🔇',
        description: '🎧 ➡️ 🔊',
      });
      return;
    }

    if (!isSupported) {
      toast({
        title: '❌',
        description: '🔊 ❌',
      });
      return;
    }

    const interpretation = interpretEmojis(phrase);
    speak(interpretation);

    setHistory((prev) => {
      const newHistory = [phrase, ...prev.filter((h) => h !== phrase)].slice(0, 20);
      return newHistory;
    });
  }, [phrase, ttsEnabled, isSupported, speak, toast, setHistory]);

  const handleStop = useCallback(() => {
    stop();
  }, [stop]);

  const handleDelete = useCallback(() => {
    setPhrase((prev) => {
      const chars = Array.from(prev);
      chars.pop();
      return chars.join('');
    });
  }, []);

  const handleClear = useCallback(() => {
    setPhrase('');
  }, []);

  const handleSaveFavorite = useCallback(() => {
    if (!phrase) return;

    if (favorites.includes(phrase)) {
      toast({
        title: '⭐',
        description: '✅',
      });
      return;
    }

    setFavorites((prev) => [phrase, ...prev].slice(0, 50));
    toast({
      title: '⭐',
      description: '✨',
    });
  }, [phrase, favorites, setFavorites, toast]);

  const handleHome = useCallback(() => {
    setPhrase('');
    setActiveCategory('👥');
    stop();
  }, [stop]);

  const handleFavoriteSpeak = useCallback((favoritePhrase: string) => {
    if (!ttsEnabled || !isSupported) return;
    const interpretation = interpretEmojis(favoritePhrase);
    speak(interpretation);
  }, [ttsEnabled, isSupported, speak]);

  const handleDeleteFavorite = useCallback((index: number) => {
    setFavorites((prev) => prev.filter((_, i) => i !== index));
  }, [setFavorites]);

  const handleSelectFavorite = useCallback((favoritePhrase: string) => {
    setPhrase(favoritePhrase);
  }, []);

  return (
    <div className="h-screen flex flex-col bg-background overflow-hidden">
      <TopBar
        ttsEnabled={ttsEnabled}
        onTtsToggle={() => setTtsEnabled(!ttsEnabled)}
        onHomeClick={handleHome}
        onFavoritesClick={() => setShowFavorites(true)}
      />

      <PhrasePanel phrase={phrase} isSpeaking={isSpeaking} />

      <CategoryTabs
        activeCategory={activeCategory}
        onCategoryChange={setActiveCategory}
      />

      <EmojiGrid
        category={activeCategory}
        onEmojiClick={handleEmojiClick}
      />

      <ActionBar
        onSpeak={handleSpeak}
        onStop={handleStop}
        onDelete={handleDelete}
        onClear={handleClear}
        onSaveFavorite={handleSaveFavorite}
        isSpeaking={isSpeaking}
        hasPhrase={phrase.length > 0}
      />

      <FavoritesPopover
        isOpen={showFavorites}
        onClose={() => setShowFavorites(false)}
        favorites={favorites}
        onSpeak={handleFavoriteSpeak}
        onDelete={handleDeleteFavorite}
        onSelect={handleSelectFavorite}
      />
    </div>
  );
}
