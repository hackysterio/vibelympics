import mappings from '../data/mappings.json';

const emojiMeanings: Record<string, { subject?: boolean; action?: boolean; object?: boolean; meaning: string }> = {
  '👋': { action: true, meaning: 'wave hello' },
  '🙂': { meaning: 'happy' },
  '😀': { meaning: 'happy' },
  '😢': { meaning: 'sad' },
  '😴': { meaning: 'tired' },
  '💤': { meaning: 'sleeping' },
  '🙏': { action: true, meaning: 'please' },
  '👍': { meaning: 'yes' },
  '👎': { meaning: 'no' },
  '❤️': { meaning: 'love' },
  '🤔': { meaning: 'thinking' },
  '🥵': { meaning: 'hot' },
  '🥶': { meaning: 'cold' },
  '💧': { object: true, meaning: 'water' },
  '🚰': { object: true, meaning: 'water tap' },
  '🍎': { object: true, meaning: 'apple' },
  '🍔': { object: true, meaning: 'burger' },
  '🍟': { object: true, meaning: 'fries' },
  '🥤': { object: true, meaning: 'drink' },
  '☕': { object: true, meaning: 'coffee' },
  '🍽️': { object: true, meaning: 'food' },
  '➡️': { action: true, meaning: 'go to' },
  '⬅️': { action: true, meaning: 'come from' },
  '🛒': { object: true, meaning: 'shopping' },
  '🏠': { object: true, meaning: 'home' },
  '🏥': { object: true, meaning: 'hospital' },
  '🚕': { object: true, meaning: 'taxi' },
  '🚗': { object: true, meaning: 'car' },
  '❗': { meaning: 'urgent' },
  '🚨': { meaning: 'emergency' },
  '🆘': { meaning: 'help' },
  '💊': { object: true, meaning: 'medicine' },
  '💉': { object: true, meaning: 'injection' },
  '🩺': { object: true, meaning: 'doctor' },
  '👨‍⚕️': { subject: true, meaning: 'doctor' },
  '👩‍⚕️': { subject: true, meaning: 'doctor' },
  '🧑‍🦯': { subject: true, meaning: 'I' },
  '🚽': { object: true, meaning: 'restroom' },
  '🧥': { object: true, meaning: 'jacket' },
  '📞': { action: true, meaning: 'call' },
  '👨‍👩‍👧': { object: true, meaning: 'family' },
  '🔑': { object: true, meaning: 'keys' },
  '📱': { object: true, meaning: 'phone' },
  '🔋': { object: true, meaning: 'battery' },
  '❌': { meaning: 'no' },
  '✅': { meaning: 'yes' },
  '❓': { meaning: 'question' },
  '💰': { object: true, meaning: 'money' },
  '⏰': { object: true, meaning: 'time' },
  '📍': { object: true, meaning: 'location' },
  '🛏️': { object: true, meaning: 'bed' },
  '🤢': { meaning: 'nauseous' },
  '🤮': { meaning: 'sick' },
  '🤕': { meaning: 'headache' },
  '🦵': { object: true, meaning: 'leg' },
  '😖': { meaning: 'pain' },
  '🥱': { meaning: 'bored' },
};

export function interpretEmojis(emojiSequence: string): string {
  const key = emojiSequence;
  if (mappings[key as keyof typeof mappings]) {
    return mappings[key as keyof typeof mappings];
  }

  const emojis = Array.from(emojiSequence);
  if (emojis.length === 0) return '';

  const parts: string[] = [];
  let hasSubject = false;

  for (const emoji of emojis) {
    const info = emojiMeanings[emoji];
    if (info) {
      if (info.subject && !hasSubject) {
        parts.unshift('I');
        hasSubject = true;
      } else if (info.action) {
        parts.push(info.meaning);
      } else if (info.object) {
        parts.push(info.meaning);
      } else {
        parts.push(info.meaning);
      }
    }
  }

  if (parts.length === 0) {
    return emojis.map(e => emojiMeanings[e]?.meaning || e).join(' ');
  }

  let sentence = parts.join(' ');
  sentence = sentence.charAt(0).toUpperCase() + sentence.slice(1);
  
  return sentence || 'I want to communicate';
}
