const $guessForm = $("#guess-form");
const $guess = $("#guess");
const $body = $("body");
const $score = $("#score");
const $time = $("#time");
const $highScore = $("#high-score");
const $gamesPlayed = $("#games-played");

const BASE_URL = "http://127.0.0.1:5000";

class Game {
  constructor() {
    this.score = 0;
    this.validWordsGuessed = [];
    this.canPlay = 1;
    this.timer = 60;
  }

  message(msg) {
    if ($body.children("#message")) {
      $("#message").remove();
    }
    $body.append(`<p id="message">${msg}</p>`);
  }

  async send_result() {
    const highScore = await axios.post(`${BASE_URL}/result`, {
      score: this.score,
    });
    $highScore.text(`${highScore.data}`);
    $gamesPlayed.text(`${parseInt($gamesPlayed.text()) + 1}`);
  }

  async handleSubmit() {
    if (this.canPlay === 0) {
      return;
    }
    const guess = $guess.val();
    const res = await axios.get(`${BASE_URL}/guess?guess=${guess}`);
    this.message(`${guess} is ${res.data.result.replaceAll("-", " ")}`);
    if (res.data.result === "ok") {
      if (!this.validWordsGuessed.includes(guess.toLowerCase())) {
        this.validWordsGuessed.push(guess.toLowerCase());
        this.score += guess.length;
        $score.text(`${this.score}`);
      } else {
        this.message(`${guess} has already been guessed!`);
      }
    }
    $guess.val("");
  }
}

game = new Game();

const timerInterval = setInterval(async () => {
  game.timer -= 1;
  $time.text(`${game.timer}`);
  if (game.timer === 0) {
    game.canPlay = 0;
    clearInterval(timerInterval);
    game.message(`Time is up! Your final score is ${game.score}!`);
    game.send_result();
  }
}, 1000);

$guessForm.on("submit", async (event) => {
  event.preventDefault();
  game.handleSubmit();
});
