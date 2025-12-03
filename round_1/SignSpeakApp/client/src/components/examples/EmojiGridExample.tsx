import EmojiGrid from '../EmojiGrid';

export default function EmojiGridExample() {
  return (
    <div className="h-64">
      <EmojiGrid
        category="👥"
        onEmojiClick={(emoji) => console.log('Emoji clicked:', emoji)}
      />
    </div>
  );
}
