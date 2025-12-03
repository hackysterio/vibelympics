import { useState } from 'react';
import TopBar from '../TopBar';

export default function TopBarExample() {
  const [ttsEnabled, setTtsEnabled] = useState(true);

  return (
    <TopBar
      ttsEnabled={ttsEnabled}
      onTtsToggle={() => setTtsEnabled(!ttsEnabled)}
      onHomeClick={() => console.log('Home clicked')}
      onFavoritesClick={() => console.log('Favorites clicked')}
    />
  );
}
