# SignSpeak - Vibelympics Entry

An emoji-only sign language communication web app where users tap emoji "signs" and the app converts them to speech using the Web Speech API.

## Features

- **Emoji-Only UI**: Absolutely no text visible in the interface - everything is communicated through emojis
- **Text-to-Speech**: Converts emoji sequences to spoken sentences using Web Speech API
- **Smart Interpretation**: 40+ predefined emoji-to-sentence mappings with grammar-based fallback
- **Favorites System**: Save frequently used phrases for quick access
- **History Tracking**: Automatically saves recent phrases
- **Mobile-First Design**: Optimized for touch devices with large tap targets
- **Containerized**: Chainguard-based Docker container for secure deployment

## How It Works

1. Tap emojis from the categorized keyboard to build a phrase
2. Press the speaker button to hear the phrase spoken aloud
3. Save favorites with the star button
4. Clear or delete emojis using the action bar

## Running Locally

### Development Mode

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at http://localhost:5000

### Production Build

```bash
# Build for production
npm run build
```

## Docker Container (Chainguard)

This app uses secure, minimal [Chainguard](https://chainguard.dev) container images:
- **Build stage**: `cgr.dev/chainguard/node` - Node.js for building the app
- **Production stage**: `cgr.dev/chainguard/nginx` - Minimal nginx for serving static files

### Build the Container

```bash
docker build -t signspeak .
```

### Run the Container

```bash
docker run -p 8080:8080 signspeak
```

The app will be available at http://localhost:8080

### From GitHub

```bash
# Clone the repository
git clone https://github.com/hackysterio/vibelympics
cd vibelympics/round_1

# Build and run
docker build -t signspeak .
docker run -p 8080:8080 signspeak
```

## Technical Notes

### Emoji-Only UI Constraint

The entire UI uses emojis exclusively for all navigation, actions, and feedback:
- Navigation: 🏁 (home), 🎧/🔇 (TTS toggle), ⭐ (favorites)
- Categories: 👥 (people), 🍔 (food), 🚕 (transport), ❤️ (emotions), ⚕️ (health), 😀 (expressions)
- Actions: 🔊/⏹️ (speak/stop), ⌫ (delete), 🗑️ (clear), ⭐ (save), 📤 (share)

### Web Speech API

The app requires browser support for the Web Speech API (SpeechSynthesis). Supported in:
- Chrome 33+
- Firefox 49+
- Safari 7+
- Edge 14+

### Interpretation Engine

1. **Exact Match**: Checks predefined mappings in `mappings.json`
2. **Grammar Fallback**: Tokenizes emojis and constructs sentences based on emoji meanings

### Local Storage

The app persists:
- Favorites list
- Recent history (last 20 phrases)
- TTS enabled/disabled state

## Project Structure

```
├── client/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── data/          # Emoji mappings and categories
│   │   ├── hooks/         # Custom React hooks
│   │   └── lib/           # Interpreter logic
│   └── index.html
├── server/                 # Express backend
├── Dockerfile             # Chainguard container
└── README.md
```

## Vibelympics Compliance

- ✅ Emoji-only visible UI (no text)
- ✅ Fully functional
- ✅ Containerized using Chainguard
- ✅ Weird / vibey / creative

## License

MIT
