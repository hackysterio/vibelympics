import PhrasePanel from '../PhrasePanel';

export default function PhrasePanelExample() {
  return (
    <div className="space-y-4">
      <PhrasePanel phrase="👋🙂❤️" isSpeaking={false} />
      <PhrasePanel phrase="" isSpeaking={false} />
    </div>
  );
}
