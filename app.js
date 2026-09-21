const gameKey = "big-fly-baseball";
const defaultState = { homeRuns: 0, fans: 0, coins: 25, streak: 0, level: 1, xp: 0, upgrades: { contact: 1, power: 1, stadium: 1 }, players: { griffey: false, jackie: false } };
let state = loadState();
state.level ??= 1;
state.xp ??= 0;
const $ = (selector) => document.querySelector(selector);
const pitchDuration = 1900;
let pitchStart = performance.now();
let pitchPhase = 0;
let lastSwingPitch = -1;
function loadState() { try { return { ...defaultState, ...JSON.parse(localStorage.getItem(gameKey)) }; } catch { return structuredClone(defaultState); } }
function saveState() { localStorage.setItem(gameKey, JSON.stringify(state)); }
function formatNumber(number) { return number.toLocaleString("en-US"); }
function upgradeCost(type) { return { contact: 10, power: 15, stadium: 20 }[type] * state.upgrades[type]; }
function xpToNextLevel() { return 20 + (state.level - 1) * 15; }
function addExperience(amount) { state.xp += amount; let leveledUp = false; while (state.xp >= xpToNextLevel()) { state.xp -= xpToNextLevel(); state.level += 1; state.coins += 10; state.fans += 25; leveledUp = true; } return leveledUp; }
function teamOverall() { const upgradePoints = Object.values(state.upgrades).reduce((total, level) => total + level - 1, 0) * 2; const playerPoints = (state.players.griffey ? 8 : 0) + (state.players.jackie ? 4 : 0); return 61 + upgradePoints + playerPoints; }
function render() {
  $("#home-runs").textContent = formatNumber(state.homeRuns); $("#fans").textContent = formatNumber(state.fans); $("#coins").textContent = formatNumber(state.coins); $("#team-ovr").textContent = teamOverall(); $("#streak-label").textContent = `${state.streak} HR streak`; $("#roster-count").textContent = `${1 + Object.values(state.players).filter(Boolean).length} / 3`;
  $("#season-level").textContent = state.level; $("#season-progress-text").textContent = `${state.xp} / ${xpToNextLevel()} XP`; $("#season-progress-fill").style.width = `${Math.min(100, (state.xp / xpToNextLevel()) * 100)}%`;
  ["contact", "power", "stadium"].forEach((type) => { const level = state.upgrades[type]; $(`#${type}-level`).textContent = level; $(`#${type}-cost`).textContent = upgradeCost(type); $(`#${type}-bar`).style.width = `${Math.min(100, level * 20)}%`; const button = $(`[data-upgrade="${type}"]`); button.disabled = state.coins < upgradeCost(type); button.setAttribute("aria-label", `Upgrade ${type} for ${upgradeCost(type)} coins`); });
  ["griffey", "jackie"].forEach((player) => { const button = $(`[data-player="${player}"]`); if (state.players[player]) { button.textContent = "SIGNED"; button.disabled = true; } else { button.textContent = player === "griffey" ? "$80" : "$100"; button.disabled = state.coins < Number(button.textContent.replace("$", "")); } });
}
function animatePitch(now) {
  pitchPhase = ((now - pitchStart) % pitchDuration) / pitchDuration;
  const windowStart = Math.max(.5, .68 - state.upgrades.contact * .025);
  const windowEnd = Math.min(.94, .82 + state.upgrades.contact * .02);
  const inWindow = pitchPhase >= windowStart && pitchPhase <= windowEnd;
  $("#pitch-meter-fill").style.width = `${pitchPhase * 100}%`;
  $(".pitch-meter").style.setProperty("--zone-left", `${windowStart * 100}%`);
  $(".pitch-meter").style.setProperty("--zone-right", `${(1 - windowEnd) * 100}%`);
  $("#ball").style.setProperty("--pitch-progress", pitchPhase);
  $(".timing-guide").classList.toggle("in-zone", inWindow);
  $("#pitch-message").textContent = inWindow ? "SWING NOW" : "WATCH THE PITCH";
  window.requestAnimationFrame(animatePitch);
}
function swing() {
  const pitchAtSwing = Math.floor((performance.now() - pitchStart) / pitchDuration);
  if (pitchAtSwing === lastSwingPitch) {
    $("#play-by-play").textContent = "Wait for the next pitch.";
    $("#multiplier").textContent = "Next pitch loading";
    return;
  }
  lastSwingPitch = pitchAtSwing;
  pitchPhase = ((performance.now() - pitchStart) % pitchDuration) / pitchDuration;
  const power = state.upgrades.power; const contact = state.upgrades.contact; const windowStart = Math.max(.5, .68 - contact * .025); const windowEnd = Math.min(.94, .82 + contact * .02); const wellTimed = pitchPhase >= windowStart && pitchPhase <= windowEnd; const early = pitchPhase < windowStart; const isHomer = wellTimed && Math.random() < Math.min(.98, .62 + contact * .08); const distance = 320 + Math.floor(Math.random() * 90) + power * 24 + (state.players.griffey ? 25 : 0); const earnedCoins = isHomer ? 2 + Math.floor(power / 2) : 0; const earnedFans = isHomer ? 8 + state.upgrades.stadium * 3 + (state.players.jackie ? 6 : 0) : 1;
  const timingCenter = (windowStart + windowEnd) / 2; const perfect = isHomer && Math.abs(pitchPhase - timingCenter) <= (windowEnd - windowStart) * .2; const bonusCoins = perfect ? 2 : 0; const bonusFans = perfect ? 5 : 0;
  const xpEarned = isHomer ? (perfect ? 12 : 8) : 1; const leveledUp = addExperience(xpEarned); const resultMessage = leveledUp ? `LEVEL UP! Welcome to level ${state.level}.` : (perfect ? `PERFECT CONTACT! ${distance} feet and gone.` : (isHomer ? `CRACK! ${distance} feet and gone.` : (early ? "Too early. Let the pitch travel." : "Too late. Watch it into the mitt.")));
  state.homeRuns += isHomer ? 1 : 0; state.streak = isHomer ? state.streak + 1 : 0; state.coins += earnedCoins + bonusCoins; state.fans += earnedFans + bonusFans; $("#last-distance").textContent = isHomer ? distance : "MISS"; $("#play-by-play").textContent = resultMessage; $("#multiplier").textContent = isHomer ? `+${earnedCoins + bonusCoins} coins · +${earnedFans + bonusFans} fans · +${xpEarned} XP` : `+${xpEarned} XP`;
  $(".diamond-panel").classList.remove("hit"); void $(".diamond-panel").offsetWidth; $(".diamond-panel").classList.add("hit"); $(".field").classList.remove("swinging"); void $(".field").offsetWidth; $(".field").classList.add("swinging"); window.setTimeout(() => $(".field").classList.remove("swinging"), 720); $("#ball").classList.remove("fly"); void $("#ball").offsetWidth; $("#ball").classList.add("fly"); saveState(); render();
}
function buyUpgrade(event) { const type = event.currentTarget.dataset.upgrade; const cost = upgradeCost(type); if (state.coins < cost) return; state.coins -= cost; state.upgrades[type] += 1; saveState(); render(); }
function signPlayer(event) { const player = event.currentTarget.dataset.player; const cost = player === "griffey" ? 80 : 100; if (state.players[player] || state.coins < cost) return; state.coins -= cost; state.players[player] = true; saveState(); render(); }
$("#swing-button").addEventListener("click", swing); document.addEventListener("keydown", (event) => { if (event.code === "Space" && event.target.tagName !== "BUTTON") { event.preventDefault(); swing(); } }); document.querySelectorAll(".upgrade-button").forEach((button) => button.addEventListener("click", buyUpgrade)); document.querySelectorAll(".sign-button").forEach((button) => button.addEventListener("click", signPlayer));
$("#reset-game").addEventListener("click", () => { if (!window.confirm("Reset your season and start over?")) return; state = structuredClone(defaultState); saveState(); render(); });
render();
window.requestAnimationFrame(animatePitch);
