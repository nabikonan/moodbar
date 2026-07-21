const messages = {
  content: [
    "Super, continue comme ça !",
    "Ravi de voir ça, belle journée !",
    "Ton énergie fait plaisir à voir."
  ],
  neutre: [
    "Ça va, une journée comme une autre.",
    "Prends bien soin de toi.",
    "Chaque jour ne se ressemble pas, c'est ok."
  ],
  pas_content: [
    "Courage, ça va aller mieux.",
    "Prends un moment pour toi, c'est important.",
    "Tes amis sont là si besoin, bon courage."
  ]
};

// fréquences différentes par humeur pour un feedback sonore simple, sans fichiers audio
const frequencies = {
  content: 660,
  neutre: 440,
  pas_content: 300
};

function playTone(frequency) {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const oscillator = ctx.createOscillator();
  const gain = ctx.createGain();

  oscillator.frequency.value = frequency;
  oscillator.connect(gain);
  gain.connect(ctx.destination);

  gain.gain.setValueAtTime(0.2, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);

  oscillator.start();
  oscillator.stop(ctx.currentTime + 0.4);
}

function randomMessage(mood) {
  const list = messages[mood];
  return list[Math.floor(Math.random() * list.length)];
}

const source = document.body.dataset.source || "web";

// TODO: brancher sur l'API réelle une fois le backend disponible (voir REQUIREMENTS.md)
async function sendVote(mood) {
  try {
    await fetch("/api/votes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ humeur: mood, source })
    });
  } catch (error) {
    console.log("Backend indisponible pour le moment, vote non envoyé :", mood);
  }
}

const feedback = document.getElementById("feedback");
let feedbackTimeout;

document.querySelectorAll(".mood-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const mood = button.dataset.mood;

    playTone(frequencies[mood]);
    feedback.textContent = randomMessage(mood);
    sendVote(mood);

    if (navigator.vibrate) {
      navigator.vibrate(30);
    }

    // remet l'écran à zéro après un délai, pour le prochain votant (surtout utile en mode kiosque)
    clearTimeout(feedbackTimeout);
    feedbackTimeout = setTimeout(() => {
      feedback.textContent = "";
    }, 4000);
  });
});
