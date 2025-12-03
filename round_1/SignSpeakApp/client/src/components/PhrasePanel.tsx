import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';

interface PhrasePanelProps {
  phrase: string;
  isSpeaking?: boolean;
}

export default function PhrasePanel({ phrase, isSpeaking }: PhrasePanelProps) {
  const emojis = Array.from(phrase);
  const isEmpty = emojis.length === 0;

  return (
    <div 
      className="h-32 md:h-40 flex items-center justify-center bg-card rounded-3xl mx-4 my-4 shadow-lg"
      data-testid="phrase-panel"
    >
      <ScrollArea className="w-full h-full">
        <div className="flex items-center justify-center min-h-[7rem] md:min-h-[9rem] px-6 py-4">
          {isEmpty ? (
            <div className="flex items-center gap-3 text-muted-foreground opacity-50">
              <span className="text-5xl md:text-7xl" role="img" aria-label="Point up">👆</span>
              <span className="text-5xl md:text-7xl" role="img" aria-label="Sparkle">✨</span>
            </div>
          ) : (
            <div 
              className={`flex flex-wrap items-center justify-center gap-1 text-5xl md:text-7xl transition-transform ${
                isSpeaking ? 'animate-pulse-speak' : ''
              }`}
            >
              {emojis.map((emoji, index) => (
                <span 
                  key={index} 
                  className="inline-block transition-transform hover:scale-110"
                  role="img"
                >
                  {emoji}
                </span>
              ))}
            </div>
          )}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </div>
  );
}
