const gameKey = "big-fly-baseball";
const defaultState = { homeRuns: 0, fans: 0, coins: 25, streak: 0, upgrades: { contact: 1, power: 1, stadium: 1 }, players: { griffey: false, jackie: false } };
let state = loadState();
const $ = (selector) => document.querySelector(selector);
function loadState() { try { return { ...defaultState, ...JSON.parse(localStorage.getItem(gameKey)) }; } catch { return structuredClone(defaultState); } }
function saveState() { localStorage.setItem(gameKey, JSON.stringify(state)); }
function formatNumber(number) { return number.toLocaleString("en-US"); }
function upgradeCost(type) { return { contact: 10, power: 15, stadium: 20 }[type] * state.upgrades[type]; }
function teamOverall() { const upgradePoints = Object.values(state.upgrades).reduce((total, level) => total + level - 1, 0) * 2; const playerPoints = (state.players.griffey ? 8 : 0) + (state.players.jackie ? 4 : 0); return 61 + upgradePoints + playerPoints; }
function render() {
  $("#home-runs").textContent = formatNumber(state.homeRuns); $("#fans").textContent = formatNumber(state.fans); $("#coins").textContent = formatNumber(state.coins); $("#team-ovr").textContent = teamOverall(); $("#streak-label").textContent = `${state.streak} HR streak`; $("#roster-count").textContent = `${1 + Object.values(state.players).filter(Boolean).length} / 3`;
  ["contact", "power", "stadium"].forEach((type) => { const level = state.upgrades[type]; $(`#${type}-level`).textContent = level; $(`#${type}-cost`).textContent = upgradeCost(type); $(`#${type}-bar`).style.width = `${Math.min(100, level * 20)}%`; const button = $(`[data-upgrade="${type}"]`); button.disabled = state.coins < upgradeCost(type); button.setAttribute("aria-label", `Upgrade ${type} for ${upgradeCost(type)} coins`); });
  ["griffey", "jackie"].forEach((player) => { const button = $(`[data-player="${player}"]`); if (state.players[player]) { button.textContent = "SIGNED"; button.disabled = true; } else { button.textContent = player === "griffey" ? "$80" : "$100"; button.disabled = state.coins < Number(button.textContent.replace("$", "")); } });
}
function swing() {
  const power = state.upgrades.power; const contact = state.upgrades.contact; const isHomer = Math.random() < Math.min(.98, .62 + contact * .08); const distance = 320 + Math.floor(Math.random() * 90) + power * 24 + (state.players.griffey ? 25 : 0); const earnedCoins = isHomer ? 2 + Math.floor(power / 2) : 0; const earnedFans = isHomer ? 8 + state.upgrades.stadium * 3 + (state.players.jackie ? 6 : 0) : 1;
  state.homeRuns += isHomer ? 1 : 0; state.streak = isHomer ? state.streak + 1 : 0; state.coins += earnedCoins; state.fans += earnedFans; $("#last-distance").textContent = isHomer ? distance : "FOUL"; $("#play-by-play").textContent = isHomer ? `CRACK! ${distance} feet and gone.` : "Just missed it. Keep your eye on the ball."; $("#multiplier").textContent = isHomer ? `+${earnedCoins} coins · +${earnedFans} fans` : "+1 fan";
  $(".diamond-panel").classList.remove("hit"); void $(".diamond-panel").offsetWidth; $(".diamond-panel").classList.add("hit"); $("#ball").classList.remove("fly"); void $("#ball").offsetWidth; $("#ball").classList.add("fly"); saveState(); render();
}
function buyUpgrade(event) { const type = event.currentTarget.dataset.upgrade; const cost = upgradeCost(type); if (state.coins < cost) return; state.coins -= cost; state.upgrades[type] += 1; saveState(); render(); }
function signPlayer(event) { const player = event.currentTarget.dataset.player; const cost = player === "griffey" ? 80 : 100; if (state.players[player] || state.coins < cost) return; state.coins -= cost; state.players[player] = true; saveState(); render(); }
$("#swing-button").addEventListener("click", swing); document.addEventListener("keydown", (event) => { if (event.code === "Space" && event.target.tagName !== "BUTTON") { event.preventDefault(); swing(); } }); document.querySelectorAll(".upgrade-button").forEach((button) => button.addEventListener("click", buyUpgrade)); document.querySelectorAll(".sign-button").forEach((button) => button.addEventListener("click", signPlayer));
$("#reset-game").addEventListener("click", () => { if (!window.confirm("Reset your season and start over?")) return; state = structuredClone(defaultState); saveState(); render(); });
render();
