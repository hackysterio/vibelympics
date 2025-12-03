import { useState } from 'react';
import ActionBar from '../ActionBar';

export default function ActionBarExample() {
  const [isSpeaking, setIsSpeaking] = useState(false);

  return (
    <ActionBar
      onSpeak={() => setIsSpeaking(true)}
      onStop={() => setIsSpeaking(false)}
      onDelete={() => console.log('Delete')}
      onClear={() => console.log('Clear')}
      onSaveFavorite={() => console.log('Save favorite')}
      isSpeaking={isSpeaking}
      hasPhrase={true}
    />
  );
}
