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

// un seul AudioContext réutilisé : en créer un nouveau à chaque clic sans le fermer
// épuise la limite de contextes simultanés du navigateur (ex. 6 sur Chrome) au bout de quelques votes
let audioCtx;

function playTone(frequency) {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  const ctx = audioCtx;
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

async function sendVote(mood) {
  const response = await fetch("/api/votes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ humeur: mood, source })
  });

  if (!response.ok) {
    throw new Error(`Erreur serveur (${response.status})`);
  }
}

const feedback = document.getElementById("feedback");
let feedbackTimeout;

document.querySelectorAll(".mood-btn").forEach((button) => {
  button.addEventListener("click", async () => {
    const mood = button.dataset.mood;

    try {
      playTone(frequencies[mood]);
    } catch (error) {
      console.log("Son non joué :", error);
    }

    if (navigator.vibrate) {
      navigator.vibrate(30);
    }

    try {
      await sendVote(mood);
      feedback.classList.remove("feedback-error");
      feedback.textContent = randomMessage(mood);
    } catch (error) {
      console.log("Vote non enregistré :", mood, error);
      feedback.classList.add("feedback-error");
      feedback.textContent = "Oups, ton vote n'a pas pu être envoyé. Réessaie dans un instant.";
    }

    // remet l'écran à zéro après un délai, pour le prochain votant (surtout utile en mode kiosque)
    clearTimeout(feedbackTimeout);
    feedbackTimeout = setTimeout(() => {
      feedback.textContent = "";
      feedback.classList.remove("feedback-error");
    }, 4000);
  });
});
