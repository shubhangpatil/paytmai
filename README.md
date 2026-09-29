# Paytm AI: Voice & Memory for 30 Million Shopkeepers

Production-grade, interactive web application built for the **Paytm Build for India AI Hackathon (Mumbai Edition)**.

## 🌟 Key Features

- **4-Page Seamless Interface**:
  - `index.html`: Home page featuring metallic specular shining animation and smooth auto-redirection.
  - `dashboard.html`: Unified tracks view combining Merchant Co-Pilot, JanSuraksha Micro-Claims, and OpsGuard AI Agent.
  - `notifications.html`: Real-time system alert feed with notification bell and live simulation controls.
  - `about.html`: Project summary, architecture details, and developer contact section.
- **Multilingual Voice Engine**: Supports 7 Indian regional languages (`Hindi` default, `English`, `Telugu`, `Tamil`, `Kannada`, `Gujarati`, `Marathi`) with authentic Indian accent speech synthesis via Web Speech API.
- **Fintech Payment Flow Animations**: Realistic payment processing overlays (`Connecting to Paytm Gateway...`, `Verifying Fraud Score...`) transitioning into success states with flying banknote particle effects and dual-tone Soundbox chimes.
- **Anti-Container Design System**: Modern fluid drop-ribbons without rigid box boundaries, paired with delayed backdrop-blur dialogs.

## 🚀 Quick Start

To launch the project locally:

```bash
# Clone the repository
git clone https://github.com/ksuchirreddy/paytmai.git
cd paytmai

# Start local HTTP server
python3 -m http.server 8080
```

Open `http://localhost:8080/index.html` in your browser.

## 📁 Repository Structure

```
├── index.html           # Landing page with specular shining title
├── dashboard.html       # Main tracks interface (vyapardost, jansuraksha, opsguard)
├── notifications.html   # Live system alerts & notifications stream
├── about.html           # About project & developer contact
├── assets/              # UI mockups & generated visual artifacts
```
